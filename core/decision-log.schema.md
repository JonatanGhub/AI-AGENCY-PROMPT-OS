# Decision Log — Schema & Protocol

> Memoria de decisiones persistente del sistema, mantenida por `orchestrator`.
> Es la **fuente de verdad** sobre qué se decidió, por qué y con qué impacto a lo largo de un workflow.
> Cada entrada es un `decision.schema.json` enriquecido con trazabilidad de ejecución.

---

## Propósito

1. Evitar que el sistema repita o contradiga decisiones ya tomadas.
2. Permitir auditoría: cualquier output es trazable hasta su decisión origen.
3. Habilitar reanudación de workflows: el estado vive en el log, no en el contexto.

---

## Estructura de una entrada

```json
{
  "id": "D-001",
  "run_id": "<workflow run id>",
  "timestamp": "2026-05-29T10:00:00Z",
  "source_module": "growth-engine",
  "decision": "Canal primario de adquisición",
  "options": ["SEO/contenido", "Paid ads", "Outbound"],
  "recommendation": "SEO/contenido como motor primario; paid como acelerador validado.",
  "impact": "high",
  "confidence": "medium",
  "reversible": true,
  "owner": "growth",
  "depends_on": ["D-000"],
  "status": "accepted",
  "superseded_by": null
}
```

`status` ∈ `proposed | accepted | rejected | escalated | superseded`.

---

## Tabla de render canónica

| ID | Módulo | Decisión | Recomendación | Impacto | Confianza | Estado |
|----|--------|----------|---------------|---------|-----------|--------|
| D-001 | growth-engine | Canal primario | SEO + paid acelerador | high | medium | accepted |

---

## Protocolo del orquestador

1. **Append-only:** nunca se borra una decisión; se marca `superseded` y se enlaza la nueva vía `superseded_by`.
2. **Conflicto = nueva entrada `escalated`** si afecta a >1 departamento y `impact ∈ {high, strategic}`.
3. **`impact: strategic` ⇒ `status: escalated`** y se añade a `human_decisions_required` del output.
4. Toda decisión de un módulo downstream que dependa de otra debe rellenar `depends_on`.
5. El log se incluye en `artifacts.decision_log` del output del orquestador para encadenamiento.

---

## Invariantes

- Ningún `id` se reutiliza.
- Una decisión `rejected` o `superseded` nunca debe alimentar módulos downstream.
- Si dos decisiones `accepted` se contradicen, es un bug del orquestador → forzar reconciliación.
