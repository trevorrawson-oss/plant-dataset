#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch14.py. Base 4c5a79d3 (the mancozeb mint's output,
rebuilt by CHAIN replay until the mint commits).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.
Every driver asserts its branch's ONE message.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch14 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "c76f14f19f4d2aa208748d0609f14a86bb5753c57fb21840f826e6a9d37599a0"

# FROZEN LITERALS -- restated, never derived from P.
CROPS = ("okra", "tomatillo", "cantaloupe", "honeydew-melon", "watermelon")
MELONS = ("cantaloupe", "honeydew-melon", "watermelon")
CONVENTIONAL_ON = (("cantaloupe", "alternaria-leaf-blight"), ("watermelon", "anthracnose"))
NEW_IDS = ("stink-bugs", "three-lined-potato-beetle", "root-and-stem-rots",
           "gummy-stem-blight", "alternaria-leaf-blight")
SHARED_PIDS = ("aphids", "spider-mites", "squash-bug", "powdery-mildew", "downy-mildew",
               "gummy-stem-blight")


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
    _UNIQ[0] += 1
    n = _UNIQ[0]
    return {"method": m, "note_beginner": f"injected beginner {_UNIQ[0]}",
            "note_seasoned": f"injected seasoned {n} differs"}


class VerifyPostIsDriven(unittest.TestCase):
    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_an_emptied_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "okra", "aphids")["control_ladder"] = []
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no ladder after promote", out)

    def test_a_conventional_outside_the_two_is_caught(self):
        snap, post = self._staged()
        _prob(post, "honeydew-melon", "gummy-stem-blight")["control_ladder"].append(
            _rung("mancozeb"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("outside the two earning ladders", out)

    def test_a_dropped_conventional_rung_is_caught(self):
        snap, post = self._staged()
        p = _prob(post, "watermelon", "anthracnose")
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "mancozeb"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped without its", out)

    def test_unearned_copper_is_caught(self):
        snap, post = self._staged()
        _prob(post, "okra", "powdery-mildew")["control_ladder"].append(_rung("copper_fungicide"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped copper unearned", out)

    def test_an_unearned_trap_rung_is_caught(self):
        snap, post = self._staged()
        _prob(post, "cantaloupe", "cucumber-beetles")["control_ladder"].insert(
            1, _rung("trap_cropping"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("trap_cropping unearned", out)

    def test_tillage_outside_its_earners_is_caught(self):
        snap, post = self._staged()
        _prob(post, "tomatillo", "cutworms")["control_ladder"].insert(
            1, _rung("off_season_tillage"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("outside its two earners", out)

    def test_a_forbidden_method_is_caught(self):
        snap, post = self._staged()
        _prob(post, "okra", "flea-beetles")["control_ladder"].append(
            _rung("disease_escape_sowing"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped forbidden", out)

    def test_a_material_on_a_no_material_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "cantaloupe", "downy-mildew")["control_ladder"].append(_rung("sulfur"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("which its prose rules out", out)

    def test_a_dropped_new_id_is_caught(self):
        """Driven through three-lined-potato-beetle, whose ladder carries no scope-guarded
        method, so no earlier branch can answer for the shipped-id check."""
        snap, post = self._staged()
        _prob(post, "tomatillo", "three-lined-potato-beetle")["id"] = "renamed-away"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("did not ship", out)

    def test_a_dropped_bystander_crop_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "pumpkin"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_an_edited_bystander_crop_is_caught(self):
        snap, post = self._staged()
        _crop(post, "pumpkin")["name"] = "MUTATED"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("touches only", out)

    def test_a_touched_method_is_caught(self):
        snap, post = self._staged()
        post["control_methods"]["mancozeb"]["best_use"] += " x"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("mints and widens NOTHING", out)

    def test_a_touched_source_is_caught(self):
        snap, post = self._staged()
        post["source_catalog"]["clemson_hgic"]["accessed"] = "2099-01"
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

    def test_the_base_already_carries_the_mint(self):
        pre = _pre()
        self.assertIn("mancozeb", pre["control_methods"])
        self.assertEqual(pre["control_methods"]["mancozeb"]["tier"], "conventional")

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

    def test_check_REFUSES_a_base_predating_the_mint(self):
        pre = _pre()
        del pre["control_methods"]["mancozeb"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("predates the mint", out)

    def test_roster_grows_to_63_laddered(self):
        post = _post()
        n = sum(1 for c in post["crops"]
                if any("control_ladder" in p for fam in ("pests", "diseases")
                       for p in c.get(fam) or []))
        self.assertEqual(n, 63)


class Conventionals(unittest.TestCase):
    """chlorothalonil + mancozeb on exactly two ladders, both required on both."""

    def test_the_two_earning_ladders_carry_both_materials(self):
        batch = P.staged()
        for slug, pid in CONVENTIONAL_ON:
            ms = [r["method"] for r in _sprob(batch, slug, pid)["control_ladder"]]
            self.assertIn("chlorothalonil", ms, (slug, pid))
            self.assertIn("mancozeb", ms, (slug, pid))

    def test_no_other_ladder_carries_either(self):
        batch = P.staged()
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                if (slug, p["id"]) in CONVENTIONAL_ON:
                    continue
                ms = [r["method"] for r in p.get("control_ladder") or []]
                self.assertNotIn("chlorothalonil", ms, (slug, p["id"]))
                self.assertNotIn("mancozeb", ms, (slug, p["id"]))

    def test_check_REFUSES_a_ladder_dropping_one_material(self):
        def m(batch):
            p = _sprob(batch, "cantaloupe", "alternaria-leaf-blight")
            p["control_ladder"] = [r for r in p["control_ladder"]
                                   if r["method"] != "chlorothalonil"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("silently un-names the other", out)

    def test_check_REFUSES_an_unearned_conventional(self):
        def m(batch):
            _sprob(batch, "honeydew-melon", "powdery-mildew")["control_ladder"].append(
                _rung("chlorothalonil"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("whose prose names both materials earn", out)

    def test_check_REFUSES_unearned_copper(self):
        def m(batch):
            _sprob(batch, "okra", "powdery-mildew")["control_ladder"].append(
                _rung("copper_fungicide"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("only tomatillo's early blight", out)

    def test_copper_IS_earned_on_tomatillo_early_blight(self):
        batch = P.staged()
        ms = [r["method"] for r in _sprob(batch, "tomatillo", "early-blight")["control_ladder"]]
        self.assertIn("copper_fungicide", ms)


class WiltPremise(unittest.TestCase):
    """The melon bacterial-wilt reuse rests on Erwinia being what the records claim."""

    def test_the_premise_holds_in_canonical(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_bacterial_wilt_premise(by))

    def test_watermelon_correctly_carries_no_bacterial_wilt(self):
        batch = P.staged()
        ids = {p["id"] for _, p in P.problems(batch["watermelon"])}
        self.assertNotIn("bacterial-wilt", ids)

    def test_check_REFUSES_when_only_honeydews_evidence_is_gone(self):
        """Strips Erwinia from HONEYDEW alone, so a premise loop that quietly stopped inspecting
        the second melon cannot pass on cantaloupe's evidence."""
        pre = _pre()
        for fam in ("pests", "diseases"):
            for p in _crop(pre, "honeydew-melon").get(fam) or []:
                if p.get("name") == "Bacterial wilt":
                    for f in ("cause_beginner", "cause_seasoned"):
                        if p.get(f):
                            p[f] = p[f].replace("Erwinia tracheiphila", "a bacterium")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer names Erwinia", out)

    def test_check_REFUSES_when_the_erwinia_evidence_is_gone(self):
        pre = _pre()
        for slug in ("cantaloupe", "honeydew-melon"):
            for fam in ("pests", "diseases"):
                for p in _crop(pre, slug).get(fam) or []:
                    if p.get("name") == "Bacterial wilt":
                        for f in ("cause_beginner", "cause_seasoned"):
                            if p.get(f):
                                p[f] = p[f].replace("Erwinia tracheiphila", "a bacterium")
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no longer names Erwinia", out)


class Alignment(unittest.TestCase):
    def test_the_correspondence_holds_on_the_real_batch(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_alignment(by, P.staged()))

    def test_the_six_shared_sets_are_identical_across_the_melons(self):
        batch = P.staged()
        for pid in SHARED_PIDS:
            first = P.ladder_key(_sprob(batch, "cantaloupe", pid))
            for slug in MELONS[1:]:
                self.assertEqual(P.ladder_key(_sprob(batch, slug, pid)), first, (slug, pid))

    def test_the_per_crop_problems_keep_their_own_texts(self):
        """cucumber beetles' prose differs per melon (wilt framing), so their ladders differ."""
        batch = P.staged()
        keys = {P.ladder_key(_sprob(batch, s, "cucumber-beetles")) for s in MELONS}
        self.assertEqual(len(keys), 3)

    def test_check_REFUSES_a_fork_on_identical_prose(self):
        def m(batch):
            _sprob(batch, "watermelon", "aphids")["control_ladder"][0]["note_beginner"] += " More."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("identical prose ships one text set", out)

    def test_check_REFUSES_a_ladder_copied_across_differing_prose(self):
        def m(batch):
            donor = _sprob(batch, "cantaloupe", "cucumber-beetles")
            _sprob(batch, "watermelon", "cucumber-beetles")["control_ladder"] = copy.deepcopy(
                donor["control_ladder"])
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("given the other's source", out)

    def test_the_shared_sets_are_crop_neutral(self):
        batch = P.staged()
        self.assertIsNone(P.check_melon_neutrality(batch))

    def test_check_REFUSES_a_crop_named_shared_rung(self):
        def m(batch):
            for slug in MELONS:
                r = _sprob(batch, slug, "spider-mites")["control_ladder"][0]
                r["note_seasoned"] += " Watermelon suffers worst."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must stay crop-neutral", out)


class TrapAndTillage(unittest.TestCase):
    def test_okra_is_the_only_trap_carrier_and_attributes_the_removal(self):
        batch = P.staged()
        carriers = []
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p.get("control_ladder") or []:
                    if r["method"] == "trap_cropping":
                        carriers.append((slug, p["id"]))
                        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                        self.assertIn("this crop's guidance", blob)
                        self.assertIn("cautions", blob)
        self.assertEqual(carriers, [("okra", "stink-bugs")])

    def test_check_REFUSES_a_trap_rung_losing_its_attribution(self):
        def m(batch):
            p = _sprob(batch, "okra", "stink-bugs")
            r = next(r for r in p["control_ladder"] if r["method"] == "trap_cropping")
            for k in ("note_beginner", "note_seasoned"):
                r[k] = r[k].replace("this crop's guidance", "sound practice")
                r[k] = r[k].replace("per this crop's guidance", "as sound practice")
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("the strongest thing it could say goes unsaid", out)

    def test_check_REFUSES_a_trap_rung_losing_its_cautions_pointer(self):
        def m(batch):
            p = _sprob(batch, "okra", "stink-bugs")
            r = next(r for r in p["control_ladder"] if r["method"] == "trap_cropping")
            for k in ("note_beginner", "note_seasoned"):
                r[k] = r[k].replace("cautions", "notes")
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("removal deadline the prose omits", out)

    def test_check_REFUSES_a_forbidden_method(self):
        def m(batch):
            _sprob(batch, "okra", "flea-beetles")["control_ladder"].append(
                _rung("disease_escape_sowing"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("sow-early fungal escape", out)

    def test_check_REFUSES_a_material_on_a_no_material_ladder(self):
        def m(batch):
            _sprob(batch, "cantaloupe", "downy-mildew")["control_ladder"].append(_rung("sulfur"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("names no such material or states there is no cure", out)

    def test_check_REFUSES_an_unearned_trap_rung(self):
        def m(batch):
            _sprob(batch, "honeydew-melon", "squash-bug")["control_ladder"].insert(
                1, _rung("trap_cropping"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("only okra's stink bugs earn", out)

    def test_check_REFUSES_tillage_outside_its_earners(self):
        def m(batch):
            _sprob(batch, "tomatillo", "cutworms")["control_ladder"].insert(
                1, _rung("off_season_tillage"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("pre-plant cultivation stays refused", out)

    def test_the_earned_tillage_rungs_are_present(self):
        batch = P.staged()
        ms = [r["method"] for r in _sprob(batch, "tomatillo", "tomato-hornworm")["control_ladder"]]
        self.assertIn("off_season_tillage", ms)
        for slug in MELONS:
            ms = [r["method"] for r in _sprob(batch, slug, "squash-vine-borer")["control_ladder"]]
            self.assertIn("off_season_tillage", ms, slug)


class Ids(unittest.TestCase):
    def test_check_REFUSES_an_id_off_the_convention_table(self):
        def m(batch):
            _sprob(batch, "okra", "stink-bugs")["id"] = "stink-bugs-leaf-footed-bugs"
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
        pre = _pre()
        for c in pre["crops"]:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if p.get("id") == "corn-earworm":
                        p["id"] = "corn-earworm-renamed"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint wearing a reuse's name", out)

    def test_check_REFUSES_a_new_id_already_taken(self):
        pre = _pre()
        _crop(pre, "pumpkin").setdefault("diseases", []).append(
            {"id": "gummy-stem-blight", "name": "Planted collision"})
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("listed as new to this base", out)


class Echo(unittest.TestCase):
    def test_no_note_echoes_a_shipped_rung(self):
        pre = _pre()
        self.assertIsNone(P.check_no_shipped_echo(P.staged(), pre))

    def test_the_echo_scan_is_not_vacuous(self):
        pre = _pre()
        donor = _prob(pre, "slicing-cucumber", "aphids")
        shipped = donor["control_ladder"][0]["note_beginner"]

        def m(batch):
            _sprob(batch, "okra", "aphids")["control_ladder"][0]["note_beginner"] = shipped
        with _Patch("staged", _staged_with(m)):
            out = P.check_no_shipped_echo(P.staged(), pre)
        self.assertIsNotNone(out)
        self.assertIn("byte-identical to the shipped", out)

    def test_the_sentence_half_of_the_echo_scan_is_not_vacuous(self):
        pre = _pre()
        donor = _prob(pre, "slicing-cucumber", "aphids")
        long_sent = next(s for r in donor["control_ladder"]
                         for s in P.sentences(r["note_beginner"] + " " + r["note_seasoned"])
                         if len(s.split()) >= 10)

        def m(batch):
            _sprob(batch, "okra", "aphids")["control_ladder"][0]["note_beginner"] += \
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
        self.assertEqual(P.rung_count(batch), 232)

    def test_check_REFUSES_a_rung_count_off_the_read(self):
        def m(batch):
            _sprob(batch, "okra", "cutworms" if False else "corn-earworm")["control_ladder"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)

    def test_check_REFUSES_identical_registers(self):
        def m(batch):
            r = _sprob(batch, "okra", "corn-earworm")["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_an_unknown_method(self):
        def m(batch):
            _sprob(batch, "okra", "corn-earworm")["control_ladder"].append(_rung("ghost_method"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_a_duplicate_method(self):
        def m(batch):
            _sprob(batch, "okra", "corn-earworm")["control_ladder"].append(_rung("handpick"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice in one ladder", out)

    def test_check_REFUSES_a_tier_decrease(self):
        def m(batch):
            lad = _sprob(batch, "okra", "corn-earworm")["control_ladder"]
            lad[0], lad[-1] = lad[-1], lad[0]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_an_applies_to_incoherent_rung(self):
        def m(batch):
            _sprob(batch, "tomatillo", "root-and-stem-rots")["control_ladder"].insert(
                1, _rung("stem_collars"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        def m(batch):
            _sprob(batch, "okra", "corn-earworm")["control_ladder"][0]["note_beginner"] += \
                " This never fails."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNone(P.hygiene("a clean sentence about melons"))


class BlastRadius(unittest.TestCase):
    def test_key_sets_are_compared_before_values(self):
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
