"""Suite for promote_pla625_p3b (PLA-625 citrus/rootstock pass, promote 3b: mandarin-clementine rootstock rows, the
recommendation, the note and its sources pair; uf_ifas_ch116 and ucce_placer_nevada_cold_damage minted).

DEVIATION, recorded: the promote was derived from promote_pla625_p2 before this suite existed. Stand-ins: POST_SHA was
matched by an INDEPENDENT minimal apply (p3b_texts.py written straight onto the base, no ops and no promote code) before
the canonical was written, and mutate_promote_pla625_p3b.py switches every guard off in turn. The pre-state is REPLAYED
from its pinned commit (promote_fixture: d52c261a -> 80e4a0c), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla625_p3b as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "d52c261ac66f6637c4be220af052858a1fa920ec64c1d6e5eeec95083fc72487"
POST_SHA = "d72aeed3072ef0555bf5ed26a00b8f1d4ee188dd485bfaad8216bdeed770beda"
MA = "mandarin-clementine"
R = "rootstock_options"
NOTE = "recommended_rootstock_note"
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


def _retext(ops, ev, path, old, new):
    o = _op(ops, MA, path)
    assert old in o["new"]
    o["new"] = o["new"].replace(old, new)
    for r in ev:
        if r["crop"] == MA and r["entry_id"] == path and old in r["value"]:
            r["value"] = r["value"].replace(old, new)


def _ev_row(ev, path, sid):
    return next(r for r in ev if r["crop"] == MA and r["entry_id"] == path and r["source_id"] == sid)


def _add_cite(ops, ev, blk, path, sid, url):
    like = next(r for r in ev if r["url"] == url)
    _op(ops, MA, f"{blk}.sources")["new"].append(sid)
    _op(ops, MA, f"{blk}.anchoring_urls")["new"][sid] = {"url": url, "verified": "2026-10-16"}
    ev.append(dict(like, crop=MA, entry_id=path, source_id=sid, field="test row"))


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (35, 100, 28, 1)
    assert (n["register_pairs"], n["hill_inspected"], n["retained"], n["nulled"], n["minted"]) == (6, 224, 4, 11, 2)
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_real_stage_values_and_sources(pre, stage):
    post = P.apply_to(pre, stage[0])
    m = P.by_slug(post)[MA]
    rows = m[R]
    vals = lambda r: (r["size_class"], r["mature_height_ft"], r["spread_ft"], r["container_suitable"],  # noqa: E731
                      r["container_size_gallons"], r["bearing_age_years"])
    assert [vals(r) for r in rows] == [("semi_dwarf", None, None, None, None, None),
                                       ("dwarf", [4, 8], None, True, None, None),
                                       ("semi_dwarf", [8, 14], None, None, None, None)]
    assert [r["sources"] for r in rows] == [
        ["uf_ifas_ch116", "uf_ifas_hs1260", "tamu_agrilife", "ucce_placer_nevada_31_018c", "ucce_placer_nevada_cold_damage",
         "ucce_riverside_citrus_qa", "az_coop_ext"],
        ["uf_ifas_ch116", "ucanr_santa_clara_mg", "ucce_placer_nevada_31_018c", "uf_ifas_hs1260"],
        ["ucr_citrus", "uf_ifas_ch116", "uf_ifas_hs1260"]]
    assert m["recommended_rootstock"] is None
    assert m["recommended_rootstock_note_sources"] == [
        "uf_ifas_hs132", "az_coop_ext", "uf_ifas_ch116", "ucce_placer_nevada_cold_damage", "tamu_agrilife",
        "ucce_riverside_citrus_qa", "ucce_placer_nevada_31_018c", "uf_ifas_hs1260"]
    for sid in P.MINTED:
        assert post["source_catalog"][sid]["title"]
    vs = m["verification_status"]
    assert (vs["status"], vs["launch_ready_core"], vs["launch_ready_seasoned"]) == ("verified_gs_arc", False, False)


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["register_pairs"] == 6


# ---------------------------------------------------------------- loading / pre
def _stage_dir(tmp_path, ops):
    (tmp_path / "ops.json").write_text(json.dumps(ops), encoding="utf-8")
    return str(tmp_path)


def test_wrong_base(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="pinned to"):
        P.load_canonical(str(p))


def test_empty_stage(tmp_path):
    with pytest.raises(Refused, match="names no op"):
        P.load_stage(_stage_dir(tmp_path, []))


def test_op_keys_must_be_exact(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["x"] = 1
    with pytest.raises(Refused, match="keys must be exactly"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_unknown_kind(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "row"
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
    _op(ops, MA, f"{R}[0].traits_seasoned")["old"] = "something else"
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, NOTE)["crop"] = "ghost-crop"
    with pytest.raises(Refused, match="is not a crop"):
        P.check_pre(pre, ops)


def test_minting_an_existing_id_is_check_pres(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch116")["path"] = "uf_ifas_hs132"
    with pytest.raises(Refused, match="uf_ifas_hs132: the base value is not the op's `old`"):
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


def test_stray_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[MA]["container_notes"]["notes_beginner"] = "x"
    _refuses(r"mandarin-clementine: changed outside the staged ops: \['container_notes", pre, ops, ev, dec, post)


def test_launch_flag_is_a_stray_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[MA]["verification_status"]["launch_ready_core"] = True
    _refuses("mandarin-clementine: changed outside the staged ops", pre, ops, ev, dec, post)


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
    """container_notes belongs to the PLA-533 container work (ruling E)."""
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)[MA]["container_notes"]
    ops.append({"crop": MA, "path": "container_notes.notes_seasoned", "kind": "prose", "old": c["notes_seasoned"],
                "new": c["notes_seasoned"] + " More.", "cited_at": "container_notes", "reason": "t"})
    _refuses("container_notes.notes_seasoned: outside the ruled scope", pre, ops, ev, dec)


def test_crop_outside_the_ruled_one(pre, stage):
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)["lemon"]
    ops.append({"crop": "lemon", "path": NOTE, "kind": "prose", "old": c[NOTE], "new": c[NOTE] + " More.",
                "cited_at": NOTE, "reason": "t"})
    _refuses("lemon is outside this promote's crop", pre, ops, ev, dec)


def test_a_catalog_kind_on_the_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, NOTE)["kind"] = "catalog"
    _refuses("a catalog op must name <catalog>", pre, ops, ev, dec)


def test_a_catalog_op_outside_the_ruled_mints(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "MINTED", ("ucce_placer_nevada_cold_damage",))
    _refuses("a catalog op on uf_ifas_ch116", pre, ops, ev, dec)


def test_rows_must_be_the_ruled_list(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "ROWS", ["Trifoliate orange", "Flying Dragon trifoliate", "Swingle citrumelo"])
    _refuses("rootstock_options rows are not", pre, ops, ev, dec)


def test_catalog_ops_are_exactly_the_ruled_ids(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["path"] != "ucce_placer_nevada_cold_damage"]
    ev = [r for r in ev if r["source_id"] != "ucce_placer_nevada_cold_damage"]
    monkeypatch.setattr(P, "MINTED", ("uf_ifas_ch116",))
    post = P.apply_to(pre, ops)
    monkeypatch.setattr(P, "MINTED", ("uf_ifas_ch116", "ucce_placer_nevada_cold_damage"))
    with pytest.raises(Refused, match="catalog ops are not exactly the ruled ids"):
        P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


# ---------------------------------------------------------------- guard V + P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    _op(ops, MA, f"{R}[0].traits_seasoned")["new"] = "Not what was written."
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, MA, f"{R}[2].size_class"); o["new"] = o["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_em_dash(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, f"{R}[2].traits_beginner", "It does poorly", "It — does poorly")
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_cultivar(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, NOTE, "Murcott on Swingle citrumelo", "the Murcott cultivar on Swingle citrumelo")
    _refuses("'cultivar' in consumer copy", pre, ops, ev, dec)


def test_bare_degree(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, f"{R}[2].traits_seasoned", "Its cold hardiness is good.", "Its cold hardiness is good to 20 degrees.")
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_null_prose(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[1].what_to_ask_nursery")["new"] = None
    _refuses("prose must be a non-empty string", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard D (+ retained)
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("DECISIONS row names ghost-crop", pre, ops, ev, dec)


def test_prose_without_cited_at(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, NOTE)["cited_at"] = None
    _refuses("prose with no cited_at", pre, ops, ev, dec)


def test_retained_on_a_non_crop(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "<roster>", "path": "x", "decision": "retained", "reason": "t"})
    _refuses("retained <roster> x: not a crop", pre, ops, ev, dec)


def test_retained_is_also_an_op(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": MA, "path": f"{R}[2].size_class", "decision": "retained", "reason": "t"})
    _refuses("also staged as an op", pre, ops, ev, dec)


def test_retained_value_moved(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": MA, "path": f"{R}[2].anchoring_urls.ucr_citrus", "decision": "retained", "reason": "t"})
    _refuses("the value moved", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard N
def test_nulled_without_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["path"] == "recommended_rootstock")]
    _refuses("recommended_rootstock: nulled with no `nulled` DECISIONS row", pre, ops, ev, dec)


def test_evidence_for_a_nulled_value(pre, stage):
    ops, ev, dec = _c(stage)
    row = dict(_ev_row(ev, f"{R}[2].size_class", "uf_ifas_hs1260"))
    row.update(entry_id=f"{R}[2].spread_ft", value="null")
    ev.append(row)
    _refuses("evidence for a value nulled by the ruling", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("a duplicate row", pre, ops, ev, dec)


def test_row_on_an_unstaged_path(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0], entry_id="container_notes.notes_seasoned"))
    _refuses("not a staged prose / value op or a retained leaf", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    _ev_row(ev, NOTE, "uf_ifas_ch116")["quote"] = "trifoliate orange is the only rootstock for every mandarin"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_url_not_cited_on_crop(pre, stage):
    ops, ev, dec = _c(stage)
    r = _ev_row(ev, f"{R}[2].traits_seasoned", "ucr_citrus")
    r["url"] = "https://citrusvariety.ucr.edu/crc2863"
    r["sha256"] = "651bd22c46ba74e1630d3a0e4479d7602aa557d9b55edbf46f0e7fac040e88cb"
    r["quote"] = "a cross of washington navel and trifoliate orange"
    _refuses("url is not cited anywhere on mandarin-clementine", pre, ops, ev, dec)


def test_one_url_per_source_id_per_block(pre, stage):
    """AZ1001 (az_coop_ext) is cited on the note; a row on the Swingle row at that url is refused: Swingle's anchors do
    not carry az_coop_ext."""
    ops, ev, dec = _c(stage)
    like = _ev_row(ev, NOTE, "az_coop_ext")
    ev.append(dict(like, entry_id=f"{R}[2].traits_seasoned", field="test row"))
    _refuses(r"rootstock_options\[2\] anchors do not carry az_coop_ext at the row's url", pre, ops, ev, dec)


def test_cited_at_names_no_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[0].traits_seasoned")["cited_at"] = f"{R}[9]"
    _refuses("names no citation block", pre, ops, ev, dec)


def test_block_sources_missing(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[2].sources")["new"].remove("ucr_citrus")
    _refuses("sources do not name ucr_citrus", pre, ops, ev, dec)


def test_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["entry_id"] == f"{R}[1].what_to_ask_nursery")]
    _refuses("what_to_ask_nursery: no EVIDENCE row", pre, ops, ev, dec)


def test_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["entry_id"] == f"{R}[1].mature_height_ft")]
    _refuses("mature_height_ft: no EVIDENCE row", pre, ops, ev, dec)


def test_retained_value_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["entry_id"] == f"{R}[1].size_class")]
    _refuses("a non-null retained value with no EVIDENCE row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A
def test_unused_unkept_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[2].sources")["new"].append("uc_anr_8100")
    _op(ops, MA, f"{R}[2].anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-16"}
    _refuses("anchor uc_anr_8100 supports no evidenced leaf", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_unused_anchor(pre, stage):
    """Positive control for the test above."""
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[2].sources")["new"].append("uc_anr_8100")
    _op(ops, MA, f"{R}[2].anchoring_urls")["new"]["uc_anr_8100"] = {"url": ANR, "verified": "2026-10-16"}
    dec.append({"crop": MA, "path": f"{R}[2].anchoring_urls.uc_anr_8100", "decision": "kept", "reason": "t"})
    assert _check(pre, ops, ev, dec)["minted"] == 2


def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[2].sources")["new"].append("uc_anr_8100")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


def test_a_source_listed_twice(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, f"{R}[2].sources")["new"].append("ucr_citrus")
    _refuses("a source id listed twice", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def test_a_minted_ids_id_is_its_path(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch116")["new"]["id"] = "uf_ifas_ch11"
    _refuses("catalog uf_ifas_ch116: its id is 'uf_ifas_ch11'", pre, ops, ev, dec)


def test_a_minted_id_must_be_titled(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "ucce_placer_nevada_cold_damage")["new"]["title"] = ""
    _refuses("must be document-scoped and titled", pre, ops, ev, dec)


def test_a_minted_id_must_be_document_scoped(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch116")["new"]["url"] = "https://ask.ifas.ufl.edu"
    _refuses("must be document-scoped and titled", pre, ops, ev, dec)


def test_a_minted_id_must_be_t1(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch116")["new"]["tier"] = "T2"
    _refuses("a minted id must be T1", pre, ops, ev, dec)


def test_a_minted_id_must_be_evidenced_at_its_url(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_ch116")["new"]["url"] = "https://ask.ifas.ufl.edu/publication/CH999"
    _refuses("catalog uf_ifas_ch116: no EVIDENCE row cites it at its url", pre, ops, ev, dec)


def test_cited_id_must_be_in_the_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, f"{R}[2]", f"{R}[2].traits_seasoned", "ghost_id",
              "https://ucanr.edu/sites/default/files/2013-12/178097.pdf")
    _refuses("EVIDENCE cites ghost_id, which is not in source_catalog", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard R
def test_seasoned_without_its_beginner(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["path"] != f"{R}[2].traits_beginner"]
    ev = [r for r in ev if r["entry_id"] != f"{R}[2].traits_beginner"]
    _refuses("without its beginner sibling", pre, ops, ev, dec)


def test_byte_identical_registers(pre, stage):
    ops, ev, dec = _c(stage)
    s, b = _op(ops, MA, f"{R}[0].traits_seasoned"), _op(ops, MA, f"{R}[0].traits_beginner")
    b["new"] = s["new"]
    ev = [r for r in ev if r["entry_id"] != f"{R}[0].traits_beginner"]
    for r in [x for x in ev if x["entry_id"] == f"{R}[0].traits_seasoned"]:
        ev.append(dict(r, entry_id=f"{R}[0].traits_beginner"))
    _refuses("byte-identical", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard H
def test_a_dropped_credit_kept(pre, stage):
    """ruling A: tamu_agrilife comes off the Flying Dragon row (it names no Flying Dragon)."""
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, f"{R}[1]", f"{R}[1].traits_seasoned", "tamu_agrilife",
              "https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/")
    _refuses(r"Flying Dragon trifoliate: still cites \['tamu_agrilife'\]", pre, ops, ev, dec)


def test_ch116_left_under_uf_ifas_edis(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, f"{R}[2]", f"{R}[2].traits_seasoned", "uf_ifas_edis",
              "https://ask.ifas.ufl.edu/publication/HS1260")
    _refuses("Swingle citrumelo: still cites uf_ifas_edis", pre, ops, ev, dec)


def test_hs132_on_a_mandarin_row(pre, stage):
    ops, ev, dec = _c(stage)
    _add_cite(ops, ev, f"{R}[0]", f"{R}[0].traits_seasoned", "uf_ifas_hs132",
              "https://ask.ifas.ufl.edu/publication/HS132")
    _refuses(r"Trifoliate orange \(Poncirus trifoliata\): uf_ifas_hs132 kept", pre, ops, ev, dec)


def test_hs132_retail_row_dropped_elsewhere(pre, stage):
    """The roster-wide half of ruling D: lemon [0] (the retail claim) must keep uf_ifas_hs132."""
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    lem = P.by_slug(post)["lemon"][R][0]
    lem["sources"].remove("uf_ifas_hs132"); del lem["anchoring_urls"]["uf_ifas_hs132"]
    pre2 = copy.deepcopy(pre)
    lem2 = P.by_slug(pre2)["lemon"][R][0]
    lem2["sources"].remove("uf_ifas_hs132"); del lem2["anchoring_urls"]["uf_ifas_hs132"]
    with pytest.raises(Refused, match=r"lemon sour orange \(Citrus aurantium\): uf_ifas_hs132 dropped"):
        P.check_post(pre2, post, ops, ev, dec, P.EVIDENCE)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, NOTE, "makes a dwarf tree.", "makes a dwarf tree; hill soil up around it.")
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
        P.gate_post(P.apply_to(pre, stage[0]), {MA})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {MA})


def test_gate_all_failure(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {MA})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {MA})
