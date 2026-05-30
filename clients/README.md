# Clients — Ejecuciones por cliente

Cada cliente es un **input** que recorre los mismos módulos del OS. Los prompts no se forkean por
cliente; solo cambia el `input`. Ver el [Agency Playbook](../docs/agency-playbook.md) para el modelo
operativo multi-cliente completo.

## Crear un cliente

```bash
cp -r clients/_template clients/<cliente>
# edita clients/<cliente>/input.json (conforme a schemas/input.schema.json)
python3 scripts/run_workflow.py full-business-build clients/<cliente>/input.json
```

## Estructura por cliente

```
clients/<cliente>/
├── input.json          # contexto, objetivo, restricciones (input.schema.json)
├── decision-log.md      # Decision Log del orquestador (por cliente)
└── outputs/             # outputs por módulo y consolidados (output.schema.json)
```

## Aislamiento y privacidad

- Un `meta.run_id` único por cliente; **nunca** mezclar `upstream_outputs` entre clientes.
- Si los datos del cliente son confidenciales, **no los versiones**: añade `clients/<cliente>/` a
  `.gitignore` o usa un repo privado por cliente. El `_template/` sí se versiona.
- Todo `input.json` bajo `clients/` se valida en CI (claves requeridas del input schema).
