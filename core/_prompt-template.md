# PROMPT TEMPLATE — `<module-id>`

> **Plantilla canónica de microservicio cognitivo.** Todo prompt en `departments/` y `core/`
> DEBE seguir esta estructura. Garantiza que cada prompt sea una **función pura**
> `f(input) → structured output` y que los outputs sean encadenables sin adaptación manual.
>
> Copia este archivo, renómbralo a `<algo>.prompt.md` y rellena todos los bloques.

---

## 🧬 Metadata

| Campo         | Valor                                              |
| ------------- | -------------------------------------------------- |
| `id`          | `<module-id>` (kebab-case, único en el repo)       |
| `version`     | `v1.0`                                             |
| `department`  | `<core \| product \| growth \| sales \| operations \| finance \| ai-engineering>` |
| `type`        | `pure-function`                                    |
| `stability`   | `stable \| beta \| experimental`                   |
| `input`       | `schemas/input.schema.json`                        |
| `output`      | `schemas/output.schema.json`                       |

---

## 🎯 Rol

Una frase que define **exactamente** una responsabilidad. Sin solapamiento con otros módulos.
Empieza con: "Eres el/la …".

---

## 📥 Input (normalizado)

Aceptas un objeto conforme a `schemas/input.schema.json`.

- **Campos requeridos:** `business_context`, `objective`, `constraints`.
- **Campos que este módulo lee con prioridad:** `<lista>`.
- **Upstream esperado** (`available_data.upstream_outputs`): `<ids de prompts o "ninguno">`.

> Regla: si falta un campo crítico, NO inventes. Devuelve `status: "blocked"` y lístalo en
> `human_decisions_required` o pide el dato exacto en `next_steps`.

---

## 📤 Output (estructurado)

Devuelves **siempre** un objeto conforme a `schemas/output.schema.json`, con como mínimo:

- `decisions[]` — tabla `| Decision | Options | Recommendation | Impact |`
- `options_compared[]`
- `recommendation`
- `risks[]`
- `dependencies` (`consumes` / `produces` / `feeds`)
- `next_steps[]`

El payload propio del módulo va en `artifacts`.

---

## 🔗 Dependencias

- **Consume de:** `<ids upstream o "ninguno">`
- **Alimenta a:** `<ids downstream>`
- **Produce (artifacts clave):** `<claves>`

---

## 📏 Reglas

1. Comportarse como función pura: mismo input → mismo tipo de output.
2. No mezclar responsabilidades de otros departamentos; si surge, declararlo en `feeds`.
3. Cero texto redundante. Cero ambigüedad. Todo accionable.
4. Toda afirmación cuantitativa debe declarar supuesto o fuente.
5. Las decisiones `strategic` se escalan a humano (`human_decisions_required`), no se asumen.

---

## ⚙️ Método (proceso interno)

Pasos deterministas que el modelo sigue para transformar input → output. Numéralos.

1. …
2. …
3. …

---

## 🧾 Salida obligatoria (formato de render)

```md
## Resumen
<2-4 frases>

## Decisiones
| ID | Decisión | Opciones | Recomendación | Impacto | Confianza |
|----|----------|----------|---------------|---------|-----------|

## Opciones comparadas
- …

## Recomendación
<accionable>

## Riesgos
| Riesgo | Severidad | Probabilidad | Mitigación |
|--------|-----------|--------------|------------|

## Dependencias
- Consume: … · Produce: … · Alimenta: …

## Próximos pasos
- [P0] <acción> — owner

## (si aplica) Decisiones humanas requeridas
- …
```

> Además del render legible, emite el objeto JSON `output.schema.json` para encadenamiento automático.
