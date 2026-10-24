# From a finished session to a specialist environment

Specialization is not a change of tone inside the current window. It is an artefact: a directory the
runtime registers as a workspace (or a saved agent) that already contains the rules, the domain card,
the acceptance criterion, the worked examples and the store of prior work for **one class of tasks**.

Build one when the same class of work has already happened and will happen again. Not for a one-off:
an environment costs more than a fresh derivation on the first round and pays from the second one
([Why](00-Why.md)).

## The five steps

| # | Step | Output | Falsifiable test |
|---:|---|---|---|
| 1 | Material | what was asked, attempted, verified, and where it broke | every claimed fact comes from this session, the session index or a file — nothing from memory |
| 2 | Cards | Task Card and Domain Card (M1, M2) | no field is a placeholder; practitioner and must-verify facts are specific |
| 3 | Environment | the directory itself | each file exists; `experience.py check` passes; no existing file was overwritten |
| 4 | Registration | the runtime knows about it | done through an API, or named as one exact manual step with the path to hand over |
| 5 | Handoff | a first prompt for the new window | it names the card, the acceptance criterion and the first task |

## Anatomy

```text
<workspace>/
  AGENTS.md                    rules for this class of work (what to check, what not to do)
  DOMAIN-CARD.md               practitioner, vocabulary, must-verify facts, definition of done
  .dsh/skills/<topic>/SKILL.md the procedure itself — visible in the palette only inside this workspace
  examples/                    1-3 worked cases: input, what was produced, what was rejected and why
  memory/                      the experience store (tasks, recipes, artifacts, failures)
  README.md                    what this environment is for, and its version
```

Each file answers one question: rules ("what must I not do"), card ("who am I and what is done"),
skill ("how is it done"), examples ("what does a correct result look like"), store ("what was already
done"). A missing file is a hole the next session fills by guessing.

## The Domain Card

Nine fields. The two that decide quality are **must verify** and **definition of done**.

```text
DOMAIN CARD
Subject:            <from the Task Card, one noun phrase>
Practitioner:       <the role title that does this work professionally>
Core vocabulary:    5-9 terms a specialist uses, one line each
Skill set:          3-6 capabilities this job actually requires
Must verify:        the 3-5 facts a specialist would never assert without checking
Sources of truth:   where the authoritative answer lives
Typical failure:    how this work usually goes wrong
Definition of done: the acceptance condition, phrased so a reviewer can test it
Anti-patterns:      what a junior does here that a senior does not
```

Two rules that keep it honest:

- **derive, do not stereotype** — the skill set comes from the subject, not from a catalogue of
  professions; two documentation jobs can require different skills;
- **"must verify" beats "must know"** — a specialist is distinguished less by recall than by knowing
  which three facts cannot be asserted from memory.

## An acceptance criterion a reviewer can test

Bad: "the report works". Good, in the shape the kit asks for:

| Domain | Acceptance criterion |
|---|---|
| PHP endpoint | the response carries the new field for one known id, and the previous response shape is unchanged |
| Windows service | the service restarts clean, the new IPC command is in the registry, and the contract test is updated |
| Documentation | every link resolves, every image has alt text, and the changelog parses against the standard |

If you cannot write it in this form, the class of work is not yet understood well enough to specialize
— go back to step 1.

## Registration: the step that decides whether it exists

| Runtime | What a model may do | What a human must do |
|---|---|---|
| AutoClaw2 | write the skill directory and the command file | reload, so the resource snapshot is rebuilt |
| HARNESS | create the whole directory with all files | one click: add the folder as a workspace |
| SagaAI or another runtime | depends on whether it exposes a registration API | say so instead of pretending the environment is live |

**A folder is not a workspace until the runtime knows about it.** Handing over an unregistered
directory is failure 17 in the list of failure modes, and gate item 12 exists to catch it.

## Handoff prompt

The last artefact of building an environment is the first message of the next session:

```text
Use the workspace at <path> (registered as "<title>").
Its rules: AGENTS.md. Its acceptance criterion: DOMAIN-CARD.md, section "Definition of done".
First task: <one sentence>.
Before planning, run: python tools/experience.py search "<the task's own words>".
Report the gate line at the end.
```

Without it, the next session starts from the request again and the environment is dead weight.

## Version it

Record a version and a date inside the environment (in `README.md` and in the card). An environment
without a version cannot be audited, and its rules drift without anyone noticing — the same failure the
linter catches on this repository's own pages.

## Cost check

A new domain must cost **one card, one examples file, one acceptance line**. If adding a specialty
requires touching the prompt, the runtime configuration and three other pages, the design has leaked —
fix the design, not the specialty.

Next: [Experience](05-Experience.md) — the store this environment keeps.
