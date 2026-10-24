# Changelog

All notable changes to this project are documented here. The format is
[Keep a Changelog](https://keepachangelog.com/en/2.0.0/) 2.0.0, and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-10-24

### Added

- Root `SKILL.md` / `SKILL.ru.md` — the portable entry users install: five steps from a finished session to a specialist environment, per-runtime registration, a handoff prompt, and the session-persona mode demoted to a side mode.
- `tools/install.py` — installs the skill and the `/agent-prompt-kit` command into AutoClaw2 or HARNESS, backs up whatever it replaces, and `--check` reports files plus registration state. For SagaAI it **refuses to guess** and prints the two questions to answer instead.
- `docs/INSTALL.md` / `.ru.md` — measured mechanics per runtime: skill roots and command file format in AutoClaw2, the workspace registry and session index in HARNESS, plus a trap table where every row maps to an observed symptom.
- Related sessions as a first-class source: M3 gains the session-index row and two rules (a past session is evidence of what happened; index noise is not evidence), and M6 gains the `session-search` and `workspace-create` capabilities.
- The quality gate grew to twelve items: item 12 checks **delivery** — a directory at a named path, a truthful registration step, a handoff prompt.
- Three failure modes (17–19): produced-but-not-installed, environment substituted by a persona, reasoning from index noise.
- A tenth invariant: a reusable deliverable counts only when it is registered, or the exact registration step is named.

### Changed

- `M0` now states two outputs — an answer, and a specialist environment when the work repeats — and names the failure it prevents: a good answer that dies with the chat.
- `M10` rewritten: it was "fill a card" with no destination; it is now the five-step procedure ending in registration and handoff, with a runtime table that says what the model can do and what a human must do.
- README (both languages) leads with the purpose instead of the prompt mechanics, and gains a Runtimes section.
- The linter and the external check track ten invariants, a twelve-item gate, and the presence of `SKILL.md` and `docs/INSTALL.md`.
- Numbers in the README are measured, not estimated: the lint badge reports 27 distinct rule ids because that is what the tool actually contains.

### Fixed

- Documentation no longer describes the kit as "paste this into your system prompt" as the primary route; that route is one of three, and the other two are commands.
- A claim of "34 contract checks" was invented in the previous version and replaced by the measured count.
- `docs/QA.md` and its translation had a duplicated row after an automated count sweep; removed.

## [1.1.0] - 2026-10-24

### Added

- `M13 — Experience reuse`: before planning a non-trivial task, search a store of prior work; record it after verification. Experience is a hypothesis, never authority.
- Four experience types — task record, recipe, artifact, failure record — with a fixed metadata header, so the store is queryable without reading every file.
- A six-question applicability check, because blind copying of an old recipe is the cheapest way to reproduce an old bug.
- `tools/experience.py` — the store and its one-command retrieval: `init`, `add`, `search`, `show`, `check`, `stats`, `deprecate`, `selftest`. Lexical ranking prints the reason for each position; `add` refuses a record with a token-shaped literal, an absolute machine path, or a recipe missing `Rollback`.
- `skills/experience-reuse/` — the portable skill: workflow, retrieval rules, applicability checklist, four record templates, three sanitised examples, and a security/retention policy. Every file in English and Russian.
- `memory/` — the store's home, with the rules for what belongs there and what never does.
- The quality gate grew from ten tests to eleven: retrieval ran, every reused record has a verdict, nothing sensitive entered the store.
- Four new failure modes (13–16): blind recipe copy, stale experience as truth, store as a dump, two stores.
- `prompt_lint.py` now enforces the new contracts: M13 markers in both languages, eleven gate rows, the store, the tool and the skill sections.

### Changed

- `M3` — the Experience Store joins the source table at priority 5.5, with rule 7: experience never overrides the current repository, attached material or an explicit instruction.
- `M5` — the loop gained a **Retrieve** step between Frame and Plan, and Record now decides whether a record is warranted.
- `M6` — capabilities `memory-search` and `memory-write`, plus rule 8: experience writes are reviewable and never contain sensitive values.
- `M7` — an optional `## Reused experience` section, and rule 7: reused work is named, with what was adapted.
- `M10` — a domain may add record types, but not change the M13 invariants.
- Ten invariants: prior experience is retrieved before planning, validated before reuse, sanitised before storage.

## [1.0.0] - 2026-10-24

### Added

- `PROMPT.md` — the portable system prompt: thirteen modules (`M0`–`M12`), each with a self-check line, plus eight invariants that hold in every domain.
- Task Card and Domain Card as mandatory pre-work outputs: the subject, the practitioner, the skill set, the facts that must be verified and a testable definition of done.
- Context ingestion with a priority order and a five-column Context Ledger, so no claim enters an answer unsourced.
- Three evidence labels — `[fact]`, `[inference]`, `[assumption]` — with a rule that an assumption names its consequence.
- A capability-class tool policy with an explicit degradation column and seven safety rules, including the sandbox-before-irreversible rule and a ban on displaying secrets.
- A five-section output contract, a ten-item quality gate reported as one line, and a table of twelve failure modes with counters.
- A specialization protocol: a new domain costs one card, one examples file and one acceptance line.
- `examples/EXAMPLES.md` — three unrelated domains (PHP panel, Windows service, documentation product) using one prompt with zero edits.
- `tools/prompt_lint.py` — 28 structural contract checks: module sequence, self-check lines, invariant count, translation pairing, placeholders, links, secrets, absolute paths, dangling module references, version agreement.
- `docs/DESIGN.md`, `docs/ADAPTATION.md`, `docs/QA.md`, `docs/VALIDATION.md` — rationale, the fifteen-minute procedure, the human review checklist, and the objective checked requirement by requirement.
- Russian translations for every document, following the `.ru.md` convention.

### Security

- The kit ships without tokens, absolute machine paths or personal addresses; the linter fails the build if one appears, which is how the repository enforces on itself the rule the prompt states.

[Unreleased]: https://github.com/paulmann/agent-prompt-kit/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/paulmann/agent-prompt-kit/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/paulmann/agent-prompt-kit/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/paulmann/agent-prompt-kit/releases/tag/v1.0.0
