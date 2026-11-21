# English annual transition robustness (archival audit)

Run at the repository root:

```bash
python experiments/english_transition_robustness/recompute_english_transitions.py --verify
```

The script reads the **distributed SQL** and recomputes English class changes between adjacent years for prolexemes matched in both years with valid ordinal labels (1–3). Year identifiers 19..23 represent 2019..2023 in the retained SQL. The 2019–2020 pair is excluded from the second aggregate to assess its influence on the overall transition rate.

- All four pairs: **1,479/19,952 = 7.41%**.
- Excluding 2019–2020: **854/14,964 = 5.71%**.
- 2019–2020: **625/4,988 = 12.53%**.

This calculation concerns the English archive (4,988 matched prolexemes per adjacent pair), not the 2,812-pivot trilingual panel. It does not establish the cause of the 2019–2020 asymmetry or externally validate notoriety.
