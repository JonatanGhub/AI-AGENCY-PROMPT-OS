# Versioning — Política de Versionado de Prompts

> Cada prompt es código. Se versiona, se cambia con disciplina y mantiene compatibilidad de contrato.

## Esquema de versión

`vMAJOR.MINOR` (ej. `v1.0`, `v1.1`, `v2.0`).

| Cambio | Incremento | Ejemplo |
|--------|------------|---------|
| Rompe el contrato de I/O (cambia `consumes`/`produces`, claves de `artifacts`) | **MAJOR** | `v1.3 → v2.0` |
| Mejora método/reglas sin romper contrato | **MINOR** | `v1.0 → v1.1` |
| Typo / wording sin efecto funcional | sin bump (commit normal) | — |

## Reglas de compatibilidad

1. **El contrato es sagrado.** Mientras `consumes` / `produces` / `artifacts` no cambien, los módulos
   downstream no deben romperse. Eso permite mejorar prompts sin reescribir el sistema.
2. Un cambio **MAJOR** obliga a revisar todos los módulos que lo declaran en `consumes`
   (ver `registry/dependency-map.md`) y actualizar `registry/prompt-index.md`.
3. Mantener compatibilidad hacia atrás un ciclo cuando sea posible (aceptar input viejo y nuevo).

## Definición de versión en cada prompt

Toda cabecera de prompt declara `version` en su tabla de Metadata. La fuente de verdad del estado
actual es `registry/prompt-index.md`.

## Changelog por prompt (formato sugerido)

Añadir al final del `.prompt.md` cuando aplique:

```md
## Changelog
- v1.1 — Añadido routing por coste en `method`. Contrato sin cambios.
- v1.0 — Versión inicial.
```

## Versionado de workflows y schemas

- **Workflows**: versionan igual; un cambio de secuencia que altere dependencias es MAJOR.
- **Schemas** (`schemas/*.json`): un cambio de `required` o eliminación de campo es MAJOR del sistema
  completo (afecta a todos los prompts). Añadir campo opcional es MINOR.

## Flujo de release

1. Editar el `.prompt.md` y su `version`.
2. Actualizar `registry/prompt-index.md`, `registry/manifest.json` (versión y aristas) y, si cambió
   el contrato, `registry/dependency-map.md`.
3. Ejecutar `python3 scripts/validate.py` (debe pasar: detecta drift entre manifiesto, index y disco).
4. Commit descriptivo (`feat(growth): growth-engine v1.1 — …`).
5. Si es MAJOR, nota de migración en el changelog del prompt.
