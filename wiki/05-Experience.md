# Experience store

The store exists because "consult your experience" is not a rule anyone follows. It costs a model a
directory walk and a guess. "Run one command that returns the three best candidates with their
applicability" costs one command. So the kit ships the command.

```bash
python tools/experience.py search "one more field in the report"
```

## Layout

```text
memory/
  index.json          rebuilt from the records; never hand-edited
  tasks/              task records: what was asked, attempted, produced, verified
  recipes/            solution patterns, not transcripts
  artifacts/          files, configs, scripts, prompts, checklists worth adapting
  failures/           what failed, the root cause, the working alternative
```

A record is plain Markdown: a header of twelve keys, then a body. Nothing to install, nothing to
migrate, readable in a diff.

```yaml
id: add-column-to-endpoint
type: recipe            # task | recipe | artifact | failure
title: Add a nullable column to a reporting endpoint
status: validated       # draft | validated | deprecated
confidence: high        # low | medium | high
applicability: PHP endpoint on MySQL where the column is additive and no client parses SELECT *
tags: [php, mysql, migration]
created_at: 2026-10-24
updated_at: 2026-10-24
last_verified_at: 2026-10-24
source: user task
related: []
```

A recipe body carries five sections, and `check` refuses the record if one is missing:

```text
## Problem   ## When to use   ## Procedure   ## Validation   ## Rollback
```

`## Rollback` is mandatory on purpose: a recipe without an undo path is a trap with a nice title.

## Commands

| Command | What it does |
|---|---|
| `experience.py init` | creates the four folders and an empty index |
| `experience.py add <file>` | validates a record, then files it by type |
| `experience.py search "<words>"` | ranked candidates with the reason for each rank |
| `experience.py show <id>` | the full record |
| `experience.py check` | schema, secrets, absolute paths, duplicates, staleness |
| `experience.py stats` | counts by type and status |
| `experience.py deprecate <id> --by <id>` | retires a record without deleting it |
| `experience.py selftest` | thirteen fixtures proving the refusals still refuse |

Exit codes: `0` clean, `1` findings at error level, `2` usage problem.

## What retrieval actually prints

Measured on a one-record sandbox, searching with the task's own words:

```text
query: report needs one more field  ·  1 candidate(s)
  [ 25] recipe    add-column-to-endpoint             validated overlap 5, validated, high confidence, verified 1d ago
        Add a nullable column to a reporting endpoint  —  memory/recipes/add-column-to-endpoint.md
```

Four decisions are visible in that line: the rank score, the type, the status, and **why** — term
overlap, validation, confidence, freshness. A result without a reason cannot be audited, so the tool
always prints one.

## What it refuses

Measured with `selftest` — these are real refusals, not documentation:

| Situation | The tool says |
|---|---|
| a credential literal in the body | `exp.secret … redact to a <placeholder>` |
| a recipe without `## Rollback` | `exp.recipe-sections … a recipe needs ## Rollback` |
| an absolute machine path | `exp.abs-path … use <path>` |
| two records with one id | `exp.duplicate-id` |
| a deprecated record without `superseded_by` | warning, not silent |
| an empty store | `exp.empty` — nothing to retrieve, so it is not a pass |

## The six questions before reuse

A record is a hypothesis. Every question must pass, or the record is adapted (and the adaptation
named) or rejected.

| # | Question | Fails when |
|---:|---|---|
| 1 | same goal? | the record solved a neighbouring problem |
| 2 | same environment? | versions, paths, permissions or dependencies differ |
| 3 | assumptions still hold? | the schema, API or contract changed |
| 4 | does its validation cover my acceptance criterion? | it proved "the page renders", you need "the export is byte-identical" |
| 5 | do security rules still allow it? | the old approach stored a credential in a config file |
| 6 | is it still current? | `last_verified_at` is old and nobody re-ran the check |

An unstated adaptation is indistinguishable from a blind copy — hence the requirement to name it in
the answer (`## Reused experience`).

## Recording rules

1. Record what is reusable, sanitised and general enough to apply elsewhere.
2. Never record a one-off context, private business data, or anything unverified.
3. Update an existing record instead of creating a near-duplicate.
4. Link the task record to the recipe, artifact and failure records it produced.
5. Deprecate with `superseded_by`; audit history is never deleted.
6. Set `last_verified_at` only after a real revalidation — never after merely reading the record.

## Security

Records are content, and content leaks. Use placeholders: `<API_KEY>`, `<HOST>`, `<USER>`, `<PATH>`,
`<CUSTOMER>`, `<DB>`. A record that touches private context declares its sensitivity (`public`,
`internal`, `restricted`), and `restricted` is not stored at all. Public repositories receive sanitised
examples only.

## Traps

| Trap | Symptom | Action |
|---|---|---|
| recording every task | the store fills with noise, retrieval finds nothing, the agent stops searching | record only reusable, general, verified work |
| treating a record as truth | an old recipe applied to a changed environment | run the six questions, name the adaptation |
| two stores | one agent keeps private notes beside the shared one | one store, one schema, one command |
| editing `index.json` by hand | retrieval and `stats` disagree with the files | let `add`/`check` rebuild it |
| stale `last_verified_at` | the rank boosts a record nobody has validated for a year | refresh only by re-running its `## Validation` |
| `check` on the repository as shipped | it also flags the store's own `README.ru.md` as a record without a header, because the checker excludes only `README.md` | known defect in the checker; point `--root` at your own environment, where only real records exist |

Next: [Checklists](06-Checklists.md) — the gate, the failure modes, the traps in one place.
