"""Suite for promote_pla625_p1 (PLA-625 citrus/rootstock pass, promote 1: orange-navel + grapefruit rootstock rows, the
recommended_rootstock note and its sources pair, three non-blocking PLA-612 findings).

DEVIATION, recorded: the promote was derived from promote_pla673_d before this suite existed. Stand-ins: POST_SHA was
matched by an INDEPENDENT minimal apply (p1_texts.py written straight onto the base, no ops and no promote code) before
the canonical was written, and mutate_promote_pla625_p1.py switches every guard off in turn. The pre-state is REPLAYED
from its pinned commit (promote_fixture: 59010fe6 -> 8b7d93e), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla625_p1 as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "59010fe6994b95eb52407fa60a6995eedefe5636bd6a52d2f960d4b08641cf68"
POST_SHA = "2f67359ecdbdbd40203e6201a2b230e50bb21a2b84d2b01a4091a988087c8080"
OR, GF = "orange-navel", "grapefruit"
CAR = "rootstock_options[name=Carrizo citrange]"
SW = "rootstock_options[name=Swingle citrumelo]"
FD = "rootstock_options[name=Flying Dragon trifoliate]"
NOTE = "recommended_rootstock_note"
OF = "verification_status.open_findings"
ANR = "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf"


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


def _add_cite(ops, ev, blk, path, sid, url):
    """Cite `sid` at `url` on block `blk` of BOTH crops (they are ruled identical), with one evidence row on `path`
    copied from an existing row at that url (same bytes and quote, so the MANIFEST and quote checks hold)."""
    like = next(r for r in ev if r["url"] == url)
    for crop in (OR, GF):
        _op(ops, crop, f"{blk}.sources")["new"].append(sid)
        _op(ops, crop, f"{blk}.anchoring_urls")["new"][sid] = {"url": url, "verified": "2026-10-13"}
        ev.append(dict(like, crop=crop, entry_id=path, source_id=sid, field="test row"))


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (57, 246, 44, 2)
    assert (n["register_pairs"], n["hill_inspected"], n["identical"]) == (12, 224, 29)
    assert (n["retained"], n["nulled"], n["findings_added"]) == (19, 13, 3)
    assert {o["crop"] for o in ops} == {OR, GF}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_real_stage_values_and_sources(pre, stage):
    post = P.by_slug(P.apply_to(pre, stage[0]))
    for crop in (OR, GF):
        rows = {r["name"]: r for r in post[crop]["rootstock_options"]}
        c, s, f = rows["Carrizo citrange"], rows["Swingle citrumelo"], rows["Flying Dragon trifoliate"]
        assert (c["size_class"], c["mature_height_ft"], c["spread_ft"], c["container_suitable"]) == \
            ("standard", None, None, None)
        assert (s["size_class"], s["mature_height_ft"], s["spread_ft"], s["container_suitable"]) == \
            ("semi_dwarf", [8, 14], None, None)
        assert (f["size_class"], f["mature_height_ft"], f["spread_ft"], f["container_suitable"]) == \
            ("dwarf", [4, 8], None, True)
        assert {r["bearing_age_years"] for r in rows.values()} == {3}
        assert c["sources"] == ["ucr_citrus", "uf_ifas_edis", "uc_anr_8100", "ucce_placer_nevada_31_018c",
                                "az_coop_ext", "tamu_agrilife"]
        assert c["anchoring_urls"]["ucr_citrus"]["url"] == "https://citrusvariety.ucr.edu/crc2863"
        assert s["sources"] == ["ucr_citrus", "uf_ifas_edis", "tamu_agrilife"]
        assert s["anchoring_urls"]["ucr_citrus"]["url"] == "https://citrusvariety.ucr.edu/crc3771"
        assert f["sources"] == ["ucce_placer_nevada_31_018c", "ucanr_santa_clara_mg", "uf_ifas_edis", "tamu_agrilife"]
    assert post[OR]["recommended_rootstock"] is None
    assert post[GF]["recommended_rootstock"] == "Swingle citrumelo"
    assert post[OR]["recommended_rootstock_note_sources"] == ["uf_ifas_hs132", "az_coop_ext",
                                                              "ucce_placer_nevada_31_018c"]
    assert post[GF]["recommended_rootstock_note_sources"] == ["ucr_citrus", "uf_ifas_edis", "tamu_agrilife",
                                                              "uf_ifas_hs132", "az_coop_ext",
                                                              "ucce_placer_nevada_31_018c"]
    assert "sour orange" not in post[GF][NOTE].lower()
    added = {c: [f["id"] for f in post[c]["verification_status"]["open_findings"]
                 if f.get("filed_in_session") == "pla625_promote1_2026_10_13"] for c in (OR, GF)}
    assert added == {OR: ["orange-navel_swingle_scion_pairing_unread_pla612"],
                     GF: ["grapefruit_carrizo_scion_pairing_unread_pla612",
                          "grapefruit_flying_dragon_scion_pairing_unread_pla612"]}
    for c in (OR, GF):
        vs = post[c]["verification_status"]
        assert (vs["launch_ready_core"], vs["launch_ready_seasoned"]) == (False, False)


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["register_pairs"] == 12


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
    _op(ops, OR, f"{CAR}.traits_seasoned")["old"] = "something else"
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    ops[0]["crop"] = "ghost-crop"
    with pytest.raises(Refused, match="is not a crop"):
        P.check_pre(pre, ops)


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
    post = P.apply_to(pre, ops); P.by_slug(post)["lemon"]["ghost_key"] = None
    _refuses("lemon: top-level crop keys changed", pre, ops, ev, dec, post)


def test_stray_crop_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)["lemon"]["recommended_rootstock_note"] = "x"
    _refuses("lemon: changed outside the staged ops", pre, ops, ev, dec, post)


def test_launch_flag_is_a_stray_change(pre, stage):
    """A launch flag or status moving is B's refusal: neither is an op path (ruling F: both stay false)."""
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[GF]["verification_status"]["launch_ready_core"] = True
    _refuses("grapefruit: changed outside the staged ops", pre, ops, ev, dec, post)


def test_catalog_stray(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    cat = post["source_catalog"]
    (cat["ucr_citrus"] if isinstance(cat, dict) else next(e for e in cat if e["id"] == "ucr_citrus"))["name"] = "x"
    _refuses("source_catalog changed outside", pre, ops, ev, dec, post)


# ---------------------------------------------------------------- guard S
def test_path_outside_the_ruled_scope(pre, stage):
    """container_notes belongs to promote 4 (ruling B)."""
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)[OR]["container_notes"]
    ops.append({"crop": OR, "path": "container_notes.notes_seasoned", "kind": "prose", "old": c["notes_seasoned"],
                "new": c["notes_seasoned"] + " More.", "cited_at": "container_notes", "reason": "t"})
    _refuses("container_notes.notes_seasoned: outside the ruled scope", pre, ops, ev, dec)


def test_crop_outside_the_ruled_two(pre, stage):
    ops, ev, dec = _c(stage)
    lem = P.by_slug(pre)["lemon"]
    ops.append({"crop": "lemon", "path": NOTE, "kind": "prose", "old": lem[NOTE], "new": lem[NOTE] + " More.",
                "cited_at": NOTE, "reason": "t"})
    _refuses("lemon is outside this promote's two crops", pre, ops, ev, dec)


def test_a_ruled_crop_with_no_op(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["crop"] != GF]
    ev = [r for r in ev if r["crop"] != GF]
    dec = [d for d in dec if d["crop"] != GF]
    _refuses("grapefruit: the stage names no op on a ruled crop", pre, ops, ev, dec)


def test_rows_must_be_the_ruled_three(pre, stage):
    ops, ev, dec = _c(stage)
    pre2 = copy.deepcopy(pre)
    r = P.by_slug(pre2)[OR]["rootstock_options"]
    r[0], r[1] = r[1], r[0]
    _refuses("orange-navel: rootstock_options rows are not", pre2, ops, ev, dec)


# ---------------------------------------------------------------- guard V + P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    _op(ops, OR, f"{CAR}.traits_seasoned")["new"] = "Not what was written."
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, OR, f"{SW}.size_class"); o["new"] = o["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_em_dash(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, OR, f"{FD}.traits_beginner", "small, usually", "small — usually")
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_cultivar(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, GF, NOTE, "adapted to grapefruit.", "adapted to grapefruit cultivars.")
    _refuses("'cultivar' in consumer copy", pre, ops, ev, dec)


def test_bare_degree(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, OR, f"{SW}.traits_seasoned", "Its cold hardiness is good.",
            "Its cold hardiness is good to 20 degrees.")
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_null_prose(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{CAR}.what_to_ask_nursery")["new"] = None
    _refuses("prose must be a non-empty string", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard D (+ retained)
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("DECISIONS row names ghost-crop", pre, ops, ev, dec)


def test_prose_without_cited_at(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, NOTE)["cited_at"] = None
    _refuses("no cited_at and no record-only DECISIONS row", pre, ops, ev, dec)


def test_retained_on_a_non_crop(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "<roster>", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("retained <roster> x: not a crop", pre, ops, ev, dec)


def test_retained_is_also_an_op(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": OR, "path": f"{SW}.size_class", "decision": "retained", "reason": "t"})
    _refuses("also staged as an op", pre, ops, ev, dec)


def test_retained_value_moved(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": OR, "path": f"{SW}.anchoring_urls.uf_ifas_edis", "decision": "retained", "reason": "t"})
    _refuses("the value moved", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard N
def test_nulled_without_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == OR and d["path"] == "recommended_rootstock")]
    _refuses("recommended_rootstock: nulled with no `nulled` DECISIONS row", pre, ops, ev, dec)


def test_evidence_for_a_nulled_value(pre, stage):
    ops, ev, dec = _c(stage)
    row = dict(_ev_row(ev, OR, f"{CAR}.size_class", "uf_ifas_edis"))
    row.update(entry_id=f"{CAR}.mature_height_ft", value="null")
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
    _refuses("not a staged prose / value op or a retained leaf", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    _ev_row(ev, GF, NOTE, "ucr_citrus")["quote"] = "swingle is the best rootstock for every citrus anywhere"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_url_not_cited_on_crop(pre, stage):
    ops, ev, dec = _c(stage)
    r = _ev_row(ev, OR, f"{SW}.traits_seasoned", "ucr_citrus")
    r["url"] = "https://citrusvariety.ucr.edu/crc2863"; r["sha256"] = "651bd22c46ba74e1630d3a0e4479d7602aa557d9b55edbf46f0e7fac040e88cb"
    r["quote"] = "a cross of washington navel and trifoliate orange"
    ops2 = [o for o in ops if not (o["crop"] == OR and o["path"].startswith(CAR))]
    ev2 = [x for x in ev if not (x["crop"] == OR and x["entry_id"].startswith(CAR))]
    _refuses("url is not cited anywhere on orange-navel", pre, ops2, ev2, dec)


def test_one_url_per_source_id_per_block(pre, stage):
    """Ruling C: a second HS132 url (the edis host, same bytes, cited elsewhere on orange-navel) under the note's
    uf_ifas_hs132 is refused, because the note's anchor names ask.ifas."""
    ops, ev, dec = _c(stage)
    r = _ev_row(ev, OR, NOTE, "uf_ifas_hs132")
    r["url"] = "https://edis.ifas.ufl.edu/publication/HS132"
    _refuses("anchors do not carry uf_ifas_hs132 at the row's url", pre, ops, ev, dec)


def test_cited_at_names_no_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{CAR}.traits_seasoned")["cited_at"] = "rootstock_options[name=Ghost]"
    _refuses("names no citation block", pre, ops, ev, dec)


def test_block_sources_missing(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{SW}.sources")["new"].remove("tamu_agrilife")
    _refuses("sources do not name tamu_agrilife", pre, ops, ev, dec)


def test_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == GF and r["entry_id"] == f"{FD}.what_to_ask_nursery")]
    _refuses("what_to_ask_nursery: no EVIDENCE row", pre, ops, ev, dec)


def test_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == OR and r["entry_id"] == f"{FD}.mature_height_ft")]
    _refuses("mature_height_ft: no EVIDENCE row", pre, ops, ev, dec)


def test_retained_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == GF and r["entry_id"] == "recommended_rootstock")]
    _refuses("a non-null retained value with no EVIDENCE row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A
def test_unused_unkept_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    for crop in (OR, GF):
        _op(ops, crop, f"{SW}.sources")["new"].append("uc_anr_8100")
        _op(ops, crop, f"{SW}.anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-13"}
    _refuses("anchor uc_anr_8100 supports no evidenced leaf", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_unused_anchor(pre, stage):
    """Positive control for the test above: with `kept` rows the same anchors pass all of check_post."""
    ops, ev, dec = _c(stage)
    for crop in (OR, GF):
        _op(ops, crop, f"{SW}.sources")["new"].append("uc_anr_8100")
        _op(ops, crop, f"{SW}.anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-13"}
        dec.append({"crop": crop, "path": f"{SW}.anchoring_urls.uc_anr_8100", "decision": "kept", "reason": "t"})
    assert _check(pre, ops, ev, dec)["identical"] == 29


def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{SW}.sources")["new"].append("uc_anr_8100")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


def test_a_source_listed_twice(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, f"{SW}.sources")["new"].append("tamu_agrilife")
    _refuses("a source id listed twice", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard K
def test_record_without_a_record_only_row(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == GF and d["path"] == OF)]
    _refuses("open_findings: no record-only DECISIONS row", pre, ops, ev, dec)


def test_findings_are_append_only(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, GF, OF); o["new"] = o["new"][1:]
    _refuses("not the base list plus appended entries", pre, ops, ev, dec)


def test_a_finding_id_twice(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, OR, OF); o["new"] = o["new"] + [dict(o["new"][-1])]
    _refuses("a finding id twice", pre, ops, ev, dec)


def test_an_appended_finding_must_not_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, OR, OF)["new"][-1]["blocks_launch"] = True
    _refuses("must be open with blocks_launch false", pre, ops, ev, dec)


def test_a_dash_in_a_finding(pre, stage):
    ops, ev, dec = _c(stage)
    f = _op(ops, OR, OF)["new"][-1]; f["summary"] = f["summary"].replace(". The row", " — the row")
    _refuses("a dash in the summary", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def test_a_catalog_op_is_an_unknown_kind(tmp_path, stage):
    """Ruling C mints no id: a catalog op is refused at load."""
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "catalog"
    with pytest.raises(Refused, match="unknown kind 'catalog'"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_cited_id_must_be_in_the_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, CAR, f"{CAR}.traits_seasoned", "ghost_id", ANR)
    _refuses("EVIDENCE cites ghost_id, which is not in source_catalog", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard R
def test_seasoned_without_its_beginner(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == OR and o["path"] == f"{SW}.traits_beginner")]
    ev = [r for r in ev if not (r["crop"] == OR and r["entry_id"] == f"{SW}.traits_beginner")]
    _refuses("without its beginner sibling", pre, ops, ev, dec)


def test_byte_identical_registers(pre, stage):
    ops, ev, dec = _c(stage)
    s, b = _op(ops, OR, f"{CAR}.traits_seasoned"), _op(ops, OR, f"{CAR}.traits_beginner")
    b["new"] = s["new"]
    ev = [r for r in ev if not (r["crop"] == OR and r["entry_id"] == f"{CAR}.traits_beginner")]
    for r in [x for x in ev if x["crop"] == OR and x["entry_id"] == f"{CAR}.traits_seasoned"]:
        ev.append(dict(r, entry_id=f"{CAR}.traits_beginner"))
    _refuses("byte-identical", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard I
def test_ruled_identical_leaves_must_stay_identical(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, GF, f"{CAR}.traits_beginner", "Carrizo grows a large, vigorous tree.",
            "Carrizo grows a big, vigorous tree.")
    _refuses("not identical across", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard H
def test_hs132_kept_on_a_row(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, SW, f"{SW}.traits_seasoned", "uf_ifas_hs132", "https://ask.ifas.ufl.edu/publication/HS132")
    _refuses("still cites uf_ifas_hs132", pre, ops, ev, dec)


def test_ucr_kept_on_flying_dragon(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, FD, f"{FD}.traits_seasoned", "ucr_citrus", "https://citrusvariety.ucr.edu/crc3771")
    _refuses("Flying Dragon: still cites ucr_citrus", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, GF, NOTE, "makes a dwarf tree.", "makes a dwarf tree; hill soil up around it.")
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
        P.gate_post(P.apply_to(pre, stage[0]), {OR})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {OR})


def test_gate_all_failure(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {OR})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {OR})
