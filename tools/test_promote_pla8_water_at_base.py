#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_water_at_base.py. Base 208e213c.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_wab_suite.py.

THE LOAD-BEARING FAMILY IS `SemanticSeparation`. This promote exists because a method's applies_to
was widened while its PROSE still described a different action, and no structural gate could see it.
So the guards that matter assert the two methods stay semantically apart: bottom_watering keeps its
tray/seedling language and loses the outdoor targets, water_at_the_base carries the outdoor language
and never claims to water from below, and each says in `best_use` which is which.

It also guards the REVERT, which is the unusual part: this partially undoes d19abe60, keeping that
promote's sourcing while moving it to the right entry.
"""
import copy, hashlib, json, os, re, sys, unittest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_water_at_base as P  # noqa: E402

POST_SHA = "75b3c0f0c253ffa7cb420d0f9c9d35e2a04c5dd47d9c222271923b2cc2b41d32"
NEW = "water_at_the_base"
MOVED_SOURCES = ("ucanr_ext_bacterial_speck", "ucanr_ext_snails_slugs")

def _pre(): return json.loads(promote_fixture.pre_state(P.BASE_SHA))
def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre()); P.apply_to(d); return d

class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)
    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)
    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out); self.assertNotIn("\n", out)

class Reachability(unittest.TestCase):
    def test_base_lacked_the_new_method(self):
        self.assertNotIn(NEW, _pre()["control_methods"])
    def test_base_HAD_the_mis_attached_targets(self):
        a = _pre()["control_methods"]["bottom_watering"]["applies_to"]
        for t in ("bacterial", "mollusk"): self.assertIn(t, a)
    def test_new_method_lands(self):
        self.assertIn(NEW, _post()["control_methods"])

class SemanticSeparation(unittest.TestCase):
    """The defect this promote fixes: a method meaning a different ACTION from its rungs."""
    def test_bottom_watering_keeps_its_tray_meaning(self):
        m = _post()["control_methods"]["bottom_watering"]
        self.assertIn("from below", m["how_it_works_beginner"].lower())
        self.assertIn("tray", m["best_use"].lower())
    def test_water_at_the_base_never_claims_to_water_from_below(self):
        """Scoped to the how_it_works fields ON PURPOSE. `best_use` is REQUIRED to name bottom
        watering in order to disambiguate the two, so scanning the whole entry made this guard fire
        on the very disambiguation it exists to protect. The first version did exactly that."""
        m = _post()["control_methods"][NEW]
        for f in ("how_it_works_beginner", "how_it_works_seasoned"):
            self.assertNotIn("from below", m[f].lower(), f)
            self.assertNotIn("bottom water", m[f].lower(), f)
    def test_each_names_the_other_so_an_author_cannot_confuse_them(self):
        self.assertIn("bottom watering", _post()["control_methods"][NEW]["best_use"].lower())
    def test_the_new_method_states_the_outdoor_mechanism(self):
        m = _post()["control_methods"][NEW]
        self.assertIn("splash", json.dumps(m).lower())
        self.assertIn("leaves", m["how_it_works_beginner"].lower())

class Revert(unittest.TestCase):
    def test_bottom_watering_loses_exactly_the_two_targets(self):
        a = set(_pre()["control_methods"]["bottom_watering"]["applies_to"])
        b = set(_post()["control_methods"]["bottom_watering"]["applies_to"])
        self.assertEqual(a - b, {"bacterial", "mollusk"})
        self.assertEqual(b, {"fungal_soilborne", "insect_general"})
    def test_bottom_watering_sources_revert(self):
        self.assertEqual(_post()["control_methods"]["bottom_watering"]["sources"], ["ucanr_ext", "umn_ext"])
    def test_its_anchoring_urls_match_its_sources_after_the_revert(self):
        m = _post()["control_methods"]["bottom_watering"]
        self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))
    def test_the_moved_sources_are_NOT_orphaned(self):
        """The revert must not strand a catalogued source with no user."""
        post = _post()
        for s in MOVED_SOURCES:
            users = [k for k, v in post["control_methods"].items() if s in v.get("sources", [])]
            self.assertTrue(users, f"{s} is orphaned")
            self.assertIn(NEW, users, f"{s} did not move to {NEW}")
    def test_handpick_keeps_the_snails_source(self):
        self.assertIn("ucanr_ext_snails_slugs", _post()["control_methods"]["handpick"]["sources"])

class BlastRadius(unittest.TestCase):
    def test_no_crop_touched(self):
        pre = _pre(); self.assertEqual(pre["crops"], _post(pre)["crops"])
    def test_source_catalog_untouched(self):
        pre = _pre(); self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])
    def test_only_bottom_watering_changed_among_existing_methods(self):
        pre = _pre(); post = _post(pre)
        changed = {k for k in pre["control_methods"] if pre["control_methods"][k] != post["control_methods"][k]}
        self.assertEqual(changed, {"bottom_watering"})
    def test_other_top_level_untouched(self):
        pre = _pre(); post = _post(pre)
        self.assertEqual(set(pre), set(post))
        for k in pre:
            if k != "control_methods": self.assertEqual(pre[k], post[k], k)

class Shape(unittest.TestCase):
    def test_required_keys_tier_and_T1(self):
        post = _post(); m = post["control_methods"][NEW]
        for f in P.REQ: self.assertTrue(m.get(f), f)
        self.assertIn(m["tier"], P.TIERS)
        self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))
        for s in m["sources"]: self.assertEqual(post["source_catalog"][s]["tier"], "T1")
    def test_covers_every_use_the_pilot_needed(self):
        from control_ladder_gate import TYPE_TARGETS
        a = set(_post()["control_methods"][NEW]["applies_to"])
        for t in ("fungal", "bacterial", "mollusk"):
            self.assertTrue(a & TYPE_TARGETS[t], f"{NEW} illegal on {t}")

class Refusals(unittest.TestCase):
    def test_refuses_when_already_present(self):
        pre = _pre(); P.apply_to(pre); self.assertIn("already exists", P.check(pre))
    def test_refuses_a_noop_revert(self):
        pre = _pre()
        pre["control_methods"]["bottom_watering"]["applies_to"] = ["fungal_soilborne", "insect_general"]
        self.assertIn("no-op", P.check(pre))
    def test_clean_base_accepted(self):
        self.assertIsNone(P.check(_pre()))

class Mechanics(unittest.TestCase):
    def test_copy_rules(self):
        m = P.content()[0][NEW]
        strs = [t for f, v in m.items() if f != "name"
                for t in (v if isinstance(v, list) else [v] if isinstance(v, str) else [])]
        for t in strs:
            for bad in ("—", "–", "--"): self.assertNotIn(bad, t)
            self.assertIsNone(re.search(r"\b(never|always|guaranteed|completely|harmless)\b", t, re.I), t[:60])
    def test_registers_differ(self):
        import difflib
        m = P.content()[0][NEW]
        r = difflib.SequenceMatcher(None, m["how_it_works_beginner"].lower(), m["how_it_works_seasoned"].lower()).ratio()
        self.assertLess(r, 0.85)

if __name__ == "__main__":
    unittest.main(verbosity=1)
