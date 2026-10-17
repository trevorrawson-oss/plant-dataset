"""PLA-608 Part 2: tools/rootstock_prose_gate.py -- a rootstock named in prose must be a row of that crop's list.

Pins the live measurement (canonical 5420479d: 21 crops by identity, 515 fields, 272 names, 253 matched, 19 waived;
PLA-625 stop 2 moved own-root wording to a propagation-mode list: 260 names, 248 matched, 12 waived; PLA-625 citrus
promote 1 (2f67359e) re-authored orange-navel's and grapefruit's rows and notes: 268 names, 258 matched, 10 waived;
promote 2 (ef1a4d35) re-authored lemon's and lime's and added two rows: 521 fields, 294 names, 288 matched, 6 waived),
proves every guard family on a SCRATCH COPY, carries PLA-608's six named injections, and drives the two entry points
(whole_crop_gate A64, gate_all's roster half) as subprocesses. Run under pytest (def test_), via
tools/run_test_tree.py --files. Mutation harness: tools/mutate_rootstock_prose_gate.py.
"""
import copy, json, os, re, subprocess, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import rootstock_prose_gate as G  # noqa: E402

DATA = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
LIVE = G.roster(DATA)


def fresh():
    return copy.deepcopy(DATA)


def by(d):
    return {c["slug"]: c for c in d["crops"]}


def row(crop, name):
    return next(r for r in crop["rootstock_options"] if r.get("name") == name)


def viol(d, slug):
    return G.crop_violations(by(d)[slug])


# ------------------------------------------------------------------ the live measurement (inspected-nothing is not clean)
def test_the_ledger_was_measured_on_this_canonical_family():
    # re-measured on 5420479d (stop-1 ruling: NOT copied from the ticket)
    assert G._K.MEASURED_ON.startswith("5420479d")
    assert len(G._K.WAIVERS) == 6
    assert len({(w["crop"], w["field"], w["name"], w["sentence"]) for w in G._K.WAIVERS}) == 6, "duplicate waiver"
    for w in G._K.WAIVERS:
        assert w["ticket"] in ("PLA-608", "PLA-566", "PLA-612") and w["reason"].strip(), w


def test_population_is_the_21_crops_carrying_the_field_by_identity():
    want = sorted(c["slug"] for c in DATA["crops"] if "rootstock_options" in c)
    assert sorted(G.KNOWN_POPULATION) == want
    assert len(want) == 21
    assert (LIVE["carrying"], LIVE["inspected"]) == (21, 21)
    assert LIVE["new_crops"] == [] and LIVE["lost_crops"] == []
    # the two shells (avocado, olive) are IN the population: gate_all's per-crop pass runs certified crops only
    assert {"avocado", "olive"} <= G.KNOWN_POPULATION


def test_inspected_fields_and_names_are_the_measurement():
    assert LIVE["fields"] == 521
    assert LIVE["mentions"] == 294
    assert LIVE["matched"] == 288
    assert G.refusal(LIVE) is None


def test_live_unresolved_equals_the_waiver_ledger_exactly():
    got = {G.waiver_key(m) for m in LIVE["unresolved"]}
    assert got == set(G.KNOWN)
    assert LIVE["violations"] == [] and LIVE["stale"] == []


def test_the_pla608_part1_hits_are_in_the_ledger_and_st_julien_is_retired():
    names = {(w["crop"], w["name"]) for w in G._K.WAIVERS}
    for hit in [("plum", "Lovell"), ("plum", "Halford"), ("apricot", "Nemaguard"), ("pear-asian", "quince")]:
        assert hit in names, hit
    # lemon's macrophylla / rough lemon and lime's alemow / Rangpur lime note waivers were retired BY CONTENT in PLA-625
    # citrus promote 2 (ef1a4d35): both notes re-authored, lemon gained its rough lemon / macrophylla row and lime its
    # alemow row; each went STALE on the post-state and moved to CLOSED
    closed = {(w["crop"], w["name"]) for w in G._K.CLOSED}
    for hit in [("lime", "alemow"), ("lime", "Rangpur lime"), ("lemon", "macrophylla"), ("lemon", "rough lemon")]:
        assert hit in closed and hit not in names, hit
    assert not any(m["crop"] in ("lemon", "lime") for m in LIVE["unresolved"])
    # plum's note St. Julien was retired BY CONTENT in PLA-626 (00dda31c): no waiver, and no live mention
    assert not any(w["crop"] == "plum" and "Julien" in w["name"] for w in G._K.WAIVERS)
    assert not any(m["crop"] == "plum" and m["id"] == "st_julien" for m in LIVE["unresolved"])
    # grapefruit's two sour orange note waivers were retired BY CONTENT in PLA-625 citrus promote 1 (2f67359e): the
    # note was re-authored without sour orange, both waivers went STALE on the post-state and were deleted
    assert not any(w["crop"] == "grapefruit" for w in G._K.WAIVERS)
    assert not any(m["crop"] == "grapefruit" for m in LIVE["unresolved"])
    assert "sour orange" not in by(fresh())["grapefruit"]["recommended_rootstock_note"].lower()


def test_the_new_container_notes_hit_is_apple_m27():
    """The stop-1 widening (container_notes, PLA-626 close-out) found apple's two M27 strings."""
    m27 = [w for w in G._K.WAIVERS if w["crop"] == "apple"]
    assert sorted(w["field"] for w in m27) == ["container_notes.notes_beginner", "container_notes.notes_seasoned"]
    assert all(w["name"] == "M27" for w in m27)


# ------------------------------------------------------------------ the table
def test_every_live_row_name_is_known_to_the_table():
    """The stated limit is 'names on no list pass silently'; a ROW the table cannot read would make every prose name
    of that stock fail OR (worse) a renamed row resolve nothing. Every live row name must read as at least one stock."""
    for c in DATA["crops"]:
        for r in c.get("rootstock_options") or []:
            n = r.get("name")
            assert G.names_in(n) or n.strip().lower() in G.ROW_NAME_ALIASES, (c["slug"], n)


@pytest.mark.parametrize("text,sid", [
    ("Citrus macrophylla", "alemow"), ("alemow", "alemow"), ("alemeow", "alemow"),
    ("Myrobalan 29C", "myrobalan"), ("P. cerasifera", "myrobalan"), ("St. Julien A", "st_julien"),
    ("P. insititia", "st_julien"), ("Poncirus trifoliata", "trifoliate_orange"), ("Citrus trifoliata", "trifoliate_orange"),
    ("C. aurantium", "sour_orange"), ("Citrus jambhiri", "rough_lemon"), ("C. volkameriana", "volkamer"),
    ("Old Home x Farmingdale", None), ("betulaefolia", "betulifolia"), ("D. virginiana", "american_persimmon"),
    ("date-plum", "date_plum"), ("Asimina triloba seedling", "pawpaw_seedling"), ("Swingle citrumelo", "swingle"),
])
def test_synonyms_name_the_same_stock(text, sid):
    hits = G.names_in(text)
    assert len(hits) == 1, (text, hits)
    if sid:
        assert hits[0][2:4] == ("stock", sid)


def test_longest_match_wins():
    """'Swingle citrumelo' is ONE stock, not swingle + the citrumelo family term."""
    assert [h[3] for h in G.names_in("ask for Swingle citrumelo")] == ["swingle"]
    assert [h[3] for h in G.names_in("Trifoliate-orange hybrids resist")] == ["trifoliate_hybrid"]


def test_a_family_term_resolves_through_any_member_row():
    stocks = {"gisela_5"}
    assert G.resolves("family", "gisela", stocks, set())
    assert not G.resolves("family", "gisela", {"mazzard"}, set())


def test_a_member_named_resolves_only_to_itself():
    assert not G.resolves("stock", "gisela_6", {"gisela_5"}, {"gisela"})
    assert not G.resolves("stock", "carrizo", {"swingle"}, {"trifoliate_hybrid"})


def test_selection_of_is_one_way():
    assert G.resolves("stock", "trifoliate_orange", {"flying_dragon"}, set())
    assert not G.resolves("stock", "flying_dragon", {"trifoliate_orange"}, set())


def test_cultivars_are_never_read_as_rootstocks():
    # exactly two cultivar hits (an all() over an empty list was vacuous: the emptied deny-list survived it)
    assert [(h[2], h[4]) for h in G.names_in("North Star and Meteor")] == [("cultivar", "North Star"), ("cultivar", "Meteor")]
    d = fresh()
    by(d)["peach"]["recommended_rootstock_note"] += " Meteor and North Star are cultivars."
    assert viol(d, "peach") == []


# ------------------------------------------------------------------ own-root wording is a propagation mode (stop-2 ruling)
# PLA-625 stop 2, ruling 1b (2026-10-13): own-root wording names how a tree is propagated, not a rootstock (PLA-464
# retired propagation modes from rootstock_options), so it sits on a printed list beside the cultivar deny-list.
OWN_ROOT_TERMS = ["own roots", "own root", "own-root", "own-rooted", "ungrafted", "cutting-grown", "from cuttings",
                  "from hardwood cuttings"]
# The 7 waivers the ruling deleted, kept here so their retirement stays proven: each one is STALE on the live data.
RETIRED_OWN_ROOT = {
    ("lime", "recommended_rootstock_note", "own roots",
     "Key lime is often grown on its own roots from seed, cuttings, or air-layers rather than grafted."),
    ("persimmon", "rootstock_options[name=Diospyros virginiana (American persimmon)].traits_seasoned", "own roots",
     "Native D. virginiana is very cold-hardy and more tolerant of heavy, wet soils and root rot than kaki on its own "
     "roots, and it improves anchorage."),
    ("persimmon", "rootstock_options[name=Diospyros virginiana (American persimmon)].traits_beginner", "own roots",
     "Native persimmon roots are very cold-hardy and handle heavy, wet soil and root rot better than the Asian type on "
     "its own roots."),
    ("mulberry", "recommended_rootstock_note", "from hardwood cuttings",
     "Mulberries root readily from hardwood cuttings, so many are grown own-root; named cultivars are also grafted or "
     "budded onto seedling Morus alba or rubra, mainly for propagation, not to dwarf the tree."),
    ("mulberry", "recommended_rootstock_note", "own-root",
     "Mulberries root readily from hardwood cuttings, so many are grown own-root; named cultivars are also grafted or "
     "budded onto seedling Morus alba or rubra, mainly for propagation, not to dwarf the tree."),
    ("mulberry", "recommended_rootstock_note", "own-root",
     "On an own-root tree there is no graft union to keep above the soil, and any suckers are the same variety."),
    ("pawpaw", "recommended_rootstock_note", "ungrafted",
     "An ungrafted seedling is a cheaper way to a tree, but expect variable fruit and a wait of about 5 to 8 years "
     "instead of around 4 for a grafted variety."),
}


@pytest.mark.parametrize("text", OWN_ROOT_TERMS)
def test_own_root_wording_is_a_propagation_mode_not_a_stock(text):
    hits = G.names_in(text)
    assert [(h[2], h[3]) for h in hits] == [("propagation", None)], (text, hits)


def test_seedling_is_not_a_propagation_mode():
    """'seedling' is a real row name on some crops (apple's row is named just that), so it stays off the list."""
    assert not any(re.search(p, "seedling", re.I) for p in G.PROPAGATION_MODES)
    assert G.names_in("a seedling") == []
    assert [h[3] for h in G.names_in("an apple seedling")] == ["apple_seedling"]


def test_own_root_prose_is_never_a_violation_and_never_hides_a_stock():
    d = fresh()
    assert by(d)["fig"]["rootstock_options"] == [] and viol(d, "fig") == []
    by(d)["peach"]["recommended_rootstock_note"] += " Some peaches grow on their own roots, ungrafted, from cuttings."
    assert viol(d, "peach") == []
    # the list hides only the mode: a stock in the same sentence still fails
    by(d)["peach"]["recommended_rootstock_note"] += " Own-root trees beat St. Julien."
    v = viol(d, "peach")
    assert len(v) == 1 and "'St. Julien'" in v[0], v


def test_no_live_mention_is_a_propagation_mode():
    ms = [m for c in DATA["crops"] if G.has_field(c) for m in G.scan_crop(c)[0]]
    assert ms and not any(m["kind"] == "propagation" for m in ms)
    assert not any(re.search(p, w["name"], re.I) for w in G._K.WAIVERS for p in G.PROPAGATION_MODES)


def test_the_seven_own_root_waivers_are_STALE_and_deleted():
    """Ruling 1b: prove each STALE, then delete it in the same commit."""
    assert not (RETIRED_OWN_ROOT & set(G.KNOWN))
    known = dict(G.KNOWN)
    known.update({k: {"ticket": "PLA-608", "reason": "retired"} for k in RETIRED_OWN_ROOT})
    r = G.roster(DATA, known)
    assert set(r["stale"]) == RETIRED_OWN_ROOT
    assert r["violations"] == []


# ------------------------------------------------------------------ closed by content: kept by identity for the era
# A waiver retired BY CONTENT (the prose changed) still fires on every post-state before that promote, so a LANDED
# promote replaying one gates against the set live in its era (KNOWN_AT_ARMING = KNOWN + CLOSED), the A62 precedent
# (e47e58a). The default follows the era switch A62 binds (whole_crop_gate / gate_all run A64 as subprocesses). The 7
# own-root waivers are NOT closed: they were retired by a gate change and fire on no earlier state either. Measured RED
# 2026-10-14: the full tree on 5603b28 failed 40 tests, grapefruit's sour orange pair among the replays' violations.
P1_BASE = "59010fe6994b95eb52407fa60a6995eedefe5636bd6a52d2f960d4b08641cf68"   # PLA-625 citrus promote 1's base
SOUR_ORANGE = {("grapefruit", "recommended_rootstock_note", "sour orange"),
               ("grapefruit", "recommended_rootstock_note", "Sour orange")}
LEMON_LIME = {("lemon", "recommended_rootstock_note", "macrophylla"), ("lemon", "recommended_rootstock_note", "rough lemon"),
              ("lime", "recommended_rootstock_note", "alemow"), ("lime", "recommended_rootstock_note", "Rangpur lime")}


@pytest.fixture(scope="module")
def p1_base():
    import promote_fixture
    return json.loads(promote_fixture.pre_state(P1_BASE))


@pytest.fixture
def era(monkeypatch):
    import sourced_block_ratchet_gate as SBR
    monkeypatch.delenv(SBR.ERA_ENV, raising=False)
    monkeypatch.setattr(SBR, "_ERA_BOUND", None)
    return SBR


def test_closed_is_the_sour_orange_pair_and_the_lemon_lime_four_disjoint_and_the_arming_set_is_12():
    closed = {(w["crop"], w["field"], w["name"]) for w in G._K.CLOSED}
    assert closed == SOUR_ORANGE | LEMON_LIME
    assert not (set(G.KNOWN) & set(G.CLOSED))
    assert set(G.KNOWN_AT_ARMING) == set(G.KNOWN) | set(G.CLOSED)
    assert len(G.KNOWN_AT_ARMING) == 12
    for w in G._K.CLOSED:
        want = "PLA-612" if w["crop"] == "grapefruit" else "PLA-608"
        assert w["closed_by"].strip() and w["ticket"] == want, w


def test_on_promote_1s_base_the_live_set_flags_exactly_the_closed_six(p1_base, era):
    v = G.roster(p1_base)["violations"]
    assert len(v) == 6 and all(" recommended_rootstock_note: names '" in x for x in v), v
    assert {(x.split(" ")[0], x.split("'")[1]) for x in v} == {(c, n) for c, _f, n in SOUR_ORANGE | LEMON_LIME}


def test_on_promote_1s_base_the_era_set_flags_none(p1_base, era):
    r = G.roster(p1_base, G.KNOWN_AT_ARMING)
    assert r["violations"] == [] and r["stale"] == []


def test_the_live_canonical_needs_no_era_set(era):
    assert G.roster(DATA)["violations"] == []


def test_the_default_follows_the_bound_era_switch(p1_base, era, monkeypatch):
    monkeypatch.setenv(era.ERA_ENV, P1_BASE)
    monkeypatch.setattr(era, "_ERA_BOUND", P1_BASE)
    assert G.roster(p1_base)["violations"] == []


def test_the_switch_set_but_never_bound_refuses(p1_base, era, monkeypatch):
    monkeypatch.setenv(era.ERA_ENV, P1_BASE)
    with pytest.raises(era.EraRefused):
        G.roster(p1_base)


def test_a_row_named_only_seedling_holds_apple_seedling():
    """apple's row is named just "seedling" (ROW_NAME_ALIASES): apple prose naming its seedling stock resolves there,
    and the same sentence on a crop without that row fails."""
    d = fresh()
    by(d)["apple"]["recommended_rootstock_note"] += " An apple seedling rootstock makes the largest tree."
    assert viol(d, "apple") == []
    by(d)["pear-european"]["recommended_rootstock_note"] += " An apple seedling rootstock makes the largest tree."
    assert any("apple seedling" in v for v in viol(d, "pear-european"))


# ------------------------------------------------------------------ PARENTAGE (PLA-625 promote 2 amendment, 2026-10-16)
PARENT_SENTENCE = "Swingle is a citrumelo, a cross of Duncan grapefruit and trifoliate orange."
LIME_SWINGLE = "Swingle citrumelo (trifoliate hybrid)"


def _lime_with(where):
    """A scratch copy whose lime carries PARENT_SENTENCE at `where` (lime has no trifoliate or Flying Dragon row)."""
    d = fresh()
    lime = by(d)["lime"]
    assert not ({"trifoliate_orange", "flying_dragon"} & G.row_index(lime)[0])
    if where == "swingle_row":
        row(lime, LIME_SWINGLE)["traits_seasoned"] = PARENT_SENTENCE
    elif where == "note":
        lime["recommended_rootstock_note"] += " " + PARENT_SENTENCE
    elif where == "alemow_row":
        lime["rootstock_options"].append({"name": "Alemow (Citrus macrophylla)", "traits_seasoned": PARENT_SENTENCE})
    elif where == "container_notes":
        lime["container_notes"]["notes_seasoned"] += " " + PARENT_SENTENCE
    return d


def test_parentage_is_the_ruled_table():
    """Exactly the two hybrids the amendment names, each parent set as ruled."""
    assert {s: tuple(e["parents"]) for s, e in G.PARENTAGE.items()} == {
        "swingle": ("Duncan grapefruit", "trifoliate orange"),
        "carrizo": ("Washington navel orange", "trifoliate orange")}
    assert G.parent_stocks({"swingle"}) == {"trifoliate_orange"}
    assert G.parent_stocks({"carrizo"}) == {"trifoliate_orange"}
    assert G.parent_stocks({"rough_lemon", "alemow"}) == set()


def test_parentage_basis_is_in_cached_t1_bytes():
    """Entered only from cached T1 bytes: every basis quote is in the hashed, MANIFEST-listed page it names."""
    from cited_promote_common import cached_quote, manifest
    ev = os.path.join(HERE, ".evidence_cache")
    man, cache = manifest(ev), {}
    n = 0
    for sid, e in G.PARENTAGE.items():
        assert e["basis"], sid
        for label, url, sha, quote in e["basis"]:
            cached_quote({"url": url, "sha256": sha, "quote": quote}, man, ev, cache, f"{sid} {label}")
            n += 1
    assert n == 3


def test_a_hybrids_own_row_may_name_its_parent():
    assert viol(_lime_with("swingle_row"), "lime") == []


@pytest.mark.parametrize("where", ["note", "alemow_row", "container_notes"])
def test_the_parent_named_anywhere_else_still_FAILS(where):
    v = viol(_lime_with(where), "lime")
    assert len(v) == 1 and "names 'trifoliate orange'" in v[0], v


def test_a_parent_not_in_the_table_FAILS():
    d = fresh()
    row(by(d)["lime"], LIME_SWINGLE)["traits_seasoned"] = "Swingle is a cross of sour orange and Cleopatra mandarin."
    v = viol(d, "lime")
    assert sorted(re.findall(r"names '([^']+)'", " ".join(v))) == ["Cleopatra mandarin", "sour orange"], v


def test_emptying_the_table_makes_lime_FAIL(monkeypatch):
    monkeypatch.setattr(G, "PARENTAGE", {})
    v = viol(_lime_with("swingle_row"), "lime")
    assert len(v) == 1 and "names 'trifoliate orange'" in v[0], v


# ------------------------------------------------------------------ PLA-608's six named injections
def test_injection_1_st_julien_into_peachs_note_FAILS():
    d = fresh()
    by(d)["peach"]["recommended_rootstock_note"] += " St. Julien is another option."
    v = viol(d, "peach")
    assert len(v) == 1 and "'St. Julien'" in v[0] and "recommended_rootstock_note" in v[0]


def test_injection_2_deleting_a_row_the_note_names_FAILS():
    d = fresh()
    c = by(d)["lemon"]
    c["rootstock_options"] = [r for r in c["rootstock_options"] if not r["name"].startswith("sour orange")]
    v = viol(d, "lemon")
    assert any("'sour orange'" in x and "recommended_rootstock_note" in x for x in v), v


def test_injection_3_renaming_a_row_to_a_synonym_PASSES():
    """Positive control for the table: plum's prose says 'Myrobalan'; the row renamed to its botanical synonym still
    resolves it."""
    d = fresh()
    c = by(d)["plum"]
    row(c, "Myrobalan 29C (P. cerasifera)")["name"] = "Prunus cerasifera"
    assert "Myrobalan" in c["recommended_rootstock_note"]
    assert viol(d, "plum") == []


def test_injection_4_a_crop_gaining_the_field_moves_the_population():
    d = fresh()
    c = by(d)["cabbage"]
    assert "rootstock_options" not in c
    c["rootstock_options"] = [{"name": "Lovell", "traits_seasoned": "St. Julien is not on this list."}]
    r = G.roster(d)
    assert (r["carrying"], r["inspected"]) == (22, 22)
    assert r["new_crops"] == ["cabbage"]
    assert G.refusal(r) is None
    assert any(v.startswith("cabbage ") and "St. Julien" in v for v in r["violations"]), "the new crop is inspected"


def test_injection_5_strip_one_add_one_REFUSES():
    d = fresh()
    del by(d)["mulberry"]["rootstock_options"]
    by(d)["cabbage"]["rootstock_options"] = []
    r = G.roster(d)
    assert r["carrying"] == 21, "the count holds, so a count floor would pass"
    assert r["lost_crops"] == ["mulberry"]
    assert "mulberry" in (G.refusal(r) or "")


def test_injection_6_rewording_the_pear_asian_exclusion_goes_STALE_and_FAILS():
    d = fresh()
    c = by(d)["pear-asian"]
    old = "so it is not an option here."
    assert c["recommended_rootstock_note"].count(old) == 1
    c["recommended_rootstock_note"] = c["recommended_rootstock_note"].replace(old, "so it can work here.")
    r = G.roster(d)
    assert any(k[0] == "pear-asian" and k[2] == "quince" for k in r["stale"]), r["stale"]
    assert any(v.startswith("pear-asian ") and "'quince'" in v for v in r["violations"]), r["violations"]


# ------------------------------------------------------------------ reach: every field the rule names is read
@pytest.mark.parametrize("path", [
    ("recommended_rootstock_note",),
    ("rootstock_options", 0, "traits_seasoned"),
    ("rootstock_options", 0, "traits_beginner"),
    ("rootstock_options", 0, "what_to_ask_nursery"),
    ("container_notes", "notes_seasoned"),
    ("container_notes", "overwintering", "approach_seasoned"),
])
def test_every_named_field_is_read(path):
    d = fresh()
    o = by(d)["orange-navel"]
    for k in path[:-1]:
        o = o[k]
    o[path[-1]] = (o.get(path[-1]) or "") + " Ask about St. Julien too."
    v = viol(d, "orange-navel")
    assert len(v) == 1 and "St. Julien" in v[0], (path, v)


def test_recommended_rootstock_itself_is_not_read():
    """REFUSAL-SPEC: the value field belongs to PLA-589 (held). A green here is the ruling, not vacuity."""
    d = fresh()
    by(d)["lemon"]["recommended_rootstock"] = "St. Julien A"
    assert viol(d, "lemon") == []


def test_citation_keys_and_varieties_are_not_read():
    d = fresh()
    c = by(d)["orange-navel"]
    c["container_notes"]["sources_note_provenance"] = "St. Julien"
    c.setdefault("varieties", {})["notes_x"] = "St. Julien"
    assert viol(d, "orange-navel") == []


def test_a_crop_without_the_field_is_a_no_op():
    assert G.crop_violations(by(DATA)["cabbage"]) == []


# ------------------------------------------------------------------ waivers: identity AND character
def test_a_waived_name_in_a_reworded_sentence_FAILS():
    """Retargeted to plum's Lovell / Halford waivers when lemon's note waivers closed (PLA-625 citrus promote 2)."""
    d = fresh()
    w = next(w for w in G._K.WAIVERS if w["crop"] == "plum" and w["name"] == "Lovell")
    r = next(r for r in by(d)["plum"]["rootstock_options"] if w["field"].startswith(f"rootstock_options[name={r['name']}]"))
    assert w["sentence"] in r["traits_seasoned"]
    r["traits_seasoned"] = r["traits_seasoned"].replace(w["sentence"], w["sentence"].replace("Peach-seedling", "Peach seedling", 1))
    v = viol(d, "plum")
    assert any("'Lovell'" in x for x in v) and any("'Halford'" in x for x in v), v


def test_a_waiver_does_not_cover_the_same_name_on_another_crop():
    d = fresh()
    w = next(w for w in G._K.WAIVERS if w["crop"] == "plum" and w["name"] == "Lovell")
    by(d)["orange-navel"]["recommended_rootstock_note"] += " " + w["sentence"]
    assert any("'Lovell'" in x for x in viol(d, "orange-navel"))


def test_a_waiver_whose_name_now_resolves_is_STALE():
    """A content fix (add the row) retires its waiver: the gate reports it STALE, and main() exits 1 until deleted."""
    d = fresh()
    by(d)["apricot"]["rootstock_options"].append({"name": "Nemaguard"})
    r = G.roster(d)
    assert [k[:3] for k in r["stale"]] == [("apricot", "rootstock_options[name=Lovell (peach seedling)].traits_seasoned",
                                            "Nemaguard")]
    assert r["violations"] == []


# ------------------------------------------------------------------ refusals
def test_zero_population_REFUSES():
    d = fresh()
    d["crops"] = []
    assert "inspected 0" in G.refusal(G.roster(d))


def test_a_lost_crop_REFUSES_even_when_others_remain():
    d = fresh()
    del by(d)["olive"]["rootstock_options"]
    assert "olive" in G.refusal(G.roster(d))


# ------------------------------------------------------------------ the entry points
def _write(tmp_path, d):
    p = tmp_path / "canon.json"
    p.write_text(json.dumps(d, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    return str(p)


def _run(args):
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def test_cli_live_passes_and_prints_its_population_and_limit():
    rc, out = _run([os.path.join(HERE, "rootstock_prose_gate.py")])
    assert rc == 0, out
    assert "inspected 21 crops carrying rootstock_options (of 21), 521 fields, 294 rootstock names (288 matched a row)" in out
    assert G.LIMIT_LINE in out
    assert G.PROPAGATION_LINE in out and "ungrafted" in G.PROPAGATION_LINE
    assert G.PARENTAGE_LINE in out and "swingle: Duncan grapefruit, trifoliate orange" in G.PARENTAGE_LINE


def test_cli_exit_codes(tmp_path):
    d = fresh()
    by(d)["peach"]["recommended_rootstock_note"] += " St. Julien too."
    rc, out = _run([os.path.join(HERE, "rootstock_prose_gate.py"), _write(tmp_path, d)])
    assert rc == 1 and "VIOLATION: peach recommended_rootstock_note" in out, out
    d = fresh()
    d["crops"] = []
    rc, out = _run([os.path.join(HERE, "rootstock_prose_gate.py"), _write(tmp_path, d)])
    assert rc == 2 and "REFUSED" in out, out
    d = fresh()
    by(d)["apricot"]["rootstock_options"].append({"name": "Nemaguard"})
    rc, out = _run([os.path.join(HERE, "rootstock_prose_gate.py"), _write(tmp_path, d)])
    assert rc == 1 and "STALE waiver (PLA-566): apricot" in out, out


def test_whole_crop_gate_A64_fails_by_name(tmp_path):
    d = fresh()
    by(d)["peach"]["recommended_rootstock_note"] += " St. Julien is another option."
    rc, out = _run([os.path.join(HERE, "whole_crop_gate.py"), "peach", _write(tmp_path, d)])
    assert rc != 0, out
    assert "A64. rootstock prose" in out
    assert "rootstock-prose: peach recommended_rootstock_note: names 'St. Julien'" in out, out[-3000:]


def test_whole_crop_gate_A64_live_prints_its_counts():
    rc, out = _run([os.path.join(HERE, "whole_crop_gate.py"), "lime"])
    assert rc == 0, out[-3000:]
    assert "A64. rootstock prose" in out and "rootstock names: 23 (23 matched a row); violations: 0" in out


def test_gate_all_runs_the_roster_half_on_a_SHELL(tmp_path):
    """olive is a shell: gate_all's per-crop pass never runs whole_crop_gate on it, so only the roster half sees it."""
    d = fresh()
    assert by(d)["olive"]["verification_status"]["status"] != "verified_gs_arc"
    by(d)["olive"]["recommended_rootstock_note"] = "Olives are sometimes grafted onto St. Julien."
    rc, out = _run([os.path.join(HERE, "gate_all.py"), _write(tmp_path, d)])
    assert rc == 1, out[-3000:]
    assert "VIOLATION: rootstock_prose_gate: olive recommended_rootstock_note" in out, out[-3000:]
