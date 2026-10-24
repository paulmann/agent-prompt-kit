# agent-prompt-kit

**Turn work you have already done into a specialist environment for the work coming next. One command reads the current session and the runtime's related sessions, writes a Task Card and a Domain Card, and creates a workspace or saved agent that already holds the rules, the acceptance criterion, worked examples and a store of prior work. Fourteen modules, machine-checked.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Modules](https://img.shields.io/badge/modules-14-6f42c1)](PROMPT.md)
[![Lint](https://img.shields.io/badge/lint-prompt__lint.py-informational)](tools/prompt_lint.py)
[![Experience](https://img.shields.io/badge/experience-reuse-0f766e)](skills/experience-reuse/SKILL.md)
[![Rules](https://img.shields.io/badge/lint%20rules-27-brightgreen)](tools/prompt_lint.py)
[![Русская версия](https://img.shields.io/badge/lang-EN%20%2F%20RU-0ea5e9)](README.ru.md)

<img src="https://github.com/paulmann/agent-prompt-kit/raw/main/assets/social-preview.png"
     alt="agent-prompt-kit — a portable system prompt that makes an agent a topic specialist"
     width="100%">

A good answer dies with the chat. The next time the same class of work arrives, a fresh session
starts from zero: the same discovery, the same dead ends, the same questions. This kit makes that
repetition cheap — not by remembering harder, but by leaving a **registered working environment**
behind.

One command, one result: a directory — a workspace, or a saved agent — that already holds the rules
for that class of work, a domain card with a testable acceptance criterion, worked examples including
one failure, a store of prior work, and a starting prompt for the next window.

| What the command does | Why it matters |
|---|---|
| reads the current session **and the runtime's related sessions** | the material is the real work, not a description of it |
| writes Task Card + Domain Card before acting | the subject is declared instead of assumed |
| creates the environment directory with every part in place | the next round starts from the eleventh step, not the first |
| names the registration step, per runtime | HARNESS: one click; AutoClaw2: a reload; pretending otherwise is the bug |
| hands over a starting prompt | a directory with no handoff is a museum, not a workplace |

Every runtime claim in this repository is marked as measured here or reported from a session — see
[`docs/INSTALL.md`](docs/INSTALL.md).

> **Status.** Every number here was measured on 2026-10-24 against version 1.2.0 with
> `python tools/prompt_lint.py`. Long guides live in [`docs/`](docs/) and the
> [Wiki](https://github.com/paulmann/agent-prompt-kit/wiki).

## Contents

- [What it is](#what-it-is)
- [In numbers](#in-numbers)
- [Installation](#installation)
- [Runtimes](#runtimes)
- [Usage](#usage)
- [The fourteen modules](#the-fourteen-modules)
- [Experience reuse](#experience-reuse)
- [The quality gate](#the-quality-gate)
- [Portability](#portability)
- [Documentation](#documentation)
- [Languages](#languages)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## What it is

One file, `PROMPT.md`, plus the material needed to trust and adapt it.

| Piece | What it gives you |
|---|---|
| [`PROMPT.md`](PROMPT.md) | the system prompt: 14 modules, 14 self-checks, 10 invariants |
| [`AGENTS.md`](AGENTS.md) | the same contract in machine-facing form, for coding agents that read repository rules |
| [`skills/experience-reuse/`](skills/experience-reuse/SKILL.md) | the M13 skill: workflow, applicability checklist, four record templates, a security policy |
| [`tools/experience.py`](tools/experience.py) | the experience store and its one-command retrieval, with schema and secret checks |
| [`memory/`](memory/README.md) | where records live; three sanitised examples ship with the kit |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | verifies module completeness, translation pairing, placeholders, links, secrets, version agreement, M13 and the gate width |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | three domains, same shape: routine case, ambiguous case, failure case |
| [`docs/`](docs/) | design rationale, adaptation protocol, QA checklist, validation against the objective |

The prompt solves five concrete problems, in this order:

1. **Subject drift** — the agent answers a neighbouring, easier question. Countered by the Task
   Card (M1) and the Domain Card (M2), which must exist before any action.
2. **Invented context** — "as we discussed earlier" about a thread that was never read. Countered
   by the Context Ledger (M3) and three evidence labels (M4).
3. **Unverifiable claims** — "it works" with no observation. Countered by the operating loop (M5),
   the capability table (M6) and the gate (M8).
4. **Repeated work** — the same task re-derived because nothing surfaced the prior attempt. Countered
   by the Experience Store and its applicability check (M13).
5. **Reuse cost** — a new domain means rewriting the prompt. Countered by the specialization
   protocol (M10): one card, one examples file, one acceptance line.

## In numbers

Measured in this tree on 2026-10-24:

| Surface | Value | Measurement source |
|---|---:|---|
| Modules in the prompt | 14 | `PROMPT.md`, headings `M0`…`M13` |
| Self-check lines | 14 | `grep -c '^\*\*Check:\*\*' PROMPT.md` |
| Invariants | 10 | `PROMPT.md`, section "Invariants" |
| Quality-gate tests | 12 | `PROMPT.md`, section M8 |
| Distinct rule ids in the linter | 27 | `grep -o 'add("[a-z]*", "[a-z.-]*"' tools/prompt_lint.py \| sort -u` |
| Experience self-tests | 13 | `python tools/experience.py selftest` |
| Worked examples | 3 + 3 sanitised records | `examples/`, `skills/experience-reuse/examples/` |
| Runtime dependencies | 0 | imports in `tools/` |

## Installation

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit

python tools/prompt_lint.py            # exit 0 means the document is structurally complete
```

Only Python 3.11+ is required. No packages, no service, no account.

## Runtimes

The same procedure, three different mechanisms. What a model can do and what a human must do are
different per runtime, and this table says which is which — measured on this machine, or marked as
reported from a session.

| Runtime | The command | The model does | The human does | Verified |
|---|---|---|---|---|
| **AutoClaw2** | `/agent-prompt-kit` (also `/skill:agent-prompt-kit`) | writes the skill into `%USERPROFILE%\.pi\agent\skills\` and the command into `...\prompts\` | reloads so the resource snapshot is rebuilt | measured in the app bundle |
| **HARNESS** | `/agent-prompt-kit` | creates the whole workspace directory with every file | one click: add the directory as a workspace | mechanism measured here; the click reported |
| **SagaAI** | — | paste `PROMPT.md` as the operating contract | as the runtime requires | **not verified**: the installer refuses to guess |

```bash
python tools/install.py --runtime autoclaw2 --check    # files plus registration state
python tools/install.py --runtime autoClaw2 --write    # install, backup anything it replaces
python tools/install.py --runtime harness  --write
```

The installer never reports a manual step as done. In HARNESS it prints the click; in AutoClaw2 it
checks the resource manifest and says `NOT READY` until the reload happened. Full mechanics and the
trap table: [`docs/INSTALL.md`](docs/INSTALL.md).

## Usage

1. Open `PROMPT.md`.
2. Paste everything below the YAML header into your agent's system prompt field.
3. Give the agent a real request. It must answer with a Task Card, a Domain Card, the deliverable,
   the evidence labels and a gate line.

The prompt is deliberately tool-agnostic — see [Portability](#portability). A worked answer, in three
unrelated domains, is in [`examples/EXAMPLES.md`](examples/EXAMPLES.md).

## The fourteen modules

| Module | Question it answers | Verified by |
|---|---|---|
| M0 | Whose voice is this, and in which two phases? | the subject is named in one sentence |
| M1 | What is actually being asked? | Task Card, every field filled or `unknown` |
| M2 | Which specialist is needed, and what must be verified? | Domain Card, acceptance condition testable |
| M3 | What context exists, and how good is it? | Context Ledger with a source per claim |
| M4 | How do I label what I know? | `[fact]` / `[inference]` / `[assumption]` |
| M5 | How do I work without breaking things? | loop: frame → retrieve → plan → act → verify → record |
| M6 | What may I use, and what is forbidden? | capability table, safety rules |
| M7 | What shape does the answer have? | five sections plus an optional reused-experience section |
| M8 | How do I know it is finished? | twelve-item gate, reported as a line |
| M9 | How is this prompt defeated? | sixteen failure modes with counters |
| M10 | How do I point it at a new domain? | one card, one examples file, one acceptance line |
| M11 | What does a good answer look like? | three worked examples |
| M12 | What do I check before sending? | five questions, answered in one line each |
| M13 | How do I avoid redoing work already done? | retrieval before planning, applicability verdict, sanitised store |

## Experience reuse

M13 turns "we did this before" into a tool call instead of a hope:

```bash
python tools/experience.py search "add nullable column to list endpoint" --limit 5
```

```text
query: add nullable column to list endpoint  ·  2 candidate(s)
  [ 25] recipe    add-nullable-column-to-list-endpoint validated overlap 5, validated, high confidence, verified 2d ago
  [ 11] failure   retry-migration-until-it-passes    validated overlap 1, validated, prior failure: read before acting
```

Each line carries the reason for its rank, so the agent can reject a candidate on evidence rather
than on vibes. Six questions decide reuse — goal, environment, assumptions, validation coverage,
security, freshness — and an unstated adaptation counts as a blind copy.

What the store refuses, measured by its own tests: a record containing a token-shaped literal, a
recipe without a `Rollback` section, a record without `last_verified_at` marked `validated`. What it
warns about: a validation older than 180 days, a near-duplicate title. What it never does: delete —
records are deprecated with a pointer to the replacement.

## The quality gate

The agent must print one line, for example `gate 12/12` or `gate 10/12 — 6, 9 failed: <reason>`.
The twelve tests are defined in M8; the two that fail most often in practice are:

- **#4 evidence coverage** — a factual claim that never entered the Context Ledger;
- **#6 verification** — "it works" without a command or an observation.

A gate line is not decoration: it is what makes an answer auditable by someone who did not watch
the agent work. `docs/QA.md` turns the same twelve tests into a human review checklist.

## Portability

No tool names appear in the prompt. Capabilities are named by class and resolved per runtime:

| Capability class | Example mappings |
|---|---|
| `read-files` | read tool, shell `cat`, editor buffer |
| `write-files` | write/patch tool, heredoc, inline suggestion |
| `run-commands` | shell, sandbox, CI runner |
| `web-search` | search tool, browser, fetched URLs supplied by the user |
| `publish` | git push, package registry, wiki API |

If a runtime lacks a capability, the prompt degrades explicitly (M6): it asks for the content,
produces the artefact as text, or names the missing capability. It never pretends.

Verified import targets: AutoClaw2, HARNESS, SagaAI, and any agent that accepts a system prompt.
The machine-facing variant is [`AGENTS.md`](AGENTS.md).

## Documentation

| Document | Content |
|---|---|
| [`docs/DESIGN.md`](docs/DESIGN.md) | why modules, which decisions were rejected and why |
| [`docs/ADAPTATION.md`](docs/ADAPTATION.md) | specializing in a new domain in fifteen minutes |
| [`docs/QA.md`](docs/QA.md) | the review checklist derived from the gate |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | the original objective, requirement by requirement, with the check for each |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | three domains, three cards, three gate lines |

## Languages

English files are canonical; Russian translations carry the `.ru.md` suffix — the convention
GitHub itself uses. Both are kept in sync by `tools/prompt_lint.py`, which fails the build when a
document has no twin.

| English | Russian |
|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) |
| [PROMPT.md](PROMPT.md) | [PROMPT.ru.md](PROMPT.ru.md) |
| [AGENTS.md](AGENTS.md) | [AGENTS.ru.md](AGENTS.ru.md) |
| [docs/VALIDATION.md](docs/VALIDATION.md) | [docs/VALIDATION.ru.md](docs/VALIDATION.ru.md) |

## Development

```bash
python tools/prompt_lint.py            # structural contracts
python tools/prompt_lint.py --json     # machine-readable findings
```

Changing the prompt:

1. Edit `PROMPT.md`; keep module identifiers stable — tools and reviews refer to them.
2. Update `PROMPT.ru.md` in the same commit.
3. Bump `version` in the front matter and add a `CHANGELOG.md` entry; the linter compares them.
4. Run the lint until it exits `0`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security policy: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE).
