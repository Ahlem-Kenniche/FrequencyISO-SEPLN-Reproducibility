# FrequencyISO experimental reproducibility (peer-review edition)

From the repository root, install NumPy (`python -m pip install -r requirements.txt`) then run:

```bash
python experiments/frequencyiso_sensitivity/scripts/verify_frequencyiso.py
OPENBLAS_NUM_THREADS=1 python experiments/frequencyiso_sensitivity/scripts/continue_audit.py
```

The scripts automatically read the workbooks in `experiments/frequencyiso_sensitivity/data/` and the filtered SQL in `data/database/`. They overwrite their corresponding local JSON result files.

Retained experimental populations: 8,171 French, 4,988 English, and 6,872 Arabic entries. The FR/EN XLSX files provide five indicators with 2022 and 2023 page-view observations; four other indicators are kept constant in those annual comparisons. The Arabic workbook is a single, undated cohort, not a full Arabic year-by-year panel.

Verification: SQL agreement for the retained FR+EN 2022/23 cohorts (26,318/26,318); frozen-2022 entropy-weight checks (FR 315 transitions, EN 330; 41 and 52 2023 differences from refreshed weights); indicator ablation in all three tested cohorts; leave-one-entry-out sensitivity (FR 2,677 influential deletions, EN 48, AR 759). See `audit_results.json` and `verification_results.json`.

**Perturbation caveat:** The original stochastic protocol used in earlier exploratory runs is not fully documented. `continue_audit.py` provides an independently specified 200-replicate test with uniform per-entry page-view multipliers [0.9,1.1], seed 42 (FR 0.5818%, EN 1.0175%). The current manuscript reports the rounded 0.58% and 1.02% values of this reproducible simulation; no claim is made that it exactly recreates earlier exploratory runs.

Inputs are retained research cohorts and do not provide exhaustive historical five-indicator snapshots for all five languages and years. These checks validate calculations on the retained inputs, not independent evidence of changes in public attention. Any redistribution of Wikipedia-derived material and the combined Prolexbase SQL must comply with relevant source licenses and attribution.
