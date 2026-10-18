"""test_climate_threshold_gate -- the register #7 climate gate, including the PLA-750 P5 amendment.

P5 (ruling b963b423, 2026-10-17): heat_threshold_f null + a STRESS heat_effect means "the stress is real,
no sourced number" (no weather alert fires), for the exact (slug, effect) pairs in NULL_STRESS_KNOWN.
Everything else about the heat pairing is unchanged: null + heat_tolerant is reviewed-N/A, an int with
heat_tolerant fails, and null + a stress effect on any OTHER crop still fails. A known entry that stops
matching the roster is STALE.

The gate had no suite of its own before PLA-750 (its only coverage was two A41 rows in
test_whole_crop_gate_register_shape); the pre-existing rules are pinned here too, so the amendment cannot
loosen them unnoticed. Run under pytest (every check is a def test_).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import climate_threshold_gate as g  # noqa: E402


def crop(slug="kale", **kw):
    c = {"slug": slug, "heat_threshold_f": 82, "heat_effect": "quality_loss", "frost_tolerance_f": 20,
         "frost_effect": "foliage_damaged", "chilling_sensitivity_f": None}
    c.update(kw)
    return c


def run_main(tmp_path, crops):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"crops": crops}))
    r = subprocess.run([sys.executable, os.path.join(HERE, "climate_threshold_gate.py"), str(p), "--coverage"],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def known_crops():
    return [crop(s, heat_threshold_f=None, heat_effect=e) for (s, e) in g.NULL_STRESS_KNOWN]


# ---- the P5 allowlist is exactly the three ruled crops --------------------------------------------
def test_known_set_is_exactly_the_three_ruled_crops():
    assert set(g.NULL_STRESS_KNOWN) == {("sweet-pea", "quality_loss"), ("sweet-alyssum", "quality_loss"),
                                        ("nasturtium", "quality_loss")}
    for why in g.NULL_STRESS_KNOWN.values():
        assert why.startswith("PLA-750 D5")


def test_known_crop_null_plus_its_stress_effect_passes():
    for c in known_crops():
        assert g.check_crop(c) == [], c["slug"]


def test_unknown_crop_null_plus_stress_effect_fails():
    v = g.check_crop(crop("borage", heat_threshold_f=None, heat_effect="quality_loss"))
    assert len(v) == 1 and "borage: heat_threshold_f is null but heat_effect is 'quality_loss'" in v[0]


def test_known_crop_with_a_different_stress_effect_fails():
    v = g.check_crop(crop("sweet-pea", heat_threshold_f=None, heat_effect="bolting"))
    assert len(v) == 1 and "sweet-pea: heat_threshold_f is null but heat_effect is 'bolting'" in v[0]


def test_known_crop_null_plus_heat_tolerant_still_passes_per_crop():
    # per-crop check is unchanged for the N/A marker; the roster run reports the entry STALE instead
    assert g.check_crop(crop("sweet-pea", heat_threshold_f=None, heat_effect="heat_tolerant")) == []


def test_roster_run_reports_a_stale_entry(tmp_path):
    crops = known_crops()
    crops[0]["heat_effect"] = "heat_tolerant"            # sweet-pea reverts to the N/A marker
    rc, out = run_main(tmp_path, crops)
    assert rc == 1
    assert "sweet-pea: NULL_STRESS_KNOWN entry (quality_loss) is STALE" in out


def test_roster_run_reports_a_stale_entry_when_the_crop_is_gone(tmp_path):
    rc, out = run_main(tmp_path, known_crops()[1:])
    assert rc == 1 and "is STALE" in out


def test_roster_run_green_with_all_three_known_and_reports_population(tmp_path):
    rc, out = run_main(tmp_path, known_crops() + [crop()])
    assert rc == 0, out
    assert "PASS (0 violations across 4 crops; 3 NULL_STRESS_KNOWN entries firing)" in out
    assert "stress, no number 3" in out


# ---- pre-existing heat rules, pinned so the amendment cannot loosen them ----------------------------
def test_int_threshold_with_heat_tolerant_fails():
    v = g.check_crop(crop(heat_effect="heat_tolerant"))
    assert any("heat_effect 'heat_tolerant' but heat_threshold_f is a number" in x for x in v)


def test_int_threshold_with_heat_tolerant_fails_for_a_known_crop_too():
    v = g.check_crop(crop("nasturtium", heat_threshold_f=85, heat_effect="heat_tolerant"))
    assert any("heat_effect 'heat_tolerant' but heat_threshold_f is a number" in x for x in v)


def test_null_with_heat_tolerant_passes():
    assert g.check_crop(crop("okra", heat_threshold_f=None, heat_effect="heat_tolerant")) == []


def test_unknown_enum_fails_even_for_a_known_crop():
    v = g.check_crop(crop("sweet-pea", heat_threshold_f=None, heat_effect="wilting"))
    assert any("not in" in x for x in v)


def test_missing_effect_and_orphan_effect_fail():
    c = crop(); del c["heat_effect"]
    assert any("heat_effect missing" in x for x in g.check_crop(c))
    c = crop(); del c["heat_threshold_f"]
    assert any("orphan" in x for x in g.check_crop(c))


def test_range_and_coherence_still_enforced():
    assert any("out of range" in x for x in g.check_crop(crop(heat_threshold_f=140)))
    assert any("must be <" in x for x in g.check_crop(crop(heat_threshold_f=74, frost_tolerance_f=40,
                                                            chilling_sensitivity_f=None) | {"frost_tolerance_f": 80}))
