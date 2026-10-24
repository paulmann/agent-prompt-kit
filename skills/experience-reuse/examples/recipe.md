---
id: add-nullable-column-to-list-endpoint
type: recipe
title: Add a nullable column to a list endpoint without widening the select
status: validated
confidence: high
applicability: A server-rendered admin panel whose list query names its columns explicitly
tags: [php, sql, migration, api]
created_at: 2026-10-01
updated_at: 2026-10-22
last_verified_at: 2026-10-22
source: agent execution
related: [retry-migration-until-it-passes]
---

# Example: recipe

## Problem

A list screen must show one more field. The tempting change is `SELECT *`, which quietly alters three
other endpoints that share the query builder.

## When to use

- The column already exists in the table, or a migration adds it as nullable.
- The list query names its columns explicitly.
- The field is display-only: no filtering or sorting is being added.

## When not to use

- The column is computed from other tables: the join changes, not the select.
- The endpoint is cached per session: the new field will appear late and look like a bug.
- The column is not nullable and the table is large: the migration locks the table.

## Prerequisites

- Access to the schema of the live table, not only to the migrations.
- A test that already covers the endpoint, so a regression is visible.

## Inputs

- The real column name.
- The acceptance condition: what the reviewer must see.

## Procedure

1. Read the migration that created the column, and confirm the real name. `[fact]` from the file.
2. Confirm nullability; a non-nullable column needs a backfill first.
3. Add the field to the explicit select list.
4. Add it to the presenter, formatting the value (dates as ISO, NULL as an em dash).
5. Extend the existing test with one row containing NULL.
6. Run the suite.

## Commands or code

```text
# Sanitized example only. Names are placeholders.
grep -n "<column_name>" migrations/*.sql
php tests/run.php --filter <endpoint_name>
```

## Expected result

The endpoint returns the new field; the screen renders a date for rows that have one and `<dash>` for
rows that do not. No other endpoint's output changes.

## Validation

- The suite is green.
- One assertion on a NULL row.
- `git diff --stat` touching exactly the select list, the presenter and the test.

## Rollback

Revert the select list and presenter changes. No schema change is involved, so the rollback is a
single revert commit. If a nullable column was added, dropping it is separate and needs the backup
rule.

## Known failures

- `retry-migration-until-it-passes` — the migration variant that hides a partial apply.
- Em dash in a Cyrillic or Latin subset font: the character may be missing from the subset; verify in
  the rendered page, not in the source.
