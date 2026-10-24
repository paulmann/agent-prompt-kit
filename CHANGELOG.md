# Changelog

All notable changes to this project are documented here. The format is
[Keep a Changelog](https://keepachangelog.com/en/2.0.0/) 2.0.0, and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/paulmann/agent-prompt-kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/paulmann/agent-prompt-kit/releases/tag/v1.0.0
