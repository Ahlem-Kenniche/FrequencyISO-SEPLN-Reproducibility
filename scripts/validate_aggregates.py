#!/usr/bin/env python3
"""Check internal arithmetic of manuscript-derived aggregate CSVs.
Does NOT recreate FrequencyISO scores or verify underlying data provenance.
"""
from pathlib import Path
import csv
base=Path(__file__).resolve().parents[1]/'data'/'aggregates'
def read(name):
 with (base/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
for r in read('table1_levels_ar_en_fr.csv'):
 labels=sum(int(r[f'level{i}']) for i in [1,2,3]); records=int(r['records'])
 assert labels<=records,(r['language'],labels,records)
 print(f"{r['language']}: {labels} valid ordinal levels, {records-labels} non-ordinal rows")
for r in read('table2_transitions_2019_2023.csv'):
 rate=100*int(r['changed_pairs'])/int(r['matched_adjacent_pairs'])
 assert abs(rate-float(r['transition_pct_reported']))<0.011,(r,rate)
 print(f"{r['language']}: {rate:.2f}% transitions")
for r in read('table3_leave_one_out.csv'):
 assert int(r['deletions_affecting_others'])<=int(r['deletions'])
 assert int(r['labels_changed'])>=int(r['deletions_affecting_others'])
for r in read('frozen_weights_reported.csv'):
 assert int(r['shared_transitions'])+int(r['archive_only_transitions'])==int(r['archived_transitions'])
 assert int(r['shared_transitions'])+int(r['frozen_only_transitions'])==int(r['frozen_weight_transitions'])
 print(f"{r['language']}: frozen-weight transition set arithmetic OK")
print('PASS: reported aggregate arithmetic internally consistent.')
