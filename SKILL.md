---
name: agent-prompt-kit
description: "From finished work to a specialist environment. On /agent-prompt-kit the skill reads the current session and the runtime's related sessions, writes a Task Card and a Domain Card (modules M1, M2), creates a new workspace or saved-agent directory with AGENTS.md rules, a specialization skill, worked examples, an acceptance criterion and a store of prior work, then names the registration step and hands over a starting prompt. Load when a class of work repeats and the next round should start from a prepared environment: 'make a specialist for this topic', 'create a workspace for these tasks', 'we did this before — prepare the working environment', 'analyse the session and build the environment'."
license: MIT
version: 1.2.2
upstream: https://github.com/paulmann/agent-prompt-kit
---

# `/agent-prompt-kit` — from a session to a specialist environment

One command, one result: **a directory in which similar work is done well from the first step** —
because the rules, the specialization, the worked examples, the acceptance criterion and the prior
experience are already inside it.

This is **not** "give the current session a different personality". Changing the role inside the
current window is a side mode (see §7). The main action is to create a working environment, register
it, and hand the task over to it.

## 1. Material: this session and the related ones

Sources in order of trust:

| # | Source | What it gives |
|---|---|---|
| 1 | The current session's own context | what was asked, done, verified, and where it broke |
| 2 | The runtime's index over all sessions, when it has one | the same across past sessions and other environments |
| 3 | Session transcripts and files | detail the index truncated |
| 4 | The project tree and `memory/` | rules that apply now, and existing experience records |

Rules:

- Quote a session, not an impression: "in session `<id>` we tried X and got Y".
- **Filter index noise.** An index contains injected context, tool transcripts and environment dumps.
  "We discussed this" is concluded only from the user's own messages.
- A past session is evidence of what happened, not of what is true now. Re-verify before reuse.

## 2. Cards: what this class of work is

```text
TASK CARD
Subject · Deliverable · Audience · Success looks like · Constraints · Unknown · Out of scope

DOMAIN CARD
Practitioner · Vocabulary (5-9 terms) · Skill set (3-6) · Must verify (3-5 facts) ·
Sources of truth · Typical failure · Definition of done · Anti-patterns
```

What the material does not support, write as `unknown`. A guess instead of a fact is a defect: the
next agent will read it as a rule.

## 3. Environment: what exactly to create

```text
<new environment root>/
  AGENTS.md              rules for this class of work (short: invariants plus domain bans)
  DOMAIN-CARD.md         the domain card; inside it, an acceptance criterion a reviewer can test
  .dsh/skills/<topic>/SKILL.md   the specialization: visible in the palette only inside this environment
  examples/              two or three worked cases: one routine, one failure
  memory/                the experience store (M13): recipes/, failures/, tasks/, artifacts/
  README.md              what it is, how to use it, version and date
```

Content requirements:

| File | Must contain |
|---|---|
| `AGENTS.md` | safety rules, no secrets, a verification step for every piece of work, domain boundaries |
| `DOMAIN-CARD.md` | the acceptance criterion in one sentence, testable without asking the author |
| `SKILL.md` | when to load it, what to do, how to verify; the domain's anti-patterns |
| `examples/` | at least one failure with its cause — otherwise the examples teach only the happy path |
| `memory/` | at least one recipe or failure record that passes `experience.py check` |

## 4. Registration: honest per runtime

An environment works only when the runtime knows about it. This is the one step a model often cannot
do, and it may never be reported as done when it was not.

| Runtime | The model does | The human does | How to check |
|---|---|---|---|
| **HARNESS** | creates the whole directory with every file | adds the directory as a workspace (left panel → add workspace) | the directory appears in the workspace list |
| **AutoClaw2** | writes the skill into `<profile>\.pi\agent\skills\` and the command file into `...\prompts\` | reloads the app so the resource snapshot is rebuilt | the command appears in the `/` palette, the skill in the list |
| **SagaAI / other** | depends on whether it exposes a registration API | as the runtime requires | name the step instead of assuming it |

How to report it: "the directory exists at X; one step remains that I cannot do: <exact action>".

## 5. Handoff: the starting prompt

The last output is ready-to-paste text for the new window, not "now go and work":

```text
Environment: <path>
Rules: this environment's AGENTS.md — read it first.
Task: <the first concrete task of this class>
Acceptance: <from DOMAIN-CARD.md>
Start with: python tools/experience.py search "<task words>" --root .
```

## 6. Verifying the result

- Every file exists at the named path; no existing file was overwritten.
- `python tools/experience.py check --root <environment>` → `PASS`.
- The acceptance criterion in `DOMAIN-CARD.md` is testable without asking the author.
- The registration step is named and its effect is observable (an entry in the workspace list, a
  command in the palette).
- The report ends with a gate line: `gate 12/12`, or `gate N/12 — failed: <reasons>`.

## 7. Side mode: specializing the current session

When no environment is needed — the task is one-off — the skill works as a session prompt: Task Card
and Domain Card before acting, `[fact]`/`[inference]`/`[assumption]` labels, the twelve-item gate as one
line. Same contract, without steps 3–5. Do not mix the modes: having promised an environment, deliver a
directory, not a mood.

## 8. Safety

1. Credentials, tokens, keys, cookies and session data never enter the environment or `memory/`.
   Use `<HOST>`, `<USER>`, `<PATH>`, `<API_KEY>`, `<DB>`, `<CUSTOMER>`.
2. Personal data and customer content are not stored; the shape of a solution is.
3. Experience records are deprecated, never deleted.
4. Do not overwrite existing files: on a path collision, keep a backup beside it and say so in the report.

## 9. Kit contents

| File | What it is |
|---|---|
| `PROMPT.md` / `PROMPT.ru.md` | the framework: 14 modules, 14 `Check` lines, 10 invariants, a 12-item gate |
| `docs/INSTALL.md` | installation into AutoClaw2, HARNESS, SagaAI, with verification |
| `docs/ADAPTATION.md` | how to fill the domain card |
| `skills/experience-reuse/` | M13: record templates, examples, policy |
| `tools/experience.py` | the store: `search`, `add`, `check`, `deprecate`, `selftest` |
| `tools/install.py` | installs the skill and the command into a runtime, with `--check` |

Version 1.2.0 · MIT · https://github.com/paulmann/agent-prompt-kit
