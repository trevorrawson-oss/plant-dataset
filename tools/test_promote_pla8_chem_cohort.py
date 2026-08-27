#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_chem_cohort.py. Base 04b5aa69.

REPLAY-PINNED WITH A REAL RED PHASE: `test_pre_state_carries_the_defect` asserts the canonical this
promote is based on FAILS the false-rating scan on neem_oil (caution, pros, and one strawberry
rung), so the load-bearing guard is red on real shipped data and green only after the fix.

`VerifyPostIsDriven` is FIRST in this file by design. Eight of the conventional round's twelve
first-run mutation survivors were verify_post guards with no driver -- check() refuses every input
that could reach them, leaving the whole post-state half untested while green, for the fifth time
in this arc. Every test in that class doctors the APPLIED post directly, bypassing check().

`RatingScan` is the defect family: a medium-band method claiming a low bee/pollinator rating. It is
deliberately SCOPED to medium-band methods because insecticidal_soap is genuinely bee-low and its
"Low toxicity to bees" pro is CORRECT -- an unscoped token scan would flag correct prose, the
conventional round's lesson 5.

`CopperSplit` guards the caution that is purchasing advice: the four copper compounds split L/L/M/H
on acute, checked by SIDE with `named()` word-boundary matching so a compound moved to the wrong
rating, or named on two sides, is refused by name.

`Kept` pins the three methods verified byte-for-byte -- a verification is only worth recording if a
guard notices when it stops being true.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_chem_cohort as P  # noqa: E402

POST_SHA = "674fab251aec7063ffa970f8c81e6156ab6fdbcab1a5800d9a1c93627cdcd740"

# FROZEN LITERALS, deliberately not derived from the tables they validate (the computed-expected-
# value trap). If a P.* table is emptied, these stay put and the comparison reddens.
CHANGED = ("copper_fungicide", "neem_oil", "insecticidal_soap", "horticultural_oil")
KEPT = ("sulfur", "spinosad", "iron_phosphate_slug_bait")
MEDIUM = ("neem_oil", "spinosad", "horticultural_oil")
COPPERS = {"copper octanoate": "L", "copper ammonium complex": "L",
           "copper oxychloride sulfate": "M", "copper hydroxide": "H"}
ANCHORS = {"copper_fungicide": "125", "neem_oil": "38", "insecticidal_soap": "50",
           "horticultural_oil": "142"}


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _method(data, key):
    return data["control_methods"][key]


def _rung(data):
    r, problem = P.find_rung(data)
    assert problem is None, problem
    return r


class _Swap:
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = copy.deepcopy(getattr(P, self.n))
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _cautions(key, mapper):
    c = copy.deepcopy(P.CAUTIONS)
    c[key] = mapper(list(c[key]))
    return c


class VerifyPostIsDriven(unittest.TestCase):
    """EVERY post-state guard gets an input that REACHES it, by doctoring the applied post."""

    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_band_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        cs = [c.replace("except between sunset and midnight where the label allows, ", "")
              for c in _method(post, "neem_oil")["cautions"]]
        _method(post, "neem_oil")["cautions"] = cs
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("post-state fails the band check", problem)

    def test_rating_scan_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "horticultural_oil")["cautions"] = (
            _method(post, "horticultural_oil")["cautions"]
            + ["It has low toxicity to bees. Do not spray anything in flower except between "
               "sunset and midnight."])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("rating scan", problem)

    def test_split_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        cs = [c.replace("Moderate for copper oxychloride sulfate",
                        "Moderate for copper octanoate and copper oxychloride sulfate")
              for c in _method(post, "copper_fungicide")["cautions"]]
        _method(post, "copper_fungicide")["cautions"] = cs
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("copper octanoate", problem)

    def test_authored_cautions_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        cs = list(_method(post, "insecticidal_soap")["cautions"])
        _method(post, "insecticidal_soap")["cautions"] = cs[1:] + cs[:1]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("not what was authored", problem)

    def test_authored_pros_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "neem_oil")["pros"] = list(reversed(_method(post, "neem_oil")["pros"]))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("pros are not what was authored", problem)

    def test_field_set_change_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "copper_fungicide")["smuggled_field"] = "x"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("field set changed", problem)

    def test_frozen_field_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "copper_fungicide")["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("best_use", problem)

    def test_anchor_set_equality_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "neem_oil")["anchoring_urls"]["stray_source"] = {
            "url": "https://example.org", "verified": P.VERIFIED}
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("anchoring_urls keys do not match sources", problem)

    def test_anchor_pointing_at_the_wrong_page_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "neem_oil")["anchoring_urls"][P.SOURCE_ID]["url"] = P.DETAIL % "115"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("does not point at its own page", problem)

    def test_kept_method_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _method(post, "spinosad")["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("kept method spinosad", problem)

    def test_rung_landing_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _rung(post)[P.RUNG["register"]] = P.RUNG["old"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("rung edit did not land", problem)

    def test_beyond_the_rung_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        crop = [c for c in post["crops"] if c.get("slug") == "strawberry"][0]
        crop["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("beyond the one rung register", problem)

    def test_residual_rating_claim_in_strawberry_runs_on_the_post(self):
        """A second low-bee claim elsewhere in the crop must be caught even with the rung fixed.
        The same claim is planted in BOTH the snapshot and the post, so the byte-compare guards
        stay quiet and only the residual scan can object."""
        pre = _pre()
        for p in [c for c in pre["crops"] if c.get("slug") == "strawberry"][0]["pests"]:
            if p.get("id") == "two-spotted-spider-mite":
                for r in p["control_ladder"]:
                    if r.get("method") == "neem_oil":
                        r["note_beginner"] += " It has low toxicity to bees."
        snap = P.snapshot(pre)
        post = _post(pre)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("still carries a low-bee-rating claim", problem)

    def test_bystander_crop_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        other = [c for c in post["crops"] if c.get("slug") != "strawberry"][0]
        other["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander crop", problem)

    def test_bystander_method_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        bystander = sorted(k for k in post["control_methods"] if k not in P.COHORT)[0]
        _method(post, bystander)["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander method", problem)

    def test_source_catalog_edit_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["source_catalog"][P.SOURCE_ID]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches no source", problem)

    def test_added_method_is_caught_set_equality_first(self):
        """PLA-162: iterating pre makes ADDITIONS in post invisible."""
        pre, snap, post = self._staged()
        post["control_methods"]["ghost_method"] = copy.deepcopy(
            post["control_methods"]["sulfur"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("control_methods roster", problem)

    def test_added_crop_is_caught(self):
        pre, snap, post = self._staged()
        ghost = copy.deepcopy(post["crops"][0])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("crop roster", problem)

    def test_added_source_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["ghost_source"] = {"tier": "T1"}
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog roster", problem)


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

    def test_method_and_source_counts_unchanged(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(pre["control_methods"]), len(post["control_methods"]))
        self.assertEqual(len(pre["source_catalog"]), len(post["source_catalog"]))
        self.assertEqual(len(pre["crops"]), len(post["crops"]))

    def test_clean_promote_passes_both_phases(self):
        pre = _pre()
        self.assertIsNone(P.check(pre))
        p = copy.deepcopy(pre)
        self.assertIsNone(P.verify_post(P.snapshot(pre), P.apply_to(p)))


class RatingScan(unittest.TestCase):
    """The defect family: a medium-band method claiming a low bee/pollinator rating."""

    def test_pre_state_carries_the_defect(self):
        """RED on the shipped canonical: the caution, the pro, and the rung all claim it."""
        pre = _pre()
        m = _method(pre, "neem_oil")
        self.assertIsNotNone(P.false_rating_violation("neem_oil", m))
        self.assertTrue(any("low in toxicity to bees" in c for c in m["cautions"]))
        self.assertTrue(any("pollinators" in p for p in m["pros"]))
        self.assertTrue(P.FALSE_RATING.search(_rung(pre)[P.RUNG["register"]]))

    def test_pre_state_anchor_never_made_the_claim(self):
        """The false rating cites UC IPM; the entry's anchor is pn7404, which rates nothing.
        Forward assertion of the read, not a mechanical check -- the document was read live."""
        m = _method(_pre(), "neem_oil")
        self.assertIn("pn7404", m["anchoring_urls"]["ucanr_ext"]["url"])

    def test_post_state_is_clean_on_every_medium_band_method(self):
        post = _post()
        for key in MEDIUM:
            self.assertIsNone(P.false_rating_violation(key, _method(post, key)), key)

    def test_scan_is_scoped_so_soaps_correct_claim_survives(self):
        """insecticidal_soap IS bee-low; an unscoped scan would flag its correct pro."""
        post = _post()
        soap = _method(post, "insecticidal_soap")
        self.assertTrue(any("Low toxicity to bees" in p for p in soap["pros"]))
        self.assertIsNone(P.false_rating_violation("insecticidal_soap", soap))
        self.assertEqual(P.BAND_OF["insecticidal_soap"], "low")

    def test_scan_reads_every_copy_field_not_just_cautions(self):
        m = copy.deepcopy(_method(_post(), "neem_oil"))
        for f in ("best_use", "how_it_works_beginner", "find_it_beginner"):
            doctored = copy.deepcopy(m)
            doctored[f] = (doctored[f] or "") + " Low toxicity to bees."
            self.assertIsNotNone(P.false_rating_violation("neem_oil", doctored), f)

    def test_scan_matches_both_shipped_defect_spellings(self):
        self.assertTrue(P.FALSE_RATING.search("rates neem low in toxicity to bees"))
        self.assertTrue(P.FALSE_RATING.search("low toxicity to bees but, as a contact spray"))
        self.assertTrue(P.FALSE_RATING.search("Low toxicity to people, pets, and pollinators"))

    def test_scan_does_not_flag_prescriptions_or_low_residue(self):
        self.assertIsNone(P.FALSE_RATING.search(
            "another low-residue option that coats and disrupts aphids, spray at dusk to avoid "
            "wetting bees"))
        self.assertIsNone(P.FALSE_RATING.search("hard on bees while the spray is wet"))

    def test_check_refuses_an_authored_rung_that_keeps_the_claim(self):
        with _Swap("RUNG", {**copy.deepcopy(P.RUNG), "new": P.RUNG["old"]}):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("still claims a low bee rating", problem)

    def test_promote_refuses_to_run_if_the_defect_is_already_gone(self):
        pre = _pre()
        m = _method(pre, "neem_oil")
        m["cautions"] = [c for c in m["cautions"] if "low in toxicity" not in c]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("should not run", problem)

    def test_check_refuses_a_drifted_rung(self):
        """Re-verify before acting: if the rung is not the recorded pre-state string, decline."""
        pre = _pre()
        _rung(pre)[P.RUNG["register"]] = "Someone edited this rung since the read."
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("not the recorded pre-state", problem)

    def test_check_refuses_an_ambiguous_rung(self):
        """A second neem rung on the same ladder makes the edit target ambiguous; decline."""
        pre = _pre()
        crop = [c for c in pre["crops"] if c.get("slug") == "strawberry"][0]
        for p in crop["pests"]:
            if p.get("id") == P.RUNG["problem"]:
                ladder = p["control_ladder"]
                ladder.append(copy.deepcopy(
                    [r for r in ladder if r.get("method") == P.RUNG["method"]][0]))
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("exactly one neem_oil rung", problem)


class Band(unittest.TestCase):
    def test_authored_bee_cautions_carry_the_window(self):
        cm = _post()["control_methods"]
        for key in P.AUTHORED_BEE:
            blob = " ".join(cm[key]["cautions"]).lower()
            self.assertIn("sunset", blob, key)
            self.assertIn("midnight", blob, key)
            self.assertIsNone(P.band_violation(key, cm[key]["cautions"]))

    def test_losing_the_window_is_refused(self):
        for key in P.AUTHORED_BEE:
            def strip(cs):
                return [c.replace(
                    "except between sunset and midnight where the label allows, ", "")
                    for c in cs]
            with _Swap("CAUTIONS", _cautions(key, strip)):
                problem = P.check(_pre())
            self.assertIsNotNone(problem, key)
            self.assertIn("middle bee band", problem)

    def test_dropping_the_bee_caution_is_refused_by_the_band_guard(self):
        for key in P.AUTHORED_BEE:
            def drop(cs):
                return [c for c in cs if "flower" not in c.lower()]
            with _Swap("CAUTIONS", _cautions(key, drop)):
                problem = P.check(_pre())
            self.assertIsNotNone(problem, key)
            self.assertIn("no caution mentions flowering plants", problem)

    def test_band_table_matches_the_measured_ratings(self):
        by_name = {v[0]: v for v in P.RATINGS.values()}
        self.assertEqual(by_name["neem oil"][3], "medium")
        self.assertEqual(by_name["azadirachtin"][3], "medium")
        self.assertEqual(by_name["horticultural oil"][3], "medium")
        self.assertEqual(by_name["spinosad"][3], "medium")
        self.assertEqual(by_name["potassium salts of fatty acids"][3], "low")
        self.assertEqual(by_name["sulfur"][3], "low")
        self.assertEqual(by_name["iron phosphate"][3], "low")
        for key in MEDIUM:
            self.assertEqual(P.BAND_OF[key], "medium", key)

    def test_spinosads_dusk_advice_is_the_medium_bands_own_allowance(self):
        """The conventional round's defect was dusk advice on a HIGH-band material. Spinosad is
        MEDIUM, so its shipped dusk caution is correct and kept -- the refusal-spec pass."""
        m = _method(_pre(), "spinosad")
        self.assertIn("dusk", " ".join(m["cautions"]).lower())
        self.assertEqual(P.BAND_OF["spinosad"], "medium")
        self.assertIn("spinosad", KEPT)


class CopperSplit(unittest.TestCase):
    def test_the_split_is_the_frozen_four(self):
        """Literal here, table in P; emptying either reddens this."""
        want = {}
        for rating, names in P.ACUTE_SIDES.items():
            for n in names:
                want[n] = rating
        self.assertEqual(want, COPPERS)

    def test_sides_cross_check_the_ratings_rows(self):
        by_name = {v[0]: v for v in P.RATINGS.values()}
        for name, rating in COPPERS.items():
            self.assertEqual(by_name[name][4], rating, name)
            self.assertEqual(by_name[name][5], "nkr", name)

    def test_clean_split_passes(self):
        self.assertIsNone(P.split_violation(P.CAUTIONS["copper_fungicide"]))

    def test_moving_each_copper_to_each_wrong_side_is_refused_by_name(self):
        c0 = P.CAUTIONS["copper_fungicide"]
        moves = [
            ("copper hydroxide", "High, the DANGER signal-word band, for copper hydroxide",
             "High, the DANGER signal-word band, for copper oxide"),
            ("copper octanoate", "Low for copper octanoate", "Low for copper stearate"),
            ("copper ammonium complex", "and for copper ammonium complex", "and more"),
            ("copper oxychloride sulfate", "Moderate for copper oxychloride sulfate",
             "Moderate for copper chloride"),
        ]
        for name, old, new in moves:
            cs = [c.replace(old, new) for c in c0]
            if cs == list(c0):
                self.fail(f"{name}: the injection is inert")
            problem = P.split_violation(cs)
            self.assertIsNotNone(problem, name)
            self.assertIn(name, problem)

    def test_a_copper_named_on_two_sides_is_refused(self):
        cs = [c.replace("Moderate for copper oxychloride sulfate",
                        "Moderate for copper hydroxide and copper oxychloride sulfate")
              for c in P.CAUTIONS["copper_fungicide"]]
        problem = P.split_violation(cs)
        self.assertIsNotNone(problem)
        self.assertIn("copper hydroxide", problem)

    def test_word_boundary_matters_for_copper_names(self):
        """'copper' alone, or a name inside a longer name, must not satisfy the side check."""
        self.assertFalse(P.named("copper octanoate", "low for copper octanoate-free blends"))
        self.assertTrue(P.named("copper octanoate", "low for copper octanoate, the soap"))
        self.assertFalse(P.named("copper hydroxide", "high for copper"))

    def test_losing_the_chronic_absence_clause_is_refused(self):
        cs = [c.replace("; none of the four carries a California Prop 65 or US EPA chronic "
                        "listing", "") for c in P.CAUTIONS["copper_fungicide"]]
        problem = P.split_violation(cs)
        self.assertIsNotNone(problem)
        self.assertIn("chronic-absence", problem)

    def test_two_acute_cautions_are_refused(self):
        cs = list(P.CAUTIONS["copper_fungicide"]) + ["More acute toxicity notes."]
        problem = P.split_violation(cs)
        self.assertIsNotNone(problem)
        self.assertIn("exactly one", problem)

    def test_split_guard_runs_inside_check(self):
        def scramble(cs):
            return [c.replace("Low for copper octanoate", "Low for copper stearate") for c in cs]
        with _Swap("CAUTIONS", _cautions("copper_fungicide", scramble)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("copper octanoate", problem)

    def test_no_bee_caution_is_authored_for_copper_and_that_is_deliberate(self):
        """Hydroxide alone carries a band (medium); the home form is unrated and the entry gives
        no bee timing advice. Recorded as checked-and-not-added; this pins the decision."""
        blob = " ".join(_method(_post(), "copper_fungicide")["cautions"]).lower()
        self.assertNotIn("sunset", blob)
        self.assertNotIn("bee", blob)
        by_name = {v[0]: v for v in P.RATINGS.values()}
        self.assertEqual(by_name["copper hydroxide"][3], "medium")
        self.assertEqual(by_name["copper octanoate"][3], "unrated")


class Disclosure(unittest.TestCase):
    AXES = {
        "copper_fungicide": ("acute toxicity", "prop 65", "aquatic", "label"),
        "neem_oil": ("flower", "90°f"),
        "insecticidal_soap": ("acute toxicity", "no known risk", "lowest band", "90°f"),
        "horticultural_oil": ("flower", "90°f"),
    }

    def test_every_axis_is_present_on_every_changed_method(self):
        cm = _post()["control_methods"]
        for key, tokens in self.AXES.items():
            blob = " ".join(cm[key]["cautions"]).lower()
            for t in tokens:
                self.assertIn(t, blob, f"{key} missing {t!r}")

    def test_soap_states_the_mild_halves_with_the_moderate_rating(self):
        """A standard that reports only the alarming axis is not a standard -- and the inverse:
        an entry that reported only the mild axis now states the Moderate one, with the mild
        halves kept beside it."""
        cs = _method(_post(), "insecticidal_soap")["cautions"]
        acute = [c for c in cs if "acute toxicity" in c.lower()]
        self.assertEqual(len(acute), 1)
        self.assertIn("Moderate", acute[0])
        self.assertIn("no known risk", acute[0])
        self.assertIn("lowest band", acute[0])

    def test_soap_pros_no_longer_claim_low_toxicity_to_people(self):
        pre_pros = _method(_pre(), "insecticidal_soap")["pros"]
        post_pros = _method(_post(), "insecticidal_soap")["pros"]
        self.assertTrue(any("people" in p for p in pre_pros))
        self.assertFalse(any("people" in p for p in post_pros))

    def test_neem_pros_keep_people_and_drop_pollinators(self):
        """Symmetric with soap: for neem the SUPPORTED half is people/pets (acute L, chronic
        NKR) and the unsupported half is pollinators (band medium)."""
        post_pros = _method(_post(), "neem_oil")["pros"]
        self.assertTrue(any("people and pets" in p for p in post_pros))
        self.assertFalse(any("pollinators" in p for p in post_pros))

    def test_duplicate_caution_is_refused(self):
        with _Swap("CAUTIONS", _cautions("copper_fungicide", lambda cs: cs + [cs[0]])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("duplicate", problem)


class Preserved(unittest.TestCase):
    def test_preserved_claims_survive_in_post(self):
        cm = _post()["control_methods"]
        for key, claims in P.PRESERVED.items():
            blob = " ".join(list(cm[key]["cautions"]) + list(cm[key].get("pros") or []))
            for c in claims:
                self.assertIn(c, blob, f"{key} lost {c[:40]!r}")

    def test_dropping_a_preserved_caution_claim_is_refused(self):
        for key, claims in P.PRESERVED.items():
            for claim in claims:
                if not any(claim in c for c in P.CAUTIONS[key]):
                    continue  # pros-side claims are guarded below
                def drop(cs, cl=claim):
                    return [c for c in cs if cl not in c]
                if len(drop(list(P.CAUTIONS[key]))) == len(P.CAUTIONS[key]):
                    self.fail(f"{key}: {claim[:40]!r} matched nothing")
                with _Swap("CAUTIONS", _cautions(key, drop)):
                    problem = P.check(_pre())
                self.assertIsNotNone(problem, f"{key} passed having dropped {claim[:40]!r}")

    def test_dropping_a_preserved_pros_claim_is_refused(self):
        pros = copy.deepcopy(P.PROS)
        pros["insecticidal_soap"] = [p for p in pros["insecticidal_soap"]
                                     if "Leaves no toxic residue" not in p]
        with _Swap("PROS", pros):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("preserved claim dropped", problem)

    def test_a_preserved_claim_absent_from_the_pre_state_is_refused(self):
        pres = copy.deepcopy(P.PRESERVED)
        pres["copper_fungicide"] = pres["copper_fungicide"] + (
            "Invented claim never previously shipped",)
        cs = _cautions("copper_fungicide",
                       lambda c: c + ["Invented claim never previously shipped"])
        with _Swap("PRESERVED", pres), _Swap("CAUTIONS", cs):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("absent from the pre-state", problem)

    def test_the_rung_edit_keeps_the_prescription_and_the_heat_clause(self):
        self.assertIn("apply at dusk", P.RUNG["new"])
        self.assertIn("Avoid above 90°F or on stressed plants.", P.RUNG["new"])
        self.assertIn("contact smothering and as an antifeedant and growth regulator",
                      P.RUNG["new"])


class Kept(unittest.TestCase):
    def test_kept_methods_are_byte_identical(self):
        pre, post = _pre()["control_methods"], _post()["control_methods"]
        for key in KEPT:
            self.assertEqual(pre[key], post[key], key)

    def test_kept_methods_do_not_gain_the_source(self):
        post = _post()["control_methods"]
        for key in KEPT:
            self.assertNotIn(P.SOURCE_ID, post[key].get("sources") or [])

    def test_kept_pins_are_present_pre_and_post(self):
        pre, post = _pre()["control_methods"], _post()["control_methods"]
        for key, pin in P.KEPT_PINS.items():
            self.assertIn(pin, json.dumps(pre[key], ensure_ascii=False), key)
            self.assertIn(pin, json.dumps(post[key], ensure_ascii=False), key)

    def test_removing_a_kept_pin_is_refused(self):
        pre = _pre()
        m = _method(pre, "sulfur")
        m["cautions"] = [c for c in m["cautions"] if "predatory" not in c]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("kept method sulfur", problem)

    def test_kept_set_and_changed_set_partition_the_cohort(self):
        self.assertEqual(set(KEPT) | set(CHANGED), set(P.COHORT))
        self.assertEqual(set(KEPT) & set(CHANGED), set())
        self.assertEqual(set(P.KEPT), set(KEPT))
        self.assertEqual(set(P.CAUTIONS), set(CHANGED))


class Sources(unittest.TestCase):
    def test_no_source_is_minted_and_the_catalog_is_untouched(self):
        pre, post = _pre()["source_catalog"], _post()["source_catalog"]
        self.assertEqual(pre, post)

    def test_precondition_the_source_already_exists(self):
        pre = _pre()
        del pre["source_catalog"][P.SOURCE_ID]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("not in source_catalog", problem)

    def test_each_changed_method_anchors_its_own_ingredient_page(self):
        cm = _post()["control_methods"]
        seen = set()
        for key, uai in ANCHORS.items():
            self.assertEqual(dict(P.ANCHOR_KEY)[key], uai)
            url = cm[key]["anchoring_urls"][P.SOURCE_ID]["url"]
            self.assertTrue(url.endswith("uaiKey=" + uai), f"{key} anchors the wrong page")
            self.assertEqual(cm[key]["anchoring_urls"][P.SOURCE_ID]["verified"], P.VERIFIED)
            seen.add(uai)
        self.assertEqual(len(seen), 4, "two methods share one ingredient page")

    def test_every_anchor_key_is_a_row_that_was_read(self):
        for key, uai in P.ANCHOR_KEY.items():
            self.assertIn(uai, P.RATINGS, f"{key} anchors a page with no recorded reading")

    def test_prior_anchors_survive(self):
        pre, post = _pre()["control_methods"], _post()["control_methods"]
        for key in CHANGED:
            for sid, anchor in pre[key]["anchoring_urls"].items():
                self.assertEqual(post[key]["anchoring_urls"][sid], anchor, f"{key}/{sid}")

    def test_second_run_is_refused(self):
        pre = _pre()
        _method(pre, "neem_oil")["sources"].append(P.SOURCE_ID)
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already declares", problem)


class Hygiene(unittest.TestCase):
    def test_authored_copy_is_clean(self):
        for key, cs in P.CAUTIONS.items():
            for c in cs:
                self.assertIsNone(P.hygiene(c), f"{key}: {c[:60]!r}")
        for key, ps in P.PROS.items():
            for p in ps:
                self.assertIsNone(P.hygiene(p), f"{key}: {p[:60]!r}")
        self.assertIsNone(P.hygiene(P.RUNG["new"]))

    def test_em_dash_is_refused(self):
        with _Swap("CAUTIONS",
                   _cautions("copper_fungicide", lambda cs: [cs[0] + " — really"] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("em or en dash", problem)

    def test_safety_absolute_is_refused(self):
        with _Swap("CAUTIONS",
                   _cautions("copper_fungicide",
                             lambda cs: [cs[0] + " It is harmless to pets."] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("safety absolute", problem)

    def test_superlative_safest_is_now_an_absolute(self):
        """The artichoke rung's 'safest option' is filed, not fixed; the list at least refuses
        NEW copy making the same claim."""
        self.assertIn("absolute", P.hygiene("the safest bait around pets"))

    def test_rung_hygiene_is_checked(self):
        with _Swap("RUNG", {**copy.deepcopy(P.RUNG), "new": P.RUNG["new"] + " -- extra"}):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("rung: copy hygiene", problem)

    def test_hygiene_families_are_each_reachable(self):
        self.assertIn("em or en dash", P.hygiene("a — b"))
        self.assertIn("double hyphen", P.hygiene("a -- b"))
        self.assertIn("British", P.hygiene("the centre"))
        self.assertIn("absolute", P.hygiene("it is harmless"))
        self.assertIn("degree", P.hygiene("above 85 ° F"))
        self.assertIsNone(P.hygiene("Keep it out of ponds and streams."))


class RatingsAreTheControl(unittest.TestCase):
    def test_chlorothalonil_row_matches_the_verified_screenshot(self):
        """The positive control re-fetched LIVE this round before any cohort page was trusted."""
        self.assertEqual(P.RATINGS["115"],
                         ("chlorothalonil", "H", "L", "medium", "H", "prop65+epa"))

    def test_neem_rows_license_the_fix(self):
        """Both neem pages -- the whole oil and the active fraction -- sit in the medium band,
        so the split between them changes no verdict and the entry needs no which-one caution."""
        self.assertEqual(P.RATINGS["38"][0], "neem oil")
        self.assertEqual(P.RATINGS["38"][3], "medium")
        self.assertEqual(P.RATINGS["91"][0], "azadirachtin")
        self.assertEqual(P.RATINGS["91"][3], "medium")
        self.assertEqual(P.ANCHOR_KEY["neem_oil"], "38")

    def test_soap_row_licenses_the_moderate_disclosure(self):
        self.assertEqual(P.RATINGS["50"][4], "M")
        self.assertEqual(P.RATINGS["50"][3], "low")
        self.assertEqual(P.RATINGS["50"][5], "nkr")

    def test_iron_phosphate_and_its_rival_chemistry_were_both_read(self):
        """The prep asked which chemistry the entry means: iron phosphate (24), and ferric
        sodium EDTA (8) was read to confirm no split caution is owed -- both mild, chronic NKR."""
        self.assertEqual(P.RATINGS["24"], ("iron phosphate", "--", "L", "low", "VL", "nkr"))
        self.assertEqual(P.RATINGS["8"][0], "ferric sodium EDTA")
        self.assertEqual(P.RATINGS["8"][5], "nkr")

    def test_sulfurs_split_natural_enemy_rating_matches_its_kept_caution(self):
        self.assertEqual(P.RATINGS["70"][2], "LH")
        pre = _method(_pre(), "sulfur")
        self.assertTrue(any("predatory" in c for c in pre["cautions"]))

    def test_ratings_table_covers_exactly_what_was_read(self):
        self.assertEqual(len(P.RATINGS), 13)
        self.assertEqual({v[0] for v in P.RATINGS.values()},
                         {"chlorothalonil", "copper ammonium complex", "copper hydroxide",
                          "copper octanoate", "copper oxychloride sulfate", "sulfur", "neem oil",
                          "azadirachtin", "spinosad", "potassium salts of fatty acids",
                          "horticultural oil", "iron phosphate", "ferric sodium EDTA"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
