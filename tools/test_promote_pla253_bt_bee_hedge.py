#!/usr/bin/env python3
"""Guard suite for promote_pla253_bt_bee_hedge.py (base 5f2d9555).

PLA-253, second pass on the SAME leaf. The first pass removed the blanket "harmless to
people, pets, and bees" and its own close-out flagged what it had left behind: "bees are
not at risk" is still absolute-SHAPED, where NPIC's register for the active ingredient is
"low in toxicity to bees". This promote replaces exactly that clause and nothing else.

THE FIXTURE IS REBUILT BY REPLAY. 5f2d9555 was never a commit -- PLA-253 ran two promotes
on one leaf before committing -- so promote_fixture rebuilds it from 394bb8bd by replaying
`promote_pla253_bt_safety.py`, hash-verified. It is registered in CHAIN, not COMMIT_FOR.

WHAT MAKES THIS SUITE DIFFERENT FROM THE FIRST PASS'S. A second pass on prose that was just
rewritten has two failure modes the first pass did not:

  1. IT CAN SILENTLY UNDO THE FIRST PASS. `test_pass_one_gains_all_survive` re-asserts every
     property the first promote established -- no "harmless" anywhere in the entry, the
     eye-and-skin precaution present, the non-target caterpillar limit present. A hedge that
     fixes the bee clause by reverting the field is not a fix.
  2. IT CAN EDIT MORE THAN THE CLAUSE. `test_the_change_is_exactly_one_clause` asserts the
     new value is the old value with ONE substring substituted and every other byte
     identical, so a "small wording fix" cannot quietly reflow the rest of the paragraph.

Mutation harness: tools/mutate_pla253_bee_hedge_suite.py (PLA-215, liveness-defended).
"""
import hashlib
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

BASE_SHA = '5f2d95559256df1553dd2ac0ba19cfa275ec497ab9ba0264ca28dbd94290af0e'
PASS_ONE_SHA = '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660'
SCRIPT = os.path.join(HERE, 'promote_pla253_bt_bee_hedge.py')
FIELD_PATH = 'control_methods.bt.how_it_works_beginner'

CLAUSE_OLD = 'so bees are not at risk'
CLAUSE_NEW = 'so the risk to bees is low'

# Hand-typed, not imported from the promote script.
PREV = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
        "the Bt proteins wreck its gut, and it stops feeding and dies. It only affects "
        "caterpillars, so bees are not at risk, and people and pets cannot activate the "
        "proteins at all, which is why a treated vegetable is safe to eat. Two things to "
        "watch. The spray itself can irritate eyes and skin, so wear gloves and keep it "
        "away from your face. And it does not tell good caterpillars from bad, so spray "
        "only the plants that have a pest problem.")
NEW = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
       "the Bt proteins wreck its gut, and it stops feeding and dies. It only affects "
       "caterpillars, so the risk to bees is low, and people and pets cannot activate the "
       "proteins at all, which is why a treated vegetable is safe to eat. Two things to "
       "watch. The spray itself can irritate eyes and skin, so wear gloves and keep it "
       "away from your face. And it does not tell good caterpillars from bad, so spray "
       "only the plants that have a pest problem.")

NPIC_URL = 'https://npic.orst.edu/factsheets/btgen.html'
CACHE = os.path.join(HERE, '.doc_cache')

_post = {}


def post_bytes():
    if 'raw' not in _post:
        path, sha = promote_fixture.scratch(BASE_SHA)
        assert sha == BASE_SHA
        r = subprocess.run([sys.executable, SCRIPT, '--canonical', path,
                            f'--expect-sha={BASE_SHA}', '--apply'],
                           capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-800:]}'
        _post['raw'] = open(path, 'rb').read()
    return _post['raw']


def pre_data():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


def post_data():
    return json.loads(post_bytes())


def leaves(obj):
    out = {}

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, f'{p}.{k}' if p else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f'{p}[{i}]')
        else:
            out[p] = o

    walk(obj, '')
    return out


def get(d):
    return d['control_methods']['bt']['how_it_works_beginner']


# ------------------------------------------------- the fixture is the state we think it is
def test_base_is_the_first_passs_output_rebuilt_by_replay():
    """5f2d9555 is not a commit. If CHAIN ever stops producing it, this suite must FAIL
    here rather than quietly test some other state."""
    raw = promote_fixture.pre_state(BASE_SHA)
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    assert get(json.loads(raw)) == PREV


def test_pre_state_carries_the_clause_being_hedged():
    assert CLAUSE_OLD in get(pre_data())
    assert CLAUSE_NEW not in get(pre_data())


# ------------------------------------------- key sets BEFORE value comparison (PLA-215 #4)
def test_key_sets_are_identical_before_any_value_comparison():
    pre_k, post_k = set(leaves(pre_data())), set(leaves(post_data()))
    assert not pre_k - post_k, f'{len(pre_k - post_k)} leaves DROPPED'
    assert not post_k - pre_k, f'{len(post_k - pre_k)} leaves ADDED'


def test_exactly_one_leaf_changed_and_it_is_the_named_field():
    pre_l, post_l = leaves(pre_data()), leaves(post_data())
    assert set(pre_l) == set(post_l)
    changed = {k for k in pre_l if pre_l[k] != post_l[k]}
    assert changed == {FIELD_PATH}, f'blast radius is {sorted(changed)}'


def test_no_other_crop_or_top_level_key_moved():
    pre_d, post_d = pre_data(), post_data()
    assert pre_d['crops'] == post_d['crops']
    for k in pre_d:
        if k != 'control_methods':
            assert pre_d[k] == post_d[k], f'top-level key {k} moved'
    for k, v in pre_d['control_methods'].items():
        if k != 'bt':
            assert post_d['control_methods'][k] == v, f'control method {k} moved'


# ------------------------------------------------------------------- the hedge itself
def test_new_text_is_exactly_the_authored_delivery():
    assert get(post_data()) == NEW


def test_the_change_is_exactly_one_clause_and_every_other_byte_is_identical():
    """A wording fix must not reflow the paragraph around it. The post value must be the
    pre value with ONE substring substituted -- proven by reconstructing it, and by
    checking the two strings agree on every character outside that one span."""
    before, after = get(pre_data()), get(post_data())
    assert before.replace(CLAUSE_OLD, CLAUSE_NEW) == after
    assert before.count(CLAUSE_OLD) == 1, 'the clause is not unique; a blind replace is unsafe'
    head = before.index(CLAUSE_OLD)
    assert before[:head] == after[:head], 'text BEFORE the clause moved'
    assert before[head + len(CLAUSE_OLD):] == after[head + len(CLAUSE_NEW):], \
        'text AFTER the clause moved'


def test_the_absolute_is_gone_and_the_hedge_is_present():
    entry = post_data()['control_methods']['bt']
    blob = json.dumps(entry, ensure_ascii=False).lower()
    assert 'not at risk' not in blob
    assert CLAUSE_NEW in get(post_data())


def test_the_hedge_matches_npics_register_for_the_active_ingredient():
    """The whole point of the second pass: our beginner wording should be the document's
    own strength of claim, in plain words. NPIC says kurstaki is LOW IN TOXICITY to bees;
    'the risk to bees is low' carries that, 'bees are not at risk' overstated it."""
    p = os.path.join(CACHE, hashlib.sha1(NPIC_URL.encode()).hexdigest() + '.txt')
    if not os.path.exists(p):
        pytest.skip('NPIC factsheet not in the shared cache')
    doc = ' '.join(open(p, encoding='utf-8', errors='replace').read().split()).lower()
    assert 'kurstaki are low in toxicity to bees' in doc
    # the document never makes the absolute claim we removed
    assert 'no risk to bees' not in doc
    assert 'harmless to bees' not in doc
    new = get(post_data()).lower()
    assert 'risk to bees is low' in new
    assert 'bees are not at risk' not in new


# --------------------------------------------- the first pass must not be undone (regression)
def test_pass_one_gains_all_survive():
    """Every property the first promote established, re-asserted. A hedge that fixes the
    bee clause by reverting the field is not a fix."""
    entry = post_data()['control_methods']['bt']
    blob = json.dumps(entry, ensure_ascii=False).lower()
    new = get(post_data()).lower()
    assert 'harmless' not in blob, 'pass one removed this absolute; it is back'
    assert 'practically nontoxic' in blob, 'the correct seasoned hedge was lost'
    assert 'irritate eyes and skin' in new and 'gloves' in new, 'the precaution was lost'
    assert 'good caterpillars' in new and 'spray only the plants' in new, \
        'the non-target caterpillar limit was lost'
    assert 'butterflies' in ' '.join(entry['cautions']).lower()


def test_register_is_not_collapsed():
    post = post_data()
    beginner = post['control_methods']['bt']['how_it_works_beginner']
    seasoned = post['control_methods']['bt']['how_it_works_seasoned']
    assert beginner != seasoned
    assert seasoned == pre_data()['control_methods']['bt']['how_it_works_seasoned']
    assert 'kurstaki' not in beginner.lower()
    # the hedge must be plain-language, not the technical category term lifted across
    assert 'practically nontoxic' not in beginner.lower()


def test_new_copy_meets_house_style():
    new = get(post_data())
    assert '—' not in new and '–' not in new and '--' not in new


# ------------------------------------------------------ REFUSAL-SPEC (PLA-215 item 5)
def test_refusal_spec_promote_refuses_a_wrong_base_sha():
    path, sha = promote_fixture.scratch(
        BASE_SHA, mutate=lambda crops, data: data.__setitem__('_sabotage', 'x'))
    assert sha != BASE_SHA
    r = subprocess.run([sys.executable, SCRIPT, '--canonical', path, '--apply'],
                       capture_output=True, text=True)
    assert r.returncode != 0
    assert 'base SHA mismatch' in (r.stdout + r.stderr)


def test_refusal_spec_promote_refuses_when_already_hedged():
    path, sha = promote_fixture.scratch(
        BASE_SHA,
        mutate=lambda crops, data: data['control_methods']['bt'].__setitem__(
            'how_it_works_beginner', NEW))
    assert sha != BASE_SHA
    r = subprocess.run([sys.executable, SCRIPT, '--canonical', path,
                        f'--expect-sha={sha}', '--apply'], capture_output=True, text=True)
    assert r.returncode != 0
    assert 'already' in (r.stdout + r.stderr).lower()


def test_refusal_spec_promote_refuses_text_it_was_not_written_against():
    """Specifically including the PASS-ONE-BASE text: running this second pass against
    394bb8bd must refuse, not half-apply a hedge to a sentence that still says
    'harmless'."""
    path, sha = promote_fixture.scratch(
        BASE_SHA,
        mutate=lambda crops, data: data['control_methods']['bt'].__setitem__(
            'how_it_works_beginner',
            'Bt is a natural soil bacterium. It is harmless to people, pets, and bees.'))
    r = subprocess.run([sys.executable, SCRIPT, '--canonical', path,
                        f'--expect-sha={sha}', '--apply'], capture_output=True, text=True)
    assert r.returncode != 0
    assert 're-read before replacing' in (r.stdout + r.stderr)


# ------------------------------------------------------------------------- mechanics
def test_compact_formatting_preserved():
    raw = post_bytes()
    assert not raw.endswith(b'\n')
    assert b'\n' not in raw
    assert b'": "' not in raw
