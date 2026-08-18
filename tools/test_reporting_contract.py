#!/usr/bin/env python3
"""RED-first suite for tools/reporting_contract.py (PLA-161, predicate 2).

THE NAMED RED CASE, reproduced live from the tool before this file was written:

    $ python3 tools/campaign_c_reprice.py
    HONEST OPEN after re-scope :  0 of 25 decisions,   0 of 68 nodes

  printed while campaign C's own seven hunts carry 196 MASKED node-citations over 39 MASKED-ONLY
  decisions, which `if not sole: continue` removed before counting. The zero is true of what it
  counted and silent about what it filtered away.

  Second half of the same case: hunt #24 (warm_arid/nmsu_chart) and hunt #17
  (warm_arid/nmsu_donaana_mg) BOTH contribute zero rows. #24 is genuinely fixed; #17 is 0 SOLE /
  18 MASKED. Nothing in the output distinguished them.

UNITS are named on every count here, because sliding between NODES and DECISIONS is how this arc
kept re-pricing itself.
"""
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import reporting_contract as RC  # noqa: E402

# Campaign C's close, transcribed from the tool's own output -- NOT computed from the predicate
# it validates ([[computed-guard-expectations-are-vacuous]]).
#
# TWO MASKED-ROW NUMBERS EXIST AND THEY ARE BOTH RIGHT. PLA-161's table says 196: every masked
# node-citation in C's seven hunts, including rows on decisions that ALSO have SOLE rows. The
# contract wants 195: masked rows on MASKED-ONLY decisions -- the ones no campaign counted at all.
# A decision with even one SOLE row DID enter a denominator. The gap is one row, and it is a unit
# difference rather than drift; stated here so the next reader does not "fix" one into the other.
C_OPEN_DECISIONS = 0
C_TOTAL_DECISIONS = 25
C_MASKED_DECISIONS = 39      # MASKED-ONLY DECISIONS in C's hunts
C_MASKED_ROWS = 195          # masked node-CITATIONS on those masked-only decisions
C_ALL_MASKED_ROWS = 196      # every masked node-CITATION in C's hunts (PLA-161's table figure)
C_HUNTS = (7, 8, 13, 14, 17, 21, 24)


def test_a_clean_zero_is_refused_while_masked_units_exist():
    """The RED case: campaign C's own closing line must not be printable."""
    with pytest.raises(RC.UnreportableCompletion, match='masked-only'):
        RC.assert_completion_reportable(
            'HONEST OPEN after re-scope', C_OPEN_DECISIONS, C_TOTAL_DECISIONS,
            masked_units=C_MASKED_DECISIONS, masked_rows=C_MASKED_ROWS,
            hunts_expected=C_HUNTS, hunts_with_rows=C_HUNTS)


def test_an_unexplained_empty_hunt_is_refused():
    """A hunt that was FIXED and one that was FILTERED AWAY must not render identically."""
    with pytest.raises(RC.UnreportableCompletion, match='#17'):
        RC.assert_completion_reportable(
            'campaign C', 0, 25, hunts_expected=C_HUNTS,
            hunts_with_rows=(7, 8, 13, 14, 21), empty_hunt_reasons={24: 'fixed'})


def test_an_empty_hunt_WITH_a_reason_is_accepted():
    """Naming why a hunt is empty is exactly what makes the completion honest."""
    assert RC.assert_completion_reportable(
        'campaign C', 0, 25, hunts_expected=C_HUNTS,
        hunts_with_rows=(7, 8, 13, 14, 21),
        empty_hunt_reasons={24: 'fixed', 17: 'fully masked'}) is True


def test_EVERY_reason_is_collected_not_just_the_first():
    """Inherited from predicate 1: fixing the masked residue must not then reveal the empty-hunt
    problem as if it were news ([[guard-tests-pass-because-an-earlier-check-fires]])."""
    with pytest.raises(RC.UnreportableCompletion) as exc:
        RC.assert_completion_reportable(
            'campaign C', 0, 25, masked_units=39, masked_rows=196,
            hunts_expected=C_HUNTS, hunts_with_rows=(7, 8, 13, 14, 21))
    message = str(exc.value)
    assert 'masked-only' in message, 'the masked residue must be reported'
    assert '#17' in message and '#24' in message, 'the unexplained hunts must ALSO be reported'


def test_an_empty_denominator_is_undetermined_not_complete():
    """`0 of 0` establishes nothing and must never read as done."""
    with pytest.raises(RC.UnreportableCompletion, match='denominator'):
        RC.assert_completion_reportable('empty scope', 0, 0)


def test_a_genuinely_clean_scope_is_accepted():
    """The predicate must be capable of PASSING, or it is just a thrown exception."""
    assert RC.assert_completion_reportable(
        'campaign C', 0, 25, masked_units=0, masked_rows=0,
        hunts_expected=C_HUNTS, hunts_with_rows=C_HUNTS) is True


def test_completion_line_returns_the_text_only_when_the_contract_holds():
    line = RC.completion_line('HONEST OPEN', 0, 25, hunts_expected=(7,), hunts_with_rows=(7,))
    assert line == 'HONEST OPEN: 0 of 25 decisions'
    with pytest.raises(RC.UnreportableCompletion):
        RC.completion_line('HONEST OPEN', 0, 25, masked_units=39, masked_rows=196,
                           hunts_expected=(7,), hunts_with_rows=(7,))


def test_MUTATION_the_unguarded_line_reproduces_the_original_defect():
    """Kept as the WRONG method, the way `proximity_band_hits` is.

    It prints campaign C's exact closing text with 39 masked decisions in scope and says nothing
    about them. Without this the predicate looks like a preference rather than a fix.
    """
    lying = RC.unguarded_completion_line(
        'HONEST OPEN after re-scope', C_OPEN_DECISIONS, C_TOTAL_DECISIONS)
    assert lying == 'HONEST OPEN after re-scope: 0 of 25 decisions'
    assert 'masked' not in lying, 'the wrong method must stay silent -- that is the defect'
    with pytest.raises(RC.UnreportableCompletion):
        RC.assert_completion_reportable(
            'HONEST OPEN after re-scope', C_OPEN_DECISIONS, C_TOTAL_DECISIONS,
            masked_units=C_MASKED_DECISIONS, masked_rows=C_MASKED_ROWS)


def test_describe_refusal_renders_undetermined_not_a_number():
    try:
        RC.assert_completion_reportable('scope', 0, 25, masked_units=39, masked_rows=196)
    except RC.UnreportableCompletion as exc:
        rendered = RC.describe_refusal(exc)
    assert rendered.startswith('UNDETERMINED')
    assert '39' in rendered and '196' in rendered


def test_predicate_1_is_re_exported_so_callers_import_one_module():
    assert RC.assert_absence_reportable is not None
    assert issubclass(RC.UnreportableAbsence, Exception)


# --- the contract measured against the LIVE hunt footprint ------------------------------------

def test_campaign_C_still_cannot_report_a_clean_completion_today():
    """Re-derive C's residue from `hunt_footprint` and assert the contract still refuses.

    Pinning the numbers alone would go stale silently; this asks the live footprint. Units:
    MASKED-ONLY DECISIONS and masked NODE-citations, both per campaign C's own hunts.
    """
    import json
    import hunt_footprint as HF
    with open(os.path.join(REPO, 'crops_data_final.json'), encoding='utf-8') as fh:
        data = json.load(fh)
    dec = HF.decisions(data)
    masked_dec = masked_rows = 0
    for (slug, reg, sid), d in dec.items():
        entry = HF.FOOTPRINT.get((reg, sid))
        if not entry or entry[1] != 'C':
            continue
        if d['sole'] == 0 and d['masked']:
            masked_dec += 1
            masked_rows += d['masked']
    assert masked_dec > 0, 'campaign C has no masked residue -- the RED case is gone, re-derive'
    assert (masked_dec, masked_rows) == (C_MASKED_DECISIONS, C_MASKED_ROWS), (
        f'C residue moved to {masked_dec} DECISIONS / {masked_rows} rows -- read why before '
        f're-pinning; the contract is only as honest as this number')
    with pytest.raises(RC.UnreportableCompletion, match='masked-only'):
        RC.assert_completion_reportable(
            'HONEST OPEN after re-scope', 0, 25,
            masked_units=masked_dec, masked_rows=masked_rows)


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))


# --- adoption: the contract must actually be WIRED, not merely importable --------------------
#
# PLA-161 ruling: adopt in B, D and bare_host_scan as well as C. Neither B nor D was thought to
# print a `0 of N` line; campaign B in fact prints
#     HONEST OPEN, document work :  0 of 33 decisions,   0 of 97 nodes
# so the defect was live in two tools, not one. Adopting only where it is currently visible
# leaves the next `0 of N` someone adds unguarded, which is the treadmill this arc keeps finding.

import subprocess  # noqa: E402

TOOLS = os.path.join(REPO, 'tools')


def _run(script):
    return subprocess.run([sys.executable, os.path.join(TOOLS, script)],
                          capture_output=True, text=True, timeout=300).stdout


def test_campaign_C_prints_a_refusal_not_a_zero():
    out = _run('campaign_c_reprice.py')
    assert 'COMPLETION REFUSED' in out
    assert 'masked-only decisions' in out
    assert 'HONEST OPEN after re-scope :  0 of 25' not in out, 'the unguarded line is back'


def test_campaign_B_prints_a_refusal_not_a_zero():
    out = _run('campaign_b_reprice.py')
    assert 'COMPLETION REFUSED' in out
    assert 'HONEST OPEN, document work :  0 of 33' not in out, 'the unguarded line is back'


def test_campaign_D_refuses_and_names_its_unexplained_hunts():
    """D's completion claim is over HUNTS while its residue is DECISIONS -- both must be labelled."""
    out = _run('campaign_d_reprice.py')
    assert 'COMPLETION REFUSED' in out
    assert 'masked-only decisions' in out, 'the residue unit must say DECISIONS'
    assert 'of 12 hunts" line' in out, "the completion unit must say HUNTS"
    for hunt in ('#25', '#26', '#27', '#28', '#29'):
        assert hunt in out, f'hunt {hunt} produced no rows and must be named'


def test_bare_host_scan_states_the_population_it_creates():
    """The SOLE/corroborated split is where the masked population is made; it must say so."""
    out = _run('bare_host_scan.py')
    assert 'MASKED-ONLY DECISIONS' in out
    assert 'The SOLE column is not the worklist' in out


def test_the_residue_is_derived_live_not_pinned_into_the_tools():
    """A constant would put the contract back to sleep the moment the residue moved."""
    for script in ('campaign_b_reprice.py', 'campaign_c_reprice.py', 'campaign_d_reprice.py'):
        src = open(os.path.join(TOOLS, script), encoding='utf-8').read()
        assert 'hunt_footprint.decisions(' in src, f'{script} must re-derive its residue'
