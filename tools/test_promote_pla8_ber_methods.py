#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_ber_methods.py. Base d19abe60.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_ber_suite.py.

THE LOAD-BEARING FAMILY IS `Distinctness`. These two methods exist BECAUSE widening the existing
ones would have produced prose that gates clean and reads as a non-sequitur, so the guards that
matter are the ones asserting the new copy does not drift back into the copy it was split from:
no aphids in the nitrogen method, no strawberries or gray mold in the mulch method, and each stating
its own mechanism rather than restating `even_watering`.
"""
import copy, hashlib, json, os, re, sys, unittest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_ber_methods as P  # noqa: E402

POST_SHA = "208e213cb14dce4e2df6b0a48ad49f7e6818337dcd4ce5b1b52691954af542ce"
NEW = ("moisture_buffering_mulch", "avoid_ammoniacal_nitrogen")
TIERS = ("cultural","physical","biological","soft_chemical","conventional")
REQ = ("name","tier","applies_to","how_it_works_beginner","how_it_works_seasoned","best_use",
       "pros","cons","sources","anchoring_urls")

def _pre(): return json.loads(promote_fixture.pre_state(P.BASE_SHA))
def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre()); P.apply_to(d); return d
def _strings():
    return [(f"{k}.{f}", t) for k, m in P.content().items() for f, v in m.items() if f != "name"
            for t in (v if isinstance(v, list) else [v] if isinstance(v, str) else [])]

class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)
    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)
    def test_output_is_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out); self.assertNotIn("\n", out)

class Reachability(unittest.TestCase):
    def test_base_lacked_both(self):
        pre = _pre()
        for k in NEW: self.assertNotIn(k, pre["control_methods"])
    def test_both_land(self):
        post = _post()
        for k in NEW: self.assertIn(k, post["control_methods"])
    def test_scope_is_exactly_two(self):
        self.assertEqual(sorted(P.content()), sorted(NEW))
    def test_physiological_gains_exactly_these(self):
        def legal(d): return {k for k, v in d["control_methods"].items()
                              if "any" in v["applies_to"] or "physiological" in v["applies_to"]}
        self.assertEqual(legal(_post()) - legal(_pre()), set(NEW))

class Distinctness(unittest.TestCase):
    """These exist because widening the originals would have shipped the WRONG PROSE."""
    def test_the_nitrogen_method_never_mentions_aphids_or_sappy_growth(self):
        m = _post()["control_methods"]["avoid_ammoniacal_nitrogen"]
        blob = json.dumps(m).lower()
        for bad in ("aphid", "sappy", "soft-bodied"):
            self.assertNotIn(bad, blob.replace("soft-bodied pests feed on", ""), bad)
    def test_the_mulch_method_never_mentions_strawberries_or_gray_mold(self):
        m = _post()["control_methods"]["moisture_buffering_mulch"]
        blob = json.dumps(m).lower()
        self.assertNotIn("gray mold", blob)
        self.assertNotIn("berries up off", blob)
    def test_each_states_its_own_mechanism(self):
        cm = _post()["control_methods"]
        self.assertIn("calcium", cm["avoid_ammoniacal_nitrogen"]["how_it_works_beginner"].lower())
        self.assertIn("compet", json.dumps(cm["avoid_ammoniacal_nitrogen"]).lower())
        self.assertIn("swing", cm["moisture_buffering_mulch"]["how_it_works_beginner"].lower())
    def test_the_mulch_method_distinguishes_itself_from_straw_mulch(self):
        self.assertIn("straw mulch", _post()["control_methods"]["moisture_buffering_mulch"]["best_use"].lower())
    def test_the_nitrogen_method_distinguishes_itself_from_balance_nitrogen(self):
        s = _post()["control_methods"]["avoid_ammoniacal_nitrogen"]["how_it_works_seasoned"].lower()
        self.assertIn("different lever", s)
    def test_neither_is_a_restatement_of_even_watering(self):
        import difflib
        cm = _post()["control_methods"]
        ev = cm["even_watering"]["how_it_works_beginner"].lower()
        for k in NEW:
            r = difflib.SequenceMatcher(None, cm[k]["how_it_works_beginner"].lower(), ev).ratio()
            self.assertLess(r, 0.85, f"{k} is a near-copy of even_watering ({r:.3f})")

class BlastRadius(unittest.TestCase):
    def test_no_crop_touched(self):
        pre = _pre(); self.assertEqual(pre["crops"], _post(pre)["crops"])
    def test_no_existing_method_changed(self):
        pre = _pre(); post = _post(pre)
        for k in pre["control_methods"]:
            self.assertEqual(pre["control_methods"][k], post["control_methods"][k], k)
    def test_source_catalog_untouched(self):
        pre = _pre(); self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])
    def test_other_top_level_untouched(self):
        pre = _pre(); post = _post(pre)
        self.assertEqual(set(pre), set(post))
        for k in pre:
            if k != "control_methods": self.assertEqual(pre[k], post[k], k)

class Shape(unittest.TestCase):
    def test_required_keys_and_tier(self):
        post = _post()
        for k in NEW:
            m = post["control_methods"][k]
            for f in REQ: self.assertTrue(m.get(f), f"{k}.{f}")
            self.assertIn(m["tier"], TIERS)
    def test_sources_are_T1_and_anchored(self):
        post = _post()
        for k in NEW:
            m = post["control_methods"][k]
            self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))
            for s in m["sources"]:
                self.assertEqual(post["source_catalog"][s]["tier"], "T1")
    def test_no_new_source_was_minted(self):
        self.assertEqual(set(_pre()["source_catalog"]), set(_post()["source_catalog"]))
    def test_anchor_points_at_the_document_read(self):
        for k in NEW:
            u = _post()["control_methods"][k]["anchoring_urls"]["clemson_hgic"]["url"]
            self.assertIn("tomato-diseases-disorders", u)

class Refusals(unittest.TestCase):
    def test_refuses_when_already_present(self):
        pre = _pre(); P.apply_to(pre)
        self.assertIn("already exists", P.check(pre))
    def test_clean_base_accepted(self):
        self.assertIsNone(P.check(_pre()))

class Mechanics(unittest.TestCase):
    def test_no_dashes(self):
        for w, t in _strings():
            for bad in ("—", "–", "--"): self.assertNotIn(bad, t, w)
    def test_american_english(self):
        for w, t in _strings():
            for b in ("colour","flavour","fertilise","organise","sulphur","centre","metre","mould","grey","labour"):
                self.assertIsNone(re.search(rf"\b{b}\b", t, re.I), f"{w}: {b}")
    def test_no_absolutes(self):
        for w, t in _strings():
            self.assertIsNone(re.search(r"\b(never|always|guaranteed|completely|totally|harmless)\b", t, re.I), w)
    def test_registers_differ(self):
        import difflib
        for k, m in P.content().items():
            r = difflib.SequenceMatcher(None, m["how_it_works_beginner"].lower(), m["how_it_works_seasoned"].lower()).ratio()
            self.assertLess(r, 0.85, k)

if __name__ == "__main__":
    unittest.main(verbosity=1)
