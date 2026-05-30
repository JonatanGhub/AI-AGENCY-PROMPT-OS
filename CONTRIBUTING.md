# Contribuir al AI Agency Prompt OS

Cada prompt es código. Contribuye con la misma disciplina que a un sistema de software:
contratos estables, sin redundancia, todo ejecutable.

## Principios

- Un prompt = **una responsabilidad** (función pura `f(input) → structured output`).
- El **contrato es sagrado**: mientras `consumes` / `produces` / `artifacts` no cambien, los módulos
  downstream no se rompen.
- Sin texto redundante, sin ambigüedad, sin mezcla de responsabilidades.

## Añadir o modificar un prompt

1. Copia [`core/_prompt-template.md`](core/_prompt-template.md) a `departments/<dept>/<id>.prompt.md`.
2. Rellena Metadata, Rol, Input, Método, Salida obligatoria, Dependencias (`consumes`/`feeds`) y Reglas.
3. Regístralo en:
   - [`registry/prompt-index.md`](registry/prompt-index.md) — catálogo legible.
   - [`registry/dependency-map.md`](registry/dependency-map.md) — aristas del grafo.
   - [`registry/manifest.json`](registry/manifest.json) — **fuente de verdad legible por máquina**.
4. Versiona según [`registry/versioning.md`](registry/versioning.md).
5. Ejecuta el validador (ver abajo). Debe pasar antes de abrir PR.

> El grafo debe seguir siendo un **DAG**. Las relaciones bidireccionales legítimas
> (`pricing-strategy ⇄ unit-economics`, `financial-scenarios ⇄ scaling-ops`) se resuelven por
> iteración explícita en el workflow, nunca por recursión.

## Validar localmente

```bash
python3 scripts/validate.py
```

Sin dependencias externas. Comprueba: JSON de schemas válido, cada prompt registrado en el index,
sin referencias colgantes, manifiesto sincronizado con el disco, inputs de ejemplo válidos.
El mismo check corre en CI ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)).

## Commits y PRs

- Mensajes de commit descriptivos con prefijo de tipo: `feat(growth): …`, `docs: …`, `ci: …`.
- Un PR por cambio coherente. Abre el PR en **draft** hasta que CI esté en verde.
- Si el cambio rompe un contrato (MAJOR), añade nota de migración en el changelog del prompt y revisa
  todos los módulos que lo declaran en `consumes`.

## Estructura del repo

Ver [`README.md`](README.md) para el árbol completo y cómo ejecutar workflows con Claude Code.
