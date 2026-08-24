#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r2.py. Base 6b295d44.

REPLAY-PINNED; no RED phase claimed. Evidence is Reachability + tools/mutate_pla8_cr2_suite.py.

TWO LOAD-BEARING FAMILIES.

`SemanticSeparation` is the usual one for this arc: `prune_out_infection` must state the ACTION that
distinguishes it (cut beyond the visible margin into clean tissue) and must name `garden_sanitation`
as the home of the other action, or an author reaches for it again exactly as eight batch-1 rungs did.

`ShippedDataProtection` is the family this promote could not have been written without. The obvious
fix -- narrow `garden_sanitation` away from in-season removal and mint a herbaceous equivalent --
would have broken ~14 of its 42 rungs on SEVEN ALREADY-CERTIFIED crops, because its best_use legitimately
claims "in-season removal of the first infected leaves" and those rungs rely on it. So this family
asserts `garden_sanitation` is byte-identical before and after, and that the shipped in-season-removal
rungs still point at it. A promote that "fixes" a defect by creating fourteen more is the failure this
guards.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r2 as P  # noqa: E402
import build_pla8_catalog_r2_content as C  # noqa: E402

POST_SHA = "6876840ed629ca5a86f4052697426120b2c245d5895c1663e9b8722112f8e670"
MINTS = ("off_season_tillage", "certified_clean_stock")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")
# Shipped rungs that use garden_sanitation for IN-SEASON removal of infected tissue. If
# garden_sanitation is ever narrowed away from that meaning, every one of these becomes a mismatch.
SHIPPED_IN_SEASON = [
    ("broccoli", "downy-mildew"), ("broccoli", "clubroot"), ("broccoli", "black-rot"),
    ("strawberry", "gray-mold"), ("strawberry", "anthracnose"), ("strawberry", "verticillium-wilt"),
    ("celery", "pink-rot"), ("celery", "carrot-rust-fly"), ("asparagus", "asparagus-rust"),
    ("artichoke", "botrytis-gray-mold"), ("artichoke", "artichoke-curly-dwarf"),
]


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _leaves(data):
    out = {}
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for i, p in enumerate(c.get(fam) or []):
                if not isinstance(p, dict):
                    continue
                for k, v in p.items():
                    if isinstance(v, str):
                        out[f"{c.get('slug')}|{fam}|{i}|{k}"] = v
                for j, r in enumerate(p.get("control_ladder") or []):
                    for k, v in r.items():
                        if isinstance(v, str):
                            out[f"{c.get('slug')}|{fam}|{i}|rung{j}|{k}"] = v
    return out


def _ladder(data, slug, pid):
    p = P._problem(data, slug, pid)
    return (p or {}).get("control_ladder") or []


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

    def test_method_count_43_to_45(self):
        self.assertEqual(len(_pre()["control_methods"]), 43)
        self.assertEqual(len(_post()["control_methods"]), 45)


# --------------------------------------------------------------------------- reachability
class Reachability(unittest.TestCase):
    def test_base_lacked_both_mints(self):
        cm = _pre()["control_methods"]
        for k in MINTS:
            self.assertNotIn(k, cm)

    def test_base_had_both_artichoke_misuses(self):
        pre = _pre()
        for e in C.ARTICHOKE:
            self.assertEqual(_ladder(pre, "artichoke", e["id"])[e["rung"]]["method"], e["from"])

    def test_base_prune_reachable_from_four_sites(self):
        self.assertEqual(len(P.prune_sites(_pre())), 4)

    def test_base_fails_the_post_check(self):
        self.assertIsNotNone(P.verify_post(_pre()))

    def test_post_passes_the_post_check(self):
        self.assertIsNone(P.verify_post(_post()))


# --------------------------------------------------------------------------- load-bearing 1
class SemanticSeparation(unittest.TestCase):
    def test_prune_states_its_defining_action(self):
        m = _post()["control_methods"]["prune_out_infection"]
        self.assertIn("clean tissue", m["best_use"].lower())
        self.assertIn("beyond the visible margin", m["best_use"].lower())

    def test_prune_names_garden_sanitation_as_the_other_route(self):
        m = _post()["control_methods"]["prune_out_infection"]
        self.assertIn("garden sanitation", m["best_use"].lower())
        self.assertIn("garden sanitation", m["how_it_works_seasoned"].lower())

    def test_prune_beginner_leads_with_WHERE_you_cut(self):
        m = _post()["control_methods"]["prune_out_infection"]
        self.assertIn("where you cut", m["how_it_works_beginner"].lower())

    def test_off_season_tillage_names_garden_sanitation_as_distinct(self):
        m = _post()["control_methods"]["off_season_tillage"]
        self.assertIn("garden sanitation", m["best_use"].lower())
        self.assertIn("soil", m["best_use"].lower())

    def test_the_two_mints_do_not_claim_each_others_action(self):
        cm = _post()["control_methods"]
        self.assertNotIn("till", cm["certified_clean_stock"]["how_it_works_beginner"].lower())
        self.assertNotIn("seed", cm["off_season_tillage"]["best_use"].lower())

    def test_clean_stock_carries_the_basil_hot_water_exception(self):
        """The seasoned half must keep the source's caveat: basil seed is NOT hot-water treatable.
        A method that says 'treat your seed' without it would send a reader to ruin their seed."""
        m = _post()["control_methods"]["certified_clean_stock"]
        s = m["how_it_works_seasoned"].lower()
        self.assertIn("not amenable to hot-water", s)


# --------------------------------------------------------------------------- load-bearing 2
class ShippedDataProtection(unittest.TestCase):
    """garden_sanitation must survive byte-identical; ~14 shipped rungs depend on its meaning."""

    def test_garden_sanitation_is_untouched(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(pre["control_methods"]["garden_sanitation"],
                         post["control_methods"]["garden_sanitation"])

    def test_garden_sanitation_still_claims_in_season_leaf_removal(self):
        m = _post()["control_methods"]["garden_sanitation"]
        self.assertIn("removal of the first infected leaves", m["best_use"].lower())

    def test_shipped_in_season_rungs_still_point_at_garden_sanitation(self):
        post = _post()
        for slug, pid in SHIPPED_IN_SEASON:
            methods = [r.get("method") for r in _ladder(post, slug, pid)]
            self.assertIn("garden_sanitation", methods, f"{slug}/{pid}")

    def test_no_shipped_crop_other_than_artichoke_changes(self):
        pre = _pre()
        post = _post(pre)
        for slug in ("broccoli", "strawberry", "celery", "asparagus", "apple", "microgreens-mix"):
            self.assertEqual(P._crop(pre, slug), P._crop(post, slug), slug)


# --------------------------------------------------------------------------- artichoke
class ArtichokeRepoint(unittest.TestCase):
    def test_curly_dwarf_rung_changes_KEY_ONLY(self):
        pre, post = _pre(), None
        post = _post(pre)
        a = _ladder(pre, "artichoke", "artichoke-curly-dwarf")[1]
        b = _ladder(post, "artichoke", "artichoke-curly-dwarf")[1]
        self.assertEqual(a["method"], "prune_out_infection")
        self.assertEqual(b["method"], "certified_clean_stock")
        for k in ("note_beginner", "note_seasoned"):
            self.assertEqual(a.get(k), b.get(k), f"prose changed on {k}; only the key should move")

    def test_crown_rot_ladder_loses_the_self_refuting_rung(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(len(_ladder(pre, "artichoke", "bacterial-crown-rot")), 2)
        lad = _ladder(post, "artichoke", "bacterial-crown-rot")
        self.assertEqual(len(lad), 1)
        self.assertEqual(lad[0]["method"], "garden_sanitation")

    def test_the_dropped_rungs_content_is_not_lost(self):
        """The dropped rung told the reader to remove the whole plant rather than cut it back.
        That instruction must survive the drop, in the rung above."""
        lad = _ladder(_post(), "artichoke", "bacterial-crown-rot")
        note = lad[0]["note_beginner"].lower()
        self.assertIn("lift it out with its roots", note)
        self.assertIn("rather than trying to cut back", note)

    def test_no_rung_anywhere_still_tells_the_reader_not_to_do_its_own_method(self):
        """The crown-rot rung read 'rather than trying to cut back to healthy tissue' while filed
        under Pruning out infections. Nothing may point at prune_out_infection and say that."""
        post = _post()
        for slug, pid in P.prune_sites(post):
            for r in _ladder(post, slug, pid):
                if r.get("method") != "prune_out_infection":
                    continue
                self.assertNotIn("rather than trying to cut back",
                                 (r.get("note_beginner") or "").lower(), f"{slug}/{pid}")

    def test_artichoke_ladders_stay_tier_non_decreasing(self):
        post = _post()
        order = {t: i for i, t in enumerate(P.TIERS)}
        cm = post["control_methods"]
        for pid in ("artichoke-curly-dwarf", "bacterial-crown-rot", "botrytis-gray-mold"):
            tiers = [order[cm[r["method"]]["tier"]] for r in _ladder(post, "artichoke", pid)]
            self.assertEqual(tiers, sorted(tiers), pid)


# --------------------------------------------------------------------------- survivors
class PruneSurvivors(unittest.TestCase):
    def test_exactly_the_two_genuine_cut_back_rungs_remain(self):
        self.assertEqual(P.prune_sites(_post()), P.PRUNE_SURVIVORS)

    def test_apple_fire_blight_is_untouched(self):
        pre = _pre()
        self.assertEqual(P._problem(pre, "apple", "fire-blight"),
                         P._problem(_post(pre), "apple", "fire-blight"))


# --------------------------------------------------------------------------- blast radius
class BlastRadius(unittest.TestCase):
    def test_leaf_sets_compared_before_any_value_comparison(self):
        pre = _pre()
        post = _post(pre)
        a, b = _leaves(pre), _leaves(post)
        dropped = set(a) - set(b)
        # exactly one rung is removed, so its leaves are the only permitted disappearance
        self.assertTrue(all(k.startswith("artichoke|") and "|rung1|" in k for k in dropped), dropped)
        self.assertEqual(set(b) - set(a), set(), "no leaf may be ADDED to a crop")

    def test_only_artichoke_changes_among_crops(self):
        pre = _pre()
        post = _post(pre)
        changed = [c["slug"] for c in pre["crops"]
                   if c != P._crop(post, c["slug"])]
        self.assertEqual(changed, ["artichoke"])

    def test_source_catalog_untouched(self):
        pre = _pre()
        self.assertEqual(pre["source_catalog"], _post(pre)["source_catalog"])

    def test_only_the_expected_methods_change(self):
        pre = _pre()
        post = _post(pre)
        a, b = pre["control_methods"], post["control_methods"]
        self.assertEqual(set(b) - set(a), set(MINTS))
        changed = {k for k in a if a[k] != b[k]}
        self.assertEqual(changed, {"prune_out_infection"})

    def test_prune_applies_to_and_sources_are_unchanged(self):
        pre = _pre()
        post = _post(pre)
        for f in ("applies_to", "sources", "anchoring_urls", "tier", "name"):
            self.assertEqual(pre["control_methods"]["prune_out_infection"][f],
                             post["control_methods"]["prune_out_infection"][f], f)


# --------------------------------------------------------------------------- sourcing
class Sourcing(unittest.TestCase):
    def test_every_mint_source_is_catalogued_and_T1(self):
        post = _post()
        sc = post["source_catalog"]
        for k in MINTS:
            m = post["control_methods"][k]
            self.assertTrue(m["sources"])
            for s in m["sources"]:
                self.assertIn(s, sc)
                self.assertEqual(sc[s].get("tier"), "T1", s)
            self.assertEqual(set(m["anchoring_urls"]), set(m["sources"]))

    def test_the_source_reads_are_recorded_for_both_mints(self):
        covered = {r["for"] for r in C.SOURCE_READS}
        self.assertEqual(covered, set(MINTS))
        for r in C.SOURCE_READS:
            self.assertTrue(r["quote"].strip())
            self.assertEqual(r["read"], "2026-08-24")

    def test_what_was_not_minted_is_recorded_with_a_reason(self):
        """A written list of what was not done is a legitimate close; an empty one is not."""
        self.assertEqual(set(C.NOT_MINTED), {"pheromone_trap", "container_culture", "staking_support"})
        for k, v in C.NOT_MINTED.items():
            self.assertGreater(len(v), 20, k)


# --------------------------------------------------------------------------- copy hygiene
class CopyHygiene(unittest.TestCase):
    def _new_strings(self):
        """Only text THIS PROMOTE AUTHORS. The merge preserves the surrounding original sentences
        byte-for-byte, including 'you may never see this at all' -- grading carried-over clauses
        would flag prose this promote did not write and pressure an edit nobody asked for."""
        import difflib
        out = []
        for m in C.NEW_METHODS.values():
            for k, v in m.items():
                if isinstance(v, str):
                    out.append(v)
                elif isinstance(v, list):
                    out += [x for x in v if isinstance(x, str)]
        for f in ("best_use", "how_it_works_beginner", "how_it_works_seasoned"):
            out.append(C.NARROW[f]["new"])
        old, new = C.ARTICHOKE_MERGE["old"], C.ARTICHOKE_MERGE["new"]
        sm = difflib.SequenceMatcher(None, old, new)
        inserted = "".join(new[j1:j2] for tag, _i1, _i2, j1, j2 in sm.get_opcodes()
                           if tag in ("insert", "replace"))
        self.assertTrue(inserted.strip(), "merge inserted nothing; the diff is vacuous")
        out.append(inserted)
        return out

    def test_no_dash_forms_barred_in_copy(self):
        for s in self._new_strings():
            self.assertIsNone(re.search(r"[—–]", s), s[:60])
            self.assertNotIn("--", s)

    def test_american_english(self):
        for s in self._new_strings():
            for w in BRITISH:
                self.assertIsNone(re.search(rf"\b{w}\b", s, re.I), f"{w} in {s[:60]}")

    def test_no_absolute_claims(self):
        for s in self._new_strings():
            self.assertIsNone(re.search(
                r"\b(?:always|never|guaranteed|completely|totally|harmless)\b", s, re.I), s[:80])

    def test_registers_are_materially_different(self):
        for k, m in C.NEW_METHODS.items():
            self.assertNotEqual(m["how_it_works_beginner"], m["how_it_works_seasoned"], k)


# --------------------------------------------------------------------------- refusals
class Refusals(unittest.TestCase):
    """REFUSAL-SPEC: green here means check() REFUSED a bad input."""

    def test_refuses_when_already_applied(self):
        self.assertIsNotNone(P.check(_post()))

    def test_refuses_a_mint_that_already_exists(self):
        d = _pre()
        d["control_methods"]["off_season_tillage"] = {"name": "x"}
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_non_T1_source(self):
        d = _pre()
        d["source_catalog"]["cornell_ext"] = dict(d["source_catalog"]["cornell_ext"], tier="T2")
        self.assertIsNotNone(P.check(d))

    def test_refuses_when_an_artichoke_rung_is_not_the_expected_method(self):
        d = _pre()
        _ladder(d, "artichoke", "bacterial-crown-rot")[1]["method"] = "garden_sanitation"
        self.assertIsNotNone(P.check(d))

    def test_refuses_when_the_merge_target_text_moved(self):
        d = _pre()
        lad = _ladder(d, "artichoke", "bacterial-crown-rot")
        lad[0]["note_beginner"] = lad[0]["note_beginner"].replace("Do not", "Don't")
        self.assertIsNotNone(P.check(d))

    def test_refuses_when_prune_is_used_somewhere_unreviewed(self):
        """A new site appearing before the narrowing must stop the promote, not be narrowed around."""
        d = _pre()
        _ladder(d, "celery", "pink-rot")[0]["method"] = "prune_out_infection"
        self.assertIsNotNone(P.check(d))

    def test_refuses_a_narrowing_whose_anchor_text_moved(self):
        d = _pre()
        m = d["control_methods"]["prune_out_infection"]
        m["best_use"] = m["best_use"].replace("The core fire blight control", "The main fire blight control")
        self.assertIsNotNone(P.check(d))

    def test_check_passes_on_the_real_base(self):
        self.assertIsNone(P.check(_pre()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
