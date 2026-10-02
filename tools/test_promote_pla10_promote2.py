#!/usr/bin/env python3
"""Guard suite for promote_pla10_promote2 (PLA-10 promote 2), built in the session-1 tools commit
(2026-10-02) BEFORE any stage exists. Run: python3 -m pytest tools/test_promote_pla10_promote2.py -q

This commit gives promote 2 its two RECORD allowances (SESSION3_HANDOFF owed items 1 and 2):
  - a rootstock_options[] row may gain ONE source + its anchoring url, only while the same stage authors
    that row's spacing_inches override (R1, apple only);
  - an open finding under verification_status may have a dated [CORRECTION ...] APPENDED to its summary.
Nothing else under verification_status, and nothing else on a rootstock row, becomes writable.

The base is replay-pinned through promote_fixture (cf1d480d -> d021116), never the live file. Drivers build
a SYNTHETIC stage + evidence cache in a temp dir (nothing here is a citation), plus one control that runs
apple's owed overrides against the REAL hashed NCSU bytes in tools/.evidence_cache. Each guard family has a
driver that injects its defect and asserts the REFUSAL TEXT.
SHIPS MUTATION-TESTED via mutate_pla10_promote2.py.
"""
import copy, csv, hashlib, inspect, json, os, shutil, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla10_promote2 as P  # noqa: E402
import pla10_promote_common as C  # noqa: E402

BASE = json.loads(promote_fixture.pre_state(P.BASE_SHA))
IDX = {c["slug"]: c for c in BASE["crops"]}
NCSU = "ncsu_ext_handbook_tree_fruit"
NCSU_URL = "https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts"
NCSU_SHA = "0e16d13e3df8fe822acab5ae904bdcc1de5346cf7ba7d96db5bb15e3dc164408"
# SESSION3_HANDOFF owed item 1: NCSU Extension Gardener Handbook Table 15-4, nonspur, feet.
OWED = {"M9": ([48, 96], "M.9** 4 – 8 3 – 5 6 – 11"), "M26": (None, None), "MM106": ([144, 192], "MM.106 12 – 16 8 – 11 17 – 22"),
        "MM111": ([168, 216], "MM.111 14 – 18 9 – 12 20 – 25"), "seedling": ([216, 300], "Seedling* 18 – 25 12 – 16 25 – 35")}
# owed item 2: the seven in-canonical *_pilot_spacing_* findings (fava's is a plan decision, not a fixture).
PILOT = {"acorn-squash": "acorn_pilot_spacing_prose", "spaghetti-squash": "spaghetti_pilot_spacing_prose",
         "butternut-squash": "butternut_pilot_spacing_capped_72in",
         "watermelon": "watermelon_pilot_spacing_capped_72in", "pumpkin": "pumpkin_pilot_spacing_capped_72in",
         "honeydew-melon": "honeydew_pilot_spacing_capped_48in", "cantaloupe": "cantaloupe_pilot_spacing_in_row"}
APPEND = " [CORRECTION 2026-10-02: synthetic fixture text -- see test_promote_pla10_promote2.]"


def corr(fid, append=APPEND):
    return {"id": fid, "append": append}


class Synthetic:
    """A stage + evidence cache in a temp dir. Quotes are written into synthetic page bytes, so the
    evidence machinery runs end to end; `real=True` uses the real cache for apple's NCSU rows instead."""

    def __init__(self, real=False):
        self.root = tempfile.mkdtemp(prefix="pla10p2_")
        self.stage = os.path.join(self.root, "stage")
        os.makedirs(os.path.join(self.stage, "crops"))
        self.real = real
        self.ev_dir = P.EVIDENCE if real else os.path.join(self.root, "evidence")
        if not real:
            os.makedirs(self.ev_dir)
        self.crops, self.ev, self.manifest = {}, [], []
        rows = []
        for name, (val, quote) in OWED.items():
            r = {"name": name, "spacing_inches": val}
            if val is not None:
                r["add_source"] = {"id": NCSU, "url": NCSU_URL, "verified": "2026-10-02"}
                self.add_ev("apple", f"rootstock_options[name={name}]", "spacing_inches", val, NCSU, NCSU_URL,
                            quote)
            rows.append(r)
        self.crops["apple"] = {"slug": "apple", "decision": "synthetic: NCSU Table 15-4 nonspur",
                               "rootstock_spacing": rows}
        for slug, fid in PILOT.items():
            self.crops[slug] = {"slug": slug, "decision": "synthetic: D1a correction",
                                "finding_corrections": [corr(fid)]}

    def add_ev(self, crop, entry_id, field, value, sid, url, quote, page=None):
        if self.real:
            sha = NCSU_SHA
        else:
            body = (page if page is not None else f"<html><p>{quote}</p></html>").encode("utf-8")
            sha = hashlib.sha256(body).hexdigest()
            with open(os.path.join(self.ev_dir, sha + ".html"), "wb") as f:
                f.write(body)
            self.manifest.append({"sha256": sha, "url": url})
        self.ev.append({"crop": crop, "entry_id": entry_id, "field": field, "value": C.compact(value),
                        "source_id": sid, "url": url, "sha256": sha, "quote": quote})

    def write(self):
        for slug, s in self.crops.items():
            with open(os.path.join(self.stage, "crops", slug + ".json"), "w", encoding="utf-8") as f:
                json.dump(s, f, ensure_ascii=False)
        with open(os.path.join(self.stage, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=C.EVIDENCE_COLS, delimiter="\t")
            w.writeheader()
            w.writerows(self.ev)
        if not self.real:
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
        return stage, ev, P.apply_to(copy.deepcopy(BASE), stage)

    def check_post(self, stage, ev, post):
        return P.check_post(copy.deepcopy(BASE), post, stage, ev, self.ev_dir)

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


def row(data, name, slug="apple"):
    c = next(c for c in data["crops"] if c["slug"] == slug)
    return next(r for r in c["rootstock_options"] if r["name"] == name)


def finding(data, slug, fid):
    c = next(c for c in data["crops"] if c["slug"] == slug)
    return next(f for f in c["verification_status"]["open_findings"] if f.get("id") == fid)


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
class Clean(Base):
    def test_the_clean_stage_passes_and_changes_exactly_the_named_leaves(self):
        post, n = self.s.run()
        self.assertEqual(n, {"crops": 8, "overrides": 4, "nulls": 1, "sources_added": 4, "corrections": 7})
        for name, (val, _) in OWED.items():
            r, b = row(post, name), row(BASE, name)
            self.assertEqual(r["spacing_inches"], val)
            if val is None:
                self.assertEqual(r["sources"], b["sources"])
            else:
                self.assertEqual(r["sources"], b["sources"] + [NCSU])
                self.assertEqual(r["anchoring_urls"][NCSU], {"url": NCSU_URL, "verified": "2026-10-02"})
        for slug, fid in PILOT.items():
            self.assertEqual(finding(post, slug, fid)["summary"], finding(BASE, slug, fid)["summary"] + APPEND)
        changed = set()
        for a, b in zip(BASE["crops"], post["crops"]):
            changed |= {(a["slug"],) + p for p in C.leaf_diff(a, b)}
        want = {("apple", "rootstock_options", i, k) for i, r in enumerate(IDX["apple"]["rootstock_options"])
                for k in ("spacing_inches",) + (("sources", ) if OWED[r["name"]][0] else ())}
        want |= {("apple", "rootstock_options", i, "anchoring_urls", NCSU)
                 for i, r in enumerate(IDX["apple"]["rootstock_options"]) if OWED[r["name"]][0]}
        for slug, fid in PILOT.items():
            i = [f.get("id") for f in IDX[slug]["verification_status"]["open_findings"]].index(fid)
            want.add((slug, "verification_status", "open_findings", i, "summary"))
        self.assertEqual(changed, want)

    def test_apples_owed_overrides_pass_against_the_REAL_hashed_ncsu_bytes(self):
        real = Synthetic(real=True)
        try:
            post, n = real.run()
            self.assertEqual(n["overrides"], 4)
            self.assertEqual(row(post, "MM111")["spacing_inches"], [168, 216])
        finally:
            real.close()

    def test_the_base_is_pinned(self):
        self.assertEqual(P.BASE_SHA, "cf1d480dfc926b226f63fde2fbdbc548e9d06487ed749e7431a06710431f2e49")
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_an_empty_stage_REFUSES(self):
        self.s.crops = {}
        self.refuses_run("the stage names no crop")

    def test_the_rootstock_crop_list_is_the_literal(self):
        self.assertEqual(P.ROOTSTOCK_CROPS, ("apple",))

    def test_the_copied_helpers_are_byte_identical_to_promote_1(self):
        import promote_pla10_planting_layout as P1
        for name in ("sha256_bytes", "serialize", "compact", "leaf_diff", "norm_text", "_numbers",
                     "quote_states", "pdf_text", "manifest"):
            self.assertEqual(inspect.getsource(getattr(C, name)), inspect.getsource(getattr(P1, name)), name)
        self.assertEqual((C.IDIOMS, C.PDF_TEXT_EXTRACTOR, C.EVIDENCE_COLS),
                         (P1.IDIOMS, P1.PDF_TEXT_EXTRACTOR, P1.EVIDENCE_COLS))


# ------------------------------------------------------------------ stage shape
class StageShape(Base):
    def test_an_unknown_stage_key_REFUSES(self):
        self.s.crops["apple"]["edits"] = []
        self.refuses(self.s.load, "unknown keys ['edits']")

    def test_a_stage_needs_a_decision_row(self):
        self.s.crops["apple"]["decision"] = "  "
        self.refuses(self.s.load, "the decision row is empty")

    def test_a_slug_that_does_not_match_its_file_REFUSES(self):
        self.s.crops["apple"]["slug"] = "pear-asian"
        self.refuses(self.s.load, "does not match its file name")


# ------------------------------------------------------------------ guard R: rootstock overrides
class Rootstock(Base):
    def test_an_override_on_a_crop_off_the_R1_list_REFUSES(self):
        self.s.crops["pear-asian"] = {"slug": "pear-asian", "decision": "x", "rootstock_spacing": [
            {"name": r["name"], "spacing_inches": None} for r in IDX["pear-asian"]["rootstock_options"]]}
        self.refuses_run("pear-asian: rootstock_spacing is ruled for ['apple'] only (R1)")

    def test_every_row_must_be_named_missing(self):
        self.s.crops["apple"]["rootstock_spacing"] = [r for r in self.s.crops["apple"]["rootstock_spacing"]
                                                      if r["name"] != "M26"]
        self.refuses_run("apple: rootstock_spacing names != the crop's rows; missing ['M26'], extra []")

    def test_every_row_must_be_named_extra(self):
        self.s.crops["apple"]["rootstock_spacing"].append({"name": "G.41", "spacing_inches": None})
        self.refuses_run("missing [], extra ['G.41']")

    def test_a_row_named_twice_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"].append({"name": "M26", "spacing_inches": None})
        self.refuses_run("apple: rootstock row 'M26' is named twice")

    def test_an_unknown_row_key_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][1]["mature_height_ft"] = [10, 14]
        self.refuses_run("apple M26: a rootstock_spacing row takes only name, spacing_inches, add_source")

    def test_an_override_out_of_order_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][0]["spacing_inches"] = [96, 48]
        self.refuses_run("apple M9: spacing_inches must be null or [lo, hi] with 0 < lo <= hi")

    def test_an_override_not_a_pair_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][0]["spacing_inches"] = "4-8 ft"
        self.refuses_run("apple M9: spacing_inches must be null or [lo, hi]")

    def test_a_base_that_already_carries_an_override_REFUSES(self):
        base = copy.deepcopy(BASE)
        row(base, "M26")["spacing_inches"] = None
        stage, ev = self.s.load()
        self.refuses(lambda: P.run(base, stage, ev, self.s.ev_dir),
                     "base already carries rootstock_options[].spacing_inches on apple M26")

    # -- the source allowance is scoped to the spacing override
    def test_add_source_on_a_null_override_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][1]["add_source"] = {"id": NCSU, "url": NCSU_URL,
                                                                       "verified": "2026-10-02"}
        self.refuses_run("apple M26: add_source is allowed only while authoring a non-null spacing_inches")

    def test_add_source_already_cited_by_the_row_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][0]["add_source"]["id"] = "umd_ext"
        self.refuses_run("apple M9: add_source 'umd_ext' is already in the row's sources")

    def test_add_source_off_the_catalog_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][0]["add_source"]["id"] = "not_a_source"
        self.refuses_run("apple M9: add_source 'not_a_source' is not in source_catalog")

    def test_add_source_shape_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][0]["add_source"] = {"id": NCSU, "url": NCSU_URL}
        self.refuses_run("apple M9: add_source needs exactly id, url, verified")

    # -- post-state tampering (the transform is not trusted)
    def test_a_source_added_to_a_NULL_override_row_in_the_post_REFUSES(self):
        def m(post):
            r = row(post, "M26")
            r["sources"] = r["sources"] + [NCSU]
            r["anchoring_urls"][NCSU] = {"url": NCSU_URL, "verified": "2026-10-02"}
        self.refuses_post(m, "apple: changed outside what the stage names")

    def test_a_source_on_a_non_spacing_rootstock_field_REFUSES(self):
        def m(post):
            row(post, "M9")["mature_height_ft_sources"] = [NCSU]
        self.refuses_post(m, "apple: changed outside what the stage names: ['rootstock_options[0].mature_height_ft_sources']")

    def test_another_rootstock_field_edited_REFUSES(self):
        def m(post):
            row(post, "MM106")["spread_ft"] = 16
        self.refuses_post(m, "rootstock_options[2].spread_ft")

    def test_an_existing_anchor_rewritten_REFUSES(self):
        def m(post):
            row(post, "M9")["anchoring_urls"]["umd_ext"]["verified"] = "2026-10-02"
        self.refuses_post(m, "rootstock_options[0].anchoring_urls.umd_ext")

    def test_sources_replaced_not_appended_REFUSES(self):
        def m(post):
            row(post, "M9")["sources"] = [NCSU]
        self.refuses_post(m, "apple M9: sources must be the base's plus exactly 'ncsu_ext_handbook_tree_fruit'")

    def test_sources_reordered_REFUSES(self):
        def m(post):
            row(post, "M9")["sources"] = [NCSU, "umd_ext"]
        self.refuses_post(m, "apple M9: sources must be the base's plus exactly")

    def test_the_added_anchor_not_the_stages_REFUSES(self):
        def m(post):
            row(post, "M9")["anchoring_urls"][NCSU]["url"] = NCSU_URL + "#t15-4"
        self.refuses_post(m, "apple M9: anchoring_urls['ncsu_ext_handbook_tree_fruit'] is not the stage's add_source")

    def test_an_override_value_not_the_stages_REFUSES(self):
        def m(post):
            row(post, "M9")["spacing_inches"] = [48, 72]
        self.refuses_post(m, "apple M9: spacing_inches is not the stage's")

    def test_a_null_override_dropped_from_the_post_REFUSES(self):
        def m(post):
            del row(post, "M26")["spacing_inches"]
        self.refuses_post(m, "apple M26: spacing_inches is not the stage's")


# ------------------------------------------------------------------ guard E: evidence on every override
class Evidence(Base):
    def test_an_override_without_evidence_REFUSES(self):
        self.s.ev = [r for r in self.s.ev if r["entry_id"] != "rootstock_options[name=MM106]"]
        self.refuses_run("apple rootstock_options[name=MM106]: spacing_inches [144,192] has no EVIDENCE row")

    def test_a_value_mismatch_REFUSES(self):
        self.s.ev[0]["value"] = "[48,72]"
        self.refuses_run("value [48,72] != the row's [48,96]")

    def test_evidence_for_a_null_override_REFUSES(self):
        self.s.add_ev("apple", "rootstock_options[name=M26]", "spacing_inches", [96, 144], NCSU, NCSU_URL,
                      "M.26** 8 – 12 5 – 8 11 – 17")
        self.refuses_run("the row carries no spacing_inches")

    def test_evidence_naming_no_row_REFUSES(self):
        self.s.ev[0]["entry_id"] = "rootstock_options[name=G.41]"
        self.refuses_run("no such crop/row in the post-state")

    def test_the_source_must_be_the_rows(self):
        self.s.ev[0]["source_id"] = "uga_ext"
        self.refuses_run("source 'uga_ext' is not in the row's sources")

    def test_the_url_must_be_the_rows_anchor(self):
        self.s.ev[0]["url"] = NCSU_URL + "?x"
        self.refuses_run("url is not the row's anchoring url")

    def test_a_url_not_in_the_manifest_REFUSES(self):
        self.s.manifest[0]["url"] = "https://example.org/other"
        self.refuses_run("is not in")

    def test_a_quote_not_in_the_bytes_REFUSES(self):
        self.s.ev[0]["quote"] = "M.9** 4 – 9 3 – 5 6 – 11"
        self.refuses_run("the quote is not in the cached bytes")

    def test_a_quote_that_states_no_endpoint_REFUSES(self):
        self.s.ev = [r for r in self.s.ev if r["entry_id"] != "rootstock_options[name=M9]"]
        self.s.add_ev("apple", "rootstock_options[name=M9]", "spacing_inches", [48, 96], NCSU, NCSU_URL,
                      "M.9 trees should be staked at planting")
        self.refuses_run("the quote states neither endpoint of [48,96]")

    def test_tampered_bytes_REFUSE(self):
        self.s.write()
        p = os.path.join(self.s.ev_dir, self.s.ev[0]["sha256"] + ".html")
        with open(p, "ab") as f:
            f.write(b" ")
        stage, ev = P.load_stage(self.s.stage)
        self.refuses(lambda: P.run(copy.deepcopy(BASE), stage, ev, self.s.ev_dir), "hash to")

    def test_a_row_source_off_the_catalog_REFUSES(self):
        stage, ev, post = self.s.post()
        post["source_catalog"] = {k: v for k, v in post["source_catalog"].items() if k != NCSU}
        self.refuses(lambda: P.check_evidence({c["slug"]: c for c in post["crops"]}, stage, ev,
                                              post["source_catalog"], self.s.ev_dir),
                     "source 'ncsu_ext_handbook_tree_fruit' is not in source_catalog")


# ------------------------------------------------------------------ guard F: finding corrections
class Corrections(Base):
    def test_a_correction_must_be_one_dated_correction_line(self):
        for bad in (" corrected: was a blend", "[CORRECTION 2026-10-02: x -- see y.]",
                    " [CORRECTION 2026-13-02: x -- see y.]", " [CORRECTION 2026-10-02: x.]",
                    " [CORRECTION 2026-10-02: x -- see y.] [CORRECTION 2026-10-02: z -- see w.]",
                    " [CORRECTION 2026-10-02: x -- see y.] trailing"):
            self.s.crops["pumpkin"]["finding_corrections"] = [corr(PILOT["pumpkin"], bad)]
            self.refuses_run("pumpkin pumpkin_pilot_spacing_capped_72in: append must be exactly one ' [CORRECTION <YYYY-MM-DD>: <what> -- see <ref>.]'")

    def test_a_correction_on_an_unknown_finding_REFUSES(self):
        self.s.crops["pumpkin"]["finding_corrections"] = [corr("pumpkin_no_such_finding")]
        self.refuses_run("pumpkin: open finding 'pumpkin_no_such_finding' matches 0 findings")

    def test_two_corrections_on_one_finding_in_one_stage_REFUSES(self):
        self.s.crops["pumpkin"]["finding_corrections"].append(corr(PILOT["pumpkin"]))
        self.refuses_run("pumpkin: finding 'pumpkin_pilot_spacing_capped_72in' is corrected twice")

    def test_a_correction_row_shape_REFUSES(self):
        self.s.crops["pumpkin"]["finding_corrections"] = [{"id": PILOT["pumpkin"], "append": APPEND,
                                                            "field": "basis"}]
        self.refuses_run("pumpkin: a finding correction takes exactly id and append")

    def test_a_correction_already_applied_REFUSES(self):
        base = copy.deepcopy(BASE)
        finding(base, "pumpkin", PILOT["pumpkin"])["summary"] += APPEND
        stage, ev = self.s.load()
        self.refuses(lambda: P.run(base, stage, ev, self.s.ev_dir),
                     "pumpkin pumpkin_pilot_spacing_capped_72in: the summary already ends with this correction")

    # -- post-state tampering
    def test_a_correction_that_REWRITES_rather_than_appends_REFUSES(self):
        def m(post):
            f = finding(post, "pumpkin", PILOT["pumpkin"])
            f["summary"] = f["summary"].replace("spacing_inches is [36,72]", "spacing_inches was [36,72]")
        self.refuses_post(m, "pumpkin pumpkin_pilot_spacing_capped_72in: summary must be the base's, byte for byte, plus the append")

    def test_a_correction_written_into_basis_REFUSES(self):
        def m(post):
            f = finding(post, "pumpkin", PILOT["pumpkin"])
            f["basis"] += APPEND
        self.refuses_post(m, "pumpkin: changed outside what the stage names: ['verification_status.open_findings[1].basis']")

    def test_the_status_edited_REFUSES(self):
        def m(post):
            next(c for c in post["crops"] if c["slug"] == "pumpkin")["verification_status"]["status"] = "pending"
        self.refuses_post(m, "verification_status.status")

    def test_a_launch_flag_edited_REFUSES(self):
        def m(post):
            next(c for c in post["crops"] if c["slug"] == "plum")["verification_status"]["launch_ready_core"] = True
        self.refuses_post(m, "plum: changed outside what the stage names: ['verification_status.launch_ready_core']")

    def test_the_log_ref_edited_REFUSES(self):
        def m(post):
            vs = next(c for c in post["crops"] if c["slug"] == "pumpkin")["verification_status"]
            vs["verification_log_ref"] = str(vs.get("verification_log_ref")) + APPEND
        self.refuses_post(m, "verification_status.verification_log_ref")

    def test_a_finding_added_REFUSES(self):
        def m(post):
            vs = next(c for c in post["crops"] if c["slug"] == "pumpkin")["verification_status"]
            vs["open_findings"].append({"id": "new", "summary": "x"})
        self.refuses_post(m, "verification_status.open_findings")

    def test_another_findings_summary_edited_REFUSES(self):
        def m(post):
            f = next(c for c in post["crops"] if c["slug"] == "pumpkin")["verification_status"]["open_findings"][0]
            f["summary"] += APPEND
        self.refuses_post(m, "pumpkin: changed outside what the stage names: ['verification_status.open_findings[0].summary']")

    def test_a_field_addition_record_edited_REFUSES(self):
        def m(post):
            vs = next(c for c in post["crops"] if c["slug"] == "apple")["verification_status"]
            vs["field_additions"].append({"field": "x"})
        self.refuses_post(m, "verification_status.field_additions")


# ------------------------------------------------------------------ guard B: blast radius, sets first
class BlastRadius(Base):
    def test_a_roster_reorder_REFUSES(self):
        self.refuses_post(lambda p: p["crops"].reverse(), "the roster changed (set or order)")

    def test_a_top_level_key_added_REFUSES(self):
        self.refuses_post(lambda p: p.__setitem__("ghost", 1), "top-level keys changed: ['ghost']")

    def test_a_top_level_change_REFUSES(self):
        self.refuses_post(lambda p: p["source_catalog"].pop(NCSU), "top-level 'source_catalog' changed")

    def test_a_shell_change_REFUSES(self):
        shell = next(c["slug"] for c in BASE["crops"] if not P.certified(c))

        def m(post):
            next(c for c in post["crops"] if c["slug"] == shell)["name"] = "x"
        self.refuses_post(m, f"shell {shell} changed")

    def test_a_stray_crop_field_REFUSES(self):
        def m(post):
            next(c for c in post["crops"] if c["slug"] == "apple")["spacing_inches"] = [48, 96]
        self.refuses_post(m, "apple: changed outside what the stage names: ['spacing_inches[0]', 'spacing_inches[1]']")

    def test_a_removed_crop_key_REFUSES(self):
        def m(post):
            del next(c for c in post["crops"] if c["slug"] == "lettuce-leaf")["row_spacing_reason"]
        self.refuses_post(m, "lettuce-leaf: changed outside what the stage names: ['row_spacing_reason']")

    def test_an_unstaged_crop_edited_REFUSES(self):
        def m(post):
            row(post, "Gisela 6", "cherry-sweet")["spacing_inches"] = [144, 180]
        self.refuses_post(m, "cherry-sweet: changed outside what the stage names")


# ------------------------------------------------------------------ guard G: the gates on the post-state
class Gates(Base):
    def test_A63_runs_on_the_post_state(self):
        # a sole bare anchor no allowance can create, so it is seeded in the base: A63 must see it in the post
        base = copy.deepcopy(BASE)
        row(base, "M26")["anchoring_urls"]["umd_ext"]["url"] = "https://extension.umd.edu/"
        stage, ev = self.s.load()
        post = P.apply_to(base, stage)
        self.refuses(lambda: P.check_post(base, post, stage, ev, self.s.ev_dir), "A63 on the post-state")

    def test_A62_runs_on_the_post_state(self):
        base = copy.deepcopy(BASE)
        r = row(base, "M26")
        r["sources"], r["anchoring_urls"] = [], {}
        stage, ev = self.s.load()
        post = P.apply_to(base, stage)
        self.refuses(lambda: P.check_post(base, post, stage, ev, self.s.ev_dir), "A62 on the post-state")

    def test_A44_runs_on_the_post_state(self):
        base = copy.deepcopy(BASE)
        next(c for c in base["crops"] if c["slug"] == "lettuce-leaf")["spacing_inches"] = [1, 2]
        stage, ev = self.s.load()
        post = P.apply_to(base, stage)
        self.refuses(lambda: P.check_post(base, post, stage, ev, self.s.ev_dir), "planting_layout_gate (armed)")

    def test_an_override_over_numeric_sanity_REFUSES(self):
        self.s.crops["apple"]["rootstock_spacing"][4]["spacing_inches"] = [216, 420]
        self.s.ev = [r for r in self.s.ev if r["entry_id"] != "rootstock_options[name=seedling]"]
        self.s.add_ev("apple", "rootstock_options[name=seedling]", "spacing_inches", [216, 420], NCSU, NCSU_URL,
                      "Seedling* 18 – 35 12 – 16 25 – 35")
        self.refuses_run("apple: numeric_sanity / display_readiness")

    def test_a_bare_host_anchor_on_the_added_source_REFUSES(self):
        # A63 alone passes this (co-cited beside umd_ext); the promote's own guard refuses it.
        for r in self.s.crops["apple"]["rootstock_spacing"]:
            if r.get("add_source"):
                r["add_source"]["url"] = "https://content.ces.ncsu.edu/"
        for r in self.s.ev:
            r["url"] = "https://content.ces.ncsu.edu/"
        self.s.manifest = [{"sha256": r["sha256"], "url": "https://content.ces.ncsu.edu/"} for r in self.s.ev]
        self.refuses_run("apple M9: add_source url 'https://content.ces.ncsu.edu/' is a bare host")


if __name__ == "__main__":
    unittest.main()
