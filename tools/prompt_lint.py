#!/usr/bin/env python3
"""prompt_lint — verifies the structural contracts of this kit.

The prompt is a document, so its quality is mostly a matter of judgement. What *can* be
verified mechanically is that the document is complete, paired with its translation, free of
unresolved placeholders and consistent with the changelog. That is what this tool does.

    python tools/prompt_lint.py [--root .] [--json] [--quiet]

Exit codes: 0 clean, 1 findings at error level, 2 usage problem.
Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2
MODULE_IDS = [f"M{n}" for n in range(0, 14)]
REQUIRED_FRONT_MATTER = ("id", "version", "title", "language", "portable", "requires")
INVARIANT_COUNT = 10
GATE_ITEMS = 12
EXPERIENCE_MARKERS = {
    "PROMPT.md": ("## M13 — ", "Experience Store", "applicability", "last_verified_at"),
    "PROMPT.ru.md": ("## M13 — ", "хранилище опыта", "применимост", "last_verified_at"),
}
SKIP_FILES = {"_Sidebar.md", "_Footer.md"}

SECRET_PATTERNS = [
    ("github-token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----")),
]
ABS_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[\\/]{1,2}Users[\\/]{1,2}[^\\/\s`'\"]+"),
    re.compile(r"(?<![\w.])/(?:home|Users)/[a-z0-9._-]+/", re.IGNORECASE),
]

findings: list[tuple[str, str, str, int, str]] = []   # level, rule, path, line, message


def add(level: str, rule: str, message: str, path: str = "", line: int = 0) -> None:
    findings.append((level, rule, path, line, message))


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n")


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    block = text[4:].split("\n---", 1)[0]
    data: dict[str, str] = {}
    for line in block.split("\n"):
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip('"')
    return data


def modules(text: str) -> list[str]:
    return re.findall(r"^## (M\d+) — ", text, flags=re.MULTILINE)


def check_front_matter(root: Path) -> None:
    for name in ("PROMPT.md", "PROMPT.ru.md"):
        path = root / name
        if not path.exists():
            add("error", "prompt.missing", f"{name} is absent")
            continue
        data = front_matter(read(path))
        if not data:
            add("error", "prompt.front-matter", "no YAML front matter", name, 1)
            continue
        for key in REQUIRED_FRONT_MATTER:
            if not data.get(key):
                add("error", "prompt.front-matter", f"front matter key '{key}' is missing or empty", name, 1)
        if data.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
            add("error", "prompt.version", f"version '{data['version']}' is not semantic", name, 1)


def check_modules(root: Path) -> None:
    english = root / "PROMPT.md"
    russian = root / "PROMPT.ru.md"
    if not english.exists():
        return
    en_text = read(english)
    en_modules = modules(en_text)
    if en_modules != MODULE_IDS:
        missing = [m for m in MODULE_IDS if m not in en_modules]
        extra = [m for m in en_modules if m not in MODULE_IDS]
        add("error", "prompt.modules",
            f"module sequence is wrong; missing {missing or 'none'}, unexpected {extra or 'none'}",
            "PROMPT.md")
    if len(set(en_modules)) != len(en_modules):
        add("error", "prompt.modules", "a module identifier is repeated", "PROMPT.md")
    checks = len(re.findall(r"^\*\*Check:\*\*", en_text, flags=re.MULTILINE))
    if checks != len(MODULE_IDS):
        add("error", "prompt.check-lines",
            f"{checks} 'Check:' lines for {len(MODULE_IDS)} modules", "PROMPT.md")
    if "## Invariants" not in en_text:
        add("error", "prompt.invariants", "the Invariants section is absent", "PROMPT.md")
    else:
        block = en_text.split("## Invariants", 1)[1].split("\n## ", 1)[0]
        numbered = len(re.findall(r"^\d+\. ", block, flags=re.MULTILINE))
        if numbered != INVARIANT_COUNT:
            add("error", "prompt.invariants",
                f"{numbered} invariants, expected {INVARIANT_COUNT}", "PROMPT.md")

    if russian.exists():
        ru_modules = modules(read(russian))
        if set(ru_modules) != set(en_modules):
            add("error", "prompt.translation",
                "the translation does not carry the same module identifiers: "
                f"missing {sorted(set(en_modules) - set(ru_modules))}, "
                f"extra {sorted(set(ru_modules) - set(en_modules))}", "PROMPT.ru.md")


def check_experience_module(root: Path) -> None:
    """M13 is the module whose absence is invisible: the prompt still reads as complete without it."""
    for name in ("PROMPT.md", "PROMPT.ru.md"):
        path = root / name
        if not path.exists():
            continue
        text = read(path)
        for marker in EXPERIENCE_MARKERS.get(name, ()):
            if marker not in text:
                add("error", "prompt.experience", f"M13 is incomplete: '{marker}' not found", name)
        gate = re.search(r"## M8 .*?(?=\n## )", text, flags=re.DOTALL)
        if gate:
            rows = len(re.findall(r"^\| \d+ \| ", gate.group(0), flags=re.MULTILINE))
            if rows != GATE_ITEMS:
                add("error", "prompt.gate",
                    f"the quality gate lists {rows} items, expected {GATE_ITEMS}", name)
    tool = root / "tools" / "experience.py"
    if not tool.exists():
        add("error", "experience.tool", "tools/experience.py is absent; M13 promises a store and a command")
        return
    if not (root / "memory" / "README.md").exists():
        add("error", "experience.store", "memory/README.md is absent; the store has no documented home")
    for pair in ("SKILL.md", "SKILL.ru.md", "docs/INSTALL.md", "docs/INSTALL.ru.md"):
        if not (root / pair).exists():
            add("error", "skill.entry", f"{pair} is absent; users install the kit through it")
    skill = root / "skills" / "experience-reuse" / "SKILL.md"
    if not skill.exists():
        add("error", "experience.skill", "skills/experience-reuse/SKILL.md is absent")
        return
    body = read(skill)
    for needle in ("## Applicability checklist", "## Record templates", "## Security and privacy"):
        if needle not in body:
            add("error", "experience.skill", f"the skill lacks '{needle}'", "skills/experience-reuse/SKILL.md")


def check_pairs(root: Path) -> None:
    markdown = [p for p in root.rglob("*.md")
                if ".git" not in p.parts and p.name not in SKIP_FILES]
    for path in sorted(markdown):
        relative = path.relative_to(root).as_posix()
        if "." in path.stem and path.stem.endswith(".ru"):
            twin = path.with_name(path.name.replace(".ru.md", ".md"))
            if not twin.exists():
                add("error", "pairs.orphan-translation",
                    f"{relative} has no English original", relative)
            continue
        twin = path.with_name(path.stem + ".ru.md")
        if not twin.exists():
            add("error", "pairs.missing-translation",
                f"{relative} has no Russian version ({twin.name})", relative)


def check_language_direction(root: Path) -> None:
    """A file named .ru.md must be Russian and its canonical twin must be English.

    The pairing rule alone only checks that both files exist. Two files with swapped contents pass it
    silently — measured on this repository, where SKILL.md held the Russian text and SKILL.ru.md the
    English one. Proportions are measured on prose only: code, inline code and URLs carry no language.
    """
    cyrillic = re.compile(r"[А-Яа-яЁё]")
    latin = re.compile(r"[A-Za-z]")

    def share(text: str) -> float | None:
        prose = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`]*`", " ", prose)
        prose = re.sub(r"https?://\S+", " ", prose)
        cyr, lat = len(cyrillic.findall(prose)), len(latin.findall(prose))
        if cyr + lat < 200:          # too little prose to judge
            return None
        return cyr / (cyr + lat)

    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".ghagent"} for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        ratio = share(read(path))
        if ratio is None:
            continue
        if path.name.endswith(".ru.md"):
            if ratio < 0.20:
                add("error", "language.direction",
                    f"a .ru.md file is only {ratio:.0%} Cyrillic: it holds English text", relative)
        elif ratio > 0.05:
            add("error", "language.direction",
                f"the canonical file is {ratio:.0%} Cyrillic: it holds Russian text — swap it with its twin",
                relative)


def check_wiki_counts(root: Path) -> None:
    """Wiki pages restate numbers from the prompt, so they drift silently. Compare them.

    Measured drift: the English wiki said "Nine rules" while the prompt had ten, and the Russian page
    claimed ten while listing nine. Nothing else in the kit compares a page against M8 or the
    invariants section.
    """
    prompt = root / "PROMPT.md"
    wiki = root / "wiki"
    if not prompt.exists() or not wiki.is_dir():
        return
    text = read(prompt)
    gate = re.search(r"## M8 .*?(?=\n## )", text, flags=re.DOTALL)
    gate_rows = len(re.findall(r"^\| \d+ \| ", gate.group(0), flags=re.MULTILINE)) if gate else 0
    invariants = (len(re.findall(r"^\d+\. ", text.split("## Invariants", 1)[1], flags=re.MULTILINE))
                  if "## Invariants" in text else 0)

    numbers = {9: ("nine", "девять"), 10: ("ten", "десять"), 11: ("eleven", "одиннадцать"),
               12: ("twelve", "двенадцать"), 13: ("thirteen", "тринадцать")}
    by_word = {word: number for number, pair in numbers.items() for word in pair}

    patterns = (
        # "Nine rules never change" / "Ten rules never change"
        (re.compile(r"\b(nine|ten|eleven|twelve|thirteen|девять|десять|одиннадцать|двенадцать|тринадцать)"
                    r"\s+(?:rules never change|правил(?:а)? не меня(?:ются|ется))", re.IGNORECASE),
         "invariants", invariants),
        # "twelve-item gate" / "ворота из двенадцати проверок"
        (re.compile(r"\b(nine|ten|eleven|twelve|thirteen)-item gate", re.IGNORECASE), "gate", gate_rows),
        (re.compile(r"ворот[аы]?\s+из\s+(девяти|десяти|одиннадцати|двенадцати|тринадцати)\s+провер", re.IGNORECASE),
         "gate", gate_rows),
    )

    for path in sorted(wiki.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        body = read(path)
        relative = path.relative_to(root).as_posix()
        for pattern, kind, actual in patterns:
            for match in pattern.finditer(body):
                word = match.group(1).lower()
                stated = by_word.get(word)
                if stated is None or actual == 0 or stated == actual:
                    continue
                add("error", "wiki.drift",
                    f"the page states {stated} {kind}, PROMPT.md has {actual}", relative)


def check_text(root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        text = read(path)
        if "\r\n" in path.read_bytes().decode("utf-8", errors="replace"):
            add("error", "text.crlf", "CRLF line endings", relative, 1)
        if path.read_bytes().startswith(b"\xef\xbb\xbf"):
            add("error", "text.bom", "file starts with a BOM", relative, 1)
        for name, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                add("error", "privacy.secret", f"{name} literal", relative,
                    text.count("\n", 0, match.start()) + 1)
        for pattern in ABS_PATH_PATTERNS:
            for match in pattern.finditer(text):
                add("error", "privacy.abs-path", "absolute machine path", relative,
                    text.count("\n", 0, match.start()) + 1)
        # placeholders are allowed inside fenced blocks and inline code only
        outside = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        outside = re.sub(r"``[^`]*``|`[^`]*`", "", outside)
        for match in re.finditer(r"\{\{[^}]*\}\}", outside):
            add("error", "prompt.placeholder", "unresolved {{placeholder}} outside a code fence",
                relative, outside.count("\n", 0, match.start()) + 1)


def check_changelog(root: Path) -> None:
    changelog = root / "CHANGELOG.md"
    prompt = root / "PROMPT.md"
    if not changelog.exists() or not prompt.exists():
        return
    versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", read(changelog), flags=re.MULTILINE)
    declared = front_matter(read(prompt)).get("version", "")
    if not versions:
        add("error", "changelog.versions", "no version headings in CHANGELOG.md", "CHANGELOG.md")
        return
    if declared and versions[0] != declared:
        add("error", "changelog.version",
            f"CHANGELOG.md starts at {versions[0]}, PROMPT.md declares {declared}", "CHANGELOG.md")
    if read(changelog).count("Keep a Changelog") == 0:
        add("warn", "changelog.format", "the preamble does not name the format", "CHANGELOG.md")


def check_cross_references(root: Path) -> None:
    prompt = root / "PROMPT.md"
    if not prompt.exists():
        return
    known = set(modules(read(prompt)))
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts or path.name.startswith("PROMPT"):
            continue
        relative = path.relative_to(root).as_posix()
        for match in re.finditer(r"\bM(\d{1,2})\b", read(path)):
            identifier = f"M{match.group(1)}"
            if identifier not in known:
                add("error", "prompt.dangling-reference",
                    f"{identifier} is referenced but not defined in PROMPT.md", relative, 1)


def check_links(root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        text = read(path)
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if any(token in target for token in ("<", ">", "{{")):
                continue
            candidate = (path.parent / target.split("#", 1)[0]).resolve()
            if not candidate.exists():
                # wiki pages are addressed without an extension, and translations
                # are addressed with a language suffix: 01-Usage and Home.ru
                if "wiki" in path.parts and path.suffix == ".md":
                    stem = path.parent / target.split("#", 1)[0]
                    if stem.with_suffix(".md").exists() or Path(str(stem) + ".md").exists():
                        continue
                add("error", "link.missing", f"link target does not exist: {target}", relative,
                    text.count("\n", 0, match.start()) + 1)


def check_workflow(root: Path) -> None:
    workflow = root / ".github" / "workflows" / "lint.yml"
    if not workflow.exists():
        add("warn", "ci.missing", "no workflow runs the lint", ".github/workflows")
        return
    if "prompt_lint.py" not in read(workflow):
        add("warn", "ci.not-wired", "the workflow does not run tools/prompt_lint.py", str(workflow))


def main(argv: list[str]) -> int:
    root = Path(".")
    as_json = "--json" in argv
    quiet = "--quiet" in argv
    if "--root" in argv:
        index = argv.index("--root")
        if index + 1 >= len(argv):
            print("prompt_lint: --root needs a path", file=sys.stderr)
            return EXIT_USAGE
        root = Path(argv[index + 1])
    if not root.is_dir():
        print(f"prompt_lint: not a directory: {root}", file=sys.stderr)
        return EXIT_USAGE
    if not (root / "PROMPT.md").exists():
        print(f"prompt_lint: no PROMPT.md under {root}", file=sys.stderr)
        return EXIT_USAGE

    check_front_matter(root)
    check_modules(root)
    check_experience_module(root)
    check_pairs(root)
    check_language_direction(root)
    check_wiki_counts(root)
    check_text(root)
    check_changelog(root)
    check_cross_references(root)
    check_links(root)
    check_workflow(root)

    errors = [f for f in findings if f[0] == "error"]
    warnings = [f for f in findings if f[0] == "warn"]
    if as_json:
        print(json.dumps({
            "root": str(root),
            "counts": {"error": len(errors), "warn": len(warnings)},
            "findings": [{"level": l, "rule": r, "path": p, "line": n, "message": m}
                         for l, r, p, n, m in findings],
        }, ensure_ascii=False, indent=2))
    elif not quiet or errors:
        for level, rule, path, line, message in findings:
            location = f"{path}:{line}" if line else (path or "-")
            print(f"[{level.upper():5}] {rule:26} {location}  {message}")
        verdict = "FAIL" if errors else ("WARN" if warnings else "PASS")
        print(f"{verdict}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return EXIT_FAIL if errors else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
