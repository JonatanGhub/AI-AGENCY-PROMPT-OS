#!/usr/bin/env python3
"""
Validador de integridad del AI Agency Prompt OS.

Comprueba, sin dependencias externas:
  1. Todos los schemas/*.json son JSON bien formado.
  2. Cada prompt en disco (*.prompt.md) está registrado en registry/prompt-index.md.
  3. Cada id de prompt referenciado en prompt-index.md existe en disco.
  4. Cada fila de registry/dependency-map.md referencia (1ª columna) un prompt existente.
  5. Cada workflow en disco está listado en prompt-index.md.
  6. Cada examples/**/input.json es JSON válido y declara las claves requeridas por el input schema.

Salida: exit code 0 si todo OK; 1 si hay algún fallo (lista los problemas).
Pensado para correr en CI y en local.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def prompt_ids_on_disk() -> set[str]:
    ids = set()
    for p in ROOT.rglob("*.prompt.md"):
        ids.add(p.name[: -len(".prompt.md")])
    return ids


def workflow_ids_on_disk() -> set[str]:
    return {p.name[: -len(".workflow.md")] for p in (ROOT / "workflows").glob("*.workflow.md")}


def first_backtick(line: str) -> str | None:
    m = re.search(r"`([^`]+)`", line)
    return m.group(1) if m else None


def check_json_schemas() -> None:
    schema_dir = ROOT / "schemas"
    files = sorted(schema_dir.glob("*.json"))
    if not files:
        fail("schemas/: no se encontró ningún .json")
    for f in files:
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"JSON inválido en {f.relative_to(ROOT)}: {e}")


def check_index_covers_disk(disk_ids: set[str], index_text: str) -> None:
    for pid in sorted(disk_ids):
        if f"`{pid}`" not in index_text:
            fail(f"prompt en disco no registrado en prompt-index.md: {pid}")


def check_index_refs_exist(disk_ids: set[str], index_text: str) -> None:
    # Filas de tabla cuya columna 'archivo' apunta a un *.prompt.md
    for line in index_text.splitlines():
        if "*.prompt.md" in line:  # cabecera/ejemplo, ignorar
            continue
        if ".prompt.md" in line and line.lstrip().startswith("|"):
            pid = first_backtick(line)
            if pid and pid != "_prompt-template" and pid not in disk_ids:
                fail(f"prompt-index.md referencia un prompt inexistente: {pid}")


def check_dependency_map(disk_ids: set[str], dep_text: str) -> None:
    in_table = False
    for line in dep_text.splitlines():
        stripped = line.strip()
        # Tabla principal: filas que empiezan por | `<id>` |
        if stripped.startswith("| `") and "|" in stripped[3:]:
            pid = first_backtick(stripped)
            if pid and pid in disk_ids:
                in_table = True
                continue
            # primera columna con id desconocido (saltar cabeceras/separadores)
            if pid and pid not in disk_ids and in_table:
                fail(f"dependency-map.md: módulo desconocido en 1ª columna: {pid}")


def check_workflows_indexed(wf_ids: set[str], index_text: str) -> None:
    for wid in sorted(wf_ids):
        if f"`{wid}`" not in index_text:
            fail(f"workflow en disco no listado en prompt-index.md: {wid}")


def check_example_inputs() -> None:
    required = {"business_context", "objective", "constraints"}
    examples_dir = ROOT / "examples"
    if not examples_dir.exists():
        return
    for f in examples_dir.rglob("input.json"):
        rel = f.relative_to(ROOT)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"JSON inválido en {rel}: {e}")
            continue
        missing = required - set(data)
        if missing:
            fail(f"{rel}: faltan claves requeridas del input schema: {sorted(missing)}")


def main() -> int:
    disk_ids = prompt_ids_on_disk()
    wf_ids = workflow_ids_on_disk()
    index_text = (ROOT / "registry" / "prompt-index.md").read_text(encoding="utf-8")
    dep_text = (ROOT / "registry" / "dependency-map.md").read_text(encoding="utf-8")

    check_json_schemas()
    check_index_covers_disk(disk_ids, index_text)
    check_index_refs_exist(disk_ids, index_text)
    check_dependency_map(disk_ids, dep_text)
    check_workflows_indexed(wf_ids, index_text)
    check_example_inputs()

    print(f"prompts en disco: {len(disk_ids)} · workflows: {len(wf_ids)}")
    if errors:
        print(f"\n❌ {len(errors)} problema(s) de integridad:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("✅ Integridad OK: schemas válidos y registry consistente con el disco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
