"""Suite for promote_pla666_row_figures (PLA-666: row figures for raspberry and pawpaw; elderberry decision-only).

WRITTEN BEFORE THE PROMOTE (RED first, 2026-10-05). The pre-state is REPLAYED from its pinned commit
(promote_fixture.pre_state(afbd4113) -> 367c702), never read live, so the suite survives this promote landing.
POST_SHA (re-pinned after rulings A-E, then once more after rulings 1-2, 2026-10-05) was computed by an independent minimal apply (deepcopy, set each op's `new`, compact serialize) BEFORE the
promote existed, so the real-stage test is not a pin of the promote's own output.
One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts
the refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla666_row_figures as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"
POST_SHA = "350eda387fbed55464b16688a3bdc3263214b7c20631da98c7bbcb79f1d487c7"
ENTRY = "planting_layout[id=row-none]"


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


def _entry(crop):
    es = [e for e in crop["planting_layout"] if e["id"] == "row-none"]
    assert len(es) == 1
    return es[0]


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (49, 72, 58, 2)
    assert n["scanner_hits"] == 2          # both rewritten planting-notes leaves restate distances (evidenced)
    assert {o["crop"] for o in ops} == {"raspberry", "pawpaw", "<catalog>"}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_the_row_figures_and_their_mirrors(pre, stage):
    post = P.by_slug(P.apply_to(pre, stage[0]))
    for slug, rows in (("raspberry", [60, 120]), ("pawpaw", [144, 216])):
        c, e = post[slug], _entry(post[slug])
        assert (e["row_spacing_inches"], e["row_spacing_reason"]) == (rows, None)
        assert (c["row_spacing_inches"], c["row_spacing_reason"]) == (rows, None)
    assert _entry(post["raspberry"])["in_row_inches"] == [18, 24]
    assert _entry(post["pawpaw"])["in_row_inches"] == [96, 96]
    assert set(_entry(post["pawpaw"])["anchoring_urls"]) == {"ksu_pawpaw", "ksu_pawpaw_pbi004"}


def test_ruling_e_citation_blocks(pre, stage):
    ras = P.by_slug(P.apply_to(pre, stage[0]))["raspberry"]
    sm, gs0 = ras["start_method"], ras["growth_stages"][0]
    assert list(sm)[-2:] == ["anchoring_urls", "sources"]          # the fava key order
    assert sm["sources"] == ["umn_ext", "uada_ext_fsa6107"] and set(sm["anchoring_urls"]) == set(sm["sources"])
    assert gs0["sources"] == ["umn_ext", "psu_ext", "uada_ext_fsa6107"]
    assert set(gs0["anchoring_urls"]) == set(gs0["sources"])
    for leaf in ("notes_seasoned", "notes_beginner"):
        assert "1 to 2 inches" not in sm[leaf] and "late winter" not in sm[leaf] and "handle" not in sm[leaf]


def test_elderberry_is_decision_only(pre, stage):
    ops, _ev, dec = stage
    post = P.apply_to(pre, ops)
    assert P.by_slug(post)["elderberry"] == P.by_slug(pre)["elderberry"]
    assert _entry(P.by_slug(post)["elderberry"])["row_spacing_reason"] == "not_authored"
    assert [d["decision"] for d in dec if d["crop"] == "elderberry"] == ["not_authored after hunt"]


def test_canonical_bytes_stay_compact(pre, stage):
    blob = P.serialize(P.apply_to(pre, stage[0]))
    assert not blob.endswith(b"\n") and b'": ' not in blob[:2000]


def test_empty_stage_refuses(tmp_path):
    (tmp_path / "ops.json").write_text("[]")
    with pytest.raises(Refused, match="the stage names no op"):
        P.load_stage(str(tmp_path))


def test_unknown_kind_refuses(tmp_path, stage):
    ops = copy.deepcopy(stage[0])
    ops[0]["kind"] = "append"            # kinds this promote does not carry are refused, not silently applied
    (tmp_path / "ops.json").write_text(json.dumps(ops))
    with pytest.raises(Refused, match="unknown kind 'append'"):
        P.load_stage(str(tmp_path))


def test_wrong_base_refuses(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="this promote is pinned to"):
        P.load_canonical(str(p))


# ---------------------------------------------------------------- guard V (base + post value)
def test_drifted_base_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "raspberry", "planting_method_notes_seasoned")]["old"] = "something else"
    _refuses("the base value is not the op's `old`", pre, ops, ev, dec)


def test_noop_op_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "raspberry", "planting_method_notes_beginner")
    ops[i]["new"] = ops[i]["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_post_value_not_new_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    _entry(P.by_slug(post)["pawpaw"])["row_spacing_inches"] = [144, 240]
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


# ---------------------------------------------------------------- guard B (blast radius, sets first)
def test_stray_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    _entry(P.by_slug(post)["raspberry"])["in_row_inches"] = [18, 30]
    _refuses("raspberry: changed outside the staged ops", pre, ops, ev, dec, post)


def test_unstaged_crop_change_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    _entry(P.by_slug(post)["elderberry"])["row_spacing_inches"] = [120, 144]
    _refuses("elderberry: changed outside the staged ops", pre, ops, ev, dec, post)


def test_catalog_stray_refuses(pre, stage):
    ops, ev, dec = stage
    post = P.apply_to(pre, ops)
    post["source_catalog"]["ksu_pawpaw"]["accessed"] = "2099-01"
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


# ---------------------------------------------------------------- guard P (prose shape)
def test_em_dash_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "raspberry", "planting_method_notes_beginner")]["new"] += " Water well — always."
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_bare_degree_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "raspberry", "planting_method_notes_beginner")]["new"] += " Plant above 50 degrees."
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_degree_f_passes_the_prose_check():
    P._prose_ok("highs only into the low 80s °F", "t")


# ---------------------------------------------------------------- guard O (orthography-only, ruling 1 of 2026-10-05)
ORTHO_PATH = "regions.se_gulf.region_notes_seasoned"


def test_orthography_table_is_the_ruled_spelling():
    assert P.ORTHOGRAPHY == {"Dorman Red": "Dormanred"}


def test_orthography_op_that_changes_more_than_spelling_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "raspberry", ORTHO_PATH)
    ops[i]["new"] = ops[i]["new"].replace("heat-tolerant", "heat-loving", 1)
    _refuses("an orthography op may only apply", pre, ops, ev, dec)


def test_orthography_op_without_its_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if not (d["path"] == ORTHO_PATH and d["decision"] == "orthography-only")]
    _refuses("needs an orthography-only DECISIONS row", pre, ops, ev, dec)


def test_orthography_decisions_say_claims_were_not_reviewed(stage):
    ortho = [o for o in stage[0] if o["kind"] == "orthography"]
    rows = [d for d in stage[2] if d["decision"] == "orthography-only"]
    assert len(ortho) == 25 and len(rows) == 25 and all("NOT reviewed" in d["reason"] for d in rows)
    assert {(o["crop"], o["path"]) for o in ortho} == {(d["crop"], d["path"]) for d in rows}


def test_the_variety_name_key_is_left_alone(pre, stage):
    post = P.by_slug(P.apply_to(pre, stage[0]))["raspberry"]
    assert post["varieties"]["recommended"][12]["name"] == "Dorman Red"     # slug key: dorman-red (ruling 1)
    assert "Dorman Red" in post["regions"]["rgv"]["plantings_provenance"]  # a record, not display text


# ---------------------------------------------------------------- guard D (decisions)
def test_null_without_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if not (d["crop"] == "pawpaw" and d["path"] == "row_spacing_reason")]
    _refuses("a null value needs a DECISIONS row", pre, ops, ev, dec)


def test_record_only_without_decision_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if not (d["path"] == "planting_method_notes_beginner" and d["decision"] == "record-only")]
    _refuses("no cited_at and no record-only DECISIONS row", pre, ops, ev, dec)


def test_decision_on_a_crop_not_in_the_roster_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    next(d for d in dec if d["crop"] == "elderberry")["crop"] = "elderbery"
    _refuses("DECISIONS row names elderbery, which is not a crop", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E (evidence)
def test_prose_without_evidence_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev = [r for r in ev if r["entry_id"] != "planting_method_notes_beginner"]
    _refuses("no EVIDENCE row", pre, ops, ev, dec)


def test_value_without_evidence_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev = [r for r in ev if not (r["crop"] == "pawpaw" and r["entry_id"] == "row_spacing_inches")]
    _refuses("op 12 pawpaw row_spacing_inches: no EVIDENCE row", pre, ops, ev, dec)


def test_quote_not_in_bytes_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    next(r for r in ev if r["crop"] == "pawpaw")["quote"] = "rows 15 to 20 feet apart in a home garden"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_row_on_an_unstaged_path_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev[0]["entry_id"] = "cane_management_seasoned"
    _refuses("not a staged prose / value op", pre, ops, ev, dec)


def test_url_not_cited_on_crop_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    r = next(r for r in ev if r["crop"] == "raspberry" and r["entry_id"] == "planting_method_notes_seasoned")
    paw = next(x for x in ev if x["crop"] == "pawpaw")
    r.update(source_id=paw["source_id"], url=paw["url"], sha256=paw["sha256"], quote=paw["quote"])
    _refuses("url is not cited anywhere on raspberry", pre, ops, ev, dec)


def test_row_source_missing_from_block_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "raspberry", f"{ENTRY}.anchoring_urls")
    ops[i]["new"]["uada_ext_fsa6107"]["url"] = "https://www.uaex.uada.edu/publications/PDF/FSA-6108.pdf"
    _refuses(r"planting_layout\[id=row-none\].anchoring_urls does not carry uada_ext_fsa6107", pre, ops, ev, dec)


def test_row_source_missing_from_sources_refuses(pre, stage):
    # the pawpaw entry's sources op is dropped: its sources stay ["ksu_pawpaw"] while its row cites PBI-004
    ops, ev, dec = copy.deepcopy(stage)
    ops = [o for o in ops if not (o["crop"] == "pawpaw" and o["path"] == f"{ENTRY}.sources")]
    _refuses(r"planting_layout\[id=row-none\].sources does not name ksu_pawpaw_pbi004", pre, ops, ev, dec)


def test_duplicate_row_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ev.append(dict(ev[0]))
    _refuses("a duplicate row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A (anchors)
def test_unused_unkept_anchor_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    dec = [d for d in dec if d["path"] != f"{ENTRY}.anchoring_urls.ksu_pawpaw"]
    _refuses("anchor ksu_pawpaw supports no evidenced leaf", pre, ops, ev, dec)


def test_sources_and_anchors_diverge_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    i = _find(ops, "raspberry", f"{ENTRY}.sources")
    ops[i]["new"] = ops[i]["new"] + ["ghost_ext"]
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C (catalog mint)
def test_catalog_id_must_match_its_key(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "<catalog>", "ksu_pawpaw_pbi004")]["new"]["id"] = "ksu_pawpaw"
    _refuses("catalog ksu_pawpaw_pbi004: its id is 'ksu_pawpaw'", pre, ops, ev, dec)


def test_catalog_mint_must_be_evidenced_at_its_url(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops[_find(ops, "<catalog>", "ksu_pawpaw_pbi004")]["new"]["url"] = "https://www.kysu.edu/elsewhere.pdf"
    _refuses("catalog ksu_pawpaw_pbi004: no EVIDENCE row cites it at its url", pre, ops, ev, dec)


def test_catalog_mint_over_an_existing_id_refuses(pre, stage):
    ops, ev, dec = copy.deepcopy(stage)
    ops.append({"crop": "<catalog>", "path": "ksu_pawpaw", "kind": "catalog", "old": "<absent>", "new": {},
                "cited_at": None, "reason": "x"})
    _refuses("op 49 <catalog> ksu_pawpaw: the base value is not the op's `old`", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G (gates)
def test_gate_failure_refuses(pre, stage):
    post = P.apply_to(pre, stage[0])
    P.by_slug(post)["pawpaw"]["row_spacing_inches"] = [144, 240]   # mirror drift: A44 must fail the crop
    with pytest.raises(Refused, match="whole_crop_gate pawpaw rc="):
        P.gate_post(post, {"pawpaw"})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    post = P.apply_to(pre, stage[0])
    assert P.gate_post(post, {"raspberry", "pawpaw"}) == 2
    silent = lambda *a, **k: P.subprocess.CompletedProcess(a, 0, stdout="", stderr="")  # noqa: E731
    monkeypatch.setattr(P.subprocess, "run", silent)
    with pytest.raises(Refused, match="printed 0 PASS verdicts for 2 crops"):
        P.gate_post(post, {"raspberry", "pawpaw"})
