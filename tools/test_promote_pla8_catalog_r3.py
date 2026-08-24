#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r3.py. Base 6876840e.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_cr3_suite.py.

THE LOAD-BEARING FAMILY IS `Disambiguation`. Every one of these four mints sits next to an existing
method that means something close but different, and "close but different" is exactly how batch 1
produced 22 method-meaning mismatches. So each mint's `best_use` MUST name its neighbour, and the
guard checks the pairing rather than the mere presence of text:
    prompt_harvest        vs garden_sanitation
    sound_sowing_practice vs sensible_seeding_rate
    augmentative_release  vs beneficial_predators
    resistant_rootstock   vs resistant_varieties

`SourceFidelity` is the second family and guards the thing this round exists to prove. All four
claims were first recorded as unsourced and then found at T1 on a proper hunt. The guards assert
each mint carries the caveat its source actually publishes -- most importantly that
`augmentative_release` keeps UC IPM's warning that released predators starve or migrate elsewhere.
A mint that quotes the helpful half of a source and drops the limiting half is worse than no mint,
because it reads as sourced.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r3 as P  # noqa: E402
import build_pla8_catalog_r3_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "afe4d6978aa76ea3a0b8213f8c7f5e57e2dd373292ee20fd14e3f9e04de2fa6e"
MINTS = ("prompt_harvest", "sound_sowing_practice", "augmentative_release", "resistant_rootstock")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


# --------------------------------------------------------------------------- fixture
class Fixture(unittest.TestCase):
    def test_base_reconstructs(self):
        self.assertEqual(
            hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(), P.BASE_SHA)

    def test_post_sha_pinned(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_compact(self):
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_method_count_45_to_49(self):
        self.assertEqual(len(_pre()["control_methods"]), 45)
        self.assertEqual(len(_post()["control_methods"]), 49)


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_lacked_all_four(self):
        cm = _pre()["control_methods"]
        for k in MINTS:
            self.assertNotIn(k, cm)

    def test_all_four_land(self):
        cm = _post()["control_methods"]
        for k in MINTS:
            self.assertIn(k, cm)

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))


# --------------------------------------------------------------------------- load-bearing 1
class Disambiguation(unittest.TestCase):
    def test_every_mint_names_its_neighbour_in_best_use(self):
        cm = _post()["control_methods"]
        for k, neighbour in C.DISAMBIGUATION.items():
            self.assertIn(neighbour.lower(), cm[k]["best_use"].lower(), k)

    def test_every_named_neighbour_actually_exists(self):
        cm = _post()["control_methods"]
        for k, neighbour in C.DISAMBIGUATION.items():
            self.assertIn(neighbour.replace(" ", "_"), cm, f"{k} points at a method that is not there")

    def test_the_pairing_is_complete(self):
        self.assertEqual(set(C.DISAMBIGUATION), set(MINTS))

    def test_augmentative_release_distinguishes_BUYING_from_conserving(self):
        m = _post()["control_methods"]["augmentative_release"]
        s = (m["best_use"] + " " + m["how_it_works_beginner"]).lower()
        self.assertIn("conserv", s)
        self.assertTrue("buy" in s or "bought" in s or "purchase" in s)

    def test_sound_sowing_distinguishes_itself_from_DENSITY(self):
        m = _post()["control_methods"]["sound_sowing_practice"]
        self.assertIn("density", m["best_use"].lower())

    def test_prompt_harvest_distinguishes_the_crop_you_want_from_culls(self):
        m = _post()["control_methods"]["prompt_harvest"]
        self.assertIn("garden sanitation", m["best_use"].lower())

    def test_resistant_rootstock_distinguishes_root_from_cultivar(self):
        m = _post()["control_methods"]["resistant_rootstock"]
        self.assertIn("cultivar", m["best_use"].lower())


# --------------------------------------------------------------------------- load-bearing 2
class SourceFidelity(unittest.TestCase):
    def test_augmentative_release_keeps_the_limiting_half_of_its_source(self):
        """UC IPM says released predators starve or migrate elsewhere without prey, and that the
        best results come from conserving resident predators. A mint that kept only the helpful
        half would read as sourced while overselling a bought control."""
        m = _post()["control_methods"]["augmentative_release"]
        s = m["how_it_works_seasoned"].lower()
        self.assertIn("starve or migrate", s)
        self.assertIn("naturally occurring predators", s)

    def test_augmentative_release_cons_carry_the_same_limit(self):
        m = _post()["control_methods"]["augmentative_release"]
        self.assertTrue(any("starve" in c.lower() for c in m["cons"]))

    def test_sound_sowing_carries_the_measured_figures_from_source(self):
        m = _post()["control_methods"]["sound_sowing_practice"]
        s = m["how_it_works_seasoned"]
        self.assertIn("twice the width", s.lower())
        self.assertIn("65", s)

    def test_every_mint_records_a_source_read_with_a_quote(self):
        covered = {r["for"] for r in C.SOURCE_READS}
        self.assertEqual(covered, set(MINTS))
        for r in C.SOURCE_READS:
            self.assertTrue(r["quote"].strip())
            self.assertTrue(r["url"].startswith("https://"))
            self.assertEqual(r["read"], "2026-08-24")

    def test_recorded_quotes_belong_to_the_recorded_source_id(self):
        post = _post()
        for r in C.SOURCE_READS:
            m = post["control_methods"][r["for"]]
            self.assertIn(r["id"], m["sources"], f"{r['for']} does not cite {r['id']}")
            self.assertEqual(m["anchoring_urls"][r["id"]]["url"], r["url"])

    def test_pheromone_trap_is_recorded_as_NOT_NEEDED_not_merely_missing(self):
        """The hunt corrected a read finding; that correction has to survive in the record or the
        next session re-opens it as an owed mint."""
        self.assertIn("pheromone_trap", C.NOT_MINTED)
        self.assertIn("NOT NEEDED", C.NOT_MINTED["pheromone_trap"])
        self.assertNotIn("pheromone_trap", _post()["control_methods"])


# --------------------------------------------------------------------------- sourcing
class Sourcing(unittest.TestCase):
    def test_every_source_is_catalogued_and_T1(self):
        post = _post()
        sc = post["source_catalog"]
        for k in MINTS:
            m = post["control_methods"][k]
            self.assertTrue(m["sources"])
            for s in m["sources"]:
                self.assertIn(s, sc)
                self.assertEqual(sc[s].get("tier"), "T1", s)
            self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))

    def test_no_source_is_minted(self):
        pre = _pre()
        self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])

    def test_every_applies_to_target_is_reachable_from_some_problem_type(self):
        reachable = set().union(*TYPE_TARGETS.values())
        for k, m in C.NEW_METHODS.items():
            for t in m["applies_to"]:
                self.assertIn(t, reachable, f"{k}: {t} is unreachable, so the mint would be dead")


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_only_the_four_methods_are_added_and_none_edited(self):
        pre = _pre()
        post = _post(pre)
        a, b = pre["control_methods"], post["control_methods"]
        self.assertEqual(set(b) - set(a), set(MINTS))
        self.assertEqual(set(a) - set(b), set())
        self.assertEqual({k for k in a if a[k] != b[k]}, set(),
                         "this promote ADDS; it must not edit an existing method")

    def test_no_crop_is_touched(self):
        pre = _pre()
        self.assertEqual(pre["crops"], _post(pre)["crops"])

    def test_top_level_keys_unchanged(self):
        pre = _pre()
        self.assertEqual(set(pre), set(_post(pre)))


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def _strings(self):
        out = []
        for m in C.NEW_METHODS.values():
            for v in m.values():
                if isinstance(v, str):
                    out.append(v)
                elif isinstance(v, list):
                    out += [x for x in v if isinstance(x, str)]
        return out

    def test_no_dash_forms_barred_in_copy(self):
        for s in self._strings():
            self.assertIsNone(re.search(r"[—–]", s), s[:60])
            self.assertNotIn("--", s)

    def test_american_english(self):
        for s in self._strings():
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", s, re.I), f"{w} in {s[:60]}")

    def test_no_absolute_claims(self):
        for s in self._strings():
            self.assertIsNone(re.search(
                r"\b(?:always|guaranteed|completely|totally|harmless)\b", s, re.I), s[:80])

    def test_degrees_are_unspaced(self):
        for s in self._strings():
            self.assertIsNone(re.search(r"\s°F", s), s[:80])

    def test_registers_are_materially_different(self):
        for k, m in C.NEW_METHODS.items():
            self.assertNotEqual(m["how_it_works_beginner"], m["how_it_works_seasoned"], k)

    def test_beginner_glosses_the_jargon_it_uses(self):
        """A grafted plant and a scion are not common tongue; the beginner half must explain."""
        m = _post()["control_methods"]["resistant_rootstock"]
        self.assertIn("two plants joined", m["how_it_works_beginner"].lower())
        self.assertNotIn("scion", m["how_it_works_beginner"].lower())


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    """REFUSAL-SPEC: green here means check() REFUSED a bad input."""

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_a_non_T1_source(self):
        d = _pre()
        d["source_catalog"]["ncsu_ext"] = dict(d["source_catalog"]["ncsu_ext"], tier="T2")
        self.assertIsNotNone(P.check(d))

    def test_refuses_if_a_disambiguation_neighbour_is_missing_from_the_catalog(self):
        d = _pre()
        d["control_methods"].pop("beneficial_predators")
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
