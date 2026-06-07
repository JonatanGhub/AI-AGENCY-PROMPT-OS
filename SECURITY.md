# Política de seguridad

## Alcance

Este repositorio es un **motor de prompts determinista**: no ejecuta LLMs, no realiza
llamadas de red y no maneja secretos ni datos de usuarios en tiempo de ejecución. El único
código ejecutable es Python de utilidad (`scripts/validate.py`, `scripts/run_workflow.py`)
que opera sobre archivos locales del repo, **sin dependencias externas**.

Aun así, nos tomamos en serio cualquier problema de seguridad.

## Qué reportar

- Vulnerabilidades en los scripts de `scripts/` (p. ej. lectura de rutas no controlada).
- Contenido en prompts que pueda inducir comportamiento inseguro al ejecutarse en un agente.
- Fugas accidentales de secretos o datos sensibles en el historial del repo.

## Cómo reportar

Por favor **no abras un issue público** para vulnerabilidades. Usa los
[GitHub Security Advisories](https://github.com/JonatanGhub/AI-AGENCY-PROMPT-OS/security/advisories/new)
del repositorio, o contacta de forma privada al mantenedor.

Intentaremos confirmar la recepción en un plazo razonable y mantenerte al tanto de la resolución.

## Nota para consumidores (SaaS)

Si embebes este motor (p. ej. como submodule) en una aplicación que **sí** llama a un LLM,
la validación de inputs/outputs, el manejo de secretos y los guardrails de ejecución son
responsabilidad de la aplicación consumidora. Ver [`docs/integration-acos.md`](docs/integration-acos.md).
