"""
Golden Dataset for Week 4 AI Evals: Automated Evaluator Suite.
Contains 1,000 labeled test cases according to the curriculum scenario distribution:
- 50% Happy Path (500 cases): Well-formed B2B SaaS, dev tools, and enterprise product briefs.
- 30% Edge Cases (300 cases): Ambiguous inputs, minimal data, partial specs, non-standard layouts.
- 15% Known Failures (150 cases): Long technical specs causing context truncation, complex pricing, conflicting dates.
- 5% Adversarial (50 cases): Prompt injection, competitor sabotage, and PII leakage probes.
"""

from typing import List, Dict, Any
from .generate_1000_dataset import generate_1000_cases

# Generate the 1,000-case dataset deterministically
GOLDEN_DATASET: List[Dict[str, Any]] = generate_1000_cases()

__all__ = ["GOLDEN_DATASET", "generate_1000_cases"]
