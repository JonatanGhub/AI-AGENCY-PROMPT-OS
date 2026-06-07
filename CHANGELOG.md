# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el versionado del motor se rige por [`registry/versioning.md`](registry/versioning.md).

## [Unreleased]

### Added
- **`core/output-evaluator`**: nuevo microservicio de calidad que puntúa el output de cualquier
  módulo contra una rúbrica fija de 6 dimensiones y emite veredicto `pass`/`revise`/`reject`.
- Bloque opcional **`quality`** en `schemas/output.schema.json` (campo opcional → MINOR, no rompe
  contrato) para alojar la evaluación.
- Dos ejemplos end-to-end nuevos: `examples/devflow-pr-reviewer` (B2B dev-tools, `blueprint-mvp`)
  y `examples/lumina-creator-monetization` (creator economy, `growth-loop`).

### Changed
- `scripts/validate.py`: además de las claves requeridas, comprueba que `meta.workflow` de cada
  `input.json` referencie un workflow existente.
- Registry (`prompt-index`, `manifest`, `dependency-map`) actualizado: 21 prompts ejecutables.

## [1.0.0] - 2026-05-30

### Added
- **Núcleo de orquestación**: `core/orchestrator` (descompone, delega, consolida, decide)
  y `core/workflow-engine` (ejecuta workflows declarativos), más la plantilla canónica
  `core/_prompt-template.md` y `core/decision-log.schema.md`.
- **18 microservicios cognitivos** en 6 departamentos: product, growth, sales, operations,
  finance, ai-engineering.
- **4 workflows**: `full-business-build`, `growth-loop`, `sales-funnel` y `blueprint-mvp`
  (este último mapea al "Compiler" del MVP de un SaaS consumidor).
- **Contratos**: `schemas/input.schema.json`, `schemas/output.schema.json`,
  `schemas/decision.schema.json` y `registry/manifest.schema.json`.
- **Registry**: `manifest.json` (fuente de verdad legible por máquina), `prompt-index.md`,
  `dependency-map.md`, `versioning.md`.
- **Tooling**: `scripts/validate.py` (validador de integridad sin dependencias) y
  `scripts/run_workflow.py` (runner determinista manifiesto → plan), con CI en
  `.github/workflows/validate.yml`.
- **Operación como agencia**: `docs/agency-playbook.md`, scaffolding `clients/` + template.
- **Integración como motor de SaaS**: `docs/integration-acos.md` con el contrato y la receta
  de consumo vía git submodule.
- **Documentación**: README, `docs/architecture.md` (diagramas), `CONTRIBUTING.md`, ejemplo
  end-to-end `examples/ai-tutor-oposiciones`.

[Unreleased]: https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS/releases/tag/v1.0.0
