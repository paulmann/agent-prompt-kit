# agent-prompt-kit

<!-- md-i18n:switcher -->
**In anderen Sprachen:** [English](README.md) · Deutsch · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Русский](README.ru.md)

**Machen Sie aus bereits erledigter Arbeit eine Spezialistenumgebung für die Arbeit, die als Nächstes kommt. Ein Befehl liest die aktuelle Sitzung und die verwandten Sitzungen der Laufzeitumgebung, schreibt eine Task Card und eine Domain Card und legt einen Arbeitsbereich oder einen gespeicherten Agenten an, der die Regeln, das Abnahmekriterium, bearbeitete Beispiele und einen Speicher früherer Arbeit bereits enthält. Vierzehn Module, maschinell geprüft.**

[![Lizenz: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Module](https://img.shields.io/badge/modules-14-6f42c1)](PROMPT.md)
[![Lint](https://img.shields.io/badge/lint-prompt__lint.py-informational)](tools/prompt_lint.py)
[![Erfahrung](https://img.shields.io/badge/experience-reuse-0f766e)](skills/experience-reuse/SKILL.md)
[![Regeln](https://img.shields.io/badge/lint%20rules-27-brightgreen)](tools/prompt_lint.py)
[![Russische Fassung](https://img.shields.io/badge/lang-EN%20%2F%20RU-0ea5e9)](README.ru.md)

<img src="https://github.com/paulmann/agent-prompt-kit/raw/main/assets/social-preview.png"
     alt="agent-prompt-kit — ein portabler System-Prompt, der einen Agenten zum Fachspezialisten macht"
     width="100%">

Eine gute Antwort stirbt mit dem Chat. Wenn das nächste Mal dieselbe Art von Arbeit ansteht,
beginnt eine neue Sitzung bei null: dieselbe Erkundung, dieselben Sackgassen, dieselben Fragen.
Dieses Kit macht diese Wiederholung billig — nicht durch intensiveres Erinnern, sondern indem es
eine **registrierte Arbeitsumgebung** hinterlässt.

Ein Befehl, ein Ergebnis: ein Verzeichnis — ein Arbeitsbereich oder ein gespeicherter Agent —, das
bereits die Regeln für diese Art von Arbeit enthält, eine Domain Card mit einem prüfbaren
Abnahmekriterium, bearbeitete Beispiele einschließlich eines Fehlfalls, einen Speicher früherer
Arbeit und einen Start-Prompt für das nächste Fenster.

| Was der Befehl tut | Warum das zählt |
|---|---|
| liest die aktuelle Sitzung **und die verwandten Sitzungen der Laufzeitumgebung** | das Material ist die tatsächliche Arbeit, nicht ihre Beschreibung |
| schreibt Task Card + Domain Card, bevor er handelt | das Thema wird erklärt statt angenommen |
| legt das Umgebungsverzeichnis mit allen Teilen an | die nächste Runde beginnt beim elften Schritt, nicht beim ersten |
| nennt den Registrierungsschritt je Laufzeitumgebung | HARNESS: ein Klick; AutoClaw2: ein Neuladen; etwas anderes vorzugeben ist der Fehler |
| übergibt einen Start-Prompt | ein Verzeichnis ohne Übergabe ist ein Museum, kein Arbeitsplatz |

Jede Aussage über eine Laufzeitumgebung in diesem Repository ist als hier gemessen oder aus einer
Sitzung berichtet gekennzeichnet — siehe [`docs/INSTALL.md`](docs/INSTALL.md).

> **Status.** Jede Zahl hier wurde am 24.10.2026 gegen Version 1.2.0 mit
> `python tools/prompt_lint.py` gemessen. Ausführliche Anleitungen liegen in [`docs/`](docs/) und im
> [Wiki](https://github.com/paulmann/agent-prompt-kit/wiki).

## Inhalt

- [Was es ist](#was-es-ist)
- [In Zahlen](#in-zahlen)
- [Installation](#installation)
- [Laufzeitumgebungen](#laufzeitumgebungen)
- [Verwendung](#verwendung)
- [Die vierzehn Module](#die-vierzehn-module)
- [Wiederverwendung von Erfahrung](#wiederverwendung-von-erfahrung)
- [Das Qualitätstor](#das-qualitätstor)
- [Portabilität](#portabilität)
- [Dokumentation](#dokumentation)
- [Sprachen](#sprachen)
- [Entwicklung](#entwicklung)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)

## Was es ist

Eine Datei, `PROMPT.md`, dazu das Material, um ihr zu vertrauen und sie anzupassen.

| Baustein | Was er liefert |
|---|---|
| [`PROMPT.md`](PROMPT.md) | der System-Prompt: 14 Module, 14 Selbstprüfungen, 10 Invarianten |
| [`AGENTS.md`](AGENTS.md) | derselbe Vertrag in maschinenlesbarer Form, für Coding-Agenten, die Repository-Regeln lesen |
| [`skills/experience-reuse/`](skills/experience-reuse/SKILL.md) | der Skill zu M13: Arbeitsablauf, Checkliste zur Anwendbarkeit, vier Vorlagen für Einträge, eine Sicherheitsrichtlinie |
| [`tools/experience.py`](tools/experience.py) | der Erfahrungsspeicher und sein Abruf mit einem Befehl, mit Schema- und Secret-Prüfungen |
| [`memory/`](memory/README.md) | wo Einträge liegen; drei bereinigte Beispiele gehören zum Kit |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | prüft Vollständigkeit der Module, Paarung der Übersetzungen, Platzhalter, Links, Secrets, Übereinstimmung der Versionen, M13 und die Breite des Gates |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | drei Domänen, gleiche Form: Routinefall, mehrdeutiger Fall, Fehlfall |
| [`docs/`](docs/) | Entwurfsbegründung, Anpassungsprotokoll, QA-Checkliste, Validierung gegen das Ziel |

Der Prompt löst fünf konkrete Probleme, in dieser Reihenfolge:

1. **Themenabweichung** — der Agent beantwortet eine benachbarte, leichtere Frage. Dagegen wirken die
   Task Card (M1) und die Domain Card (M2), die vor jeder Aktion vorliegen müssen.
2. **Erfundener Kontext** — „wie wir vorhin besprochen haben“ über einen Thread, der nie gelesen
   wurde. Dagegen wirken das Context Ledger (M3) und drei Evidenz-Labels (M4).
3. **Nicht prüfbare Behauptungen** — „es funktioniert“ ohne Beobachtung. Dagegen wirken die
   Arbeitsschleife (M5), die Fähigkeitstabelle (M6) und das Gate (M8).
4. **Wiederholte Arbeit** — dieselbe Aufgabe wird neu hergeleitet, weil nichts den früheren Versuch
   hervorholte. Dagegen wirken der Experience Store und seine Prüfung der Anwendbarkeit (M13).
5. **Kosten der Wiederverwendung** — eine neue Domäne bedeutet, den Prompt neu zu schreiben. Dagegen
   wirkt das Spezialisierungsprotokoll (M10): eine Card, eine Beispieldatei, eine Abnahmezeile.

## In Zahlen

Gemessen in diesem Baum am 24.10.2026:

| Kennzahl | Wert | Messquelle |
|---|---:|---|
| Module im Prompt | 14 | `PROMPT.md`, Überschriften `M0`…`M13` |
| Selbstprüfungszeilen | 14 | `grep -c '^\*\*Check:\*\*' PROMPT.md` |
| Invarianten | 10 | `PROMPT.md`, Abschnitt "Invariants" |
| Tests des Qualitätstors | 12 | `PROMPT.md`, Abschnitt M8 |
| Verschiedene Regel-IDs im Linter | 27 | `grep -o 'add("[a-z]*", "[a-z.-]*"' tools/prompt_lint.py \| sort -u` |
| Selbsttests des Erfahrungsspeichers | 13 | `python tools/experience.py selftest` |
| Bearbeitete Beispiele | 3 + 3 bereinigte Einträge | `examples/`, `skills/experience-reuse/examples/` |
| Laufzeitabhängigkeiten | 0 | Importe in `tools/` |

## Installation

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit

python tools/prompt_lint.py            # exit 0 means the document is structurally complete
```

Es wird nur Python 3.11+ benötigt. Keine Pakete, kein Dienst, kein Konto.

## Laufzeitumgebungen

Dasselbe Verfahren, drei verschiedene Mechanismen. Was ein Modell tun kann und was ein Mensch tun
muss, unterscheidet sich je Laufzeitumgebung; diese Tabelle sagt, was was ist — auf dieser Maschine
gemessen oder als aus einer Sitzung berichtet gekennzeichnet.

| Laufzeitumgebung | Der Befehl | Das Modell tut | Der Mensch tut | Geprüft |
|---|---|---|---|---|
| **AutoClaw2** | `/agent-prompt-kit` (auch `/skill:agent-prompt-kit`) | schreibt den Skill nach `%USERPROFILE%\.pi\agent\skills\` und den Befehl nach `...\prompts\` | lädt neu, damit der Ressourcen-Snapshot neu gebaut wird | im App-Bundle gemessen |
| **HARNESS** | `/agent-prompt-kit` | erzeugt das gesamte Arbeitsbereichsverzeichnis mit jeder Datei | ein Klick: das Verzeichnis als Arbeitsbereich hinzufügen | Mechanismus hier gemessen; der Klick berichtet |
| **SagaAI** | — | `PROMPT.md` als Betriebsvertrag einfügen | wie es die Laufzeitumgebung verlangt | **nicht geprüft**: der Installer weigert sich zu raten |

```bash
python tools/install.py --runtime autoclaw2 --check    # files plus registration state
python tools/install.py --runtime autoClaw2 --write    # install, backup anything it replaces
python tools/install.py --runtime harness  --write
```

Der Installer meldet einen manuellen Schritt niemals als erledigt. In HARNESS gibt er den Klick
aus; in AutoClaw2 prüft er das Ressourcen-Manifest und meldet `NOT READY`, bis das Neuladen erfolgt
ist. Vollständige Mechanik und die Tabelle der Fallstricke: [`docs/INSTALL.md`](docs/INSTALL.md).

## Verwendung

1. `PROMPT.md` öffnen.
2. Alles unterhalb des YAML-Kopfes in das Feld für den System-Prompt des Agenten einfügen.
3. Dem Agenten eine echte Anfrage geben. Er muss mit einer Task Card, einer Domain Card, dem
   Liefergegenstand, den Evidenz-Labels und einer Gate-Zeile antworten.

Der Prompt ist bewusst werkzeugunabhängig — siehe [Portabilität](#portabilität). Eine bearbeitete
Antwort, in drei voneinander unabhängigen Domänen, steht in
[`examples/EXAMPLES.md`](examples/EXAMPLES.md).

## Die vierzehn Module

| Modul | Frage, die es beantwortet | Geprüft durch |
|---|---|---|
| M0 | Wessen Stimme ist das, und in welchen zwei Phasen? | das Thema wird in einem Satz benannt |
| M1 | Was wird tatsächlich gefragt? | Task Card, jedes Feld ausgefüllt oder `unknown` |
| M2 | Welcher Spezialist wird gebraucht, und was muss geprüft werden? | Domain Card, Abnahmebedingung prüfbar |
| M3 | Welcher Kontext liegt vor, und wie gut ist er? | Context Ledger mit einer Quelle je Aussage |
| M4 | Wie kennzeichne ich, was ich weiß? | `[fact]` / `[inference]` / `[assumption]` |
| M5 | Wie arbeite ich, ohne etwas kaputtzumachen? | Schleife: rahmen → abrufen → planen → handeln → prüfen → festhalten |
| M6 | Was darf ich nutzen, und was ist verboten? | Fähigkeitstabelle, Sicherheitsregeln |
| M7 | Welche Form hat die Antwort? | fünf Abschnitte plus ein optionaler Abschnitt zur wiederverwendeten Erfahrung |
| M8 | Woran erkenne ich, dass es fertig ist? | Gate mit zwölf Punkten, als Zeile berichtet |
| M9 | Wie wird dieser Prompt ausgehebelt? | sechzehn Fehlermodi mit Gegenmaßnahmen |
| M10 | Wie richte ich ihn auf eine neue Domäne? | eine Card, eine Beispieldatei, eine Abnahmezeile |
| M11 | Wie sieht eine gute Antwort aus? | drei bearbeitete Beispiele |
| M12 | Was prüfe ich vor dem Senden? | fünf Fragen, jede in einer Zeile beantwortet |
| M13 | Wie vermeide ich, bereits erledigte Arbeit erneut zu tun? | Abruf vor der Planung, Urteil zur Anwendbarkeit, bereinigter Speicher |

## Wiederverwendung von Erfahrung

M13 macht aus „das haben wir schon einmal gemacht“ einen Werkzeugaufruf statt einer Hoffnung:

```bash
python tools/experience.py search "add nullable column to list endpoint" --limit 5
```

```text
query: add nullable column to list endpoint  ·  2 candidate(s)
  [ 25] recipe    add-nullable-column-to-list-endpoint validated overlap 5, validated, high confidence, verified 2d ago
  [ 11] failure   retry-migration-until-it-passes    validated overlap 1, validated, prior failure: read before acting
```

Jede Zeile trägt den Grund für ihren Rang, sodass der Agent einen Kandidaten anhand von Belegen
statt aus dem Bauch ablehnen kann. Sechs Fragen entscheiden über die Wiederverwendung — Ziel,
Umgebung, Annahmen, Abdeckung der Validierung, Sicherheit, Aktualität — und eine nicht genannte
Anpassung gilt als blinde Kopie.

Was der Speicher ablehnt, gemessen durch seine eigenen Tests: einen Eintrag, der ein Literal in
Token-Form enthält; ein Rezept ohne Abschnitt `Rollback`; einen Eintrag ohne `last_verified_at`, der
als `validated` markiert ist. Wovor er warnt: eine Validierung, die älter als 180 Tage ist; einen
nahezu doppelten Titel. Was er nie tut: löschen — Einträge werden mit einem Verweis auf den Ersatz
als veraltet markiert.

## Das Qualitätstor

Der Agent muss eine Zeile ausgeben, zum Beispiel `gate 12/12` oder
`gate 10/12 — 6, 9 failed: <reason>`. Die zwölf Tests sind in M8 definiert; die beiden, die in der
Praxis am häufigsten scheitern, sind:

- **#4 Evidenzabdeckung** — eine Tatsachenbehauptung, die nie in das Context Ledger einging;
- **#6 Verifikation** — „es funktioniert“ ohne Befehl oder Beobachtung.

Eine Gate-Zeile ist keine Zierde: Sie macht eine Antwort für jemanden prüfbar, der dem Agenten
nicht bei der Arbeit zugesehen hat. `docs/QA.md` verwandelt dieselben zwölf Tests in eine Checkliste
für die menschliche Prüfung.

## Portabilität

Im Prompt kommen keine Werkzeugnamen vor. Fähigkeiten werden nach Klasse benannt und je
Laufzeitumgebung aufgelöst:

| Fähigkeitsklasse | Beispielhafte Zuordnungen |
|---|---|
| `read-files` | Werkzeug zum Lesen, Shell-`cat`, Editor-Puffer |
| `write-files` | Schreib-/Patch-Werkzeug, Heredoc, Inline-Vorschlag |
| `run-commands` | Shell, Sandbox, CI-Runner |
| `web-search` | Suchwerkzeug, Browser, vom Benutzer gelieferte abgerufene URLs |
| `publish` | git push, Paket-Registry, Wiki-API |

Fehlt einer Laufzeitumgebung eine Fähigkeit, baut der Prompt ausdrücklich ab (M6): Er fragt nach dem
Inhalt, erzeugt das Artefakt als Text oder benennt die fehlende Fähigkeit. Er tut nie so, als wäre
sie vorhanden.

Geprüfte Importziele: AutoClaw2, HARNESS, SagaAI und jeder Agent, der einen System-Prompt annimmt.
Die maschinenlesbare Variante ist [`AGENTS.md`](AGENTS.md).

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [`docs/DESIGN.md`](docs/DESIGN.md) | warum Module, welche Entscheidungen verworfen wurden und warum |
| [`docs/ADAPTATION.md`](docs/ADAPTATION.md) | in fünfzehn Minuten auf eine neue Domäne spezialisieren |
| [`docs/QA.md`](docs/QA.md) | die aus dem Gate abgeleitete Prüfcheckliste |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | das ursprüngliche Ziel, Anforderung für Anforderung, mit der Prüfung zu jeder |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | drei Domänen, drei Cards, drei Gate-Zeilen |

## Sprachen

Englische Dateien sind maßgeblich; russische Übersetzungen tragen das Suffix `.ru.md` — die
Konvention, die GitHub selbst verwendet. Beide werden von `tools/prompt_lint.py` synchron gehalten,
das den Build scheitern lässt, wenn einem Dokument das Gegenstück fehlt.

| Englisch | Russisch |
|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) |
| [PROMPT.md](PROMPT.md) | [PROMPT.ru.md](PROMPT.ru.md) |
| [AGENTS.md](AGENTS.md) | [AGENTS.ru.md](AGENTS.ru.md) |
| [docs/VALIDATION.md](docs/VALIDATION.md) | [docs/VALIDATION.ru.md](docs/VALIDATION.ru.md) |

## Entwicklung

```bash
python tools/prompt_lint.py            # structural contracts
python tools/prompt_lint.py --json     # machine-readable findings
```

Den Prompt ändern:

1. `PROMPT.md` bearbeiten; Modulbezeichner stabil halten — Werkzeuge und Reviews verweisen darauf.
2. `PROMPT.ru.md` im selben Commit aktualisieren.
3. `version` im Front Matter erhöhen und einen Eintrag in `CHANGELOG.md` hinzufügen; der Linter
   vergleicht beides.
4. Den Lint laufen lassen, bis er mit `0` endet.

## Mitwirken

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Sicherheitsrichtlinie: [SECURITY.md](SECURITY.md).

## Lizenz

[MIT](LICENSE).
