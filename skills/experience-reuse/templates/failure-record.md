---
id: <lowercase-hyphen-slug>
type: failure
title: <the failing action, phrased so it is found by searching for the symptom>
status: draft
confidence: high
applicability: <when this failure is likely to recur>
tags: [<technology>, <domain>, <symptom>]
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
last_verified_at: null
source: <user task | agent execution | manual import>
related: []
---

# Failure record

## What was attempted

The approach, with enough detail to recognize the same attempt next time.

## Symptom

What the operator observes: the exact error text with `<PLACEHOLDER>`s, the timeout, the silent wrong
output. Silent failures need the strongest description — they are what makes a record worth keeping.

## Root cause

Why it failed. If the cause is a hypothesis, say so and mark confidence `low` or `medium`.

## Cost

How much time and effort the discovery took. This is why the record exists.

## Working alternative

What succeeded instead, or "none found" with what was tried.

## Prevention

The check that would catch this earlier: a lint rule, a test, a precondition in a recipe.

## Related

The recipe this failure belongs to, by id.
