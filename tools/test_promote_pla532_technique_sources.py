#!/usr/bin/env python3
"""Guard suite for promote_pla532_technique_sources -- PLA-532, technique sources admitted to the catalog.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (`promote_fixture.pre_state`), never live canonical,
and the post-state is REPLAYED from it (its sha is pinned), so this suite is immune to later promotes.
SHIPS MUTATION-TESTED (PLA-215) via `mutate_pla532_technique_sources_suite.py`.

The evidence guard is driven HERMETICALLY (a temp evidence dir, a synthetic manifest, an injected
text reader), so its logic is proven without the gitignored caches. One test reads the real caches;
when they are absent it fails as CACHE COVERAGE, NOT A DATA DEFECT (the PLA-544 convention).
"""
import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import promote_fixture  # noqa: E402
import promote_pla532_technique_sources as P  # noqa: E402

BASE_SHA = "00dda31cc6616b9ea865f04fe0ce97fb1fb5d821f0c94724d3a03dbad8c8dd8e"
OUTPUT_SHA = "c5fc3d13764f6d08b24574bbb07ecb15f5cfddeb7ba80f7439a72d8829813e28"
ROSTER = 128
PRE_CATALOG = 221
POST_CATALOG = 229
# Named as literals, never derived from the content module.
IDS = {"umd_ext_containers_salad_tables", "vce_426_336", "psu_ext_container_vegetables",
       "uvm_ext_small_spaces_budget", "umaine_ext_2762", "umn_ext_trellises_cages", "vce_hort_189",
       "ncsu_ext_handbook_vegetable"}
CLASS_OF = {"umd_ext_containers_salad_tables": {"D"}, "vce_426_336": {"D"},
            "psu_ext_container_vegetables": {"D"}, "uvm_ext_small_spaces_budget": {"D"},
            "umaine_ext_2762": {"D"}, "umn_ext_trellises_cages": {"A", "B"}, "vce_hort_189": {"B"},
            "ncsu_ext_handbook_vegetable": {"B", "C"}}


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blob = promote_fixture.pre_state(P.BASE_SHA)
        if isinstance(cls.blob, str):
            cls.blob = cls.blob.encode("utf-8")
        cls.data = json.loads(cls.blob)
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def post(self, data=None, spec=None):
        return P.apply_to(data or self.data, spec or self.spec)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(self.blob), BASE_SHA)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)
        self.assertEqual(len(self.data["source_catalog"]), PRE_CATALOG)

    def test_the_spec_admits_exactly_the_named_ids(self):
        self.assertEqual(set(self.spec["catalog_new"]), IDS)
        self.assertEqual(P.EXPECTED_NEW_SOURCES, len(IDS))
        self.assertEqual({k: set(v) for k, v in self.spec["claim_class"].items()}, CLASS_OF)

    def test_every_queued_claim_class_is_served(self):
        served = set().union(*CLASS_OF.values())
        self.assertEqual(served, {"A", "B", "C", "D"})


class Entry(Base):
    """Guard 0: the canonical must be the base."""

    def test_check_base_accepts_the_base(self):
        self.assertEqual(P.check_base(self.blob), BASE_SHA)

    def test_main_refuses_a_moved_base(self):
        d = self.fresh_data()
        d["version"] = str(d.get("version")) + "x"
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "c.json")
            with open(p, "wb") as f:
                f.write(P.serialize(d))
            self.assertRefuses("is not the base", P.main, ["--canonical", p])


class SpecShape(Base):
    """Guard 1."""

    def test_spec_shape_passes(self):
        self.assertEqual(P.check_spec_shape(self.spec), len(IDS))

    def test_refuses_a_ninth_id(self):
        s = self.fresh_spec()
        e = copy.deepcopy(s["catalog_new"]["vce_hort_189"])
        e["id"] = "zz_extra"
        s["catalog_new"]["zz_extra"] = e
        self.assertRefuses("expected 8", P.check_spec_shape, s)

    def test_refuses_tables_that_disagree(self):
        s = self.fresh_spec()
        s["quotes"]["zz_other"] = s["quotes"].pop("vce_hort_189")
        self.assertRefuses("quotes names", P.check_spec_shape, s)

    def test_refuses_an_extra_key(self):
        s = self.fresh_spec()
        s["catalog_new"]["vce_426_336"]["note"] = "x"
        self.assertRefuses("key set differs", P.check_spec_shape, s)

    def test_refuses_an_id_that_is_not_its_key(self):
        s = self.fresh_spec()
        s["catalog_new"]["vce_426_336"]["id"] = "vce_426_331"
        self.assertRefuses("carries id", P.check_spec_shape, s)

    def test_refuses_an_unknown_claim_class(self):
        s = self.fresh_spec()
        s["claim_class"]["vce_hort_189"] = ("E",)
        self.assertRefuses("outside A/B/C/D", P.check_spec_shape, s)

    def test_refuses_an_empty_claim_class(self):
        s = self.fresh_spec()
        s["claim_class"]["vce_hort_189"] = ()
        self.assertRefuses("outside A/B/C/D", P.check_spec_shape, s)

    def test_refuses_an_entry_with_no_quote(self):
        s = self.fresh_spec()
        s["quotes"]["vce_hort_189"] = []
        self.assertRefuses("pins no verbatim quote", P.check_spec_shape, s)


class Entries(Base):
    """Guard 2."""

    def test_entries_pass(self):
        self.assertEqual(P.check_entries(self.spec), len(IDS))

    def test_every_url_is_pathed(self):
        for sid, e in self.spec["catalog_new"].items():
            self.assertFalse(P.is_bare(e["url"]), sid)

    def test_refuses_a_bare_host(self):
        s = self.fresh_spec()
        s["catalog_new"]["umn_ext_trellises_cages"]["url"] = "https://extension.umn.edu/"
        s["evidence"]["umn_ext_trellises_cages"]["url"] = "https://extension.umn.edu/"
        self.assertRefuses("bare host or site root", P.check_entries, s)

    def test_refuses_a_site_root_page(self):
        s = self.fresh_spec()
        s["catalog_new"]["umn_ext_trellises_cages"]["url"] = "https://extension.umn.edu/index.html"
        s["evidence"]["umn_ext_trellises_cages"]["url"] = "https://extension.umn.edu/index.html"
        self.assertRefuses("bare host or site root", P.check_entries, s)

    def test_refuses_plain_http(self):
        s = self.fresh_spec()
        u = s["catalog_new"]["vce_426_336"]["url"].replace("https://", "http://")
        s["catalog_new"]["vce_426_336"]["url"] = u
        self.assertRefuses("not https", P.check_entries, s)

    def test_refuses_a_url_other_than_the_fetched_one(self):
        s = self.fresh_spec()
        s["catalog_new"]["umn_ext_trellises_cages"]["url"] = "https://extension.umn.edu/planting-and-growing-guides/trellises-and-cages"
        self.assertRefuses("not the url its evidence was fetched from", P.check_entries, s)

    def test_refuses_a_t2(self):
        s = self.fresh_spec()
        s["catalog_new"]["vce_426_336"]["tier"] = "T2"
        self.assertRefuses("not a T1", P.check_entries, s)

    def test_refuses_a_wrong_admission_date(self):
        s = self.fresh_spec()
        s["catalog_new"]["vce_426_336"]["accessed"] = "2026-04"
        self.assertRefuses("not the admission date", P.check_entries, s)

    def test_refuses_a_blank_title(self):
        s = self.fresh_spec()
        s["catalog_new"]["uvm_ext_small_spaces_budget"]["title"] = "  "
        self.assertRefuses("no title", P.check_entries, s)

    def test_refuses_a_blank_citable_for(self):
        s = self.fresh_spec()
        s["catalog_new"]["uvm_ext_small_spaces_budget"]["citable_for"] = ""
        self.assertRefuses("no citable_for", P.check_entries, s)

    def test_the_uvm_title_is_the_documents_not_the_file_name(self):
        # Read off the rendered first page, 2026-09-30. The scouting name was the file name.
        self.assertEqual(self.spec["catalog_new"]["uvm_ext_small_spaces_budget"]["title"],
                         "Gardening in Small Spaces on a Budget")

    def test_the_umd_caption_is_not_offered_as_a_minimum(self):
        cf = self.spec["catalog_new"]["umd_ext_containers_salad_tables"]["citable_for"]
        self.assertIn("is ONE photo caption", cf)
        self.assertIn("The 25-gallon figure is not a minimum and must not be cited as one", cf)
        self.assertIn("not as body guidance", cf)


class PreState(Base):
    """Guard 3."""

    def test_pre_state_passes(self):
        self.assertEqual(P.check_pre_state(self.spec, self.data), PRE_CATALOG)

    def test_refuses_an_id_that_already_exists(self):
        d = self.fresh_data()
        d["source_catalog"]["vce_hort_189"] = {"id": "vce_hort_189", "url": "https://example.edu/x"}
        del d["source_catalog"]["vce_426_331"]  # keep the count pinned so only the overwrite guard fires
        self.assertRefuses("already exists", P.check_pre_state, self.spec, d)

    def test_refuses_a_url_already_catalogued(self):
        d = self.fresh_data()
        d["source_catalog"]["vce_426_331"]["url"] = self.spec["catalog_new"]["vce_426_336"]["url"]
        self.assertRefuses("already catalogued as 'vce_426_331'", P.check_pre_state, self.spec, d)

    def test_refuses_a_moved_catalog_count(self):
        d = self.fresh_data()
        d["source_catalog"]["zz_new"] = {"id": "zz_new", "url": "https://example.edu/y"}
        self.assertRefuses("re-measure before running", P.check_pre_state, self.spec, d)


class Evidence(Base):
    """Guard 4, driven hermetically."""

    def rig(self, spec):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        rows = ["sha256\tbytes\tfetched\tagents\turl\tsaved_by"]
        texts = {}
        for sid, ev in spec["evidence"].items():
            body = (" ".join(spec["quotes"][sid]) + " " + sid).encode("utf-8")
            ev["sha256"] = hashlib.sha256(body).hexdigest()
            with open(os.path.join(t.name, f"{ev['sha256']}.{ev['ext']}"), "wb") as f:
                f.write(body)
            rows.append("\t".join([ev["sha256"], str(len(body)), "d", "a", ev["url"], "s"]))
            texts[ev["url"]] = body.decode("utf-8")
        man = os.path.join(t.name, "MANIFEST.tsv")
        with open(man, "w", encoding="utf-8") as f:
            f.write("\n".join(rows) + "\n")
        return t.name, man, texts

    def test_rigged_evidence_passes(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        n = P.check_evidence(s, d, man, texts.get)
        self.assertEqual(n, sum(len(q) for q in s["quotes"].values()))

    def test_refuses_absent_raw_bytes(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        os.remove(os.path.join(d, f"{s['evidence']['vce_hort_189']['sha256']}.html"))
        self.assertRefuses("raw bytes absent", P.check_evidence, s, d, man, texts.get)

    def test_refuses_bytes_that_do_not_hash(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        with open(os.path.join(d, f"{s['evidence']['vce_hort_189']['sha256']}.html"), "ab") as f:
            f.write(b" drift")
        self.assertRefuses("cached bytes hash", P.check_evidence, s, d, man, texts.get)

    def test_refuses_a_missing_manifest_row(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        with open(man, encoding="utf-8") as f:
            lines = [ln for ln in f.read().splitlines() if s["evidence"]["vce_hort_189"]["url"] not in ln]
        with open(man, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        self.assertRefuses("no MANIFEST.tsv row", P.check_evidence, s, d, man, texts.get)

    def test_refuses_absent_cached_text(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        del texts[s["evidence"]["vce_hort_189"]["url"]]
        self.assertRefuses("no cached text", P.check_evidence, s, d, man, texts.get)

    def test_refuses_a_quote_not_on_the_page(self):
        s = self.fresh_spec()
        d, man, texts = self.rig(s)
        s["quotes"]["vce_hort_189"] = s["quotes"]["vce_hort_189"] + ["Melons need a 40-inch cage."]
        self.assertRefuses("quote not on the page", P.check_evidence, s, d, man, texts.get)

    def test_the_real_evidence_is_present_and_every_quote_is_on_its_page(self):
        missing = [sid for sid, ev in self.spec["evidence"].items()
                   if not os.path.exists(os.path.join(P.EVIDENCE_DIR, f"{ev['sha256']}.{ev['ext']}"))
                   or P.cached_text(ev["url"]) is None]
        if missing:
            raise AssertionError(f"CACHE COVERAGE, NOT A DATA DEFECT: {len(missing)} of {len(IDS)} PLA-532 "
                                 f"documents absent from the local tools/.evidence_cache or tools/.doc_cache: {missing}")
        self.assertEqual(P.check_evidence(self.spec), sum(len(q) for q in self.spec["quotes"].values()))


class PostState(Base):
    """Guard 5."""

    def test_the_replayed_post_is_the_pinned_output(self):
        self.assertEqual(P.sha256_bytes(P.serialize(self.post())), OUTPUT_SHA)

    def test_verify_post_passes(self):
        post = self.post()
        self.assertEqual(P.verify_post(self.data, post, self.spec), len(IDS))
        self.assertEqual(len(post["source_catalog"]), POST_CATALOG)

    def test_the_post_is_compact(self):
        b = P.serialize(self.post())
        self.assertFalse(b.endswith(b"\n"))
        self.assertNotIn(b'": ', b[:5000])

    def test_refuses_a_dropped_entry(self):
        post = self.post()
        del post["source_catalog"]["vce_426_331"]
        self.assertRefuses("DROPPED", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_undeclared_addition(self):
        post = self.post()
        post["source_catalog"]["zz_ghost"] = copy.deepcopy(post["source_catalog"]["vce_hort_189"])
        self.assertRefuses("gained", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_declared_id_that_did_not_land(self):
        post = self.post()
        del post["source_catalog"]["vce_hort_189"]
        self.assertRefuses("gained", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_edited_existing_entry(self):
        post = self.post()
        post["source_catalog"]["umn_ext"]["citable_for"] += " Container technique."
        self.assertRefuses("existing catalog entry 'umn_ext' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_changed_crop(self):
        post = self.post()
        post["crops"][0]["name"] = post["crops"][0]["name"] + " "
        self.assertRefuses("top-level key 'crops' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_changed_other_top_level_key(self):
        post = self.post()
        post["container_safety"] = copy.deepcopy(post["container_safety"])
        if isinstance(post["container_safety"], dict):
            post["container_safety"]["_x"] = 1
        else:
            post["container_safety"].append(1)
        self.assertRefuses("top-level key 'container_safety' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_new_top_level_key(self):
        post = self.post()
        post["zz_new_key"] = 1
        self.assertRefuses("top-level keys changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_a54_violation(self):
        post = self.post()
        post["source_catalog"]["vce_hort_189"]["title"] = ""
        s = self.fresh_spec()
        s["catalog_new"]["vce_hort_189"]["title"] = ""
        pre = self.fresh_data()
        self.assertRefuses("A54", P.verify_post, pre, post, s)

    def test_refuses_a_crop_citing_a_new_id(self):
        # An isolated crop dict, because verify_post's crops-identical check would fire first on a
        # whole post-state. This drives cites() directly on the shape verify_post walks.
        crop = copy.deepcopy(self.data["crops"][0])
        crop.setdefault("storage", {})["sources"] = ["vce_hort_189"]
        self.assertEqual(P.cites(crop, IDS), {"vce_hort_189"})
        crop2 = copy.deepcopy(self.data["crops"][0])
        crop2["watering_anchoring_urls"] = {"umn_ext_trellises_cages": {"url": "https://x.edu/a"}}
        self.assertEqual(P.cites(crop2, IDS), {"umn_ext_trellises_cages"})

    def test_verify_post_reaches_the_crop_citation_check(self):
        # Entry-point reach: pre AND post both carry the citing crop, so crops are identical and only
        # the citation check can fire.
        pre = self.fresh_data()
        pre["crops"][0].setdefault("storage", {})["sources"] = ["vce_hort_189"]
        post = P.apply_to(pre, self.spec)
        self.assertRefuses("this promote admits, it does not cite", P.verify_post, pre, post, self.spec)

    def test_no_live_crop_cites_a_new_id(self):
        self.assertEqual(set().union(*(P.cites(c, IDS) for c in self.post()["crops"])), set())


if __name__ == "__main__":
    unittest.main()
