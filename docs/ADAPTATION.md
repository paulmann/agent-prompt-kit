# Adaptation: a new domain in fifteen minutes

The prompt does not know any domain, so adding one is a bounded procedure. If it takes longer, the
prompt is being edited where it should be configured.

## The procedure

### 1. Write the Domain Card (10 minutes)

Copy the template from `PROMPT.md` M2. Fill it from the material you actually have:

| Field | Test of a good entry |
|---|---|
| Practitioner | a job title you could hire |
| Core vocabulary | 5–9 terms; if you cannot define one in a line, you do not know it well enough |
| Skill set | 3–6; each must be exercised by the task, not by the domain in general |
| Must verify | facts you would be embarrassed to assert from memory |
| Sources of truth | files, schemas, standards, API docs — named, not described |
| Typical failure | how this work usually breaks |
| Definition of done | one sentence a reviewer can test without asking you anything |
| Anti-patterns | what a junior does here that a senior does not |

### 2. Add one worked example (5 minutes)

Put it in `examples/`, same shape as the existing three: routine case, or the ambiguous one if you
already have a routine case. Include the cards, a compressed answer with labels, and a gate line.

### 3. Write the acceptance line

One sentence: what must be observable for the job to be accepted. Not "the code is clean" — that is
not observable. "The endpoint returns the field and the existing suite passes" is.

### 4. Version it

Add a `CHANGELOG.md` entry with the date. A specialized agent without a version cannot be audited; the
next reader will not know which behaviour was tested.

### 5. Seed the store with one recipe

A domain with an empty store has nothing to retrieve on the first repeat. After the first successful
task in the new domain, write one recipe from `skills/experience-reuse/templates/recipe.md` and check
it:

```bash
python tools/experience.py add drafts/first-recipe.md
python tools/experience.py search "the next task in your own words"
```

The second command is the real acceptance test: if retrieval does not surface the recipe for a query
written the way a future requester would write it, the record's title and applicability are wrong, not
the tool.

## What not to change

| Invariant | Why it must survive |
|---|---|
| M3 ingestion order | otherwise priority becomes whatever the agent prefers |
| M4 three labels | dropping one collapses the other two under pressure |
| M6 safety rules | a domain never justifies a shortcut on secrets or irreversible actions |
| M8 gate | without it, "done" is an opinion |
| M13 sanitisation and applicability | a domain-specific store that skips the six questions turns reuse into blind copying |

If a domain seems to require changing one of these, the honest answer is usually that the task is a
different task — restate the Task Card.

## Signs the adaptation went wrong

| Symptom | Diagnosis | Fix |
|---|---|---|
| The prompt grew by a page for one domain | the domain was written into the prompt | move it into the Domain Card |
| Two cards disagree about "done" | acceptance was copied, not derived | write one acceptance line, delete the other |
| The examples need different answer shapes | the output contract is too rigid for this domain | keep M7's five sections, change only their content |
| Every task in the domain is "special" | the card is too broad | split the domain, one card each |
| Retrieval always returns nothing | the records use the store's vocabulary, not the requester's | rewrite titles and applicability in the words a future request would use |

## Worked micro-example

```text
DOMAIN CARD — database migration review
Practitioner:        database reliability engineer
Core vocabulary:     additive migration, lock window, backfill, rollback path, online DDL
Skill set:           reading query plans; estimating lock time; writing reversible migrations
Must verify:         table size; whether the change is additive; the deployment window
Sources of truth:    schema migrations, table statistics, the deployment calendar
Typical failure:     a NOT NULL column added without a default, locking the table
Definition of done:  migration applies and rolls back on a copy, lock time measured and stated
Anti-patterns:       testing on an empty database; "it ran fine locally" as evidence
```

That is the whole adaptation: eight fields, one sentence of acceptance, one changelog line.
