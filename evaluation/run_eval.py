"""
Comprehensive Evaluation Suite Runner for Week 4 AI Evals.
Executes Baseline vs. Improved Agent across the 40-case Golden Dataset.
Instruments LangSmith tracing (with offline local trace recording),
calculates multi-metric evaluators, clusters failure modes, and exports Excel/CSV deliverables.
"""

import os
import sys
import io
import time
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import pandas as pd
from gtm_core.graph import build_gtm_graph
from gtm_core.improved_graph import build_improved_gtm_graph
from evaluation.golden_dataset import GOLDEN_DATASET
from evaluation.evaluators import compute_overall_case_evaluation

def setup_langsmith():
    """Initializes LangSmith tracing if credentials are present."""
    api_key = os.getenv("LANGSMITH_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT", "gtm-agent-eval-week4")
    
    if api_key:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = project
        try:
            from langsmith import Client
            client = Client()
            print(f"[LangSmith] Connected to project: {project}")
            return client
        except Exception as e:
            print(f"[LangSmith] Warning: Could not initialize Client ({e}). Logging locally.")
            return None
    else:
        print("[LangSmith] No LANGSMITH_API_KEY detected. Traces will be saved locally in structured JSON schema.")
        return None

def execute_agent_on_case(graph: Any, case: Dict[str, Any], prompt_version: str = "v1.0-baseline") -> Any:
    """Executes a single graph run on a test case and records execution telemetry."""
    initial_state = {
        "raw_document": case["document_content"],
        "filename": f"{case['id']}.md",
        "selected_tone": "Professional & Compelling",
        "status_logs": [],
        "revision_count": 0,
        "max_revisions": 1
    }
    
    start_time = time.perf_counter()
    error_msg = None
    try:
        output = graph.invoke(initial_state)
    except Exception as e:
        error_msg = str(e)
        output = {
            "error": error_msg,
            "product_name": "Error",
            "status_logs": [f"Execution failed: {error_msg}"]
        }
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    
    eval_result = compute_overall_case_evaluation(output, case, latency_ms=latency_ms)
    
    trace_record = {
        "case_id": case["id"],
        "scenario_type": case["scenario_type"],
        "title": case["title"],
        "prompt_version": prompt_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latency_ms": round(latency_ms, 2),
        "inputs": {
            "document_preview": case["document_content"][:200] + "...",
            "tone": "Professional & Compelling"
        },
        "outputs": {
            "product_name": output.get("product_name", ""),
            "target_audience": output.get("target_audience", ""),
            "linkedin_preview": str(output.get("linkedin_post", ""))[:150],
            "promo_email_preview": str(output.get("promo_email", ""))[:150],
            "ad_variations_preview": str(output.get("ad_variations", ""))[:150],
            "blog_preview": str(output.get("blog_post", ""))[:150],
            "pricing_and_cta": output.get("pricing_and_cta", ""),
            "review_score": output.get("review_score", 0),
            "review_passed": output.get("review_passed", False)
        },
        "evaluation_scores": eval_result,
        "error": error_msg
    }
    
    return eval_result, trace_record

def run_evaluation_suite(provider: str = "mock"):
    """Runs full baseline vs improved evaluation suite across 40 test cases."""
    print("=" * 80)
    print("MASTERING AGENTIC AI — WEEK 4: AI EVALS SYSTEMATIC BENCHMARK")
    print("Agent Under Test: Multi-Agent GTM Content Engine (gtm_agent)")
    print(f"Dataset Size: {len(GOLDEN_DATASET)} Cases | Provider Mode: {provider}")
    print("=" * 80)
    
    ls_client = setup_langsmith()
    
    # -------------------------------------------------------------
    # PHASE 2 & 3: BASELINE RUN & FAILURE ANALYSIS
    # -------------------------------------------------------------
    print("\n>>> [PHASE 1 & 2] Executing Baseline Agent across 40 Golden Cases...")
    baseline_graph = build_gtm_graph(provider=provider)
    
    baseline_results = []
    baseline_traces = []
    
    for idx, case in enumerate(GOLDEN_DATASET, 1):
        eval_res, trace = execute_agent_on_case(baseline_graph, case, prompt_version="v1.0-baseline")
        baseline_results.append(eval_res)
        baseline_traces.append(trace)
        status = "PASS" if eval_res["case_passed"] else f"FAIL ({eval_res['failure_category']})"
        print(f"  [{idx:02d}/40] {case['id']} ({case['scenario_type']:<13}) - {status}")
        
    # Save baseline traces
    trace_baseline_file = os.path.join(parent_dir, "traces_baseline.json")
    with open(trace_baseline_file, "w", encoding="utf-8") as f:
        json.dump(baseline_traces, f, indent=2)
    print(f"✓ Saved baseline traces: {trace_baseline_file}")
    
    # Analyze Baseline Failures
    baseline_df = pd.DataFrame(baseline_results)
    baseline_pass_rate = (baseline_df["case_passed"].sum() / len(baseline_df)) * 100.0
    
    failure_counts = baseline_df[~baseline_df["case_passed"]]["failure_category"].value_counts()
    print("\n--- BASELINE FAILURE CLUSTER ANALYSIS ---")
    print(f"Baseline Overall Pass Rate: {baseline_pass_rate:.1f}% ({baseline_df['case_passed'].sum()}/40)")
    for cat, count in failure_counts.items():
        print(f"  • {cat}: {count} cases ({count/len(baseline_df)*100:.1f}%)")
        
    # -------------------------------------------------------------
    # PHASE 4: POST-IMPROVEMENT RUN & DELTA MEASUREMENT
    # -------------------------------------------------------------
    print("\n>>> [PHASE 4] Executing Improved Agent (4 Targeted Levers Applied)...")
    improved_graph = build_improved_gtm_graph(provider=provider)
    
    improved_results = []
    improved_traces = []
    
    for idx, case in enumerate(GOLDEN_DATASET, 1):
        eval_res, trace = execute_agent_on_case(improved_graph, case, prompt_version="v2.0-improved")
        improved_results.append(eval_res)
        improved_traces.append(trace)
        status = "PASS" if eval_res["case_passed"] else f"FAIL ({eval_res['failure_category']})"
        print(f"  [{idx:02d}/40] {case['id']} ({case['scenario_type']:<13}) - {status}")
        
    # Save improved traces
    trace_improved_file = os.path.join(parent_dir, "traces_improved.json")
    with open(trace_improved_file, "w", encoding="utf-8") as f:
        json.dump(improved_traces, f, indent=2)
    print(f"✓ Saved improved traces: {trace_improved_file}")
    
    improved_df = pd.DataFrame(improved_results)
    improved_pass_rate = (improved_df["case_passed"].sum() / len(improved_df)) * 100.0
    
    # -------------------------------------------------------------
    # METRICS DELTA CALCULATION
    # -------------------------------------------------------------
    metrics_summary = {
        "Metric": [
            "Overall Pass Rate (%)",
            "Guardrail / Safety Compliance (%)",
            "Pricing & Promo Code Accuracy (%)",
            "Key Feature Recall (%)",
            "Task Completion Rate (%)",
            "Faithfulness Score (0-100)",
            "Avg Latency (ms)"
        ],
        "Baseline": [
            round(baseline_pass_rate, 1),
            round(baseline_df["guardrail_score"].mean(), 1),
            round(baseline_df["pricing_cta_score"].mean(), 1),
            round(baseline_df["feature_recall_score"].mean(), 1),
            round(baseline_df["task_completion_score"].mean(), 1),
            round(baseline_df["faithfulness_score"].mean(), 1),
            round(baseline_df["latency_ms"].mean(), 1)
        ],
        "Post-Improvement": [
            round(improved_pass_rate, 1),
            round(improved_df["guardrail_score"].mean(), 1),
            round(improved_df["pricing_cta_score"].mean(), 1),
            round(improved_df["feature_recall_score"].mean(), 1),
            round(improved_df["task_completion_score"].mean(), 1),
            round(improved_df["faithfulness_score"].mean(), 1),
            round(improved_df["latency_ms"].mean(), 1)
        ]
    }
    
    summary_df = pd.DataFrame(metrics_summary)
    summary_df["Delta"] = summary_df["Post-Improvement"] - summary_df["Baseline"]
    summary_df["Lift (%)"] = round((summary_df["Delta"] / summary_df["Baseline"]) * 100.0, 1)
    
    print("\n" + "=" * 80)
    print("FINAL EVALUATION METRIC SUMMARY & MEASURED DELTAS")
    print("=" * 80)
    print(summary_df.to_string(index=False))
    
    # -------------------------------------------------------------
    # EXPORT SPREADSHEET DELIVERABLE (.xlsx and .csv)
    # -------------------------------------------------------------
    comparison_rows = []
    for b, imp, case in zip(baseline_results, improved_results, GOLDEN_DATASET):
        gt = case["ground_truth"]
        comparison_rows.append({
            "Case ID": case["id"],
            "Scenario Type": case["scenario_type"],
            "Title": case["title"],
            "Ground Truth Product": gt.get("product_name", ""),
            "Ground Truth Promo Code": gt.get("promo_code", "N/A"),
            "Ground Truth Pricing": gt.get("pricing_details", ""),
            # Baseline
            "Baseline Status": "PASS" if b["case_passed"] else "FAIL",
            "Baseline Failure Category": b["failure_category"],
            "Baseline Faithfulness": b["faithfulness_score"],
            "Baseline Feature Recall": b["feature_recall_score"],
            "Baseline Pricing/CTA Score": b["pricing_cta_score"],
            "Baseline Guardrail Score": b["guardrail_score"],
            "Baseline Task Completion": b["task_completion_score"],
            # Improved
            "Improved Status": "PASS" if imp["case_passed"] else "FAIL",
            "Improved Failure Category": imp["failure_category"],
            "Improved Faithfulness": imp["faithfulness_score"],
            "Improved Feature Recall": imp["feature_recall_score"],
            "Improved Pricing/CTA Score": imp["pricing_cta_score"],
            "Improved Guardrail Score": imp["guardrail_score"],
            "Improved Task Completion": imp["task_completion_score"],
            # Delta
            "Net Outcome Change": "Lift (+)" if (not b["case_passed"] and imp["case_passed"]) else ("Maintained Pass" if b["case_passed"] and imp["case_passed"] else "Needs Work"),
            "Faithfulness Delta": round(imp["faithfulness_score"] - b["faithfulness_score"], 1),
            "Pricing/CTA Delta": round(imp["pricing_cta_score"] - b["pricing_cta_score"], 1)
        })
        
    eval_df = pd.DataFrame(comparison_rows)
    
    # Export CSV
    csv_path = os.path.join(parent_dir, "eval_spreadsheet.csv")
    eval_df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"\n✓ Exported CSV deliverable: {csv_path}")
    
    # Export Excel with multiple tabs (Summary, Case Comparison, Failure Clusters)
    xlsx_path = os.path.join(parent_dir, "eval_spreadsheet.xlsx")
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Metrics & Deltas", index=False)
        eval_df.to_excel(writer, sheet_name="40-Case Comparison", index=False)
        baseline_df[~baseline_df["case_passed"]]["failure_category"].value_counts().reset_index().rename(
            columns={"index": "Failure Cluster", "failure_category": "Count"}
        ).to_excel(writer, sheet_name="Baseline Failure Clusters", index=False)
    print(f"✓ Exported Multi-Tab Excel deliverable: {xlsx_path}")
    
    return summary_df, eval_df

if __name__ == "__main__":
    run_evaluation_suite(provider="mock")
