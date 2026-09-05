#!/usr/bin/env python3
"""Tests for control_ladder_gate. Run: python3 tools/test_control_ladder_gate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from control_ladder_gate import catalog_violations

def data(methods, crops=None, srcs=None):
    return {
        "control_methods": methods,
        "source_catalog": srcs or {"umn_ext": {"tier": "T1"}, "seed_co": {"tier": "T2"}},
        "crops": crops or [],
    }

def method(**over):
    m = {"name": "Insecticidal soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"],
         "how_it_works_beginner": "x", "how_it_works_seasoned": "x", "best_use": "x",
         "pros": ["low tox"], "cons": ["contact only"], "sources": ["umn_ext"],
         "anchoring_urls": {"umn_ext": {"url": "u", "verified": "2026-07-22"}}}
    m.update(over); return m

# clean catalog -> no violations
assert catalog_violations(data({"insecticidal_soap": method()})) == []
# missing required key
assert any("missing/empty" in v for v in catalog_violations(data({"insecticidal_soap": method(pros=[])})))
# invalid tier
assert any("invalid tier" in v for v in catalog_violations(data({"insecticidal_soap": method(tier="nuke")})))
# NB: catalog method KEYS are snake_case (mirroring source_catalog keys) -- NOT format-checked here.
# The kebab ID_RE check applies only to per-crop pest/disease `id` (Task 3 identity).
# source not in catalog
assert any("not in source_catalog" in v for v in catalog_violations(data({"m": method(sources=["ghost"], anchoring_urls={"ghost": {}})})))
# source not T1
assert any("not T1" in v for v in catalog_violations(data({"m": method(sources=["seed_co"], anchoring_urls={"seed_co": {}})})))
# anchoring_urls mismatch
assert any("anchoring_urls" in v for v in catalog_violations(data({"m": method(anchoring_urls={})})))
print("catalog_violations tests: OK")

from control_ladder_gate import ladder_violations

CAT = {
    "rotate_crops":     {"name": "Rotation", "tier": "cultural", "applies_to": ["any"]},
    "insecticidal_soap":{"name": "Soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"]},
    "copper":           {"name": "Copper", "tier": "soft_chemical", "applies_to": ["fungal_foliar"]},
    "pyrethrin":        {"name": "Pyrethrin", "tier": "conventional", "applies_to": ["insect_general"]},
}
def crop(problems, key="pests"):
    return {"slug": "broccoli", key: problems}
def prob(**over):
    p = {"id": "aphids", "name": "Aphids", "type": "insect",
         "control_ladder": [{"method": "rotate_crops"}, {"method": "insecticidal_soap"}]}
    p.update(over); return p
def D(crop_obj):  # gate expects (data, crop)
    return ({"control_methods": CAT}, crop_obj)

# clean softest-first ladder -> no violations
assert ladder_violations(*D(crop([prob()]))) == []
# absent ladder -> not a ladder violation (coverage handles it)
assert ladder_violations(*D(crop([prob(control_ladder=None)]))) == []
# EMPTY ladder -> IS a violation. `None` means "not yet laddered", which is legal through the
# rollout; `[]` means "laddered and left blank", which is a defect in every case. Found 2026-08-24
# when a batch-2 authoring agent correctly refused to pad sweet-corn's raccoons ladder (no catalog
# method reaches vertebrate exclusion) and emitted []. control_ladder_gate returned 0 violations and
# gate_all stayed 121/121, so the crop's HIGHEST-SEVERITY problem would have shipped with no
# guidance at all, invisibly. This is NOT the coverage floor, which stays deliberately unarmed.
assert any("empty" in v for v in ladder_violations(*D(crop([prob(control_ladder=[])]))))
# and it must fire on a disease as well as a pest
assert any("empty" in v for v in ladder_violations(*D(crop([prob(control_ladder=[])], key="diseases"))))
# dangling method reference
assert any("unknown method" in v for v in ladder_violations(*D(crop([prob(control_ladder=[{"method": "ghost"}])]))))
# NON-monotonic: conventional before cultural
bad = [{"method": "pyrethrin"}, {"method": "rotate_crops"}]
assert any("softest-first" in v for v in ladder_violations(*D(crop([prob(control_ladder=bad)]))))
# applies_to mismatch: insecticidal soap under a FUNGAL disease
fung = prob(id="downy-mildew", name="Downy mildew", type="fungal",
            control_ladder=[{"method": "rotate_crops"}, {"method": "insecticidal_soap"}])
assert any("does not fit problem type" in v for v in ladder_violations(*D(crop([fung], key="diseases"))))
# cultural-only SHORT ladder (clubroot) -> MUST PASS
club = prob(id="clubroot", name="Clubroot", type="fungal", control_ladder=[{"method": "rotate_crops"}])
assert ladder_violations(*D(crop([club], key="diseases"))) == []
# bad-tier catalog method in a ladder must NOT crash (catalog_violations reports the bad tier separately)
_badcat = {"broken": {"name": "Broken", "applies_to": ["any"]}}  # no tier key
assert ladder_violations({"control_methods": _badcat}, crop([prob(control_ladder=[{"method": "broken"}])])) == []
# unrecognized problem type -> flagged (applies_to coherence cannot be checked)
_unk = prob(id="mystery", type="fungusy", control_ladder=[{"method": "insecticidal_soap"}])
assert any("not a recognized type" in v for v in ladder_violations(*D(crop([_unk]))))
print("ladder_violations tests: OK")

from control_ladder_gate import identity_violations, all_violations, coverage_report

_L = [{"method": "m"}]  # a ladder just needs to be present (non-None) to bring a problem in-scope
# missing id (in-scope: has a ladder)
assert any("missing 'id'" in v for v in identity_violations({"slug": "x", "pests": [{"name": "Aphids", "control_ladder": _L}]}))
# duplicate id within crop
dup = {"slug": "x", "pests": [{"id": "aphids", "control_ladder": _L}], "diseases": [{"id": "aphids", "control_ladder": _L}]}
assert any("duplicate id" in v for v in identity_violations(dup))
# non-kebab id
assert any("kebab" in v for v in identity_violations({"slug": "x", "pests": [{"id": "Cabbage_Worm", "control_ladder": _L}]}))
# a problem WITHOUT a ladder is out of scope -> not flagged for a missing id (soft-pilot staging)
assert identity_violations({"slug": "x", "pests": [{"name": "Not yet migrated"}]}) == []
# clean -> none
assert identity_violations({"slug": "x", "pests": [{"id": "aphids", "control_ladder": _L}], "diseases": [{"id": "clubroot", "control_ladder": _L}]}) == []

# coverage_report counts certified problems + ladders
cov = coverage_report({
    "control_methods": {"a": {}, "b": {}},
    "crops": [
        {"verification_status": {"status": "verified_gs_arc"}, "pests": [{"id": "p", "control_ladder": [{"method": "a"}]}], "diseases": []},
        {"verification_status": {"status": "shell"}, "pests": [{"id": "q"}]},
    ],
})
assert cov == {"catalog_methods": 2, "certified_crops": 1, "problems_on_certified": 1, "problems_with_ladder": 1}, cov
print("identity + coverage tests: OK")

# --- vertebrate type (strawberry Birds): bird exclusion is coherent, insecticide is not ---
_vcat = {
    "bird_netting": method(name="Bird netting", tier="physical", applies_to=["vertebrate"]),
    "pyrethrin":    method(name="Pyrethrin", tier="conventional", applies_to=["insect_general"]),
}
_birds_ok = prob(id="birds", name="Birds", type="vertebrate",
                 control_ladder=[{"method": "bird_netting"}])
_birds_bad = prob(id="birds", name="Birds", type="vertebrate",
                  control_ladder=[{"method": "pyrethrin"}])
# coherent: netting applies to vertebrates
assert ladder_violations(data(_vcat, [crop([_birds_ok])]), crop([_birds_ok])) == []
# incoherent: an insecticide does not apply to a vertebrate
assert any("applies_to" in v for v in
           ladder_violations(data(_vcat, [crop([_birds_bad])]), crop([_birds_bad])))

# ---------------------------------------------------------------------------------------------
# THE COVERAGE FLOOR (PLA-8 arc close, 2026-09-05). `control_ladder_gate`'s INV-1 condition.
#
# THE UNIT IS THE PROBLEM ENTRY, NOT THE CROP. "every crop laddered" is the wrong test and would
# fail at 121/128 forever: the seven shells (avocado, olive, the five mushrooms) carry
# `pests: []` / `diseases: []` -- present and empty by intent -- so they hold ZERO entries to
# ladder and satisfy an entry-scoped floor by construction, at any certification status.
#
# ABSENCE only. `[]` is a DIFFERENT defect ("laddered and left blank") and belongs to
# ladder_violations, which has owned it since 2026-08-24. The floor must stay silent on it, or the
# same defect is reported twice under two names.
from control_ladder_gate import coverage_violations

_LAD = [{"method": "rotate_crops"}]

# fully laddered -> silent
assert coverage_violations({"slug": "apple", "pests": [{"id": "codling-moth", "control_ladder": _LAD}]}) == []
# control_ladder: None -> the floor fires
assert any("no control_ladder" in v for v in
           coverage_violations({"slug": "apple", "pests": [{"id": "codling-moth", "control_ladder": None}]}))
# control_ladder KEY ABSENT -> the floor fires. This is the shape a newly-authored problem entry
# actually arrives in; a floor that only checks `is None` never sees it.
assert any("no control_ladder" in v for v in
           coverage_violations({"slug": "apple", "pests": [{"id": "codling-moth"}]}))
# ...and on diseases[] as well as pests[]
assert any("no control_ladder" in v for v in
           coverage_violations({"slug": "apple", "diseases": [{"id": "apple-scab"}]}))
# THE SEVEN SHELLS: present-and-empty arrays hold no entries -> the floor is silent, cert status
# irrelevant. A floor written "every crop carries a ladder" fails here, which is the whole point.
assert coverage_violations({"slug": "avocado", "pests": [], "diseases": []}) == []
assert coverage_violations({"slug": "olive", "pests": [], "diseases": [],
                            "verification_status": {"status": "verified_gs_arc"}}) == []
# a crop carrying neither key at all -> also silent
assert coverage_violations({"slug": "button-mushroom"}) == []
# REFUSAL SPEC: `[]` is ladder_violations' defect, not the floor's. Silent here is the contract.
assert coverage_violations({"slug": "sweet-corn", "pests": [{"id": "raccoons", "control_ladder": []}]}) == []

# THE MICROGREEN SCHEMA (PLA-452): `name_seasoned` / `name_beginner`, NO `name`, on 8 crops. Three
# instruments this arc were blind to it or dead. The floor must READ these entries, and must name
# them legibly when it fires -- a floor that reports "?" is a floor nobody can act on.
_MICRO = {"id": "fungus-gnats", "name_beginner": "Fungus gnats", "name_seasoned": "Fungus gnats",
          "type": "insect"}
_v = coverage_violations({"slug": "wheatgrass", "pests": [dict(_MICRO)]})
assert any("no control_ladder" in v for v in _v), _v
assert any("fungus-gnats" in v for v in _v), _v
# and with no `id` either -- the label falls through the display-name schema, never to "?"
_v = coverage_violations({"slug": "wheatgrass",
                          "diseases": [{"name_beginner": "Damping off", "name_seasoned": "Damping-off"}]})
assert any("Damping" in v for v in _v), _v
assert not any("?" in v for v in _v), _v

# ---------------------------------------------------------------------------------------------
# WHERE THE FLOOR IS WIRED, AND WHERE IT DELIBERATELY IS NOT.
#
# `all_violations` STAYS INTEGRITY-ONLY. Putting the floor in it was tried on 2026-09-05 and
# reverted the same day: 29 pinned PLA-8 promote suites assert `all_violations(post) == []` on
# HISTORICAL post-states, and those states legitimately carried unladdered problems -- batch 20's
# post-state has 190 of them, because it is a snapshot of a rollout in progress. Widening
# `all_violations` made every one of those suites assert something FALSE about its own moment, and
# turned a 5-failure tree into 33. A gate must not be armed on data it reddens; a pinned fixture is
# data. Do not "finish the job" by adding it back.
_mid_arc = {"crops": [{"slug": "apple", "pests": [{"id": "codling-moth"}]}],
            "control_methods": {}, "source_catalog": {}}
assert not any("no control_ladder" in v for v in all_violations(_mid_arc)), all_violations(_mid_arc)

# It IS reached from the two places that police the SHIPPING roster: whole_crop_gate A57 (covered by
# tools/mutate_a57_coverage_floor.py, graded through the full gate) and this module's own CLI. A
# guard whose entry point is never called is a zero with extra steps -- the catalog-r8 lesson was 53
# green tests over a main() that never called check() -- so the CLI path is exercised for real.
import subprocess, tempfile, json as _json
_fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
_json.dump(_mid_arc, _fh); _fh.close()
_r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "control_ladder_gate.py"), _fh.name],
                    capture_output=True, text=True)
os.unlink(_fh.name)
assert _r.returncode != 0, _r.stdout
assert "COVERAGE FLOOR" in _r.stdout, _r.stdout
assert "no control_ladder" in _r.stdout, _r.stdout
print("coverage_violations tests: OK")
