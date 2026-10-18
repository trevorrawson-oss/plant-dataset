"""test_sowing_heat_ceiling_gate -- register #35 (PLA-750), docs/sowing_heat_ceiling_contract.md.

Every check is a def test_ (run under pytest). Fixtures are synthetic: a tiny roster plus a scratch
evidence directory whose pages are written, hashed and MANIFEST-listed here, so the byte checks read
real hashed files exactly as the gate does on the canonical.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sowing_heat_ceiling_gate as g  # noqa: E402

U_SP = "https://extension.example.edu/spinach"
U_LT = "https://extension.example.edu/leafy-greens"
U_KO_C = "https://extension.example.edu/kohlrabi-a"
U_KO_T = "https://extension.example.edu/kohlrabi-b"
U_CAL = "https://journal.example.org/calendula"
U_BR = "https://extension.example.edu/broccoli"

PAGES = {
    U_SP: "<html><p>For a continuous spring supply, plant spinach seeds every one to two weeks, until outdoor "
          "temperatures reach 80&deg;F.</p></html>",
    U_LT: "<p>Soil temperatures above 80 °F cause the seeds of some crops (lettuce, spinach, others) to go "
          "dormant.</p>",
    U_KO_C: "<p>Avoid planting after May 1. The high temperatures will not produce good quality.</p>",
    U_KO_T: "<p>Kohlrabi grows best when temperatures do not exceed 75°F.</p>",
    U_CAL: "<p>Calendula seed should only be sown in the field if environmental temperature conditions are "
           "predicted to be below 30°C during seed germination.</p>",
    U_BR: "<p>Direct seed broccoli in July for a fall crop.</p>",
}
CAT = {k: {"id": k, "tier": "T1"} for k in ("umn_ext", "usu_ext", "eberle_2014")}


def anchors(**kv):
    return {k: {"url": u, "verified": "2026-10-17"} for k, u in kv.items()}


def held(**kw):
    f = {"temp_f": 80, "measures": "air", "basis": "sowing_statement",
         "claim": "For a continuous spring supply, plant spinach seeds every one to two weeks, until outdoor "
                  "temperatures reach 80°F.",
         "claim_source": "umn_ext", "sources": ["umn_ext"], "anchoring_urls": anchors(umn_ext=U_SP)}
    f.update(kw)
    return f


def soil(**kw):
    f = {"temp_f": 80, "measures": "soil", "basis": "germination",
         "claim": "Soil temperatures above 80 °F cause the seeds of some crops (lettuce, spinach, others) to go "
                  "dormant.",
         "claim_source": "usu_ext", "note": "Soil figure; the app compares a forecast air high (D2 proxy).",
         "sources": ["usu_ext"], "anchoring_urls": anchors(usu_ext=U_LT)}
    f.update(kw)
    return f


def nulled(**kw):
    f = {"temp_f": None, "note": 'No sowing hold: UMN, "Direct seed broccoli in July for a fall crop."',
         "sources": ["umn_ext"], "anchoring_urls": anchors(umn_ext=U_BR)}
    f.update(kw)
    return f


def crop(slug, field, pause):
    c = {"slug": slug, "succession_policy": {"pause_in_heat": pause}}
    if field is not None:
        c[g.FIELD] = field
    return c


@pytest.fixture
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    rows = ["sha256\tbytes\tfetched\tagents\turl\tsaved_by"]
    for url, text in PAGES.items():
        raw = text.encode()
        h = hashlib.sha256(raw).hexdigest()
        (d / f"{h}.html").write_bytes(raw)
        rows.append(f"{h}\t{len(raw)}\t2026-10-17\tcurl\t{url}\ttest")
    (d / "MANIFEST.tsv").write_text("\n".join(rows) + "\n")
    return str(d)


def shape(c):
    return g.check_crop(c, CAT)


def byt(c, ev):
    return g.check_bytes(c, g.load_manifest(ev), ev, {})


# ---- shape ---------------------------------------------------------------------------------------
def test_clean_held_soil_and_null_pass_shape():
    assert shape(crop("spinach", held(), True)) == []
    assert shape(crop("lettuce-leaf", soil(), True)) == []
    assert shape(crop("broccoli", nulled(), False)) == []


def test_absent_field_without_a_hold_is_todo_not_a_violation():
    assert shape(crop("tomato", None, False)) == []
    assert shape({"slug": "okra"}) == []


@pytest.mark.parametrize("pause,field", [(True, nulled()), (False, held()), (None, held())])
def test_invariant_pause_iff_int(pause, field):
    v = shape(crop("x", field, pause))
    assert any("pause_in_heat" in s for s in v), v


def test_a_hold_with_no_reviewed_field_fails():
    v = shape(crop("dill", None, True))
    assert v == ["dill: succession_policy.pause_in_heat is true but sowing_heat_ceiling is absent "
                 "(a hold with no reviewed reason)"]


@pytest.mark.parametrize("mut,needle", [
    (lambda f: f.update(temp_f=80.0), "not an int"),
    (lambda f: f.update(temp_f=True), "not an int"),
    (lambda f: f.update(temp_f=110), "out of range"),
    (lambda f: f.update(measures="water"), "measures"),
    (lambda f: f.update(basis="vibes"), "basis"),
    (lambda f: f.update(claim="  "), "claim"),
    (lambda f: f.update(claim_source="usu_ext"), "claim_source"),
    (lambda f: f.update(temp_source="umn_ext"), "temp_source"),
    (lambda f: f.update(temp_source="usu_ext"), "temp_source"),
    (lambda f: f.update(sources=["umn_ext", "umn_ext"]), "twice"),
    (lambda f: f.update(sources=[]), "sources"),
    (lambda f: f["anchoring_urls"].update(usu_ext={"url": U_LT, "verified": "2026-10-17"}), "differ"),
    (lambda f: f["anchoring_urls"]["umn_ext"].update(url="https://extension.example.edu/"), "document"),
    (lambda f: f["anchoring_urls"]["umn_ext"].pop("verified"), "verified"),
    (lambda f: f.update(extra=1), "keys"),
    (lambda f: f.pop("basis"), "keys"),
])
def test_held_shape_mutations_fail(mut, needle):
    f = held()
    mut(f)
    v = shape(crop("spinach", f, True))
    assert any(needle in s for s in v), (needle, v)


def test_source_not_in_catalog_fails():
    f = held(claim_source="nowhere_ext", sources=["nowhere_ext"], anchoring_urls=anchors(nowhere_ext=U_SP))
    assert any("not in source_catalog" in s for s in shape(crop("spinach", f, True)))


def test_soil_row_needs_a_note_and_air_row_may_omit_it():
    f = soil()
    del f["note"]
    assert any("note" in s for s in shape(crop("lettuce-leaf", f, True)))
    assert shape(crop("spinach", held(), True)) == []


@pytest.mark.parametrize("mut,needle", [
    (lambda f: f.update(note=""), "note"),
    (lambda f: f.pop("note"), "keys"),
    (lambda f: f.update(sources=[], anchoring_urls={}), "sources"),
    (lambda f: f.update(measures="air"), "keys"),
    (lambda f: f.update(claim="x"), "keys"),
])
def test_null_shape_mutations_fail(mut, needle):
    f = nulled()
    mut(f)
    v = shape(crop("broccoli", f, False))
    assert any(needle in s for s in v), (needle, v)


def test_field_must_be_an_object():
    assert any("object" in s for s in shape(crop("spinach", 80, True)))
    assert any("object" in s for s in shape(crop("spinach", None, True) | {g.FIELD: None}))


# ---- bytes ---------------------------------------------------------------------------------------
def test_clean_rows_pass_the_byte_checks(ev):
    assert byt(crop("spinach", held(), True), ev) == []
    assert byt(crop("lettuce-leaf", soil(), True), ev) == []
    assert byt(crop("broccoli", nulled(), False), ev) == []


def test_claim_not_in_the_bytes_fails(ev):
    f = held(claim="Plant spinach seeds until outdoor temperatures reach 80°F, says nobody.")
    v = byt(crop("spinach", f, True), ev)
    assert len(v) == 1 and "claim is not in the hashed bytes" in v[0]


def test_claim_on_the_wrong_page_fails(ev):
    f = held(anchoring_urls=anchors(umn_ext=U_BR))
    assert any("claim is not in the hashed bytes" in s for s in byt(crop("spinach", f, True), ev))


def test_unhashed_url_fails(ev):
    f = held(anchoring_urls=anchors(umn_ext="https://extension.example.edu/never-fetched"))
    assert any("no MANIFEST-listed bytes" in s for s in byt(crop("spinach", f, True), ev))


def test_tampered_bytes_fail(ev):
    for name in os.listdir(ev):
        if name.endswith(".html"):
            p = os.path.join(ev, name)
            if "spinach" in open(p).read():
                open(p, "a").write("tampered")
    assert any("hash to" in s for s in byt(crop("spinach", held(), True), ev))


def test_number_must_be_in_the_claim(ev):
    v = byt(crop("spinach", held(temp_f=78), True), ev)
    assert any("temp_f 78 is not in the claim" in s for s in v)


def test_celsius_claim_carries_its_fahrenheit_rounding(ev):
    f = held(temp_f=86, claim="Calendula seed should only be sown in the field if environmental temperature "
                              "conditions are predicted to be below 30°C during seed germination.",
             claim_source="eberle_2014", sources=["eberle_2014"], anchoring_urls=anchors(eberle_2014=U_CAL))
    assert byt(crop("calendula", f, True), ev) == []
    f85 = copy.deepcopy(f)
    f85["temp_f"] = 85
    assert any("temp_f 85 is not in the claim" in s for s in byt(crop("calendula", f85, True), ev))


def test_ordinal_degree_sign_still_carries_the_number(ev, tmp_path):
    # NFKC turns the masculine ordinal "º" (USU's "80ºF") into "o"; the number must still be found
    f = held(claim="Peas require soil and air temperatures to remain below 80ºF for best germination.")
    assert not any("is not in the claim" in s for s in byt(crop("sugar-snap-peas", f, True), ev))
    f78 = held(temp_f=78, claim=f["claim"])
    assert any("temp_f 78 is not in the claim" in s for s in byt(crop("sugar-snap-peas", f78, True), ev))


def test_a_number_inside_a_longer_number_does_not_count(ev):
    f = held(temp_f=80, claim="Plant spinach seeds every one to two weeks, until outdoor temperatures reach 180°F.")
    assert any("temp_f 80 is not in the claim" in s for s in byt(crop("spinach", f, True), ev))


def test_publisher_period_before_the_celsius_unit_is_tolerated(ev):
    # the 2014 abstract page renders 30 °C as "30. °C"; the claim keeps it verbatim
    f = held(temp_f=86, claim="Calendula seed should be sown only if soil conditions are below 30. °C.",
             claim_source="eberle_2014", sources=["eberle_2014"], anchoring_urls=anchors(eberle_2014=U_CAL))
    assert not any("is not in the claim" in s for s in byt(crop("calendula", f, True), ev))
    f["claim"] = "Calendula seed should be sown only if soil conditions are below 31. °C."
    assert any("temp_f 86 is not in the claim" in s for s in byt(crop("calendula", f, True), ev))


def kohlrabi(**kw):
    f = held(temp_f=75, basis="maturity_coupled",
             claim="Avoid planting after May 1. The high temperatures will not produce good quality.",
             claim_source="umn_ext", temp_source="usu_ext", sources=["umn_ext", "usu_ext"],
             anchoring_urls=anchors(umn_ext=U_KO_C, usu_ext=U_KO_T))
    f.update(kw)
    return f


def test_temp_source_page_must_state_the_number_with_a_unit(ev):
    assert byt(crop("kohlrabi", kohlrabi(), True), ev) == []
    v = byt(crop("kohlrabi", kohlrabi(temp_f=72), True), ev)
    assert any("temp_f 72 is not stated with a degree unit" in s for s in v)


def test_quoted_note_span_must_be_in_the_bytes(ev):
    f = nulled(note='No sowing hold: UMN, "Direct seed broccoli in August for a spring crop."')
    v = byt(crop("broccoli", f, False), ev)
    assert len(v) == 1 and "note quote is not in the hashed bytes" in v[0]


def test_curly_quoted_note_span_is_checked_too(ev):
    f = nulled(note="No sowing hold: UMN, “Direct seed broccoli in August for a spring crop.”")
    assert any("note quote" in s for s in byt(crop("broccoli", f, False), ev))


def test_a_note_with_no_quote_passes_the_byte_check(ev):
    assert byt(crop("lettuce-leaf", soil(note="Soil figure; the app compares an air high."), True), ev) == []


# ---- the roster run ------------------------------------------------------------------------------
def run(tmp_path, crops, *args):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"crops": crops, "source_catalog": CAT}))
    r = subprocess.run([sys.executable, os.path.join(HERE, "sowing_heat_ceiling_gate.py"), str(p), *args],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def roster():
    return [crop("spinach", held(), True), crop("lettuce-leaf", soil(), True),
            crop("broccoli", nulled(), False), crop("tomato", None, False)]


def test_roster_run_reports_its_population(tmp_path, ev):
    rc, out = run(tmp_path, roster(), "--evidence", ev, "--floor", "3")
    assert rc == 0, out
    assert "inspected 3 crop(s) carrying sowing_heat_ceiling (held 2, not held 1) of 4 scanned; TODO 1" in out
    assert "byte checks: 3 crop(s) against" in out
    assert "PASS" in out


def test_roster_run_refuses_below_its_floor(tmp_path, ev):
    rc, out = run(tmp_path, roster(), "--evidence", ev, "--floor", "4")
    assert rc == 2 and "REFUSED: inspected 3 crop(s), below the floor of 4" in out


def test_default_floor_is_the_pilot_thirty():
    assert g.POPULATION_FLOOR == 30


def test_roster_run_refuses_an_empty_population(tmp_path):
    rc, out = run(tmp_path, [crop("tomato", None, False)], "--floor", "0")
    assert rc == 2 and "REFUSED: inspected 0 crop(s)" in out


def test_roster_run_fails_on_a_violation(tmp_path, ev):
    crops = roster()
    crops[0][g.FIELD]["temp_f"] = 78
    rc, out = run(tmp_path, crops, "--evidence", ev, "--floor", "3")
    assert rc == 1 and "temp_f 78 is not in the claim" in out


def test_roster_run_without_evidence_says_bytes_were_not_checked(tmp_path):
    rc, out = run(tmp_path, roster(), "--floor", "3")
    assert rc == 0 and "byte checks: SKIPPED (no --evidence)" in out


def test_a_crop_added_to_the_roster_is_inspected(tmp_path, ev):
    crops = roster() + [crop("ghost-crop", held(temp_f=99), True)]
    rc, out = run(tmp_path, crops, "--evidence", ev, "--floor", "3")
    assert rc == 1 and "ghost-crop" in out and "inspected 4 crop(s)" in out
