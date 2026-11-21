# FrequencyISO – GDELT exploratory news-proxy supplement (peer-review edition)

## Purpose and scope
This package contains *all nine* English-language class-changing cases from the feasibility pilot and *all three* stable-class controls. The experiment tests the feasibility of extracting news-proxy comparisons independent of Wikipedia, not the validity of annual notoriety classes.

## Selection
The feasibility pilot contains nine evaluated English-language referents with transitions between 2022 and 2023: **six upward** and **three downward**. These nine cases were assembled from a previously stratified candidate list, including Milan Kundera from an earlier feasibility test and Roman Abramovich from a subsequent pilot. An initial seeded draw (`random_state=42`) was performed within direction strata for part of the candidate set, but the final nine evaluated cases are **not the direct output of a single five-per-stratum seeded draw**. The pilot selection is non-representative and must not be described as random sampling from the full Prolexbase population. Three stable-class controls were chosen purposively. Original upstream population construction is not fully reproduced by the distributed files. All evaluated cases, positive and negative, are retained in `gdelt_case_counts.csv`.

## Sampling calendars
- Calendar 1: January 15, April 15, July 15, October 15 in **each of 2022 and 2023**, four days per year. All twelve cases use this calendar.
- Calendar 2: January 4, February 11, March 17, April 17, May 21, June 28, July 4, August 8 in **each of 2022 and 2023**, eight days per year. Only Milan Kundera, Roman Abramovich, Mel Gibson were tested; the remainder are explicitly **not tested**, not assumed robust.

## Data source and query semantics
Source: Google BigQuery public table `gdelt-bq.gdeltv2.webngrams` (GDELT Web Ngrams), accessed during the November 2026 pilot. Yearly labels refer to 2022 and 2023; the news-proxy observations are **only sampled days**. Each SQL query restricts `lang='en'`, matches the exact `ngram` first-token value and `STARTS_WITH(post, remaining_name)` case-sensitively. No alternative spelling, homonym disambiguation or additional identity matching was conducted. These prefixes may include unintended matches, and URL duplicates or syndicated articles may remain. `COUNT(DISTINCT url)` counts distinct URLs matching the expression among the sampled days, not independently verified articles. The rates are not normalized against total indexed English-language URLs. A zero denotes no match under the chosen query and dates, not no coverage.

See `query_templates.sql` for the timestamp-range BigQuery SQL shape and `query_mappings.csv` for names actually queried. These **templates reconstruct the declared query design**, but original cloud job IDs and complete execution logs are not available in this package. Reported counts were transcribed from the Colab outputs of the experiment; they cannot be independently re-extracted from the local data alone.

## Statistical interpretation
FrequencyISO direction is `up` for movement toward level 1 (e.g. 3→2) and `down` toward level 3. News direction is the difference between the sampled URL counts in 2023 and 2022. Six of nine changing cases agreed (66.7%). The exact two-sided binomial p-value versus 0.5 is approximately 0.508, used as an illustrative reference only; unequal directional marginals and selected cases make 0.5 an imperfect null. Three stable controls are descriptive; `N/A` is the only valid directional-match classification for them. No broad external validity or annual media-trend claim follows.

## Files
- `gdelt_case_counts.csv`: counts for all 12 cases and both calendars where available
- `query_mappings.csv`: exact first-token, `post` prefix, language and special orthography choices
- `query_templates.sql`: query template matching the BigQuery procedure
- `analyze_cases.py`: arithmetic and directional agreement calculation from recorded counts
- `sampling_dates.csv`: exact paired dates

## Limitations
No full-year sampling, normalization to all available news URLs, alternative-script coverage or systematic manual resolution of homonyms. Calendar 2 was applied to three cases only. The repository avoids any claim of completed independent external validation.

## Reproducibility and redistribution
This supplement uses the English-language news queries, not the separate Arabic Lisa Marie Presley demonstration. Recorded GDELT counts are transcribed from interactive BigQuery outputs; no GDELT raw articles are redistributed. Prolexbase candidate data are included under the resource license noted in the repository root. The 2022–2023 comparison is an exploratory feasibility check only.
