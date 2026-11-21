# Year-Indexed FrequencyISO in Multilingual Prolexbase — Reproducibility Materials

Companion repository for *Year-Indexed FrequencyISO in Multilingual Prolexbase: Resource Representation, Cross-Language Trajectories, and Computational Sensitivity*.

**Anonymous peer-review edition:** submission-author names and affiliations are omitted. Historical Prolexbase references and license notices are preserved. The anonymous submitting team contributed to the integration of Arabic into Prolexbase and the development of FrequencyISO; original Prolexbase contributions are attributed in `COPYRIGHT_AND_ATTRIBUTION.md`.

## Included material

- `data/database/prolexbase_without_derivatives_instances.sql`: filtered Prolexbase 4.1 dump; tables of derivatives and instances and the relevant dependent foreign keys are removed. Other volumes and annual FrequencyISO records remain available for audit.
- `scripts/` and `data/recomputed/`: reproducible archived distributions and matched-year transition tables (manuscript Tables 1–3) and reconciled 2,812-pivot trilingual cohort (2019–2023).
- `experiments/frequencyiso_sensitivity/`: retained experimental workbooks, source code and audit logs for Shannon–SAW reconstruction, frozen weights, all fifteen indicator ablations, three-language leave-one-entry-out experiments, and a separately specified stochastic perturbation check.
- `experiments/gdelt_news_proxy/`: recorded exploratory GDELT pilot (6/9 directional matches) and its calculation.
- `experiments/sparql_temporal_queries/`: executable SPARQL tests and recorded GraphDB reference results (query execution requires the separate RDF/GraphDB representation).
- `experiments/english_transition_robustness/`: reproducible English annual transition counts and the 2019–2020 exclusion analysis.
- `figures/`, `data/aggregates/`, `docs/`: corresponding illustrations, published summary values and documentation.
- `LICENSE-LGPLLR.txt`, `COPYRIGHT_AND_ATTRIBUTION.md`: resource licensing and historical attribution, and scope of license and attribution.

## Re-run the checks

Python 3.9 or newer; NumPy is only necessary for the sensitivity analysis.

```bash
python scripts/recompute_tables.py --verify
python scripts/validate_aggregates.py
python experiments/english_transition_robustness/recompute_english_transitions.py --verify
python scripts/reconcile_trilingual_panel.py
python experiments/gdelt_news_proxy/analyze_cases.py
python -m pip install -r requirements.txt
python experiments/frequencyiso_sensitivity/scripts/verify_frequencyiso.py
OPENBLAS_NUM_THREADS=1 python experiments/frequencyiso_sensitivity/scripts/continue_audit.py
```

The last command can be computation-intensive and updates `audit_results.json`. See `experiments/frequencyiso_sensitivity/README.md` for the exact experimental scope.

## Additional reproducibility materials

This release adds the documented SPARQL queries and the English 2019–2020 sensitivity breakdown. It does not claim that the separate RDF repository is distributed in this ZIP. Detailed individual labels from the 2023 frozen-weights English counterfactual are not included; published aggregate results remain in `data/aggregates/frozen_weights_reported.csv`.

## Boundaries

The manuscript uses the **2,812 uniquely mapped Arabic–English–French pivots**, not the earlier unreconciled 3,043 estimate. No absent prolexeme→pivot link is fabricated. The retrospective class labels are relative to individual language-year cohorts and not externally calibrated popularity scores.

The retained matrices reproduce the specified cohorts, not the complete Wikipedia historical extraction pipeline. Perturbation is a close new stochastic check, **not** a bitwise recreation of the unpublished original random process. The GDELT pilot is limited to selected days and does not validate annual news attention.

## Redistribution conditions

The filtered Prolexbase SQL combines historical multilingual material with Arabic lexical records and year-indexed FrequencyISO data. The Prolexbase linguistic-resource component is provided with the LGPL-LR license text and the historical project and scholarly credits; the filtered distribution is explicitly documented. The anonymous review edition omits submitting-author identities while preserving source attribution. Redistribution remains subject to the relevant license and third-party rights. See `COPYRIGHT_AND_ATTRIBUTION.md` and `LICENSE_INFO.md`.
