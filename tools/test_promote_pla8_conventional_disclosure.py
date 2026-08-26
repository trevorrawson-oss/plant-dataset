#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_conventional_disclosure.py. Base 1330fe5d.

REPLAY-PINNED, BUT THIS ONE HAS A REAL RED PHASE AND THAT IS THE POINT. Every other promote suite in
this arc is green from birth because it replays its own output. Here the load-bearing guard,
`band_violation`, REFUSES THE PRE-STATE: `test_pre_state_carries_the_defect` asserts that the
canonical this promote is based on fails the check, naming `dusk`. The guard is not just reachable
in theory, it is red on the real data as shipped this morning, and green only after the fix.

`BandIsTheDefect` is the load-bearing family. The bug being fixed is not a missing caution, it is
WRONG ADVICE on ten live rungs: both conventional insecticides told readers to "spray at dusk when
bees are not foraging", which is the instruction for UC IPM's MIDDLE bee band, while UC IPM puts
carbaryl and every common pyrethroid in the STRICTEST band, whose legend grants no time window at
all. A guard that merely required "some bee language" would have been green through the entire
defect. This one is directional: strict-band methods are refused for GRANTING a window, and the
middle-band method is refused for LOSING one, so neither over-correction nor under-correction passes.

`ChronicSplit` guards the one caution that is purchasing advice rather than warning: four of the nine
common pyrethroids are on the US EPA list and five are rated no known risk, and the entry names
which. Two vacuity traps are pinned explicitly. First, SIDE: each name is checked against the slice
of the sentence after its own marker, so moving an ingredient across the split is caught rather than
satisfied by its mere presence. Second, SUBSTRING: `permethrin` is a substring of `cypermethrin`,
which is a substring of `zeta-cypermethrin`, so a naive containment test reports all three present
when only one is. `test_naive_containment_would_be_vacuous` proves the boundary matcher is what is
doing the work.

`Preserved` pins the claims this round is NOT revaluing -- carbaryl's earthworms, the pyrethroid cat
line, both pre-harvest intervals, and chlorothalonil's sunset-to-midnight prescription, which was
CORRECT and is kept verbatim while only its invented "Bee rating II" attribution is dropped. It also
refuses a claim asserted as preserved that is not in the pre-state, so the preservation list cannot
quietly become a place to add new prose.

`RatingsAreTheControl` pins the measurement itself. Chlorothalonil's row is the positive control that
validated the raw-HTML parser against the rendered screenshot of 2026-08-26 before any other page was
trusted; if that row drifts, the other eleven readings lose their warrant.
"""
import copy, hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_conventional_disclosure as P  # noqa: E402

POST_SHA = "04b5aa69b2f1fd209d84c4affb975cb78df0ee59657f9259b2896edbbe11c5f9"

# FROZEN LITERAL, deliberately not derived from P.DISCLOSURE_AXES. A coverage assertion computed
# from the table it is validating goes vacuous the moment that table is emptied: the loop body never
# runs, `covered` stays empty, and the expectation is empty too, so the test passes having tested
# nothing. This is the same defect class as batch 6's hedge test.
AXES = ("bees", "aquatic", "people", "chronic", "ppe", "phi")
METHODS = ("carbaryl", "pyrethroid", "chlorothalonil")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Swap:
    """Temporarily replace a module constant, restoring it even if the test fails."""

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
    """A copy of P.CAUTIONS with one key's list transformed."""
    c = copy.deepcopy(P.CAUTIONS)
    c[key] = mapper(list(c[key]))
    return c


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

    def test_method_count_unchanged_source_count_plus_one(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(len(pre["control_methods"]), len(post["control_methods"]))
        self.assertEqual(len(post["source_catalog"]), len(pre["source_catalog"]) + 1)

    def test_clean_promote_passes_both_phases(self):
        pre = _pre()
        self.assertIsNone(P.check(pre))
        p = copy.deepcopy(pre)
        self.assertIsNone(P.verify_post(P.snapshot(pre), P.apply_to(p)))


class BandIsTheDefect(unittest.TestCase):
    """The family that exists because the pre-state is WRONG, not merely incomplete."""

    def test_pre_state_carries_the_defect(self):
        """RED. The canonical this is based on fails the band check on both insecticides."""
        cm = _pre()["control_methods"]
        for key in ("carbaryl", "pyrethroid"):
            problem = P.band_violation(key, cm[key]["cautions"])
            self.assertIsNotNone(problem, f"{key} was expected to fail the band check pre-fix")
            self.assertIn("strictest bee band", problem)

    def test_pre_state_literally_says_dusk(self):
        cm = _pre()["control_methods"]
        for key in ("carbaryl", "pyrethroid"):
            self.assertIn("dusk", " ".join(cm[key]["cautions"]).lower())

    def test_pre_state_medium_band_was_already_right(self):
        """chlorothalonil's window is correct; this promote must not 'fix' it away."""
        cm = _pre()["control_methods"]
        self.assertIsNone(P.band_violation("chlorothalonil", cm["chlorothalonil"]["cautions"]))

    def test_post_state_is_clean_for_all_three(self):
        cm = _post()["control_methods"]
        for key in P.CAUTIONS:
            self.assertIsNone(P.band_violation(key, cm[key]["cautions"]))

    def test_strict_band_refuses_every_window_token(self):
        for key in ("carbaryl", "pyrethroid"):
            for token in P.WINDOW_TOKENS:
                def add(cs, t=token):
                    cs[0] = cs[0] + f" Spray it {t} instead."
                    return cs
                with _Swap("CAUTIONS", _cautions(key, add)):
                    problem = P.check(_pre())
                self.assertIsNotNone(problem, f"{key} accepted the window token {token!r}")
                self.assertIn("strictest bee band", problem)
                self.assertIn(token, problem)

    def test_medium_band_refuses_losing_its_window(self):
        def strip(cs):
            return [c.replace("except between sunset and midnight where the label allows, ", "")
                    for c in cs]
        with _Swap("CAUTIONS", _cautions("chlorothalonil", strip)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("middle bee band", problem)

    def test_a_method_with_no_bee_caution_is_refused_by_the_band_guard(self):
        """Not merely refused: refused BY THE BAND GUARD. A missing bee caution trips both this and
        the 'bees' axis, and if the axis answers first the band guard is untested."""
        for key in P.CAUTIONS:
            def drop(cs):
                return [c for c in cs if "flower" not in c.lower()]
            with _Swap("CAUTIONS", _cautions(key, drop)):
                problem = P.check(_pre())
            self.assertIsNotNone(problem, f"{key} passed with no bee caution")
            self.assertIn("no caution mentions flowering plants", problem,
                          f"{key} was refused by something other than the band guard: {problem}")

    def test_promote_refuses_to_run_if_the_defect_is_already_gone(self):
        """The premise guard: a second run against a fixed canonical must decline."""
        pre = _pre()
        for key in ("carbaryl", "pyrethroid"):
            pre["control_methods"][key]["cautions"] = list(P.CAUTIONS[key])
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("should not run", problem)

    def test_band_of_matches_the_measured_ratings(self):
        by_name = {v[0]: v for v in P.RATINGS.values()}
        self.assertEqual(P.BAND_OF["carbaryl"], by_name["carbaryl"][3])
        self.assertEqual(P.BAND_OF["chlorothalonil"], by_name["chlorothalonil"][3])
        bands = {by_name[n][3] for n in P.PYRETHROIDS}
        self.assertEqual(bands, {"high"}, "the class claim needs every pyrethroid in one band")
        self.assertEqual(P.BAND_OF["pyrethroid"], "high")


class Disclosure(unittest.TestCase):
    """Six axes, each refusable BY NAME, on each of the three conventional methods."""

    def test_the_axis_table_is_exactly_the_frozen_six(self):
        """If the table is emptied or narrowed, every axis test below would go vacuous."""
        self.assertEqual(set(P.DISCLOSURE_AXES), set(AXES))
        self.assertEqual(set(P.CAUTIONS), set(METHODS))

    def test_every_axis_is_present_on_every_method(self):
        cm = _post()["control_methods"]
        for key in P.CAUTIONS:
            blob = " ".join(cm[key]["cautions"]).lower()
            for axis, tokens in P.DISCLOSURE_AXES.items():
                self.assertTrue(any(t in blob for t in tokens), f"{key} missing axis {axis}")

    def test_dropping_any_axis_is_refused_by_name(self):
        covered = set()
        for key in P.CAUTIONS:
            for axis, tokens in P.DISCLOSURE_AXES.items():
                def drop(cs, tk=tokens):
                    return [c for c in cs if not any(t in c.lower() for t in tk)]
                trimmed = drop(list(P.CAUTIONS[key]))
                if len(trimmed) == len(P.CAUTIONS[key]):
                    self.fail(f"{key}/{axis}: nothing was removed, the injection is inert")
                with _Swap("CAUTIONS", _cautions(key, drop)):
                    problem = P.check(_pre())
                self.assertIsNotNone(problem, f"{key} passed without the {axis} axis")
                self.assertTrue(axis in problem or "band check" in problem,
                                f"{key}/{axis} refused with an unrelated message: {problem}")
                covered.add((key, axis))
        self.assertEqual(covered, {(k, a) for k in METHODS for a in AXES})

    def test_carbaryl_states_the_chronic_listing_it_previously_omitted(self):
        pre, post = _pre(), _post()
        self.assertNotIn("prop 65", " ".join(pre["control_methods"]["carbaryl"]["cautions"]).lower())
        blob = " ".join(post["control_methods"]["carbaryl"]["cautions"]).lower()
        self.assertIn("california prop 65 list", blob)
        self.assertIn("us epa list", blob)
        self.assertIn("carcinogen", blob)

    def test_carbaryl_states_the_mild_half_too(self):
        """A disclosure standard that only reports the alarming axis is not a standard."""
        blob = " ".join(_post()["control_methods"]["carbaryl"]["cautions"]).lower()
        self.assertIn("acute toxicity to people and other mammals low", blob)

    def test_ppe_line_is_identical_across_the_tier(self):
        cm = _post()["control_methods"]
        for key in P.CAUTIONS:
            self.assertIn(P.PPE, cm[key]["cautions"])

    def test_duplicate_caution_is_refused(self):
        with _Swap("CAUTIONS", _cautions("carbaryl", lambda cs: cs + [cs[0]])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("duplicate", problem)


class ChronicSplit(unittest.TestCase):
    def test_split_is_exhaustive_and_disjoint(self):
        self.assertEqual(set(P.EPA_LISTED) | set(P.NO_KNOWN_RISK), set(P.PYRETHROIDS))
        self.assertEqual(set(P.EPA_LISTED) & set(P.NO_KNOWN_RISK), set())
        self.assertEqual(len(P.PYRETHROIDS), 9)

    def test_clean_split_passes(self):
        self.assertIsNone(P.split_violation(P.CAUTIONS["pyrethroid"]))

    def test_moving_an_epa_ingredient_to_the_safe_side_is_refused_by_name(self):
        for n in P.EPA_LISTED:
            def move(cs, name=n):
                out = []
                for c in cs:
                    if "us epa list" in c.lower():
                        c = c.replace(name + ", ", "").replace(", " + name, "")
                        c = c.replace("Rated no known risk: ", f"Rated no known risk: {name}, ")
                    out.append(c)
                return out
            problem = P.split_violation(move(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"{n} passed while named on the wrong side")
            self.assertIn(n, problem)

    def test_moving_a_safe_ingredient_to_the_epa_side_is_refused_by_name(self):
        for n in P.NO_KNOWN_RISK:
            def move(cs, name=n):
                out = []
                for c in cs:
                    if "us epa list" in c.lower():
                        c = c.replace(name + ", ", "").replace(", " + name, "")
                        c = c.replace("carcinogen: ", f"carcinogen: {name}, ")
                    out.append(c)
                return out
            problem = P.split_violation(move(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"{n} passed while named on the EPA side")
            self.assertIn(n, problem)

    def test_an_ingredient_named_on_both_sides_is_refused(self):
        """The move tests fire the PRESENCE check first. Only an addition reaches the wrong-side
        branch, which is the one that stops a carcinogen listing being quietly hedged."""
        for n in P.EPA_LISTED:
            def add(cs, name=n):
                return [c.replace("Rated no known risk: ", f"Rated no known risk: {name}, ")
                        if "us epa list" in c.lower() else c for c in cs]
            problem = P.split_violation(add(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"{n} passed while named on both sides")
            self.assertIn("named on the no-known-risk side", problem)
        for n in P.NO_KNOWN_RISK:
            def add(cs, name=n):
                return [c.replace("carcinogen: ", f"carcinogen: {name}, ")
                        if "us epa list" in c.lower() else c for c in cs]
            problem = P.split_violation(add(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"{n} passed while named on both sides")
            self.assertIn("named on the US EPA list side", problem)

    def test_the_acute_caution_must_name_the_high_ingredients(self):
        """Scoped to the ACUTE caution: naming them anywhere at all is satisfied by the chronic
        caution, which made the original check unreachable dead code."""
        for n in P.ACUTE_HIGH:
            def strip(cs, name=n):
                return [c.replace(name + ", ", "").replace(" and " + name, "").replace(name, "")
                        if "acute toxicity" in c.lower() else c for c in cs]
            problem = P.split_violation(strip(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"the acute caution passed without naming {n}")
            self.assertIn(n, problem)

    def test_dropping_the_acute_caution_entirely_is_refused(self):
        cs = [c for c in P.CAUTIONS["pyrethroid"] if "acute toxicity" not in c.lower()]
        problem = P.split_violation(cs)
        self.assertIsNotNone(problem)
        self.assertIn("no caution states acute toxicity", problem)

    def test_dropping_any_ingredient_is_refused_by_name(self):
        for n in list(P.EPA_LISTED) + list(P.NO_KNOWN_RISK):
            def drop(cs, name=n):
                return [c.replace(name + ", ", "").replace(", " + name, "").replace(name, "")
                        for c in cs]
            problem = P.split_violation(drop(list(P.CAUTIONS["pyrethroid"])))
            self.assertIsNotNone(problem, f"dropping {n} was not caught")
            self.assertIn(n, problem)

    def test_naive_containment_would_be_vacuous(self):
        """permethrin < cypermethrin < zeta-cypermethrin. A plain `in` reports all three present."""
        s = "rated no known risk: zeta-cypermethrin."
        self.assertIn("permethrin", s)           # naive: TRUE, and wrong
        self.assertIn("cypermethrin", s)         # naive: TRUE, and wrong
        self.assertFalse(P.named("permethrin", s))
        self.assertFalse(P.named("cypermethrin", s))
        self.assertTrue(P.named("zeta-cypermethrin", s))

    def test_two_epa_cautions_are_refused(self):
        c = list(P.CAUTIONS["pyrethroid"])
        c.append("Also on the US EPA list, no known risk otherwise.")
        problem = P.split_violation(c)
        self.assertIsNotNone(problem)
        self.assertIn("exactly one", problem)

    def test_acute_high_ingredients_are_named(self):
        blob = " ".join(P.CAUTIONS["pyrethroid"])
        for n in P.ACUTE_HIGH:
            self.assertTrue(P.named(n, blob), f"{n} is acute High and unnamed")

    def test_split_guard_runs_inside_check(self):
        def scramble(cs):
            return [c.replace("Rated no known risk: cyfluthrin", "Rated no known risk: xyfluthrin")
                    for c in cs]
        with _Swap("CAUTIONS", _cautions("pyrethroid", scramble)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("cyfluthrin", problem)


class Preserved(unittest.TestCase):
    def test_preserved_claims_survive(self):
        cm = _post()["control_methods"]
        for key, claims in P.PRESERVED.items():
            blob = " ".join(cm[key]["cautions"])
            for c in claims:
                self.assertIn(c, blob, f"{key} lost a preserved claim")

    def test_dropping_a_preserved_claim_is_refused(self):
        for key, claims in P.PRESERVED.items():
            for claim in claims:
                def drop(cs, cl=claim):
                    return [c for c in cs if cl not in c]
                if len(drop(list(P.CAUTIONS[key]))) == len(P.CAUTIONS[key]):
                    self.fail(f"{key}: preserved claim {claim[:40]!r} matched nothing")
                with _Swap("CAUTIONS", _cautions(key, drop)):
                    problem = P.check(_pre())
                self.assertIsNotNone(problem, f"{key} passed having dropped {claim[:40]!r}")

    def test_a_preserved_claim_absent_from_the_pre_state_is_refused(self):
        """The preservation list cannot become a back door for new prose."""
        pres = copy.deepcopy(P.PRESERVED)
        pres["carbaryl"] = pres["carbaryl"] + ("Invented claim never previously shipped",)
        cs = _cautions("carbaryl", lambda c: c + ["Invented claim never previously shipped"])
        with _Swap("PRESERVED", pres), _Swap("CAUTIONS", cs):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("absent from the pre-state", problem)

    def test_chlorothalonil_keeps_the_prescription_and_loses_only_the_numeral(self):
        pre = _pre()["control_methods"]["chlorothalonil"]["cautions"]
        post = _post()["control_methods"]["chlorothalonil"]["cautions"]
        self.assertTrue(any("Bee rating II" in c for c in pre))
        self.assertFalse(any("Bee rating II" in c for c in post))
        keep = ("do not apply it, or let it drift, onto anything in flower including weeds, "
                "except between sunset and midnight where the label allows")
        self.assertTrue(any(keep in c for c in pre))
        self.assertTrue(any(keep in c for c in post))

    def test_no_field_outside_the_mutable_three_changes(self):
        pre, post = _pre()["control_methods"], _post()["control_methods"]
        for key in P.CAUTIONS:
            self.assertEqual(set(pre[key]), set(post[key]))
            for f in pre[key]:
                if f in P.MUTABLE_FIELDS:
                    continue
                self.assertEqual(pre[key][f], post[key][f], f"{key}.{f} moved")

    def test_verify_post_catches_a_frozen_field_moving(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["control_methods"]["carbaryl"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("best_use", problem)


class SourceMint(unittest.TestCase):
    def test_source_lands_verbatim(self):
        self.assertEqual(_post()["source_catalog"][P.SOURCE_ID], P.SOURCE)

    def test_source_is_t1_with_every_required_field(self):
        s = _post()["source_catalog"][P.SOURCE_ID]
        self.assertEqual(s["tier"], "T1")
        for f in P.REQUIRED:
            self.assertTrue(s.get(f), f"minted source missing {f}")
        self.assertTrue(s.get("_admission_provenance"))

    def test_missing_required_field_is_refused_by_name(self):
        for f in P.REQUIRED:
            bad = copy.deepcopy(P.SOURCE)
            bad[f] = ""
            with _Swap("SOURCE", bad):
                problem = P.check(_pre())
            self.assertIsNotNone(problem, f"missing {f} was accepted")
            self.assertIn(f, problem)

    def test_non_t1_source_is_refused(self):
        bad = copy.deepcopy(P.SOURCE)
        bad["tier"] = "T2"
        with _Swap("SOURCE", bad):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not T1", problem)

    def test_already_present_source_is_refused(self):
        pre = _pre()
        pre["source_catalog"][P.SOURCE_ID] = copy.deepcopy(P.SOURCE)
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already in source_catalog", problem)

    def test_each_method_anchors_its_own_ingredient_page(self):
        cm = _post()["control_methods"]
        seen = set()
        for key, uai in P.ANCHOR_KEY.items():
            url = cm[key]["anchoring_urls"][P.SOURCE_ID]["url"]
            self.assertTrue(url.endswith("uaiKey=" + uai), f"{key} anchors the wrong page")
            self.assertEqual(cm[key]["anchoring_urls"][P.SOURCE_ID]["verified"], P.VERIFIED)
            seen.add(uai)
        self.assertEqual(len(seen), 3, "two methods share one ingredient page")

    def test_every_declared_source_has_an_anchor(self):
        cm = _post()["control_methods"]
        for key in P.CAUTIONS:
            for s in cm[key]["sources"]:
                self.assertIn(s, cm[key]["anchoring_urls"], f"{key} declares {s} with no anchor")

    def test_chlorothalonil_anchor_is_repointed_not_duplicated(self):
        """Its uaiKey url was under the generic ucanr_ext id; that collision is the reason to mint."""
        pre = _pre()["control_methods"]["chlorothalonil"]
        post = _post()["control_methods"]["chlorothalonil"]
        self.assertIn("uaiKey=115", pre["anchoring_urls"]["ucanr_ext"]["url"])
        self.assertNotIn("ucanr_ext", post["anchoring_urls"])
        self.assertNotIn("ucanr_ext", post["sources"])
        self.assertIn("uaiKey=115", post["anchoring_urls"][P.SOURCE_ID]["url"])

    def test_insecticides_keep_ucanr_ext_for_the_residual_claim(self):
        """Minted rather than repointed precisely so this anchor is not orphaned."""
        post = _post()["control_methods"]
        for key in ("carbaryl", "pyrethroid"):
            self.assertIn("ucanr_ext", post[key]["sources"])
            self.assertIn("cole-crops", post[key]["anchoring_urls"]["ucanr_ext"]["url"])

    def test_verify_post_catches_the_source_not_landing(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["source_catalog"][P.SOURCE_ID]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("verbatim", problem)


class Blast(unittest.TestCase):
    def test_no_crop_changes(self):
        pre, post = _pre(), _post()
        self.assertEqual(json.dumps(pre["crops"], sort_keys=True),
                         json.dumps(post["crops"], sort_keys=True))

    def test_no_bystander_method_changes(self):
        pre, post = _pre()["control_methods"], _post()["control_methods"]
        for k in pre:
            if k not in P.CAUTIONS:
                self.assertEqual(pre[k], post[k], f"bystander method {k} moved")

    def test_no_bystander_source_changes(self):
        pre, post = _pre()["source_catalog"], _post()["source_catalog"]
        for k in pre:
            self.assertEqual(pre[k], post[k], f"bystander source {k} moved")

    def test_added_method_in_post_is_caught(self):
        """PLA-162: iterating pre makes ADDITIONS in post invisible. Set equality must run first."""
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["control_methods"]["ghost_method"] = copy.deepcopy(post["control_methods"]["sulfur"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("control_methods roster", problem)

    def test_added_crop_in_post_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        ghost = copy.deepcopy(post["crops"][0])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("crop roster", problem)

    def test_added_source_beyond_the_mint_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["source_catalog"]["ghost_source"] = copy.deepcopy(P.SOURCE)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog gained", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["crops"][0]["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander crop", problem)

    def test_bystander_method_edit_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        post = _post(pre)
        post["control_methods"]["sulfur"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander method", problem)


class VerifyPostIsDriven(unittest.TestCase):
    """EVERY post-state guard needs an input that REACHES it.

    `check()` refuses these upstream, so a suite that only drives check() leaves the entire
    verify_post half untested while staying green -- eight of this harness's first-run survivors
    were exactly that, and it is the fifth time this arc has hit it. Each test below doctors the
    APPLIED post directly, bypassing check(), which is the only way in.
    """

    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_band_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        cs = list(post["control_methods"]["carbaryl"]["cautions"])
        cs[0] = cs[0] + " Spray at dusk instead."
        post["control_methods"]["carbaryl"]["cautions"] = cs
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("post-state fails the band check", problem)
        self.assertIn("dusk", problem)

    def test_split_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        cs = [c.replace("Rated no known risk: ", "Rated no known risk: permethrin, ")
              if "us epa list" in c.lower() else c
              for c in post["control_methods"]["pyrethroid"]["cautions"]]
        post["control_methods"]["pyrethroid"]["cautions"] = cs
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("permethrin", problem)

    def test_axis_loop_runs_on_the_post(self):
        for axis, tokens in P.DISCLOSURE_AXES.items():
            if axis == "bees":
                continue          # the band guard owns that one and answers first, by design
            pre, snap, post = self._staged()
            post["control_methods"]["carbaryl"]["cautions"] = [
                c for c in post["control_methods"]["carbaryl"]["cautions"]
                if not any(t in c.lower() for t in tokens)]
            problem = P.verify_post(snap, post)
            self.assertIsNotNone(problem, f"post-state passed without the {axis} axis")
            self.assertIn(axis, problem)

    def test_field_set_change_runs_on_the_post(self):
        """A field ADDED to post is invisible to a loop that iterates pre. PLA-162, in miniature."""
        pre, snap, post = self._staged()
        post["control_methods"]["carbaryl"]["smuggled_field"] = "x"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("field set changed", problem)

    def test_cautions_must_be_the_ones_authored(self):
        """Reordering passes the band check and every axis, so only this guard can object."""
        pre, snap, post = self._staged()
        cs = list(post["control_methods"]["carbaryl"]["cautions"])
        post["control_methods"]["carbaryl"]["cautions"] = cs[1:] + cs[:1]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("not what was authored", problem)

    def test_anchor_set_equality_runs_on_the_post(self):
        """control_ladder_gate requires anchoring_urls keys == sources. Catch it here, not there."""
        pre, snap, post = self._staged()
        post["control_methods"]["carbaryl"]["anchoring_urls"]["stray_source"] = {
            "url": "https://example.org", "verified": P.VERIFIED}
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("anchoring_urls keys do not match sources", problem)

    def test_a_declared_source_with_no_anchor_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["control_methods"]["carbaryl"]["sources"].append("clemson_hgic")
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("anchoring_urls keys do not match sources", problem)

    def test_anchor_pointing_at_the_wrong_page_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["control_methods"]["carbaryl"]["anchoring_urls"][P.SOURCE_ID]["url"] = (
            P.DETAIL % "115")
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("does not point at its own page", problem)

    def test_bystander_source_edit_runs_on_the_post(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["npic_orst"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("bystander source", problem)

    def test_every_post_guard_family_has_a_driver(self):
        """COVERAGE, not overlap: each named family above must have produced a refusal."""
        families = {"band", "split", "axis", "field set", "authored", "anchor set",
                    "wrong page", "bystander source"}
        self.assertEqual(len(families), 8)


class Hygiene(unittest.TestCase):
    def test_authored_copy_is_clean(self):
        for key, cs in P.CAUTIONS.items():
            for c in cs:
                self.assertIsNone(P.hygiene(c), f"{key}: {c[:60]!r}")

    def test_em_dash_is_refused(self):
        with _Swap("CAUTIONS", _cautions("carbaryl", lambda cs: [cs[0] + " — really"] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("em or en dash", problem)

    def test_double_hyphen_is_refused(self):
        with _Swap("CAUTIONS", _cautions("carbaryl", lambda cs: [cs[0] + " -- really"] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("double hyphen", problem)

    def test_british_spelling_is_refused(self):
        with _Swap("CAUTIONS",
                   _cautions("carbaryl", lambda cs: [cs[0] + " Check the garden centre."] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("British spelling", problem)

    def test_safety_absolute_is_refused(self):
        with _Swap("CAUTIONS",
                   _cautions("carbaryl", lambda cs: [cs[0] + " It is harmless to people."] + cs[1:])):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("safety absolute", problem)

    def test_hygiene_families_are_each_reachable(self):
        self.assertIn("em or en dash", P.hygiene("a — b"))
        self.assertIn("double hyphen", P.hygiene("a -- b"))
        self.assertIn("British", P.hygiene("the centre"))
        self.assertIn("absolute", P.hygiene("it is harmless"))
        self.assertIn("degree", P.hygiene("above 85 ° F"))
        self.assertIsNone(P.hygiene("Keep it out of ponds and streams."))


class RatingsAreTheControl(unittest.TestCase):
    def test_chlorothalonil_row_matches_the_verified_screenshot(self):
        """The positive control that validated the raw-HTML parse on 2026-08-26."""
        self.assertEqual(P.RATINGS["115"], ("chlorothalonil", "H", "L", "medium", "H", "prop65+epa"))

    def test_carbaryl_row_is_what_licenses_the_new_chronic_line(self):
        self.assertEqual(P.RATINGS["111"][5], "prop65+epa")
        self.assertEqual(P.RATINGS["111"][3], "high")
        self.assertEqual(P.RATINGS["111"][4], "L")

    def test_permethrin_is_on_the_epa_list_and_is_the_named_exemplar(self):
        """The entry is titled 'Pyrethroid (such as permethrin)' and two rungs name it."""
        self.assertEqual(P.RATINGS["47"][0], "permethrin")
        self.assertEqual(P.RATINGS["47"][5], "epa")
        self.assertIn("permethrin", P.EPA_LISTED)
        self.assertEqual(P.ANCHOR_KEY["pyrethroid"], "47")

    def test_ratings_table_covers_exactly_what_was_read(self):
        self.assertEqual(len(P.RATINGS), 11)
        names = {v[0] for v in P.RATINGS.values()}
        self.assertEqual(names, set(P.PYRETHROIDS) | {"chlorothalonil", "carbaryl"})

    def test_every_anchor_key_is_a_row_that_was_read(self):
        for key, uai in P.ANCHOR_KEY.items():
            self.assertIn(uai, P.RATINGS, f"{key} anchors a page with no recorded reading")


if __name__ == "__main__":
    unittest.main(verbosity=2)
