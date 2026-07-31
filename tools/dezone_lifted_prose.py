#!/usr/bin/env python3
"""De-zone the consumer prose on zone-span-LIFTED rows. NOT a gate; a one-shot content pass.

WHY THIS EXISTS. `tools/build_zonespan_widen_patch.py` reconciled five warm regions to the
2023 USDA map by `copy.deepcopy`-ing a donor zone's `resolved_by_zone` row onto the new zone
label and stamping `lifted_from_zone`. That was the right data call: the map moved the cities
the regions were authored for, so the row genuinely IS that city's data. But the pass never
rewrote the PROSE, so 66 cells across 15 crops name the DONOR zone to the reader. A
`ca_south_coast` z11 gardener is told "Zone 10 on the south coast almost never freezes".

DE-ZONE, DO NOT RENUMBER. Renumbering looks like the obvious fix and is the wrong one:
  * It would assert zone-specific claims we cannot source. Mandarin's `ca_south_coast` cell
    names the Ojai Pixie; Ojai is not zone 11.
  * De-zoning is safe for every NUMBER in the prose because each donor->lifted pair carries
    an identical `region_chill_delivered` band (low_desert_az 9/10 [100,400]; ca_south_coast
    10/11 [50,350]; ca_desert 10/11 [100,300]; hawaii_tropical 10-13 [0,150]; se_gulf 9/10
    [350,650]). Verified before authoring; the tests pin the figures.
Each rule swaps ONLY the zone-naming noun phrase. Everything after it stays byte-identical,
which is what makes this a label correction rather than a rewrite.

    $ python3 tools/dezone_lifted_prose.py            # report what would change
    $ python3 tools/dezone_lifted_prose.py --diff     # show every before/after string
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

PROSE_SUFFIXES = ('_seasoned', '_beginner')

# A sentence-initial noun phrase that asserts what THIS cell's zone is or does. The trailing
# verb keeps it to assertions; the word blacklist and COMPARATIVE below keep comparisons out.
SELF_REF = re.compile(
    r'(?:^|(?<=[.;] ))(?:[A-Z][a-z-]+(?:[ -][a-z]+){0,3} )?[Zz]ones? (\d{1,2})\b'
    r'(?![^.]*\b(?:hardy|rated|than|compared|colder|warmer|below|above|south of|north of)\b)'
    r'[^.]*?\b(?:is|are|sits|fruits|banks|has|have|does|gets|stays|runs|ripens|grows)\b')

# "As in interior zone 8, pawpaw is marginal here" is correct copy, not a defect.
COMPARATIVE = re.compile(r'(?i)^\s*(?:as in|like|unlike|compared with|versus)\b')

# (zone-naming noun phrase -> replacement). Longest first: several are prefixes of others,
# and "Tropical zone 11" must not fire inside "Tropical zone 11 in Hawaii".
RULES = [
    # -- Hawaii. "Tropical Hawaii" is elevation-neutral; the cells span z10-z13 and the
    #    lower numbers are the COOLER uplands, so "lowland" would be wrong for some.
    ('Zone 11 in tropical Hawaii', 'Tropical Hawaii'),
    ('Tropical zone 11 in Hawaii', 'Tropical Hawaii'),
    ('Zone 11 tropical Hawaii', 'Tropical Hawaii'),
    ('Zone 11 in Hawaii', 'Tropical Hawaii'),
    ('Tropical zone 11', 'Tropical Hawaii'),
    ('Zone 11 Hawaii', 'Tropical Hawaii'),

    # -- California south coast
    ('Zone 10 on the South Coast', 'The South Coast'),
    ('Zone 10 on the south coast', 'The south coast'),
    ('The warmest coastal zone 10', 'The warmest coastal ground'),
    ('The immediate coast in zone 10', 'The immediate coast'),
    ('South-coast zone 10', 'The south coast'),
    ('Zone 10 South Coast', 'The South Coast'),
    ('Zone 10 south coast', 'The south coast'),

    # -- California desert
    ('Zone 10 in the California desert', 'The California desert'),
    ('The hottest desert zone 10', 'The hottest desert'),
    ('Zone 10 in the low desert', 'The low desert'),
    ('Zone 10 in the desert', 'The desert'),
    ('Zone 10 low desert', 'The low desert'),
    ('Zone 10 desert', 'The desert'),

    # -- Arizona low desert
    ('Zone 9 in the Arizona low desert', 'The Arizona low desert'),
    ('The zone 9 Arizona low desert', 'The Arizona low desert'),
    ('Zone 9 in the Arizona desert', 'The Arizona desert'),
    ('Zone 9 Arizona low desert', 'The Arizona low desert'),

    # -- Southeast / Gulf. "The Gulf coast" keeps the WARM-END sense: se_gulf also holds z8,
    #    where "mostly safe for mandarins" would not be true.
    ('Zone 9 across the Gulf region', 'The Gulf coast'),
    ('Zone 9 across the Gulf', 'The Gulf coast'),
    ('Zone 9 in the Southeast', 'The Gulf coast'),
    ('Zone 9 on the Gulf', 'The Gulf coast'),
    ('Zone 9 Gulf', 'The Gulf coast'),
    ('Zone 9 grows', 'The Gulf coast grows'),

    # -- shared low-desert phrasing (ca_desert and low_desert_az both use it)
    ('Low-desert zone 10', 'The low desert'),
    ('Low-desert zone 9', 'The low desert'),

    # -- crop-name-led sentences, where the zone sits mid-clause
    ('Thyme can persist in zone 9', 'Thyme can persist here'),
    ('Thyme takes zone 10 heat', 'Thyme takes the heat'),
    ("Zone 10's mild", 'The mild'),
    ('In zone 10, sage', 'Sage'),
    ('In zone 11, sage', 'Sage'),
    ('In zone 9, sage', 'Sage'),
    ('In zone 9, heat and humidity', 'Heat and humidity'),
]
RULES.sort(key=lambda r: -len(r[0]))

Defect = collections.namedtuple(
    'Defect', 'crop_index slug region zone key text named_zone')


def _self_refs(text, own_zone):
    """Zone numbers this string asserts about ITSELF that are not `own_zone`."""
    out = []
    for m in SELF_REF.finditer(text):
        if m.group(1) == str(own_zone):
            continue
        if COMPARATIVE.match(m.group(0)):
            continue
        out.append(m.group(1))
    return out


def find_defects(data):
    """Prose on a LIFTED row that names a zone other than the row's own."""
    rows = []
    for i, crop in enumerate(data.get('crops') or []):
        for region, rv in (crop.get('regions') or {}).items():
            for zone, cell in ((rv or {}).get('resolved_by_zone') or {}).items():
                if not isinstance(cell, dict) or 'lifted_from_zone' not in cell:
                    continue
                for key, val in cell.items():
                    if not (isinstance(val, str) and key.endswith(PROSE_SUFFIXES)):
                        continue
                    named = _self_refs(val, zone)
                    if named:
                        rows.append(Defect(i, crop['slug'], region, zone, key, val, named[0]))
    return rows


def rule_for(text):
    """The single rule that rewrites this string, or None if we have none."""
    for old, new in RULES:
        if old in text:
            return old, new
    return None


def rewrite(text):
    """De-zoned text, or None when no rule applies -- never a silent pass-through."""
    r = rule_for(text)
    if r is None:
        return None
    old, new = r
    return text.replace(old, new, 1)


def apply(data):
    """Rewrite every defect in place and return `data`. Idempotent."""
    for d in find_defects(data):
        cell = data['crops'][d.crop_index]['regions'][d.region]['resolved_by_zone'][d.zone]
        new = rewrite(cell[d.key])
        if new is None:
            raise SystemExit(
                f'ABORT: no rule for {d.slug}/{d.region}/z{d.zone}.{d.key}: {cell[d.key][:90]!r}')
        cell[d.key] = new
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diff', action='store_true', help='print every before/after string')
    args = ap.parse_args()
    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    defects = find_defects(data)
    cells = {(d.slug, d.region, d.zone) for d in defects}
    print(f'lifted-row prose naming the wrong zone: {len(defects)} strings / '
          f'{len(cells)} cells / {len({d.slug for d in defects})} crops')
    missing = [d for d in defects if rewrite(d.text) is None]
    if missing:
        print(f'  !! {len(missing)} strings have NO rule')
        for d in missing:
            print(f'     {d.slug}/{d.region}/z{d.zone}.{d.key}: {d.text[:100]}')
        return 1
    if args.diff:
        for d in sorted(defects, key=lambda x: (x.slug, x.region, int(x.zone), x.key)):
            print(f'\n--- {d.slug} / {d.region} / z{d.zone} '
                  f'(lifted from z{data["crops"][d.crop_index]["regions"][d.region]["resolved_by_zone"][d.zone]["lifted_from_zone"]}) [{d.key}]')
            print(f'  -  {d.text}')
            print(f'  +  {rewrite(d.text)}')
    else:
        print('  every string has a rule; run with --diff to review the copy')
    return 0


if __name__ == '__main__':
    sys.exit(main())
