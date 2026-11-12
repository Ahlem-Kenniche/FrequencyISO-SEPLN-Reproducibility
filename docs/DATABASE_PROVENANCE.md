# Database provenance

This repository includes a filtered SQL export identified as Prolexbase 4.1, based on a phpMyAdmin dump dated 6 June 2026. The released database header uses the generic label `prolexbase`; all other lexical records remain unchanged.

Excluded: tables with prefix `derivative_` or `instance_`, `derivative_category`, and affected foreign-key declarations. Retained: FrequencyISO frequency tables, prolexemes and other original tables.

Resource licensing is identified as LGPL-LR (SPDX: LGPLLR); see the full license and historical attribution. The Prolexbase project and historical source references are credited in `COPYRIGHT_AND_ATTRIBUTION.md`; all applicable third-party rights and existing notices remain in force. The included reconstruction scripts only recalculate summaries from stored classifications, not their original indicator-derived creation.
