# 🧠 AI Agency Prompt OS

[![CI](https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS/actions/workflows/validate.yml/badge.svg)](https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS/actions/workflows/validate.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

> Sistema operativo modular de prompts para una agencia de IA. Cada prompt es un
> **microservicio cognitivo** especializado: una función pura `f(input) → structured output`
> que se puede encadenar, reutilizar y versionar como código.

Diseñado para ejecutarse en un repositorio de GitHub con **Claude Code (Opus 4.8)**:
leer el repo completo, ejecutar prompts como módulos, encadenar workflows y generar nuevos prompts.

---

## 🎯 Qué resuelve

- **Generar estrategias completas de negocio IA** en minutos.
- **Ejecutar por departamentos** (Product, Growth, Sales, Ops, Finance, AI Engineering).
- **Encadenar outputs** entre módulos sin adaptación manual.
- **Reutilizar prompts** como productos independientes.
- **Escalar a SaaS** interno o externo reutilizando los mismos módulos.

---

## 🏗️ Arquitectura

> Vista de conjunto con diagramas (capas, DAG de dependencias y ciclo de ejecución):
> [`docs/architecture.md`](docs/architecture.md).

```
ai-agency-prompt-os/
├── core/                 # Orquestación y motor de workflows
│   ├── orchestrator.prompt.md        # Descompone, delega, consolida, decide
│   ├── workflow-engine.prompt.md     # Ejecuta workflows de prompts
│   ├── decision-log.schema.md        # Memoria de decisiones persistente
│   └── _prompt-template.md           # Plantilla canónica de microservicio
│
├── departments/          # 18 microservicios cognitivos
│   ├── product/          # product-builder · ux-strategy · roadmap-generator
│   ├── growth/           # growth-engine · funnel-designer · content-strategy
│   ├── sales/            # sales-system · crm-automation · closing-playbooks
│   ├── operations/       # ops-automation · workflow-designer · scaling-ops
│   ├── finance/          # pricing-strategy · unit-economics · financial-scenarios
│   └── ai-engineering/   # ai-architecture · model-selection · agent-design
│
├── workflows/            # Encadenamientos declarativos de prompts
│   ├── full-business-build.workflow.md
│   ├── growth-loop.workflow.md
│   ├── sales-funnel.workflow.md
│   └── blueprint-mvp.workflow.md     # "Compiler" mínimo para un SaaS consumidor
│
├── schemas/              # Contratos de I/O (JSON Schema)
│   ├── input.schema.json
│   ├── output.schema.json
│   └── decision.schema.json
│
├── registry/             # Catálogo, dependencias y versionado
│   ├── prompt-index.md       # Vista humana del catálogo
│   ├── manifest.json         # Fuente de verdad legible por máquina (grafo + workflows)
│   ├── manifest.schema.json
│   ├── dependency-map.md
│   └── versioning.md
│
├── examples/             # Ejecuciones de referencia end-to-end
├── scripts/validate.py   # Validador de integridad (corre en CI)
└── README.md
```

---

## 🧩 Principio central: prompts como funciones puras

Cada prompt cumple tres contratos:

1. **Input normalizado** — `schemas/input.schema.json`
   Siempre: contexto del negocio · objetivo · restricciones · datos disponibles.

2. **Output estructurado** — `schemas/output.schema.json`
   Siempre: decisiones · opciones comparadas · recomendación · riesgos · dependencias · próximos pasos.

3. **Compatibilidad** — el output de un módulo alimenta a otro sin transformación manual.
   El payload propio viaja en `artifacts`; el siguiente módulo lo lee desde
   `available_data.upstream_outputs`.

```
product-builder → growth-engine → sales-system → ops-automation
```

Cada módulo declara su contrato de encadenamiento (`consumes` / `produces` / `feeds`),
registrado en [`registry/dependency-map.md`](registry/dependency-map.md).

---

## 🧠 El orquestador

[`core/orchestrator.prompt.md`](core/orchestrator.prompt.md) es el cerebro del sistema:

- **Nunca diseña** si existe un prompt especializado — **delega primero**.
- Recoge outputs, **resuelve conflictos** entre departamentos y **consolida decisiones**.
- Solo escala a humano las **decisiones estratégicas**.
- Mantiene un **Decision Log** permanente ([`core/decision-log.schema.md`](core/decision-log.schema.md)).

---

## 🚀 Cómo se ejecuta con Claude Code (Opus 4.8)

El sistema está diseñado para que un agente lea el repo y ejecute módulos. Flujo típico:

1. **Define tu input** conforme a `schemas/input.schema.json` (contexto, objetivo, restricciones).
2. **Pide un workflow.** Ejemplo de prompt al agente:

   > "Actúa como `core/orchestrator`. Ejecuta el workflow `full-business-build` para este negocio:
   > {tu business_context, objective, constraints}. Delega a cada módulo según
   > `registry/prompt-index.md`, respeta el DAG de `registry/dependency-map.md` y devuelve el
   > output consolidado conforme a `schemas/output.schema.json`."

3. **El orquestador** invoca `workflow-engine`, que recorre el DAG módulo a módulo, valida cada
   output contra el schema y acumula el estado.
4. **Recibes** un output consolidado: resumen ejecutivo, decisiones, conflictos resueltos,
   recomendación final y el próximo workflow sugerido.

### Ejecutar un único módulo (prompt como producto)

> "Actúa como `departments/finance/pricing-strategy`. Aquí tienes el input
> (`schemas/input.schema.json`) y el upstream `product-builder`. Devuelve el output estructurado."

---

## 🔁 Workflows incluidos

| Workflow | Objetivo | Resultado |
|----------|----------|-----------|
| [`full-business-build`](workflows/full-business-build.workflow.md) | Diseñar una empresa de IA completa | Plan integrado de 10 módulos + merge |
| [`growth-loop`](workflows/growth-loop.workflow.md) | Motor de crecimiento + viabilidad económica | Modelo, funnel, contenido, gate de unit economics |
| [`sales-funnel`](workflows/sales-funnel.workflow.md) | Sistema de ventas automatizado | Pipeline, CRM, playbooks de cierre |
| [`blueprint-mvp`](workflows/blueprint-mvp.workflow.md) | Blueprint mínimo (idea → blueprint exportable) | Producto, IA, growth, pricing, unit-economics, roadmap + merge |

### Runner (manifiesto → acción)

[`scripts/run_workflow.py`](scripts/run_workflow.py) lee `registry/manifest.json` y prepara la
orquestación de forma determinista (sin llamar a ningún LLM ni necesitar API key):

```bash
python3 scripts/run_workflow.py --list                  # workflows disponibles
python3 scripts/run_workflow.py full-business-build examples/ai-tutor-oposiciones/input.json
python3 scripts/run_workflow.py growth-loop mi-input.json --compose   # mega-prompt componido
```

Resuelve el orden de pasos, valida el encadenamiento (señala errores de orden y distingue los
*soft-cycles* esperados), y emite un plan listo para que `core/orchestrator` lo ejecute en Claude Code.

---

## 📂 Ejemplos

[`examples/`](examples/) contiene ejecuciones de referencia end-to-end. La primera,
[`ai-tutor-oposiciones`](examples/ai-tutor-oposiciones/), muestra un `input.json` normalizado y la
ejecución encadenada de `full-business-build` (10 módulos → merge del orquestador), evidenciando
cómo el output de cada módulo alimenta al siguiente sin adaptación manual.

---

## 🏢 Operar como agencia (multi-cliente)

El [Agency Playbook](docs/agency-playbook.md) explica cómo entregar a **muchos clientes reutilizando
los mismos módulos**: los prompts no cambian, cambia el `input`. Cada cliente vive en
[`clients/<cliente>/`](clients/) a partir de [`clients/_template/`](clients/_template/), con su propio
`run_id`, Decision Log y outputs aislados. Esto habilita servicios productizados, retainers y un
futuro SaaS self-serve sin reescribir nada.

---

## 🔌 Usar este repo como motor de un SaaS

Este repo es el **motor reutilizable** (prompts + contratos + grafo). Una app SaaS puede consumirlo
como su pipeline de generación de blueprints. Ver [`docs/integration-acos.md`](docs/integration-acos.md)
para el contrato de integración y el pipeline [`blueprint-mvp`](workflows/blueprint-mvp.workflow.md),
pensado como "Compiler" mínimo (idea → blueprint exportable).

---

## 🧭 Principios de diseño

**Priorizar:** modularidad · reutilización · automatización · claridad estructural · compatibilidad entre prompts.
**Evitar:** texto redundante · ambigüedad · prompts no ejecutables · mezcla de responsabilidades.

---

## ➕ Añadir un nuevo prompt

1. Copia [`core/_prompt-template.md`](core/_prompt-template.md) a `departments/<dept>/<id>.prompt.md`.
2. Rellena Metadata, Rol, I/O, Dependencias, Reglas, Método y Salida obligatoria.
3. Regístralo en [`registry/prompt-index.md`](registry/prompt-index.md) y
   [`registry/dependency-map.md`](registry/dependency-map.md).
4. Versiona según [`registry/versioning.md`](registry/versioning.md).
5. Ejecuta `python3 scripts/validate.py` (sin dependencias) para verificar que los schemas
   son válidos y que el registry no tiene referencias colgantes. El mismo check corre en CI
   ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)) en cada PR.

---

## 📐 Convenciones

- `id` en kebab-case, único en todo el repo.
- Todo prompt acepta `input.schema.json` y emite `output.schema.json`.
- Las decisiones siguen `decision.schema.json` (tabla `| Decision | Options | Recommendation | Impact |`).
- El grafo de dependencias es un **DAG**; las relaciones bidireccionales se resuelven por iteración, no por recursión.

---

## 🤝 Contribuir

Lee [`CONTRIBUTING.md`](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md). Todo PR debe
pasar `python3 scripts/validate.py` (el mismo check corre en CI). Para reportar fallos de seguridad,
sigue [`SECURITY.md`](SECURITY.md).

---

## 📄 Licencia

Distribuido bajo la licencia **Apache 2.0**. Ver [`LICENSE`](LICENSE) y [`NOTICE`](NOTICE).
Puedes usar, modificar y embeber este motor (p. ej. como submodule en un SaaS) manteniendo los
avisos de copyright y licencia. Incluye concesión expresa de patentes.
