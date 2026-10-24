# memory/ — the experience store

Prior work lives here: one Markdown file per record, validated against a schema, retrieved with one
command. The skill that governs it is `skills/experience-reuse/SKILL.md`; the module in the prompt is
M13.

```bash
python tools/experience.py check                                    # is the store healthy
python tools/experience.py search "add nullable column to endpoint"  # retrieve before planning
python tools/experience.py add skills/experience-reuse/examples/recipe.md
python tools/experience.py stats
```

Four folders, one record type each: `recipes/`, `failures/`, `tasks/`, `artifacts/`.

## What belongs here

A record is worth writing when the work would cost more than ten minutes to rediscover and the
result is reusable: a procedure that will apply again, a failure that was expensive, an artifact that
can be adapted, a task whose outcome explains a later one.

A record does **not** belong here when it is a one-off, contains private context, or states something
unverified.

## What must never appear

Credentials, personal data, customer content, internal hostnames and absolute machine paths. The
store ships with three sanitised examples only — they use `<PLACEHOLDER>`s throughout, and
`experience.py check` fails on a token-shaped literal.

## Status, not deletion

`draft` → `validated` → `deprecated`. A record is deprecated with a pointer to its replacement, never
deleted: the audit trail is the reason a supermarket of prior work can be trusted at all.
`last_verified_at` older than 180 days raises a warning; only a real re-run clears it.
