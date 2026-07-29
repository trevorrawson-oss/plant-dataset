#!/usr/bin/env python3
"""Hardening item 2: discharge the three thin asparagus values.

docs/2026-07-26-post-asparagus-hardening-kickoff.md item 2 -- "each of 2a/2b/2c is either
re-sourced or has a written acceptance recorded in its open_finding, with the finding's
status updated accordingly."

TWO KINDS OF CHANGE, kept separable:

(A) DATA -- warm_arid z8 provenance RE-ANCHORED (2a). The window "Feb 1 - Feb 28" is
    UNCHANGED; only its provenance moves, from drawn-bar geometry to extension TEXT.
    TAMU EHT-066 "Easy Gardening: Asparagus" states verbatim: "Asparagus is grown from
    1- or 2-year-old crowns planted in January or February, or as soon as the ground can
    be worked." Verified in this session by urllib download + pypdf extraction (HTTP 200,
    1,301,793 bytes, 42 asparagus mentions), NOT from a WebFetch summary.
    Geography is authorized by the dataset's own region_source_map, which labels this
    region "Warm Arid (S. NM / W. TX)" and names tamu_agrilife as its z8 anchor for the
    "far-west TX / El Paso corridor"; EHT-066 itself names West Texas as one of the two
    areas asparagus is best suited to. resolution_method moves to the value an existing
    warm_arid z8 cell already uses (lettuce-leaf, sources ['nmsu_ext','tamu_agrilife'])
    rather than inventing an 81st method string.

(B) FINDINGS -- dated dispositions appended to findings 9, 10, 11, 21, with statuses set.
    Findings are append-only in the same spirit as verification_log_ref
    (docs/verification_log_ref_convention.md): the original text stays byte-for-byte and
    a dated line is concatenated, because finding 21 is itself proof of the hazard -- it
    sat `open` asserting a z9 harvest of "Feb - Mar" two revisions after the value became
    "Mar - May", and that stale text is what caused a full re-sourcing pass to be
    commissioned against a value that no longer existed.

Guards: canonical SHA; each finding's expected tail present verbatim; no finding already
carrying a 2026-07-29 disposition; the z8 window string UNCHANGED by this script.

Writes COMPACT per CLAUDE.md.
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

EXPECT_SHA = 'b961d502b280d3703463372cbbea58519631e8a93abde9c2ac54bc25846a1db1'

EHT066_URL = 'https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2021/03/EHT-066.pdf'
WINDOW = 'Feb 1 - Feb 28 (dormant crowns, one-time planting)'

DISPOSITIONS = {
    9: ('...UMaine, Iowa State/Illinois, UConn, Missouri).', 'open',
        ' DISPOSITION 2026-07-29 (hardening item 2b): the zone-keyed gap is CONFIRMED and '
        'FORMALLY ACCEPTED, and the ladder VALUES are upheld. A fresh multi-state hunt found '
        'the regional source this finding said did not exist, and it argues FOR accepting the '
        'gap rather than closing it: the Midwest Vegetable Production Guide (an 8-state '
        'land-grant collaboration spanning z3b-z7a, MSU-published) states one undifferentiated '
        'window for the whole footprint, verbatim "Transplant April 15 to May 15", with ZERO '
        'zone-keyed references anywhere in its asparagus section (verified here by pypdf '
        'extraction, HTTP 200, 8 pages, 44 asparagus mentions). So the multi-state literature '
        'does not resolve by zone either; a five-rung ladder is finer than any source, which is '
        'what state_source_zone_mapped already says. Each rung was re-verified against a '
        'verbatim in-state T1 quote and all five land inside their anchor (z3 May 1 vs UMN and '
        'NDSU "early May"; z4 Apr 20 vs SDSU "mid-April through June"; z5 Apr 10 vs Iowa State '
        '"early spring (April)"; z6 Apr 1 vs UConn "early April to late May"; z7 Mar 20 vs '
        'Missouri G6405 "late March or early April"). RE-DERIVATION FROM FROST WAS TESTED AND '
        'REJECTED: the ladder steps 10-11 days per zone while zone frost steps 14-15, so a '
        'constant offset reproduces z3-z5 and breaks z6 (Mar 18 against UConn early April) and '
        'z7 (Mar 1 against three sources saying late March or April). Crown timing is soil-thaw '
        'and nursery-shipping bound at the ends, not frost-bound, so the non-constant offset on '
        'this frost_anchored crop is DELIBERATE. Do not re-open on sourcing effort. The '
        'CITATION defects this hunt surfaced are a separate arc, filed below.'),
    10: ('...Revisit if a crown-rot finding contradicts it.', 'open',
         ' DISPOSITION 2026-07-29 (hardening item 2b): the soil-workability ruling is UPHELD on '
         'a re-adjudication with fresh eyes, and one part of this finding is RETRACTED as '
         'fabricated. CAMP COUNT, all verbatim: soil-workability has FIVE independent '
         'institutions (Illinois, Missouri in two documents, UConn, Arkansas, Oregon State); '
         'frost-safe has ONE (UMaine Bulletin #2071). A real agronomic tie-breaker exists and is '
         'sourced, which this finding said was missing: Missouri G6405 states "Spring freezes '
         'will not harm the crowns or subsequent harvests but can damage emerging spears", i.e. '
         'the frost hazard is to EMERGED SPEARS, not to dormant crowns, which is the frost-safe '
         'rule\'s whole premise. And the literature\'s actual frost lever is planting DEPTH, not '
         'DATE, including in UMaine\'s own document ("Planting crowns too shallowly will '
         'encourage spears to emerge too early, making them more susceptible to frost injury"), '
         'with SDSU and UConn saying the same. UMaine is also the outlier against its own '
         'regional guide: the 6-state New England Vegetable Management Guide applies "after the '
         'danger of frost has passed" only to 8-to-12-week-old SEEDLING transplants and gives '
         'crowns no date at all. RETRACTION: the "Fusarium-in-cold-wet-soil rationale" this '
         'finding attributes to UMaine IS NOT IN BULLETIN #2071. Verified here by direct fetch '
         'and tag-strip (HTTP 200, 50 asparagus mentions): the document contains five Fusarium '
         'statements, none of them a cold-wet-soil argument, and the strings "cold wet", "cold, '
         'wet", "wet soil" and "cold soil" each occur ZERO times. UMaine gives the after-frost '
         'rule bare, with only a 50F soil threshold and no stated reason. The rationale was '
         'invented by an earlier pass and must not be reasoned from. The ruling stands on the '
         'camp count plus the two real tie-breakers above.'),
    11: ('...if one publishes an asparagus date.', 'resolved',
         ' RESOLVED 2026-07-29 (hardening item 2a): the window is UNCHANGED at Feb 1 - Feb 28 '
         'and its provenance is no longer geometry. TAMU EHT-066 "Easy Gardening: Asparagus" '
         '(Joseph Masabni, rev. 5/14) states in TEXT: "Asparagus is grown from 1- or '
         '2-year-old crowns planted in January or February, or as soon as the ground can be '
         'worked." Verified by urllib download + pypdf extraction, HTTP 200, 1,301,793 bytes, 42 '
         'asparagus mentions, NOT a WebFetch summary. Its geography is authorized by this '
         'dataset\'s own region_source_map, which labels the region "Warm Arid (S. NM / W. TX)" '
         'and names tamu_agrilife the z8 anchor for the far-west TX / El Paso corridor, and by '
         'EHT-066 itself naming West Texas one of the two areas the crop is best suited to. '
         'The cell now cites tamu_agrilife alongside nmsu_ext with resolution_method '
         'nmsu_tamu_arid_month_resolution, matching the existing warm_arid z8 precedent on '
         'lettuce-leaf; nmsu_chart is retained as CORROBORATION rather than sole authority, so '
         'the drawn-bar geometry and the Shillingburg/Las-Cruces provenance weaknesses stop '
         'being load-bearing. THE SEARCH FOR AN NMSU DATE IS CLOSED, not merely unfinished: '
         'NMSU H-227, CR-457 and CR-457-B (the last revised January 2026) were all read and '
         'none publishes an asparagus crown date; CR-457-B\'s planting table has no date columns '
         'at all, and the El Paso County MG planting calendar omits asparagus entirely. '
         'RESIDUAL CAVEAT, now the honest one: the MONTH is text-sourced and independently '
         'corroborated by USDA NRCS SCAN 8-inch soil data at Jornada Experimental Range in Dona '
         'Ana County (median first sustained 50F crossing Feb 2 over 2010-2025, against NMSU '
         'H-227\'s own "plant crowns in the spring after the soil temperature has reached 50F" '
         'criterion); the DAY EDGES are conventions no source publishes, and the higher-elevation '
         'z8 fringe likely runs one to three weeks later than the Rio Grande valley. Do not '
         'widen into March: that would collide with the region\'s own March spear emergence.'),
    21: ('...If z9 is ever re-sourced, revisit the pair together.', 'resolved',
         ' RESOLVED 2026-07-29 (hardening item 2c). THIS FINDING WAS ITSELF THE LIVE DEFECT: it '
         'sat `open` asserting z9 carries "Feb - Mar" and z10 reads later, two revisions after '
         'commit 7738de1 (2026-07-27) moved z9 to "Mar - May" and its plant_out to Jan 1 - Mar '
         '1. Current values are z9 "Mar - May" and z10 "Mar - Apr", so BOTH START IN MARCH and '
         'there is no inversion left to fix; zone_order_gate and harvest_duration_gate both '
         'return 0. The stale finding text is what caused a full re-sourcing pass to be '
         'commissioned against a value that no longer existed, which is the same hazard ruled on '
         'for verification_log_ref the same day (docs/verification_log_ref_convention.md). The '
         're-source it asked for WAS performed anyway and returned nothing, for a GEOGRAPHIC '
         'rather than an effort reason, and that closes the re-open door: UC\'s four-district '
         'California planting scheme scopes "Desert Valleys" to the Imperial and Coachella '
         'valleys, which is z10, so neither Barstow nor the Palo Verde Valley sits inside ANY UC '
         'district and no UC crop publication will ever cover z9 by construction. The two county '
         'programs that do cover that ground (UCCE MG San Bernardino and UC MG Riverside) '
         'publish planting-only monthly lists with no harvest month. z9 therefore keeps '
         'harvest_sourced_duration_modeled_start permanently. TWO THINGS SURFACED AND FILED '
         'RATHER THAN PAPERED OVER: the uc_ipm URL cited on ca_desert z9/z10/z11 resolves to UC '
         'IPM\'s ARCHIVED cultural-tips page, which self-labels "not actively maintained ... All '
         'links have been removed", while a live equivalent exists and additionally carries a '
         'California-specific 3-4 week / 8-10 week harvest ramp; and z9 is climatically BIMODAL '
         '(Barstow around 2,100 ft high desert against Blythe around 270 ft low desert, which '
         'reads 10a on the 2023 USDA map) while its prose describes only the cooler half.'),
}


def die(msg):
    print(f'ABORT: {msg}', file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    raw = open(CANONICAL, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        die(f'canonical SHA drift.\n  expected {EXPECT_SHA}\n  found    {sha}')
    print(f'canonical SHA verified: {sha[:8]}')

    data = json.loads(raw.decode('utf-8'))
    before = copy.deepcopy(data)
    crop = [c for c in data['crops'] if c['slug'] == 'asparagus'][0]

    # ---- (A) warm_arid z8 provenance re-anchor. The WINDOW must not move. ----
    cell = crop['regions']['warm_arid']['resolved_by_zone']['8']
    if cell.get('plant_out') != WINDOW:
        die(f'warm_arid z8 plant_out is {cell.get("plant_out")!r}, expected {WINDOW!r}')
    if cell.get('resolution_method') != 'extension_chart_geometry':
        die(f'warm_arid z8 resolution_method is {cell.get("resolution_method")!r}, '
            f'expected extension_chart_geometry')
    if sorted(cell.get('sources') or []) != ['nmsu_chart', 'nmsu_ext']:
        die(f'warm_arid z8 sources drift: {cell.get("sources")}')
    if 'tamu_agrilife' not in data['source_catalog']:
        die('tamu_agrilife missing from source_catalog')

    cell['sources'] = ['nmsu_ext', 'nmsu_chart', 'tamu_agrilife']
    cell['anchoring_urls']['tamu_agrilife'] = {'url': EHT066_URL, 'verified': '2026-07-29'}
    cell['resolution_method'] = 'nmsu_tamu_arid_month_resolution'
    if cell['plant_out'] != WINDOW:
        die('window moved; this script must never change it')
    print('  2a: warm_arid z8 re-anchored (window UNCHANGED, +tamu_agrilife, method '
          '-> nmsu_tamu_arid_month_resolution)')

    # ---- (B) finding dispositions, append-only ----
    findings = crop['verification_status']['open_findings']
    for idx, (tail, status, addendum) in DISPOSITIONS.items():
        f = findings[idx]
        key = 'summary' if f.get('summary') else 'finding'
        text = f[key]
        expected_tail = tail[3:] if tail.startswith('...') else tail
        if not text.endswith(expected_tail):
            die(f'finding[{idx}] tail mismatch.\n  expected ...{expected_tail!r}\n'
                f'  found    ...{text[-len(expected_tail):]!r}')
        if '2026-07-29' in text:
            die(f'finding[{idx}] already carries a 2026-07-29 disposition')
        f[key] = text + addendum
        if not f[key].startswith(text):
            die(f'finding[{idx}] append-only violated')
        f['status'] = status
        print(f'  finding[{idx}] {f.get("id")}: +{len(addendum)} chars, status -> {status}')

    # ---- footprint ----
    b = {c['slug']: c for c in before['crops']}
    n = {c['slug']: c for c in data['crops']}
    diff = [s for s in b if b[s] != n[s]]
    if diff != ['asparagus']:
        die(f'footprint: crops changed {diff}, expected only asparagus')
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            die(f'top-level key {k!r} changed')
    print('  footprint: asparagus only, no top-level change')

    out = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if out.endswith('\n'):
        die('refusing to write a trailing newline')
    if args.dry_run:
        print(f'\nDRY RUN. Would become: {hashlib.sha256(out.encode("utf-8")).hexdigest()}')
        return 0
    with open(CANONICAL, 'w', encoding='utf-8') as fh:
        fh.write(out)
    print(f'\nwritten. canonical {EXPECT_SHA[:8]} -> '
          f'{hashlib.sha256(open(CANONICAL, "rb").read()).hexdigest()[:8]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
