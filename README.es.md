# agent-prompt-kit

<!-- md-i18n:switcher -->
**En otros idiomas:** [English](README.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · Español · [Русский](README.ru.md)

**Convierte el trabajo que ya has hecho en un entorno especializado para el trabajo que viene. Un solo comando lee la sesión actual y las sesiones relacionadas del entorno de ejecución, escribe una ficha de tarea y una ficha de dominio, y crea un espacio de trabajo o un agente guardado que ya contiene las reglas, el criterio de aceptación, ejemplos resueltos y un almacén del trabajo previo. Catorce módulos, verificados por máquina.**

[![Licencia: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Módulos](https://img.shields.io/badge/modules-14-6f42c1)](PROMPT.md)
[![Lint](https://img.shields.io/badge/lint-prompt__lint.py-informational)](tools/prompt_lint.py)
[![Experiencia](https://img.shields.io/badge/experience-reuse-0f766e)](skills/experience-reuse/SKILL.md)
[![Reglas](https://img.shields.io/badge/lint%20rules-27-brightgreen)](tools/prompt_lint.py)
[![Versión en ruso](https://img.shields.io/badge/lang-EN%20%2F%20RU-0ea5e9)](README.ru.md)

<img src="https://github.com/paulmann/agent-prompt-kit/raw/main/assets/social-preview.png"
     alt="agent-prompt-kit — un system prompt portátil que convierte a un agente en especialista de un tema"
     width="100%">

Una buena respuesta muere con el chat. La próxima vez que llega el mismo tipo de trabajo, una sesión
nueva empieza de cero: el mismo descubrimiento, los mismos callejones sin salida, las mismas
preguntas. Este kit abarata esa repetición — no recordando con más fuerza, sino dejando detrás un
**entorno de trabajo registrado**.

Un comando, un resultado: un directorio — un espacio de trabajo o un agente guardado — que ya contiene
las reglas de ese tipo de trabajo, una ficha de dominio con un criterio de aceptación comprobable,
ejemplos resueltos incluido un fallo, un almacén del trabajo previo y un prompt inicial para la
siguiente ventana.

| Qué hace el comando | Por qué importa |
|---|---|
| lee la sesión actual **y las sesiones relacionadas del entorno de ejecución** | el material es el trabajo real, no una descripción de él |
| escribe la ficha de tarea y la ficha de dominio antes de actuar | el tema se declara en lugar de darse por supuesto |
| crea el directorio del entorno con cada parte en su sitio | la siguiente ronda empieza en el paso once, no en el primero |
| nombra el paso de registro, por entorno de ejecución | HARNESS: un clic; AutoClaw2: una recarga; fingir lo contrario es el defecto |
| entrega un prompt inicial | un directorio sin entrega es un museo, no un lugar de trabajo |

Toda afirmación sobre el entorno de ejecución en este repositorio está marcada como medida aquí o
reportada desde una sesión — véase [`docs/INSTALL.md`](docs/INSTALL.md).

> **Estado.** Cada número de este documento se midió el 2026-10-24 contra la versión 1.2.0 con
> `python tools/prompt_lint.py`. Las guías largas viven en [`docs/`](docs/) y en la
> [Wiki](https://github.com/paulmann/agent-prompt-kit/wiki).

## Contenido

- [Qué es](#qué-es)
- [En cifras](#en-cifras)
- [Instalación](#instalación)
- [Entornos de ejecución](#entornos-de-ejecución)
- [Uso](#uso)
- [Los catorce módulos](#los-catorce-módulos)
- [Reutilización de la experiencia](#reutilización-de-la-experiencia)
- [La puerta de calidad](#la-puerta-de-calidad)
- [Portabilidad](#portabilidad)
- [Documentación](#documentación)
- [Idiomas](#idiomas)
- [Desarrollo](#desarrollo)
- [Cómo contribuir](#cómo-contribuir)
- [Licencia](#licencia)

## Qué es

Un archivo, `PROMPT.md`, más el material necesario para confiar en él y adaptarlo.

| Pieza | Qué te da |
|---|---|
| [`PROMPT.md`](PROMPT.md) | el system prompt: 14 módulos, 14 autocomprobaciones, 10 invariantes |
| [`AGENTS.md`](AGENTS.md) | el mismo contrato en forma legible por máquina, para agentes de código que leen las reglas del repositorio |
| [`skills/experience-reuse/`](skills/experience-reuse/SKILL.md) | la habilidad M13: flujo de trabajo, lista de comprobación de aplicabilidad, cuatro plantillas de registro, una política de seguridad |
| [`tools/experience.py`](tools/experience.py) | el almacén de experiencia y su recuperación en un solo comando, con comprobación de esquema y de secretos |
| [`memory/`](memory/README.md) | dónde viven los registros; el kit incluye tres ejemplos anonimizados |
| [`tools/prompt_lint.py`](tools/prompt_lint.py) | verifica la completitud de los módulos, el emparejamiento de traducciones, los marcadores de posición, los enlaces, los secretos, la coincidencia de versión, M13 y la anchura de la puerta |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | tres dominios con la misma forma: caso rutinario, caso ambiguo, caso de fallo |
| [`docs/`](docs/) | el razonamiento de diseño, el protocolo de adaptación, la lista de control de QA, la validación frente al objetivo |

El prompt resuelve cinco problemas concretos, en este orden:

1. **Deriva del tema** — el agente responde a una pregunta vecina y más fácil. Se contrarresta con la
   ficha de tarea (M1) y la ficha de dominio (M2), que deben existir antes de cualquier acción.
2. **Contexto inventado** — «como comentamos antes» sobre un hilo que nunca se leyó. Se contrarresta
   con el registro de contexto (M3) y tres etiquetas de evidencia (M4).
3. **Afirmaciones no verificables** — «funciona» sin ninguna observación. Se contrarresta con el bucle
   operativo (M5), la tabla de capacidades (M6) y la puerta (M8).
4. **Trabajo repetido** — la misma tarea deducida otra vez porque nada mostró el intento anterior. Se
   contrarresta con el almacén de experiencia y su comprobación de aplicabilidad (M13).
5. **Coste de reutilización** — un dominio nuevo obliga a reescribir el prompt. Se contrarresta con el
   protocolo de especialización (M10): una ficha, un archivo de ejemplos, una línea de aceptación.

## En cifras

Medido en este árbol el 2026-10-24:

| Superficie | Valor | Fuente de la medición |
|---|---:|---|
| Módulos del prompt | 14 | `PROMPT.md`, títulos `M0`…`M13` |
| Líneas de autocomprobación | 14 | `grep -c '^\*\*Check:\*\*' PROMPT.md` |
| Invariantes | 10 | `PROMPT.md`, sección «Invariantes» |
| Pruebas de la puerta de calidad | 12 | `PROMPT.md`, sección M8 |
| Identificadores de regla distintos en el linter | 27 | `grep -o 'add("[a-z]*", "[a-z.-]*"' tools/prompt_lint.py \| sort -u` |
| Autopruebas de experiencia | 13 | `python tools/experience.py selftest` |
| Ejemplos resueltos | 3 + 3 registros anonimizados | `examples/`, `skills/experience-reuse/examples/` |
| Dependencias del entorno de ejecución | 0 | imports de `tools/` |

## Instalación

```bash
git clone https://github.com/paulmann/agent-prompt-kit.git
cd agent-prompt-kit

python tools/prompt_lint.py            # exit 0 means the document is structurally complete
```

Solo se necesita Python 3.11+. Sin paquetes, sin servicio, sin cuenta.

## Entornos de ejecución

El mismo procedimiento, tres mecanismos distintos. Lo que un modelo puede hacer y lo que una persona
debe hacer difieren según el entorno de ejecución, y esta tabla dice qué es cada cosa — medido en esta
máquina, o marcado como reportado desde una sesión.

| Entorno de ejecución | El comando | Qué hace el modelo | Qué hace la persona | Verificado |
|---|---|---|---|---|
| **AutoClaw2** | `/agent-prompt-kit` (también `/skill:agent-prompt-kit`) | escribe la habilidad en `%USERPROFILE%\.pi\agent\skills\` y el comando en `...\prompts\` | recarga para que se reconstruya la instantánea de recursos | medido en el paquete de la aplicación |
| **HARNESS** | `/agent-prompt-kit` | crea el directorio de espacio de trabajo completo con todos los archivos | un clic: añadir el directorio como espacio de trabajo | mecanismo medido aquí; el clic reportado |
| **SagaAI** | — | pegar `PROMPT.md` como contrato operativo | según lo requiera el entorno de ejecución | **no verificado**: el instalador se niega a adivinar |

```bash
python tools/install.py --runtime autoclaw2 --check    # files plus registration state
python tools/install.py --runtime autoClaw2 --write    # install, backup anything it replaces
python tools/install.py --runtime harness  --write
```

El instalador nunca informa un paso manual como hecho. En HARNESS imprime el clic; en AutoClaw2
comprueba el manifiesto de recursos y dice `NOT READY` hasta que se ha producido la recarga. Mecánica
completa y tabla de trampas: [`docs/INSTALL.md`](docs/INSTALL.md).

## Uso

1. Abre `PROMPT.md`.
2. Pega todo lo que hay debajo de la cabecera YAML en el campo de system prompt de tu agente.
3. Da al agente una petición real. Debe responder con una ficha de tarea, una ficha de dominio, el
   entregable, las etiquetas de evidencia y una línea de puerta.

El prompt es deliberadamente independiente de las herramientas — véase [Portabilidad](#portabilidad). Una
respuesta resuelta, en tres dominios no relacionados, está en [`examples/EXAMPLES.md`](examples/EXAMPLES.md).

## Los catorce módulos

| Módulo | Pregunta que responde | Verificado por |
|---|---|---|
| M0 | ¿De quién es esta voz, y en qué dos fases? | el tema se nombra en una frase |
| M1 | ¿Qué se está pidiendo en realidad? | ficha de tarea, cada campo relleno o `unknown` |
| M2 | ¿Qué especialista hace falta y qué hay que verificar? | ficha de dominio, condición de aceptación comprobable |
| M3 | ¿Qué contexto existe y qué calidad tiene? | registro de contexto con una fuente por afirmación |
| M4 | ¿Cómo etiqueto lo que sé? | `[fact]` / `[inference]` / `[assumption]` |
| M5 | ¿Cómo trabajo sin romper cosas? | bucle: encuadrar → recuperar → planificar → actuar → verificar → registrar |
| M6 | ¿Qué puedo usar y qué está prohibido? | tabla de capacidades, reglas de seguridad |
| M7 | ¿Qué forma tiene la respuesta? | cinco secciones más una sección opcional de experiencia reutilizada |
| M8 | ¿Cómo sé que está terminado? | puerta de doce puntos, reportada como una línea |
| M9 | ¿Cómo se derrota este prompt? | dieciséis modos de fallo con sus contramedidas |
| M10 | ¿Cómo lo apunto a un dominio nuevo? | una ficha, un archivo de ejemplos, una línea de aceptación |
| M11 | ¿Cómo se ve una buena respuesta? | tres ejemplos resueltos |
| M12 | ¿Qué compruebo antes de enviar? | cinco preguntas, respondidas en una línea cada una |
| M13 | ¿Cómo evito rehacer trabajo ya hecho? | recuperación antes de planificar, veredicto de aplicabilidad, almacén anonimizado |

## Reutilización de la experiencia

M13 convierte «esto ya lo hicimos» en una llamada a una herramienta en lugar de una esperanza:

```bash
python tools/experience.py search "add nullable column to list endpoint" --limit 5
```

```text
query: add nullable column to list endpoint  ·  2 candidate(s)
  [ 25] recipe    add-nullable-column-to-list-endpoint validated overlap 5, validated, high confidence, verified 2d ago
  [ 11] failure   retry-migration-until-it-passes    validated overlap 1, validated, prior failure: read before acting
```

Cada línea lleva el motivo de su posición, así el agente puede rechazar un candidato por la evidencia
y no por una corazonada. Seis preguntas deciden la reutilización — objetivo, entorno, supuestos,
cobertura de validación, seguridad, frescura — y una adaptación no declarada cuenta como copia ciega.

Lo que el almacén rechaza, medido por sus propias pruebas: un registro que contiene un literal con
forma de token, una receta sin sección `Rollback`, un registro sin `last_verified_at` marcado
`validated`. De lo que avisa: una validación con más de 180 días, un título casi duplicado. Lo que
nunca hace: borrar — los registros se marcan obsoletos con un puntero al reemplazo.

## La puerta de calidad

El agente debe imprimir una línea, por ejemplo `gate 12/12` o `gate 10/12 — 6, 9 failed: <reason>`.
Las doce pruebas se definen en M8; las dos que fallan más a menudo en la práctica son:

- **#4 cobertura de evidencia** — una afirmación factual que nunca entró en el registro de contexto;
- **#6 verificación** — «funciona» sin un comando ni una observación.

Una línea de puerta no es adorno: es lo que hace que una respuesta sea auditable por alguien que no vio
trabajar al agente. `docs/QA.md` convierte las mismas doce pruebas en una lista de revisión humana.

## Portabilidad

En el prompt no aparece ningún nombre de herramienta. Las capacidades se nombran por clase y se
resuelven por entorno de ejecución:

| Clase de capacidad | Ejemplos de correspondencia |
|---|---|
| `read-files` | herramienta de lectura, `cat` del shell, búfer del editor |
| `write-files` | herramienta de escritura/parche, heredoc, sugerencia en línea |
| `run-commands` | shell, sandbox, ejecutor de CI |
| `web-search` | herramienta de búsqueda, navegador, URL obtenidas que aporta el usuario |
| `publish` | git push, registro de paquetes, API de la wiki |

Si a un entorno de ejecución le falta una capacidad, el prompt degrada de forma explícita (M6): pide el
contenido, produce el artefacto como texto o nombra la capacidad ausente. Nunca finge.

Objetivos de importación verificados: AutoClaw2, HARNESS, SagaAI y cualquier agente que acepte un
system prompt. La variante legible por máquina es [`AGENTS.md`](AGENTS.md).

## Documentación

| Documento | Contenido |
|---|---|
| [`docs/DESIGN.md`](docs/DESIGN.md) | por qué módulos, qué decisiones se rechazaron y por qué |
| [`docs/ADAPTATION.md`](docs/ADAPTATION.md) | especializarse en un dominio nuevo en quince minutos |
| [`docs/QA.md`](docs/QA.md) | la lista de revisión derivada de la puerta |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | el objetivo original, requisito por requisito, con la comprobación de cada uno |
| [`examples/EXAMPLES.md`](examples/EXAMPLES.md) | tres dominios, tres fichas, tres líneas de puerta |

## Idiomas

Los archivos en inglés son canónicos; las traducciones al ruso llevan el sufijo `.ru.md` — la
convención que usa GitHub. Ambos se mantienen sincronizados con `tools/prompt_lint.py`, que hace fallar
la compilación cuando un documento no tiene gemelo.

| Inglés | Ruso |
|---|---|
| [README.md](README.md) | [README.ru.md](README.ru.md) |
| [PROMPT.md](PROMPT.md) | [PROMPT.ru.md](PROMPT.ru.md) |
| [AGENTS.md](AGENTS.md) | [AGENTS.ru.md](AGENTS.ru.md) |
| [docs/VALIDATION.md](docs/VALIDATION.md) | [docs/VALIDATION.ru.md](docs/VALIDATION.ru.md) |

## Desarrollo

```bash
python tools/prompt_lint.py            # structural contracts
python tools/prompt_lint.py --json     # machine-readable findings
```

Cambiar el prompt:

1. Edita `PROMPT.md`; mantén estables los identificadores de módulo — las herramientas y las revisiones
   se refieren a ellos.
2. Actualiza `PROMPT.ru.md` en el mismo commit.
3. Sube `version` en el front matter y añade una entrada a `CHANGELOG.md`; el linter los compara.
4. Ejecuta el lint hasta que termine con `0`.

## Cómo contribuir

Véase [CONTRIBUTING.md](CONTRIBUTING.md). Política de seguridad: [SECURITY.md](SECURITY.md).

## Licencia

[MIT](LICENSE).
