# Prompt Index — Registro de Microservicios Cognitivos

> Catálogo único y autoritativo de todos los prompts del sistema. El `orchestrator` consulta este
> índice antes de delegar. Mantener sincronizado al añadir/versionar prompts.
>
> **Versión legible por máquina:** [`manifest.json`](manifest.json) (validada por `scripts/validate.py`).
> Para recorrer el grafo programáticamente con Cloud Code, usa el manifiesto; este archivo es la vista humana.

## Core

| id | archivo | tipo | versión | resumen |
|----|---------|------|---------|---------|
| `orchestrator` | `core/orchestrator.prompt.md` | coordinator | v1.0 | Descompone, delega, consolida, decide. |
| `workflow-engine` | `core/workflow-engine.prompt.md` | executor | v1.0 | Ejecuta workflows declarativos de prompts. |
| `_prompt-template` | `core/_prompt-template.md` | template | v1.0 | Plantilla canónica de microservicio. |

## Product

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `product-builder` | `departments/product/product-builder.prompt.md` | v1.0 | Idea → definición de producto + MVP. |
| `ux-strategy` | `departments/product/ux-strategy.prompt.md` | v1.0 | Flujos, momento aha, activación. |
| `roadmap-generator` | `departments/product/roadmap-generator.prompt.md` | v1.0 | Fases, hitos, criterios de salida. |

## Growth

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `growth-engine` | `departments/growth/growth-engine.prompt.md` | v1.0 | Modelo de crecimiento, canales, loops, NSM. |
| `funnel-designer` | `departments/growth/funnel-designer.prompt.md` | v1.0 | Funnel AARRR con métricas por etapa. |
| `content-strategy` | `departments/growth/content-strategy.prompt.md` | v1.0 | Pilares, formatos, distribución. |

## Sales

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `sales-system` | `departments/sales/sales-system.prompt.md` | v1.0 | Modelo de ventas, pipeline, calificación. |
| `crm-automation` | `departments/sales/crm-automation.prompt.md` | v1.0 | Triggers, secuencias, scoring. |
| `closing-playbooks` | `departments/sales/closing-playbooks.prompt.md` | v1.0 | Discovery, objeciones, cierre. |

## Operations

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `ops-automation` | `departments/operations/ops-automation.prompt.md` | v1.0 | Procesos core, mapa de automatización, SLAs. |
| `workflow-designer` | `departments/operations/workflow-designer.prompt.md` | v1.0 | Workflows operativos paso a paso. |
| `scaling-ops` | `departments/operations/scaling-ops.prompt.md` | v1.0 | Capacidad, breakpoints, plan de escalado. |

## Finance

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `pricing-strategy` | `departments/finance/pricing-strategy.prompt.md` | v1.0 | Value metric, modelo, tiers, anchor. |
| `unit-economics` | `departments/finance/unit-economics.prompt.md` | v1.0 | CAC, LTV, márgenes, payback. |
| `financial-scenarios` | `departments/finance/financial-scenarios.prompt.md` | v1.0 | Escenarios, runway, breakeven, capital. |

## AI Engineering

| id | archivo | versión | resumen |
|----|---------|---------|---------|
| `ai-architecture` | `departments/ai-engineering/ai-architecture.prompt.md` | v1.0 | Patrón, componentes, flujo de datos, NFR. |
| `model-selection` | `departments/ai-engineering/model-selection.prompt.md` | v1.0 | Modelo por tarea, routing, coste. |
| `agent-design` | `departments/ai-engineering/agent-design.prompt.md` | v1.0 | Agentes, tools, guardrails, handoff. |

## Workflows

| id | archivo | versión |
|----|---------|---------|
| `full-business-build` | `workflows/full-business-build.workflow.md` | v1.0 |
| `growth-loop` | `workflows/growth-loop.workflow.md` | v1.0 |
| `sales-funnel` | `workflows/sales-funnel.workflow.md` | v1.0 |
| `blueprint-mvp` | `workflows/blueprint-mvp.workflow.md` | v1.0 |

**Total:** 21 prompts (3 core + 18 departamento) · 4 workflows · 3 schemas.
