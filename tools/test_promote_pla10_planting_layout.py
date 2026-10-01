#!/usr/bin/env python3
"""Guard suite for promote_pla10_planting_layout (PLA-10 promote 1), built in the tools commit
(2026-10-01) BEFORE any stage exists. Run: python3 tools/test_promote_pla10_planting_layout.py

The real stage is authored in sessions 2-3, so every driver here runs against a SYNTHETIC stage built
mechanically from the base (one row-none entry per crop, in_row = the base spacing, cited by a
document-pathed source the crop already cites, evidence bytes written to a temp evidence cache). The
synthetic stage proves the MACHINERY; it is never a stage, and nothing here is a citation.

The base is replay-pinned through promote_fixture (c5fc3d13 -> a181270), never the live file, so the
suite does not move when canonical does. Each guard family in the promote's docstring has a driver
that injects its defect and asserts the REFUSAL TEXT.
SHIPS MUTATION-TESTED via mutate_pla10_promote1.py.
"""
import copy, hashlib, json, os, shutil, sys, tempfile, unittest
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla10_planting_layout as P  # noqa: E402
import planting_layout_migration_known as MIG  # noqa: E402

BASE = json.loads(promote_fixture.pre_state(P.BASE_SHA))
IDX = P.by_slug(BASE)
MICROGREENS = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens", "microgreens-mix",
               "pea-shoots", "radish-microgreens", "sunflower-sprouts", "wheatgrass")


def _anchors(c):
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "anchoring_urls" or k.endswith("_anchoring_urls"):
                    if isinstance(v, dict):
                        for s, a in v.items():
                            if isinstance(a, dict) and isinstance(a.get("url"), str):
                                out.append((s, a))
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(c)
    return out


def pick_source(c, catalog):
    """A (source_id, anchor) the crop already cites at a DOCUMENT (not a bare host), in the catalog."""
    for s, a in _anchors(c):
        if s in catalog and len(urlparse(a["url"]).path.strip("/")) > 0:
            return s, {"url": a["url"], "verified": "2026-10-01"}
    raise AssertionError(f"no document-pathed cited source on {c['slug']}")


class Synthetic:
    """A full synthetic stage + evidence cache in a temp dir."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="pla10p1_")
        self.stage = os.path.join(self.root, "stage")
        self.ev_dir = os.path.join(self.root, "evidence")
        os.makedirs(os.path.join(self.stage, "crops"))
        os.makedirs(self.ev_dir)
        self.crops, self.ev, self.manifest = {}, [], []
        cat = BASE["source_catalog"]
        for c in BASE["crops"]:
            if not P.certified(c) or c.get("zone_independent") is True:
                continue
            slug = c["slug"]
            sid, anc = pick_source(c, cat)
            sp = c["spacing_inches"]
            arr = "block" if c.get("pollination_block_min_rows") is not None else "row"
            e = {"id": f"{arr}-none", "arrangement": arr, "support": "none", "default": True,
                 "in_row_inches": list(sp), "row_spacing_inches": None, "row_spacing_reason": "not_authored",
                 "sources": [sid], "anchoring_urls": {sid: anc}}
            s = {"slug": slug, "decision": "synthetic: base spacing carried", "planting_layout": [e]}
            if P.RETIRED in c:
                for rs, ra in c[P.RETIRED].items():
                    if rs not in e["sources"]:
                        e["sources"].append(rs)
                        e["anchoring_urls"][rs] = {"url": ra["url"], "verified": ra["verified"]}
                s["retired_anchor"] = {rs: "moved" for rs in c[P.RETIRED]}
            if slug in P.ROOTSTOCK_CROPS:
                s["rootstock_spacing"] = {r["name"]: None for r in c.get("rootstock_options") or []}
                s["restatements"] = [{"path": p, "verdict": "agrees", "note": "synthetic"}
                                     for p in P.spacing_strings(c)]
            self.crops[slug] = s
            self.add_evidence(slug, e["id"], "in_row_inches", sp, sid, anc["url"],
                              f"Space plants {sp[0]:g} to {sp[1]:g} inches apart in the row.")
        self.write()

    def add_evidence(self, slug, eid, field, value, sid, url, quote, page_text=None):
        text = page_text if page_text is not None else f"<html><p>{slug} page. {quote}</p></html>"
        raw = text.encode("utf-8")
        h = hashlib.sha256(raw).hexdigest()
        with open(os.path.join(self.ev_dir, h + ".html"), "wb") as f:
            f.write(raw)
        self.manifest.append((h, url))
        self.ev.append({"crop": slug, "entry_id": eid, "field": field, "value": P.compact(value),
                        "source_id": sid, "url": url, "sha256": h, "quote": quote})

    def write(self):
        cd = os.path.join(self.stage, "crops")
        for f in os.listdir(cd):
            os.remove(os.path.join(cd, f))
        for slug, s in self.crops.items():
            with open(os.path.join(cd, slug + ".json"), "w", encoding="utf-8") as f:
                json.dump(s, f)
        with open(os.path.join(self.stage, "EVIDENCE.tsv"), "w", encoding="utf-8") as f:
            f.write("\t".join(P.EVIDENCE_COLS) + "\n")
            for r in self.ev:
                f.write("\t".join(r[k] for k in P.EVIDENCE_COLS) + "\n")
        with open(os.path.join(self.ev_dir, "MANIFEST.tsv"), "w", encoding="utf-8") as f:
            f.write("sha256\tbytes\tfetched\tagents\turl\tsaved_by\n")
            for h, u in self.manifest:
                f.write(f"{h}\t0\t2026-10-01\ttest\t{u}\ttest\n")

    def run(self):
        self.write()
        stage, ev = P.load_stage(self.stage)
        return P.run(copy.deepcopy(BASE), stage, ev, self.ev_dir)

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


_CLEAN = None


def clean_post():
    global _CLEAN
    if _CLEAN is None:
        s = Synthetic()
        try:
            _CLEAN = s.run()
        finally:
            s.close()
    return _CLEAN


class Base(unittest.TestCase):
    def setUp(self):
        self.s = Synthetic()

    def tearDown(self):
        self.s.close()

    def refused(self, *needles):
        with self.assertRaises(P.Refused) as cm:
            self.s.write()
            self.s.run()
        msg = str(cm.exception)
        for n in needles:
            self.assertIn(n, msg)
        return msg


class Literals(unittest.TestCase):
    def test_the_pins_are_the_measurement(self):
        self.assertEqual(P.BASE_SHA, "c5fc3d13764f6d08b24574bbb07ecb15f5cfddeb7ba80f7439a72d8829813e28")
        self.assertEqual((P.EXPECTED_CERTIFIED, P.EXPECTED_STAGED), (121, 113))
        self.assertEqual(P.NULL_SPACING_EXPECTED, MICROGREENS)
        self.assertEqual(P.ROOTSTOCK_CROPS, ("apple",))
        self.assertEqual(len(P.RETIRED_ANCHOR_CROPS), 11)


class PositiveControl(unittest.TestCase):
    def test_the_synthetic_stage_promotes_clean(self):
        post, n, r, n_ev = clean_post()
        self.assertEqual(n, 113)
        self.assertEqual((r["certified"], r["entries"], r["list_shaped"], r["legacy"]), (121, 113, 121, 0))
        self.assertEqual(tuple(r["null_spacing"]), MICROGREENS)
        self.assertEqual(n_ev, 113)
        idx = P.by_slug(post)
        for m in MICROGREENS:
            c = idx[m]
            self.assertEqual((c["planting_layout"], c["spacing_inches"], c["row_spacing_inches"],
                              c["row_spacing_reason"]), ([], None, None, "not_applicable"))
        self.assertFalse(any(P.RETIRED in c for c in post["crops"]))
        self.assertEqual(idx["sweet-corn"]["pollination_block_min_rows"], 4)

    def test_the_post_state_serializes_compact(self):
        blob = P.serialize(clean_post()[0])
        self.assertFalse(blob.endswith(b"\n"))
        self.assertNotIn(b'": ', blob[:2000])


class FixedList(Base):
    def test_a_missing_crop_REFUSES(self):
        del self.s.crops["cabbage"]
        self.refused("FIXED LIST", "missing ['cabbage']")

    def test_a_microgreen_staged_REFUSES(self):
        self.s.crops["wheatgrass"] = copy.deepcopy(self.s.crops["cabbage"]); self.s.crops["wheatgrass"]["slug"] = "wheatgrass"
        self.refused("FIXED LIST", "extra ['wheatgrass']")

    def test_null_spacing_beyond_the_microgreens_REFUSES(self):
        post = copy.deepcopy(clean_post()[0])
        P.by_slug(post)["cabbage"]["spacing_inches"] = None
        stage, ev = P.load_stage(self.s.stage)
        with self.assertRaises(P.Refused) as cm:
            P.check_post(BASE, post, stage, ev, self.s.ev_dir)
        self.assertIn("FIXED LIST", str(cm.exception))

    def test_the_base_pin(self):
        tmp = os.path.join(self.s.root, "c.json")
        with open(tmp, "wb") as f:
            f.write(promote_fixture.pre_state(P.BASE_SHA) + b" ")
        with self.assertRaises(P.Refused) as cm:
            P.load_canonical(tmp)
        self.assertIn("pinned to c5fc3d13", str(cm.exception))


class Evidence(Base):
    def row(self, slug):
        return next(r for r in self.s.ev if r["crop"] == slug)

    def test_a_figure_without_evidence_REFUSES(self):
        self.s.ev = [r for r in self.s.ev if r["crop"] != "cabbage"]
        self.refused("cabbage row-none: in_row_inches", "has no EVIDENCE row")

    def test_a_row_figure_needs_its_own_evidence(self):
        self.s.crops["cabbage"]["planting_layout"][0].update(row_spacing_inches=[24, 36], row_spacing_reason=None)
        self.refused("cabbage row-none: row_spacing_inches [24,36] has no EVIDENCE row")

    def test_a_quote_not_in_the_bytes_REFUSES(self):
        self.row("cabbage")["quote"] = "Space plants 99 to 99 inches apart in the row."
        self.refused("the quote is not in the cached bytes")

    def test_tampered_bytes_REFUSE(self):
        r = self.row("cabbage")
        with open(os.path.join(self.s.ev_dir, r["sha256"] + ".html"), "ab") as f:
            f.write(b" ")
        self.refused("hash to")

    def test_a_value_mismatch_REFUSES(self):
        self.row("cabbage")["value"] = "[1,2]"
        self.refused("value [1,2] != the entry's")

    def test_a_quote_that_states_no_endpoint_REFUSES(self):
        r = self.row("cabbage")
        r["quote"] = "Cabbage page. Space plants evenly"
        self.s.ev.remove(r)
        self.s.add_evidence("cabbage", "row-none", "in_row_inches", IDX["cabbage"]["spacing_inches"],
                            r["source_id"], r["url"], "Space plants evenly in the row, never crowded.")
        self.refused("states neither endpoint")

    def test_feet_on_the_page_states_inches(self):
        """A page in feet supports an inch figure: 24 in == '2 feet'. Positive control for the unit rule."""
        c = self.s.crops["cabbage"]["planting_layout"][0]
        c["in_row_inches"] = [24, 24]
        r = self.row("cabbage"); self.s.ev.remove(r)
        self.s.add_evidence("cabbage", "row-none", "in_row_inches", [24, 24], r["source_id"], r["url"],
                            "Set transplants 2 feet apart in the row.")
        self.s.crops["cabbage"]["restatements"] = [{"path": p, "verdict": "agrees", "note": "t"}
                                                   for p in P.spacing_strings(IDX["cabbage"])]
        self.s.write(); self.s.run()

    def test_a_url_not_in_the_manifest_REFUSES(self):
        self.s.manifest = [(h, u) for h, u in self.s.manifest if h != self.row("cabbage")["sha256"]]
        self.refused("is not in", "MANIFEST.tsv")

    def test_the_url_must_be_the_entrys_anchor(self):
        self.row("cabbage")["url"] = "https://example.edu/other"
        self.refused("url is not the entry's anchoring url")

    def test_the_source_must_be_the_entrys(self):
        self.row("cabbage")["source_id"] = "zz_src"
        self.refused("is not in the entry's sources")

    def test_a_source_off_the_catalog_REFUSES(self):
        e = self.s.crops["cabbage"]["planting_layout"][0]
        e["sources"].append("zz_not_catalogued"); e["anchoring_urls"]["zz_not_catalogued"] = {
            "url": "https://example.edu/x", "verified": "2026-10-01"}
        self.refused("'zz_not_catalogued' is not in source_catalog")


class RetiredAnchors(Base):
    def test_moved_but_absent_REFUSES(self):
        e = self.s.crops["potato"]["planting_layout"][0]
        sid = next(iter(IDX["potato"][P.RETIRED]))
        others = [s for s in e["sources"] if s != sid]
        self.assertTrue(others, "potato's synthetic entry must carry a non-retired source")
        e["sources"].remove(sid); del e["anchoring_urls"][sid]
        self.s.ev = [r for r in self.s.ev if not (r["crop"] == "potato" and r["source_id"] == sid)]
        self.refused(f"potato: {sid} marked moved, but no entry anchors")

    def test_dropped_needs_a_reason(self):
        sid = next(iter(IDX["lemon"][P.RETIRED]))
        self.s.crops["lemon"]["retired_anchor"][sid] = {"dropped": " "}
        self.refused("disposition must be 'moved' or")

    def test_every_retired_anchor_is_dispositioned(self):
        self.s.crops["lemon"]["retired_anchor"] = {}
        self.refused("lemon: retired_anchor names []")

    def test_retired_anchor_only_where_the_base_carries_one(self):
        self.s.crops["cabbage"]["retired_anchor"] = {}
        self.refused("cabbage: retired_anchor is required iff")

    def test_dropped_with_a_reason_passes(self):
        """lemon's uf_ifas_hs1153 points at HS402 (spec §2.4): dropping it, with the reason, is legal."""
        sid = next(iter(IDX["lemon"][P.RETIRED]))
        cat = BASE["source_catalog"]
        other, anc = next((s, a) for s, a in _anchors(IDX["lemon"]) if s != sid and s in cat
                          and len(urlparse(a["url"]).path.strip("/")) > 0)
        anc = {"url": anc["url"], "verified": "2026-10-01"}
        e = self.s.crops["lemon"]["planting_layout"][0]
        e["sources"] = [other]; e["anchoring_urls"] = {other: anc}
        self.s.ev = [r for r in self.s.ev if r["crop"] != "lemon"]
        sp = e["in_row_inches"]
        self.s.add_evidence("lemon", e["id"], "in_row_inches", sp, other, anc["url"],
                            f"Space trees {sp[0]:g} to {sp[1]:g} inches apart.")
        self.s.crops["lemon"]["retired_anchor"][sid] = {"dropped": "keyed hs1153, url is HS402 (spec §2.4)"}
        post = self.s.run()[0]
        self.assertNotIn(sid, P.by_slug(post)["lemon"]["planting_layout"][0]["sources"])


class Restatements(Base):
    def move(self, slug="cabbage", new=None):
        sp = IDX[slug]["spacing_inches"]
        new = new or [sp[0], sp[1] + 6]
        self.s.crops[slug]["planting_layout"][0]["in_row_inches"] = new
        r = next(x for x in self.s.ev if x["crop"] == slug); self.s.ev.remove(r)
        self.s.add_evidence(slug, "row-none", "in_row_inches", new, r["source_id"], r["url"],
                            f"Space plants {new[0]:g} to {new[1]:g} inches apart in the row.")
        return P.spacing_strings(IDX[slug])

    def test_the_scanner_finds_cabbage_restatements(self):
        """Positive control: the drivers below are vacuous if cabbage restates no spacing."""
        self.assertGreater(len(P.spacing_strings(IDX["cabbage"])), 0)

    def test_an_unadjudicated_restatement_REFUSES(self):
        hits = self.move()
        self.refused("cabbage: spacing_inches moves", "is not adjudicated", hits[0])

    def test_adjudicated_agrees_passes(self):
        hits = self.move()
        self.s.crops["cabbage"]["restatements"] = [{"path": p, "verdict": "agrees", "note": "t"} for p in hits]
        self.s.write(); self.s.run()

    def test_edited_without_an_edit_REFUSES(self):
        hits = self.move()
        self.s.crops["cabbage"]["restatements"] = [{"path": p, "verdict": "edited", "note": "t"} for p in hits]
        self.refused("adjudicated 'edited' but no edit touches it")

    def test_edited_with_its_edit_passes(self):
        hits = self.move()
        p0 = hits[0]
        self.s.crops["cabbage"]["restatements"] = [{"path": p, "verdict": "edited" if p == p0 else "agrees",
                                                    "note": "t"} for p in hits]
        self.s.crops["cabbage"]["edits"] = [{"path": p0, "new": "Re-authored sentence.", "reason": "t"}]
        post = self.s.run()[0]
        node = P.by_slug(post)["cabbage"]
        for seg in P.resolve(IDX["cabbage"], p0):
            node = node[seg]
        self.assertEqual(node, "Re-authored sentence.")

    def test_a_restatement_needs_a_note(self):
        hits = self.move()
        self.s.crops["cabbage"]["restatements"] = [{"path": p, "verdict": "agrees", "note": ""} for p in hits]
        self.refused("needs path, verdict agrees|edited, and a note")


class BlastRadius(Base):
    def check(self, mutate):
        post = copy.deepcopy(clean_post()[0])
        mutate(post)
        stage, ev = P.load_stage(self.s.stage)
        with self.assertRaises(P.Refused) as cm:
            P.check_post(BASE, post, stage, ev, self.s.ev_dir)
        return str(cm.exception)

    def test_a_stray_crop_field_REFUSES(self):
        self.assertIn("cabbage: changed outside what the stage names: ['water']",
                      self.check(lambda p: P.by_slug(p)["cabbage"].update(water="x")))

    def test_an_added_crop_key_REFUSES(self):
        self.assertIn("changed outside", self.check(lambda p: P.by_slug(p)["cabbage"].update(zz=1)))

    def test_a_removed_crop_key_REFUSES(self):
        self.assertIn("changed outside", self.check(lambda p: P.by_slug(p)["cabbage"].pop("water")))

    def test_a_shell_change_REFUSES(self):
        self.assertIn("shell olive changed", self.check(lambda p: P.by_slug(p)["olive"].update(zz=1)))

    def test_a_top_level_change_REFUSES(self):
        self.assertIn("top-level 'source_catalog' changed",
                      self.check(lambda p: p["source_catalog"].update(zz={})))

    def test_a_top_level_key_added_REFUSES(self):
        self.assertIn("top-level keys changed", self.check(lambda p: p.update(zz=1)))

    def test_a_roster_reorder_REFUSES(self):
        self.assertIn("the roster changed", self.check(lambda p: p["crops"].reverse()))

    def test_a_layout_not_the_stage_verbatim_REFUSES(self):
        self.assertIn("planting_layout is not the stage's", self.check(
            lambda p: P.by_slug(p)["cabbage"]["planting_layout"][0].update(row_spacing_reason="not_authored ")))


class Edits(Base):
    def test_an_edit_to_a_record_REFUSES(self):
        self.s.crops["cabbage"]["edits"] = [{"path": "verification_status.status", "new": "x", "reason": "t"}]
        self.refused("touches a key the promote owns or a record")

    def test_an_edit_needs_a_reason(self):
        self.s.crops["cabbage"]["edits"] = [{"path": "water", "new": "x", "reason": ""}]
        self.refused("an edit needs exactly path, new and a reason")

    def test_an_edit_to_nothing_REFUSES(self):
        self.s.crops["cabbage"]["edits"] = [{"path": "growth_stages[id=zz].note", "new": "x", "reason": "t"}]
        self.refused("matches 0 items")

    def test_an_edit_lands_and_nothing_else(self):
        """thin_to_inches is the fava case (spec §10.1): a numeric restatement edited by path."""
        self.s.crops["cabbage"]["edits"] = [{"path": "water", "new": "Moderate", "reason": "t"}]
        post = self.s.run()[0]
        self.assertEqual(P.by_slug(post)["cabbage"]["water"], "Moderate")

    def test_a_tampered_edit_value_REFUSES(self):
        self.s.crops["cabbage"]["edits"] = [{"path": "water", "new": "Moderate", "reason": "t"}]
        self.s.write()
        stage, ev = P.load_stage(self.s.stage)
        post = P.apply_to(copy.deepcopy(BASE), stage)
        P.by_slug(post)["cabbage"]["water"] = "High!"
        with self.assertRaises(P.Refused) as cm:
            P.check_post(BASE, post, stage, ev, self.s.ev_dir)
        self.assertIn("water is not the edit's new value", str(cm.exception))


class Rootstock(Base):
    def test_rootstock_spacing_off_apple_REFUSES(self):
        self.s.crops["pear-european"]["rootstock_spacing"] = {}
        self.refused("rootstock_spacing is apple's alone")

    def test_every_apple_row_is_present_or_null(self):
        rs = self.s.crops["apple"]["rootstock_spacing"]
        rs.pop(next(iter(rs)))
        self.refused("apple: rootstock_spacing names")

    def test_apple_rows_land_as_staged(self):
        rs = self.s.crops["apple"]["rootstock_spacing"]
        first = next(iter(rs)); rs[first] = [72, 96]
        post = self.s.run()[0]
        row = next(r for r in P.by_slug(post)["apple"]["rootstock_options"] if r["name"] == first)
        self.assertEqual(row["spacing_inches"], [72, 96])

    def test_a_rootstock_override_off_apple_in_the_post_REFUSES(self):
        post = copy.deepcopy(clean_post()[0])
        pear = P.by_slug(post)["pear-european"]
        pear["rootstock_options"][0]["spacing_inches"] = [1, 2]
        stage, ev = P.load_stage(self.s.stage)
        with self.assertRaises(P.Refused) as cm:
            P.check_post(BASE, post, stage, ev, self.s.ev_dir)
        self.assertIn("pear-european: changed outside what the stage names: ['rootstock_options[0].spacing_inches']",
                      str(cm.exception))


class GatesOnThePost(Base):
    def test_an_entry_that_fails_A44_REFUSES(self):
        self.s.crops["cabbage"]["planting_layout"][0]["support"] = "vertical"
        self.refused("planting_layout_gate (armed)")

    def test_an_uncited_entry_REFUSES(self):
        e = self.s.crops["cabbage"]["planting_layout"][0]
        e["sources"] = []; e["anchoring_urls"] = {}
        self.s.ev = [r for r in self.s.ev if r["crop"] != "cabbage"]
        self.refused("cabbage")

    def test_a_numeric_bound_REFUSES(self):
        e = self.s.crops["cabbage"]["planting_layout"][0]
        e.update(row_spacing_inches=[2, 3], row_spacing_reason=None)
        self.s.add_evidence("cabbage", "row-none", "row_spacing_inches", [2, 3], e["sources"][0],
                            e["anchoring_urls"][e["sources"][0]]["url"], "Rows 2 to 3 inches apart.")
        self.refused("numeric_sanity")


class R5Migration(Base):
    def waive(self, slug, in_row):
        saved = dict(MIG.WAIVERS)
        MIG.WAIVERS.clear(); MIG.WAIVERS[slug] = {"entry_id": "row-none", "in_row_inches": in_row, "hunt": "t"}
        self.addCleanup(lambda: (MIG.WAIVERS.clear(), MIG.WAIVERS.update(saved)))

    def uncite(self, slug):
        e = self.s.crops[slug]["planting_layout"][0]
        e["sources"] = []; e["anchoring_urls"] = {}
        self.s.ev = [r for r in self.s.ev if r["crop"] != slug]

    def test_a_waived_entry_ships_uncited_without_evidence(self):
        self.waive("bok-choy", list(IDX["bok-choy"]["spacing_inches"]))
        self.uncite("bok-choy")
        self.s.write(); self.s.run()

    def test_a_waiver_off_the_base_value_REFUSES(self):
        sp = IDX["bok-choy"]["spacing_inches"]
        self.waive("bok-choy", [sp[0], sp[1] + 1])
        self.uncite("bok-choy")
        self.refused("bok-choy: migration waiver in_row")

    def test_a_waiver_off_the_R5_list_REFUSES(self):
        self.waive("cabbage", list(IDX["cabbage"]["spacing_inches"]))
        self.uncite("cabbage")
        self.refused("cabbage: a migration waiver off the R5 list")


class CLI(unittest.TestCase):
    def test_out_may_not_target_the_canonical(self):
        self.assertEqual(P.main(["--out", P.CANON, "--check"]), 1)

    def test_no_stage_yet_REFUSES_on_the_fixed_list(self):
        """The real stage is authored in sessions 2-3; until then the promote must refuse, not pass."""
        empty = tempfile.mkdtemp(prefix="pla10p1_empty_")
        try:
            os.makedirs(os.path.join(empty, "crops"))
            tmp = os.path.join(empty, "c.json")
            with open(tmp, "wb") as f:
                f.write(promote_fixture.pre_state(P.BASE_SHA))
            self.assertEqual(P.main(["--check", "--canonical", tmp, "--stage", empty]), 1)
        finally:
            shutil.rmtree(empty, ignore_errors=True)


if __name__ == "__main__":
    import io
    stream = io.StringIO()
    res = unittest.TextTestRunner(stream=stream, verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    print(stream.getvalue()[-3000:])
    if not res.wasSuccessful():
        raise SystemExit(1)
    print(f"PASS test_promote_pla10_planting_layout ({res.testsRun} tests)")
