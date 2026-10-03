#!/usr/bin/env python3
"""Guard suite for promote_pla10_promote3 (PLA-10 promote 3: heights on 46 crops + the 16-crop mature_dimensions
backfill), built in the promote-3 session-1 tools commit (2026-10-02) BEFORE any stage exists.
Run: python3 -m pytest tools/test_promote_pla10_promote3.py -q

T4 first: cited_promote_common.quote_states_ft, the height/spread quote check, run against REAL quotes from the
plan-58 measurements (C_tipover_heights_pla465_backfill.md, D_heights_remaining.tsv) as its positive control,
so the check is measured against the page types the stage will cite before anything is authored to it.
Then the promote: the fixed list (46 + 16 = 62), the T3 record allowance, the sibling pair, the backfill
(re-hash K3, apple's re-point K1, blueberry's conditional re-anchor K2), restatement adjudication (H3), the
evidence, and the gates on the post-state. The base is replay-pinned through promote_fixture (31b766e8 ->
7177af3), never the live file. Drivers build a SYNTHETIC full-list stage + evidence cache in a temp dir
(nothing here is a citation) and inject one defect each, asserting the REFUSAL TEXT.
SHIPS MUTATION-TESTED via mutate_pla10_promote3.py.
"""
import copy, csv, hashlib, inspect, json, os, shutil, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cited_promote_common as C  # noqa: E402
import promote_fixture  # noqa: E402
import promote_pla10_promote3 as P  # noqa: E402

BASE = json.loads(promote_fixture.pre_state(P.BASE_SHA))
IDX = {c["slug"]: c for c in BASE["crops"]}

H, S = "mature_height_ft", "mature_spread_ft"
BROC = "full-grown plants reach about 47 inches tall and 20 inches wide, relying on bees for cross-pollination."

# (field, value as it will be stored, verbatim quote in norm_text form): every row is a real quote from a
# cached cited page (plan 58 measurements C and D), at the value the measurement proposes.
REAL = [
    (H, [3, 4], "peppers are produced on bushy plants that can reach 3-4 ft. in height."),
    (H, [3.9167, 3.9167], BROC),
    (S, [1.6667, 1.6667], BROC),
    (H, [2, 4], "the plants can grow 2-4 feet tall and wide on a thick stalk."),
    (S, [2, 4], "the plants can grow 2-4 feet tall and wide on a thick stalk."),
    (H, [2, 6], "it is a stiffly erect plant that grows 2-6 feet tall and prefers moist loams"),
    (H, [3, 6], "garden cosmos can reach 3-6 feet and has finer, string-like foliage."),
    (H, [1.5, 4], "dill plants grow 18 inches to 4 feet tall and resemble fennel."),
    (H, [2, 4], "the plant may grow 2 to 4 feet tall and is multi-branched."),
    (H, [3, 4], "these easy to grow indeterminate plants grow to 3 to 4 feet in height and width"),
    (S, [3, 4], "these easy to grow indeterminate plants grow to 3 to 4 feet in height and width"),
    (S, [3, 4], "tomatillos grow 3-4 feet tall and wide"),
    (H, [2.5, 3], "kale is a large plant, often growing to 2.5-3 feet tall."),
    (H, [0.6667, 1], "it grows to a height of 8-12 inches."),
    (H, [0.6667, 2], "size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety"),
    (S, [0.6667, 1], "size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety"),
    (H, [2, 2], "bush beans are upright plants that do not need support, growing about two feet tall."),
    (H, [3, 3], "plants are approximately 3 feet tall and do not require support."),
    (H, [1, 2], "height: 1 ft. 0 in. - 2 ft. 0 in. width: 1 ft. 0 in. - 1 ft. 6 in."),
    (S, [1, 1.5], "height: 1 ft. 0 in. - 2 ft. 0 in. width: 1 ft. 0 in. - 1 ft. 6 in."),
    (H, [1, 1], "the vines can extend up to 15 feet in length, depending on the variety, and about 12 inches in "
                "height when situated on the ground."),
    (H, [1, 3], "height: 1 to 3 feet spread: 0.5 to 1 feet"),
    (S, [0.5, 1], "height: 1 to 3 feet spread: 0.5 to 1 feet"),
    (H, [1, 1.5], 'the foliage grows 12-18" high, and the flower stems reach 2-3 feet.'),
    (S, [1, 1.4167], "height: 1 ft. 0 in. - 1 ft. 6 in. width: 1 ft. 0 in. - 1 ft. 5 in."),
    (H, [1, 2], "growing quickly 1 to 2 feet high and wide"),
    (S, [1, 2], "growing quickly 1 to 2 feet high and wide"),
    (H, [3, 6], "plant heights vary by cultivar and pruning practices. most fall within the 3-6 foot range"),
    (H, [1.5, 2], "celery grows to a height of 18 to 24 inches"),
    (S, [2, 4], "height: 3 to 6 feet spread: 2 to 4 feet"),
    (H, [5, 6], "asparagus foliage can reach 5 to 6 feet in height"),
    (H, [1, 4], "as an annual, marigolds are upright and typically 1 to 4 feet tall."),
    (H, [2, 10], "rough, coarse, hairy stems that grow 2 to10 feet tall"),
    (H, [1.5833, 3.1667], "height: 1 ft. 7 in. - 3 ft. 2 in. width: 1 ft. 0 in. - 1 ft. 4 in."),
    (S, [1, 1.3333], "height: 1 ft. 7 in. - 3 ft. 2 in. width: 1 ft. 0 in. - 1 ft. 4 in."),
    (H, [2, 3], "borage is an exuberant annual that grows two to three feet tall"),
    (S, [1, 1.1667], "size: 1 to 2 feet tall, 12 to 14 inches wide"),
    (H, [0.25, 0.8333], "height: 0 ft. 3 in. - 0 ft. 10 in. width: 0 ft. 6 in. - 1 ft. 0 in."),
    (H, [2, 3], "this plant grows 24-36 inches in height."),
    (H, [0.5, 0.75], "it grows 6 to 9 inches in height and 9 to 12 inches in width."),
    (S, [0.75, 1], "it grows 6 to 9 inches in height and 9 to 12 inches in width."),
    (H, [2, 3], "plants grow two to three feet tall, and can have a width of two inches."),
    (H, [15, 25], "the tree will grow quickly to 15-25 feet tall and wide"),
    (H, [10, 14], "m 26-semi-dwarf habit, 10'-14' tall, common in home orchards"),
    (H, [10, 20], "trees may reach 10-20 ft (3.1-6.1 m) in height (morton 1987)."),
    (S, [0.5, 1.3333], "about 6 to 12 inches high and 6 to 16 inches wide"),
    (S, [15, 30], "height & spread: 15 - 30 ft tall and wide"),
    (S, [8, 10], "10 to 12 feet tall and 8 to 10 feet wide"),
    (H, [20, 30], "height: 20 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 25 ft. 0 in."),
    (S, [15, 25], "height: 20 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 25 ft. 0 in."),
    (S, [2, 3], "up to 2 feet tall and 2 to 3 feet wide"),
    (H, [3, 3], "a height of 3 feet with a 2 foot spread"),
    (S, [2, 2], "a height of 3 feet with a 2 foot spread"),
]


class QuoteStatesFt(unittest.TestCase):
    """T4 (plan 58 §8, ruling H4): the height/spread quote check. A stored endpoint is STATED by a figure in the
    quote's clause for that dimension that rounds to it at 4 places (|e - figure| <= TOL_FT); an inches
    figure is divided by 12 first. A spread must come from a width clause, a height from a height clause."""

    def test_the_tolerance_is_the_stated_literal(self):
        self.assertEqual(C.TOL_FT, 0.00005)

    def test_H4_broccoli_rounded_quotient_passes(self):
        self.assertTrue(C.quote_states_ft(H, [3.9167, 3.9167], BROC))
        self.assertTrue(C.quote_states_ft(H, [47 / 12, 47 / 12], BROC))

    def test_H4_a_LOOSE_rounding_FAILS(self):
        """3.9 against "47 inches" is the injection the plan names: 47/12 = 3.91667, off by 0.0167."""
        for v in (3.9, 3.92, 3.917, 3.916):
            self.assertFalse(C.quote_states_ft(H, [v, v], BROC), v)

    def test_a_spread_quoted_from_a_HEIGHT_clause_FAILS(self):
        self.assertFalse(C.quote_states_ft(S, [3.9167, 3.9167], BROC))
        self.assertFalse(C.quote_states_ft(S, [0.6667, 1], "it grows to a height of 8-12 inches."))
        self.assertFalse(C.quote_states_ft(S, [2, 4], "the plant may grow 2 to 4 feet tall and is multi-branched."))

    def test_a_height_quoted_from_a_WIDTH_clause_FAILS(self):
        self.assertFalse(C.quote_states_ft(H, [1.6667, 1.6667], BROC))
        self.assertFalse(C.quote_states_ft(H, [0.75, 1], "it grows 6 to 9 inches in height and 9 to 12 inches in width."
                                                        .replace("6 to 9", "5 to 8")))

    def test_vine_run_and_spacing_state_no_dimension(self):
        """spec §4.5: vine run is not spread; a spacing is neither."""
        vine = "the vines can extend up to 15 feet in length, depending on the variety"
        self.assertFalse(C.quote_states_ft(S, [15, 15], vine))
        self.assertFalse(C.quote_states_ft(H, [15, 15], vine))
        self.assertFalse(C.quote_states_ft(H, [1.5, 1.5], "plants grow best set 18 inches apart in the row"))

    def test_a_compound_figure_reads_to_4_places(self):
        q = "height: 1 ft. 7 in. - 3 ft. 2 in. width: 1 ft. 0 in. - 1 ft. 4 in."
        self.assertTrue(C.quote_states_ft(H, [1.5833, 1.5833], q))
        self.assertFalse(C.quote_states_ft(H, [1.58, 1.58], q))

    def test_ft_endpoints_reports_WHICH_ends_are_stated(self):
        """The promote requires both ends stated across a field's rows; per row it needs at least one."""
        self.assertEqual(C.ft_endpoints_stated(H, [1, 2], "up to 2 feet tall and 2 to 3 feet wide"), {2})
        self.assertEqual(C.ft_endpoints_stated(S, [0.5, 0.75], "it grows 6 to 9 inches in height and 9 to 12 "
                                                               "inches in width."), {0.75})
        self.assertEqual(C.ft_endpoints_stated(H, [1.5, 4], "dill plants grow 18 inches to 4 feet tall"), {1.5, 4})

    def test_REAL_quotes_from_the_measurements_all_pass(self):
        """The positive control: every real quote at its measured value. A check that cannot pass one of
        these is the always-red half of the vacuity rule (the PDF lesson, 2026-10-01)."""
        for field, value, quote in REAL:
            self.assertTrue(C.quote_states_ft(field, value, C.norm_text(quote)), (field, value, quote))
            self.assertEqual(C.ft_endpoints_stated(field, value, C.norm_text(quote)) != set(), True)

    def test_REAL_quotes_fail_for_the_OTHER_dimension_where_the_figures_differ(self):
        """Both ways (a guard can refuse GOOD input): the same real quotes, field swapped, fail wherever the
        two clauses state different figures."""
        n = 0
        for field, value, quote in REAL:
            other = S if field == H else H
            other_vals = {v for g in C._ft_groups(C.norm_text(quote)) if (other == H and "H" in g[0]) or
                          (other == S and "W" in g[0]) for v in g[1]}
            if not any(abs(e - v) <= C.TOL_FT for e in value for v in other_vals):
                self.assertFalse(C.quote_states_ft(other, value, C.norm_text(quote)), (other, value, quote))
                n += 1
        self.assertGreaterEqual(n, 25, "the swapped-field control inspected too few rows")


# ================================================================== the promote
UMD = "https://extension.umd.edu/resource/growing-peppers-home-garden"
UMD_SHA = "4fe5a4ddae5c61744f5919ac66105662c70483d16207334fe7d5221db9612c6f"
UMD_QUOTE = "peppers are produced on bushy plants that can reach 3-4 ft. in height."
FA_NOTE = "PLA-10 promote 3 synthetic fixture record (test_promote_pla10_promote3)."
# New crops the synthetic stage authors with a SPREAD too (the rest author height only).
WITH_SPREAD = ("broccoli", "brussels-sprouts", "tomatillo", "potato", "basil")


def fmtn(x):
    return f"{x:g}"


class Synthetic:
    """A full fixed-list stage (all 62 crops) + an evidence cache in a temp dir. Quotes are written into synthetic
    page bytes so the evidence machinery runs end to end; bell-pepper runs against the REAL hashed UMD bytes."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="pla10p3_")
        self.stage = os.path.join(self.root, "stage")
        os.makedirs(os.path.join(self.stage, "crops"))
        self.ev_dir = os.path.join(self.root, "evidence")
        os.makedirs(self.ev_dir)
        self.crops, self.ev, self.manifest = {}, [], []
        shutil.copy2(os.path.join(P.EVIDENCE, UMD_SHA + ".html"), self.ev_dir)
        self.manifest.append({"sha256": UMD_SHA, "url": UMD})
        for slug in P.NEW_CROPS:
            if slug == "bell-pepper":
                self.new(slug, [3, 4], None, sid="umd_ext", url=UMD, real=True)
            else:
                self.new(slug, [1, 2], [0.5, 1] if slug in WITH_SPREAD else None)
        for slug in P.BACKFILL_CROPS:
            self.backfill(slug)

    def anchor(self, url):
        return {"url": url, "verified": "2026-10-02"}

    def new(self, slug, h, sp, sid="ncsu_ext", url=None, real=False):
        url = url or f"https://plants.ces.ncsu.edu/plants/{slug}-synthetic/"
        st = {"slug": slug, "decision": "synthetic", P.H: h, P.S: sp, "sources": [sid],
              "anchoring_urls": {sid: self.anchor(url)},
              "field_addition": {"field": "plant_dimensions", "date": "2026-10-02", "sources": [sid],
                                 "note": FA_NOTE},
              "restatements": [{"path": x, "verdict": "agrees", "note": "synthetic"}
                               for x in P.height_strings(IDX[slug], sp is not None)]}
        self.crops[slug] = st
        if real:
            self.add_ev(slug, P.H, h, sid, url, UMD_QUOTE, sha=UMD_SHA)
            return
        self.add_ev(slug, P.H, h, sid, url, f"synthetic {slug}: plants grow {fmtn(h[0])} to {fmtn(h[1])} feet tall.")
        if sp is not None:
            self.add_ev(slug, P.S, sp, sid, url,
                        f"synthetic {slug}: plants spread {fmtn(sp[0])} to {fmtn(sp[1])} feet wide.")

    def backfill(self, slug):
        c = IDX[slug]
        rec = P._records(c)[0]
        sid = rec["sources"][0]
        sid, url = P.REPOINT.get(slug, (sid, P.record_url(c)))
        st = {"slug": slug, "decision": "synthetic backfill", P.H: c[P.H], P.S: c[P.S], "sources": [sid],
              "anchoring_urls": {sid: self.anchor(url)}}
        self.crops[slug] = st
        self.add_ev(slug, P.H, c[P.H], sid, url,
                    f"synthetic {slug}: trees grow {fmtn(c[P.H][0])} to {fmtn(c[P.H][1])} feet tall.")
        if c[P.S] is not None:
            self.add_ev(slug, P.S, c[P.S], sid, url,
                        f"synthetic {slug}: trees spread {fmtn(c[P.S][0])} to {fmtn(c[P.S][1])} feet wide.")

    def add_ev(self, crop, field, value, sid, url, quote, sha=None, page=None):
        if sha is None:
            body = (page if page is not None else f"<html><p>{quote}</p></html>").encode("utf-8")
            sha = hashlib.sha256(body).hexdigest()
            with open(os.path.join(self.ev_dir, sha + ".html"), "wb") as f:
                f.write(body)
            self.manifest.append({"sha256": sha, "url": url})
        self.ev.append({"crop": crop, "entry_id": "mature_dimensions", "field": field, "value": C.compact(value),
                        "source_id": sid, "url": url, "sha256": sha, "quote": quote})

    def drop_ev(self, crop, field=None):
        self.ev = [r for r in self.ev if not (r["crop"] == crop and (field is None or r["field"] == field))]

    def write(self):
        shutil.rmtree(os.path.join(self.stage, "crops"))
        os.makedirs(os.path.join(self.stage, "crops"))
        for slug, s in self.crops.items():
            with open(os.path.join(self.stage, "crops", slug + ".json"), "w", encoding="utf-8") as f:
                json.dump(s, f, ensure_ascii=False)
        with open(os.path.join(self.stage, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=C.EVIDENCE_COLS, delimiter="\t")
            w.writeheader()
            w.writerows(self.ev)
        with open(os.path.join(self.ev_dir, "MANIFEST.tsv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=("sha256", "url"), delimiter="\t")
            w.writeheader()
            w.writerows(self.manifest)

    def load(self):
        self.write()
        return P.load_stage(self.stage)

    def run(self):
        stage, ev = self.load()
        return P.run(copy.deepcopy(BASE), stage, ev, self.ev_dir)

    def post(self):
        stage, ev = self.load()
        P.check_pre(copy.deepcopy(BASE), stage)
        return stage, ev, P.apply_to(copy.deepcopy(BASE), stage)

    def check_post(self, stage, ev, post):
        return P.check_post(copy.deepcopy(BASE), post, stage, ev, self.ev_dir)

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


_POST = {}


def clean_post():
    """The clean run, once per process (62 crops x the armed gates); callers deep-copy what they mutate."""
    if not _POST:
        s = Synthetic()
        try:
            _POST["post"], _POST["n"] = s.run()
        finally:
            s.close()
    return _POST["post"], _POST["n"]


def crop(data, slug):
    return next(c for c in data["crops"] if c["slug"] == slug)


class Base(unittest.TestCase):
    def setUp(self):
        self.s = Synthetic()

    def tearDown(self):
        self.s.close()

    def refuses(self, fn, text):
        with self.assertRaises(P.Refused) as cm:
            fn()
        self.assertIn(text, str(cm.exception))
        return str(cm.exception)

    def refuses_run(self, text):
        return self.refuses(self.s.run, text)

    def refuses_post(self, mutate, text):
        stage, ev, post = self.s.post()
        mutate(post)
        return self.refuses(lambda: self.s.check_post(stage, ev, post), text)


# ------------------------------------------------------------------ the clean path and the controls
class Clean(unittest.TestCase):
    def test_the_clean_stage_passes_and_changes_exactly_the_named_leaves(self):
        post, n = clean_post()
        self.assertEqual({k: n[k] for k in ("crops", "authored", "null", "backfilled", "records", "k2")},
                         {"crops": 62, "authored": 46, "null": 0, "backfilled": 16, "records": 46, "k2": 0})
        changed = set()
        for a, b in zip(BASE["crops"], post["crops"]):
            changed |= {(a["slug"],) + p[:1] if p[0] != "verification_status" else (a["slug"],) + p[:2]
                        for p in C.leaf_diff(a, b)}
        want = set()
        for slug in P.NEW_CROPS:
            want |= {(slug, P.H), (slug, P.SIB_S), (slug, P.SIB_A), (slug, "verification_status", "field_additions")}
            if slug in WITH_SPREAD:
                want.add((slug, P.S))
        for slug in P.BACKFILL_CROPS:
            want |= {(slug, P.SIB_S), (slug, P.SIB_A)}
        self.assertEqual(changed, want)
        for slug in P.NEW_CROPS:
            a, b = crop(BASE, slug), crop(post, slug)
            self.assertEqual(b["verification_status"]["field_additions"],
                             (a["verification_status"].get("field_additions") or [])
                             + [{"field": "plant_dimensions", "date": "2026-10-02",
                                 "sources": b[P.SIB_S], "note": FA_NOTE}])
            keys = list(b)
            self.assertEqual(keys.index(P.SIB_S), keys.index(P.S) + 1, slug)
            self.assertEqual(keys.index(P.SIB_A), keys.index(P.S) + 2, slug)
        self.assertEqual(crop(post, "apple")[P.SIB_A]["wsu_ext"]["url"], P.REPOINT["apple"][1])

    def test_the_REAL_umd_bytes_carry_bell_peppers_height(self):
        post, _ = clean_post()
        self.assertEqual(crop(post, "bell-pepper")[P.H], [3, 4])
        self.assertEqual(crop(post, "bell-pepper")[P.SIB_A]["umd_ext"]["url"], UMD)

    def test_the_base_is_pinned(self):
        self.assertEqual(P.BASE_SHA, "31b766e86a01377c88898568171bcb372d3da1d3146fa50f6cbd6288dd8b6369")
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_the_fixed_list_is_plan_58s_literal(self):
        self.assertEqual(len(P.TIPOVER), 11)
        self.assertEqual(len(P.CLOSED), 35)
        self.assertEqual(len(P.BACKFILL_CROPS), 16)
        self.assertEqual(len(set(P.NEW_CROPS) | set(P.BACKFILL_CROPS)), 62)
        self.assertEqual(set(P.TIPOVER), {"bell-pepper", "jalapeno", "banana-pepper", "cayenne-pepper", "habanero",
                                          "broccoli", "brussels-sprouts", "broad-beans-fava", "dill", "eggplant",
                                          "cosmos"})
        self.assertEqual(set(P.BACKFILL_CROPS), {"peach", "nectarine", "apple", "lemon", "blueberry", "thyme",
                                                 "rosemary", "oregano", "sage", "fig", "pomegranate", "elderberry",
                                                 "persimmon", "mulberry", "pawpaw", "lavender"})
        for slug in P.NEW_CROPS:
            c = IDX[slug]
            self.assertTrue(P.certified(c) and c[P.H] is None and c[P.S] is None and not P._records(c), slug)
        for slug in P.BACKFILL_CROPS:
            self.assertTrue(IDX[slug][P.H] is not None and len(P._records(IDX[slug])) == 1, slug)
        authored = {c["slug"] for c in BASE["crops"] if c.get(P.H) is not None or c.get(P.S) is not None}
        self.assertEqual(authored, set(P.BACKFILL_CROPS), "the backfill is EVERY authored crop on the base")

    def test_the_rulings_are_the_literals(self):
        self.assertEqual(P.REPOINT, {"apple": ("wsu_ext", "https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/"
                                                          "2109/2019/12/fruit_handbook_western_wa.pdf")})
        self.assertEqual(P.K2, {"blueberry": {"height": [4, 8], "source": "psu_ext",
                                              "url": "https://extension.psu.edu/highbush-blueberry-production"}})

    def test_promotes_do_not_import_promotes(self):
        src = open(P.__file__, encoding="utf-8").read()
        self.assertNotRegex(src, r"(?m)^\s*(?:import|from)\s+promote_")


class Refusals(Base):
    def test_an_empty_stage_REFUSES(self):
        self.s.crops = {}
        self.refuses_run("the stage names no crop")

    # ---- X: the fixed list
    def test_FIXED_LIST_a_missing_crop_REFUSES(self):
        del self.s.crops["dill"]
        self.refuses_run("missing ['dill']")

    def test_FIXED_LIST_an_extra_crop_REFUSES(self):
        self.s.crops["parsley"] = {"slug": "parsley", "decision": "x", P.H: None, P.S: None}
        self.refuses_run("extra ['parsley']")

    def test_an_unknown_stage_key_REFUSES(self):
        self.s.crops["dill"]["zz"] = 1
        self.refuses(self.s.load, "unknown keys ['zz']")

    def test_a_stage_needs_a_decision_row(self):
        self.s.crops["dill"]["decision"] = " "
        self.refuses(self.s.load, "the decision row is empty")

    def test_a_base_already_carrying_a_sibling_REFUSES(self):
        stage, ev = self.s.load()
        pre = copy.deepcopy(BASE)
        crop(pre, "carrot")[P.SIB_S] = ["umn_ext"]
        self.refuses(lambda: P.check_pre(pre, stage), "base already carries mature_dimensions_sources on carrot")

    # ---- V: values
    def test_a_value_key_missing_REFUSES(self):
        del self.s.crops["dill"][P.S]
        self.refuses_run("must state mature_spread_ft")

    def test_a_value_out_of_order_REFUSES(self):
        self.s.crops["dill"][P.H] = [4, 1.5]
        self.refuses_run("0 < lo <= hi")

    def test_H4_more_than_4_decimals_REFUSES(self):
        self.s.crops["broccoli"][P.H] = [47 / 12, 47 / 12]
        self.refuses_run("more than 4 decimals")

    def test_a_backfill_value_moved_REFUSES(self):
        self.s.crops["peach"][P.H] = [15, 30]
        self.refuses_run("a BACKFILL crop's values stay the base's")

    def test_a_backfill_spread_moved_REFUSES(self):
        self.s.crops["fig"][P.S] = [10, 30]
        self.refuses_run("a BACKFILL crop's values stay the base's")

    def test_K2_moves_only_to_the_ruled_value(self):
        self.s.crops["blueberry"][P.H] = [4, 7]
        self.refuses_run("K2's re-anchor moves the height to exactly [4, 8]")

    def test_K2_spread_stays_or_goes_null(self):
        b = self.s.crops["blueberry"]
        b[P.H] = [4, 8]
        b[P.S] = [4, 8]
        self.refuses_run("under K2 the spread stays the base's")

    def test_K2_taken_cites_the_ruled_page(self):
        b = self.s.crops["blueberry"]
        b[P.H] = [4, 8]
        self.refuses_run("the backfill anchor for 'psu_ext' must be 'https://extension.psu.edu/highbush-blueberry")

    def test_K2_taken_end_to_end_passes(self):
        b = self.s.crops["blueberry"]
        url = P.K2["blueberry"]["url"]
        b[P.H], b[P.S] = [4, 8], None
        b["anchoring_urls"] = {"psu_ext": self.s.anchor(url)}
        b["restatements"] = [{"path": x, "verdict": "agrees", "note": "synthetic"}
                             for x in P.height_strings(IDX["blueberry"], False)]
        self.s.drop_ev("blueberry")
        self.s.add_ev("blueberry", P.H, [4, 8], "psu_ext", url, "highbush blueberries are usually 4 to 8 feet tall "
                                                                "at maturity")
        post, n = self.s.run()
        self.assertEqual((crop(post, "blueberry")[P.H], crop(post, "blueberry")[P.S], n["k2"]), ([4, 8], None, 1))

    def test_a_NEW_crop_carrying_a_value_on_the_base_REFUSES(self):
        stage, ev = self.s.load()
        pre = copy.deepcopy(BASE)
        crop(pre, "dill")[P.H] = [1, 2]
        self.refuses(lambda: P.check_pre(pre, stage), "a NEW crop must be null on the base")

    # ---- C: the sibling
    def test_a_value_with_no_sources_REFUSES(self):
        self.s.crops["dill"]["sources"] = []
        self.refuses_run("a value needs sources")

    def test_a_source_off_the_catalog_REFUSES(self):
        d = self.s.crops["dill"]
        d["sources"] = ["zz_nowhere"]
        d["anchoring_urls"] = {"zz_nowhere": d["anchoring_urls"]["ncsu_ext"]}
        d["field_addition"]["sources"] = ["zz_nowhere"]
        self.refuses_run("'zz_nowhere' is not in source_catalog")

    def test_a_source_twice_REFUSES(self):
        self.s.crops["dill"]["sources"] = ["ncsu_ext", "ncsu_ext"]
        self.refuses_run("lists a source twice")

    def test_a_SOURCE_WITH_NO_ANCHOR_REFUSES(self):
        d = self.s.crops["dill"]
        d["sources"] = ["ncsu_ext", "uwi_hort"]
        self.refuses_run("anchoring_urls keys must be exactly the sources")

    def test_an_anchor_with_extra_keys_REFUSES(self):
        self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["quote"] = "x"
        self.refuses_run("needs exactly url and verified")

    def test_a_bare_host_anchor_REFUSES(self):
        self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["url"] = "https://plants.ces.ncsu.edu/"
        self.refuses_run("is a bare host")

    def test_an_undated_anchor_REFUSES(self):
        self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["verified"] = "recently"
        self.refuses_run("is not a date")

    def test_K3_the_backfill_anchor_is_the_records_url(self):
        self.s.crops["peach"]["anchoring_urls"]["ncsu_ext"]["url"] = "https://plants.ces.ncsu.edu/plants/elsewhere/"
        self.refuses_run("the backfill anchor for 'ncsu_ext' must be 'https://plants.ces.ncsu.edu/plants/prunus-persica/'")

    def test_K3_the_backfill_cites_the_records_source(self):
        p = self.s.crops["peach"]
        p["sources"] = ["clemson_hgic"]
        p["anchoring_urls"] = {"clemson_hgic": self.s.anchor("https://hgic.clemson.edu/factsheet/peach/")}
        self.refuses_run("the backfill must cite 'ncsu_ext'")

    def test_K1_apple_on_its_records_s3_url_REFUSES(self):
        self.s.crops["apple"]["anchoring_urls"]["wsu_ext"]["url"] = P.record_url(IDX["apple"])
        self.refuses_run("the backfill anchor for 'wsu_ext' must be 'https://wpcdn.web.wsu.edu")

    def test_a_sibling_on_a_null_crop_REFUSES(self):
        d = self.s.crops["dill"]
        d[P.H] = None
        d.pop("field_addition")
        d.pop("restatements")
        self.refuses_run("no value is authored, so the stage takes no sources")

    # ---- R: the record (T3)
    def test_T3_a_NULL_crop_writes_nothing(self):
        d = self.s.crops["dill"]
        for k in ("sources", "anchoring_urls", "field_addition", "restatements"):
            d.pop(k)
        d[P.H] = None
        self.s.drop_ev("dill")
        post, n = self.s.run()
        self.assertEqual(C.compact(crop(post, "dill")), C.compact(IDX["dill"]))
        self.assertEqual((n["authored"], n["null"], n["records"]), (45, 1, 45))

    def test_T3_a_record_on_a_crop_with_NO_HEIGHT_authored_REFUSES(self):
        d = self.s.crops["dill"]
        for k in ("sources", "anchoring_urls", "restatements"):
            d.pop(k)
        d[P.H] = None
        self.refuses_run("the stage takes no field_addition (a record on a crop with no height authored refuses)")

    def test_T3_a_SECOND_record_on_a_backfill_crop_REFUSES(self):
        self.s.crops["peach"]["field_addition"] = {"field": "plant_dimensions", "date": "2026-10-02",
                                                   "sources": ["ncsu_ext"], "note": "x"}
        self.refuses_run("a BACKFILL crop already carries its 'plant_dimensions' record; a second record refuses")

    def test_T3_a_SECOND_record_on_a_new_crop_REFUSES(self):
        stage, ev = self.s.load()
        pre = copy.deepcopy(BASE)
        crop(pre, "dill")["verification_status"].setdefault("field_additions", []).append(
            {"field": "plant_dimensions", "date": "2026-09-16", "sources": ["uwi_hort"], "note": "x"})
        self.refuses(lambda: P.check_pre(pre, stage), "already carries a 'plant_dimensions' record; a second record")

    def test_T3_two_records_appended_in_the_post_REFUSES(self):
        def two(post):
            fa = crop(post, "dill")["verification_status"]["field_additions"]
            fa.append(copy.deepcopy(fa[-1]))
        self.refuses_post(two, "dill: field_additions must be the base's, byte for byte, plus exactly the staged")

    def test_T3_ANOTHER_field_additions_entry_edited_REFUSES(self):
        def edit(post):
            crop(post, "dill")["verification_status"]["field_additions"][0]["note"] += " (edited)"
        self.refuses_post(edit, "dill: field_additions must be the base's, byte for byte")

    def test_T3_a_backfill_records_note_edited_REFUSES(self):
        def edit(post):
            P._records(crop(post, "peach"))[0]["note"] += " re-hashed"
        self.refuses_post(edit, "peach: changed outside what the stage names")

    def test_T3_another_verification_status_key_edited_REFUSES(self):
        def edit(post):
            crop(post, "dill")["verification_status"]["launch_ready_content"] = False
        self.refuses_post(edit, "dill: changed outside what the stage names")

    def test_T3_a_new_crop_with_a_value_and_no_record_REFUSES(self):
        self.s.crops["dill"].pop("field_addition")
        self.refuses_run("needs its 'plant_dimensions' field_addition record")

    def test_T3_record_shape_REFUSES(self):
        self.s.crops["dill"]["field_addition"]["extra"] = 1
        self.refuses_run("field_addition needs exactly")

    def test_T3_record_names_the_field(self):
        self.s.crops["dill"]["field_addition"]["field"] = "mature_height_ft"
        self.refuses_run("field_addition field must be 'plant_dimensions'")

    def test_T3_record_sources_within_the_sibling(self):
        self.s.crops["dill"]["field_addition"]["sources"] = ["uwi_hort"]
        self.refuses_run("field_addition sources must be a non-empty subset")

    def test_T3_record_dated_and_noted(self):
        self.s.crops["dill"]["field_addition"]["date"] = "soon"
        self.refuses_run("field_addition date 'soon' is not a date")
        self.s.crops["dill"]["field_addition"]["date"] = "2026-10-02"
        self.s.crops["dill"]["field_addition"]["note"] = " "
        self.refuses_run("field_addition note is empty")

    # ---- E: evidence
    def test_a_value_without_evidence_REFUSES(self):
        self.s.drop_ev("dill")
        self.refuses_run("dill: mature_height_ft [1,2] has no EVIDENCE row")

    def test_a_spread_without_evidence_REFUSES(self):
        self.s.drop_ev("broccoli", P.S)
        self.refuses_run("broccoli: mature_spread_ft [0.5,1] has no EVIDENCE row")

    def test_a_ONE_ENDED_quote_cannot_carry_a_range(self):
        self.s.drop_ev("dill")
        url = self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["url"]
        self.s.add_ev("dill", P.H, [1, 2], "ncsu_ext", url, "synthetic dill: plants grow up to 2 feet tall.")
        self.refuses_run("the rows state only [2]; both endpoints must be stated")

    def test_a_value_mismatch_REFUSES(self):
        self.s.ev[[r["crop"] for r in self.s.ev].index("dill")]["value"] = "[1,3]"
        self.refuses_run("value [1,3] != the crop's [1,2]")

    def test_the_source_must_be_the_siblings(self):
        self.s.ev[[r["crop"] for r in self.s.ev].index("dill")]["source_id"] = "uwi_hort"
        self.refuses_run("source 'uwi_hort' is not in mature_dimensions_sources")

    def test_the_url_must_be_the_siblings_anchor(self):
        self.s.ev[[r["crop"] for r in self.s.ev].index("dill")]["url"] = "https://hort.extension.wisc.edu/x/"
        self.refuses_run("url is not the sibling's anchoring url")

    def test_a_url_not_in_the_manifest_REFUSES(self):
        dill = [r["sha256"] for r in self.s.ev if r["crop"] == "dill"][0]
        self.s.manifest = [m for m in self.s.manifest if m["sha256"] != dill]
        self.refuses_run("is not in")

    def test_a_quote_not_in_the_bytes_REFUSES(self):
        self.s.ev[[r["crop"] for r in self.s.ev].index("dill")]["quote"] = "dill plants grow 1 to 2 feet tall on mars"
        self.refuses_run("the quote is not in the cached bytes")

    def test_a_quote_stating_the_WRONG_DIMENSION_REFUSES(self):
        self.s.drop_ev("broccoli", P.S)
        url = self.s.crops["broccoli"]["anchoring_urls"]["ncsu_ext"]["url"]
        self.s.add_ev("broccoli", P.S, [0.5, 1], "ncsu_ext", url, "synthetic: plants grow 0.5 to 1 feet tall here.")
        self.refuses_run("the quote states neither endpoint of [0.5,1] as a mature_spread_ft")

    def test_tampered_bytes_REFUSE(self):
        stage, ev = self.s.load()
        sha = [r["sha256"] for r in ev if r["crop"] == "dill"][0]
        with open(os.path.join(self.s.ev_dir, sha + ".html"), "ab") as f:
            f.write(b" ")
        self.refuses(lambda: P.run(copy.deepcopy(BASE), stage, ev, self.s.ev_dir), "not their name")

    def test_evidence_for_a_field_the_crop_does_not_carry_REFUSES(self):
        url = self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["url"]
        self.s.add_ev("dill", P.S, [1, 2], "ncsu_ext", url, "synthetic dill: 1 to 2 feet wide.")
        self.refuses_run("the crop carries no mature_spread_ft")

    def test_a_row_naming_another_entry_REFUSES(self):
        self.s.ev[[r["crop"] for r in self.s.ev].index("dill")]["entry_id"] = "row-none"
        self.refuses_run("a height row names entry 'mature_dimensions'")

    # ---- S: restatements (H3)
    def test_H3_an_unadjudicated_restatement_REFUSES(self):
        self.s.crops["dill"]["restatements"] = self.s.crops["dill"]["restatements"][1:]
        self.refuses_run("dill: a height moves (null -> [1,2]) and the restatement at")

    def test_H3_dills_5_ft_edited_lands(self):
        d = self.s.crops["dill"]
        hits = P.height_strings(IDX["dill"], False)
        target = next(p for p in hits if "5 feet" in C.compact(self._at(IDX["dill"], p)))
        old = self._at(IDX["dill"], target)
        new = old.replace("3 to 5 feet", "18 inches to 4 feet").replace("5 feet", "4 feet")
        self.assertNotEqual(old, new)
        for r in d["restatements"]:
            if r["path"] == target:
                r["verdict"] = "edited"
        d["edits"] = [{"path": target, "new": new, "reason": "H3: UW-Madison states 18 inches to 4 feet"}]
        post, _ = self.s.run()
        self.assertEqual(self._at(crop(post, "dill"), target), new)

    def _at(self, c, path):
        node = c
        for seg in P.resolve(c, path):
            node = node[seg]
        return node

    def test_edited_without_an_edit_REFUSES(self):
        self.s.crops["dill"]["restatements"][0]["verdict"] = "edited"
        self.refuses_run("is adjudicated 'edited' but no edit touches it")

    def test_an_edit_not_at_an_edited_restatement_REFUSES(self):
        p = self.s.crops["dill"]["restatements"][0]["path"]
        self.s.crops["dill"]["edits"] = [{"path": p, "new": "x", "reason": "r"}]
        self.refuses_run("is not at a restatement adjudicated 'edited'")

    def test_an_edit_on_an_owned_key_REFUSES(self):
        self.s.crops["dill"]["edits"] = [{"path": "mature_height_ft", "new": [1, 5], "reason": "r"}]
        self.refuses_run("touches a key the promote owns or a record")
        self.s.crops["dill"]["edits"] = [{"path": "verification_status.status", "new": "x", "reason": "r"}]
        self.refuses_run("touches a key the promote owns or a record")

    def test_restatements_on_a_backfill_crop_whose_values_do_not_move_REFUSE(self):
        self.s.crops["peach"]["restatements"] = [{"path": "description_beginner", "verdict": "agrees", "note": "x"}]
        self.refuses_run("peach: restatements staged but no value moves")

    def test_a_restatement_with_no_note_REFUSES(self):
        self.s.crops["dill"]["restatements"][0]["note"] = ""
        self.refuses_run("a restatement needs path, verdict agrees|edited, and a note")

    def test_an_edit_value_not_the_stages_in_the_post_REFUSES(self):
        d = self.s.crops["dill"]
        p = d["restatements"][0]["path"]
        d["restatements"][0]["verdict"] = "edited"
        d["edits"] = [{"path": p, "new": "synthetic new prose", "reason": "r"}]
        stage, ev, post = self.s.post()
        P.set_at(crop(post, "dill"), P.resolve(crop(post, "dill"), p), "something else")
        self.refuses(lambda: self.s.check_post(stage, ev, post), "is not the edit's new value")

    # ---- B: blast radius
    def test_a_roster_reorder_REFUSES(self):
        self.refuses_post(lambda p: p["crops"].reverse(), "the roster changed")

    def test_a_top_level_change_REFUSES(self):
        self.refuses_post(lambda p: p["source_catalog"].pop("umd_ext"), "top-level 'source_catalog' changed")

    def test_a_shell_change_REFUSES(self):
        shell = next(c["slug"] for c in BASE["crops"] if not P.certified(c))
        self.refuses_post(lambda p: crop(p, shell).__setitem__("zz", 1), f"shell {shell} changed")

    def test_an_unstaged_crop_edited_REFUSES(self):
        self.refuses_post(lambda p: crop(p, "carrot").__setitem__("mature_height_ft", [1, 2]),
                          "carrot: changed outside what the stage names")

    def test_a_backfill_crop_value_changed_in_the_post_REFUSES(self):
        self.refuses_post(lambda p: crop(p, "peach").__setitem__("mature_height_ft", [15, 26]),
                          "peach: changed outside what the stage names")

    def test_a_stray_field_on_a_staged_crop_REFUSES(self):
        self.refuses_post(lambda p: crop(p, "dill").__setitem__("footprint_inches", 4),
                          "dill: changed outside what the stage names")

    def test_a_value_not_the_stages_in_the_post_REFUSES(self):
        self.refuses_post(lambda p: crop(p, "dill").__setitem__("mature_height_ft", [1, 3]),
                          "dill: mature_height_ft [1,3] is not the stage's [1,2]")

    def test_a_sibling_not_the_stages_in_the_post_REFUSES(self):
        self.refuses_post(lambda p: crop(p, "dill")[P.SIB_S].append("uwi_hort"), "dill: the sibling pair is not")


class Gates(Base):
    def test_A59_sibling_runs_on_the_post_state(self):
        def strip(p):
            c = crop(p, "dill")
            c[P.SIB_A]["ncsu_ext"]["url"] = "ftp://x"
        self.refuses_post(strip, "dill: the sibling pair is not the stage's")
        stage, ev, post = self.s.post()
        import plant_dimensions_gate as PDG
        c = crop(post, "dill")
        c[P.SIB_A]["ncsu_ext"]["url"] = "ftp://x"
        self.assertTrue(PDG.sibling_violations(c))

    def test_A62_runs_ARMED_on_the_post_state(self):
        """A crop authored with no sibling in the post fails A62's armed mature_dimensions block."""
        def strip(p):
            c = crop(p, "carrot")
            c["mature_height_ft"] = [1, 2]
        stage, ev, post = self.s.post()
        strip(post)
        import sourced_block_ratchet_gate as SBR
        self.assertTrue(any("carrot|mature_dimensions|" in m
                            for m in SBR.roster(post, mature_dimensions_armed=True)[3]))

    def test_the_post_state_gates_run_armed(self):
        src = inspect.getsource(P.check_post)
        self.assertIn("presence=True, coverage=True, sibling=True", src)
        self.assertIn("mature_dimensions_armed=True", src)

    # REACHABILITY. Stage guard C refuses every defect these gates catch, so a normal stage can never reach
    # them (an earlier check masks the guard). Each driver corrupts the stage AFTER check_pre, so the defect
    # survives into a post-state that passes every value and evidence check, and only the gate can refuse it.
    def _past_pre(self, corrupt, patch_a59=False):
        stage, ev = self.s.load()
        P.check_pre(copy.deepcopy(BASE), stage)
        corrupt(stage, ev)
        self.s.ev = ev
        self.s.write()
        stage2, ev2 = P.load_stage(self.s.stage)
        post = P.apply_to(copy.deepcopy(BASE), stage2)
        import plant_dimensions_gate as PDG
        saved = PDG.all_violations
        if patch_a59:
            PDG.all_violations = lambda *a, **k: []
        try:
            return self.refuses(lambda: P.check_post(copy.deepcopy(BASE), post, stage2, ev2, self.s.ev_dir), "")
        finally:
            PDG.all_violations = saved

    def test_REACH_A59_sibling_a_source_with_no_anchor(self):
        def corrupt(stage, ev):
            stage["dill"]["sources"] = ["ncsu_ext", "uwi_hort"]
            self.s.crops = stage
        msg = self._past_pre(corrupt)
        self.assertIn("A59 (armed: presence, coverage, sibling)", msg)
        self.assertIn("'uwi_hort' has no http(s) anchor", msg)

    def test_REACH_A62_armed_a_blank_sibling_source(self):
        """A59 is patched out so A62's armed mature_dimensions block is the only gate that can refuse."""
        def corrupt(stage, ev):
            d = stage["dill"]
            d["sources"] = [" "]
            d["anchoring_urls"] = {" ": d["anchoring_urls"]["ncsu_ext"]}
            for r in ev:
                if r["crop"] == "dill":
                    r["source_id"] = " "
            self.s.crops = stage
        msg = self._past_pre(corrupt, patch_a59=True)
        self.assertIn("A62 (mature_dimensions armed)", msg)
        self.assertIn("dill|mature_dimensions|mature_dimensions_sources", msg)

    def test_REACH_A63_a_bare_host_sibling_anchor(self):
        def corrupt(stage, ev):
            bare = "https://plants.ces.ncsu.edu/"
            stage["dill"]["anchoring_urls"]["ncsu_ext"]["url"] = bare
            for r in ev:
                if r["crop"] == "dill":
                    r["url"] = bare
                    self.s.manifest.append({"sha256": r["sha256"], "url": bare})
            self.s.crops = stage
        msg = self._past_pre(corrupt)
        self.assertIn("A63 on the post-state", msg)

    def test_numeric_sanity_runs_on_the_post_state(self):
        self.s.crops["dill"][P.H] = [1, 40]
        url = self.s.crops["dill"]["anchoring_urls"]["ncsu_ext"]["url"]
        self.s.drop_ev("dill")
        self.s.add_ev("dill", P.H, [1, 40], "ncsu_ext", url, "synthetic dill: plants grow 1 to 40 feet tall.")
        self.refuses_run("numeric_sanity / display_readiness")


class HeightScanner(unittest.TestCase):
    def test_the_scanner_finds_dills_5_ft_prose(self):
        hits = P.height_strings(IDX["dill"], False)
        self.assertGreaterEqual(len(hits), 4, hits)

    def test_width_words_scan_only_when_a_spread_is_authored(self):
        c = {"slug": "t", "tips": ["rows sit 3 feet wide."]}
        self.assertEqual(P.height_strings(c, False), [])
        self.assertEqual(P.height_strings(c, True), ["tips[0]"])

    def test_the_scanner_skips_records_and_citations(self):
        c = {"slug": "t", "verification_status": {"note": "grows 3 feet tall"},
             "mature_dimensions_anchoring_urls": {"x": {"url": "grows 3 feet tall"}}}
        self.assertEqual(P.height_strings(c, True), [])


if __name__ == "__main__":
    unittest.main()
