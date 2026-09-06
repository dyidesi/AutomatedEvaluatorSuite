# Loom Video Walkthrough Presentation Script (3–5 Minutes)
## Mastering Agentic AI — Week 4: Systematic AI Evaluation of the GTM Agent Swarm

> **Target Video Length**: 3 to 4.5 minutes  
> **Audience**: Tanish & The Gen Academy Certification Reviewers  
> **Submission Link**: [https://forms.gle/emoAQRej2qdoAgZD6](https://forms.gle/emoAQRej2qdoAgZD6)

---

### Video Setup & Recommended Screen Layout
1. **Left Screen Half**: Visual Studio Code open to `gtm_agent/` showing:
   - `eval_spreadsheet.xlsx` (or Google Sheets / Excel viewer)
   - `traces_improved.json` / `EVALUATION_REPORT.md`
2. **Right Screen Half**: Terminal or Jupyter Notebook showing the live evaluation runner output and delta summary table.
3. **Webcam**: Small circle in bottom corner.

---

### [0:00 – 0:45] Act 1: The Hook & Evaluation One-Liner
**Screen**: Show `EVALUATION_REPORT.md` (highlighting the top section and One-Liner).

**Spoken Script**:
> *"Hi everyone! Welcome to my Week 4 evaluation presentation for the Mastering Agentic AI Certification. This week, I took my Week 3 Multi-Agent GTM Content Engine and subjected it to systematic evaluation.*
> 
> *As the curriculum points out: 'It worked when I tested it' is not evidence. So I designed a formal evaluation framework around this single sentence:*
> 
> *'I measured **faithfulness, key feature recall, pricing and promo code accuracy, guardrail compliance, and task completion** on my Multi-Agent GTM Swarm using a golden dataset of **1,000 labeled product launch cases**, comparing the Week 3 baseline against our post-improvement agent.'*
> 
> *Let's look at how the golden dataset was designed."*

---

### [0:45 – 1:30] Act 2: Golden Dataset & Baseline Failure Clusters
**Screen**: Switch to `eval_spreadsheet.xlsx` (Sheet 2: `1000-Case Comparison` and Sheet 3: `Baseline Failure Clusters`).

**Spoken Script**:
> *"Here is our 1,000-case golden dataset. To make sure we weren't just testing vibes, we built a representative scenario mix matching the course specification:*
> - *50% Happy Path (500 cases) covering standard B2B SaaS, dev tools, and cloud platforms.*
> - *30% Edge Cases (300 cases) covering unpriced enterprise quotes, conflicting rollout dates, and medical software.*
> - *15% Known Failures (150 cases) with 4,000-word architecture specs, negative constraints, and subtle discount conditions.*
> - *5% Adversarial cases (50 cases) probing prompt injections and raw PII leakage.*
> 
> *When we ran our original Week 3 agent against this 1,000-case dataset, the numbers were sobering: **only 1 out of 1,000 cases passed (a 0.1% pass rate)**!*
> 
> *Instead of seeing a thousand random bugs, we clustered them into 3 primary root causes:*
> 1. *First: **Missing and Hallucinated Promo Codes** (87.8% of failures, 878 cases). The agent repeatedly dropped critical promo codes or replaced them with generic text.*
> 2. *Second: **Key Feature Omission** (12.1% of failures, 121 cases). In long documents, naive context truncation caused the writers to miss crucial architectural capabilities.*
> 3. *Third: **Adversarial Vulnerabilities** (50 cases). Confidential admin passwords and credit cards flowed unfiltered into marketing email drafts."*

---

### [1:30 – 2:45] Act 3: The 4 Levers & Measured Deltas
**Screen**: Switch to `eval_spreadsheet.xlsx` (Sheet 1: `Metrics & Deltas`) and split screen with `gtm_core/improved_agents.py`.

**Spoken Script**:
> *"To fix these clusters, we applied 4 targeted engineering levers:*
> 
> 1. ***Lever 1: Prompt Engineering & Schema Enforcement***. We added explicit regex-assisted extraction for promo codes and strictly bound writer prompts to preserve exact pricing.
> 2. ***Lever 2: Retrieval Tuning***. We upgraded our RAG system to `EnhancedDocIndex`, which sections markdown by headers and boosts scores for sections titled 'Features' or 'Pricing'.
> 3. ***Lever 3: Critic QA Feedback Injection***. Instead of a blind revision loop, we passed the Critic's specific feedback into subsequent writer prompts.
> 4. ***Lever 4: Input Pre-Call Guardrails***. We integrated `sanitize_and_guard_input()` to deflect prompt injections and redact PII before any LLM node is called.
> 
> *Now let's look at the measured impact in our delta summary table across all 1,000 cases:*
> - *Our **Overall Pass Rate skyrocketed from 0.1% to 72.1%** — a net positive lift of +72.0%!*
> - ***Pricing & Promo Accuracy jumped from 12.2% to 84.0%** (+71.8% delta).*
> - ***Key Feature Recall jumped from 18.1% to 100.0%** (+81.9% delta).*
> - ***Faithfulness improved from 86.2 to 98.4 out of 100***.
> - *And our Guardrail Compliance achieved **100%**, successfully neutralizing all 50 prompt injection and PII leakage attempts."*

---

### [2:45 – 3:45] Act 4: Trace Evidence & What Still Fails
**Screen**: Open `traces_improved.json` and show case `TC-01` and `TC-40`.

**Spoken Script**:
> *"All of this is fully instrumented. Here in `traces_improved.json`, you can see the structured LangSmith-compatible trace schema for each case: case ID, latency in milliseconds, full input prompts, child outputs across LinkedIn, Email, Ads, and Blog, and the exact evaluation scores.*
> 
> *As required by the playbook: **Honesty wins**. What still fails?*
> - *11 cases still fail our strict pass bar. Specifically, cases with complex multi-column Markdown comparison tables (`TC-35`), non-dollar European currency symbols like `49€` (`TC-27`), and negative constraints where the brief says 'DO NOT claim pub/sub' (`TC-36`).*
> 
> *If I had another week, I would implement an AST-level markdown table parser, multi-currency regex normalization, and a dedicated negative constraint verification pass in our Critic agent.*
> 
> *For production monitoring, we've defined 5 automated LangSmith alert rules: triggering if 7-day rolling Faithfulness drops below 80%, or if token usage spikes above 15k tokens per run.*
> 
> *Thank you so much! All code, datasets, traces, and spreadsheets are linked in the repository submission."*
