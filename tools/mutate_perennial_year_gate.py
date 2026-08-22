#!/usr/bin/env python3
"""Mutation harness for tools/perennial_year_gate.py -- the PLA-215 bar, liveness-defended.

WHY THIS IS THE ONLY NON-VACUITY EVIDENCE FOR TWO OF THE THREE FAMILIES.

ESTAB-CAPTION and YEAR-DUP are both GREEN on live canonical, and YEAR-DUP was green from birth
(0 hits in 5,484 same-field cross-stage comparisons). A guard that refuses an input and stays
green is a REFUSAL-SPEC pass, not a vacuity -- but "green" and "not wired up" are the same
observation from outside. The only way to tell them apart is to inject the defect class each
guard claims to catch and watch it redden. PILL-CAPTION is RED on live data and therefore has
its own evidence, but it is mutated here too so a future scope change cannot silently narrow it.

THE LIVENESS DEFENCE (PLA-138's harness dedented an already-indented template, silently ran the
CLEAN fixture, and reported every mutation as surviving):

  1. MUTATION-APPLIED MARKER. Every mutation is read BACK off the scratch file after writing and
     asserted to differ from the original value. A mutation that did not land is a harness fault,
     never a survivor.
  2. SENTINEL. One mutation targets a crop that is CLEAN on live data in every family and not
     yet migrated to the year-pill trio. If the harness were running the clean fixture, no
     finding for that crop could appear. The sentinel not reddening exits HARNESS DEAD
     regardless of what the other mutations reported -- which it did, on the first run after the
     Round 2 pilot authored apple and suppressed apple's PILL-CAPTION. THE SENTINEL CROP IS
     THEREFORE ROLLOUT-SENSITIVE and must be re-chosen as waves land; the harness says so loudly
     rather than degrading quietly.
  3. POSITIVE CONTROL. The unmutated scratch copy is gated first and must reproduce the exact
     4-finding baseline. If a mutation's expected finding is already in the baseline, the
     injection would be invisible and is reported as UNMEASURABLE rather than as caught.
  4. NEGATIVE CONTROL (scope). The same defect injected into a crop that renders no pills must
     NOT be caught. A guard that fires there has lost the scope that keeps it at 4 findings.

No two-state guard here, so the `assert set(pre) == set(post)` rule does not apply -- this gate
reads one state and writes nothing. The scratch copy is written under the session scratchpad and
the canonical is opened read-only; CLAUDE.md's READ-ONLY rule on crops_data_final.json holds.

Run: python3 tools/mutate_perennial_year_gate.py
Exit 0 only when every mutation is CAUGHT by its own target family and every control holds.
"""
import copy
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from perennial_year_gate import (  # noqa: E402
    estab_caption_violations, pill_caption_violations, renders_pills, violations,
    year_dup_violations,
)

CANONICAL = os.path.join(os.path.dirname(HERE), "crops_data_final.json")

SENTINEL_SLUG = None   # resolved in main() by _sentinel_slug()

# THE BASELINE MOVES AS THE ROLLOUT LANDS, and that is the point rather than a nuisance.
# Measured fe26f783: 4 findings (artichoke x2, mandarin-clementine, orange-navel). PLA-6 Round 2
# wave 2 authored `full_harvest_notes_*` for the citrus, which SUPPRESSES the family for those
# registers -- the app prefers that field and never shears it, so the harvest_ready lead sentence
# is no longer rendered and reporting it would name a defect nobody can see. Down to 2 at
# 4ec3ce8c. artichoke is wave 4 and will take it to 0, at which point the gate can arm as an
# A-number. If this drifts unexpectedly the assertion says so loudly rather than letting every
# mutation quietly re-baseline against new data.
# THE ROLLOUT CLOSED THIS OUT. 4 findings at fe26f783, 2 after wave 2 suppressed the citrus,
# 0 at 20a32c47 once wave 4 authored artichoke. The family then armed as whole_crop_gate A55.
# An empty baseline is the strongest possible positive control: any finding at all is a
# regression, and the mutations below restore the pre-arc condition to prove the guard still
# fires rather than having quietly stopped reaching anything.
BASELINE = []

FAMILY = {
    "PILL-CAPTION": pill_caption_violations,
    "ESTAB-CAPTION": estab_caption_violations,
    "YEAR-DUP": year_dup_violations,
}


def by_slug(data, slug):
    for c in data["crops"]:
        if c.get("slug") == slug:
            return c
    raise KeyError(f"{slug} not in roster -- harness cannot run")


def baseline_ids(data):
    out = []
    for c in data["crops"]:
        if c.get("perennial") is not True:
            continue
        for v in pill_caption_violations(c):
            out.append(f"{c['slug']}:{v.split(':')[1].strip()}")
    return sorted(out)


# --------------------------------------------------------------------------- the mutations
# Each returns (description, mutator, target_slug, target_family). The mutator edits IN PLACE.

def _sentinel_slug(clean):
    """Pick a sentinel crop FROM THE DATA rather than naming one.

    THIS FUNCTION HAS BEEN RIGHT TWICE AND THEN OBSOLETE ONCE, and both are worth recording.
    It first exited HARNESS DEAD when the Round 2 pilot authored apple, then again when wave 1
    authored plum: PILL-CAPTION is suppressed for any register carrying `full_harvest_notes_*`,
    so an authored crop can no longer redden. Deriving the crop instead of naming it fixed that.

    Then the rollout finished and derivation ran out of candidates too, because EVERY
    pill-rendering perennial is now authored. That was the correct signal -- the family reached
    zero and armed as whole_crop_gate A55 -- but it left this harness unable to sentinel at all.

    So the injection now RESTORES the pre-arc condition rather than hunting for a survivor of it:
    the mutator strips `full_harvest_notes_*` from the chosen crop, which un-suppresses the family
    exactly as it stood before this arc, and then shortens the caption. Any pill-rendering crop
    serves, since all are clean, so this picks the first deterministically.
    """
    for c in clean["crops"]:
        if c.get("perennial") is True and renders_pills(c):
            return c["slug"]
    raise AssertionError("no pill-rendering perennial in the roster at all")


def m_pill_short_lead(data):
    """PILL-CAPTION: the pre-arc condition, restored and then broken.

    Strips `full_harvest_notes_*` so the family is no longer suppressed -- which is precisely the
    state every perennial was in before PLA-6 Round 2 -- and gives harvest_ready a bare topic
    sentence. THE SENTINEL: trivially checkable, so a failure to redden means the harness is not
    gating the mutated fixture at all."""
    c = by_slug(data, SENTINEL_SLUG)
    c.pop("full_harvest_notes_beginner", None)
    c.pop("full_harvest_notes_seasoned", None)
    c["harvest_ready_beginner"] = "Pick them. " + c["harvest_ready_beginner"]
    return c["harvest_ready_beginner"]



def m_pill_unterminated(data):
    """PILL-CAPTION: no sentence terminator at all -- first_sentence returns the whole string,
    so a SHORT unterminated field must still flag (the app renders the same short string).

    Also DERIVED rather than named. This mutation was pinned to peach and survived the moment
    wave 1 authored peach's full_harvest_notes, which suppresses the family for that register --
    the same staleness that hit the sentinel twice. It targets the seasoned register while the
    sentinel targets beginner, so one unmigrated crop serves both without collision."""
    c = by_slug(data, SENTINEL_SLUG)
    c.pop("full_harvest_notes_beginner", None)
    c.pop("full_harvest_notes_seasoned", None)
    c["harvest_ready_seasoned"] = "Pick when ripe"
    return c["harvest_ready_seasoned"]


def m_estab_drop_seasoned(data):
    """ESTAB-CAPTION: the string captioning two pills loses its seasoned register."""
    c = by_slug(data, "apple")
    del c["tips_by_stage"]["establishment"][0]["text_seasoned"]
    return c["tips_by_stage"]["establishment"][0]


def m_estab_empty_list(data):
    """ESTAB-CAPTION: the establishment stage exists but carries no tip."""
    c = by_slug(data, "blueberry")
    c["tips_by_stage"]["establishment"] = []
    return c["tips_by_stage"]["establishment"]


def m_dup_exact(data):
    """YEAR-DUP: two stages of one crop carry byte-identical guidance."""
    c = by_slug(data, "apple")
    c["growth_stages"][2]["user_action_beginner"] = c["growth_stages"][1]["user_action_beginner"]
    return c["growth_stages"][2]["user_action_beginner"]


def m_dup_near(data):
    """YEAR-DUP: a near-duplicate above DUP_RATIO but not byte-identical."""
    c = by_slug(data, "peach")
    src = c["growth_stages"][1]["what_to_look_for_seasoned"]
    c["growth_stages"][3]["what_to_look_for_seasoned"] = src.replace(".", ",", 1) + " Watch it."
    return c["growth_stages"][3]["what_to_look_for_seasoned"]


MUTATIONS = [
    ("PILL-CAPTION", None, m_pill_short_lead, True),   # slug filled in at run time
    ("PILL-CAPTION", None, m_pill_unterminated, False),   # slug filled in at run time
    ("ESTAB-CAPTION", "apple", m_estab_drop_seasoned, False),
    ("ESTAB-CAPTION", "blueberry", m_estab_empty_list, False),
    ("YEAR-DUP", "apple", m_dup_exact, False),
    ("YEAR-DUP", "peach", m_dup_near, False),
]

# NEGATIVE CONTROL: the same PILL-CAPTION defect on a crop that renders no pills (sage carries no
# years_to_first_harvest) must NOT be caught. This is the scope that keeps the gate at 4.
def m_scope_control(data):
    c = by_slug(data, "sage")
    c["harvest_ready_beginner"] = "Snip it. " + c["harvest_ready_beginner"]
    return c["harvest_ready_beginner"]


def main():
    if not os.path.exists(CANONICAL):
        print("HARNESS DEAD: canonical not found")
        return 2
    clean = json.load(open(CANONICAL, encoding="utf-8"))
    global SENTINEL_SLUG
    SENTINEL_SLUG = _sentinel_slug(clean)
    print(f"SENTINEL  derived from the data: {SENTINEL_SLUG} "
          f"(clean, renders pills, not yet migrated)")

    scratch = os.environ.get("CLAUDE_SCRATCH") or tempfile.mkdtemp(prefix="pyg-mut-")
    os.makedirs(scratch, exist_ok=True)

    # ---- (3) POSITIVE CONTROL: the clean fixture reproduces the measured baseline.
    base = baseline_ids(clean)
    print(f"POSITIVE CONTROL  baseline PILL-CAPTION ids: {len(base)}")
    if base != BASELINE:
        print(f"HARNESS DEAD: baseline drifted.\n  expected {BASELINE}\n  got      {base}")
        return 2
    clean_total = sum(len(violations(c)) for c in clean["crops"] if c.get("perennial") is True)
    print(f"POSITIVE CONTROL  clean total findings: {clean_total}  (expected {len(BASELINE)})")
    if clean_total != len(BASELINE):
        print("HARNESS DEAD: clean fixture is not the state the mutations were written against")
        return 2

    results = []
    sentinel_reddened = False

    for family, slug, mutator, is_sentinel in MUTATIONS:
        slug = slug or SENTINEL_SLUG
        data = copy.deepcopy(clean)
        before = json.dumps(by_slug(data, slug), sort_keys=True)
        applied = mutator(data)

        # ---- (1) MUTATION-APPLIED MARKER: write, read back, prove it landed and CHANGED.
        path = os.path.join(scratch, f"mut_{family}_{slug}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
        reread = json.load(open(path, encoding="utf-8"))
        after = json.dumps(by_slug(reread, slug), sort_keys=True)
        if before == after:
            print(f"HARNESS DEAD: mutation {family}/{slug} did not land on disk "
                  f"(scratch copy identical to clean)")
            return 2

        crop = by_slug(reread, slug)
        found = FAMILY[family](crop)
        clean_found = FAMILY[family](by_slug(clean, slug))

        # ---- (3b) invisible-injection check: was this crop already flagged by this family?
        if clean_found and len(found) <= len(clean_found):
            verdict = "UNMEASURABLE"
        elif found and len(found) > len(clean_found):
            verdict = "CAUGHT"
            if is_sentinel:
                sentinel_reddened = True
        else:
            verdict = "SURVIVED"

        results.append((family, slug, verdict, mutator.__doc__.split("\n")[0]))
        marker = " [SENTINEL]" if is_sentinel else ""
        print(f"  {verdict:12s} {family:14s} {slug:20s}{marker} "
              f"clean={len(clean_found)} mutated={len(found)}")
        if verdict == "CAUGHT" and found:
            print(f"               -> {found[-1][:130]}")

    # ---- (4) NEGATIVE CONTROL (scope)
    data = copy.deepcopy(clean)
    m_scope_control(data)
    path = os.path.join(scratch, "mut_SCOPE_sage.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
    reread = json.load(open(path, encoding="utf-8"))
    sage = by_slug(reread, "sage")
    scope_ok = pill_caption_violations(sage) == []
    if sage["harvest_ready_beginner"] == by_slug(clean, "sage")["harvest_ready_beginner"]:
        print("HARNESS DEAD: negative control did not land")
        return 2
    print(f"  {'HELD' if scope_ok else 'BROKEN':12s} {'SCOPE(neg ctrl)':14s} {'sage':20s} "
          f"(no years_to_first_harvest -> must not flag)")

    # ---- (2) SENTINEL verdict governs everything.
    print()
    if not sentinel_reddened:
        print(f"HARNESS DEAD: the sentinel mutation ({SENTINEL_SLUG} PILL-CAPTION) did not redden. "
              f"{SENTINEL_SLUG} is clean and unmigrated on live data, so this means the harness "
              f"did not gate the mutated fixture. Every verdict above is void.")
        return 2

    survived = [r for r in results if r[2] == "SURVIVED"]
    unmeasurable = [r for r in results if r[2] == "UNMEASURABLE"]
    caught = [r for r in results if r[2] == "CAUGHT"]
    fams = {r[0] for r in caught}
    print(f"MUTATIONS: {len(results)}  CAUGHT: {len(caught)}  SURVIVED: {len(survived)}  "
          f"UNMEASURABLE: {len(unmeasurable)}")
    print(f"families with at least one caught mutation: {sorted(fams)} "
          f"(required: {sorted(FAMILY)})")
    print(f"sentinel: REDDENED   negative control: {'HELD' if scope_ok else 'BROKEN'}")

    ok = (not survived and not unmeasurable and fams == set(FAMILY) and scope_ok)
    print("\nRESULT:", "PASS -- every guard family is live" if ok else "FAIL -- see above")
    for f, s, v, doc in survived + unmeasurable:
        print(f"  {v}: {f} / {s} -- {doc}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
