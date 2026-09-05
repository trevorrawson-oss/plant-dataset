#!/usr/bin/env python3
"""control_ladder_gate -- the IPM pest/disease control-ladder honesty engine (spec 2026-07-22).

SOFT + standalone (overwinter_hardiness / variety_detail pattern) through the pilot. INTEGRITY
hard-flipped into whole_crop_gate as A56 on 2026-08-22; COVERAGE hard-flipped as A57 on 2026-09-05,
when the roster-wide rollout reached full coverage at 913 of 913 problem entries laddered. INV-1 is
therefore SATISFIED, not pending.

  CATALOG   -- every control_methods entry has the required keys, a valid tier, non-empty pros/cons,
               and T1 catalogued sources.
  LADDER    -- every control_ladder is referentially sound, monotonic by tier (softest-first), and
               applies_to-coherent with the problem's `type`.
  IDENTITY  -- every pest/disease carries a unique kebab `id` within its crop.
  COVERAGE  -- every problem ENTRY is laddered (the floor; see coverage_violations for why the unit
               is the entry and not the crop, and why the seven shells pass rather than needing a
               carve-out).
Short ladders are VALID (a cultural-only ladder must pass); the gate never requires reaching `conventional`.

Usage: control_ladder_gate.py [PATH] [--coverage]
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from problem_id_collision_gate import display_names   # the PLA-449 schema table, imported not retyped

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
TIER_RANK = {t: i for i, t in enumerate(TIERS)}

# type -> the applies_to targets that legitimately apply to it
TYPE_TARGETS = {
    "insect":        {"insect_soft_bodied", "insect_chewing", "insect_boring", "insect_general"},
    "mite":          {"mite", "insect_general"},
    "mollusk":       {"mollusk"},
    "fungal":        {"fungal_foliar", "fungal_soilborne", "disease_general"},
    "bacterial":     {"bacterial", "disease_general"},
    "viral":         {"viral", "disease_general"},
    "physiological": {"physiological"},
    "nematode":      {"nematode"},
    "vertebrate":    {"vertebrate"},
}
UNIVERSAL_TARGET = "any"   # cultural/physical practices that apply broadly
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_REQ_METHOD = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
               "best_use", "pros", "cons", "sources", "anchoring_urls")


def load(path):
    with open(path) as f:
        return json.load(f)


def catalog(data):
    return data.get("control_methods") or {}


def _problems(crop):
    return list(crop.get("pests") or []) + list(crop.get("diseases") or [])


def catalog_violations(data):
    V = []
    cat = catalog(data)
    srcs = data.get("source_catalog") or {}
    for mid, m in cat.items():
        for k in _REQ_METHOD:
            if k not in m or m[k] in (None, "", [], {}):
                V.append(f"control_methods/{mid}: missing/empty required key '{k}'")
        if m.get("tier") not in TIER_RANK:
            V.append(f"control_methods/{mid}: invalid tier {m.get('tier')!r}")
        for s in (m.get("sources") or []):
            if s not in srcs:
                V.append(f"control_methods/{mid}: source '{s}' not in source_catalog")
            elif srcs[s].get("tier") != "T1":
                V.append(f"control_methods/{mid}: source '{s}' is not T1")
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            V.append(f"control_methods/{mid}: anchoring_urls keys do not match sources")
    return V


def ladder_violations(data, crop):
    V = []
    cat = catalog(data)
    slug = crop.get("slug", "?")
    for p in _problems(crop):
        pid = p.get("id") or p.get("name") or "?"
        ladder = p.get("control_ladder")
        if ladder is None:
            # `None` = not yet laddered. Legal through the rollout; coverage_report tracks it.
            continue
        if not ladder:
            # `[]` = laddered and left BLANK, which is a defect in every case and is NOT the same
            # state as `None`. Added 2026-08-24: a batch-2 authoring agent correctly refused to pad
            # sweet-corn's raccoons ladder (no catalog method reaches vertebrate exclusion) and
            # emitted []. Every gate passed it -- control_ladder_gate 0 violations, gate_all
            # 121/121 -- so the crop's highest-severity problem would have shipped with no guidance
            # at all, invisibly. A SHAPE gate cannot see ABSENCE unless absence is spelled out.
            V.append(f"{slug}/{pid}: control_ladder is empty; use null for 'not yet laddered', "
                     f"or author at least one rung")
            continue
        ptype = p.get("type")
        if ptype not in TYPE_TARGETS:
            # fail-closed: an unrecognized/missing type means applies_to coherence cannot be
            # verified, so we flag it rather than silently passing (also enforces the type enum).
            V.append(f"{slug}/{pid}: problem type {ptype!r} is not a recognized type "
                     f"(applies_to coherence cannot be checked)")
        ranks = []
        for rung in ladder:
            mid = rung.get("method")
            m = cat.get(mid)
            if m is None:
                V.append(f"{slug}/{pid}: control_ladder references unknown method '{mid}'")
                continue
            rank = TIER_RANK.get(m.get("tier"))  # defensive: a bad tier is catalog_violations' job to report
            if rank is not None:
                ranks.append(rank)
            targets = set(m.get("applies_to") or [])
            if UNIVERSAL_TARGET not in targets and ptype in TYPE_TARGETS:
                if not (targets & TYPE_TARGETS[ptype]):
                    V.append(f"{slug}/{pid}: method '{mid}' (applies_to {sorted(targets)}) "
                             f"does not fit problem type '{ptype}'")
        if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):
            V.append(f"{slug}/{pid}: control_ladder is not softest-first (tier ranks {ranks})")
    return V


def identity_violations(crop):
    V = []
    slug = crop.get("slug", "?")
    seen = {}
    for p in _problems(crop):
        if p.get("control_ladder") is None:
            # In-scope only once a ladder is authored. Not a hole since 2026-09-05: an
            # unladdered entry is coverage_violations' defect, reported there exactly once.
            continue
        pid = p.get("id")
        if not pid:
            V.append(f"{slug}/{p.get('name') or p.get('name_beginner') or '?'}: pest/disease missing 'id'")
            continue
        if not ID_RE.match(pid):
            V.append(f"{slug}/{pid}: id is not kebab-case")
        seen[pid] = seen.get(pid, 0) + 1
    for pid, n in seen.items():
        if n > 1:
            V.append(f"{slug}/{pid}: duplicate id ({n}x) within crop")
    return V


def _label(p):
    """A problem entry's display handle, `id` first, then every name schema the roster uses.

    The microgreens (PLA-452, 8 crops) carry `name_seasoned` / `name_beginner` and NO `name`, so a
    name-keyed label prints "?" on exactly the crops that were already the arc's blind spot -- the
    PLA-449 collision gate reported two minted ids BLIND when its DISPLAY_NAME_FIELDS was narrowed
    to ("name",). A floor nobody can read the output of is not a floor.
    """
    for v in [p.get("id")] + display_names(p):
        if v:
            return v
    return "unnamed problem entry"


def coverage_violations(crop):
    """THE COVERAGE FLOOR. Armed 2026-09-05 at the PLA-8 arc close; this module's INV-1 condition.

    THE UNIT IS THE PROBLEM ENTRY, NEVER THE CROP. "every certified crop carries a ladder" is the
    wrong test and would sit red at 121 of 128 forever: the seven shells (avocado, olive, the five
    mushrooms) carry `pests: []` / `diseases: []` -- present and empty by intent -- so they hold
    zero entries to ladder and pass by construction, at any certification status. That also answers
    the question the arm deferred: a crop with no problems is legal, because there is nothing
    unladdered about it.

    ABSENCE ONLY -- a `control_ladder` that is missing or `None`. `[]` is the separate "laddered and
    left blank" defect and has belonged to `ladder_violations` since 2026-08-24; reporting it here
    too would name one defect twice under two guards.
    """
    slug = crop.get("slug", "?")
    return [f"{slug}/{_label(p)}: problem entry carries no control_ladder "
            f"(every problem entry on a crop must be laddered)"
            for p in _problems(crop) if p.get("control_ladder") is None]


def all_violations(data):
    """INTEGRITY ONLY -- catalog + ladder + identity. The COVERAGE FLOOR IS DELIBERATELY NOT HERE.

    DO NOT "finish the job" by adding `coverage_violations` to this list. It was tried on
    2026-09-05 and reverted the same day. 29 pinned PLA-8 promote suites assert
    `all_violations(post) == []` on HISTORICAL post-states, and a mid-rollout post-state
    legitimately carries unladdered problems -- batch 20's carries 190 of them, because that is what
    a rollout in progress looks like. Widening this function made all 29 assert something false
    about their own moment and took the tree from 5 failures to 33. A gate must not be armed on data
    it reddens, and a pinned fixture is data.

    The floor polices the SHIPPING roster, and it is reached from the two places that do that:
    `whole_crop_gate` A57 (per crop, enforced roster-wide by `gate_all`) and this module's `main()`.
    """
    V = list(catalog_violations(data))
    for crop in data.get("crops", []):
        V += ladder_violations(data, crop)
        V += identity_violations(crop)
    return V


def coverage_report(data):
    crops = data.get("crops", [])
    certified = [c for c in crops if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    problems = sum(len(_problems(c)) for c in certified)
    with_ladder = sum(1 for c in certified for p in _problems(c) if p.get("control_ladder") is not None)
    return {"catalog_methods": len(catalog(data)), "certified_crops": len(certified),
            "problems_on_certified": problems, "problems_with_ladder": with_ladder}


def main():
    argv = sys.argv[1:]
    pos = [a for a in argv if not a.startswith("--")]
    path = pos[0] if pos else "crops_data_final.json"
    data = load(path)
    if "--coverage" in argv:
        import pprint; pprint.pprint(coverage_report(data))
    V = all_violations(data)
    for v in V:
        print("VIOLATION:", v)
    # The coverage floor prints SEPARATELY, because it is a different claim from integrity and
    # because a reader has to be able to tell which half failed. It counts toward the exit status:
    # a person running this on the live canonical is asking whether the SHIPPING roster is sound.
    C = [v for crop in data.get("crops", []) for v in coverage_violations(crop)]
    for v in C:
        print("COVERAGE FLOOR:", v)
    print(f"control_ladder_gate: {len(V)} integrity violation(s), "
          f"{len(C)} unladdered problem entr{'y' if len(C) == 1 else 'ies'}")
    sys.exit(1 if (V or C) else 0)


if __name__ == "__main__":
    main()
