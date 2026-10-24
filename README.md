# agent-prompt-kit

**A portable system prompt that turns any AI agent into a topic specialist at runtime: it derives the subject and skill set from the conversation, ingests context under a source ledger, labels every claim, and gates its own output. Twelve numbered modules, machine-checked.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Modules](https://img.shields.io/badge/modules-13-6f42c1)](PROMPT.md)
[![Lint](https://img.shields.io/badge/lint-prompt__lint.py-informational)](tools/prompt_lint.py)
[![Tests](https://img.shields.io/badge/contracts-28%20checks-brightgreen)](tools/prompt_lint.py)
[![Русская версия](https://img.shields.io/badge/lang-EN%20%2F%20RU-0ea5e9)](README.ru.md)

<img src="https://github.com/paulmann/agent-prompt-kit/raw/main/assets/social-preview.png"
     alt="agent-prompt-kit — a portable system prompt that makes an agent a topic specialist"
     width="100%">

Most agent prompts fail in one of two ways: they are so generic that the agent answers everything
shallowly, or so domain-bound that they cannot be reused. This kit takes a third route — the agent
is generic until it reads the request, then it writes down the subject, the skill set, the facts it
must verify and its own definition of done, and works inside that contract.

> **Status.** Every number here was measured on 2026-10-24 against version 1.0.0 with
> `python tools/prompt_lint.py`. Long guides live in [`docs/`](docs/) and the
> [Wiki](https://github.com/paulmann/agent-prompt-kit/wiki).

## Contents

- [What it is](#what-it-is)
- [In numbers](#in-numbers)
- [Quick start](#quick-start)
- [The thirteen modules](#the-thirteen-modules)
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
| [`PROMPT.md`](PROMPT.md) | the system prompt: 13 modules, 13 self-checks, 8 invariants |
| [`AGENTS.md`](AGENTS.md) | the same contract in machine-facing form, for coding agents that read repository rules |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | verifies module completeness, translation pairing, placeholders, links, secrets, version agreement |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | three domains, same shape: routine case, ambiguous case, failure case |
| [`docs/`](docs/) | design rationale, adaptation protocol, QA checklist, validation against the objective |

The prompt solves four concrete problems, in this order:

1. **Subject drift** — the agent answers a neighbouring, easier question. Countered by the Task
   Card (M1) and the Domain Card (M2), which must exist before any action.
2. **Invented context** — "as we discussed earlier" about a thread that was never read. Countered
   by the Context Ledger (M3) and three evidence labels (M4).
3. **Unverifiable claims** — "it works" with no observation. Countered by the operating loop (M5),
   the capability table (M6) and the gate (M8).
4. **Reuse cost** — a new domain means rewriting the prompt. Countered by the specialization
   protocol (M10): one card, one examples file, one acceptance line.

## In numbers

Measured in this tree on 2026-10-24:

| Surface | Value | Measurement source |
|---|---:|---|
| Modules in the prompt | 13 | `PROMPT.md`, headings `M0`…`M12` |
| Self-check lines | 13 | `grep -c '^\*\*Check:\*\*' PROMPT.md` |
| Invariants | 8 | `PROMPT.md`, section "Invariants" |
| Contract checks in the linter | 28 | `python tools/prompt_lint.py --json` |
| Worked examples | 3 | `examples/EXAMPLES.md` |
| Runtime dependencies | 0 | imports in `tools/` |

## Quick start

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit

python tools/prompt_lint.py            # exit 0 means the document is structurally complete
```

Use the prompt:

1. Open `PROMPT.md`.
2. Paste everything below the YAML header into your agent's system prompt field.
3. Give the agent a real request. It must answer with a Task Card, a Domain Card, the deliverable,
   the evidence labels and a gate line.

Nothing else is required: no packages, no service, no account. The prompt is deliberately
tool-agnostic — see [Portability](#portability).

## The thirteen modules

| Module | Question it answers | Verified by |
|---|---|---|
| M0 | Whose voice is this, and in which two phases? | the subject is named in one sentence |
| M1 | What is actually being asked? | Task Card, every field filled or `unknown` |
| M2 | Which specialist is needed, and what must be verified? | Domain Card, acceptance condition testable |
| M3 | What context exists, and how good is it? | Context Ledger with a source per claim |
| M4 | How do I label what I know? | `[fact]` / `[inference]` / `[assumption]` |
| M5 | How do I work without breaking things? | loop: frame → plan → act → verify → record |
| M6 | What may I use, and what is forbidden? | capability table, safety rules |
| M7 | What shape does the answer have? | five sections, language follows the user |
| M8 | How do I know it is finished? | ten-item gate, reported as a line |
| M9 | How is this prompt defeated? | twelve failure modes with counters |
| M10 | How do I point it at a new domain? | one card, one examples file, one acceptance line |
| M11 | What does a good answer look like? | three worked examples |
| M12 | What do I check before sending? | five questions, answered in one line each |

## The quality gate

The agent must print one line, for example `gate 10/10` or `gate 8/10 — 6, 9 failed: <reason>`.
The ten tests are defined in M8; the two that fail most often in practice are:

- **#4 evidence coverage** — a factual claim that never entered the Context Ledger;
- **#6 verification** — "it works" without a command or an observation.

A gate line is not decoration: it is what makes an answer auditable by someone who did not watch
the agent work. `docs/QA.md` turns the same ten tests into a human review checklist.

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
