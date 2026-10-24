---
id: retry-migration-until-it-passes
type: failure
title: Retrying a failed migration until it passes, instead of reading why it failed
status: validated
confidence: high
applicability: Any project where a migration applies partially and the first impulse is to rerun it
tags: [sql, migration, validation, silent-corruption]
created_at: 2026-10-01
updated_at: 2026-10-22
last_verified_at: 2026-10-22
source: agent execution
related: [add-nullable-column-to-list-endpoint]
---

# Example: failure record

## What was attempted

A schema migration failed halfway on a test database. The response was to rerun it three times, then
to comment out the failing statement and apply the rest.

## Symptom

The second run failed with a different error than the first — a duplicate column — and the third run
reported success. The table then held a column with a default that the migration had never intended,
because the original statement had partially applied before failing.

## Root cause

DDL is not atomic across statements on every engine, and a partially applied migration leaves the
schema in a state no migration file describes. Rerunning re-executes statements that already ran.

## Cost

About ninety minutes, including a false conclusion that the migration was fine because the third run
exited zero.

## Working alternative

1. Read the first error, not the third.
2. Snapshot the schema before touching it: `SHOW CREATE TABLE <name>` into a file.
3. Determine which statements already applied by comparing the snapshot with the migration file.
4. Apply the remainder by hand, one statement at a time, verifying after each.
5. Record the actual schema state in the migration's notes.

## Prevention

- Apply migrations only to a copy first, with a decoy table that must survive untouched.
- Assert the expected schema **after** the run instead of trusting an exit code.
- A migration that has failed once is never rerun unchanged.

## Related

`add-nullable-column-to-list-endpoint` — the recipe whose validation caught a variant of this.
