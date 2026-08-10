"""Structural guards for tools/hunt_footprint.py -- the canonical hunt-footprint list.

These pin the FOOTPRINT's structure to the ledger with LITERAL expectations (never values
computed from the module under test -- `computed-guard-expectations-are-vacuous`). They do
not pin canonical-dependent counts; those live in the PLA-187 report, dated.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hunt_footprint as hf


def test_footprint_is_the_ledgers_32_hunts_exactly_once_each():
    hunt_numbers = sorted(h for h, _ in hf.FOOTPRINT.values())
    assert hunt_numbers == list(range(1, 33))


def test_campaign_partition_matches_the_ledger_table():
    # A 8 (#3-6, #9-12) / B 2 (#1, #2) / C 7 (#7, #8, #13, #14, #17, #21, #24) /
    # D 11 own (#16, #18, #23, #25-32) / withdrawn 4 (the ucr_citrus hunts).
    by_camp = {}
    for hunt, camp in hf.FOOTPRINT.values():
        by_camp.setdefault(camp, set()).add(hunt)
    assert by_camp['A'] == {3, 4, 5, 6, 9, 10, 11, 12}
    assert by_camp['B'] == {1, 2}
    assert by_camp['C'] == {7, 8, 13, 14, 17, 21, 24}
    assert by_camp['D'] == {16, 18, 23, 25, 26, 27, 28, 29, 30, 31, 32}
    assert by_camp['withdrawn'] == {15, 19, 20, 22}


def test_residue_pairs_are_the_seven_d_reprice_pins_and_all_in_footprint():
    assert len(hf.RESIDUE_PAIRS) == 7
    assert hf.RESIDUE_PAIRS <= set(hf.FOOTPRINT)
    from campaign_d_reprice import RESIDUE_HUNTS
    assert hf.RESIDUE_PAIRS == set(RESIDUE_HUNTS)


def test_citrus_residue_reassigns_to_d_and_non_citrus_does_not():
    assert hf.campaign_of('ca_interior', 'ucanr_ext', 'lime') == (3, 'D(residue)')
    assert hf.campaign_of('ca_interior', 'ucanr_ext', 'arugula') == (3, 'A')
    assert hf.campaign_of('rgv', 'tamu_agrilife', 'basil') == (13, 'C')
    assert hf.campaign_of('pnw', 'clemson_hgic', 'basil') == (None, None)


def test_same_institution_families_bridge_id_spelling_variants():
    # the miss that undercounted SAMEINST: two spellings of one institution
    assert hf.family('ufifas_ext') == hf.family('uf_ifas_vh021')
    assert hf.family('uc_mg') == hf.family('ucanr_ext_mg_timeplanting')
    assert hf.family('uc_mg') == hf.family('uc_ipm')
    assert hf.family('nmsu_ext') != hf.family('tamu_agrilife')


def test_the_two_walks_agree_on_live_canonical():
    with open(hf.CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    hf.decisions(data)  # raises on walk disagreement


def test_walk_crosscheck_actually_fires_on_a_defective_scanner():
    # RED-team the guard itself: sneak a dataset the two walks MUST disagree on is not
    # possible (they read the same data), so instead prove the assertion is reachable by
    # breaking one walker's view -- a sources-only citation flips is_sole in both walks
    # identically, so the only way they diverge is a code defect; simulate one.
    import bare_host_scan
    real = bare_host_scan.scan
    try:
        bare_host_scan.scan = lambda data: []
        hf.scan = bare_host_scan.scan
        with open(hf.CANONICAL, encoding='utf-8') as fh:
            data = json.load(fh)
        try:
            hf.decisions(data)
        except AssertionError:
            return
        raise SystemExit('cross-check guard is vacuous: a scanner returning nothing passed')
    finally:
        bare_host_scan.scan = real
        hf.scan = real
