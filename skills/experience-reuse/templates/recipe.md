---
id: <lowercase-hyphen-slug>
type: recipe
title: <short searchable title: what the recipe does, not what the task was called>
status: draft
confidence: medium
applicability: <one sentence: the situation in which this recipe applies>
tags: [<technology>, <domain>, <task-type>]
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
last_verified_at: null
source: <user task | agent execution | manual import>
related: []
---

# Recipe

## Problem

The situation this recipe resolves, in two or three sentences. Name the symptom, not the topic.

## When to use

Concrete preconditions. If a precondition cannot be checked by reading a file or running a command,
it is not a precondition.

## When not to use

The neighbouring cases where this recipe is wrong. This section prevents most bad reuse.

## Prerequisites

Tools, versions, permissions, access. Version numbers are part of the recipe.

## Inputs

What the operator must supply: a path, a table name, a target environment.

## Procedure

1. One action per step.
2. Each step states its expected observation.
3. No step depends on a previous conversation.

## Commands or code

```text
# Sanitized example only. Use <PLACEHOLDER> for hosts, paths and identifiers.
```

## Expected result

What the operator sees when it worked, precisely enough to distinguish success from near-success.

## Validation

How the result is proven, as a command or an observation. "It looked right" is not validation.

## Rollback

How to undo it, step by step. If there is no rollback, say so and say what makes the action safe.

## Known failures

Each known failure with its symptom and its working alternative. Link a `failure` record by id.
