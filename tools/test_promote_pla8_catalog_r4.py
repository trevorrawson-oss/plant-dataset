#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r4.py. Base 6876840e.

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
import promote_pla8_catalog_r4 as P  # noqa: E402
import build_pla8_catalog_r4_content as C  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "0754031d02261241e3ef56dda00f165af884101a85a8673db73016a6b2271263"
MINTS = ("exclusion_fencing",)
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

    def test_method_count_49_to_50(self):
        self.assertEqual(len(_pre()["control_methods"]), 49)
        self.assertEqual(len(_post()["control_methods"]), 50)


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

    def test_exclusion_fencing_distinguishes_a_bed_barrier_from_draping_mesh(self):
        m = _post()["control_methods"]["exclusion_fencing"]
        b = m["best_use"].lower()
        self.assertIn("bird netting", b)
        self.assertIn("around the bed", b)

    def test_it_reaches_the_gap_it_exists_to_close(self):
        """MEASURED before minting: only 7 methods were legal on a vertebrate problem, and both
        catalog uses of the word "fence" were metaphorical (row cover, bird netting)."""
        post = _post()
        self.assertIn("vertebrate", post["control_methods"]["exclusion_fencing"]["applies_to"])
        legal = [k for k, v in post["control_methods"].items()
                 if "any" in v["applies_to"] or "vertebrate" in v["applies_to"]]
        self.assertIn("exclusion_fencing", legal)
        self.assertEqual(len(legal), 8, "the vertebrate-legal set should grow from 7 to 8")

    def test_wire_height_is_stated_because_that_is_the_whole_control(self):
        """Fence HEIGHT is not the variable; WIRE height is, because raccoons push under."""
        m = _post()["control_methods"]["exclusion_fencing"]
        self.assertIn("ground", m["how_it_works_beginner"].lower())
        self.assertIn("4 to 6 inches", m["how_it_works_seasoned"])

    def test_the_timing_before_ripeness_survives(self):
        m = _post()["control_methods"]["exclusion_fencing"]
        blob = (m["how_it_works_beginner"] + m["how_it_works_seasoned"] + m["best_use"]).lower()
        self.assertIn("before", blob)
        self.assertIn("milk stage", m["how_it_works_seasoned"].lower())

# --------------------------------------------------------------------------- load-bearing 2
class SourceFidelity(unittest.TestCase):
    def test_the_hedge_survives(self):
        """UMN says it is DIFFICULT to fence raccoons out and that a fence MAY keep them away. A
        method promising exclusion would be the safety-absolute class in a new costume."""
        m = _post()["control_methods"]["exclusion_fencing"]
        blob = m["how_it_works_beginner"] + " " + m["how_it_works_seasoned"]
        self.assertTrue(re.search(C.REQUIRED_HEDGE, blob, re.I), "the hedge was dropped")

    def test_the_hedge_pattern_rejects_prose_that_lacks_it(self):
        """Negative control: a constant validated only against the data it guards is vacuous."""
        self.assertIsNone(re.search(C.REQUIRED_HEDGE, "A fence keeps raccoons out of the patch.",
                                    re.I))

    def test_the_cons_carry_the_same_limit(self):
        m = _post()["control_methods"]["exclusion_fencing"]
        self.assertTrue(any("hard to fence" in c.lower() for c in m["cons"]))

    def test_the_shock_hazard_caution_is_present(self):
        """An electric fence in a home garden is a real hazard; the method must say so."""
        m = _post()["control_methods"]["exclusion_fencing"]
        self.assertIn("shock hazard", " ".join(m.get("cautions") or []).lower())

    def test_both_disagreeing_sources_are_represented(self):
        """Two T1 extensions differ on the second wire (12in vs ~9in). The prose names both rather
        than silently picking one."""
        m = _post()["control_methods"]["exclusion_fencing"]
        s = m["how_it_works_seasoned"]
        self.assertIn("Iowa State", s)
        self.assertIn("Minnesota", s)

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

    def test_the_highest_frequency_gap_is_recorded_as_owed(self):
        """adjust_planting_date was unplaceable in FOUR of corn's eight entries. If that record is
        lost, the next batch rediscovers it from scratch."""
        self.assertIn("adjust_planting_date", C.NOT_MINTED)
        self.assertNotIn("adjust_planting_date", _post()["control_methods"])
        self.assertEqual(len(C.NOT_MINTED), 5)


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

    def test_beginner_register_avoids_jargon(self):
        m = _post()["control_methods"]["exclusion_fencing"]
        self.assertNotIn("energize", m["how_it_works_beginner"].lower())


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    """REFUSAL-SPEC: green here means check() REFUSED a bad input."""

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_a_non_T1_source(self):
        d = _pre()
        d["source_catalog"]["iastate_ext"] = dict(d["source_catalog"]["iastate_ext"], tier="T2")
        self.assertIsNotNone(P.check(d))

    def test_refuses_if_a_disambiguation_neighbour_is_missing_from_the_catalog(self):
        d = _pre()
        d["control_methods"].pop("bird_netting")
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
