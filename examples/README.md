# Examples — Ejecuciones de referencia

Ejemplos end-to-end que demuestran el sistema en funcionamiento: un `input.json` normalizado
y la ejecución encadenada de un workflow, mostrando cómo el output de cada módulo alimenta al
siguiente sin adaptación manual.

| Ejemplo | Workflow | Qué demuestra |
|---------|----------|---------------|
| [`ai-tutor-oposiciones/`](ai-tutor-oposiciones/) | `full-business-build` | Diseño completo de un SaaS B2C de IA: encadenamiento de 10 módulos + merge del orquestador, con gating económico. |

## Cómo usar un ejemplo con Cloud Code

> "Carga `examples/ai-tutor-oposiciones/input.json` como input. Actúa como `core/orchestrator` y
> ejecuta el workflow `full-business-build`. Devuelve el output consolidado conforme a
> `schemas/output.schema.json`."

El archivo `*.run.md` de cada ejemplo es una **referencia esperada** del resultado (abreviada),
útil para entender el formato y verificar que tu ejecución produce algo equivalente.

## Validación

Los `input.json` de los ejemplos se comprueban en CI (`scripts/validate.py`): deben ser JSON
bien formado y declarar las claves requeridas por `schemas/input.schema.json`
(`business_context`, `objective`, `constraints`).
