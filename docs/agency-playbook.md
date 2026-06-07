# Agency Playbook — Operar el Prompt OS con múltiples clientes

> Cómo una agencia de IA usa este sistema operativo para entregar a **muchos clientes** reutilizando
> exactamente los mismos módulos. El principio: **los prompts no cambian; cambia el `input`.**

---

## 1. Modelo operativo

Cada cliente es un **input distinto** que recorre los **mismos** módulos y workflows. No se forkean
prompts por cliente: eso rompería la reutilización y multiplicaría el mantenimiento.

```
                 ┌─ clients/acme/input.json ─┐
mismos módulos → ├─ clients/globex/input.json ┤ → outputs aislados por cliente
  (un solo OS)   └─ clients/initech/input.json┘
```

- **Un OS, N clientes.** El repo es el producto; cada cliente es una ejecución parametrizada.
- **Aislamiento por `run_id`.** `meta.run_id` y la carpeta `clients/<cliente>/` separan estado,
  Decision Logs y artefactos. Ningún output de un cliente alimenta a otro.
- **Versionado central.** Mejorar `growth-engine` v1.1 beneficia a todos los clientes a la vez.

---

## 2. Estructura recomendada por cliente

```
clients/
├── _template/
│   └── input.json            # esqueleto conforme a schemas/input.schema.json
└── <cliente>/
    ├── input.json            # contexto, objetivo y restricciones del cliente
    ├── decision-log.md        # Decision Log del orquestador (por cliente)
    └── outputs/               # outputs por módulo (output.schema.json) y consolidados
```

> `clients/` está pensado para datos de cliente. Si son confidenciales, manténlo fuera de control de
> versiones (añádelo a `.gitignore`) o en un repo privado por cliente. El `_template` sí se versiona.

---

## 3. Ciclo de un encargo (engagement lifecycle)

| Fase | Workflow / módulo | Entregable |
|------|-------------------|------------|
| 1. Discovery | rellenar `input.json` con el cliente | Input normalizado validado |
| 2. Diseño integral | [`full-business-build`](../workflows/full-business-build.workflow.md) | Plan de empresa consolidado + Decision Log |
| 3. Crecimiento | [`growth-loop`](../workflows/growth-loop.workflow.md) | Motor de growth + gate económico |
| 4. Comercial | [`sales-funnel`](../workflows/sales-funnel.workflow.md) | Pipeline + CRM + playbooks |
| 5. Retainer | re-ejecución periódica con métricas reales en `available_data.known_metrics` | Iteración continua |

En cada fase, el `orchestrator` mantiene el Decision Log del cliente y escala a humano solo las
decisiones estratégicas.

---

## 4. Ejecutar para un cliente

```bash
# 1. Crear el cliente a partir del template
cp -r clients/_template clients/acme   # y editar clients/acme/input.json

# 2. Preparar la orquestación (determinista, sin LLM)
python3 scripts/run_workflow.py full-business-build clients/acme/input.json

# 3. (opcional) Mega-prompt componido para pegar en Claude Code
python3 scripts/run_workflow.py full-business-build clients/acme/input.json --compose
```

Luego, en Claude Code: *"Actúa como `core/orchestrator` y ejecuta el plan para `clients/acme`;
guarda los outputs en `clients/acme/outputs/` y el Decision Log en `clients/acme/decision-log.md`."*

---

## 5. Productizar módulos (vender prompts como producto)

Como cada prompt es una función pura con contrato estable, se puede empaquetar y vender por separado:

- **Diagnóstico exprés:** solo `product-builder` + `growth-engine` + `unit-economics`.
- **Sprint de pricing:** `pricing-strategy` + `unit-economics` + `financial-scenarios`.
- **Setup comercial:** workflow `sales-funnel` completo.

Cada paquete = un subconjunto de módulos del manifiesto + un `input` del cliente. El mismo OS soporta
servicios productizados, retainers y un futuro SaaS self-serve sin reescribir nada.

---

## 6. Buenas prácticas multi-cliente

1. **Nunca mezclar contextos.** Un `run_id` por cliente; no reutilizar `upstream_outputs` entre clientes.
2. **Datos reales > supuestos.** Rellenar `available_data.known_metrics` con métricas del cliente para
   que `unit-economics` y `financial-scenarios` dejen de estimar.
3. **Compliance por cliente.** `constraints.compliance` se define por encargo (GDPR, sector, etc.).
4. **Mejora central, no por cliente.** Un bug o mejora de prompt se arregla una vez en `departments/`.
5. **Auditable.** El Decision Log por cliente hace trazable cada recomendación entregada.

---

## 7. Escalado de la propia agencia

- **10 clientes:** carpetas `clients/*` + ejecución manual asistida por el runner.
- **100 clientes:** automatizar la invocación (el `output.schema.json` permite encadenar sin humano
  salvo decisiones `strategic`).
- **SaaS:** exponer `input.schema.json` como formulario y el `orchestrator` como backend de ejecución.

El cuello de botella nunca es el contenido (es reutilizable), sino las **decisiones estratégicas
humanas**: el sistema está diseñado para minimizarlas y dejarlas explícitas.
