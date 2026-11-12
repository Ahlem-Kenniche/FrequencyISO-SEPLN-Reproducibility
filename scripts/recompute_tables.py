#!/usr/bin/env python3
"""Recompute Tables 1–2 directly from the distributed Prolexbase SQL export.

Uses Python standard library; no SQL server needed. Reconstructs the archival
annual levels, adjacent-year transitions, and 2019-static disagreement for
2019–2023. This is NOT a rerun of the Shannon–SAW classifier.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
import re

LANGUAGES = {'Arabic':'arb','English':'eng','French':'fra','Polish':'pol','Serbian':'srp'}
ROW = re.compile(r'\((\d+),\s*(\d+),\s*(\d+|NULL)\)')


def extract_records(sql: str, suffix: str):
    inserts = re.finditer(r'INSERT INTO `frequency_' + suffix + r'`[^;]*;', sql, re.S)
    for block in inserts:
        for prolexeme, year, level in ROW.findall(block.group()):
            yield int(prolexeme), int(year), None if level == 'NULL' else int(level)


def compute(sql: str):
    summaries, transitions = [], []
    for name, suffix in LANGUAGES.items():
        records = list(extract_records(sql,suffix))
        levels = Counter(level for _,_,level in records)
        entries = defaultdict(dict)
        for prolexeme, year, level in records:
            if 19 <= year <= 23:
                entries[prolexeme][year] = level
        matched = changes = disagreement = 0
        for annual in entries.values():
            first = annual.get(19)
            for year in range(20,24):
                previous, current = annual.get(year-1), annual.get(year)
                if previous in (1,2,3) and current in (1,2,3):
                    matched += 1
                    changes += previous != current
                    # Static baseline: first observed level in 2019, on this matched cohort
                    if first in (1,2,3):
                        disagreement += first != current
        summaries.append(dict(language=name,records=len(records),distinct_entries=len({p for p,_,_ in records}),level1=levels[1],level2=levels[2],level3=levels[3],non_ordinal=len(records)-sum(levels[l] for l in (1,2,3))))
        transitions.append(dict(language=name,matched_adjacent_pairs=matched,changed_pairs=changes,transition_pct=round(100*changes/matched,2),static_mismatch_pct=round(100*disagreement/matched,2)))
    return summaries, transitions


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sql',type=Path,default=Path('data/database/prolexbase_without_derivatives_instances.sql'))
    parser.add_argument('--verify',action='store_true',help='compare recalculated counts and displayed percentages against manuscript CSVs')
    parser.add_argument('--out',type=Path,default=Path('data/recomputed'),help='CSV output directory')
    args=parser.parse_args()
    summaries,transitions=compute(args.sql.read_text(encoding='utf-8'))
    args.out.mkdir(parents=True,exist_ok=True)
    for name,rows in [('table1_all_languages_from_sql.csv',summaries),('table2_from_sql.csv',transitions)]:
        with (args.out/name).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    if args.verify:
        with Path('data/aggregates/table1_levels_ar_en_fr.csv').open(newline='',encoding='utf-8') as f: expected1=list(csv.DictReader(f))
        with Path('data/aggregates/table2_transitions_2019_2023.csv').open(newline='',encoding='utf-8') as f: expected2=list(csv.DictReader(f))
        m1={r['language']:r for r in summaries};m2={r['language']:r for r in transitions}
        for e in expected1:
            actual=m1[e['language']]
            for field in ('records','distinct_entries','level1','level2','level3'):
                assert int(e[field])==actual[field],f"Table 1: {e['language']} {field}: {e[field]} != {actual[field]}"
        for e in expected2:
            actual=m2[e['language']]
            for field in ('matched_adjacent_pairs','changed_pairs'):
                assert int(e[field])==actual[field],f"Table 2: {e['language']} {field}"
            for old,new in [('transition_pct_reported','transition_pct'),('static_mismatch_pct_reported','static_mismatch_pct')]:
                assert abs(float(e[old])-actual[new]) < 0.001,f"Table 2: {e['language']} {old}"
        print('PASS: Tables 1 and 2 match the SQL export.')
    for d in transitions:
        print(f"{d['language']}: {d['changed_pairs']}/{d['matched_adjacent_pairs']} = {d['transition_pct']:.2f}%; static mismatch {d['static_mismatch_pct']:.2f}%")
    print('NOT TESTED: Shannon–SAW rerun, leave-one-out sensitivity, ablations, frozen weights.')

if __name__=='__main__':main()
