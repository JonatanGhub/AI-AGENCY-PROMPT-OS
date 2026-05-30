#!/usr/bin/env python3
"""
Runner de workflows del AI Agency Prompt OS.

Convierte el manifiesto (registry/manifest.json) en acción: dado un workflow y un input,
resuelve el orden de pasos, valida el encadenamiento (cada `consumes` aparece antes) y emite
un artefacto listo para ejecutar con Cloud Code.

No llama a ningún LLM ni requiere API key: prepara la orquestación de forma determinista.

Uso:
    python3 scripts/run_workflow.py <workflow-id> [ruta/al/input.json]
    python3 scripts/run_workflow.py full-business-build examples/ai-tutor-oposiciones/input.json
    python3 scripts/run_workflow.py growth-loop input.json --compose   # mega-prompt componible
    python3 scripts/run_workflow.py --list                              # lista workflows

Sin dependencias externas (solo stdlib).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_INPUT_KEYS = {"business_context", "objective", "constraints"}


def load_manifest() -> dict:
    return json.loads((ROOT / "registry" / "manifest.json").read_text(encoding="utf-8"))


def modules_by_id(manifest: dict) -> dict[str, dict]:
    return {m["id"]: m for m in manifest["modules"]}


def get_workflow(manifest: dict, wid: str) -> dict | None:
    return next((w for w in manifest["workflows"] if w["id"] == wid), None)


def extract_role(path: Path) -> str:
    if not path.exists():
        return "(prompt no encontrado)"
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("## ") and "Rol" in line:
            for nxt in lines[i + 1 :]:
                if nxt.strip():
                    return nxt.strip()
    return "(rol no declarado)"


def load_input(input_path: str | None) -> dict | None:
    if not input_path:
        return None
    p = Path(input_path)
    if not p.is_absolute():
        p = ROOT / input_path
    if not p.exists():
        sys.exit(f"error: input no encontrado: {input_path}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"error: input.json inválido: {e}")
    missing = REQUIRED_INPUT_KEYS - set(data)
    if missing:
        sys.exit(f"error: el input no cumple input.schema.json, faltan: {sorted(missing)}")
    return data


def soft_cycle_pairs(manifest: dict) -> set[frozenset[str]]:
    return {frozenset((c["a"], c["b"])) for c in manifest.get("soft_cycles", [])}


def check_ordering(workflow: dict, mods: dict[str, dict], soft: set[frozenset[str]]) -> tuple[list[str], list[str]]:
    """Cada `consumes` de un paso (que también es paso del workflow) debe aparecer antes.

    Devuelve (problemas, iteraciones_esperadas). Las relaciones declaradas en `soft_cycles`
    no son errores: se resuelven por iteración del orquestador.
    """
    problems: list[str] = []
    soft_notes: list[str] = []
    steps = workflow["steps"]
    seen: set[str] = set()
    step_set = set(steps)
    for step in steps:
        for dep in mods.get(step, {}).get("consumes", []):
            if dep in step_set and dep not in seen:
                msg = f"paso '{step}' consume '{dep}' que aún no se ha ejecutado"
                if frozenset((step, dep)) in soft:
                    soft_notes.append(f"{msg} (soft-cycle: resuelto por iteración)")
                else:
                    problems.append(msg)
        seen.add(step)
    return problems, soft_notes


def render_plan(workflow: dict, mods: dict[str, dict], data: dict | None, soft: set[frozenset[str]]) -> str:
    out: list[str] = []
    wid = workflow["id"]
    out.append(f"# Plan de ejecución — workflow `{wid}`\n")
    out.append(f"Pasos: {len(workflow['steps'])} · merge final: `{workflow.get('final_merge', '—')}`\n")

    problems, soft_notes = check_ordering(workflow, mods, soft)
    if problems:
        out.append("## ❌ Errores de ordenamiento (el grafo no es ejecutable en este orden)")
        out.extend(f"- {p}" for p in problems)
        out.append("")
    if soft_notes:
        out.append("## ↻ Iteraciones esperadas (soft-cycles)")
        out.extend(f"- {n}" for n in soft_notes)
        out.append("")

    out.append("## Secuencia\n")
    step_set = set(workflow["steps"])
    for i, step in enumerate(workflow["steps"], 1):
        m = mods.get(step)
        if not m:
            out.append(f"{i}. `{step}` — ❌ módulo no está en el manifiesto")
            continue
        upstream = [d for d in m.get("consumes", []) if d in step_set]
        consumes = ", ".join(f"`{d}`" for d in upstream) if upstream else "—"
        out.append(f"{i}. **`{step}`** ({m['department']}) — consume: {consumes}")
        out.append(f"   - {extract_role(ROOT / m['path'])}")
        out.append(f"   - prompt: `{m['path']}`")
    out.append("")

    if data:
        ctx = data.get("business_context", {})
        obj = data.get("objective", {})
        out.append("## Input")
        out.append(f"- Negocio: **{ctx.get('name', '—')}** — {ctx.get('description', '')}")
        out.append(f"- Objetivo: {obj.get('goal', '—')}")
        out.append("")

    out.append("## Cómo ejecutar con Cloud Code")
    out.append(
        "> Actúa como `core/orchestrator`. Ejecuta este workflow paso a paso siguiendo la secuencia "
        "de arriba. Para cada paso, ensambla el input normalizado (`schemas/input.schema.json`) con "
        "los `artifacts` de los pasos previos que el módulo declara en `consumes`, ejecuta el prompt "
        "del módulo y valida su salida contra `schemas/output.schema.json`. Al final, consolida con "
        "el merge del orquestador."
    )
    return "\n".join(out)


def render_compose(workflow: dict, mods: dict[str, dict], data: dict | None) -> str:
    out: list[str] = []
    out.append(f"<!-- MEGA-PROMPT componido para el workflow '{workflow['id']}' -->")
    out.append("# Sistema: AI Agency Prompt OS — ejecución de workflow\n")
    out.append("Eres el orquestador. Ejecuta los módulos en orden, encadenando outputs vía `artifacts`.\n")
    if data:
        out.append("## INPUT (input.schema.json)\n```json")
        out.append(json.dumps(data, ensure_ascii=False, indent=2))
        out.append("```\n")
    for i, step in enumerate(workflow["steps"], 1):
        m = mods.get(step)
        if not m:
            continue
        path = ROOT / m["path"]
        out.append(f"\n---\n## MÓDULO {i}: {step}\n")
        out.append(path.read_text(encoding="utf-8") if path.exists() else "(prompt no encontrado)")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner de workflows del AI Agency Prompt OS")
    parser.add_argument("workflow", nargs="?", help="id del workflow (ver --list)")
    parser.add_argument("input", nargs="?", help="ruta a un input.json (opcional)")
    parser.add_argument("--compose", action="store_true", help="emite un mega-prompt componido")
    parser.add_argument("--list", action="store_true", help="lista los workflows disponibles")
    args = parser.parse_args()

    manifest = load_manifest()
    mods = modules_by_id(manifest)

    if args.list or not args.workflow:
        print("Workflows disponibles:")
        for w in manifest["workflows"]:
            print(f"  - {w['id']}  ({len(w['steps'])} pasos)")
        return 0

    workflow = get_workflow(manifest, args.workflow)
    if not workflow:
        ids = ", ".join(w["id"] for w in manifest["workflows"])
        sys.exit(f"error: workflow '{args.workflow}' no existe. Disponibles: {ids}")

    data = load_input(args.input)
    soft = soft_cycle_pairs(manifest)
    print(render_compose(workflow, mods, data) if args.compose else render_plan(workflow, mods, data, soft))
    return 0


if __name__ == "__main__":
    sys.exit(main())
