#!/usr/bin/env python3
"""Tests for bare_host_gate -- PLA-544: a SOLE citation anchored at a bare host fails, on every
certified crop, whether or not the crop paths that source elsewhere.

TDD: written and run RED before the module existed (ModuleNotFoundError, 2026-09-30).

MEASURED 2026-09-30 on canonical 00dda31c: 30102 anchors inspected on 121 certified crops;
1242 bare-host citations = 381 SOLE (on 41 crops) + 861 co-cited. The 381 are waived by identity.

THE BLIND SPOT THIS CLOSES, named in the ticket and re-confirmed here: grapefruit and orange-navel
carry the SAME bare, sole-cited Flying Dragon row (`rootstock_options[2]`, `ucr_citrus` at
https://citrusvariety.ucr.edu). bare_host_scan.self_pathed sees grapefruit's (it paths ucr_citrus
elsewhere) and NOT orange-navel's (it never does). This gate sees both.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bare_host_gate as G  # noqa: E402
import bare_host_scan as B  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
SHA = "00dda31cc6616b9ea865f04fe0ce97fb1fb5d821f0c94724d3a03dbad8c8dd8e"
VICTIM = "cabbage"
UCR = "https://citrusvariety.ucr.edu"
FLYING_DRAGON = {"grapefruit|rootstock_options[2]|anchoring_urls|ucr_citrus",
                 "orange-navel|rootstock_options[2]|anchoring_urls|ucr_citrus"}
LEMON_TAMU = {"lemon|rootstock_options[0]|anchoring_urls|tamu_agrilife",
              "lemon|rootstock_options[1]|anchoring_urls|tamu_agrilife"}


def canon():
    with open(CANON, encoding="utf-8") as f:
        return json.load(f)


_CANON = canon()


def fresh():
    return copy.deepcopy(_CANON)


def by(data):
    return {c["slug"]: c for c in data["crops"]}


def violations(data):
    return G.roster(data)[4]


def first_single_cited_node(crop):
    """A node on `crop` citing exactly one source with a pathed anchor -> (node, sid)."""
    for k in ("storage", "watering", "soil", "ph", "fertilizer"):
        node = crop.get(k)
        if isinstance(node, dict) and len(node.get("anchoring_urls") or {}) >= 1:
            return node, sorted(node["anchoring_urls"])[0]
    raise AssertionError("no cited dict block to inject into")


class PinsAreTheMeasurement(unittest.TestCase):
    def test_waiver_file_is_the_measured_population(self):
        self.assertEqual(G._KNOWN_DOC["measured_on"], SHA)
        self.assertEqual((G._KNOWN_DOC["count"], len(G.KNOWN)), (381, 381))
        self.assertEqual(len(G._KNOWN_DOC["identities"]), 381, "duplicate identities")

    def test_floor(self):
        self.assertEqual(G.MIN_INSPECTED, 28000)

    def test_the_bare_predicate_is_IMPORTED_from_the_scan(self):
        self.assertIs(G.BARE, B.BARE)


class LiveCanonical(unittest.TestCase):
    def test_population_and_verdict(self):
        """Measured 30102 anchors / 381 SOLE on 41 crops / 861 co-cited on 00dda31c. NOT pinned to
        the anchor or co-cited count: both move legitimately with any cited promote, and a pin that
        reddens on every promote is the PLA-544 class. Pinned: live SOLE == the waiver set."""
        n, insp, sole, co, V, stale = G.roster(_CANON)
        self.assertGreaterEqual(insp, G.MIN_INSPECTED)
        self.assertEqual((V, stale), ([], []))
        self.assertEqual(set(sole), set(G.KNOWN))
        self.assertIsNone(G.refusal(n, insp))
        self.assertLessEqual(len({i.split("|")[0] for i in G.KNOWN}), 41)

    def test_the_named_examples(self):
        """Confirm the three cases the brief names, from the data, both severities."""
        n, insp, sole, co, V, stale = G.roster(_CANON)
        self.assertTrue(FLYING_DRAGON <= set(sole), "Flying Dragon rows must be SOLE")
        self.assertTrue(LEMON_TAMU <= set(co), "lemon TAMU rows must be CO-CITED, non-blocking")
        idx = by(_CANON)
        for slug in ("grapefruit", "orange-navel"):
            row = idx[slug]["rootstock_options"][2]
            self.assertIn("Flying Dragon", row["name"])
            self.assertEqual(row["sources"], ["ucr_citrus"])
            self.assertEqual(row["anchoring_urls"]["ucr_citrus"]["url"], UCR)

    def test_the_self_pathed_blind_spot_is_real_and_closed(self):
        sp = {(r["crop"], r["path"], r["source_id"]) for r in B.self_pathed(_CANON)}
        self.assertIn(("grapefruit", "rootstock_options[2]", "ucr_citrus"), sp)
        self.assertNotIn(("orange-navel", "rootstock_options[2]", "ucr_citrus"), sp,
                         "the blind spot the ticket names")
        self.assertIn("orange-navel|rootstock_options[2]|anchoring_urls|ucr_citrus", G.KNOWN)

    def test_agrees_row_for_row_with_bare_host_scan_on_anchoring_urls(self):
        """An independent walk: the scan's rows on certified crops == this gate's."""
        cert = {c["slug"] for c in _CANON["crops"] if G.certified(c)}
        scan = {f"{r[1]}|{r[2]}|anchoring_urls|{r[0]}": r[3]
                for r in B.scan(_CANON) if r[1] in cert}
        n, insp, sole, co, *_ = G.roster(_CANON)
        mine = {**{i: True for i in sole}, **{i: False for i in co}}
        self.assertEqual(mine, scan)

    def test_a_clean_crop_passes(self):
        self.assertEqual(G.crop_violations(by(_CANON)[VICTIM]), [])


class TheDefectBounces(unittest.TestCase):
    def test_a_new_SOLE_bare_anchor_FAILS_by_name(self):
        d = fresh()
        node, sid = first_single_cited_node(by(d)[VICTIM])
        for s in list(node["anchoring_urls"]):
            node["anchoring_urls"][s]["url"] = "https://extension.example.edu/"
        v = violations(d)
        self.assertTrue(v)
        self.assertTrue(all(f"{VICTIM}|" in m for m in v), v)
        self.assertTrue(any(f"|anchoring_urls|{sid}" in m for m in v), v)

    def test_uniformly_bare_crop_is_caught_without_any_pathed_sibling(self):
        """orange-navel's shape on a new row: the crop paths the id NOWHERE and it still fails."""
        d = fresh()
        c = by(d)[VICTIM]
        c["rootstock_options"] = [{"name": "zz", "sources": ["zz_src"],
                                   "anchoring_urls": {"zz_src": {"url": "https://zz.edu",
                                                                 "verified": "2026-09-30"}}}]
        self.assertTrue(any(f"{VICTIM}|rootstock_options[0]|anchoring_urls|zz_src" in m
                            for m in violations(d)))

    def test_a_CO_CITED_bare_anchor_is_reported_not_blocking(self):
        d = fresh()
        node, sid = first_single_cited_node(by(d)[VICTIM])
        node["sources"] = list(node.get("sources") or []) + ["zz_bare"]
        node["anchoring_urls"]["zz_bare"] = {"url": "https://zz.edu/", "verified": "2026-09-30"}
        n, insp, sole, co, V, stale = G.roster(d)
        self.assertEqual(V, [])
        self.assertEqual(len(co), len(G.roster(_CANON)[3]) + 1)
        self.assertTrue(any(i.endswith("|anchoring_urls|zz_bare") for i in co), co[:5])

    def test_an_UNANCHORED_sources_id_still_co_cites(self):
        """The node's `sources` belongs to its cited set, as in bare_host_scan: a bare anchor
        beside a source id that has no anchor is CO-CITED (section F flags the missing anchor).
        Harness survivor 2026-09-30: no canonical node has this shape, so only an injection can
        see the predicate at all."""
        d = fresh()
        node, sid = first_single_cited_node(by(d)[VICTIM])
        for s in list(node["anchoring_urls"]):
            node["anchoring_urls"][s]["url"] = "https://zz.edu"
        node["sources"] = list(node["anchoring_urls"]) + ["zz_unanchored"]
        n, insp, sole, co, V, stale = G.roster(d)
        self.assertEqual(V, [])
        self.assertTrue(any(i.startswith(f"{VICTIM}|") for i in co))

    def test_a_crop_root_sibling_anchor_is_walked(self):
        """bare_host_scan.scan() never walks `<field>_anchoring_urls`; this gate must."""
        d = fresh()
        c = by(d)[VICTIM]
        c["harvest_ready_sources"] = ["zz_src"]
        c["harvest_ready_anchoring_urls"] = {"zz_src": {"url": "https://zz.edu",
                                                        "verified": "2026-09-30"}}
        self.assertTrue(any(f"{VICTIM}|<crop>|harvest_ready_anchoring_urls|zz_src" in m
                            for m in violations(d)))

    def test_a_bare_anchor_in_a_region_cell_is_walked(self):
        d = fresh()
        c = by(d)[VICTIM]
        c["regions"]["zz_region"] = {"cell": {"sources": ["zz_src"], "anchoring_urls": {
            "zz_src": {"url": "http://zz.edu", "verified": "2026-09-30"}}}}
        self.assertTrue(any("regions.zz_region.cell|anchoring_urls|zz_src" in m
                            for m in violations(d)))

    def test_site_root_page_spellings_are_bare(self):
        for u in ("https://zz.edu", "https://zz.edu/", "http://zz.edu/index.html",
                  "https://zz.edu/index.php", "https://zz.edu/#top", "https://ZZ.edu/INDEX.HTM"):
            self.assertTrue(G.is_bare(u), u)

    def test_a_real_document_is_not_bare(self):
        """The predicate both ways: a path, or a query naming a page, is a document."""
        for u in ("https://zz.edu/pubs/x", "https://zz.edu/?p=123", "https://zz.edu/a/index.html",
                  "https://edis.ifas.ufl.edu/publication/HS132", None, "", "TODO"):
            self.assertFalse(G.is_bare(u), u)

    def test_an_uncertified_shell_is_exempt(self):
        d = fresh()
        av = by(d)["avocado"]
        av["storage"] = {"x": 1, "sources": ["zz"], "anchoring_urls": {"zz": {"url": "https://zz.edu"}}}
        self.assertEqual(G.crop_violations(av), [])
        self.assertEqual(violations(d), [])


class TheRatchet(unittest.TestCase):
    def test_repointing_a_waived_row_PASSES_and_reports_stale(self):
        d = fresh()
        row = by(d)["orange-navel"]["rootstock_options"][2]
        row["anchoring_urls"]["ucr_citrus"]["url"] = "https://citrusvariety.ucr.edu/citrus/flyingdragon.html"
        n, insp, sole, co, V, stale = G.roster(d)
        self.assertEqual(V, [])
        self.assertEqual(stale, ["orange-navel|rootstock_options[2]|anchoring_urls|ucr_citrus"])

    def test_substitution_FAILS(self):
        d = fresh()
        by(d)["orange-navel"]["rootstock_options"][2]["anchoring_urls"]["ucr_citrus"]["url"] = \
            "https://citrusvariety.ucr.edu/citrus/flyingdragon.html"
        node, sid = first_single_cited_node(by(d)[VICTIM])
        for s in list(node["anchoring_urls"]):
            node["anchoring_urls"][s]["url"] = "https://zz.edu"
        n, insp, sole, co, V, stale = G.roster(d)
        self.assertGreaterEqual(len(sole), 381)
        self.assertTrue(any(f"{VICTIM}|" in m for m in V), V)

    def test_co_citing_a_waived_sole_row_demotes_it(self):
        d = fresh()
        row = by(d)["orange-navel"]["rootstock_options"][2]
        row["sources"].append("uf_ifas_hs132")
        row["anchoring_urls"]["uf_ifas_hs132"] = {"url": "https://edis.ifas.ufl.edu/publication/HS132",
                                                  "verified": "2026-09-30"}
        n, insp, sole, co, V, stale = G.roster(d)
        self.assertEqual(V, [])
        self.assertIn("orange-navel|rootstock_options[2]|anchoring_urls|ucr_citrus", co)


class RefusesAnEmptyPopulation(unittest.TestCase):
    def test_zero_certified_REFUSES(self):
        d = fresh()
        for c in d["crops"]:
            (c.get("verification_status") or {})["status"] = "draft"
        n, insp, *_ = G.roster(d)
        self.assertEqual((n, insp), (0, 0))
        self.assertIn("0 certified", G.refusal(n, insp))

    def test_below_floor_REFUSES(self):
        self.assertIn("below the declared floor", G.refusal(121, G.MIN_INSPECTED - 1))
        self.assertIsNone(G.refusal(121, G.MIN_INSPECTED))


class CLI(unittest.TestCase):
    def _run(self, path):
        r = subprocess.run([sys.executable, os.path.join(HERE, "bare_host_gate.py"), path],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def _tmp(self, data):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
        f.close()
        return f.name

    def test_canonical_rc0_reports_population(self):
        rc, out = self._run(CANON)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"inspected \d+ anchors on \d+ certified crops; \d+ SOLE bare")
        self.assertRegex(out, r"\d+ co-cited bare \(reported, non-blocking\)")

    def test_injection_rc1(self):
        d = fresh()
        node, sid = first_single_cited_node(by(d)[VICTIM])
        for s in list(node["anchoring_urls"]):
            node["anchoring_urls"][s]["url"] = "https://zz.edu"
        p = self._tmp(d)
        try:
            rc, out = self._run(p)
        finally:
            os.remove(p)
        self.assertEqual(rc, 1, out)
        self.assertIn(f"{VICTIM}|", out)

    def test_empty_population_rc2(self):
        d = fresh()
        for c in d["crops"]:
            (c.get("verification_status") or {})["status"] = "draft"
        p = self._tmp(d)
        try:
            rc, out = self._run(p)
        finally:
            os.remove(p)
        self.assertEqual(rc, 2, out)


if __name__ == "__main__":
    unittest.main()
