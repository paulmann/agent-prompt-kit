---
id: <lowercase-hyphen-slug>
type: artifact
title: <what the file is and what it is for>
status: draft
confidence: medium
applicability: <the project shape in which this artifact can be adapted>
tags: [<technology>, <artifact-kind>]
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
last_verified_at: null
source: <user task | agent execution | manual import>
related: []
---

# Artifact

## Purpose

What problem the artifact solves, and what it must not be used for.

## Adaptation points

| Placeholder | Replace with | Notes |
|---|---|---|
| `<PROJECT>` | the target project name | appears in three lines |
| `<PATH>` | the real path | keep it relative if possible |

## Content

```text
# Sanitized artifact. No credentials, no absolute machine paths.
```

## Validation

How to prove the adapted artifact works: the command and its expected output.

## Known limitations

What it does not handle, and the failure it produces when it meets that case.
