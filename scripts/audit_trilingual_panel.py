#!/usr/bin/env python3
"""Audit pivot alignment using only the supplied SQL, not the original analytic population.

WARNING: the shipped SQL contains English frequency IDs with no matching
prolexeme_eng row. Consequently its trilingual join is not a complete
reproduction of the manuscript panel, and discrepancies must not be
silently 'fixed' by rewriting the manuscript.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse, re

LANGS = ('arb', 'eng', 'fra')

def parse_sql(sql):
    out = {}
    for lang in LANGS:
        prolexeme_to_pivot = {}
        for block in re.finditer(r'INSERT INTO `prolexeme_' + lang + r'`[^;]*;', sql, re.S):
            for line in block.group().splitlines():
                m = re.match(r'^\((\d+),.*?,\s*(\d+|NULL),\s*(?:\'|NULL)', line)
                if m and m.group(2) != 'NULL':
                    prolexeme_to_pivot[int(m.group(1))] = int(m.group(2))
        annual = defaultdict(dict)
        for block in re.finditer(r'INSERT INTO `frequency_' + lang + r'`[^;]*;', sql, re.S):
            for pid, year, level in re.findall(r'\((\d+),\s*(\d+),\s*(\d+|NULL)\)', block.group()):
                if 19 <= int(year) <= 23 and level in ('1','2','3'):
                    annual[int(pid)][int(year)] = int(level)
        pivot_to_entries = defaultdict(list)
        for pid, values in annual.items():
            if len(values) == 5 and pid in prolexeme_to_pivot:
                pivot_to_entries[prolexeme_to_pivot[pid]].append((pid, tuple(values[y] for y in range(19,24))))
        unmatched = len(set(annual).difference(prolexeme_to_pivot))
        print(f'{lang}: prolexeme rows={len(prolexeme_to_pivot)}, frequency IDs in 2019–2023 unmatched to prolexeme={unmatched}, complete-series pivots={len(pivot_to_entries)}')
        out[lang] = pivot_to_entries
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sql',type=Path,default=Path('data/database/prolexbase_without_derivatives_instances.sql'))
    args=parser.parse_args()
    a=parse_sql(args.sql.read_text(encoding='utf-8'))
    common=set.intersection(*(set(a[l]) for l in LANGS))
    unique={pivot for pivot in common if all(len(a[l][pivot])==1 for l in LANGS)}
    print('Common pivots with >=1 complete-series entry in each language:',len(common))
    print('Common pivots with exactly 1 complete-series entry in each language:',len(unique))
    direction=Counter()
    for pivot in unique:
        for lang in LANGS:
            vals=a[lang][pivot][0][1]
            for prev,now in zip(vals,vals[1:]):
                if now!=prev:direction[(lang,'higher' if now<prev else 'lower')]+=1
    for lang in LANGS:
        print(lang, 'higher',direction[(lang,'higher')],'lower',direction[(lang,'lower')])
    print('STATUS: not equivalent to manuscript panel; must reconcile missing English prolexeme mappings and selection provenance.')
if __name__ == '__main__':main()
