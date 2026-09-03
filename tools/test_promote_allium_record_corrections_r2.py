#!/usr/bin/env python3
"""Guard suite for tools/promote_allium_record_corrections_r2.py. Base 80519a28.

REPLAY-PINNED. Evidence the guards are live: `MainWiringIsDriven` plus
tools/mutate_allium_record_corrections_r2_suite.py.

Two classes carry the arc's lesson that a harness proves a guard FIRES and never that it MEASURES
the right thing. `PositiveControl` asserts every retired claim is PRESENT in the pre-state and every
required claim is ABSENT there, so each check is a measurement rather than a restatement.
`MatcherBehaviour` asserts each predicate in BOTH directions on constructed text, including the
promote's own replacements: "two to three generations" must NOT trip the two-generation pattern,
"the soil around it" must NOT trip the soil-only-mechanism pattern, and "per local extension
guidance" must NOT trip the false-attribution device. A guard that rejects correct input is as much
a defect as one that accepts bad input, and no branch mutation finds it.
"""
import hashlib, json, os, re, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_allium_record_corrections_r2 as P  # noqa: E402

POST_SHA = "50ffedb00d680576d413a73e1ec7c2bcb1fd07db66bf9c09c017dce148a035f8"
LM, ALM = "Leek moth", "Allium leaf miner"
# The SIBLINGS spell it as one word. That difference is the adjudicated-but-deferred rename
# (PLA-448 s2) and this suite must not paper over it by reusing leek's name for them.
SIB = "Allium leafminer"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _applied():
    d = _pre()
    P.apply_to(d)
    return d


def _expect(case, sentence, fn):
    with case.assertRaises(SystemExit) as cm:
        fn()
    case.assertIn(sentence, str(cm.exception))


class _Patch:
    def __init__(self, n, v):
        self.n, self.v = n, v

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)

    def __exit__(self, *e):
        setattr(P, self.n, self.old)
        return False


class CleanRun(unittest.TestCase):
    def test_pre_state_is_the_pinned_shape(self):
        self.assertEqual(hashlib.sha256(P.serialize(_pre())).hexdigest(), P.BASE_SHA)

    def test_apply_produces_the_pinned_post_sha(self):
        self.assertEqual(hashlib.sha256(P.serialize(_applied())).hexdigest(), POST_SHA)

    def test_counts_are_pinned(self):
        self.assertEqual((len(P.PROSE), len(P.SOURCES)), (P.EXPECTED_PROSE, P.EXPECTED_SOURCE_SETS))
        self.assertEqual(len(P.TARGETS), 2)
        self.assertEqual(len(P.RETIRED), 6)
        self.assertEqual(len(P.REQUIRED), 7)
        self.assertEqual(sum(len(f) for _t, f, _p, _l in P.REQUIRED), 16)

    def test_the_roster_shape_is_unchanged(self):
        a, b = _pre(), _applied()
        self.assertEqual(len(a["crops"]), len(b["crops"]))
        self.assertEqual(sum(len(P.problems(c)) for c in a["crops"]),
                         sum(len(P.problems(c)) for c in b["crops"]))
        self.assertEqual(sum(len(P.problems(c)) for c in b["crops"]), 912)
        self.assertEqual(sum(len(p.get("control_ladder") or []) for c in b["crops"]
                             for p in P.problems(c)), 3243)

    def test_neither_target_carries_an_id_or_ladder_before_or_after(self):
        for d in (_pre(), _applied()):
            for slug, name in P.TARGETS:
                p = P.find_problem(d, slug, name)
                self.assertIsNone(p.get("id"))
                self.assertIsNone(p.get("control_ladder"))

    def test_severity_is_untouched(self):
        a, b = _pre(), _applied()
        for slug, name in P.TARGETS:
            self.assertEqual(P.find_problem(a, slug, name)["severity"],
                             P.find_problem(b, slug, name)["severity"])

    def test_the_problem_names_are_untouched(self):
        """PLA-448: no rename during the arc. 'Allium leaf miner' keeps its two-word name."""
        b = _applied()
        names = [p["name"] for p in P.problems(P.by_slug(b)["leek"])]
        self.assertIn("Allium leaf miner", names)
        self.assertIn("Leek moth", names)


class PositiveControl(unittest.TestCase):
    def test_every_retired_claim_is_present_in_the_pre_state(self):
        d = _pre()
        for (slug, name), still_present, label in P.RETIRED:
            p = P.find_problem(d, slug, name)
            self.assertTrue(any(isinstance(v, str) and still_present(v) for v in p.values()),
                            "%s/%s: %s was not present to begin with" % (slug, name, label))

    def test_every_required_claim_is_absent_from_every_declared_register_in_the_pre_state(self):
        d = _pre()
        for (slug, name), fields, pat, label in P.REQUIRED:
            p = P.find_problem(d, slug, name)
            for f in fields:
                self.assertIsNone(pat.search(p.get(f) or ""),
                                  "%s/%s/%s already carried %s" % (slug, name, f, label))

    def test_the_retired_guard_fails_on_the_untouched_pre_state(self):
        _expect(self, "still carries", lambda: P.check_retired_claims(_pre()))

    def test_the_required_guard_fails_on_the_untouched_pre_state(self):
        _expect(self, "lacks", lambda: P.check_required_claims(_pre()))

    def test_both_pass_after_the_promote(self):
        self.assertEqual(P.check_retired_claims(_applied()), 6)
        self.assertEqual(P.check_required_claims(_applied()), 16)

    def test_rhs_is_cited_before_and_by_neither_after(self):
        d = _pre()
        for slug, name in P.TARGETS:
            self.assertIn("rhs", P.find_problem(d, slug, name)["sources"])
        _expect(self, "still cites 'rhs': ['leek/Leek moth', 'leek/Allium leaf miner']",
                lambda: P.check_sources_retired(_pre()))
        P.check_sources_retired(_applied())

    def test_leek_disagreed_with_its_siblings_before_and_agrees_after(self):
        _expect(self, "leek/Allium leaf miner does not carry the siblings' 'September into October' "
                      "window", lambda: P.check_sibling_window_agreement(_pre()))
        self.assertEqual(P.check_sibling_window_agreement(_applied()), 2)

    def test_the_siblings_really_carry_the_phrase_in_the_pre_state(self):
        d = _pre()
        for slug, name in P.SIBLINGS:
            blob = " ".join(v for v in P.find_problem(d, slug, name).values() if isinstance(v, str))
            self.assertIn(P.SIBLING_PHRASE, blob)

    def test_taxa_are_named_before_and_after(self):
        self.assertEqual(P.check_taxa_survive(_pre()), 2)
        self.assertEqual(P.check_taxa_survive(_applied()), 2)


class MatcherBehaviour(unittest.TestCase):
    """THE MEASUREMENT, in both directions, on constructed text and on the promote's own output."""

    def _fn(self, label_fragment):
        hits = [fn for _t, fn, label in P.RETIRED if label_fragment in label]
        self.assertEqual(len(hits), 1, label_fragment)
        return hits[0]

    def test_two_generation_pattern_catches_two_and_passes_two_to_three(self):
        fn = self._fn("two-generation count")
        for t in ("two generations feed roughly May to June", "There are two waves, in late spring",
                  "Two generations a year.", "with two waves of damage"):
            self.assertTrue(fn(t), t)
        for t in ("two to three generations follow one another", "two or three rounds of caterpillars",
                  "New York records two to three generations a year", "larvae feed for two to three weeks"):
            self.assertFalse(fn(t), t)

    def test_uk_feeding_months_pattern(self):
        fn = self._fn("larval-feeding months")
        self.assertTrue(fn("feed roughly May to June and August to October."))
        self.assertTrue(fn("second flight August to October"))
        for t in ("Injury first shows in June and builds through September",
                  "flights around mid-April to mid-May, mid-June to mid-July and late July to late August"):
            self.assertFalse(fn(t), t)

    def test_moth_cover_during_pattern(self):
        # both problems declare a cover-during check under the same label; order is the moth's
        # first, the leafminer's second, and each is asserted on its own wording
        fns = [f for _t, f, label in P.RETIRED if label == "netting DURING the flights"]
        self.assertEqual(len(fns), 2)
        moth, alm = fns
        for t in ("Cover the crop with insect-proof mesh through the flight periods",
                  "fine insect netting during late spring and late summer when the moths are active"):
            self.assertTrue(moth(t), t)
        for t in ("have insect netting or row cover on before the overwintered moths emerge",
                  "leave it on for the season instead of taking it off between flights",
                  "left in place rather than lifted between flights"):
            self.assertFalse(moth(t), t)
        for t in ("Cover the crop with insect-proof mesh during the two flight periods",
                  "cover during the flight periods", "in fall when the flies are active"):
            self.assertTrue(alm(t), t)
        for t in ("put insect netting or row cover on before each flight begins",
                  "keep it on for the whole egg-laying period, roughly eight weeks",
                  "Cover the bed with fine insect netting or row cover before the flies show up"):
            self.assertFalse(alm(t), t)

    def test_rhs_window_pattern(self):
        fn = self._fn("RHS flight window")
        self.assertTrue(fn("active roughly March to April and again September to November"))
        for t in ("adults emerge from late March through April, sometimes into May",
                  "a second flight runs from about September into October"):
            self.assertFalse(fn(t), t)

    def test_soil_only_mechanism_pattern(self):
        fn = self._fn("soil-only overwintering mechanism")
        self.assertTrue(fn("since the flies emerge from pupae in the soil."))
        self.assertTrue(fn("Pupae in the soil hatch in spring"))
        for t in ("Pupae overwinter in the plant tissue or the soil around it",
                  "the pupae wait in old plant tissue or in the soil right around it",
                  "trap the flies coming up out of the ground"):
            self.assertFalse(fn(t), t)

    def test_required_patterns_in_both_directions(self):
        pats = {label: pat for _t, _f, pat, label in P.REQUIRED}
        self.assertTrue(pats["cover BEFORE the moths emerge"].search("on before the moths emerge"))
        self.assertIsNone(pats["cover BEFORE the moths emerge"].search("beforehand, cover it"))
        self.assertTrue(pats["the two-to-three generation count"].search("two to three generations"))
        self.assertTrue(pats["the two-to-three generation count"].search("two or three rounds"))
        self.assertIsNone(pats["the two-to-three generation count"].search("two to three weeks"))
        self.assertIsNone(pats["the two-to-three generation count"].search("two generations"))
        self.assertTrue(pats["the 50°F emergence anchor"].search("reach about 50°F,"))
        self.assertIsNone(pats["the 50°F emergence anchor"].search("reach about 50 °F"))
        self.assertTrue(pats["the UMass late-cover evidence"].search("two weeks after the flight"))
        self.assertIsNone(pats["the UMass late-cover evidence"].search("twelve weeks"))
        self.assertTrue(pats["the US spring window"].search("from late March through April"))
        self.assertIsNone(pats["the US spring window"].search("March to April"))

    def test_hygiene_false_attribution_device(self):
        for t in ("the guidance names row cover", "onion's guidance asks for rotation",
                  "shallot's own sourcing says so", "the guidance points at emergence"):
            self.assertIn("false-attribution device", P.hygiene(t), t)
        for t in ("treat persistent outbreaks per local extension guidance",
                  "ask your local extension office what to use",
                  "Where a spray is warranted, spinosad applied 7 to 10 days after a peak flight"):
            self.assertNotIn("false-attribution device", P.hygiene(t), t)

    def test_hygiene_british_and_absolutes(self):
        self.assertIn("british:\\bautumn\\b", P.hygiene("the autumn generation"))
        self.assertIn("absolute:never", P.hygiene("Never cover a bed"))
        self.assertIn("ladder vocabulary", P.hygiene("pair it with the rotation rung"))
        self.assertIn("spaced degF", P.hygiene("reach 50 °F"))
        self.assertEqual(P.hygiene("Fall leeks get hit hardest, reach 50°F"), [])

    def test_the_promotes_own_replacements_pass_every_predicate(self):
        for (slug, name, _f), (_before, after) in P.PROSE.items():
            self.assertEqual(P.hygiene(after), [], after[:60])
            for (ts, tn), fn, label in P.RETIRED:
                if (ts, tn) == (slug, name):
                    self.assertFalse(fn(after), "%s trips %r: %s" % (name, label, after[:60]))


class Pins(unittest.TestCase):
    def test_stale_prose_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "leek", LM)["cause_beginner"] = "moved on"
        _expect(self, "leek/Leek moth/cause_beginner does not match its pinned text; the record moved",
                lambda: P.check_pins(d))

    def test_a_target_outside_the_declared_set_refuses(self):
        d = _pre()
        pr = dict(P.PROSE)
        pr[("leek", "Leek rust", "cause_beginner")] = ("x", "y")
        with _Patch("PROSE", pr), _Patch("EXPECTED_PROSE", len(pr)):
            _expect(self, "leek/Leek rust is not a declared target", lambda: P.check_pins(d))

    def test_table_sizes_are_asserted(self):
        d = _pre()
        with _Patch("EXPECTED_PROSE", 11):
            _expect(self, "edit tables hold 12/2, expected 11/2", lambda: P.check_pins(d))

    def test_an_identical_replacement_refuses(self):
        d = _pre()
        k = ("leek", LM, "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][0])
        with _Patch("PROSE", pr):
            _expect(self, "leek/Leek moth/cause_beginner replacement is identical",
                    lambda: P.check_pins(d))

    def test_hygiene_on_the_replacement_refuses(self):
        d = _pre()
        k = ("leek", LM, "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " Netting completely stops it.")
        with _Patch("PROSE", pr):
            _expect(self, "leek/Leek moth/cause_beginner replacement: absolute:completely",
                    lambda: P.check_pins(d))

    def test_a_british_replacement_refuses(self):
        d = _pre()
        k = ("leek", ALM, "cause_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " Worst in autumn.")
        with _Patch("PROSE", pr):
            _expect(self, "leek/Allium leaf miner/cause_beginner replacement: british:",
                    lambda: P.check_pins(d))

    def test_the_false_attribution_device_refuses(self):
        d = _pre()
        k = ("leek", ALM, "management_beginner")
        pr = dict(P.PROSE)
        pr[k] = (P.PROSE[k][0], P.PROSE[k][1] + " The guidance names February.")
        with _Patch("PROSE", pr):
            _expect(self, "management_beginner replacement: false-attribution device",
                    lambda: P.check_pins(d))

    def test_a_stale_source_pin_refuses(self):
        d = _pre()
        P.find_problem(d, "leek", LM)["sources"] = ["rhs", "umd_ext"]
        _expect(self, "leek/Leek moth sources are ['rhs', 'umd_ext'], pinned ['rhs']",
                lambda: P.check_pins(d))

    def test_citing_an_id_not_in_the_catalog_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("leek", LM)] = (["rhs"], ["cornell_ext", "uvm_ext"],
                             {"cornell_ext": "https://x", "uvm_ext": "https://y"})
        with _Patch("SOURCES", src):
            _expect(self, "leek/Leek moth cites 'uvm_ext', which is not in source_catalog",
                    lambda: P.check_pins(d))

    def test_an_anchor_outside_the_new_source_list_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("leek", LM)] = (["rhs"], ["cornell_ext", "unh_ext"],
                             {"cornell_ext": "https://x", "unh_ext": "https://y", "uc_ipm": "https://z"})
        with _Patch("SOURCES", src):
            _expect(self, "leek/Leek moth anchors 'uc_ipm' which is not in its new source list",
                    lambda: P.check_pins(d))

    def test_a_cited_id_without_a_document_anchor_refuses(self):
        """A bare catalog root on a node is the citation-cleanup defect class."""
        d = _pre()
        src = dict(P.SOURCES)
        src[("leek", LM)] = (["rhs"], ["cornell_ext", "unh_ext"], {"cornell_ext": "https://x"})
        with _Patch("SOURCES", src):
            _expect(self, "leek/Leek moth cites 'unh_ext' without a document anchor",
                    lambda: P.check_pins(d))

    def test_a_duplicate_in_the_new_source_list_refuses(self):
        d = _pre()
        src = dict(P.SOURCES)
        src[("leek", LM)] = (["rhs"], ["cornell_ext", "cornell_ext"], {"cornell_ext": "https://x"})
        with _Patch("SOURCES", src):
            _expect(self, "leek/Leek moth new source list is empty or has duplicates",
                    lambda: P.check_pins(d))

    def test_a_target_with_prose_but_no_source_set_refuses(self):
        d = _pre()
        src = {k: v for k, v in P.SOURCES.items() if k != ("leek", ALM)}
        with _Patch("SOURCES", src), _Patch("EXPECTED_SOURCE_SETS", 1):
            _expect(self, "leek/Allium leaf miner is declared but not fully edited",
                    lambda: P.check_pins(d))

    def test_an_ambiguous_problem_name_refuses(self):
        d = _pre()
        P.by_slug(d)["leek"]["pests"].append({"name": "Leek moth"})
        _expect(self, "leek has 2 problems named 'Leek moth', expected exactly 1",
                lambda: P.check_pins(d))


class RetiredClaimsPerBranch(unittest.TestCase):
    """One driver per retired claim on the APPLIED state, each isolating its own predicate."""

    def _reintroduce(self, name, field, text):
        d = _applied()
        P.find_problem(d, "leek", name)[field] = text
        return d

    def test_the_uk_feeding_months_coming_back(self):
        d = self._reintroduce(LM, "identification_beginner", "Caterpillars feed May to June.")
        _expect(self, "leek/Leek moth/identification_beginner still carries the UK larval-feeding "
                      "months relabelled as flight periods", lambda: P.check_retired_claims(d))

    def test_the_two_generation_count_coming_back(self):
        d = self._reintroduce(LM, "cause_beginner", "There are two generations a year.")
        _expect(self, "still carries a two-generation count (the US has two to three)",
                lambda: P.check_retired_claims(d))

    def test_moth_netting_during_coming_back(self):
        d = self._reintroduce(LM, "management_beginner", "Net the bed when the moths are active.")
        _expect(self, "leek/Leek moth/management_beginner still carries netting DURING the flights",
                lambda: P.check_retired_claims(d))

    def test_the_rhs_window_coming_back(self):
        d = self._reintroduce(ALM, "cause_seasoned", "Active September to November.")
        _expect(self, "leek/Allium leaf miner/cause_seasoned still carries the RHS flight window",
                lambda: P.check_retired_claims(d))

    def test_leafminer_netting_during_coming_back(self):
        d = self._reintroduce(ALM, "management_seasoned", "Cover during the two flight periods.")
        _expect(self, "leek/Allium leaf miner/management_seasoned still carries netting DURING the "
                      "flights", lambda: P.check_retired_claims(d))

    def test_the_soil_only_mechanism_coming_back(self):
        d = self._reintroduce(ALM, "cause_beginner", "The flies emerge from pupae in the soil.")
        _expect(self, "still carries the soil-only overwintering mechanism",
                lambda: P.check_retired_claims(d))

    def test_a_claim_surviving_in_a_SIBLING_field_is_caught(self):
        """The whole point of scanning the problem rather than the edited field."""
        d = self._reintroduce(LM, "identification_seasoned",
                              "Damage runs August to October on late plantings.")
        _expect(self, "leek/Leek moth/identification_seasoned still carries",
                lambda: P.check_retired_claims(d))


class RequiredClaimsPerBranch(unittest.TestCase):
    def _strip(self, name, field, pat):
        d = _applied()
        p = P.find_problem(d, "leek", name)
        p[field] = pat.sub("later", p[field])
        return d

    def test_each_required_claim_is_checked_in_each_declared_register(self):
        for (slug, name), fields, pat, label in P.REQUIRED:
            for f in fields:
                d = self._strip(name, f, pat)
                _expect(self, "%s/%s/%s lacks %s" % (slug, name, f, label),
                        lambda d=d: P.check_required_claims(d))

    def test_a_claim_present_in_the_seasoned_register_only_is_refused(self):
        """The beginner register is the one a novice acts on."""
        d = _applied()
        p = P.find_problem(d, "leek", ALM)
        p["management_beginner"] = p["management_beginner"].replace("before", "once")
        _expect(self, "leek/Allium leaf miner/management_beginner lacks cover BEFORE the flight",
                lambda: P.check_required_claims(d))
        self.assertIn("before", p["management_seasoned"])


class TaxaSiblingsSources(unittest.TestCase):
    def test_dropping_the_leafminer_binomial_refuses(self):
        d = _applied()
        p = P.find_problem(d, "leek", ALM)
        p["cause_seasoned"] = p["cause_seasoned"].replace("Phytomyza gymnostoma", "a fly")
        _expect(self, "leek/Allium leaf miner no longer names Phytomyza gymnostoma",
                lambda: P.check_taxa_survive(d))

    def test_dropping_the_moth_binomial_refuses(self):
        d = _applied()
        p = P.find_problem(d, "leek", LM)
        p["cause_seasoned"] = p["cause_seasoned"].replace("Acrolepiopsis assectella", "a moth")
        _expect(self, "leek/Leek moth no longer names Acrolepiopsis assectella",
                lambda: P.check_taxa_survive(d))

    def test_a_sibling_losing_the_phrase_refuses_rather_than_passing(self):
        d = _applied()
        p = P.find_problem(d, "shallot", SIB)
        for k, v in list(p.items()):
            if isinstance(v, str):
                p[k] = v.replace(P.SIBLING_PHRASE, "in the fall")
        _expect(self, "sibling shallot/Allium leafminer no longer says 'September into October'; "
                      "the agreement check has nothing to agree with",
                lambda: P.check_sibling_window_agreement(d))

    def test_leek_losing_the_phrase_refuses(self):
        d = _applied()
        p = P.find_problem(d, "leek", ALM)
        for k, v in list(p.items()):
            if isinstance(v, str):
                p[k] = v.replace(P.SIBLING_PHRASE, "in the fall")
        _expect(self, "leek/Allium leaf miner does not carry the siblings' 'September into October' "
                      "window", lambda: P.check_sibling_window_agreement(d))

    def test_rhs_surviving_only_in_anchoring_urls_is_caught(self):
        d = _applied()
        P.find_problem(d, "leek", ALM)["anchoring_urls"]["rhs"] = {
            "url": "https://www.rhs.org.uk/biodiversity/allium-leaf-miner", "verified": "2026-06-29"}
        _expect(self, "still cites 'rhs': ['leek/Allium leaf miner']",
                lambda: P.check_sources_retired(d))


class BlastRadius(unittest.TestCase):
    def _post(self):
        d = _pre()
        pre = P.snapshot(d)
        P.apply_to(d)
        return pre, d

    def test_clean_apply_changes_the_expected_leaves(self):
        pre, d = self._post()
        self.assertEqual(P.verify_post(pre, d), 17)

    def test_a_key_added_outside_sources_or_anchors_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", LM)["note"] = "x"
        _expect(self, "added or dropped outside sources/anchoring_urls", lambda: P.verify_post(pre, d))

    def test_a_source_added_on_a_NON_target_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "chives", SIB)["sources"].append("uc_ipm")
        _expect(self, "added or dropped outside the declared targets", lambda: P.verify_post(pre, d))

    def test_an_extra_prose_change_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", LM)["identification_beginner"] += " Extra."
        _expect(self, "leek/Leek moth/identification_beginner did not receive its replacement",
                lambda: P.verify_post(pre, d))

    def test_a_change_on_a_bystander_crop_refuses(self):
        """Driven on a NON-prose field; a bystander prose change trips the count check first."""
        pre, d = self._post()
        P.find_problem(d, "shallot", SIB)["severity"] = "low"
        _expect(self, "leaves changed outside the declared targets: [('shallot', 'Allium leafminer')]",
                lambda: P.verify_post(pre, d))

    def test_a_bystander_change_in_a_PROSE_field_is_caught_by_the_count(self):
        pre, d = self._post()
        P.find_problem(d, "chives", SIB)["cause_beginner"] = "changed"
        _expect(self, "13 prose leaves changed, expected 12", lambda: P.verify_post(pre, d))

    def test_a_severity_change_on_a_target_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", LM)["severity"] = "low"
        _expect(self, "leek/Leek moth severity changed; not in scope", lambda: P.verify_post(pre, d))

    def test_the_source_list_ORDER_is_pinned_not_just_the_set(self):
        pre, d = self._post()
        p = P.find_problem(d, "leek", ALM)
        p["sources"] = list(reversed(p["sources"]))
        _expect(self, "sources are ['umass_ext', 'cornell_ext', 'umd_ext'], expected "
                      "['umd_ext', 'cornell_ext', 'umass_ext']", lambda: P.verify_post(pre, d))

    def test_anchor_keys_must_match_the_source_list(self):
        pre, d = self._post()
        P.find_problem(d, "leek", LM)["anchoring_urls"].pop("unh_ext")
        _expect(self, "leek/Leek moth anchoring_urls keys ['cornell_ext'] do not match its sources",
                lambda: P.verify_post(pre, d))

    def test_a_wrong_anchor_url_refuses(self):
        pre, d = self._post()
        P.find_problem(d, "leek", ALM)["anchoring_urls"]["umd_ext"]["url"] = \
            "https://extension.umd.edu/resource/growing-leeks-home-garden"
        _expect(self, "leek/Allium leaf miner anchor umd_ext is", lambda: P.verify_post(pre, d))

    def test_the_prose_change_count_is_pinned(self):
        pre, d = self._post()
        k = ("leek", ALM, "cause_seasoned")
        P.find_problem(d, *k[:2])[k[2]] = P.PROSE[k][0]
        _expect(self, "11 prose leaves changed, expected 12", lambda: P.verify_post(pre, d))

    def test_the_umd_anchor_is_repointed_not_merely_kept(self):
        """umd_ext stays in the list; its URL must move off the leek page that has no content."""
        pre, d = self._post()
        P.verify_post(pre, d)
        au = P.find_problem(d, "leek", ALM)["anchoring_urls"]["umd_ext"]
        self.assertEqual(au["url"], "https://extension.umd.edu/resource/allium-onion-leafminer")
        self.assertEqual(au["verified"], P.VERIFIED)
        self.assertEqual(P.find_problem(_pre(), "leek", ALM)["anchoring_urls"]["umd_ext"]["url"],
                         "https://extension.umd.edu/resource/growing-leeks-home-garden")


class CatalogUntouched(unittest.TestCase):
    def setUp(self):
        d = _pre()
        self.cm, self.sc = P.serialize(d["control_methods"]), P.serialize(d["source_catalog"])

    def test_control_methods_change_refuses(self):
        d = _pre()
        d["control_methods"]["crop_rotation"]["tier"] = "physical"
        _expect(self, "control_methods changed; this promote mints nothing",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_source_catalog_change_refuses(self):
        d = _pre()
        d["source_catalog"]["unh_ext"]["name"] = "x"
        _expect(self, "source_catalog changed; every id cited here already exists",
                lambda: P.check_catalog_untouched(self.cm, self.sc, d))

    def test_every_id_this_promote_cites_already_exists(self):
        sc = _pre()["source_catalog"]
        for (_s, _n), (_b, after, _a) in P.SOURCES.items():
            for sid in after:
                self.assertIn(sid, sc)

    def test_the_real_promote_touches_neither(self):
        P.check_catalog_untouched(self.cm, self.sc, _applied())


class MainWiringIsDriven(unittest.TestCase):
    def test_apply_to_routes_through_check_pins(self):
        import inspect
        self.assertIn("check_pins(", inspect.getsource(P.apply_to))

    def test_main_runs_every_post_check(self):
        import inspect
        src = inspect.getsource(P.main)
        for frag in ("verify_post(pre, data)", "check_catalog_untouched(before_cm, before_sc, data)",
                     "check_retired_claims(data)", "check_required_claims(data)",
                     "check_taxa_survive(data)", "check_sources_retired(data)",
                     "check_sibling_window_agreement(data)", "if sha != expect:"):
            self.assertIn(frag, src)

    def test_end_to_end_through_main(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("post  SHA           : " + POST_SHA, r.stdout)
            self.assertIn("retired claims gone : 6/6", r.stdout)
            self.assertIn("required claims in  : 16 registers", r.stdout)
            self.assertIn("taxa survive        : 2/2", r.stdout)
            self.assertIn("sibling window      : leek agrees with chives + shallot in 2 fields",
                          r.stdout)
            self.assertIn("dry run; pass --apply to write", r.stdout)
        finally:
            os.unlink(path)

    def test_the_canonical_flag_form_is_accepted(self):
        """promote_fixture's CHAIN replay passes `--canonical PATH`; r3's suite rebuilds its base by
        replaying this promote until r2 is committed and pinned."""
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, "--canonical", path,
                                "--expect-sha", P.BASE_SHA], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("post  SHA           : " + POST_SHA, r.stdout)
        finally:
            os.unlink(path)

    def test_a_wrong_base_sha_is_refused(self):
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            fh.write(P.serialize({"crops": [], "control_methods": {}, "source_catalog": {}}))
            path = fh.name
        try:
            r = subprocess.run([sys.executable, P.__file__, path], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED: base SHA", r.stdout + r.stderr)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=1)
