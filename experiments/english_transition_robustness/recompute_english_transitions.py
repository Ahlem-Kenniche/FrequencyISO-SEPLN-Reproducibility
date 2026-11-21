#!/usr/bin/env python3
"""Recompute English adjacent-year FrequencyISO class changes from the distributed SQL.

The source SQL represents years 2019..2023 using NUM_YEAR_FREQUENCY values 19..23.
Counts only year-matched prolexemes whose two codes both belong to 1,2,3.
A change 3->2 (lower number) is toward HIGHER relative notoriety.
This is an archival class audit, not external validation of public attention.
"""
from pathlib import Path
from collections import defaultdict
from importlib.util import spec_from_file_location, module_from_spec
import argparse, csv

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sql',type=Path,default=Path('data/database/prolexbase_without_derivatives_instances.sql'))
    p.add_argument('--out',type=Path,default=Path('experiments/english_transition_robustness/english_annual_transition_rates.csv'))
    p.add_argument('--verify',action='store_true')
    args=p.parse_args()
    # Reuse the repository's SQL INSERT parser for consistent archival handling.
    spec=spec_from_file_location('recompute_tables',Path('scripts/recompute_tables.py'))
    module=module_from_spec(spec);spec.loader.exec_module(module)
    observations=defaultdict(dict)
    for entry,year,code in module.extract_records(args.sql.read_text(encoding='utf-8'),'eng'):
        if 19 <= year <= 23: observations[entry][year]=code
    rows=[]
    for y in range(19,23):
        matched=up=down=0
        for annual in observations.values():
            old,new=annual.get(y),annual.get(y+1)
            if old in (1,2,3) and new in (1,2,3):
                matched+=1
                up+=new<old
                down+=new>old
        rows.append({'period':f'20{y:02d}-20{y+1:02d}','matched_pairs':matched,
                     'upward':up,'downward':down,'transitions':up+down,
                     'change_rate_pct':round(100*(up+down)/matched,4) if matched else None})
    for label,selected in [('2019-2023 (all)',rows),('2020-2023 (excluding 2019-2020)',rows[1:])]:
        agg={key:sum(r[key] for r in selected) for key in ('matched_pairs','upward','downward','transitions')}
        rows.append(dict(period=label,**agg,change_rate_pct=round(100*agg['transitions']/agg['matched_pairs'],4)))
    if args.verify:
        assert [(r['matched_pairs'],r['upward'],r['downward']) for r in rows[:4]] == [(4988,8,617),(4988,75,87),(4988,299,22),(4988,336,35)],rows
        assert [(r['matched_pairs'],r['transitions']) for r in rows[4:]] == [(19952,1479),(14964,854)],rows
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['period','matched_pairs','upward','downward','transitions','change_rate_pct'])
        writer.writeheader();writer.writerows(rows)
    for r in rows:print(r['period'],r['matched_pairs'],r['transitions'],f"{r['change_rate_pct']:.2f}%")
if __name__=='__main__':main()
