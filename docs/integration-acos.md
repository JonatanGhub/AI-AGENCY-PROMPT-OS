# Integración: este repo (motor) ⇄ ACOS (SaaS)

> **ADR / contrato de integración.** Decisión: `ai-agency-prompt-os` es el **motor reutilizable**
> (prompts + schemas + manifiesto + orquestación). **ACOS** (*AI Company Operating System*) es el
> **SaaS** que lo consume. Cerebro (este repo) + cuerpo (ACOS).

---

## 1. Por qué encajan

ACOS define tres engines —**Orchestrator · Compiler · Exporter**— y un pipeline "schema-typed" que
convierte una idea en un *AI-Business Blueprint*. Dos de esos tres **ya existen aquí**:

| Engine de ACOS | Lo aporta… | Artefacto en este repo |
|----------------|-----------|------------------------|
| **Orchestrator** | este repo | `core/orchestrator.prompt.md` + `core/workflow-engine.prompt.md` |
| **Compiler** | este repo | `departments/*` + `schemas/*` + `registry/manifest.json` + `scripts/run_workflow.py` |
| **Exporter** | **ACOS** | render del `output.schema.json` a artefactos compartibles (PDF/enlace) |
| App, UI, auth, billing, llamada al LLM | **ACOS** | runtime Next.js |

El *blueprint* que promete ACOS (market, product, business model, AI/agent architecture, roadmap,
unit-economics) es justo lo que producen los módulos `product-builder`, `ai-architecture`,
`growth-engine`, `pricing-strategy`, `unit-economics`, `roadmap-generator`.

---

## 2. La frontera (qué consume ACOS, qué construye ACOS)

**ACOS consume de este repo (no reimplementa):**
- `schemas/input.schema.json`, `schemas/output.schema.json`, `schemas/decision.schema.json`
  → el **tipado del pipeline** de ACOS.
- `registry/manifest.json` → el **grafo** que el Compiler de ACOS recorre.
- `departments/*.prompt.md` + `core/*.prompt.md` → el **contenido** de cada paso del Compiler.

**ACOS construye encima (no está aquí, ni debe estarlo):**
- El **runtime** que ejecuta el manifiesto llamando al LLM (este repo es determinista y *no* llama a LLMs).
- El **Exporter** (blueprint → artefacto compartible).
- UI, auth, billing, persistencia.

> ⚠️ **Regla anti-divergencia:** ACOS **no** debe escribir su propio orquestador ni sus propios
> schemas. Si lo hace, habrá dos fuentes de verdad que divergen. El Orchestrator de ACOS es el *código*
> que ejecuta `core/orchestrator.prompt.md`; sus tipos son los `schemas/` de aquí.

---

## 3. Cómo lo consume (mecanismo)

Recomendado, en orden de preferencia:

1. **Git submodule** de este repo dentro de ACOS (`/engine`), fijado a un tag de versión.
2. **Vendorizado** (copiar `schemas/`, `registry/manifest.json`, `core/`, `departments/` a `/engine`)
   con un script de sync.
3. Publicar el motor como **paquete versionado** y que ACOS lo declare como dependencia.

En los tres casos, **ACOS fija una versión** del motor (ver `registry/versioning.md`) y actualiza
deliberadamente. El validador (`scripts/validate.py`) garantiza que el motor publicado es íntegro.

### Receta: añadir el motor como submodule en ACOS

Ejecutar **en el repositorio de ACOS** (no en este):

```bash
# 1. Añadir este repo como submodule en /engine
git submodule add https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS.git engine
git -C engine checkout main          # o un tag de versión: git -C engine checkout v1.0

# 2. Commit del puntero del submodule
git add .gitmodules engine
git commit -m "chore: add ai-agency-prompt-os as engine submodule"

# 3. Quien clone ACOS luego usa:
git clone --recurse-submodules <url-de-acos>
# o, si ya clonó: git submodule update --init --recursive

# 4. Actualizar el motor a una nueva versión, deliberadamente:
git -C engine fetch && git -C engine checkout <tag-o-main>
git add engine && git commit -m "chore: bump engine to <version>"
```

Desde el runtime de ACOS, el Compiler lee `engine/registry/manifest.json` y los prompts en
`engine/core` + `engine/departments`, y tipa con `engine/schemas/*`. El validador del motor puede
correrse en el CI de ACOS con `python3 engine/scripts/validate.py`.

---

## 4. El "Compiler" del MVP de ACOS

ACOS recorta el MVP a **Compiler + Export** para solopreneurs. Su pipeline = el workflow
[`blueprint-mvp`](../workflows/blueprint-mvp.workflow.md) de este repo (subconjunto de
`full-business-build`):

```
product-builder → ai-architecture → growth-engine → pricing-strategy → unit-economics → roadmap-generator → orchestrator
```

Cubre exactamente las secciones del blueprint de ACOS. El resto de módulos (sales, ops, content,
agentes…) son el **roadmap post-MVP** de ACOS: ya están escritos, se activan añadiéndolos al pipeline.

Probarlo:

```bash
python3 scripts/run_workflow.py blueprint-mvp examples/ai-tutor-oposiciones/input.json
```

---

## 5. Mapeo de responsabilidades (resumen)

| | `ai-agency-prompt-os` (motor) | ACOS (SaaS) |
|---|---|---|
| Qué es | Prompts + contratos + grafo | App Next.js + UI + export |
| Ejecuta LLM | No (determinista) | Sí |
| Orquestación | Spec (`orchestrator.prompt.md`) | Runtime que la ejecuta |
| Contratos | Define los schemas | Los consume como tipos |
| Multi-cliente | `clients/` (agencia) | Multi-usuario (SaaS) |
| Versionado | Semver del motor | Fija una versión del motor |

---

## 6. Decisiones abiertas para ACOS (no para este repo)

- Mecanismo exacto de consumo (submodule vs. vendor vs. paquete).
- Marca: ¿`ai-agency-prompt-os` público/interno y ACOS comercial encima? (decisión de negocio).
- Formato de export del Exporter (PDF, página compartible, Notion, etc.).
