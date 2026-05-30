# Ejecución de ejemplo — `full-business-build` sobre **OpoCoach**

> Demuestra cómo los outputs de un módulo alimentan al siguiente **sin adaptación manual**.
> Input: [`input.json`](input.json). Workflow: [`full-business-build`](../../workflows/full-business-build.workflow.md).
>
> Por brevedad se muestran 3 módulos como objeto `output.schema.json` completo (para evidenciar el
> encadenamiento) y el resto resumido. El cierre es el render consolidado del `orchestrator`.

---

## Paso 1 — `product-builder`  (consume: —)

```json
{
  "module": "product-builder",
  "version": "v1.0",
  "run_id": "example-ai-tutor-001",
  "status": "complete",
  "summary": "OpoCoach se enfoca en el opositor autodidacta que pierde tiempo sin feedback. MVP: plan adaptativo + tests explicados sobre 1 oposición piloto.",
  "decisions": [
    { "id": "D-001", "decision": "Alcance del MVP", "options": ["3 oposiciones", "1 oposición piloto"], "recommendation": "1 oposición piloto para validar feedback adaptativo", "impact": "high", "confidence": "high" }
  ],
  "options_compared": [
    { "option": "Plataforma multi-oposición desde día 1", "pros": ["Más TAM"], "cons": ["Dispersa el contenido", "Retrasa el MVP"], "selected": false },
    { "option": "1 oposición piloto", "pros": ["Foco", "Time-to-market"], "cons": ["TAM inicial menor"], "selected": true }
  ],
  "recommendation": "Lanzar con 1 oposición de alta demanda; expandir tras validar retención.",
  "risks": [
    { "risk": "Temario desactualizado", "severity": "high", "likelihood": "medium", "mitigation": "Pipeline de revisión trimestral del temario oficial" }
  ],
  "dependencies": { "consumes": [], "produces": ["value_proposition", "mvp_scope", "icp"], "feeds": ["ai-architecture", "growth-engine", "pricing-strategy"] },
  "artifacts": {
    "value_proposition": "Aprueba antes: tu tutor de IA que sabe qué estudiar hoy y por qué fallas.",
    "icp": "Opositor autodidacta, 25-35, estudia 2-4h/día, sin academia.",
    "mvp_scope": { "must_have": ["Plan adaptativo", "Banco de tests con explicaciones", "Simulacro corregido"], "later": ["Comunidad", "Flashcards", "App móvil"] },
    "differentiators": ["Feedback explicado por IA", "Plan que se reordena según errores"]
  },
  "next_steps": [{ "action": "Validar temario piloto con 5 opositores", "owner": "human", "priority": "P0" }]
}
```

## Paso 4 — `growth-engine`  (consume: `product-builder`)

> Lee `artifacts.icp` y `artifacts.value_proposition` del paso 1 desde `available_data.upstream_outputs`.

```json
{
  "module": "growth-engine",
  "version": "v1.0",
  "run_id": "example-ai-tutor-001",
  "status": "complete",
  "summary": "Modelo content-led aprovechando la audiencia orgánica del fundador; loop de contenido educativo → registro freemium → activación con primer simulacro.",
  "decisions": [
    { "id": "D-010", "decision": "Modelo de crecimiento dominante", "options": ["paid-led", "content-led", "sales-led"], "recommendation": "content-led (hay audiencia y CAC bajo)", "impact": "high", "confidence": "medium" }
  ],
  "options_compared": [
    { "option": "Paid ads desde día 1", "pros": ["Rápido"], "cons": ["Quema budget pre-PMF"], "selected": false },
    { "option": "Content-led sobre audiencia existente", "pros": ["CAC bajo", "Aprovecha 2.000 seguidores"], "cons": ["Más lento de escalar"], "selected": true }
  ],
  "recommendation": "Content-led + freemium; paid solo como acelerador tras validar activación.",
  "risks": [
    { "risk": "Dependencia de un solo canal/creador", "severity": "medium", "likelihood": "medium", "mitigation": "Diversificar a SEO de long-tail por tema de temario" }
  ],
  "dependencies": { "consumes": ["product-builder"], "produces": ["growth_model", "north_star_metric", "primary_channels"], "feeds": ["funnel-designer", "unit-economics", "sales-system"] },
  "artifacts": {
    "growth_model": "content-led + freemium",
    "north_star_metric": "Simulacros completados por usuario activo / semana",
    "primary_channels": ["YouTube/Shorts del fundador", "SEO long-tail por tema", "Email"],
    "growth_loops": ["Contenido gratuito que resuelve una duda → CTA al test gratuito → resultado compartible → nuevo contenido"]
  },
  "next_steps": [{ "action": "Definir funnel y eventos de tracking", "owner": "funnel-designer", "priority": "P0" }]
}
```

## Paso 6 — `unit-economics`  (consume: `growth-engine`, `funnel-designer`, `pricing-strategy`, `model-selection`)

> Combina `primary_channels` (growth), conversiones (funnel), `pricing_model` (29 €/mes) y
> `cost_per_request` (model-selection) para validar el **gate económico** del workflow.

```json
{
  "module": "unit-economics",
  "version": "v1.0",
  "run_id": "example-ai-tutor-001",
  "status": "complete",
  "summary": "Con CAC content-led ~12 € y ARPU 29 €/mes a 8 meses de vida media, LTV:CAC ≈ 15 y payback < 1 mes. El coste de IA se mantiene en ~18% del precio (bajo el límite del 25%).",
  "decisions": [
    { "id": "D-020", "decision": "¿Viable para escalar gasto?", "options": ["Sí", "No, iterar"], "recommendation": "Sí; unit economics holgado", "impact": "high", "confidence": "medium" }
  ],
  "options_compared": [],
  "recommendation": "Economía sólida en el escenario base; principal sensibilidad es el churn.",
  "risks": [
    { "risk": "Churn alto tras aprobar/abandonar la oposición", "severity": "high", "likelihood": "high", "mitigation": "Multi-oposición y planes anuales para alargar vida media" }
  ],
  "dependencies": { "consumes": ["growth-engine", "funnel-designer", "pricing-strategy", "model-selection"], "produces": ["ltv_cac_ratio", "payback_months", "gross_margin"], "feeds": ["financial-scenarios", "scaling-ops"] },
  "artifacts": {
    "cac_by_channel": { "content": 12, "paid": 45 },
    "ltv": 180,
    "ltv_cac_ratio": 15,
    "payback_months": 0.5,
    "gross_margin": 0.78,
    "assumptions": ["Vida media 8 meses", "Conversión free→paid 6%", "Coste IA 5,2 €/usuario/mes"]
  },
  "next_steps": [{ "action": "Modelar escenarios y runway", "owner": "financial-scenarios", "priority": "P0" }]
}
```

---

## Pasos restantes (resumen)

| # | Módulo | Decisión clave (artifact) |
|---|--------|---------------------------|
| 2 | `ai-architecture` | Patrón **RAG** sobre temario oficial + tool-use para corregir tests. NFR: coste/latencia, eval de exactitud. |
| 3 | `model-selection` | Modelo capaz para explicaciones, modelo pequeño para clasificar errores; `cost_per_request` ≈ 0,01 €. |
| 5 | `pricing-strategy` | Suscripción 29 €/mes (mensual) + plan anual con descuento; value metric = acceso a tutor adaptativo. |
| 7 | `sales-system` | **Self-serve** (coherente con ticket bajo); sin equipo de ventas; activación = primer simulacro. |
| 8 | `ops-automation` | Onboarding y corrección automatizados; soporte asistido por IA con handoff humano para bajas. |
| 9 | `financial-scenarios` | Base: breakeven mes 7, runway 9 meses con 40k €; capital extra opcional para acelerar paid. |
| 10 | `scaling-ops` | Escalar por sistema (contenido + IA) antes que headcount; primer hire: content ops al 3x. |

---

## Paso 11 — `orchestrator`  (merge final)

```md
## Resumen ejecutivo
OpoCoach es viable como SaaS content-led con economía holgada (LTV:CAC ≈ 15). El plan: MVP de 1
oposición en 90 días, crecimiento orgánico sobre la audiencia del fundador, self-serve, y foco en
mitigar el churn estructural del nicho (el opositor se va al aprobar).

## Decisiones clave (consolidadas)
| ID | Decisión | Recomendación | Impacto | Origen |
|----|----------|---------------|---------|--------|
| D-001 | Alcance MVP | 1 oposición piloto | high | product-builder |
| D-010 | Modelo de crecimiento | content-led + freemium | high | growth-engine |
| D-020 | Escalar gasto | Sí (economía sólida) | high | unit-economics |

## Conflictos detectados y resolución
| Conflicto | Módulos | Resolución | Criterio |
|-----------|---------|------------|----------|
| Paid agresivo (growth temprano) vs. runway limitado (finanzas) | growth-engine ⇄ financial-scenarios | Paid solo tras validar activación | Proteger runway pre-PMF |

## Recomendación final
Construir el MVP de 1 oposición, crecer content-led, y atacar el churn con multi-oposición + plan
anual en la fase 2. Diferir paid hasta validar la activación (primer simulacro completado).

## Decisiones humanas requeridas
- Elegir la oposición piloto (depende de demanda y disponibilidad de temario actualizado).

## Próximo workflow a ejecutar
`growth-loop` — para detallar funnel, contenido y validar la activación antes de escalar gasto.
```

---

### Qué demuestra este ejemplo

1. **Contrato de entrada único** (`input.json`) válido para todo el workflow.
2. **Encadenamiento sin fricción:** `growth-engine` consume el `icp`/`value_proposition` de
   `product-builder`; `unit-economics` combina growth + pricing + coste de IA.
3. **Gating económico:** `unit-economics` actúa como puerta antes de recomendar escalar gasto.
4. **Consolidación y resolución de conflictos** por el `orchestrator`, con Decision Log y siguiente workflow.
