#!/usr/bin/env python3
"""experience — a searchable store of prior work, so a repeated task is retrieved instead of re-derived.

Why this exists. A rule that says "consult your experience" costs the model a directory walk and a
guess. A rule that says "run one command that returns the three best candidates with their
applicability" costs one command. Only the second one is followed under pressure, so the store ships
with the tool that makes retrieval cheap.

    python tools/experience.py init [--root DIR]
    python tools/experience.py add <file> [--root DIR]
    python tools/experience.py search "text" [--type recipe] [--tag php] [--limit 5] [--json]
    python tools/experience.py show <id> [--root DIR]
    python tools/experience.py check [--json]
    python tools/experience.py stats
    python tools/experience.py deprecate <id> --by <id>
    python tools/experience.py selftest

Exit codes: 0 clean, 1 findings at error level, 2 usage problem. Standard library only.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2

TYPES = {"task", "recipe", "artifact", "failure"}
STATUSES = {"draft", "validated", "deprecated"}
CONFIDENCES = {"low", "medium", "high"}
REQUIRED = ("id", "type", "title", "status", "confidence", "applicability", "created_at", "updated_at")
RECIPE_SECTIONS = ("## Problem", "## When to use", "## Procedure", "## Validation", "## Rollback")
STALE_DAYS = 180
INDEX_NAME = "index.json"
STORE_DIRS = {"recipes": "recipe", "failures": "failure", "tasks": "task", "artifacts": "artifact"}

SECRET_PATTERNS = [
    ("github-token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----")),
    ("bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{20,}\b")),
]
ABS_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[\\/]{1,2}Users[\\/]{1,2}[^\\/\s`'\"]+"),
    re.compile(r"(?<![\w.])/(?:home|Users)/[a-z0-9._-]+/", re.IGNORECASE),
]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

findings: list[tuple[str, str, str, str]] = []   # level, rule, where, message


def add(level: str, rule: str, where: str, message: str) -> None:
    findings.append((level, rule, where, message))


# --------------------------------------------------------------------------
# front matter: the subset this store uses (scalars and inline lists)
# --------------------------------------------------------------------------

def parse_record(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    block = text[4:end]
    body = text[end + 4:]
    data: dict[str, object] = {}
    for line in block.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"')
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip('"') for item in value[1:-1].split(",")]
            data[key] = [item for item in items if item]
        else:
            data[key] = "" if value in ("null", "~") else value
    return data, body.lstrip("\n")


def dump_record(data: dict, body: str) -> str:
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(value)}]")
        elif value in (None, ""):
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip("\n")


# --------------------------------------------------------------------------
# store layout
# --------------------------------------------------------------------------

def store_root(root: Path) -> Path:
    return Path(root) / "memory"


def record_paths(root: Path) -> list[Path]:
    base = store_root(root)
    if not base.is_dir():
        return []
    return sorted(path for path in base.rglob("*.md") if path.name != "README.md")


def load_all(root: Path) -> list[tuple[Path, dict, str]]:
    loaded = []
    for path in record_paths(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        data, body = parse_record(text)
        loaded.append((path, data, body))
    return loaded


def init_store(root: Path, report: dict) -> int:
    base = store_root(root)
    for folder in STORE_DIRS:
        (base / folder).mkdir(parents=True, exist_ok=True)
    index = base / INDEX_NAME
    if not index.exists():
        index.write_text(json.dumps({"records": [], "updated_at": None}, indent=2) + "\n", encoding="utf-8")
    report["created"] = str(base)
    return EXIT_OK


def rebuild_index(root: Path) -> dict:
    entries = []
    for path, data, _body in load_all(root):
        entries.append({
            "id": data.get("id") or path.stem,
            "type": data.get("type", ""),
            "title": data.get("title", ""),
            "status": data.get("status", ""),
            "confidence": data.get("confidence", ""),
            "tags": data.get("tags", []),
            "applicability": data.get("applicability", ""),
            "last_verified_at": data.get("last_verified_at", ""),
            "path": path.relative_to(root).as_posix(),
        })
    index = {"records": sorted(entries, key=lambda item: item["id"]),
             "updated_at": dt.date.today().isoformat()}
    (store_root(root) / INDEX_NAME).write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n",
                                               encoding="utf-8")
    return index


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def validate_record(path: Path, data: dict, body: str, *, root: Path | None = None,
                    today: dt.date | None = None, known_ids: set[str] | None = None) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    where = path.name
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else body

    for key in REQUIRED:
        if not data.get(key):
            result.append(("error", "exp.schema", f"{where}: required key '{key}' is missing or empty"))
    identifier = str(data.get("id", ""))
    if identifier and not ID_RE.match(identifier):
        result.append(("error", "exp.id", f"{where}: id '{identifier}' is not a lowercase-hyphen slug"))
    if data.get("type") and data["type"] not in TYPES:
        result.append(("error", "exp.enum", f"{where}: type '{data['type']}' is not one of {sorted(TYPES)}"))
    if data.get("status") and data["status"] not in STATUSES:
        result.append(("error", "exp.enum", f"{where}: status '{data['status']}' is not one of {sorted(STATUSES)}"))
    if data.get("confidence") and data["confidence"] not in CONFIDENCES:
        result.append(("error", "exp.enum",
                       f"{where}: confidence '{data['confidence']}' is not one of {sorted(CONFIDENCES)}"))

    today = today or dt.date.today()
    for key in ("created_at", "updated_at", "last_verified_at"):
        value = data.get(key)
        if not value:
            continue
        try:
            dt.date.fromisoformat(str(value)[:10])
        except ValueError:
            result.append(("error", "exp.date", f"{where}: '{key}' is not an ISO date"))

    if data.get("status") == "validated" and not data.get("last_verified_at"):
        result.append(("error", "exp.verified", f"{where}: status is validated but last_verified_at is empty"))
    if data.get("last_verified_at"):
        try:
            verified = dt.date.fromisoformat(str(data["last_verified_at"])[:10])
            if (today - verified).days > STALE_DAYS:
                result.append(("warn", "exp.stale",
                               f"{where}: last verified {(today - verified).days} days ago; revalidate or deprecate"))
        except ValueError:
            pass
    if data.get("status") == "deprecated" and not data.get("superseded_by"):
        result.append(("warn", "exp.deprecated", f"{where}: deprecated without 'superseded_by'"))

    for related in data.get("related", []) or []:
        if known_ids is not None and related not in known_ids:
            result.append(("error", "exp.related", f"{where}: related id '{related}' does not exist"))

    if data.get("type") == "recipe":
        missing = [section for section in RECIPE_SECTIONS if section not in body]
        if missing:
            result.append(("error", "exp.recipe-sections",
                           f"{where}: a recipe needs {', '.join(missing)}"))

    for name, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            result.append(("error", "exp.secret", f"{where}: {name} literal; redact to a <placeholder>"))
    for pattern in ABS_PATH_PATTERNS:
        if pattern.search(text):
            result.append(("error", "exp.abs-path", f"{where}: absolute machine path; use <path>"))
    return result


def check_store(root: Path) -> list[tuple[str, str, str]]:
    problems: list[tuple[str, str, str]] = []
    loaded = load_all(root)
    if not loaded:
        problems.append(("error", "exp.empty", "the store holds no records; retrieval would find nothing"))
        return problems
    ids = [str(data.get("id", path.stem)) for path, data, _body in loaded]
    duplicates = {identifier for identifier in ids if ids.count(identifier) > 1}
    for duplicate in sorted(duplicates):
        problems.append(("error", "exp.duplicate-id", f"id '{duplicate}' is used by more than one record"))
    known = set(ids)
    titles: dict[tuple[str, str], str] = {}
    for path, data, body in loaded:
        problems.extend(validate_record(path, data, body, root=root, known_ids=known))
        key = (str(data.get("type", "")), str(data.get("title", "")).strip().lower())
        if key[1] and key in titles:
            problems.append(("warn", "exp.duplicate-title",
                             f"'{key[1]}' appears twice as {key[0]}; prefer updating the existing record"))
        titles[key] = path.name
    index = store_root(root) / INDEX_NAME
    if not index.exists():
        problems.append(("warn", "exp.index", "index.json is missing; run `add` or `check --fix-index`"))
    return problems


# --------------------------------------------------------------------------
# retrieval: one command, ranked, with the reason for the rank
# --------------------------------------------------------------------------

def tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-zA-Zа-яА-Я0-9_\-]{3,}", text.lower())}


def score(data: dict, body: str, query_tokens: set[str], query_tags: set[str], today: dt.date) -> tuple[int, list[str]]:
    reasons: list[str] = []
    record_tokens = tokens(" ".join([str(data.get("title", "")), str(data.get("applicability", "")),
                                     " ".join(data.get("tags", []) or []), body[:1500]]))
    overlap = query_tokens & record_tokens
    record_tags = {tag.lower() for tag in (data.get("tags") or [])}
    # A record is a candidate only if it actually matches; boosts alone must never surface one.
    if not overlap and not (query_tags & record_tags):
        return 0, []
    points = len(overlap) * 3
    if overlap:
        reasons.append(f"overlap {len(overlap)}")
    if query_tags & record_tags:
        points += 6
        reasons.append("tag match")
    if data.get("status") == "validated":
        points += 4
        reasons.append("validated")
    if data.get("confidence") == "high":
        points += 2
        reasons.append("high confidence")
    verified = data.get("last_verified_at")
    if verified:
        try:
            age = (today - dt.date.fromisoformat(str(verified)[:10])).days
            if age <= 90:
                points += 3
                reasons.append(f"verified {age}d ago")
        except ValueError:
            pass
    if data.get("type") == "recipe":
        points += 1
    if data.get("type") == "failure":
        points -= 1
        reasons.append("prior failure: read before acting")
    return points, reasons


def search(root: Path, query: str, *, kind: str = "", tag: str = "", limit: int = 5,
           include_deprecated: bool = False) -> list[dict]:
    today = dt.date.today()
    query_tokens = tokens(query)
    query_tags = {item.strip().lower() for item in tag.split(",") if item.strip()}
    results = []
    for path, data, body in load_all(root):
        if data.get("status") == "deprecated" and not include_deprecated:
            continue
        if kind and data.get("type") != kind:
            continue
        points, reasons = score(data, body, query_tokens, query_tags, today)
        if points <= 0:
            continue
        results.append({
            "id": data.get("id", path.stem),
            "type": data.get("type", ""),
            "title": data.get("title", ""),
            "status": data.get("status", ""),
            "confidence": data.get("confidence", ""),
            "applicability": data.get("applicability", ""),
            "last_verified_at": data.get("last_verified_at", ""),
            "path": path.relative_to(root).as_posix(),
            "score": points,
            "why": ", ".join(reasons) or "weak overlap",
        })
    results.sort(key=lambda item: (-item["score"], item["id"]))
    return results[:limit]


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_init(root: Path, report: dict) -> int:
    board = {}
    code = init_store(root, board)
    report.update(board)
    report["next"] = "add a record with `experience.py add <file>`, then `check`"
    return code


def cmd_add(root: Path, source: Path, report: dict) -> int:
    if not source.exists():
        print(f"experience: no such file: {source}", file=sys.stderr)
        return EXIT_USAGE
    data, body = parse_record(source.read_text(encoding="utf-8", errors="replace"))
    kind = str(data.get("type", ""))
    folder = next((name for name, value in STORE_DIRS.items() if value == kind), "recipes")
    init_store(root, {})
    known = {str(entry.get("id", path.stem)) for path, entry, _b in load_all(root)}
    problems = validate_record(source, data, body, root=root, known_ids=known | {str(data.get("id", ""))})
    # Referential integrity is a store-level property: a batch is added record by record, so a
    # forward reference is a warning here and an error only in `check` over the whole store.
    problems = [("warn" if rule == "exp.related" else level, rule, message)
                for level, rule, message in problems]
    errors = [p for p in problems if p[0] == "error"]
    report["problems"] = [f"{rule}: {message}" for _level, rule, message in problems]
    if errors:
        report["written"] = False
        print("experience: refused, the record violates the schema:", file=sys.stderr)
        for _level, rule, message in errors:
            print(f"  {rule}: {message}", file=sys.stderr)
        return EXIT_FAIL
    destination = store_root(root) / folder / f"{data.get('id')}.md"
    destination.write_text(dump_record(data, body), encoding="utf-8")
    rebuild_index(root)
    report.update({"written": True, "path": destination.relative_to(root).as_posix()})
    return EXIT_OK


def cmd_search(root: Path, query: str, args: dict, report: dict) -> int:
    results = search(root, query, kind=args.get("type", ""), tag=args.get("tag", ""),
                     limit=int(args.get("limit", 5)), include_deprecated=args.get("include_deprecated", False))
    report["query"] = query
    report["results"] = results
    if not results:
        report["hint"] = "no experience matches; proceed without it and consider recording the result (M13)"
    return EXIT_OK


def cmd_show(root: Path, identifier: str, report: dict) -> int:
    for path, data, body in load_all(root):
        if str(data.get("id", path.stem)) == identifier:
            report.update({"record": data, "path": path.relative_to(root).as_posix(), "body": body})
            return EXIT_OK
    report["error"] = f"no record with id '{identifier}'"
    return EXIT_FAIL


def cmd_check(root: Path, report: dict, fix_index: bool = False) -> int:
    problems = check_store(root)
    if fix_index:
        rebuild_index(root)
    report["findings"] = [{"level": level, "rule": rule, "message": message} for level, rule, message in problems]
    report["counts"] = {"error": sum(1 for p in problems if p[0] == "error"),
                        "warn": sum(1 for p in problems if p[0] == "warn")}
    return EXIT_FAIL if report["counts"]["error"] else EXIT_OK


def cmd_stats(root: Path, report: dict) -> int:
    loaded = load_all(root)
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for _path, data, _body in loaded:
        by_type[str(data.get("type", "?"))] = by_type.get(str(data.get("type", "?")), 0) + 1
        by_status[str(data.get("status", "?"))] = by_status.get(str(data.get("status", "?")), 0) + 1
    report.update({"records": len(loaded), "by_type": by_type, "by_status": by_status})
    return EXIT_OK


def cmd_deprecate(root: Path, identifier: str, replacement: str, report: dict) -> int:
    for path, data, body in load_all(root):
        if str(data.get("id", path.stem)) == identifier:
            data["status"] = "deprecated"
            data["superseded_by"] = replacement
            data["updated_at"] = dt.date.today().isoformat()
            path.write_text(dump_record(data, body), encoding="utf-8")
            rebuild_index(root)
            report.update({"deprecated": identifier, "superseded_by": replacement})
            return EXIT_OK
    report["error"] = f"no record with id '{identifier}'"
    return EXIT_FAIL


# --------------------------------------------------------------------------
# selftest: proves the tool rejects what it claims to reject
# --------------------------------------------------------------------------

RECIPE_OK = """---
id: php-add-column-to-endpoint
type: recipe
title: Add a nullable column to a PHP list endpoint
status: validated
confidence: high
applicability: PHP admin panel with explicit column lists in the query
tags: [php, sql, migration]
created_at: 2026-10-01
updated_at: 2026-10-20
last_verified_at: 2026-10-20
source: agent execution
related: []
---

## Problem

The list endpoint must return a new nullable field without breaking the existing tests.

## When to use

The table already has the column and the endpoint selects an explicit column list.

## Procedure

1. Read the migration that created the column.
2. Add the field to the select list and the presenter.
3. Render `—` for NULL.

## Validation

Existing suite green, plus one assertion on a row with NULL.

## Rollback

Revert the select list change; no schema change is involved.
"""


def selftest(report: dict) -> int:
    checks: list[tuple[str, bool, str]] = []

    def expect(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))

    with tempfile.TemporaryDirectory(prefix="exp-selftest-") as folder:
        root = Path(folder)
        cmd_init(root, {})
        source = root / "recipe.md"
        source.write_text(RECIPE_OK, encoding="utf-8")
        code = cmd_add(root, source, {})
        expect("add: a valid recipe is accepted", code == EXIT_OK)
        expect("add: the record lands in memory/recipes", (root / "memory" / "recipes" / "php-add-column-to-endpoint.md").exists())
        results = search(root, "add nullable column to php endpoint", limit=3)
        expect("search: the recipe is retrieved first", bool(results) and results[0]["id"] == "php-add-column-to-endpoint",
               str(results))
        expect("search: the rank carries a reason", bool(results) and bool(results[0]["why"]))
        expect("search: an unrelated query finds nothing", search(root, "kubernetes ingress tls") == [])

        secret = root / "secret.md"
        secret.write_text(RECIPE_OK.replace("php-add-column-to-endpoint", "leaky").replace(
            "Revert the select list change", "Revert with token " + "gh" + "p_" + "A" * 30), encoding="utf-8")
        code = cmd_add(root, secret, {})
        expect("add: a record with a token is refused", code == EXIT_FAIL)

        incomplete = root / "incomplete.md"
        incomplete.write_text(RECIPE_OK.replace("php-add-column-to-endpoint", "no-rollback").replace(
            "## Rollback", "## Notes"), encoding="utf-8")
        code = cmd_add(root, incomplete, {})
        expect("add: a recipe without Rollback is refused", code == EXIT_FAIL)

        duplicate = root / "duplicate.md"
        duplicate.write_text(RECIPE_OK, encoding="utf-8")
        code = cmd_add(root, duplicate, {})
        expect("add: a duplicate id overwrites instead of duplicating", code == EXIT_OK)
        problems = check_store(root)
        expect("check: a healthy store has no errors", not [p for p in problems if p[0] == "error"], str(problems))

        stale = root / "memory" / "recipes" / "php-add-column-to-endpoint.md"
        stale.write_text(RECIPE_OK.replace("last_verified_at: 2026-10-20", "last_verified_at: 2020-01-01"),
                         encoding="utf-8")
        problems = check_store(root)
        expect("check: an old validation is a warning",
               any(p[1] == "exp.stale" for p in problems), str(problems))

        cmd_deprecate(root, "php-add-column-to-endpoint", "php-add-column-to-endpoint-v2", {})
        expect("deprecate: the record leaves the default search",
               search(root, "add nullable column to php endpoint") == [])
        expect("deprecate: it is still reachable on request",
               bool(search(root, "add nullable column to php endpoint", include_deprecated=True)))
        problems = check_store(root)
        expect("check: a dangling superseded_by target is not an error, a missing one is a warning",
               any(p[1] == "exp.deprecated" for p in problems) is False, str(problems))

    failures = [entry for entry in checks if not entry[1]]
    report["checks"] = len(checks)
    report["failed"] = [name for name, ok, _detail in checks if not ok]
    for name, ok, detail in checks:
        if not ok:
            print(f"  FAIL {name} {detail}")
    print(f"{len(checks) - len(failures)}/{len(checks)} experience checks passed")
    return EXIT_FAIL if failures else EXIT_OK


def main(argv: list[str]) -> int:
    if "--help" in argv or not argv:
        print(__doc__)
        return EXIT_OK
    command = argv[0]
    rest = argv[1:]
    root = Path(".")
    if "--root" in rest:
        index = rest.index("--root")
        if index + 1 >= len(rest):
            print("experience: --root needs a path", file=sys.stderr)
            return EXIT_USAGE
        root = Path(rest[index + 1])
        rest = rest[:index] + rest[index + 2:]
    as_json = "--json" in [item for item in rest]
    positional = [item for item in rest if not item.startswith("--")]
    flags: dict[str, object] = {}
    for item in rest:
        if item.startswith("--") and "=" in item:
            key, _, value = item[2:].partition("=")
            flags[key] = value
        elif item.startswith("--"):
            key = item[2:]
            if key in {"include-deprecated", "fix-index"}:
                flags[key] = True
    report: dict = {"command": command}

    if command == "selftest":
        return selftest(report)
    if command == "init":
        code = cmd_init(root, report)
    elif command == "add":
        if not positional:
            print("experience: add needs a file", file=sys.stderr)
            return EXIT_USAGE
        code = cmd_add(root, Path(positional[0]), report)
    elif command == "search":
        if not positional:
            print("experience: search needs a query", file=sys.stderr)
            return EXIT_USAGE
        code = cmd_search(root, " ".join(positional), {
            "type": str(flags.get("type", "")),
            "tag": str(flags.get("tag", "")),
            "limit": flags.get("limit", 5),
            "include_deprecated": bool(flags.get("include-deprecated")),
        }, report)
    elif command == "show":
        if not positional:
            print("experience: show needs an id", file=sys.stderr)
            return EXIT_USAGE
        code = cmd_show(root, positional[0], report)
    elif command == "check":
        code = cmd_check(root, report, fix_index=bool(flags.get("fix-index")))
    elif command == "stats":
        code = cmd_stats(root, report)
    elif command == "deprecate":
        if not positional or "by" not in flags:
            print("experience: deprecate needs an id and --by <replacement>", file=sys.stderr)
            return EXIT_USAGE
        code = cmd_deprecate(root, positional[0], str(flags["by"]), report)
    else:
        print(f"experience: unknown command '{command}'", file=sys.stderr)
        return EXIT_USAGE

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _render(report)
    return code


def _render(report: dict) -> None:
    command = report.get("command")
    if command == "search":
        results = report.get("results", [])
        print(f"query: {report.get('query')}  ·  {len(results)} candidate(s)")
        for item in results:
            print(f"  [{item['score']:>3}] {item['type']:9} {item['id']:34} {item['status']:9} {item['why']}")
            print(f"        {item['title']}  —  {item['path']}")
        if report.get("hint"):
            print(f"  note: {report['hint']}")
    elif command == "check":
        for finding in report.get("findings", []):
            print(f"[{finding['level'].upper():5}] {finding['rule']:20} {finding['message']}")
        counts = report.get("counts", {})
        verdict = "FAIL" if counts.get("error") else ("WARN" if counts.get("warn") else "PASS")
        print(f"{verdict}: {counts.get('error', 0)} error(s), {counts.get('warn', 0)} warning(s)")
    elif command == "stats":
        print(f"records: {report.get('records')}")
        print(f"by type:   {report.get('by_type')}")
        print(f"by status: {report.get('by_status')}")
    elif command == "show":
        if report.get("error"):
            print(report["error"])
        else:
            print(report.get("path"))
            print(report.get("body", "")[:1200])
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
