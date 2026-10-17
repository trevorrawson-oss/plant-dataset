"""Suite for promote_pla625_p3a (PLA-625 citrus/rootstock pass, promote 3a: citrus mulch, graft-union height and brown rot
on five crops; HS141 and CG009 minted; CG009 re-keyed and kept; grapefruit's mulch finding noted, still open).

DEVIATION, recorded: the promote was derived from promote_pla625_p2 before this suite existed. Stand-ins: POST_SHA was
matched by an INDEPENDENT minimal apply (p3a_texts.py written straight onto the base, no ops, no build_stage and no
promote code) before the canonical was written, and mutate_promote_pla625_p3a.py switches every guard off in turn. The
pre-state is REPLAYED from its pinned commit (promote_fixture: ef1a4d35 -> 84c3662), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla625_p3a as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "ef1a4d351e4b26ea0369f5f3da824cb7c81ffcd4e3e1e2013b94b2413dcf6261"
POST_SHA = "d52c261ac66f6637c4be220af052858a1fa920ec64c1d6e5eeec95083fc72487"
LE, LI, ON, GF, MA = "lemon", "lime", "orange-navel", "grapefruit", "mandarin-clementine"
FR, BR = P.FR, P.BR
OF = "verification_status.open_findings"
FINDING = "grapefruit_mulched_basin_contradicted_pla533"


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


def _resub(op, old_new, new_new):
    """Change one substitution's new text in a prose op, keeping `new` consistent with `subs`."""
    for s in op["subs"]:
        if s[1] == old_new:
            s[1] = new_new
    op["new"] = op["new"].replace(old_new, new_new)


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["subs"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (97, 70, 123, 33, 5)
    assert (n["evidence_only"], n["ids_added"], n["ids_moved"], n["minted"], n["noted"]) == (19, 22, 6, 2, 1)
    assert n["hill_inspected"] == 224
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_real_stage_values(pre, stage):
    post = P.apply_to(pre, stage[0])
    q = P.by_slug(post)
    for c in (LE, ON):
        anc = P._value(q[c], FR)["anchoring_urls"]
        assert anc["uf_ifas_cg009"]["note"] == P.CG009_NOTE and "CG009" in anc["uf_ifas_cg009"]["url"]
    assert "uf_ifas_hs132" not in P._value(q[LE], FR)["sources"]
    assert "uf_ifas_edis" not in P._value(q[ON], FR)["sources"]
    br = P._value(q[ON], BR)
    assert [r["method"] for r in br["control_ladder"]] == ["improve_drainage", "prompt_harvest", "garden_sanitation",
                                                          "copper_fungicide"]
    assert br["anchoring_urls"]["uc_ipm"]["url"] == P.BR_UC_IPM
    f = next(x for x in q[GF]["verification_status"]["open_findings"] if x["id"] == FINDING)
    assert f["status"] == "open" and "STAYS OPEN" in f["progress_note"]
    for c in (ON, GF, MA):
        assert "UF/IFAS's general citrus guide and Texas A&M advise against" in q[c]["watering"]["method_seasoned"]
        assert "Florida's general citrus guide and Texas A&M say not to" in q[c]["watering"]["method_beginner"]
    assert q[MA]["watering"]["anchoring_urls"]["ucanr_santa_clara_mg"]["url"].endswith("319461.pdf")
    assert q[MA]["watering"]["anchoring_urls"]["uc_mg_santa_clara_citrus"]["url"].endswith("growing-great-citrus")
    assert {"uf_ifas_ch092", "uf_ifas_ch093"} <= set(P._value(q[LI], FR)["sources"])
    assert "uf_ifas_hs141" in post["source_catalog"] and "uf_ifas_cg009" in post["source_catalog"]
    for c in (LE, LI, GF, ON, MA):
        vs = q[c]["verification_status"]
        assert vs["status"] == "verified_gs_arc"


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["subs"] == 70


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
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "rename"
    with pytest.raises(Refused, match="unknown kind"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_empty_reason(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["reason"] = " "
    with pytest.raises(Refused, match="empty reason"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_op_staged_twice(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]) * 2
    with pytest.raises(Refused, match="staged twice"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_drifted_base(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LE, "soil_prep_beginner")["old"] = "something else"
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LE, "soil_prep_beginner")["crop"] = "ghost-crop"
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
    post = P.apply_to(pre, ops); P.by_slug(post)["peach"]["ghost_key"] = None
    _refuses("peach: top-level crop keys changed", pre, ops, ev, dec, post)


def test_stray_change_on_a_touched_crop(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[GF]["watering"]["frequency_beginner"] = "x"
    _refuses(r"grapefruit: changed outside the staged ops: \['watering\.frequency_beginner'\]", pre, ops, ev, dec, post)


def test_launch_flag_is_a_stray_change(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); P.by_slug(post)[GF]["verification_status"]["launch_ready_core"] = True
    _refuses("grapefruit: changed outside the staged ops", pre, ops, ev, dec, post)


def test_catalog_stray(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["source_catalog"]["uc_ipm"]["name"] = "x"
    _refuses("source_catalog changed outside", pre, ops, ev, dec, post)


def test_catalog_lost_id(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); del post["source_catalog"]["uf_ifas_edis"]
    _refuses("source_catalog lost ids", pre, ops, ev, dec, post)


# ---------------------------------------------------------------- guard S
def test_path_outside_the_ruled_scope(pre, stage):
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)[LE]["watering"]
    ops.append({"crop": LE, "path": "watering.frequency_beginner", "kind": "prose", "old": c["frequency_beginner"],
                "new": c["frequency_beginner"] + " More.", "cited_at": None, "reason": "t",
                "subs": [[c["frequency_beginner"], c["frequency_beginner"] + " More."]]})
    _refuses("watering.frequency_beginner: outside the ruled scope", pre, ops, ev, dec)


def test_crop_outside_the_five(pre, stage):
    ops, ev, dec = _c(stage)
    c = P.by_slug(pre)["peach"]
    f = next(k for k, v in c.items() if isinstance(v, str) and k != "slug")
    ops.append({"crop": "peach", "path": f, "kind": "prose", "old": c[f], "new": c[f] + " x", "cited_at": None,
                "reason": "t", "subs": [[c[f], c[f] + " x"]]})
    _refuses("peach is outside this promote's five crops", pre, ops, ev, dec)


def test_catalog_op_outside_the_ruled_mints(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_hs141")["path"] = "uf_ifas_hs999"
    post = P.apply_to(pre, [o for o in ops])
    with pytest.raises(Refused, match="catalog op on uf_ifas_hs999"):
        P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def test_a_catalog_kind_on_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LE, "soil_prep_beginner")["kind"] = "catalog"
    _refuses("a catalog op must name <catalog>", pre, ops, ev, dec)


def test_a_ruled_crop_with_no_op(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["crop"] != MA]
    ev = [r for r in ev if r["crop"] != MA]
    dec = [d for d in dec if d["crop"] != MA]
    _refuses("mandarin-clementine: the stage names no op on a ruled crop", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard V + T + P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    _op(ops, LE, "soil_prep_beginner")["new"] = "Not what was written."
    _refuses("the post value is not the op's `new`", pre, ops, ev, dec, post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    o = _op(ops, LE, "soil_prep_beginner"); o["old"] = o["new"]
    with pytest.raises(Refused, match="a no-op"):
        P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def test_prose_without_subs(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LE, "soil_prep_beginner")["subs"] = []
    _refuses("a prose op with no ruled substitutions", pre, ops, ev, dec)


def test_a_sub_whose_old_is_not_once(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LE, "soil_prep_beginner")
    o["subs"].insert(0, ["the", "the"])
    _refuses("a substitution's old text occurs", pre, ops, ev, dec)


def test_touched_leaf_rule(pre, stage):
    """An extra edit outside the ruled substitutions (new no longer equals old + subs) is refused."""
    ops, ev, dec = _c(stage)
    o = _op(ops, LE, "soil_prep_beginner")
    o["new"] = o["new"] + " Also water deeply."
    _refuses("`new` is not `old` with the ruled substitutions", pre, ops, ev, dec)


def test_subs_on_a_non_prose_op(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, LE, f"{FR}.sources")["subs"] = [["a", "b"]]
    _refuses(r"subs on a sources op", pre, ops, ev, dec)


def test_em_dash_in_a_new_clause(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.organic_treatment_beginner")
    _resub(o, o["subs"][0][1], o["subs"][0][1].replace(", trim", " — trim").replace("before, trim", "before — trim"))
    _refuses("an em or en dash", pre, ops, ev, dec)


def test_cultivar_in_a_new_clause(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.organic_treatment_beginner")
    _resub(o, o["subs"][0][1], o["subs"][0][1].replace("low branches", "low branches of every cultivar"))
    _refuses("'cultivar' in consumer copy", pre, ops, ev, dec)


def test_bare_degree_in_a_new_clause(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.organic_treatment_beginner")
    _resub(o, o["subs"][0][1], o["subs"][0][1].replace("ground.", "ground below 50 degrees."))
    _refuses("a temperature without °F", pre, ops, ev, dec)


def test_prose_emptied(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.organic_treatment_beginner")
    o["subs"] = [[o["old"], ""]]; o["new"] = ""
    dec.append({"crop": ON, "path": f"{BR}.organic_treatment_beginner", "decision": "deleted", "reason": "t"})
    _refuses("prose must stay a non-empty string", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("a duplicate row", pre, ops, ev, dec)


def test_row_on_an_unstaged_path(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0], entry_id="watering.frequency_beginner"))
    _refuses("not a staged prose op", pre, ops, ev, dec)


def test_row_value_not_a_new_substring(pre, stage):
    ops, ev, dec = _c(stage)
    ev[0]["value"] = "Something else entirely."
    _refuses("its value is not one of the op's new substrings", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    ev[0]["quote"] = "mulch every citrus tree right up to the trunk"
    _refuses("the quote is not in the cached bytes", pre, ops, ev, dec)


def test_row_source_not_in_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(x for x in ev if x["crop"] == GF and x["entry_id"] == "year_one_notes_beginner")
    r["source_id"] = "ghost_id"
    _refuses("ghost_id is not in source_catalog", pre, ops, ev, dec)


def test_cited_at_names_no_block(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, ON, f"{BR}.prevention_seasoned")["cited_at"] = "diseases[id=ghost]"
    _refuses("names no citation block", pre, ops, ev, dec)


def test_cited_row_not_at_the_blocks_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(x for x in ev if x["crop"] == MA and x["entry_id"] == "watering.method_seasoned"
             and x["source_id"] == "uf_ifas_hs132")
    r["url"] = "https://edis.ifas.ufl.edu/publication/HS132"
    _refuses("anchors do not carry uf_ifas_hs132 at the row's url", pre, ops, ev, dec)


def test_cited_row_not_in_the_blocks_sources(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, MA, "watering.sources")["new"].remove("uf_ifas_hs141")
    _refuses("sources do not name uf_ifas_hs141", pre, ops, ev, dec)


def test_evidence_only_without_its_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == GF and d["path"] == "watering.method_beginner")]
    _refuses("an uncited string with no evidence-only DECISIONS row", pre, ops, ev, dec)


def test_a_new_clause_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == LE and r["entry_id"] == "start_method.notes_seasoned")]
    _refuses("start_method.notes_seasoned: the new clause .* has no EVIDENCE row", pre, ops, ev, dec)


def test_a_deletion_without_its_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == LE and d["decision"] == "deleted")]
    _refuses("a deletion with no `deleted` DECISIONS row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A + X
def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, ON, "companions.sources")["new"].append("uc_anr_8100")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


def test_a_source_listed_twice(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, ON, "companions.sources")["new"].append("uf_ifas_hs141")
    _refuses("a source id listed twice", pre, ops, ev, dec)


def test_an_added_id_with_no_evidenced_clause(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, ON, "companions.sources")["new"].append("uc_anr_8100")
    _op(ops, ON, "companions.anchoring_urls")["new"]["uc_anr_8100"] = {
        "url": "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf", "verified": "2026-10-16"}
    _refuses("added id uc_anr_8100 supports no evidenced clause", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_added_id(pre, stage):
    """Positive control for the test above."""
    ops, ev, dec = _c(stage)
    _op(ops, ON, "companions.sources")["new"].append("uc_anr_8100")
    _op(ops, ON, "companions.anchoring_urls")["new"]["uc_anr_8100"] = {
        "url": "https://escholarship.org/content/qt5hh528qp/qt5hh528qp.pdf", "verified": "2026-10-16"}
    dec.append({"crop": ON, "path": "companions.anchoring_urls.uc_anr_8100", "decision": "kept", "reason": "t"})
    assert _check(pre, ops, ev, dec)["ids_added"] == 23


def test_a_rekey_row_that_names_no_from(pre, stage):
    ops, ev, dec = _c(stage)
    d = next(x for x in dec if x["decision"] == "rekey" and x["crop"] == LI and x["path"].startswith("companions"))
    d["reason"] = "re-keyed"
    _refuses("rekey DECISIONS row for uf_ifas_ch092 does not name", pre, ops, ev, dec)


def test_a_rekey_that_moves_the_url(pre, stage):
    """mandarin watering's uc_mg_santa_clara_citrus carries no evidence row, so the re-key guard is what sees it."""
    ops, ev, dec = _c(stage)
    _op(ops, MA, "watering.anchoring_urls")["new"]["uc_mg_santa_clara_citrus"]["url"] = "https://ucanr.edu/x"
    _refuses("re-key ucanr_santa_clara_mg -> uc_mg_santa_clara_citrus does not keep the url", pre, ops, ev, dec)


def test_an_id_removed_without_a_decision(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, "companions.sources"); o["new"].remove("uf_ifas_hs132")
    del _op(ops, ON, "companions.anchoring_urls")["new"]["uf_ifas_hs132"]
    _refuses("id uf_ifas_hs132 removed with no cg009-off DECISIONS row", pre, ops, ev, dec)


def test_a_url_moved_without_a_repoint(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if d["decision"] != "repoint"]
    _refuses("uc_ipm moved url with no repoint DECISIONS row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard L
def test_a_ladder_op_off_the_ruled_entry(pre, stage):
    """Only orange-navel carries a brown-rot ladder, so a ladder op elsewhere reaches guard L through an in-scope path
    of another kind (scope S admits companions.sources; guard L must refuse a ladder op there)."""
    ops, ev, dec = _c(stage)
    _op(ops, ON, "companions.sources")["kind"] = "ladder"
    _refuses("a ladder op on orange-navel companions.sources", pre, ops, ev, dec)


def test_the_wrong_rung_removed(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.control_ladder")
    o["new"] = [r for r in o["old"] if r["method"] != "copper_fungicide"]
    _refuses("not the base ladder minus the splash_barrier_mulch rung", pre, ops, ev, dec)


def test_rungs_reordered(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.control_ladder")
    o["new"] = list(reversed(o["new"]))
    _refuses("not the base ladder minus the splash_barrier_mulch rung", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard K
def test_record_without_a_record_only_row(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if not (d["crop"] == GF and d["path"] == OF)]
    _refuses("no record-only DECISIONS row", pre, ops, ev, dec)


def test_findings_reordered(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, GF, OF); o["new"] = list(reversed(o["new"]))
    _refuses("open_findings ids or order changed", pre, ops, ev, dec)


def test_another_finding_touched(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, GF, OF)
    other = next(f for f in o["new"] if f["id"] != FINDING)
    other["summary"] = other["summary"] + " x"
    _refuses("a finding outside the ruled note changed", pre, ops, ev, dec)


def test_the_finding_resolved_instead_of_noted(pre, stage):
    """Amendment stop 2: the finding STAYS OPEN past 3a."""
    ops, ev, dec = _c(stage)
    f = next(x for x in _op(ops, GF, OF)["new"] if x["id"] == FINDING)
    f["status"] = "resolved"
    _refuses("a field other than progress_note moved", pre, ops, ev, dec)


def test_a_finding_field_other_than_the_note_added(pre, stage):
    ops, ev, dec = _c(stage)
    f = next(x for x in _op(ops, GF, OF)["new"] if x["id"] == FINDING)
    f["resolution_note"] = "x"
    _refuses("only a progress_note may be added", pre, ops, ev, dec)


def test_an_empty_progress_note(pre, stage):
    ops, ev, dec = _c(stage)
    f = next(x for x in _op(ops, GF, OF)["new"] if x["id"] == FINDING)
    f["progress_note"] = " "
    _refuses("an empty progress note", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def test_a_minted_ids_id_is_its_path(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_hs141")["new"]["id"] = "uf_ifas_hs14"
    _refuses("catalog uf_ifas_hs141: its id is 'uf_ifas_hs14'", pre, ops, ev, dec)


def test_a_minted_id_must_be_titled(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_cg009")["new"]["title"] = ""
    _refuses("must be document-scoped and titled", pre, ops, ev, dec)


def test_a_minted_id_must_be_t1(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "uf_ifas_hs141")["new"]["tier"] = "T2"
    _refuses("a minted id must be T1", pre, ops, ev, dec)


def test_a_minted_id_must_be_cited(pre, stage, monkeypatch):
    """A minted id that no evidence row and no anchor cites is refused (scope widened to admit the extra mint)."""
    ops, ev, dec = _c(stage)
    extra = copy.deepcopy(_op(ops, "<catalog>", "uf_ifas_hs141"))
    extra["path"] = extra["new"]["id"] = "uf_ifas_hs999"
    extra["new"]["url"] = "https://ask.ifas.ufl.edu/publication/HS999"
    ops.append(extra)
    monkeypatch.setattr(P, "MINTED", P.MINTED + ("uf_ifas_hs999",))
    _refuses("catalog uf_ifas_hs999: neither an EVIDENCE row at its url nor a MANIFEST-listed anchor cites it",
             pre, ops, ev, dec)


def test_a_minted_anchor_only_id_needs_a_manifest_url(pre, stage, monkeypatch):
    """CG009 is cited only by anchors; if its bytes were not MANIFEST-listed, the mint is refused."""
    ops, ev, dec = _c(stage)
    real = P.manifest
    monkeypatch.setattr(P, "manifest", lambda d: {k: v for k, v in real(d).items() if not k.startswith("c2bc36bb")})
    _refuses("catalog uf_ifas_cg009: neither an EVIDENCE row at its url nor a MANIFEST-listed anchor cites it",
             pre, ops, ev, dec)


# ---------------------------------------------------------------- guard H
def test_a_ruled_string_survives(pre, stage):
    """orange-navel foot-rot prevention_beginner carries two subs; reverting the 'a foot' one leaves the old phrase."""
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{FR}.prevention_beginner")
    assert o["new"].count("a foot") == 1
    _resub(o, "a foot", "a hand's width")
    for r in ev:
        if r["crop"] == ON and r["entry_id"] == f"{FR}.prevention_beginner" and r["value"] == "a foot":
            r["value"] = "a hand's width"
    _refuses("still carries \"hand's width\"", pre, ops, ev, dec)


def test_cg009_left_under_another_key(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, LE, f"{FR}.anchoring_urls")
    o["new"]["uf_ifas_hs132"] = dict(o["new"].pop("uf_ifas_cg009"))
    s = _op(ops, LE, f"{FR}.sources"); s["new"] = ["uf_ifas_hs132" if x == "uf_ifas_cg009" else x for x in s["new"]]
    dec = [d for d in dec if not (d["crop"] == LE and d["decision"] == "rekey")]
    post = P.apply_to(pre, ops)
    with pytest.raises(Refused, match="CG009 must be cited once, under uf_ifas_cg009|uf_ifas_hs132"):
        P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def test_cg009_without_its_scope_note(pre, stage):
    ops, ev, dec = _c(stage)
    del _op(ops, ON, f"{FR}.anchoring_urls")["new"]["uf_ifas_cg009"]["note"]
    _refuses("with the commercial-page scope note", pre, ops, ev, dec)


def test_splash_rung_left_in(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["kind"] != "ladder"]
    _refuses("still carries the splash_barrier_mulch rung", pre, ops, ev, dec)


def test_brown_rot_uc_ipm_not_repointed(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "BR_UC_IPM", "https://ipm.ucanr.edu/agriculture/citrus/brown-rot/")
    _refuses("uc_ipm is not the cached home-and-landscape page", pre, ops, ev, dec)


def test_the_finding_note_dropped(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if o["kind"] != "record"]
    _refuses("must stay open and carry its progress note", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, ON, f"{BR}.organic_treatment_beginner")
    new = o["subs"][0][1] + " Hill soil up around the trunk."
    for r in ev:
        if r["crop"] == ON and r["entry_id"] == f"{BR}.organic_treatment_beginner":
            r["value"] = new
    _resub(o, o["subs"][0][1], new)
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
        P.gate_post(P.apply_to(pre, stage[0]), {LE})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {LE})


def test_gate_all_failure(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {LE})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {LE})
