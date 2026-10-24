# AGENTS.md — rules for an agent using this kit

This repository ships a system prompt, not a program. An agent working with it must keep two things
true: the prompt stays structurally complete, and the two language versions never diverge.

Read `PROMPT.md` before anything else. Module identifiers (`M0`…`M12`) are stable addresses: they are
used in reviews, in `docs/` and in `tools/prompt_lint.py`.

## Verification

```bash
python tools/prompt_lint.py          # exit 0 = structural contracts hold
python tools/prompt_lint.py --json   # machine-readable findings
```

The linter fails on: a missing module, a module out of order, a missing `**Check:**` line, a
translation without its English twin, an unresolved `{{placeholder}}` outside a code fence, a broken
relative link, a secret-shaped literal, an absolute machine path, a dangling `M<number>` reference,
and a version mismatch between the prompt header and the changelog.

## Editing the prompt

1. Change `PROMPT.md`. Do not renumber modules: numbering is an interface.
2. Change `PROMPT.ru.md` in the same commit, keeping the same module set.
3. Bump `version` in both front matters and add a `CHANGELOG.md` entry.
4. Run the linter until it exits `0`.

Never edit a `.ru.md` file alone. Never translate a module differently in substance: a translation
that softens an invariant is a defect, not a style choice.

## What the prompt itself requires of you

When you operate *under* this prompt, these hold:

| Rule | Source |
|---|---|
| Declare the subject before acting | M0, M1 |
| Write the Task Card and the Domain Card | M1, M2 |
| Keep a Context Ledger; no unsourced claim | M3 |
| Label every non-trivial statement | M4 |
| Smallest verifiable step, verify after acting | M5 |
| Sandbox irreversible actions; never print secrets | M6 |
| Answer in five sections, in the user's language | M7 |
| Report the ten-item gate as one line | M8 |

## Do not

- Add a domain to the prompt itself. Domains belong in a Domain Card and in `examples/`.
- Add tool names to the prompt. Capabilities are classes; the runtime maps them (M6).
- Present the gate line without running the gate. A reported pass that was not earned is the exact
  failure the kit exists to prevent.
- Publish a version whose `version` field and changelog disagree.

## Portability targets

| Runtime | How to load |
|---|---|
| AutoClaw2 | paste the body of `PROMPT.md` into the agent's system prompt; `AGENTS.md` covers repository work |
| HARNESS | same, via its project rules |
| SagaAI | same, via its system prompt field |
| Any other agent | paste the body; if a capability is missing, expect M6 to degrade explicitly |

## Layout

```text
PROMPT.md            the prompt, English (canonical)
PROMPT.ru.md         the prompt, Russian
AGENTS.md            this file
docs/                design, adaptation, QA, validation
examples/            three worked domains
tools/prompt_lint.py the only executable here
```

## License

MIT.
