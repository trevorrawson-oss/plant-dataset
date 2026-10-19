"""test_promote_pla750 -- the PLA-750 heat-hold promote's guards, against its own staged ops on the pinned base.

The positive control runs the whole transform with every guard (gates off for speed; the promote's --check runs
them). Each negative test injects one defect into a deep copy of the stage or of the post-state and asserts the
GUARD'S OWN refusal text, so a refusal from an earlier check can never pass a test meant for a later one.
REPLAY: the base is promote_fixture.pre_state(BASE_SHA) (commit 1f651e5), never the live canonical, and it
FAILS rather than skips if the base cannot be rebuilt.
"""
import copy
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla750 as p  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

PRE = json.loads(promote_fixture.pre_state(p.BASE_SHA))
OPS, EV, DEC = p.load_stage(p.STAGE)


def run(ops=None, ev=None, dec=None, pre=None):
    return p.run(pre or PRE, OPS if ops is None else ops, EV if ev is None else ev, DEC if dec is None else dec,
                 p.EVIDENCE, gates=False)


def post_check(mutate):
    """Apply the clean stage, mutate the post, run check_post. Returns the refusal text."""
    post = p.apply_to(PRE, OPS)
    mutate(post)
    with pytest.raises(Refused) as e:
        p.check_post(PRE, post, OPS, EV, DEC, p.EVIDENCE)
    return str(e.value)


def refused(**kw):
    with pytest.raises(Refused) as e:
        run(**kw)
    return str(e.value)


def crop(data, slug):
    return next(c for c in data["crops"] if c["slug"] == slug)


def op_of(ops, crop_, path=None, kind=None):
    hits = [o for o in ops if o["crop"] == crop_ and (path is None or o["path"] == path)
            and (kind is None or o["kind"] == kind)]
    assert len(hits) == 1, (crop_, path, kind, len(hits))
    return hits[0]


# ---------------------------------------------------------------- positive control
def test_clean_stage_passes_every_guard_and_reports_its_population():
    post, n = run()
    assert n["ops"] == len(OPS) == 97
    assert n["field_inspected"] == 30
    assert n["tips_added"] == 5 and n["minted"] == 5 and n["dropped"] == 2
    assert n["ids_added"] >= 12 and n["struck"] >= 3 and n["subs"] >= 16
    assert n["evidence_rows"] == len(EV) > 40
    held = {c["slug"]: c["sowing_heat_ceiling"]["temp_f"] for c in post["crops"]
            if (c.get("sowing_heat_ceiling") or {}).get("temp_f") is not None}
    assert held == p.HELD


def test_the_stage_is_exactly_the_ruled_crops():
    assert {o["crop"] for o in OPS} - {p.CATALOG} == set(p.CROPS)
    assert len(p.CROPS) == 30 and len(p.HELD) == 10 and len(p.NOT_HELD) == 20


# ---------------------------------------------------------------- pin + pre
def test_a_drifted_base_refuses_in_check_pre():
    pre = copy.deepcopy(PRE)
    crop(pre, "carrot")["succession_policy"]["pause_in_heat"] = False
    assert "the base value is not the op's `old`" in refused(pre=pre)


def test_load_canonical_refuses_another_sha(tmp_path):
    f = tmp_path / "c.json"
    f.write_text("{}")
    with pytest.raises(Refused, match="pinned to"):
        p.load_canonical(str(f))


def test_an_empty_stage_refuses(tmp_path):
    (tmp_path / "ops.json").write_text("[]")
    with pytest.raises(Refused, match="names no op"):
        p.load_stage(str(tmp_path))


# ---------------------------------------------------------------- B blast radius
def test_a_stray_leaf_on_an_unstaged_crop_refuses():
    assert "tomato" not in p.CROPS
    msg = post_check(lambda q: crop(q, "cherry-tomato").update(difficulty="Hard"))
    assert "cherry-tomato: changed outside the staged ops" in msg


def test_a_stray_leaf_on_a_staged_crop_refuses():
    msg = post_check(lambda q: crop(q, "spinach").update(difficulty="Hard"))
    assert "spinach: changed outside the staged ops" in msg


def test_a_crop_added_to_the_roster_refuses():
    def m(q):
        g = copy.deepcopy(crop(q, "spinach")); g["slug"] = "ghost-crop"; q["crops"].append(g)
    assert "the roster changed" in post_check(m)


def test_an_unruled_catalog_id_refuses():
    msg = post_check(lambda q: q["source_catalog"].update(ghost_ext={"id": "ghost_ext", "tier": "T1"}))
    assert "not the ruled mints" in msg


def test_an_existing_catalog_entry_edited_refuses():
    msg = post_check(lambda q: q["source_catalog"]["umn_ext"].update(tier="T2"))
    assert "source_catalog umn_ext changed" in msg


# ---------------------------------------------------------------- S scope
def test_an_op_on_a_crop_outside_the_thirty_refuses():
    ops = copy.deepcopy(OPS)
    o = copy.deepcopy(op_of(ops, "sweet-pea", kind="enum"))
    o["crop"] = "okra"; o["old"] = "heat_tolerant"
    ops.append(o)
    assert "outside the 30 ruled crops" in refused(ops=ops)


def test_a_pause_op_on_a_held_crop_refuses():
    ops = copy.deepcopy(OPS)
    o = copy.deepcopy(op_of(ops, "carrot", kind="pause")); o["crop"] = "spinach"
    ops.append(o)
    assert "pause op on spinach" in refused(ops=ops)


def test_a_missing_field_op_refuses():
    ops = [o for o in OPS if not (o["crop"] == "dill" and o["kind"] == "field")]
    assert "dill: no sowing_heat_ceiling op" in refused(ops=ops)


def test_a_missing_pause_op_refuses():
    ops = [o for o in OPS if not (o["crop"] == "kale" and o["kind"] == "pause")]
    assert "kale: a pause op must exist exactly" in refused(ops=ops)


def test_an_op_outside_its_path_family_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "carrot", kind="pause"); o["path"] = "succession_policy.interval_weeks"; o["old"] = 3
    assert "outside the pause path family" in refused(ops=ops)


# ---------------------------------------------------------------- V / T / P
def test_new_not_old_plus_subs_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "spinach", "tips_by_stage.germination[0].text_seasoned")
    o["new"] = o["new"] + " Extra."
    assert "touched-leaf rule" in refused(ops=ops)


def test_a_sub_old_text_missing_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "borage", "tips_by_stage.germination[1].text_seasoned")
    o["subs"] = [["struggles in arctic cold", ""]]
    assert "occurs 0 times" in refused(ops=ops)


@pytest.mark.parametrize("bad,needle", [(" hot — dry", "dash"), (" 80 degrees", "°F"), (" a cultivar", "cultivar")])
def test_prose_rules_on_a_new_clause(bad, needle):
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "spinach", "tips_by_stage.germination[1].text_seasoned")
    o["subs"] = [[o["subs"][0][0], o["subs"][0][1] + bad]]
    o["new"] = o["old"].replace(o["subs"][0][0], o["subs"][0][1])
    assert needle in refused(ops=ops)


def test_a_no_op_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "borage", "tips_by_stage.germination[1].text_seasoned")
    o["subs"] = [[o["subs"][0][0], o["subs"][0][0]]]; o["new"] = o["old"]
    assert "a no-op (new == old)" in refused(ops=ops)


# ---------------------------------------------------------------- E evidence
def test_a_cited_clause_with_no_evidence_row_refuses():
    path = "tips_by_stage.germination[1].text_seasoned"
    ev = [r for r in EV if not (r["crop"] == "spinach" and r["entry_id"] == path)]
    assert "spinach " + path + ": a new clause with no EVIDENCE row" in refused(ev=ev)


def test_a_quote_not_in_the_hashed_bytes_refuses():
    ev = copy.deepcopy(EV)
    ev[0]["quote"] = "This sentence is on no page anywhere at all."
    assert "the quote is not in the cached bytes" in refused(ev=ev)


def test_an_evidence_row_at_a_url_the_block_does_not_anchor_refuses():
    ev = copy.deepcopy(EV)
    r = next(r for r in ev if r["crop"] == "spinach" and r["entry_id"].endswith("germination[0].text_seasoned")
             and r["source_id"] == "usu_ext")
    r["source_id"] = "uiuc_ext"
    assert "does not anchor uiuc_ext at the row's url" in refused(ev=ev)


def test_a_struck_edit_that_adds_words_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "borage", "tips_by_stage.germination[1].text_seasoned")
    o["subs"] = [[o["subs"][0][0], ", since heat is bad"]]
    o["new"] = o["old"].replace(o["subs"][0][0], ", since heat is bad")
    assert "a struck edit adds words" in refused(ops=ops)


def test_an_uncited_edit_without_its_decision_refuses():
    dec = [d for d in DEC if not (d["crop"] == "arugula" and d["path"] == "start_method.notes_seasoned")]
    assert "no evidence-only DECISIONS row" in refused(dec=dec)


def test_a_new_tip_source_without_evidence_refuses():
    ev = [r for r in EV if not (r["crop"] == "cabbage" and r["source_id"] == "umn_ext")]
    assert "the new tip cites umn_ext with no EVIDENCE row" in refused(ev=ev)


def test_an_added_anchor_with_no_evidence_refuses():
    ev = [r for r in EV if not (r["crop"] == "viola" and r["source_id"] == "ufifas_ext")]
    assert "added id ufifas_ext supports no EVIDENCE row" in refused(ev=ev)


def test_a_new_tip_appended_twice_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "kale", "tips_by_stage.harvest", "tip_add")
    o["new"] = o["new"] + [copy.deepcopy(o["new"][-1])]
    assert "append exactly one tip" in refused(ops=ops)


def test_a_new_tip_with_a_dash_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "kale", "tips_by_stage.harvest", "tip_add")
    o["new"][-1]["text_beginner"] += " Pick — now."
    assert "dash" in refused(ops=ops)


# ---------------------------------------------------------------- F field
def test_a_held_number_off_the_ruling_refuses():
    ops = copy.deepcopy(OPS)
    op_of(ops, "spinach", "sowing_heat_ceiling")["new"]["temp_f"] = 79
    msg = refused(ops=ops)
    assert "sowing_heat_ceiling_gate on the post roster" in msg and "temp_f 79 is not in the claim" in msg


def test_a_claim_not_in_its_page_refuses():
    ops = copy.deepcopy(OPS)
    op_of(ops, "beet", "sowing_heat_ceiling")["new"]["claim"] = "Temperatures above 80°F ruin beets entirely."
    assert "claim is not in the hashed bytes" in refused(ops=ops)


def test_heat_threshold_moved_refuses_as_blast_radius():
    # P4: heat_threshold_f is unchanged by this promote. No op kind may stage it, so blast radius is the guard.
    msg = post_check(lambda q: crop(q, "spinach").update(heat_threshold_f=80))
    assert "spinach: changed outside the staged ops: ['heat_threshold_f']" in msg


def test_a_held_crop_turned_null_breaks_the_ruled_split():
    ops = copy.deepcopy(OPS)
    f = op_of(ops, "radish", "sowing_heat_ceiling")["new"]
    for k in ("measures", "basis", "claim", "claim_source"):
        f.pop(k)
    f["temp_f"] = None
    msg = refused(ops=ops)
    assert "sowing_heat_ceiling population: held" in msg and "'radish'" in msg.split("not held")[1]


# ---------------------------------------------------------------- N enum
def test_an_enum_to_another_effect_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "nasturtium", kind="enum"); o["new"] = "bolting"
    assert "enum op on nasturtium" in refused(ops=ops)


def test_climate_stale_is_checked_on_the_post_roster(monkeypatch):
    monkeypatch.setitem(p.climate_threshold_gate.NULL_STRESS_KNOWN, ("borage", "quality_loss"), "injected")
    post = p.apply_to(PRE, OPS)
    with pytest.raises(Refused, match="climate_threshold_gate on the post roster"):
        p.check_post(PRE, post, OPS, EV, DEC, p.EVIDENCE)


# ---------------------------------------------------------------- D drops
def test_dropping_the_wrong_trigger_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "edamame", "weather_triggers")
    o["new"] = [x for x in o["old"] if x.get("condition") != "FROST_WARNING"]
    assert "not a ruled strike" in refused(ops=ops)


def test_dropping_two_triggers_refuses():
    ops = copy.deepcopy(OPS)
    o = op_of(ops, "chamomile", "weather_triggers")
    o["new"] = o["new"][1:]
    assert "remove exactly one trigger" in refused(ops=ops)


# ---------------------------------------------------------------- C catalog
def test_a_non_t1_mint_refuses():
    ops = copy.deepcopy(OPS)
    op_of(ops, p.CATALOG, "ucanr_pub7243")["new"]["tier"] = "T2"
    assert "catalog ucanr_pub7243: id/tier wrong" in refused(ops=ops)


def test_a_bare_host_mint_refuses():
    ops = copy.deepcopy(OPS)
    op_of(ops, p.CATALOG, "sare_necphm_arugula")["new"]["url"] = "https://www.sare.org/"
    assert "a minted id must be document-scoped" in refused(ops=ops)
