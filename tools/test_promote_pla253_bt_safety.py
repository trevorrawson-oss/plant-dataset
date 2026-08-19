#!/usr/bin/env python3
"""Guard suite for promote_pla253_bt_safety.py (base 394bb8bd).

Fixture-pinned per tools/promote_fixture.py: the pre-state is rebuilt by hash and the post
state by REPLAYING the promote on that fixture, so this suite never reads live canonical
and cannot go vacuous when canonical moves on.

**Born under the PLA-215 convention** (docs/promote_suite_mutation_convention.md), which
this promote is the first to ship under:

  item 1  one mutation per guard family, verified RED -- tools/mutate_pla253_suite.py
  item 2  liveness defense -- that harness carries a MUTATION-APPLIED marker and a
          sentinel that must redden, else it exits HARNESS DEAD
  item 3  positive control -- an injection chosen to be plausibly invisible
  item 4  `assert set(pre) == set(post)` BEFORE any value comparison, below
  item 5  REFUSAL-SPEC: the two refusal guards stay GREEN when the promote refuses; that
          is the contract being tested, not a vacuous pass

WHAT THIS PROMOTE IS. One leaf: `control_methods.bt.how_it_works_beginner`. The old line
told a first-season grower that a pesticide is "harmless to people, pets, and bees" while
its own seasoned sibling said "practically nontoxic" -- an absolute safety claim in the
register shown to the audience least equipped to add its own caution. The replacement is
verified against NPIC's Bt factsheet (npic.orst.edu/factsheets/btgen.html, Reviewed: May
2022), which is already this entry's own anchor, not against the seasoned sibling.

TWO DEFECTS, and each has its own guard, because fixing one and calling it done is the
failure mode here:
  (a) the absolute "harmless";
  (b) a true statement creating a false impression -- the old line named the one pollinator
      NOT at risk (bees) while staying silent on butterflies, which this entry's OWN
      `cautions` field says Bt kills as a group.

The suite deliberately does NOT accept the seasoned string being copied into the beginner
field: PLA-253 names that as its own defect (register collapse), so
`test_register_is_not_collapsed` fails on it.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402

BASE_SHA = '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660'
SCRIPT = os.path.join(HERE, 'promote_pla253_bt_safety.py')
FIELD = ('control_methods', 'bt', 'how_it_works_beginner')
FIELD_PATH = 'control_methods.bt.how_it_works_beginner'

# Hand-typed from the issue and the authored delivery, NOT imported from the promote
# script. An expectation computed from the thing it validates is vacuous by construction.
OLD = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
       "the Bt proteins wreck its gut and it stops feeding and dies. It is harmless to "
       "people, pets, and bees.")
NEW = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
       "the Bt proteins wreck its gut, and it stops feeding and dies. It only affects "
       "caterpillars, so bees are not at risk, and people and pets cannot activate the "
       "proteins at all, which is why a treated vegetable is safe to eat. Two things to "
       "watch. The spray itself can irritate eyes and skin, so wear gloves and keep it "
       "away from your face. And it does not tell good caterpillars from bad, so spray "
       "only the plants that have a pest problem.")

NPIC_URL = 'https://npic.orst.edu/factsheets/btgen.html'
CACHE = os.path.join(HERE, '.doc_cache')


# ------------------------------------------------------------------ fixtures
_post = {}


def post_bytes():
    if 'raw' not in _post:
        path, sha = promote_fixture.scratch(BASE_SHA)
        assert sha == BASE_SHA
        r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
        assert r.returncode == 0, f'replay failed: {(r.stdout + r.stderr)[-800:]}'
        _post['raw'] = open(path, 'rb').read()
    return _post['raw']


def pre_data():
    return json.loads(promote_fixture.pre_state(BASE_SHA))


def post_data():
    return json.loads(post_bytes())


def leaves(obj, path=''):
    """Every scalar leaf as (path, value). The unit both blast-radius guards work in."""
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

    walk(obj, path)
    return out


def get(data):
    return data[FIELD[0]][FIELD[1]][FIELD[2]]


# ------------------------------------------------- 0. the promote is aimed at something
def test_pre_state_carries_the_defect():
    """If the base no longer holds the bad sentence, this promote is aimed at nothing and
    every guard below would pass vacuously."""
    assert get(pre_data()) == OLD
    assert 'harmless' in get(pre_data())


# ------------------------------------------- item 4: key sets BEFORE value comparison
def test_key_sets_are_identical_before_any_value_comparison():
    """Iterating only the pre state makes everything ADDED in post invisible. Assert the
    key sets match in BOTH directions first; only then is a value diff meaningful."""
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
    assert pre_d['crops'] == post_d['crops'], 'a crop moved; this promote is top-level only'
    for k in pre_d:
        if k != 'control_methods':
            assert pre_d[k] == post_d[k], f'top-level key {k} moved'
    for k, v in pre_d['control_methods'].items():
        if k != 'bt':
            assert post_d['control_methods'][k] == v, f'control method {k} moved'


# ------------------------------------------------------------- the replacement itself
def test_new_text_is_exactly_the_authored_delivery():
    assert get(post_data()) == NEW


def test_defect_a_the_absolute_claim_is_gone_from_the_whole_entry():
    """Not just from the one field: an absolute that survives in `pros` or `cautions` is
    the same claim reaching the same reader by another route."""
    entry = post_data()['control_methods']['bt']
    blob = json.dumps(entry, ensure_ascii=False).lower()
    assert 'harmless' not in blob
    # the hedged, registered-category wording must SURVIVE where it was already correct
    assert 'practically nontoxic' in blob


def test_defect_b_the_butterfly_silence_is_broken():
    """The old line named bees (not at risk) and said nothing about butterflies, which this
    entry's own `cautions` says Bt kills as a group. A reader of the beginner register alone
    must now meet the non-target caterpillar limit."""
    new = get(post_data()).lower()
    assert 'caterpillars from bad' in new or 'good caterpillars' in new
    assert 'spray only the plants' in new
    cautions = ' '.join(post_data()['control_methods']['bt']['cautions']).lower()
    assert 'butterflies' in cautions, 'the caution this field must stop contradicting is gone'


def test_the_handling_precaution_the_old_line_omitted_is_present():
    new = get(post_data()).lower()
    assert 'irritate eyes and skin' in new
    assert 'gloves' in new


def test_register_is_not_collapsed():
    """PLA-253's explicit instruction: do NOT resolve this by copying the seasoned string
    into the beginner field. That produces the cosmetic-pair defect instead of fixing it."""
    post = post_data()
    beginner = post['control_methods']['bt']['how_it_works_beginner']
    seasoned = post['control_methods']['bt']['how_it_works_seasoned']
    assert beginner != seasoned
    assert seasoned == pre_data()['control_methods']['bt']['how_it_works_seasoned'], \
        'the seasoned sibling was correct and must not move'
    # beginner register stays plain: no strain binomial, no LD50-style vocabulary
    assert 'kurstaki' not in beginner.lower()
    assert 'crystal proteins' not in beginner.lower()


def test_new_copy_meets_house_style():
    new = get(post_data())
    assert '—' not in new, 'em dash in consumer copy'
    assert '–' not in new, 'en dash in consumer copy'
    assert '--' not in new, 'double hyphen in consumer copy'


# --------------------------------------------------- source truth, against the anchor
def _npic_text():
    p = os.path.join(CACHE, hashlib.sha1(NPIC_URL.encode()).hexdigest() + '.txt')
    if not os.path.exists(p):
        pytest.skip('NPIC factsheet not in the shared cache; run the fetch layer first')
    return ' '.join(open(p, encoding='utf-8', errors='replace').read().split())


def test_claims_are_supported_by_the_entrys_own_anchor():
    """PLA-253 item 2: verify against a T1 source, not against the seasoned sibling.
    Each assertion below is a sentence in the replacement, checked against NPIC's text."""
    doc = _npic_text().lower()
    # the mechanism: activation is gut-chemistry specific, and does not happen in people
    assert 'in order to activate the toxin' in doc
    assert 'not activated when the spores are eaten by people' in doc
    assert 'do not have the specific enzymes' in doc
    # the food-safety conclusion
    assert 'risk is not expected' in doc
    # the precaution the old line omitted
    assert 'eye and skin irritation' in doc
    # this entry's strain, and what it kills
    assert 'kurstaki controls caterpillars of moths and butterflies' in doc
    # the bee conclusion, for THIS strain
    assert 'kurstaki are low in toxicity to bees' in doc


def test_the_anchor_is_still_this_entrys_own_source():
    """The verification is only meaningful if the document is cited by the entry it
    verifies. A source-truth check against a document the entry does not anchor is a
    different document's truth."""
    entry = post_data()['control_methods']['bt']
    assert entry['anchoring_urls']['npic_orst']['url'] == NPIC_URL
    assert 'npic_orst' in entry['sources']


# ------------------------------------------------------ REFUSAL-SPEC (PLA-215 item 5)
# These stay GREEN by refusing. Green IS the contract here; it is not a vacuous pass.
def test_refusal_spec_promote_refuses_a_wrong_base_sha():
    path, sha = promote_fixture.scratch(
        BASE_SHA, mutate=lambda crops, data: data.__setitem__('_sabotage', 'x'))
    assert sha != BASE_SHA
    r = subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
    assert r.returncode != 0, 'promote ran against a base it was not pinned to'
    assert 'base SHA mismatch' in (r.stdout + r.stderr)


def test_refusal_spec_promote_refuses_when_the_defect_is_already_gone():
    """Re-running a completed promote must refuse, not silently no-op or double-apply.

    Reaching this branch needs --expect-sha. Measured, not assumed: any state carrying the
    replacement hashes to something other than BASE_SHA, so the SHA guard fires first and
    this refusal is unreachable on the default path. Its one live path is a deliberate
    re-pin, so the test drives it that way instead of pretending the branch is reachable
    without one -- a guard tested only through a path it can never take in production is
    the reachability failure this repo has already paid for once.
    """
    path, sha = promote_fixture.scratch(
        BASE_SHA,
        mutate=lambda crops, data: data['control_methods']['bt'].__setitem__(
            'how_it_works_beginner', NEW))
    assert sha != BASE_SHA, 'the replacement did not change the state; this test is vacuous'
    r = subprocess.run([sys.executable, SCRIPT, path, f'--expect-sha={sha}'],
                       capture_output=True, text=True)
    assert r.returncode != 0, 'promote re-applied itself'
    assert 'already' in (r.stdout + r.stderr).lower()


def test_refusal_spec_promote_refuses_text_it_was_not_written_against():
    """If the prose moved under the promote, replacing it blind would destroy an edit
    nobody looked at. Refusing is the contract."""
    path, sha = promote_fixture.scratch(
        BASE_SHA,
        mutate=lambda crops, data: data['control_methods']['bt'].__setitem__(
            'how_it_works_beginner', 'Someone else rewrote this line in the meantime.'))
    r = subprocess.run([sys.executable, SCRIPT, path, f'--expect-sha={sha}'],
                       capture_output=True, text=True)
    assert r.returncode != 0
    assert 're-read before replacing' in (r.stdout + r.stderr)


# ------------------------------------------------------------------------- mechanics
def test_compact_formatting_preserved():
    raw = post_bytes()
    assert not raw.endswith(b'\n'), 'canonical must have no trailing newline'
    assert b'\n' not in raw, 'canonical must be single-line compact'
    assert b'": "' not in raw, 'canonical must use separators=(",",":")'


def test_post_state_is_valid_json_and_unicode_preserved():
    d = post_data()
    assert d['control_methods']['bt']['cons'][1].count('°F') == 0
    assert '°F' in json.dumps(d, ensure_ascii=False)
