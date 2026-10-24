#!/usr/bin/env python3
"""install — put the kit into a runtime's skill root, and tell the truth about what is left to do.

Three runtimes, three mechanisms, measured on 2026-10-24 (see docs/INSTALL.md):

    python tools/install.py --runtime autoclaw2 --check
    python tools/install.py --runtime autoclaw2 --write
    python tools/install.py --runtime harness  --write
    python tools/install.py --runtime saga                # prints what is unknown, refuses to guess

Exit codes: 0 success / check clean, 1 findings, 2 usage problem. Standard library only.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import shutil
import sys
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2

KIT_NAME = "agent-prompt-kit"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
RESERVED_COMMANDS = {"reload", "settings"}          # measured in AutoClaw2 main.cjs
MAX_COMMAND_BYTES = 256 * 1024                      # measured in AutoClaw2 main.cjs
SKIP_DIRS = {".git", ".ghagent", ".github", "assets", "__pycache__"}
SKIP_FILES = {".gitignore", ".gitattributes", ".editorconfig"}
# the kit's own surfaces that a skill copy does not need
SKIP_TOP = {"docs"}                                 # kept only when --with-docs is passed


def home() -> Path:
    return Path(os.environ.get("USERPROFILE") or Path.home())


def runtimes() -> dict[str, dict]:
    h = home()
    return {
        "autoclaw2": {
            "skills": h / ".pi" / "agent" / "skills",
            "prompts": h / ".pi" / "agent" / "prompts",
            "revisions": (Path(os.environ.get("APPDATA") or _roaming(h))) / "AutoClaw-oversea-official" / "accounts",
            "manual": "reload AutoClaw2 so the resource snapshot is rebuilt",
        },
        "harness": {
            "skills": h / ".dsh" / "skills",
            "prompts": None,
            "registry": h / ".dsh" / "storages" / "workspace.json",
            "manual": "in the left panel choose 'add workspace' and point it at the new environment directory",
        },
        "saga": {"skills": None, "prompts": None, "manual": "unknown: no verified mechanism recorded"},
    }


def _roaming(h: Path) -> Path:
    try:
        import ctypes
        buffer = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 26, None, 0, buffer)   # CSIDL_APPDATA
        return Path(buffer.value)
    except Exception:
        return h / "AppData" / "Roaming"


def front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    block = text[4:end] if end > 0 else ""
    out: dict[str, str] = {}
    for line in block.split("\n"):
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip().strip('"')
    return out


COMMAND_TEMPLATE = """---
description: "{description}"
argument-hint: "<тема или уточнение; пусто = взять из текущего диалога>"
---

Запусти навык `{skill}` по теме текущего диалога.

${{ARGUMENTS}}

1. Прочитай `{skill_md}` и действуй по нему: материал (эта сессия + индекс связанных сессий),
   карточка задачи и карточка домена, каталог нового окружения, шаг регистрации, стартовый промпт.
2. Результат — **каталог**, а не смена тона в этом окне.
3. Шаг, который может сделать только человек, назови явно и не изображай выполненным:
   {manual}.
4. Закончи строкой ворот: `ворота 12/12` или `ворота N/12 — провалы: <причины>`.
"""


def copy_tree(source: Path, target: Path, report: list[str], *, with_docs: bool) -> list[str]:
    """Copy the kit into the skill root. Never overwrite without a backup; never touch foreign files."""
    problems: list[str] = []
    target.mkdir(parents=True, exist_ok=True)
    for item in sorted(source.rglob("*")):
        if item.is_dir():
            continue
        relative = item.relative_to(source)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if item.name in SKIP_FILES:
            continue
        if relative.parts[0] in SKIP_TOP and not with_docs:
            continue
        destination = target / relative
        payload = item.read_bytes()
        if destination.exists():
            if destination.read_bytes() == payload:
                continue
            backup = destination.with_suffix(destination.suffix + ".bak-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
            backup.write_bytes(destination.read_bytes())
            report.append(f"backup  {destination.relative_to(target)}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        report.append(f"write   {destination.relative_to(target)}")
    return problems


def newest_manifest(accounts: Path) -> Path | None:
    found = sorted(accounts.glob("*/runtime/pi-resources/revisions/*/manifest.json"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    return found[0] if found else None


def check_autoclaw2(cfg: dict, report: list[str]) -> list[str]:
    problems: list[str] = []
    skill_dir = cfg["skills"] / KIT_NAME
    entry = skill_dir / "SKILL.md"
    if not entry.exists():
        problems.append(f"skill entry missing: {entry}")
    else:
        meta = front_matter(entry.read_text(encoding="utf-8", errors="replace"))
        if meta.get("name") != KIT_NAME:
            problems.append(f"SKILL.md name is '{meta.get('name')}', expected '{KIT_NAME}'")
        if not meta.get("description"):
            problems.append("SKILL.md has no description: the skill will never be selected")
    command = cfg["prompts"] / f"{KIT_NAME}.md"
    if not command.exists():
        problems.append(f"command file missing: {command}")
    else:
        if command.stat().st_size > MAX_COMMAND_BYTES:
            problems.append(f"command file is {command.stat().st_size} bytes, over 256 KB")
        if not front_matter(command.read_text(encoding="utf-8", errors="replace")).get("description"):
            problems.append("command file has no description")

    manifest = newest_manifest(cfg["revisions"])
    if manifest is None:
        problems.append("no resource-revision manifest found; start AutoClaw2 once")
        return problems
    import json
    data = json.loads(manifest.read_text(encoding="utf-8"))
    skills = {str(r.get("name")) for r in data.get("resources", []) if r.get("kind") == "skill"}
    prompts = {str(r.get("name")) for r in data.get("resources", []) if r.get("kind") == "prompt"}
    report.append(f"revision   {manifest.parent.name[:12]}…; skills {len(skills)}, prompts {len(prompts)}")
    if KIT_NAME not in skills:
        problems.append("skill not registered yet: reload AutoClaw2")
    if KIT_NAME not in prompts:
        problems.append("command not registered yet: reload AutoClaw2")
    return problems


def check_harness(cfg: dict, report: list[str]) -> list[str]:
    problems: list[str] = []
    entry = cfg["skills"] / KIT_NAME / "SKILL.md"
    if not entry.exists():
        problems.append(f"skill entry missing: {entry}")
    else:
        meta = front_matter(entry.read_text(encoding="utf-8", errors="replace"))
        if meta.get("name") != KIT_NAME:
            problems.append(f"SKILL.md name is '{meta.get('name')}', expected '{KIT_NAME}'")
        if not meta.get("description"):
            problems.append("SKILL.md has no description: /agent-prompt-kit will not resolve")
    registry = cfg["registry"]
    if not registry.exists():
        problems.append(f"workspace registry not found: {registry}")
    else:
        import json
        data = json.loads(registry.read_text(encoding="utf-8"))
        count = len(data.get("tables", {}).get("workspaces", {}))
        report.append(f"registry   {count} workspace(s) registered")
    problems.append("manual step: add the new environment directory as a workspace (left panel) — "
                    "until that click the directory is a folder, not a workspace")
    return problems


def main(argv: list[str]) -> int:
    if "--help" in argv or not argv:
        print(__doc__)
        return EXIT_OK
    runtime = ""
    if "--runtime" in argv:
        index = argv.index("--runtime")
        if index + 1 >= len(argv):
            print("install: --runtime needs a value", file=sys.stderr)
            return EXIT_USAGE
        runtime = argv[index + 1].lower()
    if runtime not in {"autoclaw2", "harness", "saga"}:
        print(f"install: unknown runtime '{runtime}'; use autoclaw2, harness or saga", file=sys.stderr)
        return EXIT_USAGE
    write = "--write" in argv
    with_docs = "--with-docs" in argv
    source = Path(__file__).resolve().parent.parent
    cfg = runtimes()[runtime]
    report: list[str] = []

    if runtime == "saga":
        print("SagaAI: no verified mechanism is recorded in this repository, so nothing is guessed.\n")
        print("Two questions to answer before installing:")
        print("  1. Where does SagaAI read skills or commands from? (path or API)")
        print("  2. Can it register a command or an agent without a human action?\n")
        print("Portable regardless of runtime: PROMPT.md as the operating contract, memory/ and")
        print("tools/experience.py (Python 3.11 and a directory are enough).")
        return EXIT_OK

    if not (source / "SKILL.md").exists():
        print(f"install: SKILL.md not found next to tools/ ({source})", file=sys.stderr)
        return EXIT_USAGE

    skill_dir = cfg["skills"] / KIT_NAME
    if write:
        copy_tree(source, skill_dir, report, with_docs=with_docs)
        if cfg.get("prompts"):
            cfg["prompts"].mkdir(parents=True, exist_ok=True)
            command = cfg["prompts"] / f"{KIT_NAME}.md"
            text = COMMAND_TEMPLATE.format(
                description="Из текущей сессии — в специализированное окружение: сессия и связанные, карточки, каталог Workspace, регистрация, стартовый промпт",
                skill=KIT_NAME,
                skill_md=skill_dir / "SKILL.ru.md",
                manual=cfg["manual"],
            )
            if command.exists() and command.read_bytes() == text.replace("\r\n", "\n").encode("utf-8"):
                report.append("unchanged command")
            else:
                if command.exists():
                    backup = command.with_suffix(".md.bak-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
                    backup.write_bytes(command.read_bytes())
                    report.append(f"backup  {backup.name}")
                command.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
                report.append(f"write   {command}")
        print("\n".join(report) or "nothing to do")
        print("")

    problems = check_autoclaw2(cfg, report) if runtime == "autoclaw2" else check_harness(cfg, report)
    for line in report:
        print(f"  {line}")
    print(f"\nskill root: {cfg['skills'] / KIT_NAME}")
    if cfg.get("prompts"):
        print(f"command:    /{KIT_NAME}  ({cfg['prompts'] / (KIT_NAME + '.md')})")
    blocking = [p for p in problems if not p.startswith("manual step")]
    manual = [p for p in problems if p.startswith("manual step")]
    if blocking:
        print("\nNOT READY:")
        for item in blocking:
            print(f"  - {item}")
    for item in manual:
        print(f"\n  {item}")
    if blocking:
        return EXIT_FAIL
    print(f"\nREADY ({runtime})" + ("" if not manual else " except the manual step above"))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
