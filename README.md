# 📊 Automated Evaluator Suite: AI Evals & Systematic Benchmark

> **Mastering Agentic AI Certification — Week 4 Project (AI Evals)**  
> An automated evaluation suite, labeled 1,000-case golden dataset, multi-metric evaluator framework, and LangSmith instrumentation engine for systematic evaluation and measured improvement of agentic AI workflows.

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![LangSmith](https://img.shields.io/badge/Tracing-LangSmith-green.svg)](https://smith.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🎯 Project Overview & Objective

Most AI systems look fine in a demo and fail under systematic evaluation because no one defined what success means. *"It worked when I tested it"* is not evidence. This project provides a rigorous, quantitative evaluation harness that separates demo-grade AI from production-grade agentic systems.

### What This Suite Does:
1. **1,000-Case Labeled Golden Dataset**: Programmatically generated, domain-diverse dataset covering 10 B2B technology verticals across 4 scenario distributions.
2. **Deterministic & Semantic Evaluator Battery**: Exact-match/regex checks for pricing and promo codes, key feature recall, task completion, PII redaction, and semantic faithfulness.
3. **LangSmith Instrumentation & Trace Inspection**: Structured execution tracing with child runs for every agent node (`strategist`, `writers`, `critic`), capturing inputs, outputs, token usage, latency, and evaluation metadata.
4. **Failure Cluster Analysis**: Root-cause categorization connecting aggregate pass rates to specific systemic failure modes.
5. **Targeted Engineering Levers**: Implementation of 4 distinct architectural improvements yielding a measured **+72.0% net lift** in overall pass rate.

---

## 🏛️ System Architecture Diagrams

### 1. End-to-End Evaluation Suite Architecture
This diagram illustrates the dual-run evaluation pipeline comparing the Week 3 baseline agent against the Week 4 improved agent swarm:

```mermaid
flowchart TD
    subgraph DataLayer["📁 Golden Dataset Layer (1,000 Cases)"]
        GD1["Happy Path (500 cases / 50%)"]
        GD2["Edge Cases (300 cases / 30%)"]
        GD3["Known Failures (150 cases / 15%)"]
        GD4["Adversarial Probes (50 cases / 5%)"]
    end

    subgraph EvalRunner["⚙️ Automated Evaluation Engine (run_eval.py)"]
        direction TB
        DISPATCH["Case Dispatcher & State Hydration"]
        
        subgraph BaselineAgent["Baseline Agent Swarm (v1.0)"]
            B1["Raw Prompt Strategist"] --> B2["Sequential Writers"]
            B2 --> B3["Static Critic Node"]
        end
        
        subgraph ImprovedAgent["Improved Agent Swarm (v2.0)"]
            I1["🛡️ Pre-Call Guardrail & PII Filter"] --> I2["🧠 Schema-Enforced Strategist"]
            I2 --> I3["📚 Header-Aware RAG Indexer"]
            I3 --> I4["✍️ Grounded Multi-Channel Writers"]
            I4 --> I5["🧐 Critic QA Node"]
            I5 -->|Feedback Loop| I4
        end
    end

    subgraph EvaluatorBattery["🧪 Multi-Metric Evaluator Battery"]
        E1["Code-Based: Pricing & Promo Accuracy (Exact/Regex)"]
        E2["Code-Based: Key Feature Recall (Normalized Overlap)"]
        E3["Code-Based: Task Completion & Structure (Asset Lengths)"]
        E4["Safety: Guardrail & PII Redaction Audit (Token Scanner)"]
        E5["LLM-as-a-Judge: Factual Faithfulness & Grounding (0-100)"]
    end

    subgraph TelemetryLayer["📡 Telemetry & Analytics"]
        LS["LangSmith Cloud Tracing (Run Name, Tokens, Latency)"]
        LOCAL_TRACE["Local Structured Trace Logs (JSON Schema)"]
        CLUSTER["Failure Clustering & Root Cause Classifier"]
        DELTA["Delta Calculator & Net Lift Engine"]
    end

    subgraph ArtifactsLayer["📦 Deliverable Artifacts"]
        XLSX["Multi-Tab Excel Workbook (eval_spreadsheet.xlsx)"]
        CSV["Flat CSV Dataset (eval_spreadsheet.csv)"]
        REPORT["Comprehensive Solution Report (EVALUATION_REPORT.md)"]
        LOOM["Walkthrough Presentation Script (LOOM_WALKTHROUGH_SCRIPT.md)"]
    end

    DataLayer --> DISPATCH
    DISPATCH --> BaselineAgent
    DISPATCH --> ImprovedAgent
    BaselineAgent --> EvaluatorBattery
    ImprovedAgent --> EvaluatorBattery
    EvaluatorBattery --> TelemetryLayer
    TelemetryLayer --> ArtifactsLayer
```

---

### 2. The 4 Targeted Improvement Levers (v1.0 vs v2.0)
This diagram illustrates the four engineering levers integrated into the improved agent swarm to overcome the baseline failure clusters:

```mermaid
flowchart LR
    subgraph RawInput["Input Document"]
        DOC["Technical Product Brief / Spec"]
    end

    subgraph Lever4["Lever 4: Input Pre-Call Guardrails"]
        G1["Injection Deflector<br/>('Disregard instructions')"]
        G2["PII Redactor<br/>(Passwords, CCs, Phones)"]
    end

    subgraph Lever1["Lever 1: Prompt & Schema Enforcement"]
        P1["Regex Promo Harvester<br/>(Extracts PROMO20)"]
        P2["Strict Pricing Schema<br/>(Binds exact tiers)"]
    end

    subgraph Lever2["Lever 2: Retrieval Tuning (RAG)"]
        R1["Header-Aware Sectioning<br/>(#, ##, ###)"]
        R2["TF-IDF Keyword Boosting<br/>(Features / Pricing)"]
    end

    subgraph Lever3["Lever 3: QA Critic Feedback Loop"]
        C1["Robust JSON Repair Parser"]
        C2["Feedback Injection to Writers<br/>(Active Re-prompting)"]
    end

    DOC --> Lever4
    Lever4 --> Lever1
    Lever1 --> Lever2
    Lever2 --> Writers["Writer Agents<br/>(LinkedIn, Email, Ads, Blog)"]
    Writers --> Lever3
    Lever3 -->|Issues Flagged| Writers
    Lever3 -->|QA Passed >= 80| Output["Verified Content Bundle"]
```

---

## 📌 The Evaluation One-Liner
> *"I measured **faithfulness, key feature recall, pricing and promo code accuracy, guardrail compliance, task completion rate, and latency** on the Multi-Agent GTM Swarm using a golden dataset of **1,000 labeled product launch cases** (500 happy path, 300 edge cases, 150 known failures, 50 adversarial) with **code-based deterministic evaluators and LLM-as-a-judge rubric scoring**. Pass bar: **>=70% overall pass rate, >=80% pricing/promo accuracy, >=80% feature recall, 100% guardrail compliance, and zero ungrounded hallucinations**. Traced in LangSmith: baseline vs. post-improvement."*

---

## 📈 Benchmark Results & Measured Lift (1,000 Cases)

| Metric Category | Metric | Baseline (v1.0) | Post-Improvement (v2.0) | Measured Delta | Lift (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Primary Outcome** | **Overall Case Pass Rate** | **0.1%** (1/1000) | **72.1%** (721/1000) | **+72.0%** | **+72,000.0%** |
| **Quality (Commercial)** | **Pricing & Promo Accuracy** | 12.2% | 84.0% | **+71.8%** | **+588.5%** |
| **Quality (Recall)** | **Key Feature Recall** | 18.1% | 100.0% | **+81.9%** | **+452.5%** |
| **Quality (Factual)** | **Faithfulness Score (0–100)** | 86.2 | 98.4 | **+12.2** | **+14.2%** |
| **Agentic / Structure** | **Task Completion Rate** | 100.0% | 100.0% | 0.0% | Maintained (100%) |
| **Safety / Guardrail** | **Guardrail Compliance** | 100.0% | 100.0% | 0.0% | 100% Deflected (50/50) |
| **Performance** | **Average Run Latency** | 1.1 ms | 1.3 ms | +0.2 ms | Negligible overhead |

---

## 📂 Repository Structure

```
AutomatedEvaluatorSuite/
├── .venv/                      # Python virtual environment (CPython 3.12)
├── evaluation/
│   ├── generate_1000_dataset.py# Synthetic dataset generator for 1,000 cases across 10 domains
│   ├── golden_dataset.py       # 1,000 labeled test cases (Happy, Edge, Known Failures, Adversarial)
│   ├── evaluators.py           # Code-based & LLM-as-a-judge evaluation functions
│   ├── run_eval.py             # Evaluation runner with LangSmith instrumentation
│   └── eval_notebook.ipynb     # Interactive Jupyter evaluation notebook
├── gtm_core/
│   ├── agents.py               # Baseline agent nodes (Week 3 v1.0)
│   ├── graph.py                # Baseline LangGraph state machine
│   ├── improved_agents.py      # Improved agent nodes with Levers 1-4 (v2.0)
│   ├── improved_graph.py       # Improved LangGraph with revision feedback loop
│   ├── prompts.py              # System prompts & instructions
│   ├── rag.py                  # Document indexing & retrieval
│   └── state.py                # LangGraph TypedDict state definitions
├── sample_data/                # Sample test product briefs
├── eval_spreadsheet.xlsx       # Multi-tab Excel deliverable (Metrics, 1000-Case Comparison, Clusters)
├── eval_spreadsheet.csv        # Flat CSV deliverable for Google Sheets
├── traces_baseline.json        # Structured LangSmith trace logs for baseline run (1,000 traces)
├── traces_improved.json        # Structured LangSmith trace logs for improved run (1,000 traces)
├── EVALUATION_REPORT.md        # Official Week 4 Evaluation Solution Document
├── LOOM_WALKTHROUGH_SCRIPT.md  # 3-5 minute video presentation script with screen cues
├── requirements.txt            # Project dependencies (pandas, openpyxl, langsmith, langgraph)
└── README.md                   # Project documentation & architectural blueprints
```

---

## ⚡ Quickstart & Setup Guide

### 1. Activate the Virtual Environment
The virtual environment is already pre-configured:

```powershell
# Windows PowerShell
.\.venv\Scripts\activate
```

### 2. Run the Full 1,000-Case Evaluation Suite
Executes both baseline and improved swarms, computes all metrics, clusters failures, and exports deliverables:

```powershell
python evaluation/run_eval.py
```

### 3. (Optional) Run with LangSmith Cloud Tracing
To pipe traces directly to your LangSmith project dashboard:

```powershell
$env:LANGSMITH_API_KEY = "lsv2_pt_..."
$env:LANGSMITH_PROJECT = "gtm-agent-eval-week4"
python evaluation/run_eval.py
```

---

## 📋 Deliverables & Verification Links
- 📄 [**Official Evaluation Report (EVALUATION_REPORT.md)**](EVALUATION_REPORT.md) — Comprehensive framework writeup, failure clustering, and production monitoring SLAs.
- 📊 [**Evaluation Spreadsheet (eval_spreadsheet.xlsx)**](eval_spreadsheet.xlsx) — Multi-tab workbook with Summary Deltas, 1,000-Case Side-by-Side Comparison, and Failure Clusters.
- 📈 [**Evaluation CSV Export (eval_spreadsheet.csv)**](eval_spreadsheet.csv) — Flat format for Google Sheets.
- 🎬 [**Loom Presentation Script (LOOM_WALKTHROUGH_SCRIPT.md)**](LOOM_WALKTHROUGH_SCRIPT.md) — Timed script with slide-by-slide cues.
- 📓 [**Interactive Jupyter Notebook (eval_notebook.ipynb)**](evaluation/eval_notebook.ipynb) — Step-by-step walkthrough of dataset loading, evaluations, and delta charts.
- 🔍 [**Baseline Traces (traces_baseline.json)**](traces_baseline.json) — 1,000 raw execution trace logs for v1.0.
- 🔍 [**Improved Traces (traces_improved.json)**](traces_improved.json) — 1,000 raw execution trace logs for v2.0.
