"""Suite for promote_pla673_glossary (PLA-673 glossary `hill` / `hilling`, PLA-674 soil_prep siblings on all 128
records, ten document-level catalog ids).

DEVIATION, recorded: the promote was written before this suite (no RED-first phase), as in Housekeeping 60 Phase C.
Stand-ins: POST_SHA was computed by tools/staging/pla673_glossary/build_stage.py's INDEPENDENT minimal apply (no
promote code) before the promote existed, and the mutation harness (mutate_promote_pla673_glossary.py) switches off
every guard one at a time. The pre-state is REPLAYED from its pinned commit (promote_fixture: 350eda38 -> ffbbc35),
never read live, so the suite survives this promote landing.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts
the refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, subprocess, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla673_glossary as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "350eda387fbed55464b16688a3bdc3263214b7c20631da98c7bbcb79f1d487c7"
POST_SHA = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"


@pytest.fixture(scope="module")
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope="module")
def stage():
    return P.load_stage(P.STAGE)


def _c(stage):
    ops, ev, dec = stage
    return copy.deepcopy(ops), copy.deepcopy(ev), copy.deepcopy(dec)


def _check(pre, ops, ev, dec, post=None):
    P.check_pre(pre, ops)
    post = P.apply_to(pre, ops) if post is None else post
    return P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def _refuses(match, pre, ops, ev, dec, post=None):
    with pytest.raises(Refused, match=match):
        _check(pre, ops, ev, dec, post)


def _post(pre, stage):
    return P.apply_to(pre, stage[0])


def _op(ops, crop, path):
    hits = [o for o in ops if o["crop"] == crop and o["path"] == path]
    assert len(hits) == 1, (crop, path)
    return hits[0]


def _gl(ops, tid):
    return _op(ops, "<glossary>", tid)["new"]


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["catalog"], n["glossary_terms"], n["glossary_sentences"]) == (268, 10, 2, 34)
    assert (n["siblings"], n["null_siblings"], n["evidence_rows"], n["decisions"]) == (256, 254, 78, 13)
    assert (n["hill_inspected"], n["gated_crops"]) == (232, 121)
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_check_post_alone_passes(pre, stage):
    n = _check(pre, *_c(stage))
    assert n["glossary_sentences"] == 34


# ---------------------------------------------------------------- loading / pre
def test_wrong_base_refuses(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="pinned to"):
        P.load_canonical(str(p))


def _write_stage(tmp_path, ops, ev=None, dec=None):
    (tmp_path / "ops.json").write_text(json.dumps(ops), encoding="utf-8")
    return str(tmp_path)


def test_empty_stage_refuses(tmp_path):
    with pytest.raises(Refused, match="names no op"):
        P.load_stage(_write_stage(tmp_path, []))


def test_unknown_kind_refuses(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "prose"
    with pytest.raises(Refused, match="unknown kind"):
        P.load_stage(_write_stage(tmp_path, ops))


def test_op_keys_must_be_exact(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["extra"] = 1
    with pytest.raises(Refused, match="keys must be exactly"):
        P.load_stage(_write_stage(tmp_path, ops))


def test_empty_reason_refuses(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["reason"] = " "
    with pytest.raises(Refused, match="empty reason"):
        P.load_stage(_write_stage(tmp_path, ops))


def test_op_staged_twice_refuses(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]) * 2
    with pytest.raises(Refused, match="staged twice"):
        P.load_stage(_write_stage(tmp_path, ops))


def test_old_must_be_absent(pre, stage):
    ops, ev, dec = _c(stage)
    ops[0]["old"] = None
    with pytest.raises(Refused, match="creates a key"):
        P.check_pre(pre, ops)


def test_existing_key_refuses(pre, stage):
    ops, ev, dec = _c(stage)
    p2 = copy.deepcopy(pre)
    P.by_slug(p2)["carrot"]["soil_prep_sources"] = None
    with pytest.raises(Refused, match="already exists"):
        P.check_pre(p2, ops)


def test_existing_catalog_id_refuses(pre, stage):
    ops, ev, dec = _c(stage)
    p2 = copy.deepcopy(pre)
    p2["source_catalog"]["umn_ext_leeks"] = {}
    with pytest.raises(Refused, match="already exists"):
        P.check_pre(p2, ops)


def test_sibling_may_only_create_the_two_keys(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "carrot", "soil_prep_sources")["path"] = "soil_prep_notes"
    with pytest.raises(Refused, match="may only create"):
        P.check_pre(pre, ops)


def test_sibling_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "carrot", "soil_prep_sources")["crop"] = "ghost-crop"
    with pytest.raises(Refused, match="is not a crop"):
        P.check_pre(pre, ops)


# ---------------------------------------------------------------- guard B
def test_roster_change(pre, stage):
    post = _post(pre, stage); post["crops"] = post["crops"][:-1]
    _refuses("roster changed", pre, *_c(stage), post=post)


def test_top_level_key_change(pre, stage):
    post = _post(pre, stage); post["extra_key"] = 1
    _refuses("top-level keys", pre, *_c(stage), post=post)


def test_top_level_value_change(pre, stage):
    post = _post(pre, stage); post["version"] = "x"
    _refuses("top-level 'version' changed", pre, *_c(stage), post=post)


def test_existing_catalog_entry_change(pre, stage):
    post = _post(pre, stage); post["source_catalog"]["umn_ext"]["name"] = "x"
    _refuses("existing catalog entry umn_ext changed", pre, *_c(stage), post=post)


def test_catalog_additions_must_be_the_staged_ops(pre, stage):
    post = _post(pre, stage); post["source_catalog"]["ghost_id"] = {"id": "ghost_id"}
    _refuses("catalog additions", pre, *_c(stage), post=post)


def test_stray_crop_change(pre, stage):
    post = _post(pre, stage); P.by_slug(post)["carrot"]["name"] = "Karrot"
    _refuses("changed paths", pre, *_c(stage), post=post)


# ---------------------------------------------------------------- guard V
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    post["source_catalog"]["umn_ext_leeks"] = dict(post["source_catalog"]["umn_ext_leeks"], tier="T2")
    _refuses("post value is not the op's `new`", pre, ops, ev, dec, post=post)


# ---------------------------------------------------------------- guard D
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "y", "reason": "z"})
    _refuses("which is not a crop", pre, ops, ev, dec)


# ---------------------------------------------------------------- evidence rows
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("duplicate row", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    ev[0]["quote"] = "this sentence is on no page at all, anywhere."
    _refuses("not in the cached bytes", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard S
def test_every_record_gets_both_siblings(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == "avocado")]
    _refuses("EVERY roster record", pre, ops, ev, dec)


def test_sibling_placement(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)
    c = P.by_slug(post)["carrot"]
    v = c.pop("soil_prep_sources"); c["soil_prep_sources"] = v
    _refuses("not placed right after", pre, ops, ev, dec, post=post)


def test_null_sibling_without_decision(pre, stage):
    ops, ev, dec = _c(stage)
    dec = [d for d in dec if d["decision"] != "null-not-assessed"]
    _refuses("null-not-assessed", pre, ops, ev, dec)


def test_sourced_pair_shape(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", "soil_prep_anchoring_urls")["new"] = None
    _refuses("non-empty list and a non-empty map", pre, ops, ev, dec)


def test_sourced_pair_ids_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", "soil_prep_sources")["new"] = ["clemson_hgic", "uga_ext"]
    _refuses("name different ids", pre, ops, ev, dec)


def test_sourced_id_not_in_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    o, a = _op(ops, "watermelon", "soil_prep_sources"), _op(ops, "watermelon", "soil_prep_anchoring_urls")
    o["new"] = ["ghost_src", "clemson_hgic"]
    a["new"] = {"ghost_src": a["new"]["uga_ext"], "clemson_hgic": a["new"]["clemson_hgic"]}
    _refuses("ghost_src is not a catalog id", pre, ops, ev, dec)


def test_sibling_anchor_unused(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == "watermelon" and r["source_id"] == "clemson_hgic")]
    _refuses("used by no EVIDENCE row", pre, ops, ev, dec)


def test_sibling_row_at_a_url_not_carried(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["crop"] == "watermelon")
    ev.append(dict(r, source_id="umn_ext", field="x"))
    _refuses("at a url the siblings do not carry", pre, ops, ev, dec)


def test_row_on_an_unstaged_entry(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["crop"] == "watermelon")
    ev.append(dict(r, entry_id="soil_prep_seasoned"))
    _refuses("sits on no staged op", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard GL
def test_glossary_ids_must_be_the_staged_terms(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops); post["glossary"]["ghost"] = post["glossary"]["hill"]
    _refuses("glossary ids", pre, ops, ev, dec, post=post)


def test_entry_keys_inner_id(pre, stage):
    ops, ev, dec = _c(stage)
    e = _gl(ops, "hill"); e["id"] = "hill"
    _refuses("seven ruled keys", pre, ops, ev, dec)


def test_entry_keys_order(pre, stage):
    ops, ev, dec = _c(stage)
    op = _op(ops, "<glossary>", "hill"); e = op["new"]
    op["new"] = {k: e[k] for k in reversed(list(e))}
    _refuses("seven ruled keys", pre, ops, ev, dec)


def test_term_must_be_its_id(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hill")["term"] = "Hill"
    _refuses("term 'Hill'", pre, ops, ev, dec)


def _retext(ops, ev, tid, reg, old, new):
    e = _gl(ops, tid); assert old in e[reg]; e[reg] = e[reg].replace(old, new)
    for r in ev:
        if r["crop"] == "<glossary>" and r["entry_id"].startswith(f"{tid}.{reg}[") and old in r["value"]:
            r["value"] = r["value"].replace(old, new)


def test_em_dash_in_a_definition(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "hill", "definition_beginner", "one spot.", "one spot — together.")
    _refuses("em or en dash", pre, ops, ev, dec)


def test_temperature_without_F(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "hill", "definition_beginner", "one spot.", "one spot at 70 degrees.")
    _refuses("without °F", pre, ops, ev, dec)


def test_sentence_numbering_gap(pre, stage):
    ops, ev, dec = _c(stage)
    for r in ev:
        if r["entry_id"] == "hill.definition_beginner[2]":
            r["entry_id"] = "hill.definition_beginner[9]"
    _refuses("numbered 1..n", pre, ops, ev, dec)


def test_rows_disagree_on_a_sentence(pre, stage):
    ops, ev, dec = _c(stage)
    rows = [r for r in ev if r["entry_id"] == "hill.definition_beginner[1]"]
    assert len(rows) > 1
    rows[1]["value"] = rows[1]["value"] + " Extra."
    _refuses("rows disagree", pre, ops, ev, dec)


def test_unevidenced_text_in_a_definition(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hilling")["definition_seasoned"] += " An unsourced sentence."
    _refuses("evidenced sentences joined", pre, ops, ev, dec)


def test_sources_and_anchors_order(pre, stage):
    ops, ev, dec = _c(stage)
    e = _gl(ops, "hill"); e["sources"] = list(reversed(e["sources"]))
    _refuses("different ids \\(or order\\)", pre, ops, ev, dec)


def test_glossary_source_not_in_catalog(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["kind"] == "catalog" and o["path"] == "umn_ext_cucumbers")]
    _refuses("umn_ext_cucumbers is not a catalog id", pre, ops, ev, dec)


def test_portal_id_refuses(pre, stage):
    """Glossary entries cite document-level ids only (STOP 2): a portal whose catalog url is not the page refuses."""
    ops, ev, dec = _c(stage)
    e = _gl(ops, "hill")
    i = e["sources"].index("umn_ext_cucumbers")
    e["sources"][i] = "umn_ext"
    e["anchoring_urls"] = {("umn_ext" if k == "umn_ext_cucumbers" else k): v for k, v in e["anchoring_urls"].items()}
    for r in ev:
        if r["source_id"] == "umn_ext_cucumbers":
            r["source_id"] = "umn_ext"
    _refuses("not a document-level id", pre, ops, ev, dec)


def test_glossary_source_unused(pre, stage):
    """A named, catalogued, correctly anchored source that no sentence's quote uses. (Removing a source's rows
    instead would empty a sentence and trip the numbering check first, masking this guard.)"""
    ops, ev, dec = _c(stage)
    e = _gl(ops, "hill")
    e["sources"].append("umn_ext_leeks")
    e["anchoring_urls"]["umn_ext_leeks"] = {"url": "https://extension.umn.edu/vegetables/growing-leeks", "verified": "2026-10-05"}
    _refuses("umn_ext_leeks is used by no EVIDENCE row", pre, ops, ev, dec)


def test_glossary_row_cites_an_unnamed_id(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["entry_id"].startswith("hilling.") and r["source_id"] == "umn_ext_leeks")
    ev.append(dict(r, entry_id="hill.definition_beginner[1]", value=next(
        x["value"] for x in ev if x["entry_id"] == "hill.definition_beginner[1]")))
    _refuses("which the entry does not name", pre, ops, ev, dec)


def test_glossary_row_url_not_its_anchor(pre, stage):
    """The row moves to the page's OTHER MANIFEST url (same bytes, so the quote still proves) while the anchor stays
    on the catalog url: only the row-url check can fire (the document-level check sees a correct anchor)."""
    ops, ev, dec = _c(stage)
    alias = "https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/growing-potatoes"
    r = next(r for r in ev if r["source_id"] == "umn_ext_potatoes")
    r["url"] = alias
    _refuses("row's url is not umn_ext_potatoes's anchor", pre, ops, ev, dec)


def test_glossary_row_names_no_term(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["entry_id"] == "hill.definition_beginner[1]")
    ev.append(dict(r, entry_id="ghost.definition_beginner[1]"))
    _refuses("names no staged term", pre, ops, ev, dec)


def test_glossary_sources_must_be_non_empty(pre, stage):
    ops, ev, dec = _c(stage)
    e = _gl(ops, "hill"); e["sources"] = []; e["anchoring_urls"] = {}
    _refuses("sources must be a non-empty list", pre, ops, ev, dec)


def test_field_additions_shape(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hill")["field_additions"][0]["sources"].append("ghost_src")
    _refuses("field_additions entry", pre, ops, ev, dec)


def test_field_additions_empty(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hill")["field_additions"] = []
    _refuses("field_additions must be a non-empty list", pre, ops, ev, dec)


def test_match_must_classify_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hill")["match"][0]["crops"].remove("watermelon")
    _refuses("glossary match: UNCLASSIFIED", pre, ops, ev, dec)


def test_match_exclusions_must_agree(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hilling")["match"][0]["exclusions"].pop()
    _refuses("glossary match: .*exclusions differ", pre, ops, ev, dec)


def test_match_inner_id_refuses(pre, stage):
    ops, ev, dec = _c(stage)
    _gl(ops, "hill")["match"][0]["id"] = "hill"
    _refuses("glossary match: .*one matcher", pre, ops, ev, dec)


def test_match_population_floor(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "HILL_POPULATION", 233)
    _refuses("glossary match", pre, ops, ev, dec)


def test_match_population_must_be_exact(pre, stage, monkeypatch):
    """Above the floor but not the pinned population (232 vs 231): only the exact check can fire."""
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "HILL_POPULATION", 231)
    _refuses("inspected 232 consumer leaves, not 231", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def test_catalog_id_must_match(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "usu_ext_leeks")["new"]["id"] = "usu_leeks"
    _refuses("its id is 'usu_leeks'", pre, ops, ev, dec)


def test_catalog_url_needs_a_manifest_row(pre, stage):
    """A staged mint the glossary does not cite (so GL never looks at it) whose url has no MANIFEST row."""
    ops, ev, dec = _c(stage)
    ops.append({"crop": "<catalog>", "path": "ghost_mint", "kind": "catalog", "old": "<absent>",
                "new": {"id": "ghost_mint", "url": "https://example.edu/never-hashed"}, "cited_at": None, "reason": "test"})
    _refuses("ghost_mint: its url has no MANIFEST row", pre, ops, ev, dec)


def test_catalog_mint_must_be_evidenced(pre, stage):
    ops, ev, dec = _c(stage)
    ops.append({"crop": "<catalog>", "path": "ghost_mint", "kind": "catalog", "old": "<absent>",
                "new": {"id": "ghost_mint", "url": "https://extension.umn.edu/vegetables/growing-leeks"},
                "cited_at": None, "reason": "test"})
    _refuses("ghost_mint: no EVIDENCE row cites it", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G
class _R:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_gate_failure(pre, stage, monkeypatch):
    post = _post(pre, stage)
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(1, "gate_all: 1 of 121 certified crop(s) FAILED"))
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(post)


def test_gate_population_must_be_reported(pre, stage, monkeypatch):
    post = _post(pre, stage)
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "all good"))
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(post)


def test_gate_population_must_match_the_roster(pre, stage, monkeypatch):
    post = _post(pre, stage)
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "gate_all: ran whole_crop_gate on 3 certified crop(s)"))
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(post)
