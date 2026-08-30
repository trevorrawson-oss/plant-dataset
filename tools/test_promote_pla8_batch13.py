#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch13.py. Base ee0f54a3 (the disease_escape_sowing
backfill's output, a commit).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.
Every driver asserts its branch's ONE message; a hedged OR over two messages is how a masked
guard passes review (twice caught by the trap-cropping harness).
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch13 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "b6d366114461fe470aa07c48f18f83ade9e584b86a70898fd12ab5651884088d"

# FROZEN LITERALS -- restated, never derived from P.
CROPS = ("cayenne-pepper", "habanero", "banana-pepper", "bell-pepper", "eggplant")
TAXON = {"bacterial-spot": "bacterial-leaf-spot",
         "southern-bacterial-wilt": "bacterial-wilt"}
TRAP_OK = (("cayenne-pepper", "flea-beetles"), ("habanero", "flea-beetles"),
           ("eggplant", "flea-beetles"))
NEW_IDS = ("colorado-potato-beetle", "eggplant-lace-bug", "phomopsis-blight",
           "southern-blight", "southern-bacterial-wilt")


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


def _crop(data, slug):
    return next(c for c in data["crops"] if c.get("slug") == slug)


def _prob(data, slug, pid):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError(f"{slug}/{pid} not found")


class _Patch:
    def __init__(self, name, value):
        self.n, self.v = name, value

    def __enter__(self):
        self.old = getattr(P, self.n)
        setattr(P, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(P, self.n, self.old)
        return False


def _staged_with(mutator):
    batch = P.staged()
    mutator(batch)
    return lambda: batch


def _sprob(batch, slug, pid):
    for fam in ("pests", "diseases"):
        for p in batch[slug].get(fam) or []:
            if p.get("id") == pid:
                return p
    raise AssertionError(f"staged {slug}/{pid} not found")


_UNIQ = [0]


def _rung(m):
    """Notes unique per call, so an injected rung never trips the echo/duplicate scans before
    the guard the test is actually driving."""
    _UNIQ[0] += 1
    n = _UNIQ[0]
    return {"method": m, "note_beginner": f"injected beginner {_UNIQ[0]}",
            "note_seasoned": f"injected seasoned {n} differs"}


class VerifyPostIsDriven(unittest.TestCase):
    """One driver per branch of verify_post, each a plain post-state doctoring."""

    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_an_emptied_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "eggplant", "flea-beetles")["control_ladder"] = []
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no ladder after promote", out)

    def test_an_unearned_trap_rung_is_caught(self):
        snap, post = self._staged()
        _prob(post, "bell-pepper", "flea-beetles")["control_ladder"].insert(1, _rung("trap_cropping"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("trap_cropping unearned", out)

    def test_bt_on_the_potato_beetle_is_caught(self):
        """The tenebrionis ruling: the catalog's bt key means the kurstaki caterpillar spray."""
        snap, post = self._staged()
        _prob(post, "eggplant", "colorado-potato-beetle")["control_ladder"].insert(2, _rung("bt"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("outside the caterpillar ladders", out)

    def test_tillage_returning_to_cutworms_is_caught(self):
        snap, post = self._staged()
        _prob(post, "cayenne-pepper", "cutworms")["control_ladder"].insert(1, _rung("off_season_tillage"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("pre-plant cultivation as tillage", out)

    def test_a_forbidden_method_is_caught(self):
        snap, post = self._staged()
        _prob(post, "habanero", "flea-beetles")["control_ladder"].append(_rung("disease_escape_sowing"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped forbidden", out)

    def test_a_material_on_a_no_material_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "bell-pepper", "anthracnose")["control_ladder"].append(_rung("copper_fungicide"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("which its prose rules out", out)

    def test_a_dropped_taxon_id_is_caught(self):
        """All four peppers carry bacterial-spot, so the branch fires only when every one is
        renamed; its ladder holds copper, so the NO_MATERIAL lookup cannot answer first (the
        southern-bacterial-wilt id CAN'T drive this branch for exactly that reason)."""
        snap, post = self._staged()
        for slug in ("cayenne-pepper", "habanero", "banana-pepper", "bell-pepper"):
            _prob(post, slug, "bacterial-spot")["id"] = "renamed-away"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not ship", out)

    def test_the_wrong_organism_id_shipping_is_caught(self):
        snap, post = self._staged()
        _prob(post, "cayenne-pepper", "bacterial-spot")["id"] = "bacterial-leaf-spot"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("the wrong organism", out)

    def test_a_lost_weevil_weed_rung_is_caught(self):
        snap, post = self._staged()
        p = _prob(post, "banana-pepper", "pepper-weevil")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "weed_host_control"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("weed_host_control rung", out)

    def test_a_dropped_bystander_crop_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "tomatillo"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_an_edited_bystander_crop_is_caught(self):
        snap, post = self._staged()
        _crop(post, "tomatillo")["name"] = "MUTATED"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

    def test_a_touched_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["bt"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints and widens NOTHING", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["ncsu_ext"]["accessed"] = "2099-01"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("touches no source", out)

    def test_verify_post_is_clean_on_the_real_apply(self):
        snap, post = self._staged()
        self.assertIsNone(P.verify_post(snap, post))


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

    def test_check_passes_on_the_pinned_base(self):
        self.assertIsNone(P.check(_pre()))

    def test_check_REFUSES_running_over_its_own_output(self):
        out = P.check(_post())
        self.assertIsNotNone(out)
        self.assertIn("already laddered", out)

    def test_roster_grows_to_58_laddered(self):
        post = _post()
        n = sum(1 for c in post["crops"]
                if any("control_ladder" in p for fam in ("pests", "diseases")
                       for p in c.get(fam) or []))
        self.assertEqual(n, 58)


class TaxonRulings(unittest.TestCase):
    def test_the_frozen_refusals_match(self):
        self.assertEqual({k: v[0] for k, v in P.TAXON_REFUSED.items()}, TAXON)

    def test_the_wrong_strings_resolve_to_OTHER_organisms_on_the_roster(self):
        """The refusals protect against real collisions: both wrong strings exist on the roster
        and belong to different organisms (cilantro's Pseudomonas; the cucumbers' Erwinia)."""
        pre = _pre()
        ids = {}
        for c in pre["crops"]:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if p.get("id"):
                        ids.setdefault(p["id"], []).append(c.get("slug"))
        self.assertIn("bacterial-leaf-spot", ids)
        self.assertIn("cilantro-coriander", ids["bacterial-leaf-spot"])
        self.assertIn("bacterial-wilt", ids)
        self.assertNotIn("eggplant", ids["bacterial-wilt"])

    def test_check_REFUSES_the_wrong_bacterial_id(self):
        """The wrong-string-PRESENT branch, driven with the right string still shipping: a
        different problem is given the Pseudomonas id (with the convention table patched to let
        it through), so only the taxon refusal can object."""
        def m(batch):
            for slug in ("cayenne-pepper", "habanero"):
                _sprob(batch, slug, "cutworms")["id"] = "bacterial-leaf-spot"
        table = dict(P.ID_CONVENTION)
        table["Cutworms"] = "bacterial-leaf-spot"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("WRONG ORGANISM", out)

    def test_check_REFUSES_the_erwinia_reuse_on_eggplant(self):
        def m(batch):
            for slug in ("cayenne-pepper", "habanero"):
                _sprob(batch, slug, "cutworms")["id"] = "bacterial-wilt"
        table = dict(P.ID_CONVENTION)
        table["Cutworms"] = "bacterial-wilt"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("WRONG ORGANISM", out)

    def test_check_REFUSES_a_batch_that_loses_a_taxon_ruled_id(self):
        """The right-string-MISSING branch: rename the eggplant id to something inert (table
        patched along), and check must say the ruling requires it."""
        def m(batch):
            _sprob(batch, "eggplant", "southern-bacterial-wilt")["id"] = "ralstonia-wilt"
        table = dict(P.ID_CONVENTION)
        table["Bacterial wilt"] = "ralstonia-wilt"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("requires id 'southern-bacterial-wilt'", out)

    def test_check_REFUSES_an_id_off_the_convention_table(self):
        def m(batch):
            _sprob(batch, "habanero", "hornworms")["id"] = "tomato-tobacco-hornworms"
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never re-derived from the name", out)

    def test_every_reused_id_resolves_on_the_roster(self):
        pre = _pre()
        base = P.roster_ids(pre)
        for pid in P.REUSED_IDS:
            self.assertIn(pid, base, pid)

    def test_every_new_id_is_absent_from_the_roster(self):
        pre = _pre()
        base = P.roster_ids(pre)
        for pid in NEW_IDS:
            self.assertNotIn(pid, base, pid)

    def test_check_REFUSES_a_reuse_that_resolves_nowhere(self):
        """A declared REUSE whose string is missing from the roster is a mint wearing a
        reuse's name; doctor the pre so no crop carries spider-mites."""
        pre = _pre()
        for c in pre["crops"]:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if p.get("id") == "spider-mites":
                        p["id"] = "spider-mites-renamed"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint wearing a reuse's name", out)

    def test_check_REFUSES_a_new_id_already_taken(self):
        pre = _pre()
        # plant a fake 'southern-blight' problem on a bystander crop in the pre-state
        _crop(pre, "tomatillo").setdefault("diseases", []).append(
            {"id": "southern-blight", "name": "Planted collision"})
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("listed as new to this base", out)


class Alignment(unittest.TestCase):
    """Identical advice prose + same id <-> identical ladder, both directions."""

    def test_the_correspondence_holds_on_the_real_batch(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_alignment(by, P.staged()))

    def test_the_hornworm_text_is_one_set_across_all_five(self):
        batch = P.staged()
        first = P.ladder_key(_sprob(batch, "cayenne-pepper", "hornworms"))
        for slug in CROPS[1:]:
            self.assertEqual(P.ladder_key(_sprob(batch, slug, "hornworms")), first, slug)

    def test_the_eggplant_flea_beetle_near_twin_keeps_its_own_text(self):
        """One word apart ('outgrow' vs 'can outgrow'): NOT identical prose, so NOT one text
        set. This is the pair a sloppy propagation would collapse."""
        batch = P.staged()
        self.assertNotEqual(P.ladder_key(_sprob(batch, "cayenne-pepper", "flea-beetles")),
                            P.ladder_key(_sprob(batch, "eggplant", "flea-beetles")))

    def test_check_REFUSES_a_fork_on_identical_prose(self):
        def m(batch):
            _sprob(batch, "habanero", "blossom-end-rot")["control_ladder"][0]["note_beginner"] += " More."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("identical prose ships one text set", out)

    def test_check_REFUSES_a_ladder_copied_across_differing_prose(self):
        def m(batch):
            donor = _sprob(batch, "cayenne-pepper", "flea-beetles")
            _sprob(batch, "eggplant", "flea-beetles")["control_ladder"] = copy.deepcopy(
                donor["control_ladder"])
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("given the other's source", out)


class TrapContract(unittest.TestCase):
    def test_exactly_the_three_divert_carriers_hold_the_rung(self):
        batch = P.staged()
        carriers = []
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                if any(r["method"] == "trap_cropping" for r in p.get("control_ladder") or []):
                    carriers.append((slug, p["id"]))
        self.assertEqual(sorted(carriers), sorted(TRAP_OK))

    def test_no_divert_rung_attributes_the_removal_to_the_crop(self):
        batch = P.staged()
        for slug, pid in TRAP_OK:
            p = _sprob(batch, slug, pid)
            r = next(r for r in p["control_ladder"] if r["method"] == "trap_cropping")
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            self.assertNotIn("this crop's guidance", blob, (slug, pid))
            self.assertIn("cautions", blob, (slug, pid))

    def test_check_REFUSES_an_attributing_divert_rung(self):
        def m(batch):
            p = _sprob(batch, "eggplant", "flea-beetles")
            r = next(r for r in p["control_ladder"] if r["method"] == "trap_cropping")
            r["note_seasoned"] += " Destroying the loaded patch is this crop's guidance."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("stops short of", out)

    def test_check_REFUSES_a_divert_rung_without_the_cautions_pointer(self):
        def m(batch):
            p = _sprob(batch, "cayenne-pepper", "flea-beetles")
            r = next(r for r in p["control_ladder"] if r["method"] == "trap_cropping")
            r["note_beginner"] = r["note_beginner"].replace("cautions", "notes")
            r["note_seasoned"] = r["note_seasoned"].replace("cautions", "notes")
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("removal deadline", out)

    def test_check_REFUSES_an_unearned_trap_rung(self):
        def m(batch):
            _sprob(batch, "bell-pepper", "flea-beetles")["control_ladder"].insert(
                1, _rung("trap_cropping"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("whose prose names a trap planting earn", out)


class ReadRulings(unittest.TestCase):
    def test_check_REFUSES_tillage_on_cutworms(self):
        def m(batch):
            _sprob(batch, "habanero", "cutworms")["control_ladder"].insert(
                1, _rung("off_season_tillage"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("PRE-PLANT", out)

    def test_check_REFUSES_a_hornworm_ladder_without_tillage(self):
        def m(batch):
            p = _sprob(batch, "eggplant", "hornworms")
            p["control_ladder"] = [r for r in p["control_ladder"]
                                   if r["method"] != "off_season_tillage"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("fall tillage of pupae", out)

    def test_check_REFUSES_a_weevil_ladder_without_the_weed_rung(self):
        def m(batch):
            p = _sprob(batch, "cayenne-pepper", "pepper-weevil")
            p["control_ladder"] = [r for r in p["control_ladder"]
                                   if r["method"] != "weed_host_control"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("that method's action, not sanitation's", out)

    def test_check_REFUSES_weevil_sanitation_reabsorbing_the_weeds(self):
        def m(batch):
            p = _sprob(batch, "bell-pepper", "pepper-weevil")
            r = next(r for r in p["control_ladder"] if r["method"] == "garden_sanitation")
            r["note_beginner"] += " Pull the nearby nightshade weeds too."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("re-absorbed the nightshade weeds", out)

    def test_check_REFUSES_copper_on_the_unnamed_fungicide_anthracnose(self):
        """banana/bell anthracnose prose says 'a labeled fungicide', unnamed; naming copper
        would be a product claim the prose does not make."""
        def m(batch):
            _sprob(batch, "banana-pepper", "anthracnose")["control_ladder"].append(
                _rung("copper_fungicide"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("names no such material", out)

    def test_copper_IS_earned_where_the_prose_names_it(self):
        batch = P.staged()
        for slug in ("cayenne-pepper", "habanero", "banana-pepper", "bell-pepper"):
            ms = [r["method"] for r in _sprob(batch, slug, "bacterial-spot")["control_ladder"]]
            self.assertIn("copper_fungicide", ms, slug)
        for slug in ("cayenne-pepper", "habanero"):
            ms = [r["method"] for r in _sprob(batch, slug, "anthracnose")["control_ladder"]]
            self.assertIn("copper_fungicide", ms, slug)
        for slug in ("banana-pepper", "bell-pepper"):
            ms = [r["method"] for r in _sprob(batch, slug, "anthracnose")["control_ladder"]]
            self.assertNotIn("copper_fungicide", ms, slug)

    def test_check_REFUSES_bt_on_the_potato_beetle(self):
        def m(batch):
            _sprob(batch, "eggplant", "colorado-potato-beetle")["control_ladder"].insert(
                3, _rung("bt"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tenebrionis", out)

    def test_check_REFUSES_a_timing_or_escape_key(self):
        def m(batch):
            _sprob(batch, "bell-pepper", "flea-beetles")["control_ladder"].insert(
                0, _rung("planting_time_avoidance"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("transplant VIGOR", out)


class Echo(unittest.TestCase):
    def test_no_note_echoes_a_shipped_rung(self):
        pre = _pre()
        self.assertIsNone(P.check_no_shipped_echo(P.staged(), pre))

    def test_the_echo_scan_is_not_vacuous(self):
        """Plant a real shipped note into a staged rung and the scan must see it."""
        pre = _pre()
        donor = _prob(pre, "jalapeno", "aphids")
        shipped = donor["control_ladder"][0]["note_beginner"]

        def m(batch):
            _sprob(batch, "eggplant", "aphids")["control_ladder"][0]["note_beginner"] = shipped
        with _Patch("staged", _staged_with(m)):
            out = P.check_no_shipped_echo(P.staged(), pre)
        self.assertIsNotNone(out)
        self.assertIn("byte-identical to the shipped", out)

    def test_the_sentence_half_of_the_echo_scan_is_not_vacuous(self):
        """A shipped SENTENCE appended inside an otherwise-new note must also redden, or the
        10-word threshold could be silently raised without anything noticing."""
        pre = _pre()
        donor = _prob(pre, "jalapeno", "aphids")
        long_sent = next(s for r in donor["control_ladder"]
                         for s in P.sentences(r["note_beginner"] + " " + r["note_seasoned"])
                         if len(s.split()) >= 10)

        def m(batch):
            _sprob(batch, "eggplant", "aphids")["control_ladder"][0]["note_beginner"] += \
                " " + long_sent
        with _Patch("staged", _staged_with(m)):
            out = P.check_no_shipped_echo(P.staged(), pre)
        self.assertIsNotNone(out)
        self.assertIn("word sentence with the shipped", out)


class Shape(unittest.TestCase):
    def test_counts_match_the_read(self):
        batch = P.staged()
        for slug in CROPS:
            self.assertEqual(len(P.problems(batch[slug])), P.EXPECTED_PROBLEMS[slug], slug)
            n = sum(len(p.get("control_ladder") or []) for _, p in P.problems(batch[slug]))
            self.assertEqual(n, P.EXPECTED_RUNGS[slug], slug)
        self.assertEqual(P.rung_count(batch), 264)

    def test_check_REFUSES_identical_registers(self):
        def m(batch):
            r = _sprob(batch, "eggplant", "aphids")["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_an_unknown_method(self):
        """On an UNALIGNED problem (CPB has no twin), so the alignment guard cannot answer
        for the catalog-membership branch."""
        def m(batch):
            _sprob(batch, "eggplant", "colorado-potato-beetle")["control_ladder"].append(
                _rung("ghost_method"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_an_applies_to_incoherent_rung(self):
        """exclusion_fencing reaches vertebrates only; on a fungal problem the type map must
        refuse it (phomopsis is outside NO_MATERIAL and the forbidden set, so only this branch
        can answer)."""
        def m(batch):
            _sprob(batch, "eggplant", "phomopsis-blight")["control_ladder"].insert(
                2, _rung("exclusion_fencing"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_a_duplicate_method_in_one_ladder(self):
        def m(batch):
            _sprob(batch, "eggplant", "colorado-potato-beetle")["control_ladder"].append(
                _rung("crop_rotation"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice in one ladder", out)

    def test_check_REFUSES_a_rung_count_off_the_read(self):
        def m(batch):
            _sprob(batch, "eggplant", "colorado-potato-beetle")["control_ladder"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)

    def test_check_REFUSES_a_tier_decrease(self):
        def m(batch):
            lad = _sprob(batch, "eggplant", "aphids")["control_ladder"]
            lad[0], lad[-1] = lad[-1], lad[0]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        def m(batch):
            _sprob(batch, "eggplant", "aphids")["control_ladder"][0]["note_beginner"] += \
                " This never fails."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNone(P.hygiene("a clean sentence about peppers"))


class BlastRadius(unittest.TestCase):
    def test_key_sets_are_compared_before_values(self):
        """set(pre) == set(post) FIRST; iterating pre alone hides additions (PLA-162)."""
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(set(b["crops"]), set(a["crops"]))
        changed = sorted(s for s in a["crops"] if a["crops"][s] != b["crops"][s])
        self.assertEqual(changed, sorted(CROPS))

    def test_methods_and_sources_are_byte_identical(self):
        pre = _pre()
        a, b = P.snapshot(pre), P.snapshot(_post(pre))
        self.assertEqual(b["methods"], a["methods"])
        self.assertEqual(b["sources"], a["sources"])


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_the_post_state(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_the_five_ship_ids_types_and_ladders_on_every_problem(self):
        post = _post()
        for slug in CROPS:
            for _, p in P.problems(_crop(post, slug)):
                self.assertTrue(p.get("id"), (slug, p.get("name")))
                self.assertTrue(p.get("type"), (slug, p.get("id")))
                self.assertTrue(p.get("control_ladder"), (slug, p.get("id")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
