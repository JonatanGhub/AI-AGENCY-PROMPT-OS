# Arquitectura global del AI Agency Prompt OS

Vista de conjunto de cómo encajan las piezas: un `input` normalizado entra, recorre módulos
especializados orquestados sobre un grafo declarativo, y sale un resultado consolidado por cliente.

---

## 1. Diagrama de capas (flujo principal)

```mermaid
flowchart TB
  IN["input.json<br/>(input.schema.json)"] --> WE

  subgraph CORE["core/ — orquestación"]
    WE["workflow-engine<br/>ejecuta el DAG"]
    ORCH["orchestrator<br/>consolida + Decision Log"]
  end

  WE -->|lee el grafo| MAN["registry/manifest.json"]

  subgraph DEPTS["departments/ — 18 microservicios cognitivos"]
    direction LR
    PROD["product<br/>product-builder · ux-strategy · roadmap-generator"]
    AIE["ai-engineering<br/>ai-architecture · model-selection · agent-design"]
    GRW["growth<br/>growth-engine · funnel-designer · content-strategy"]
    FIN["finance<br/>pricing-strategy · unit-economics · financial-scenarios"]
    SAL["sales<br/>sales-system · crm-automation · closing-playbooks"]
    OPS["operations<br/>ops-automation · workflow-designer · scaling-ops"]
  end

  WE --> DEPTS
  DEPTS -->|outputs output.schema.json| ORCH
  ORCH --> OUT["output consolidado<br/>+ Decision Log"]
  OUT --> CLI["clients/&lt;cliente&gt;/outputs"]

  SCH["schemas/<br/>input · output · decision"] -. contrato .-> DEPTS
  SCH -. contrato .-> ORCH
  RUN["scripts/run_workflow.py"] -. prepara .-> WE
```

---

## 2. Grafo de dependencias entre módulos (DAG)

Cada módulo declara `consumes` / `feeds`. El `workflow-engine` lo ordena topológicamente.

```mermaid
flowchart LR
  PB[product-builder] --> AA[ai-architecture] --> MS[model-selection]
  PB --> UX[ux-strategy] --> RG[roadmap-generator]
  AA --> AG[agent-design]
  MS --> AG
  PB --> GE[growth-engine] --> FD[funnel-designer] --> CS[content-strategy]
  PB --> PR[pricing-strategy]
  GE --> UE[unit-economics]
  FD --> UE
  PR --> UE
  MS --> UE
  GE --> SS[sales-system]
  PR --> SS
  SS --> CRM[crm-automation] --> CP[closing-playbooks]
  PR --> CP
  SS --> OA[ops-automation]
  AG --> OA
  OA --> WD[workflow-designer] --> SC[scaling-ops]
  UE --> FS[financial-scenarios]
  PR --> FS
  FS --> SC
  SC --> ORCH[orchestrator]
  FS --> ORCH

  PR -. soft-cycle .- UE
  FS -. soft-cycle .- SC
```

Las líneas punteadas `soft-cycle` son relaciones bidireccionales resueltas por **iteración**
(no por recursión): el orquestador puede re-disparar un módulo con feedback del downstream.

---

## 3. Ciclo de ejecución (de input a entrega)

```mermaid
sequenceDiagram
  participant U as Usuario / Cliente
  participant R as run_workflow.py
  participant M as manifest.json
  participant E as workflow-engine
  participant D as módulos (departments)
  participant O as orchestrator

  U->>R: input.json + workflow id
  R->>M: lee grafo y pasos
  R-->>U: plan de ejecución / mega-prompt
  U->>E: ejecuta en Claude Code
  loop por cada paso del DAG
    E->>D: input normalizado + upstream artifacts
    D-->>E: output.schema.json (decisiones, artifacts)
  end
  E->>O: estado acumulado
  O-->>U: output consolidado + Decision Log + próximo workflow
```

---

## 4. Mapa de carpetas → responsabilidad

| Carpeta | Responsabilidad |
|---------|-----------------|
| `core/` | Orquestación: descomponer, ejecutar el grafo, consolidar, registrar decisiones. |
| `departments/` | 18 prompts especializados, cada uno una función pura con contrato estable. |
| `workflows/` | Encadenamientos declarativos de módulos (DAGs con gating). |
| `schemas/` | Contratos de I/O (input · output · decision) que garantizan la compatibilidad. |
| `registry/` | `manifest.json` (máquina) + index, dependency-map y versionado (humano). |
| `scripts/` | `validate.py` (integridad en CI) y `run_workflow.py` (manifiesto → plan ejecutable). |
| `examples/` | Ejecuciones de referencia end-to-end. |
| `clients/` | Un `input` por cliente; outputs y Decision Log aislados (ver Agency Playbook). |
| `docs/` | Playbook de agencia y esta arquitectura. |
