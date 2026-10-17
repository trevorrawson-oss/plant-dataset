"""Suite for promote_pla625_p2 (PLA-625 citrus/rootstock pass, promote 2: lemon + lime rootstock rows, the
recommended_rootstock note and its sources pair, three minted per-publication ids, promote 1's HS1260 re-key, one
non-blocking PLA-609 finding).

DEVIATION, recorded: the promote was derived from promote_pla625_p1 before this suite existed. Stand-ins: POST_SHA was
matched by an INDEPENDENT minimal apply (p2_texts.py written straight onto the base, no ops and no promote code) before
the canonical was written, and mutate_promote_pla625_p2.py switches every guard off in turn. The pre-state is REPLAYED
from its pinned commit (promote_fixture: 2f67359e -> 5603b28), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla625_p2 as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "2f67359ecdbdbd40203e6201a2b230e50bb21a2b84d2b01a4091a988087c8080"
POST_SHA = "ef1a4d351e4b26ea0369f5f3da824cb7c81ffcd4e3e1e2013b94b2413dcf6261"
LEM, LIM, OR, GF = "lemon", "lime", "orange-navel", "grapefruit"
R = "rootstock_options"
NOTE = "recommended_rootstock_note"
OF = "verification_status.open_findings"
ANR = "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf"
HS132 = "https://ask.ifas.ufl.edu/publication/HS132"


@pytest.fixture(scope="module")
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope="module")
def stage():
    return P.load_stage(P.STAGE)


def _c(stage):
    return tuple(copy.deepcopy(x) for x in stage)


def _check(pre, ops, ev, dec, post=None):
    P.check_pre(pre, ops)
    post = P.apply_to(pre, ops) if post is None else post
    return P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def _refuses(match, pre, ops, ev, dec, post=None):
    with pytest.raises(Refused, match=match):
        _check(pre, ops, ev, dec, post)


def _op(ops, crop, path):
    hits = [o for o in ops if o["crop"] == crop and o["path"] == path]
    assert len(hits) == 1, (crop, path)
    return hits[0]


def _retext(ops, ev, crop, path, old, new):
    o = _op(ops, crop, path)
    assert old in o["new"]
    o["new"] = o["new"].replace(old, new)
    for r in ev:
        if r["crop"] == crop and r["entry_id"] == path and old in r["value"]:
            r["value"] = r["value"].replace(old, new)


def _ev_row(ev, crop, path, sid):
    return next(r for r in ev if r["crop"] == crop and r["entry_id"] == path and r["source_id"] == sid)


def _add_cite(ops, ev, crop, blk, path, sid, url):
    """Cite `sid` at `url` on block `blk` of `crop`, with one evidence row on `path` copied from an existing row at that
    url (same bytes and quote, so the MANIFEST and quote checks hold)."""
    like = next(r for r in ev if r["url"] == url)
    _op(ops, crop, f"{blk}.sources")["new"].append(sid)
    _op(ops, crop, f"{blk}.anchoring_urls")["new"][sid] = {"url": url, "verified": "2026-10-16"}
    ev.append(dict(like, crop=crop, entry_id=path, source_id=sid, field="test row"))


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (61, 146, 50, 4)
    assert (n["register_pairs"], n["hill_inspected"], n["rekeyed"], n["minted"]) == (10, 224, 14, 3)
    assert (n["retained"], n["nulled"], n["new_rows"], n["findings_added"]) == (23, 16, 2, 1)
    assert {o["crop"] for o in ops} == {LEM, LIM, OR, GF, "<catalog>"}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_real_stage_values_and_sources(pre, stage):
    post = P.apply_to(pre, stage[0])
    q = P.by_slug(post)
    lem, lim = q[LEM][R], q[LIM][R]
    assert [r["name"] for r in lem] == P.ROWS[LEM] and [r["name"] for r in lim] == P.ROWS[LIM]
    vals = lambda r: (r["size_class"], r["mature_height_ft"], r["container_suitable"])  # noqa: E731
    assert [vals(r) for r in lem] == [(None, None, None), ("semi_dwarf", None, None), ("semi_dwarf", [8, 14], None),
                                      (None, None, None)]
    assert [vals(r) for r in lim] == [("standard", None, None), ("semi_dwarf", [8, 14], None), (None, None, None)]
    assert [r["sources"] for r in lem] == [
        ["uf_ifas_hs1153", "tamu_agrilife", "uf_ifas_hs1260", "uf_ifas_hs132"],
        ["tamu_agrilife", "uf_ifas_hs1153", "ucce_placer_nevada_31_018c"],
        ["ucr_citrus", "uf_ifas_hs1153", "uf_ifas_hs1260"],
        ["uf_ifas_hs1153", "uc_anr_8100"]]
    assert [r["sources"] for r in lim] == [
        ["uf_ifas_ch092", "uf_ifas_ch093", "uf_ifas_hs1153", "uf_ifas_hs1260"],
        ["uf_ifas_ch093", "ucr_citrus", "uf_ifas_hs1260"],
        ["uf_ifas_ch092", "uf_ifas_ch093", "uc_anr_8100"]]
    for r in lem[:2]:
        assert r["anchoring_urls"]["tamu_agrilife"]["url"] == \
            "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/"
    assert (q[LEM]["recommended_rootstock"], q[LIM]["recommended_rootstock"]) == (None, None)
    assert q[LEM]["recommended_rootstock_note_sources"] == ["uf_ifas_hs132", "uf_ifas_hs1153", "tamu_agrilife"]
    assert q[LIM]["recommended_rootstock_note_sources"] == ["uf_ifas_hs132", "uf_ifas_ch092", "uf_ifas_ch093"]
    for slug in (OR, GF):
        for r in q[slug][R]:
            assert "uf_ifas_edis" not in r["sources"] and "uf_ifas_hs1260" in r["sources"]
            assert r["anchoring_urls"]["uf_ifas_hs1260"]["url"] == "https://ask.ifas.ufl.edu/publication/HS1260"
    assert q[GF]["recommended_rootstock_note_sources"] == ["ucr_citrus", "uf_ifas_hs1260", "tamu_agrilife",
                                                           "uf_ifas_hs132", "az_coop_ext", "ucce_placer_nevada_31_018c"]
    for sid in P.MINTED:
        assert post["source_catalog"][sid]["title"] and post["source_catalog"][sid]["tier"] == "T1"
    added = [f["id"] for f in q[LEM]["verification_status"]["open_findings"]
             if f.get("filed_in_session") == "pla625_promote2_2026_10_16"]
    assert added == ["lemon_trifoliate_orange_rootstock_in_use_unread_pla609"]
    for slug in (LEM, LIM):
        vs = q[slug]["verification_status"]
        assert (vs["status"], vs["launch_ready_core"], vs["launch_ready_seasoned"]) == ("verified_gs_arc", True, True)


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["register_pairs"] == 10


# ---------------------------------------------------------------- loading / pre
def test_wrong_base(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="pinned to"):
        P.load_canonical(str(p))


def _stage_dir(tmp_path, ops):
    (tmp_path / "ops.json").write_text(json.dumps(ops), encoding="utf-8")
    return str(tmp_path)


def test_empty_stage(tmp_path):
    with pytest.raises(Refused, match="names no op"):
        P.load_stage(_stage_dir(tmp_path, []))


def test_op_keys_must_be_exact(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["x"] = 1
    with pytest.raises(Refused, match="keys must be exactly"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_unknown_kind(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "orthography"
    with pytest.raises(Refused, match="unknown kind"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_empty_reason(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["reason"] = ""
    with pytest.raises(Refused, match="empty reason"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_op_staged_twice(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]) * 2
    with pytest.raises(Refused, match="staged twice"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_drifted_base(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[0].traits_seasoned")["old"] = "something else"
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, NOTE)["crop"] = "ghost-crop"
    with pytest.raises(Refused, match="is not a crop"):
        P.check_pre(pre, ops)


def test_a_new_row_must_append(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LIM, f"{R}[2]"); o["path"] = f"{R}[5]"
    with pytest.raises(Refused, match="must be appended at index"):
        P.apply_to(pre, ops)


# ---------------------------------------------------------------- guard B
def test_roster_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["crops"] = post["crops"][:-1]
    _refuses("roster changed", pre, ops, ev, dec, post)


def test_top_level_key_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["ghost"] = 1
    _refuses("top-level keys changed", pre, ops, ev, dec, post)


def test_top_level_value_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["glossary"] = {}
    _refuses("top-level 'glossary' changed", pre, ops, ev, dec, post)


def test_crop_key_added(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)["mandarin-clementine"]["ghost_key"] = None
    _refuses("mandarin-clementine: top-level crop keys changed", pre, ops, ev, dec, post)


def test_stray_crop_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)["mandarin-clementine"][NOTE] = "x"
    _refuses("mandarin-clementine: changed outside the staged ops", pre, ops, ev, dec, post)


def test_launch_flag_is_a_stray_change(pre, stage):
    """lemon is launch-ready and stays so: a flag moving is B's refusal, never an op path."""
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[LEM]["verification_status"]["launch_ready_core"] = False
    _refuses("lemon: changed outside the staged ops", pre, ops, ev, dec, post)


def test_a_stray_edit_on_an_unstaged_row_leaf(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[GF][R][1]["traits_beginner"] = "x"
    _refuses(r"grapefruit: changed outside the staged ops: \['rootstock_options\[1\]\.traits_beginner'\]",
             pre, ops, ev, dec, post)


def test_an_unstaged_added_row(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[OR][R].append({"name": "Ghost"})
    _refuses(r"orange-navel: changed outside the staged ops: \['rootstock_options\[3\]'\]", pre, ops, ev, dec, post)


def test_a_lost_row(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)["mandarin-clementine"][R].pop()
    _refuses("mandarin-clementine: rootstock_options lost a row", pre, ops, ev, dec, post)


def test_catalog_stray(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["source_catalog"]["ucr_citrus"]["name"] = "x"
    _refuses("source_catalog changed outside", pre, ops, ev, dec, post)


def test_catalog_lost_id(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); del post["source_catalog"]["uf_ifas_edis"]
    _refuses("source_catalog lost ids", pre, ops, ev, dec, post)


# ---------------------------------------------------------------- guard S
def test_path_outside_the_ruled_scope(pre, stage):
    """container_notes belongs to promote 4."""
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)[LEM]["container_notes"]
    ops.append({"crop": LEM, "path": "container_notes.notes_seasoned", "kind": "prose", "old": c["notes_seasoned"],
                "new": c["notes_seasoned"] + " More.", "cited_at": "container_notes", "reason": "t"})
    _refuses("container_notes.notes_seasoned: outside the ruled scope", pre, ops, ev, dec)


def test_crop_outside_the_ruled_scope(pre, stage):
    ops, ev, dec = _c(stage)
    m = P.by_slug(pre)["mandarin-clementine"]
    ops.append({"crop": "mandarin-clementine", "path": NOTE, "kind": "prose", "old": m[NOTE], "new": m[NOTE] + " More.",
                "cited_at": NOTE, "reason": "t"})
    _refuses("mandarin-clementine is outside this promote's scope", pre, ops, ev, dec)


def test_a_rekey_crop_takes_rekeys_only(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{R}[0].sources")["kind"] = "sources"
    _refuses("orange-navel / grapefruit take re-keys only", pre, ops, ev, dec)


def test_a_rekey_crop_scope(pre, stage):
    ops, ev, dec = _c(stage)
    o = P.by_slug(pre)[OR]
    ops.append({"crop": OR, "path": NOTE, "kind": "rekey", "old": o[NOTE], "new": o[NOTE] + " x", "cited_at": NOTE,
                "reason": "t"})
    _refuses("orange-navel recommended_rootstock_note: outside the ruled scope", pre, ops, ev, dec)


def test_a_catalog_op_must_name_the_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, NOTE)["kind"] = "catalog"
    _refuses("a catalog op must name <catalog>", pre, ops, ev, dec)


def test_a_ruled_crop_with_no_op(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["crop"] != LIM]
    ev = [r for r in ev if r["crop"] != LIM]
    dec = [d for d in dec if d["crop"] != LIM]
    _refuses("lime: rootstock_options rows are not", pre, ops, ev, dec)


def test_a_ruled_crop_with_no_op_but_the_right_rows(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["crop"] != LIM]
    ev = [r for r in ev if r["crop"] != LIM]
    dec = [d for d in dec if d["crop"] != LIM]
    monkeypatch.setitem(P.ROWS, LIM, [r["name"] for r in P.by_slug(pre)[LIM][R]])
    _refuses("lime: the stage names no op on a ruled crop", pre, ops, ev, dec)


def test_rows_must_be_the_ruled_list(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[2]")["new"]["name"] = "Alemow"
    _refuses("lime: rootstock_options rows are not", pre, ops, ev, dec)


def test_catalog_ops_are_exactly_the_ruled_ids(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["path"] != "uf_ifas_ch092"]
    _refuses("catalog ops are not exactly the ruled ids", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard V + P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    _op(ops, LEM, f"{R}[0].traits_seasoned")["new"] = "Not what was written."
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LIM, f"{R}[1].size_class"); o["new"] = o["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_em_dash(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, LEM, f"{R}[1].traits_beginner", "somewhat smaller.", "somewhat smaller — usually.")
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_cultivar(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, LIM, NOTE, "Match the rootstock to your soil.", "Match the rootstock to your cultivar.")
    _refuses("'cultivar' in consumer copy", pre, ops, ev, dec)


def test_bare_degree(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, LIM, f"{R}[1].traits_seasoned", "It resists Phytophthora foot rot.",
            "It resists Phytophthora foot rot to 20 degrees.")
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_null_prose(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[0].what_to_ask_nursery")["new"] = None
    _refuses("prose must be a non-empty string", pre, ops, ev, dec)


def test_a_new_rows_prose_is_checked(pre, stage):
    ops, ev, dec = _c(stage)
    r = _op(ops, LIM, f"{R}[2]")["new"]; r["traits_beginner"] = r["traits_beginner"].replace(", and it", " — and it")
    _refuses(r"rootstock_options\[2\]\.traits_beginner: an em or en dash", pre, ops, ev, dec)


def test_a_new_row_carries_exactly_the_row_fields(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[3]")["new"]["ghost"] = None
    _refuses("a new row must carry exactly", pre, ops, ev, dec)




# ---------------------------------------------------------------- guard D (+ retained)
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("DECISIONS row names ghost-crop", pre, ops, ev, dec)


def test_prose_without_cited_at(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, NOTE)["cited_at"] = None
    _refuses("no cited_at and no record-only DECISIONS row", pre, ops, ev, dec)


def test_rename_without_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if d["decision"] != "renamed"]
    _refuses("a rename with no `renamed` DECISIONS row", pre, ops, ev, dec)


def test_retained_on_a_non_crop(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "<roster>", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("retained <roster> x: not a crop", pre, ops, ev, dec)


def test_retained_is_also_an_op(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": LIM, "path": f"{R}[1].size_class", "decision": "retained", "reason": "t"})
    _refuses("also staged as an op", pre, ops, ev, dec)


def test_retained_value_moved(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": LIM, "path": f"{R}[1].anchoring_urls.ucr_citrus", "decision": "retained", "reason": "t"})
    _refuses("the value moved", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard N
def test_nulled_without_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == LEM and d["path"] == "recommended_rootstock")]
    _refuses("recommended_rootstock: nulled with no `nulled` DECISIONS row", pre, ops, ev, dec)


def test_a_new_rows_value_must_be_null(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[2]")["new"]["size_class"] = "standard"
    _refuses("a new row's value must be null", pre, ops, ev, dec)


def test_a_new_rows_null_needs_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == LEM and d["path"] == f"{R}[3].spread_ft")]
    _refuses(r"rootstock_options\[3\]\.spread_ft: a new row's null with no `new-null`", pre, ops, ev, dec)


def test_evidence_for_a_nulled_value(pre, stage):
    ops, ev, dec = _c(stage)
    row = dict(_ev_row(ev, LEM, f"{R}[2].size_class", "uf_ifas_hs1260"))
    row.update(entry_id=f"{R}[0].size_class", value="null")
    ev.append(row)
    _refuses("evidence for a value nulled by the ruling", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("a duplicate row", pre, ops, ev, dec)


def test_row_on_an_unstaged_path(pre, stage):
    ops, ev, dec = _c(stage)
    row = dict(ev[0]); row["entry_id"] = "container_notes.notes_seasoned"
    ev.append(row)
    _refuses("not a staged prose / value op, a new row's prose or a retained leaf", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    _ev_row(ev, LIM, NOTE, "uf_ifas_ch093")["quote"] = "swingle is the best rootstock for every lime anywhere"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_url_not_cited_on_crop(pre, stage):
    ops, ev, dec = _c(stage)
    r = _ev_row(ev, LIM, f"{R}[1].traits_seasoned", "ucr_citrus")
    r["url"] = "https://citrusvariety.ucr.edu/crc2863"
    r["sha256"] = "651bd22c46ba74e1630d3a0e4479d7602aa557d9b55edbf46f0e7fac040e88cb"
    r["quote"] = "a cross of washington navel and trifoliate orange"
    _refuses("url is not cited anywhere on lime", pre, ops, ev, dec)


def test_one_url_per_source_id_per_block(pre, stage):
    """An evidence row at a url the crop cites ELSEWHERE (HS132, on lime's note) but not under its own block's anchor
    for that id is refused: the block's anchors are the only url an id may carry there."""
    ops, ev, dec = _c(stage)
    like = _ev_row(ev, LIM, NOTE, "uf_ifas_hs132")
    ev.append(dict(like, entry_id=f"{R}[1].traits_seasoned", field="test row"))
    _refuses(r"rootstock_options\[1\] anchors do not carry uf_ifas_hs132 at the row's url", pre, ops, ev, dec)


def test_cited_at_names_no_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[0].traits_seasoned")["cited_at"] = f"{R}[9]"
    _refuses("names no citation block", pre, ops, ev, dec)


def test_block_sources_missing(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LIM, f"{R}[1].sources"); o["new"].remove("ucr_citrus")
    _refuses("sources do not name ucr_citrus", pre, ops, ev, dec)


def test_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == LEM and r["entry_id"] == f"{R}[1].what_to_ask_nursery")]
    _refuses("what_to_ask_nursery: no EVIDENCE row", pre, ops, ev, dec)


def test_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == LIM and r["entry_id"] == f"{R}[1].mature_height_ft")]
    _refuses("mature_height_ft: no EVIDENCE row", pre, ops, ev, dec)


def test_a_new_rows_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == LIM and r["entry_id"] == f"{R}[2].traits_beginner")]
    _refuses(r"new row lime rootstock_options\[2\]\.traits_beginner: no EVIDENCE row", pre, ops, ev, dec)


def test_retained_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == LIM and r["entry_id"] == f"{R}[0].size_class")]
    _refuses("a non-null retained value with no EVIDENCE row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A
def test_unused_unkept_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[1].sources")["new"].append("uc_anr_8100")
    _op(ops, LIM, f"{R}[1].anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-16"}
    _refuses("anchor uc_anr_8100 supports no evidenced leaf", pre, ops, ev, dec)


def test_a_new_rows_unused_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    r = _op(ops, LEM, f"{R}[3]")["new"]
    r["sources"].append("uf_ifas_hs132"); r["anchoring_urls"]["uf_ifas_hs132"] = {"url": HS132, "verified": "x"}
    _refuses(r"lemon rootstock_options\[3\]: anchor uf_ifas_hs132 supports no evidenced leaf", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_unused_anchor(pre, stage):
    """Positive control for the test above: with a `kept` row the same anchor passes all of check_post."""
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[1].sources")["new"].append("uc_anr_8100")
    _op(ops, LIM, f"{R}[1].anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-16"}
    dec.append({"crop": LIM, "path": f"{R}[1].anchoring_urls.uc_anr_8100", "decision": "kept", "reason": "t"})
    assert _check(pre, ops, ev, dec)["rekeyed"] == 14


def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[1].sources")["new"].append("uc_anr_8100")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


def test_a_source_listed_twice(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, f"{R}[1].sources")["new"].append("ucr_citrus")
    _refuses("a source id listed twice", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard K
def test_record_without_a_record_only_row(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == LEM and d["path"] == OF)]
    _refuses("open_findings: no record-only DECISIONS row", pre, ops, ev, dec)


def test_findings_are_append_only(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LEM, OF); o["new"] = o["new"][1:]
    _refuses("not the base list plus appended entries", pre, ops, ev, dec)


def test_a_finding_id_twice(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LEM, OF); o["new"] = o["new"] + [dict(o["new"][-1])]
    _refuses("a finding id twice", pre, ops, ev, dec)


def test_an_appended_finding_must_not_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, OF)["new"][-1]["blocks_launch"] = True
    _refuses("must be open with blocks_launch false", pre, ops, ev, dec)


def test_a_dash_in_a_finding(pre, stage):
    ops, ev, dec = _c(stage)
    f = _op(ops, LEM, OF)["new"][-1]; f["summary"] = f["summary"].replace(". HS402", " — HS402")
    _refuses("a dash in the summary", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def _cat(ops, sid):
    return _op(ops, "<catalog>", sid)




def test_a_minted_ids_id_is_its_path(pre, stage):
    ops, ev, dec = _c(stage)
    _cat(ops, "uf_ifas_ch093")["new"]["id"] = "uf_ifas_ch99"
    _refuses("catalog uf_ifas_ch093: its id is 'uf_ifas_ch99'", pre, ops, ev, dec)


def test_a_minted_id_must_be_titled(pre, stage):
    ops, ev, dec = _c(stage)
    _cat(ops, "uf_ifas_hs1260")["new"]["title"] = " "
    _refuses("must be document-scoped and titled", pre, ops, ev, dec)


def test_a_minted_id_must_be_document_scoped(pre, stage):
    ops, ev, dec = _c(stage)
    _cat(ops, "uf_ifas_hs1260")["new"]["url"] = "https://ask.ifas.ufl.edu"
    _refuses("must be document-scoped and titled", pre, ops, ev, dec)


def test_a_minted_id_must_be_t1(pre, stage):
    ops, ev, dec = _c(stage)
    _cat(ops, "uf_ifas_ch092")["new"]["tier"] = "T2"
    _refuses("a minted id must be T1", pre, ops, ev, dec)


def test_a_minted_id_must_be_evidenced_at_its_url(pre, stage):
    ops, ev, dec = _c(stage)
    _cat(ops, "uf_ifas_ch092")["new"]["url"] = "https://ask.ifas.ufl.edu/publication/CH099"
    _refuses("catalog uf_ifas_ch092: no EVIDENCE row cites it at its url", pre, ops, ev, dec)


def test_cited_id_must_be_in_the_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, LIM, f"{R}[1]", f"{R}[1].traits_seasoned", "ghost_id", ANR)
    _refuses("EVIDENCE cites ghost_id, which is not in source_catalog", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard R
def test_seasoned_without_its_beginner(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == LIM and o["path"] == f"{R}[1].traits_beginner")]
    ev = [r for r in ev if not (r["crop"] == LIM and r["entry_id"] == f"{R}[1].traits_beginner")]
    _refuses("without its beginner sibling", pre, ops, ev, dec)


def test_byte_identical_registers(pre, stage):
    ops, ev, dec = _c(stage)
    s, b = _op(ops, LEM, f"{R}[0].traits_seasoned"), _op(ops, LEM, f"{R}[0].traits_beginner")
    b["new"] = s["new"]
    ev = [r for r in ev if not (r["crop"] == LEM and r["entry_id"] == f"{R}[0].traits_beginner")]
    for r in [x for x in ev if x["crop"] == LEM and x["entry_id"] == f"{R}[0].traits_seasoned"]:
        ev.append(dict(r, entry_id=f"{R}[0].traits_beginner"))
    _refuses("byte-identical", pre, ops, ev, dec)


def test_a_new_rows_registers_byte_identical(pre, stage):
    ops, ev, dec = _c(stage)
    r = _op(ops, LIM, f"{R}[2]")["new"]; r["traits_beginner"] = r["traits_seasoned"]
    ev = [x for x in ev if not (x["crop"] == LIM and x["entry_id"] == f"{R}[2].traits_beginner")]
    for x in [y for y in ev if y["crop"] == LIM and y["entry_id"] == f"{R}[2].traits_seasoned"]:
        ev.append(dict(x, entry_id=f"{R}[2].traits_beginner"))
    _refuses("a new row's registers are byte-identical", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard X
def test_a_rekey_that_moves_a_url(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{R}[1].anchoring_urls")["new"]["uf_ifas_hs1260"]["url"] = "https://ask.ifas.ufl.edu/publication/X"
    _refuses(r"orange-navel rootstock_options\[1\]\.anchoring_urls: not a mechanical", pre, ops, ev, dec)


def test_a_rekey_that_reorders(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, GF, "recommended_rootstock_note_sources"); o["new"] = list(reversed(o["new"]))
    _refuses("recommended_rootstock_note_sources: not a mechanical", pre, ops, ev, dec)


def test_a_rekey_that_drops_an_id(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, GF, f"{R}[0].sources"); o["new"].remove("tamu_agrilife")
    _refuses(r"grapefruit rootstock_options\[0\]\.sources: not a mechanical", pre, ops, ev, dec)




# ---------------------------------------------------------------- guard H
def test_hs132_kept_on_a_row_without_the_retail_claim(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, LIM, f"{R}[1]", f"{R}[1].traits_seasoned", "uf_ifas_hs132", HS132)
    _refuses("Swingle citrumelo \\(trifoliate hybrid\\): uf_ifas_hs132 kept", pre, ops, ev, dec)


def test_hs132_dropped_from_the_retail_row(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[0].sources")["new"].remove("uf_ifas_hs132")
    del _op(ops, LEM, f"{R}[0].anchoring_urls")["new"]["uf_ifas_hs132"]
    ev = [r for r in ev if not (r["crop"] == LEM and r["entry_id"].startswith(f"{R}[0].")
                                and r["source_id"] == "uf_ifas_hs132")]
    _refuses("sour orange \\(Citrus aurantium\\): uf_ifas_hs132 dropped", pre, ops, ev, dec)


def test_a_bare_host_anchor_on_a_lemon_row(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LEM, f"{R}[1].anchoring_urls")["new"]["ghost_host"] = {"url": "https://agrilifeextension.tamu.edu"}
    _op(ops, LEM, f"{R}[1].sources")["new"].append("ghost_host")
    dec.append({"crop": LEM, "path": f"{R}[1].anchoring_urls.ghost_host", "decision": "kept", "reason": "t"})
    _refuses("anchors the bare host https://agrilifeextension.tamu.edu", pre, ops, ev, dec)


def test_a_retired_id_on_a_lime_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LIM, "recommended_rootstock_note_sources")["new"].append("ufifas_ext")
    _op(ops, LIM, "recommended_rootstock_note_anchoring_urls")["new"]["ufifas_ext"] = {
        "url": "https://ask.ifas.ufl.edu/publication/CH093", "verified": "2026-10-16"}
    dec.append({"crop": LIM, "path": f"{NOTE}.anchoring_urls.ufifas_ext", "decision": "kept", "reason": "t"})
    _refuses(r"lime: a rootstock block still cites \['ufifas_ext'\]", pre, ops, ev, dec)


def test_a_rekey_left_undone(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == GF and o["path"].startswith("recommended_rootstock_note_"))]
    _refuses("grapefruit: a rootstock block still cites uf_ifas_edis", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, LIM, NOTE, "Match the rootstock to your soil.", "Match the rootstock to your soil; hill soil up.")
    _refuses("glossary match on the post roster", pre, ops, ev, dec)


def test_match_population_pinned(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "HILL_POPULATION", 223)
    _refuses("inspected 224 consumer leaves, not 223", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G
class _R:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_gate_failure(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(1, "GATE: 1 VIOLATION(S)"))
    with pytest.raises(Refused, match="whole_crop_gate .* rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {LEM})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {LEM})


def test_gate_all_failure(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {LEM})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {LEM})


def test_check_pre_refuses_minting_an_existing_id(pre, stage):
    """Guard C's 'mint only if none exists' (ruling A.1) is check_pre's: a catalog op's `old` must be the base value."""
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch092")["path"] = "uf_ifas_hs132"
    with pytest.raises(Refused, match="uf_ifas_hs132: the base value is not the op's `old`"):
        P.check_pre(pre, ops)
