# Contributing

The kit is a document plus a linter, so contribution is mostly about keeping the document honest and
the two language versions aligned.

## Before a pull request

```bash
python tools/prompt_lint.py
```

Exit `0` is required. The linter checks module sequence, self-check lines, invariant count,
translation pairing, unresolved placeholders, relative links, secrets, absolute machine paths,
dangling module references and version agreement with the changelog.

## Rules

- **Module identifiers are an interface.** `M0`…`M12` are referenced from `docs/`, from reviews and
  from the linter. Do not renumber; add a new module only if a genuinely new question appears.
- **A module without a `**Check:**` line is not accepted.** If you cannot state how it is verified,
  the module is an opinion, not an instruction.
- **Change `PROMPT.md` and `PROMPT.ru.md` in one commit.** A translation that lags is a defect: the
  two texts must say the same thing, and the linter only compares structure.
- **Bump `version` and add a changelog entry.** The linter compares the front matter with the newest
  changelog version and fails on a mismatch.
- **No tool names in the prompt.** Capabilities are classes; the runtime maps them. A product name
  couples the kit to one vendor and one version.
- **No domain in the prompt.** Domains belong in a Domain Card and in `examples/`; the point of the
  kit is that a new domain costs one card, not a rewrite.

## Adding a language

1. Copy the English file to `<name>.<lang>.md`.
2. Translate; keep the module identifiers and the `**Check:**` lines untranslated in form.
3. Extend `tools/prompt_lint.py` pairing rules if the suffix is new.

## Reporting a problem with the prompt itself

Describe the situation, the answer the agent produced, and which module did not hold. A minimal
reproduction is one request plus the gate line the agent printed; without the gate line there is
nothing to check.

## Commit messages

Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. A breaking change to the module
set is marked with `!` and described in the changelog under `Changed`.

## Language

English is canonical; `*.ru.md` carries the translation. Both are reviewed together.
