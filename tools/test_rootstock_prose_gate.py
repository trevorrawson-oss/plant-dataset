"""PLA-608 Part 2: tools/rootstock_prose_gate.py -- a rootstock named in prose must be a row of that crop's list.

Pins the live measurement (canonical 5420479d: 21 crops by identity, 515 fields, 272 names, 253 matched, 19 waived),
proves every guard family on a SCRATCH COPY, carries PLA-608's six named injections, and drives the two entry points
(whole_crop_gate A64, gate_all's roster half) as subprocesses. Run under pytest (def test_), via
tools/run_test_tree.py --files. Mutation harness: tools/mutate_rootstock_prose_gate.py.
"""
import copy, json, os, subprocess, sys

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
    assert len(G._K.WAIVERS) == 19
    assert len({(w["crop"], w["field"], w["name"], w["sentence"]) for w in G._K.WAIVERS}) == 19, "duplicate waiver"
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
    assert LIVE["fields"] == 515
    assert LIVE["mentions"] == 272
    assert LIVE["matched"] == 253
    assert G.refusal(LIVE) is None


def test_live_unresolved_equals_the_waiver_ledger_exactly():
    got = {G.waiver_key(m) for m in LIVE["unresolved"]}
    assert got == set(G.KNOWN)
    assert LIVE["violations"] == [] and LIVE["stale"] == []


def test_the_pla608_part1_hits_are_in_the_ledger_and_st_julien_is_retired():
    names = {(w["crop"], w["name"]) for w in G._K.WAIVERS}
    for hit in [("plum", "Lovell"), ("plum", "Halford"), ("grapefruit", "sour orange"), ("lime", "alemow"),
                ("lime", "Rangpur lime"), ("lemon", "macrophylla"), ("lemon", "rough lemon"),
                ("apricot", "Nemaguard"), ("pear-asian", "quince")]:
        assert hit in names, hit
    # plum's note St. Julien was retired BY CONTENT in PLA-626 (00dda31c): no waiver, and no live mention
    assert not any(w["crop"] == "plum" and "Julien" in w["name"] for w in G._K.WAIVERS)
    assert not any(m["crop"] == "plum" and m["id"] == "st_julien" for m in LIVE["unresolved"])


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
    ("date-plum", "date_plum"), ("Asimina triloba seedling", "pawpaw_seedling"), ("own roots", "own_root"),
    ("ungrafted", "own_root"), ("from cuttings", "own_root"), ("Swingle citrumelo", "swingle"),
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


def test_own_root_resolves_on_an_authored_empty_list_only():
    d = fresh()
    assert by(d)["fig"]["rootstock_options"] == []
    assert viol(d, "fig") == []
    by(d)["peach"]["recommended_rootstock_note"] += " Some peaches grow on their own roots."
    assert any("own roots" in v for v in viol(d, "peach"))


def test_a_row_named_only_seedling_holds_apple_seedling():
    """apple's row is named just "seedling" (ROW_NAME_ALIASES): apple prose naming its seedling stock resolves there,
    and the same sentence on a crop without that row fails."""
    d = fresh()
    by(d)["apple"]["recommended_rootstock_note"] += " An apple seedling rootstock makes the largest tree."
    assert viol(d, "apple") == []
    by(d)["pear-european"]["recommended_rootstock_note"] += " An apple seedling rootstock makes the largest tree."
    assert any("apple seedling" in v for v in viol(d, "pear-european"))


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
    d = fresh()
    c = by(d)["lemon"]
    c["recommended_rootstock_note"] = c["recommended_rootstock_note"].replace(
        "when grown on macrophylla or rough lemon.", "when grown on macrophylla or on rough lemon.")
    v = viol(d, "lemon")
    assert any("'macrophylla'" in x for x in v) and any("'rough lemon'" in x for x in v), v


def test_a_waiver_does_not_cover_the_same_name_on_another_crop():
    d = fresh()
    w = next(w for w in G._K.WAIVERS if w["crop"] == "lemon" and w["name"] == "macrophylla")
    by(d)["orange-navel"]["recommended_rootstock_note"] += " " + w["sentence"]
    assert any("'macrophylla'" in x for x in viol(d, "orange-navel"))


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
    assert "inspected 21 crops carrying rootstock_options (of 21), 515 fields, 272 rootstock names (253 matched a row)" in out
    assert G.LIMIT_LINE in out


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
    assert "A64. rootstock prose" in out and "rootstock names: 10 (7 matched a row); violations: 0" in out


def test_gate_all_runs_the_roster_half_on_a_SHELL(tmp_path):
    """olive is a shell: gate_all's per-crop pass never runs whole_crop_gate on it, so only the roster half sees it."""
    d = fresh()
    assert by(d)["olive"]["verification_status"]["status"] != "verified_gs_arc"
    by(d)["olive"]["recommended_rootstock_note"] = "Olives are sometimes grafted onto St. Julien."
    rc, out = _run([os.path.join(HERE, "gate_all.py"), _write(tmp_path, d)])
    assert rc == 1, out[-3000:]
    assert "VIOLATION: rootstock_prose_gate: olive recommended_rootstock_note" in out, out[-3000:]
