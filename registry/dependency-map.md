# Dependency Map — Grafo de Encadenamiento

> Mapa autoritativo de `consumes` / `feeds` entre prompts. El `workflow-engine` lo usa para el
> ordenamiento topológico; el `orchestrator` para componer workflows ad-hoc. Debe ser un DAG (sin ciclos).

## Tabla de dependencias

| Módulo | Consume de (upstream) | Alimenta a (downstream) |
|--------|------------------------|--------------------------|
| `product-builder` | — | `ai-architecture`, `ux-strategy`, `roadmap-generator`, `growth-engine`, `pricing-strategy`, `ops-automation` |
| `ux-strategy` | `product-builder` | `roadmap-generator`, `funnel-designer`, `growth-engine` |
| `roadmap-generator` | `product-builder`, `ux-strategy`, `ai-architecture` | `ops-automation`, `scaling-ops`, `financial-scenarios` |
| `growth-engine` | `product-builder`, `ux-strategy` | `funnel-designer`, `content-strategy`, `sales-system`, `unit-economics` |
| `funnel-designer` | `growth-engine`, `ux-strategy` | `sales-system`, `content-strategy`, `unit-economics` |
| `content-strategy` | `growth-engine`, `funnel-designer` | `sales-system`, `ops-automation` |
| `sales-system` | `growth-engine`, `funnel-designer`, `pricing-strategy` | `crm-automation`, `closing-playbooks`, `ops-automation`, `financial-scenarios` |
| `crm-automation` | `sales-system` | `ops-automation`, `closing-playbooks` |
| `closing-playbooks` | `sales-system`, `pricing-strategy`, `crm-automation` | (humano: sales enablement) |
| `ops-automation` | `sales-system`, `crm-automation`, `product-builder`, `roadmap-generator`, `agent-design` | `workflow-designer`, `scaling-ops` |
| `workflow-designer` | `ops-automation` | `scaling-ops` |
| `scaling-ops` | `ops-automation`, `workflow-designer`, `financial-scenarios`, `roadmap-generator` | `orchestrator` |
| `pricing-strategy` | `product-builder`, `unit-economics` | `sales-system`, `closing-playbooks`, `financial-scenarios`, `unit-economics` |
| `unit-economics` | `growth-engine`, `funnel-designer`, `pricing-strategy`, `model-selection` | `financial-scenarios`, `pricing-strategy`, `scaling-ops` |
| `financial-scenarios` | `unit-economics`, `pricing-strategy`, `growth-engine`, `scaling-ops` | `orchestrator`, `scaling-ops` |
| `ai-architecture` | `product-builder` | `model-selection`, `agent-design`, `roadmap-generator`, `ops-automation` |
| `model-selection` | `ai-architecture` | `agent-design`, `unit-economics`, `ops-automation` |
| `agent-design` | `ai-architecture`, `model-selection` | `ops-automation` |

## Ciclos controlados (soft dependencies)

Existen dependencias bidireccionales **resueltas por iteración**, no por ciclo en una sola ejecución:

- `pricing-strategy ⇄ unit-economics`: en la primera pasada, `pricing-strategy` corre con supuestos;
  `unit-economics` los valida; el `orchestrator` puede re-disparar `pricing-strategy` con feedback.
- `financial-scenarios ⇄ scaling-ops`: `scaling-ops` consume escenarios; el plan de hiring resultante
  puede refinar `financial-scenarios` en una segunda iteración.

> Regla: dentro de **una** ejecución de `workflow-engine`, cada módulo corre una vez. Las relaciones
> ⇄ se materializan como un segundo paso explícito en el workflow, nunca como recursión implícita.

## Raíces y hojas

- **Raíz** (sin upstream): `product-builder`.
- **Sumideros** (alimentan al merge): `scaling-ops`, `financial-scenarios`, `closing-playbooks` → `orchestrator`.
