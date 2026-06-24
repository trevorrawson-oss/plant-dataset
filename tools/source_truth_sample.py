#!/usr/bin/env python3
"""Source-truth sampling helper (Phase C standing QA).

Dumps the EFFECTIVE plant + harvest windows for region calendar cells, grouped by
region, so a per-batch adversarial source-truth sample can be handed to region-scoped
verification agents (each agent WebFetches that region's T1 extension planting calendar
and checks the windows). This is the data-extraction half of the QA loop documented in
`docs/source_truth_sampling_qa_v1_0.md`.

KEY RULE -- the effective plant window is the UNION of the `plant_out` string and the
`calendar[]` `plant` tokens. Region-primary cells store their sow windows in the calendar,
NOT in plant_out (which is often null). Checking only `plant_out` produces false positives
(the broccoli "harvest with no planting behind it" retraction). This tool unions both so the
verifier sees what actually renders.

NOT A GATE. Source-truth cannot be gated, only sampled (see the process doc). This tool has
no pass/fail; it only prepares the sample.

Usage:
  python3 tools/source_truth_sample.py                         # all annual crops, all regions
  python3 tools/source_truth_sample.py --regions ca_desert low_desert_az
  python3 tools/source_truth_sample.py --crops carrot lettuce-leaf --regions northern_tier
  python3 tools/source_truth_sample.py --dataset path/to/crops_data_final.json
"""
import argparse
import json
import os

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Crops with region-calendared annual windows where regional date-truth matters most.
# (Trees/berries/indoor use other models; sample them separately when relevant.)
DEFAULT_ANNUAL_CROPS = [
    'cherry-tomato', 'beefsteak-tomato', 'carrot', 'basil', 'zinnia',
    'green-beans-bush', 'zucchini-courgette', 'broccoli', 'lettuce-leaf', 'onion',
]


def tok_months(cal, tok):
    if not isinstance(cal, list) or len(cal) != 12:
        return []
    return [MONTHS[i] for i, t in enumerate(cal) if t == tok]


def effective_plant_months(plant_out, cal):
    """The EFFECTIVE plant window = calendar `plant` tokens UNION month names parsed out
    of the `plant_out` string. Returned in calendar order."""
    months = set(tok_months(cal, 'plant'))
    for raw in (plant_out or '').replace('-', ' ').replace(',', ' ').split():
        name = raw[:3].capitalize()
        if name in MONTHS:
            months.add(name)
    return sorted(months, key=MONTHS.index)


def iter_cells(data, crops, regions):
    by_slug = {c['slug']: c for c in data['crops']}
    for slug in crops:
        crop = by_slug.get(slug)
        if not crop:
            continue
        for rname, rblock in (crop.get('regions') or {}).items():
            if regions and rname not in regions:
                continue
            rbz = rblock.get('resolved_by_zone') or {}
            label = rblock.get('region_label') or rblock.get('label') or rname
            for z, cell in sorted(rbz.items(),
                                  key=lambda kv: int(kv[0]) if kv[0].isdigit() else 99):
                yield slug, rname, z, label, cell


def render(data, crops, regions):
    lines = []
    # group by region so each block can go to one region-scoped verifier
    seen_regions = []
    for rname in (regions or _all_regions(data, crops)):
        block = []
        for slug, rn, z, label, cell in iter_cells(data, crops, [rname]):
            cal = cell.get('calendar')
            eff = effective_plant_months(cell.get('plant_out'), cal)
            yr = '  YEAR_ROUND' if cell.get('year_round') else ''
            block.append(f'\n  {slug}  [{rn} z{z}]  "{label}"{yr}')
            block.append(f'      EFFECTIVE plant (plant_out UNION calendar): {eff}')
            block.append(f'      harvest string: {cell.get("harvest")!r}')
            heat = tok_months(cal, 'heat_pause')
            cold = tok_months(cal, 'cold_pause')
            if heat:
                block.append(f'      heat_pause (too hot to SOW, not no-harvest): {heat}')
            if cold:
                block.append(f'      cold_pause (frost, too cold to sow): {cold}')
        if block:
            lines.append(f'\n################ REGION: {rname} ################')
            lines.extend(block)
            seen_regions.append(rname)
    return '\n'.join(lines)


def _all_regions(data, crops):
    out = []
    for _, rname, _, _, _ in iter_cells(data, crops, None):
        if rname not in out:
            out.append(rname)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--dataset', default=os.path.join(here, 'crops_data_final.json'))
    ap.add_argument('--crops', nargs='*', default=DEFAULT_ANNUAL_CROPS)
    ap.add_argument('--regions', nargs='*', default=None)
    args = ap.parse_args()
    with open(args.dataset) as f:
        data = json.load(f)
    print(render(data, args.crops, args.regions))


if __name__ == '__main__':
    main()
