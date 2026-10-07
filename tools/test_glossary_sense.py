"""PLA-673: the glossary sense guard (tools/glossary_sense.py) over the staged match spec.

Pins the live population (224 consumer leaves on 5420479d; 225 on aaf004a2, 232 before PLA-673 B2), proves every exclusion family both on its LIVE leaves and on a
SYNTHETIC leaf injected into a scratch copy, and proves the refusal spec: a hill-word the spec does not classify fails
loud rather than taking a gloss. Run under pytest (def test_ functions), via tools/run_test_tree.py --files.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glossary_sense as gs  # noqa: E402

ROOT = os.path.dirname(HERE)
SPEC = gs.load_spec(os.path.join(HERE, "staging", "pla673_674_prep", "glossary_match.json"))
DATA = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
# Classified WITHOUT refusing, so a defect reddens the test that names it instead of aborting collection (rc 2,
# nothing run): the refusal and the floor are each asserted in their own test below.
LIVE = gs.classify_dataset(DATA, SPEC, floor=0, refuse=False)

HILL_CROPS = SPEC["terms"]["hill"]["crops"]
HILLING_CROPS = SPEC["terms"]["hilling"]["crops"]
RAW_SPEC = json.load(open(os.path.join(HERE, "staging", "pla673_674_prep", "glossary_match.json"), encoding="utf-8"))


def crop(slug):
    return next(c for c in DATA["crops"] if c["slug"] == slug)


def inject(slug, path, text):
    """A scratch copy of the dataset with `text` written at `path` (a list of keys) on crop `slug`."""
    d = copy.deepcopy(DATA)
    c = next(c for c in d["crops"] if c["slug"] == slug)
    o = c
    for k in path[:-1]:
        o = o.setdefault(k, {}) if isinstance(k, str) else o[k]
    o[path[-1]] = text
    return d


def leaf(slug, field, text):
    return gs.classify_leaf(slug, field, text, SPEC)


# ------------------------------------------------------------------ population (inspected-nothing is not clean)
def test_population_is_224_consumer_leaves():
    # 232 on 350eda38 / 3ccc25f1; 225 after PLA-673 B2 (aaf004a2) re-authored 7 leaves without a hill-word
    assert LIVE.inspected == 224
    assert len(LIVE.rows) == 224


def test_population_floor_refuses_an_empty_roster():
    empty = copy.deepcopy(DATA)
    empty["crops"] = []
    with pytest.raises(gs.Refused, match="inspected 0"):
        gs.classify_dataset(empty, SPEC, floor=1)


def test_live_roster_is_fully_classified():
    assert LIVE.unclassified == []


def test_the_default_call_accepts_the_live_roster():
    """The refusing entry point (default floor, refuse=True) passes on canonical."""
    assert gs.classify_dataset(DATA, SPEC).inspected == 224


def test_live_term_counts():
    by = {}
    for r in LIVE.rows:
        by.setdefault(r.term_ids, 0)
        by[r.term_ids] += 1
    # D8 (2026-10-05): the 3 pepper/eggplant "beds or hills" leaves moved hill -> none pending the part B2 re-author.
    # B2 (aaf004a2): eggplant's prevention_seasoned and the three squash soil_prep pairs no longer carry a hill-word
    # part D (5420479d): both peppers' prevention_seasoned lose their hill-word (none -2); watermelon thinning.method gains one (hill +1)
    assert by == {("hill",): 103, ("hilling",): 60, ("none",): 61}


def test_non_consumer_and_structural_paths_are_not_inspected():
    paths = {(r.crop, r.path) for r in LIVE.rows}
    assert not any(p.startswith("verification_status") for _, p in paths)
    assert not any(".sources" in p or "anchoring_urls" in p or "provenance" in p for _, p in paths)
    assert not any(p.endswith((".id", ".arrangement", ".tip_id", ".stage_id", ".action")) for _, p in paths)


@pytest.mark.parametrize("path", [
    ["regions", "warm_arid", "sources", 0], ["planting_layout", 0, "sources", 0], ["soil_prep_sources", 0],
    ["planting_layout", 0, "anchoring_urls", "x", "note"], ["regions", "warm_arid", "plantings_provenance"],
    ["verification_status", "note"],
])
def test_injected_non_consumer_leaf_is_not_inspected(path):
    """Positive control for the consumer filter: no live non-consumer leaf carries a core hill-word, so inject one."""
    d = copy.deepcopy(DATA)
    o = next(c for c in d["crops"] if c["slug"] == "peach")
    for k in path[:-1]:
        nxt = path[path.index(k) + 1]
        if isinstance(o, dict):
            if o.get(k) is None:              # absent OR null (PLA-674 wrote soil_prep_sources = null; fbe11bc went red here)
                o[k] = [] if isinstance(nxt, int) else {}
            o = o[k]
        else:
            o = o[k]
    if isinstance(o, list):
        o.append("Plant in hills (an unscoped crop: inspecting this leaf would refuse).")
    else:
        o[path[-1]] = "Plant in hills (an unscoped crop: inspecting this leaf would refuse)."
    assert gs.classify_dataset(d, SPEC).inspected == 224


# ------------------------------------------------------------------ positive controls
def test_positive_control_planting_hill_on_watermelon():
    assert leaf("watermelon", "soil_prep_beginner", "Plant seeds in small hills 8 feet apart.") == ("hill",)


def test_positive_control_mounded_hills_on_zucchini():
    assert leaf("zucchini-courgette", "x", "Raised beds or mounded hills improve drainage.") == ("hill",)


# eggplant's leaf was re-authored in PLA-673 B2 and both peppers' in part D (PLA-688): none carries a hill-word now.
D8_CROPS = ("bell-pepper", "banana-pepper", "eggplant")


def test_d8_no_pepper_or_eggplant_leaf_carries_a_hill_word_after_part_d():
    """D8 (2026-10-05) tagged the 3 'beds or hills' leaves none pending a re-author; B2 (eggplant) and part D (peppers)
    re-authored them without a hill-word. The exclusion stays in the glossary (a glossary change is its own ruling) and
    now matches no live leaf: proven here, so a re-introduced 'beds or hills' leaf shows up as a population change."""
    assert [(r.crop, r.path) for r in LIVE.rows if r.crop in D8_CROPS] == []
    ex = next(e for e in SPEC["exclusions"] if e["id"] == "pepper-eggplant-beds-or-hills")
    assert ex["why"] == "unsupported claim, re-author pending (part B2)"
    assert leaf("bell-pepper", "x", "Plant on raised, well-drained beds or hills.") == ("none",)


def test_d8_other_hill_text_on_pepper_refuses():
    """Pepper and eggplant are in NO term's scope, so any other hill-word there fails loud."""
    for slug in ("bell-pepper", "banana-pepper", "eggplant"):
        with pytest.raises(gs.Refused, match="UNCLASSIFIED"):
            gs.classify_dataset(inject(slug, ["description_beginner"], "Plant in hills."), SPEC)


def test_d8_beds_or_hills_on_a_hill_crop_is_not_excluded():
    """The D8 exclusion is crop-scoped: the same words on a cucurbit stay `hill`."""
    assert leaf("pumpkin", "x", "Plant on raised beds or hills.") == ("hill",)


# ------------------------------------------------------------------ exclusion 1: potato, incl. its noun "hill"
POTATO_NOUN = [
    "growth_stages.3.user_action_seasoned", "growth_stages.4.user_action_seasoned",
    "tips_by_stage.bulking.1.text_seasoned", "tips_by_stage.harvest.0.text_seasoned", "harvest_ready_seasoned",
]


def test_potato_noun_hill_live_leaves_are_hilling_never_hill():
    rows = {r.path: r for r in LIVE.rows if r.crop == "potato"}
    noun = [p for p, r in rows.items() if any(m.form == "hill" and m.noun for m in r.matches)]
    assert sorted(noun) == sorted(POTATO_NOUN)
    for p in POTATO_NOUN:
        assert rows[p].term_ids == ("hilling",)


def test_potato_all_44_live_leaves_are_hilling():
    rows = [r for r in LIVE.rows if r.crop == "potato"]
    assert len(rows) == 44
    assert {r.term_ids for r in rows} == {("hilling",)}


def test_potato_noun_hill_synthetic():
    d = inject("potato", ["harvest_ready_beginner"], "Dig at the edge of a hill and re-cover.")
    rows = [r for r in gs.classify_dataset(d, SPEC).rows if r.crop == "potato" and r.path == "harvest_ready_beginner"]
    assert [r.term_ids for r in rows] == [("hilling",)]


# ------------------------------------------------------------------ exclusion 2: every hilling crop
@pytest.mark.parametrize("slug", HILLING_CROPS)
def test_every_hilling_crop_live_leaves_are_hilling(slug):
    rows = [r for r in LIVE.rows if r.crop == slug]
    assert rows, f"{slug}: no live hill-word leaf (the parametrization would be vacuous)"
    assert {r.term_ids for r in rows} == {("hilling",)}


@pytest.mark.parametrize("slug", HILLING_CROPS)
def test_every_hilling_crop_synthetic_hilling_text(slug):
    assert leaf(slug, "x", "Hill a little soil around the base, and keep hilling.") == ("hilling",)


@pytest.mark.parametrize("text", [
    "Sow 4 to 5 seeds per hill.", "Corn may also be planted in hills.", "Hills spaced 2.5 feet apart.",
    "Plant seeds to each hill.",
])
def test_planting_group_sense_on_a_hilling_crop_refuses(text):
    """Iowa State's sweet-corn page (cited on all four corns) uses the PLANTING sense; it must not take the hilling gloss."""
    with pytest.raises(gs.Refused, match="UNCLASSIFIED"):
        gs.classify_dataset(inject("sweet-corn", ["description_beginner"], text), SPEC)


@pytest.mark.parametrize("text", ["Hill soil up around the vines.", "Keep hilling.", "Hilled plants."])
def test_hilling_sense_on_a_hill_crop_refuses(text):
    with pytest.raises(gs.Refused, match="UNCLASSIFIED"):
        gs.classify_dataset(inject("pumpkin", ["description_beginner"], text), SPEC)


# ------------------------------------------------------------------ exclusion 3: strawberry "hill system"
def test_strawberry_hill_system_live_leaves_are_none():
    rows = [r for r in LIVE.rows if r.crop == "strawberry"]
    assert len(rows) == 7
    assert {r.term_ids for r in rows} == {("none",)}
    assert {m.exclusion for r in rows for m in r.matches} == {"strawberry-hill-system"}


@pytest.mark.parametrize("text", ["Use a hill system.", "the plasticulture (annual-hill) system", "an annual-hill bed"])
def test_strawberry_hill_system_synthetic(text):
    assert leaf("strawberry", "x", text) == ("none",)


def test_strawberry_other_hill_word_refuses():
    with pytest.raises(gs.Refused, match="UNCLASSIFIED"):
        gs.classify_dataset(inject("strawberry", ["description_beginner"], "Plant in hills."), SPEC)


# ------------------------------------------------------------------ exclusion 4: black/purple raspberry "hill"
UMN_RASPBERRY = ("Set black and purple raspberries 4 feet apart because these types do not produce root suckers, "
                 "they will create what is commonly called a hill.")


def test_raspberry_has_no_live_hill_leaf():
    assert [r for r in LIVE.rows if r.crop == "raspberry"] == []


def test_raspberry_cane_hill_synthetic_is_none_never_hill():
    d = inject("raspberry", ["planting_method_notes"], UMN_RASPBERRY)
    rows = [r for r in gs.classify_dataset(d, SPEC).rows if r.crop == "raspberry"]
    assert [r.term_ids for r in rows] == [("none",)]
    assert rows[0].matches[0].exclusion == "raspberry-cane-hill"


# ------------------------------------------------------------------ exclusion 5: place and variety names
NAMES = [
    ("rosemary", "rosemary-hill-hardy", 31),
    ("rosemary", "rosemary-madalene-hill", 1),
    ("peach", "texas-hill-country", 1), ("nectarine", "texas-hill-country", 1),
    ("cherry-sweet", "texas-hill-country", 2), ("persimmon", "texas-hill-country", 2),
    ("lemongrass", "texas-hill-country", 1),
    ("apple", "beverly-hills-apple", 2),
    ("oregano", "mediterranean-hills", 1), ("lavender", "mediterranean-hills", 1),
    ("orange-navel", "hawaii-hills", 5), ("mandarin-clementine", "hawaii-hills", 5), ("snow-peas", "hawaii-hills", 1),
]


@pytest.mark.parametrize("slug,exclusion,n", NAMES)
def test_name_exclusions_live(slug, exclusion, n):
    rows = [r for r in LIVE.rows if r.crop == slug and any(m.exclusion == exclusion for m in r.matches)]
    assert len(rows) == n
    assert {r.term_ids for r in rows} == {("none",)}


@pytest.mark.parametrize("slug,text", [
    ("watermelon", "Grown commercially in the Texas Hill Country."),
    ("pumpkin", "the texas hill country"),
    ("pumpkin", "a pumpkin named for Beverly Hills"),
    ("cantaloupe", "native to Mediterranean hills"),
    ("watermelon", "It does better up in the cooler hills."),
    ("cucumber", "a strain like Hill Hardy"),
])
def test_name_exclusions_hold_on_a_hill_crop(slug, text):
    """The exclusion is applied BEFORE the term, so a place name on a hill crop is `none`, not `hill`."""
    assert leaf(slug, "x", text) == ("none",)


def test_unlisted_place_name_on_an_unscoped_crop_refuses():
    with pytest.raises(gs.Refused, match="UNCLASSIFIED"):
        gs.classify_dataset(inject("peach", ["description_beginner"], "Grown in the Ozark hills."), SPEC)


# ------------------------------------------------------------------ the spec itself
def test_term_crop_scopes_are_disjoint_and_exist():
    slugs = {c["slug"] for c in DATA["crops"]}
    assert not set(HILL_CROPS) & set(HILLING_CROPS)
    assert set(HILL_CROPS) <= slugs and set(HILLING_CROPS) <= slugs
    assert len(HILL_CROPS) == 12 and len(HILLING_CROPS) == 11


def test_every_exclusion_fires_on_live_or_is_a_declared_future_guard():
    fired = {m.exclusion for r in LIVE.rows for m in r.matches if m.exclusion}
    declared = {e["id"] for e in SPEC["exclusions"]}
    # pepper-eggplant-beds-or-hills went DORMANT at part D (5420479d): B2 and part D re-authored all three leaves it
    # tagged. It stays in the glossary (removing it is a glossary ruling) and is declared here by identity.
    assert declared - fired == {"raspberry-cane-hill", "pepper-eggplant-beds-or-hills"}


# ------------------------------------------------------------------ the ruled glossary shape (2026-10-05)
def test_spec_is_the_ruled_glossary_match_shape():
    """Each term carries exactly one matcher in `match`, with exactly the ruled matcher keys."""
    terms = {k: v for k, v in RAW_SPEC.items() if not k.startswith("_")}
    assert set(terms) == {"hill", "hilling"}
    for tid, entry in terms.items():
        assert set(entry) == {"match"}
        assert isinstance(entry["match"], list) and len(entry["match"]) == 1
        assert set(entry["match"][0]) == {"sense", "forms", "crops", "refuse_on", "exclusions"}


def test_exclusions_are_identical_across_terms():
    assert RAW_SPEC["hill"]["match"][0]["exclusions"] == RAW_SPEC["hilling"]["match"][0]["exclusions"]


def test_diverging_exclusions_refuse():
    bad = copy.deepcopy(RAW_SPEC)
    bad["hilling"]["match"][0]["exclusions"] = bad["hilling"]["match"][0]["exclusions"][:-1]
    with pytest.raises(gs.Refused, match="exclusions differ"):
        gs.build_spec(bad)


def test_glossary_entries_with_the_seven_keys_load():
    """The guard reads the dataset's glossary entries directly (the seven ruled keys, match among them)."""
    entries = {tid: {"term": tid, "definition_beginner": "x", "definition_seasoned": "x", "sources": None,
                     "anchoring_urls": None, "field_additions": [], "match": RAW_SPEC[tid]["match"]}
               for tid in ("hill", "hilling")}
    spec = gs.build_spec(entries)
    assert gs.classify_dataset(DATA, spec).inspected == 224


@pytest.mark.parametrize("mutate", [
    lambda m: m.update(id="hill"),                     # an inner id: the app projection throws on it
    lambda m: m.pop("refuse_on"),                      # a missing matcher key
], ids=["extra-inner-id", "missing-refuse_on"])
def test_malformed_matcher_refuses(mutate):
    bad = copy.deepcopy(RAW_SPEC)
    mutate(bad["hill"]["match"][0])
    with pytest.raises(gs.Refused, match="must be one matcher"):
        gs.build_spec(bad)


def test_two_matchers_refuse():
    bad = copy.deepcopy(RAW_SPEC)
    bad["hill"]["match"].append(copy.deepcopy(bad["hill"]["match"][0]))
    with pytest.raises(gs.Refused, match="must be one matcher"):
        gs.build_spec(bad)


# ------------------------------------------------------------------ the shared match fixture (PLA-673 part D)
FIXTURE = os.path.join(HERE, "staging", "pla673_674_prep", "glossary-match.fixture.json")
FIXTURE_SHA = "e075f0f8e915aff14b106b0cd29b5132ab7cbf5060db8d136dc9ab07dbb61f84"   # 35 cases (part D); 990eac25 before
# refuse_on pattern -> the ONE fixture case that fails when that pattern alone is dropped (Trevor, part D: each pattern
# exercised alone; plant-astro's mutation run found dropping any single one failed nothing).
SOLE_CASE = {
    ("hill", r"\bhill(ed|ing)?\s+(a\s+little\s+)?(soil|up|mulch)\b"): "refuse-hilling-verb-on-pumpkin",
    ("hilling", r"\bper\s+hill\b"): "refuse-planting-sense-on-corn",
    ("hilling", r"\bin\s+hills\b"): "refuse-in-hills-on-potato",
    ("hilling", r"\bhills?\s+(spaced|apart)\b"): "refuse-hills-spaced-on-carrot",
    ("hilling", r"\bseeds?\s+(in|to)\s+(a|each)\s+hill\b"): "refuse-seeds-in-each-hill-on-sweet-corn",
}
# Waived by identity AND character: UNREACHABLE as a sole cause. The hill term's forms are hill/hills, so any sentence
# these match also holds a hilled/hilling occurrence that refuses on its FORM; dropping the pattern changes no verdict.
# Reported for a ruling (PLA-673 part D). If either ever becomes the sole cause, this waiver fails as STALE.
UNREACHABLE = {("hill", r"\bhilled\b"), ("hill", r"\bhilling\b")}


def _fixture():
    import hashlib
    b = open(FIXTURE, "rb").read()
    return hashlib.sha256(b).hexdigest(), json.loads(b)


def _failing(glossary, cases):
    spec, bad = gs.build_spec(glossary), []
    for c in cases:
        ms = gs.classify_leaf_matches(c["crop"], c["text"], spec)
        ok = any(m.term is None for m in ms) if c.get("refuse") else [m.term for m in ms] == c["expect"]
        if not ok:
            bad.append(c["id"])
    return bad


def test_fixture_is_the_pinned_bytes():
    assert _fixture()[0] == FIXTURE_SHA


def test_every_fixture_case_holds_on_the_canonical_glossary():
    cases = _fixture()[1]["cases"]
    assert len(cases) == 35
    assert _failing(DATA["glossary"], cases) == []


def test_every_refuse_on_pattern_is_exercised_alone_or_waived():
    import copy as _copy
    cases = _fixture()[1]["cases"]
    seen = set()
    for tid in ("hill", "hilling"):
        for i, pat in enumerate(DATA["glossary"][tid]["match"][0]["refuse_on"]):
            seen.add((tid, pat))
            g = _copy.deepcopy(DATA["glossary"])
            del g[tid]["match"][0]["refuse_on"][i]
            got = _failing(g, cases)
            if (tid, pat) in UNREACHABLE:
                assert got == [], f"STALE waiver: {tid} {pat} is now the sole cause of {got}"
            else:
                assert got == [SOLE_CASE[(tid, pat)]], (tid, pat, got)
    assert seen == set(SOLE_CASE) | UNREACHABLE      # every pattern is named, none invented
