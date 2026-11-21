# Copyright, attribution, and provenance

**Resource:** Prolexbase 4.1 (filtered research distribution).  
**Linguistic-resource licence:** Lesser General Public License for Linguistic Resources (LGPL-LR; SPDX `LGPLLR`). The text is supplied in `LICENSE-LGPLLR.txt`.

## Resource provenance and scholarly attribution

Prolexbase is a multilingual proper-name lexical resource developed within the **Prolex research project**, led by the computer science research laboratory at the **University of Tours (France)**, with contributions from collaborating research teams. The resource's historical development and its data model are described in the following publications:

- Tran, M. and Maurel, D. (2006). *Prolexbase : un dictionnaire relationnel multilingue de noms propres*. *Traitement automatique des langues*, 47(3), 115–139.
- Bouchou, B. and Maurel, D. (2008). *Prolexbase et LMF : vers un standard pour les ressources lexicales sur les noms propres*. *Traitement automatique des langues*, 49(1), 61–88.
- Maurel, D. (2008). *Prolexbase: a Multilingual Relational Lexical Database of Proper Names*. In *Proceedings of the Sixth International Conference on Language Resources and Evaluation (LREC 2008)*, Marrakech, Morocco. European Language Resources Association (ELRA). https://aclanthology.org/L08-1435/

Institutional reference and recommended citations: https://tln.lifat.univ-tours.fr/version-francaise/ressources/prolex-unitex  
Resource distribution reference: https://www.ortolang.fr/market/lexicons/prolex  
LGPL-LR terms: https://tln.lifat.univ-tours.fr/version-francaise/liens-utiles/licence-lgpl-lr

These citations acknowledge the original research and development of Prolexbase. The resource and its historical contributions remain subject to the rights, licence conditions, and attribution notices associated with their respective sources.

## Modifications in this companion distribution

**Modified research distribution prepared 2026-11-10.** The supplied Prolexbase 4.1 SQL export was filtered to exclude tables with prefixes `derivative_` and `instance_`, the `derivative_category` table, and related foreign-key statements. The remaining SQL contents were retained. The database header was generalized for anonymous review. See `docs/DATABASE_PROVENANCE.md` and `docs/DATABASE_TABLES.txt` for details.

The submitting research team (identities withheld for double-blind review) contributed to the integration of Arabic into multilingual Prolexbase and to the development of the FrequencyISO component for language- and year-specific notoriety records. This companion package documents the year-indexed FrequencyISO representation and its computational evaluation. These contributions are distinct from the original Prolexbase architecture and earlier work acknowledged in the references above. The original project and prior scholarly contributions remain fully attributed.

## Redistribution and acknowledgement

The Prolexbase linguistic-resource component is distributed with the LGPL-LR licence text and source citations. Redistributors should retain the licence, modification notice and relevant source acknowledgements, and observe any rights notices applicable to individual contributed materials. The supplementary research scripts are not assigned a blanket licence by the linguistic-resource licence alone.

**Double-blind review:** submitting-author identities and affiliations are omitted from this peer-review package. This anonymization does not remove historical scholarly attribution.
