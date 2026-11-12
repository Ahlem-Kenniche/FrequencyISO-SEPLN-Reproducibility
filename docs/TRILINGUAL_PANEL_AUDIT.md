# Reconciled trilingual panel — verified cohort

The distributed SQL supports **2,825** pivot IDs containing at least one complete 2019–2023 series in Arabic, English and French. **13** pivot IDs have multiple complete prolexemes in at least one language and are excluded rather than arbitrarily choosing one. The resulting **2,812 uniquely matched pivot IDs** (8,436 language-specific trajectories) are the basis of manuscript Section 6 and Figures 3–4.

The original 3,043-panel total could not be traced to this supplied SQL because English frequency rows contain prolexeme identifiers missing from the supplied `prolexeme_eng` table. There are 20,262 frequency-side IDs vs 17,959 mapped prolexeme IDs across all years, including 2,013 unmatched English identifiers observed in 2019–2023. No missing pivot mappings were imputed.

The exact panel rows are in `data/recomputed/trilingual_panel_reconciled.csv`, with pivot IDs, prolexeme IDs and all annual classes. Run `python scripts/reconcile_trilingual_panel.py` from the repository root to recreate the CSV and report summary figures.

**Recomputed Section 6:** 1,702 constant pivots (60.53%); 1,110 changed (39.47%); 769 with at least two class transitions; 730 fully matching across all three language trajectories (25.96%); 2,082 cross-language disagreements. Arabic 108 higher/339 lower, English 591/628, French 314/322. Figure 3 corrects the Jason Statham Arabic trajectory to 1–2–1–2–1, matching the retained SQL.
