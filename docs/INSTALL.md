# Installation

Three runtimes, three different mechanisms. Every command in this page was run on 2026-10-24 on this
machine; anything taken from another session is marked as such. If a step needs a human action, it is
written as a human action — pretending otherwise is the failure this page exists to prevent.

## What you are installing

| Piece | Purpose | Where it must land |
|---|---|---|
| the skill | the procedure "session → specialist environment" | the runtime's skills root |
| the command | a short `/` entry that runs it | the runtime's prompts root, or the same skill |
| `tools/experience.py` | the store of prior work (M13) | inside the installed skill |

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit
python tools/install.py --runtime autoClaw2 --check     # what would happen
python tools/install.py --runtime autoClaw2 --write     # do it
```

Valid runtimes: `autoclaw2`, `harness`, `saga`. `--check` never writes.

## AutoClaw2

Measured in `resources/app/dist/main.cjs` of AutoClaw2 2.2.x on this machine.

| Fact | Value |
|---|---|
| skill roots, in priority order | `%USERPROFILE%\.pi\agent\skills` (pi-user, 1) · `%USERPROFILE%\.agents\skills` (shared) · `<account>\runtime\zwork-agent\skills` (zwork, 2) |
| command files | `%USERPROFILE%\.pi\agent\prompts\<name>.md` |
| command name | the file name without `.md`, lowercase letters, digits and hyphens |
| command front matter | `description` (required in practice), `argument-hint` (optional); arguments via `${ARGUMENTS}`, `$1`, `${1:-default}` |
| reserved names | `reload`, `settings` — a file with these names is rejected |
| body size limit | 256 KB |
| how a skill is addressed | `/skill:<name>`, name from `SKILL.md` front matter, must equal the directory name |
| registration | the app builds a resource snapshot into `<account>\runtime\pi-resources\revisions\<hash>\manifest.json`; a file that is not in that manifest is invisible to the model |

Two human steps, and both are cheap:

1. **Reload** after installation (or restart the app). The snapshot is rebuilt then; the current
   session keeps the snapshot it started with.
2. **Verify**: `python tools/install.py --runtime autoClaw2 --check` must report the skill and the
   command as registered.

Measured behaviour worth knowing: the snapshot was rebuilt on its own between turns (21:02 → 22:51),
so a restart is not always required — but a *running* session never sees a resource added after it
started. Do not trust "it should appear": check the manifest.

## HARNESS

Measured here: the install target, the session index and the workspace registry. The one-click
registration step and the AGENTS budget come from a HARNESS session on 2026-10-24 and are marked as
such.

| Fact | Value |
|---|---|
| skill root | `%USERPROFILE%\.dsh\skills\<name>\SKILL.md` |
| command | the same file: `/agent-prompt-kit` (the skill name becomes the command) |
| workspace registry | `%USERPROFILE%\.dsh\storages\workspace.json` — version 2, `tables.workspaces.<uuid>{path,title,sessionIds}`, 18 entries at the time of measurement |
| session index | `%USERPROFILE%\.dsh\cache\session-search.db` — SQLite FTS5, measured 232 sessions / 106 663 documents / 310 MB |
| workspace = path + title in the registry | the directory alone is not a workspace |
| `AGENTS.md` budget | 65 536 bytes; a longer file stops being loaded (measured in a HARNESS session) |

Install:

```bash
python tools/install.py --runtime harness --write
```

This copies the kit into `%USERPROFILE%\.dsh\skills\agent-prompt-kit\` and writes `SKILL.md` there.

**The one step a model cannot do:** adding the directory as a workspace. In the left panel choose
**add workspace** and point it at the new environment directory. Until that click, the directory is a
folder, not a workspace. Do not report it as working before it appears in the list.

Querying the session index (read-only, safe):

```bash
sqlite3 "%USERPROFILE%\.dsh\cache\session-search.db" \
  "select session_id, count(*) from persisted_docs
   where persisted_docs match '\"agent-prompt-kit\"' and type = 'user/message'
   group by session_id order by 2 desc limit 10"
```

`type` is one of `user/message`, `assistant/message`, `tool/call`, `tool/result`, `turn/end`,
`todo/write`; `surface` is `current`, `log-only` or `shadowed`. Filtering to `user/message` is what
removes the injection noise: of 106 663 documents only 3 193 are user messages.

## SagaAI

No verified facts about its skill or command mechanism are recorded in this repository. The installer
therefore **refuses to guess**: `--runtime saga` prints the portable procedure and the two questions to
answer before installing — where the skill root is, and whether an API can register a command or an
agent.

What is portable regardless of the runtime: `PROMPT.md` (paste it as the operating contract),
`memory/` and `tools/experience.py` (they only need Python 3.11 and a directory).

```bash
python tools/install.py --runtime saga
```

## Verification, in one place

```bash
python tools/prompt_lint.py                      # the document's own contracts
python tools/experience.py selftest              # 13 store checks on fixtures
python tools/install.py --runtime <rt> --check    # installed files + registration
```

## Traps, all of them measured

| Trap | Symptom | What to do |
|---|---|---|
| The command file name is wrong | the command never appears in the palette | lowercase letters, digits, hyphens only; not `reload`, not `settings` |
| The skill directory name differs from `name` in `SKILL.md` | the skill loads under an unexpected name, or not at all | keep them identical |
| No `description` in front matter | the skill is never selected automatically | write one, with the phrases a user would actually type |
| Files installed, snapshot not rebuilt | everything looks right and nothing works | reload, then check the manifest |
| A workspace directory without registration | the agent "created the environment" and the next session sees nothing | name the click explicitly |
| `AGENTS.md` over 64 KB in HARNESS | rules silently stop applying | keep the file short; move detail into `docs/` |
| Windows line endings in records | diffs full of noise, checksum mismatches | the tools write LF; do not "fix" them by hand |
| Cyrillic query against English records | the store returns few candidates | write `title` and `applicability` in the words a future request would use |
