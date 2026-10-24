"""External check of the published repository: fetch raw files, recompute, compare.

This mirrors what an independent reviewer does. It is deliberately separate from
tools/prompt_lint.py: the point is to verify the *published bytes*, not the local tree.
"""

import json
import re
import sys
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/paulmann/agent-prompt-kit/main/"
BASE = "https://github.com/paulmann/agent-prompt-kit"
API = "https://api.github.com/repos/paulmann/agent-prompt-kit/contents/"
findings = []


def fetch(name, binary=False):
    """Read the published file through the API, not the raw CDN.

    raw.githubusercontent.com serves a cached copy for minutes after a push, which makes an
    external check report findings that were already fixed. The contents API with an
    `application/vnd.github.raw` accept header answers from the repository itself.
    """
    request = urllib.request.Request(API + name, headers={
        "User-Agent": "external-check",
        "Accept": "application/vnd.github.raw",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
    except urllib.error.HTTPError:
        request = urllib.request.Request(RAW + name, headers={"User-Agent": "external-check"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
    return data if binary else data.decode("utf-8")


def add(rule, where, problem, fix):
    findings.append((rule, where, problem, fix))


def strip_inline(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    return text.strip()


def anchor(heading):
    text = strip_inline(heading).lower()
    kept = "".join(ch for ch in text if ch.isalnum() or ch in "-_ ")
    return kept.replace(" ", "-")


def anchors_of(text):
    seen, result = {}, []
    in_fence = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not match:
            continue
        base = anchor(match.group(2))
        if base in seen:
            seen[base] += 1
            base = f"{base}-{seen[base] - 1}"
        else:
            seen[base] = 1
        result.append((len(match.group(1)), base))
    return result


# 1. README contract
readme = fetch("README.md")
h1 = [line for line in readme.split("\n") if line.startswith("# ")]
if len(h1) != 1:
    add("readme.h1", "README.md", f"{len(h1)} H1 headings", "keep exactly one")
elif len(h1[0]) - 2 > 60:
    add("readme.title", "README.md:1", f"H1 is {len(h1[0]) - 2} characters", "shorten below 60")

lines = readme.split("\n")
title_at = next((i for i, line in enumerate(lines) if line.startswith("# ")), 0)
summary = next((line for line in lines[title_at + 1:] if line.strip()), "")
if not summary.startswith(("**", "[!", "<")):
    add("readme.summary", "README.md", f"summary starts with {summary[:20]!r}", "start with a bold sentence")

badges = len(re.findall(r"\[!\[[^\]]*\]\(https?://[^)]*\)\]\([^)]*\)", readme))
if not 3 <= badges <= 8:
    add("readme.badges", "README.md", f"{badges} badges", "3-8 badges")

known = {name for _level, name in anchors_of(readme)}
toc_links = re.findall(r"\]\(#([^)]+)\)", readme)
for target in toc_links:
    if target not in known:
        add("readme.toc", "README.md", f"anchor #{target} resolves to no heading", "fix the entry")
for heading in ("installation", "usage", "license"):
    if heading not in known:
        add("readme.section", "README.md", f"no '{heading}' section", f"add '## {heading.capitalize()}'")

def fences_without_language(text):
    """Count opening fences that carry no info string; closing fences are not fences."""
    pending, unlabelled = 0, 0
    for line in text.split("\n"):
        match = re.match(r"^```(\S*)", line)
        if not match:
            continue
        pending += 1
        if pending % 2 == 1 and not match.group(1):
            unlabelled += 1
    return unlabelled


fences = re.findall(r"^```(\w*)", readme, flags=re.MULTILINE)
unlabelled = fences_without_language(readme)
if unlabelled:
    add("readme.fence", "README.md", f"{unlabelled} opening fence(s) without a language", "add the language")

# 2. CHANGELOG contract
changelog = fetch("CHANGELOG.md")
allowed = {"Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"}
versions = re.findall(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})", changelog, flags=re.MULTILINE)
if not versions:
    add("changelog.versions", "CHANGELOG.md", "no dated version heading", "## [x.y.z] - YYYY-MM-DD")
if "[Unreleased]" not in changelog:
    add("changelog.unreleased", "CHANGELOG.md", "no Unreleased section", "add it above the newest version")
types = set(re.findall(r"^### (.+)$", changelog, flags=re.MULTILINE))
unknown = types - allowed
if unknown:
    add("changelog.types", "CHANGELOG.md", f"unknown types {sorted(unknown)}", "use the six standard types")
if "keepachangelog.com/en/2.0.0" not in changelog:
    add("changelog.format", "CHANGELOG.md", "does not link Keep a Changelog 2.0.0", "state the format")
refs = re.findall(r"^\[([^\]]+)\]: (https?://\S+)", changelog, flags=re.MULTILINE)
if len(refs) < len(versions) + 1:
    add("changelog.link-refs", "CHANGELOG.md", f"{len(refs)} link references for {len(versions)} versions",
        "define one per version plus Unreleased")

# 3. AGENTS.md contract
agents = fetch("AGENTS.md")
for needle, rule, fix in [
    ("```", "agents.commands", "add copy-paste commands"),
    ("Verification", "agents.verify", "add a verification section"),
    ("Do not", "agents.prohibitions", "add a prohibitions section"),
    ("| Trap", "agents.traps", "add a traps table"),
]:
    if needle not in agents:
        add(rule, "AGENTS.md", f"'{needle}' not found", fix)

# 4. PROMPT.md contract
prompt = fetch("PROMPT.md")
modules = re.findall(r"^## (M\d+) — ", prompt, flags=re.MULTILINE)
expected = [f"M{n}" for n in range(14)]
if modules != expected:
    add("prompt.modules", "PROMPT.md", f"modules are {modules}", "M0..M13 in order")
checks = len(re.findall(r"^\*\*Check:\*\*", prompt, flags=re.MULTILINE))
if checks != 14:
    add("prompt.check", "PROMPT.md", f"{checks} check lines", "one per module")
block = prompt.split("## Invariants", 1)[1] if "## Invariants" in prompt else ""
if len(re.findall(r"^\d+\. ", block, flags=re.MULTILINE)) != 10:
    add("prompt.invariants", "PROMPT.md", "invariants are not ten", "keep ten")
gate = re.search(r"## M8 .*?(?=\n## )", prompt, flags=re.DOTALL)
if gate:
    rows = len(re.findall(r"^\| \d+ \| ", gate.group(0), flags=re.MULTILINE))
    if rows != 12:
        add("prompt.gate", "PROMPT.md", f"the gate lists {rows} items", "keep twelve")
for marker in ("## M13 — ", "Experience Store", "applicability", "last_verified_at"):
    if marker not in prompt:
        add("prompt.experience", "PROMPT.md", f"M13 marker missing: {marker}", "complete M13")

# 5. translation pairing over the whole tree
listing = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://api.github.com/repos/paulmann/agent-prompt-kit/git/trees/main?recursive=1",
    headers={"User-Agent": "external-check"}), timeout=30).read().decode("utf-8"))
paths = [item["path"] for item in listing["tree"] if item["type"] == "blob" and item["path"].endswith(".md")]
for path in paths:
    if path.rsplit(".", 2)[-2] == "ru":
        twin = path.replace(".ru.md", ".md")
        if twin not in paths:
            add("pairs.orphan", path, "translation without an original", "add the English file")
    else:
        twin = path[:-3] + ".ru.md"
        if twin not in paths:
            add("pairs.missing", path, "no Russian translation", f"add {twin}")

# 6. the image
png = fetch("assets/social-preview.png", binary=True)
if not png.startswith(b"\x89PNG\r\n\x1a\n"):
    add("assets.format", "assets/social-preview.png", "not a PNG", "re-render")
else:
    width, height = int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")
    if (width, height) != (1280, 640):
        add("assets.size", "assets/social-preview.png", f"{width}x{height}", "render 1280x640")
    if len(png) > 1_000_000:
        add("assets.bytes", "assets/social-preview.png", f"{len(png)} bytes", "compress under 1 MB")
if f"{BASE}/raw/main/assets/social-preview.png" not in readme:
    add("assets.reference", "README.md", "banner not referenced by absolute raw URL", "use the raw URL")

print(f"fetched {len(paths)} markdown files, {len(versions)} released version(s), {badges} badge(s)")
for rule, where, problem, fix in findings:
    print(f"[FINDING] {rule:20} {where:28} {problem}  ->  {fix}")
print(f"verdict: {'needs-fixes (' + str(len(findings)) + ' blocking)' if findings else 'publish-ready'}")
sys.exit(1 if findings else 0)
