"""Suite for promote_housekeeping60_phase_c (housekeeping kickoff 60, Phase C, parts 1 to 3).

The pre-state is REPLAYED from its pinned commit (promote_fixture.pre_state(b331e5f2) -> 9cea239), never read live, so
the suite survives this promote landing. One test runs the whole promote (gates included) on the real stage and pins
its populations and its post SHA; every other test hands check_post a stage with ONE defect injected, and asserts the
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_housekeeping60_phase_c as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

POST_SHA = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"


@pytest.fixture(scope="module")
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope="module")
def stage():
    return P.load_stage(P.STAGE)


def _check(pre, ops, ev, dec, post=None):
    P.check_pre(pre, ops)
    post = P.apply_to(pre, ops) if post is None else post
    return P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def _refuses(match, pre, ops, ev, dec, post=None):
    with pytest.raises(Refused, match=match):
        _check(pre, ops, ev, dec, post)


def _find(ops, crop, path):
    hits = [i for i, o in enumerate(ops) if o["crop"] == crop and o["path"] == path]
    assert len(hits) == 1, (crop, path, hits)
    return hits[0]


# ---------------------------------------------------------------- the real stage
def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (77, 211, 32, 8)
    assert n["scanner_hits"] == 27
    assert {o["crop"] for o in ops} == {"chives", "sweet-corn", "broad-beans-fava", "watermelon", "tomatillo",
                                        "lavender", "basil", "oregano", "<catalog>"}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_canonical_bytes_stay_compact(pre, stage):
    post = P.apply_to(pre, stage[0])
    blob = P.serialize(post)
    assert not blob.endswith(b"\n") and b'": ' not in blob[:2000]


def test_empty_stage_refuses(tmp_path):
    (tmp_path / "ops.json").write_text("[]")
    with pytest.raises(Refused, match="the stage names no op"):
        P.load_stage(str(tmp_path))


def test_wrong_base_refuses(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="this promote is pinned to"):
        P.load_canonical(str(p))


# ---------------------------------------------------------------- guard V (base + post value)
def test_drifted_base_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "chives", "varieties.recommended[0].note")]["old"] = "something else"
    _refuses("the base value is not the op's `old`", pre, ops, ev, dec)


def test_noop_op_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "basil", "tips_by_stage.seedling[0].text_seasoned")
    ops[i]["new"] = ops[i]["old"]
    _refuses("a no-op", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard B (blast radius)
def test_stray_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    P.by_slug(post)["basil"]["failure_diagnostics"][2]["what_happened_beginner"] += " Extra."
    _refuses("basil: changed outside the staged ops", pre, ops, ev, dec, post)


def test_unstaged_crop_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    P.by_slug(post)["kale"]["description"] = "x"
    _refuses("kale: changed outside the staged ops", pre, ops, ev, dec, post)


def test_catalog_stray_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    post["source_catalog"]["clemson_hgic"]["accessed"] = "2099-01"
    _refuses("source_catalog changed outside the staged ops", pre, ops, ev, dec, post)


def test_roster_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    post["crops"].append(dict(P.by_slug(post)["kale"], slug="ghost-crop"))
    _refuses("the roster changed", pre, ops, ev, dec, post)


def test_top_level_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    post["ghost_key"] = 1
    _refuses("top-level keys changed", pre, ops, ev, dec, post)


def test_top_level_value_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    post["schema_version"] = "9.9"
    _refuses("top-level 'schema_version' changed", pre, ops, ev, dec, post)


def test_post_value_not_new_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    P.by_slug(post)["basil"]["tips_by_stage"]["seedling"][0]["text_seasoned"] = "Thin seedlings."
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


# ---------------------------------------------------------------- guard P (prose shape)
def test_em_dash_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "basil", "tips_by_stage.seedling[0].text_seasoned")]["new"] += " — always."
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_bare_degree_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "basil", "tips_by_stage.seedling[0].text_seasoned")]["new"] += " Keep above 50 degrees."
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_degree_f_passes_the_prose_check():
    P._prose_ok("highs only into the low 80s °F", "t")  # the fava string's form


# ---------------------------------------------------------------- guard R (append-only record)
def test_append_that_edits_the_original_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "verification_status.verification_log_ref")
    ops[i]["new"] = ops[i]["new"].replace("every value re-derived", "most values re-derived", 1)
    _refuses("must keep the original byte for byte", pre, ops, ev, dec)


def test_append_without_a_dated_correction_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "verification_status.verification_log_ref")
    ops[i]["new"] = ops[i]["old"] + " Re-anchored later."
    _refuses("not one dated", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard O (orthography-only)
def test_orthography_op_that_changes_more_than_spelling_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "weather_triggers[0].body_beginner")
    ops[i]["new"] = ops[i]["new"].replace("frost-tender", "frost-hardy", 1)
    _refuses("an orthography op may only apply", pre, ops, ev, dec)


def test_orthography_op_without_its_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if d["path"] != "weather_triggers[0].body_beginner"]
    _refuses("needs an orthography-only DECISIONS row", pre, ops, ev, dec)


def test_orthography_decision_says_claims_were_not_reviewed(stage):
    rows = [d for d in stage[2] if d["decision"] == "orthography-only"]
    assert len(rows) == 4 and all("NOT reviewed" in d["reason"] for d in rows)


def test_correction_allows_a_path_index_but_not_a_second_bracket():
    assert P.CORRECTION.fullmatch("[CORRECTION 2026-10-04: anchors on failure_diagnostics[5] dropped.]")
    assert not P.CORRECTION.fullmatch("[CORRECTION 2026-10-04: x [CORRECTION 2026-10-05: y]]")
    assert not P.CORRECTION.fullmatch("[CORRECTION 2026-10-04: see [note]]")


# ---------------------------------------------------------------- guard D (decisions)
def test_null_without_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if d["path"] != "days_to_maturity_mid"]
    _refuses("a null value needs a DECISIONS row", pre, ops, ev, dec)


def test_record_only_without_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if not (d["crop"] == "watermelon" and d["path"] == "soil_prep_beginner")]
    _refuses("no cited_at and no record-only DECISIONS row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E (evidence)
def test_prose_without_evidence_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev = [r for r in ev if r["entry_id"] != "tips_by_stage.seedling[0].text_seasoned"]
    _refuses("no EVIDENCE row", pre, ops, ev, dec)


def test_quote_not_in_bytes_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev[0]["quote"] = "a sentence that is on no page at all"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_uncited_url_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    r = next(r for r in ev if r["crop"] == "basil")
    r.update(crop="kale", entry_id=r["entry_id"])
    _refuses("not a staged prose / value / anchors op", pre, ops, ev, dec)


def test_url_not_cited_on_crop_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    r = next(r for r in ev if r["crop"] == "basil" and r["entry_id"] == "tips_by_stage.seedling[0].text_seasoned")
    corn = next(x for x in ev if x["crop"] == "sweet-corn" and x["source_id"] == "tamu_agrilife")
    r.update(url=corn["url"], sha256=corn["sha256"], quote=corn["quote"])
    _refuses("url is not cited anywhere on basil", pre, ops, ev, dec)


def test_row_source_missing_from_block_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "failure_diagnostics[5].anchoring_urls")
    del ops[i]["new"]["sdsu_ext"]
    _refuses(r"failure_diagnostics\[5\].anchoring_urls does not carry sdsu_ext", pre, ops, ev, dec)


def test_row_source_missing_from_sources_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "failure_diagnostics[5].sources")
    ops[i]["new"] = [s for s in ops[i]["new"] if s != "sdsu_ext"]
    _refuses(r"failure_diagnostics\[5\].sources does not name sdsu_ext", pre, ops, ev, dec)


def test_anchors_op_row_must_be_carried(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "tomatillo", "days_to_maturity_anchoring_urls")
    ops[i]["new"] = {"usu_ext": {"url": "https://extension.usu.edu/yardandgarden/research/tomatillos-in-the-garden",
                                 "verified": "2026-10-04"}}
    _refuses("days_to_maturity_anchoring_urls does not carry sdsu_ext", pre, ops, ev, dec)


def test_duplicate_row_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev.append(dict(ev[0]))
    _refuses("a duplicate row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A (anchors)
def test_unused_unkept_anchor_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if d["path"] != "failure_diagnostics[2].anchoring_urls.umass_ext"]
    _refuses("anchor umass_ext supports no evidenced leaf", pre, ops, ev, dec)


def test_sources_and_anchors_diverge_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "basil", "failure_diagnostics[2].sources")
    ops[i]["new"] = ops[i]["new"] + ["ghost_ext"]
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G (gates)
def test_gate_failure_refuses(pre, stage):
    ops, _ev, _dec = stage
    post = P.apply_to(pre, ops)
    P.by_slug(post)["basil"]["verification_status"]["status"] = "ghost_status"
    with pytest.raises(Refused, match="whole_crop_gate basil rc="):
        P.gate_post(post, {"basil"})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    post = P.apply_to(pre, stage[0])
    assert P.gate_post(post, {"basil", "chives"}) == 2
    # a gate that exits 0 without its verdict line (a stub, a crash swallowed upstream) is not a gated crop
    silent = lambda *a, **k: P.subprocess.CompletedProcess(a, 0, stdout="", stderr="")  # noqa: E731
    monkeypatch.setattr(P.subprocess, "run", silent)
    with pytest.raises(Refused, match="printed 0 PASS verdicts for 2 crops"):
        P.gate_post(post, {"basil", "chives"})
