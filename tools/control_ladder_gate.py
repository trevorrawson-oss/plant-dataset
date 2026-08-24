#!/usr/bin/env python3
"""control_ladder_gate -- the IPM pest/disease control-ladder honesty engine (spec 2026-07-22).

SOFT + standalone (overwinter_hardiness / variety_detail pattern) through the pilot; HARD-FLIPS into
whole_crop_gate A39 + gate_all when the roster-wide rollout reaches full coverage (INV-1).

  CATALOG   -- every control_methods entry has the required keys, a valid tier, non-empty pros/cons,
               and T1 catalogued sources.
  LADDER    -- every control_ladder is referentially sound, monotonic by tier (softest-first), and
               applies_to-coherent with the problem's `type`.
  IDENTITY  -- every pest/disease carries a unique kebab `id` within its crop.
Short ladders are VALID (a cultural-only ladder must pass); the gate never requires reaching `conventional`.

Usage: control_ladder_gate.py [PATH] [--coverage]
"""
import json, os, re, sys

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
            continue  # in-scope only once a ladder is authored (soft-pilot staging; rollout adds a coverage floor)
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


def all_violations(data):
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
    print(f"control_ladder_gate: {len(V)} violation(s)")
    sys.exit(1 if V else 0)


if __name__ == "__main__":
    main()
