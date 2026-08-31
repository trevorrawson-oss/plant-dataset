#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch15.py. Base c76f14f1 (batch 14's output, a commit).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.
Every driver asserts its branch's ONE message.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch15 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "098dd0b18cc85aebf05bbb50071ab9ba1c50bf377afb1235d9359cc07d894bfa"

# FROZEN LITERALS -- restated, never derived from P.
CROPS = ("marigold", "zinnia", "cosmos", "calendula", "sweet-alyssum")
NEW_IDS = ("japanese-beetles", "leaf-spots", "zinnia-leaf-spots", "aster-leafhoppers",
           "stem-canker", "cucumber-mosaic")
BANNED = ("trap crop", "trap-crop", "sacrificial", "banker")


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
        _prob(post, "cosmos", "aphids")["control_ladder"] = []
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no ladder after promote", out)

    def test_a_forbidden_method_is_caught(self):
        """The inversion driver: trap_cropping on zinnia's Japanese beetles is the documented
        INVERTED case, and the forbidden sweep must name it."""
        snap, post = self._staged()
        _prob(post, "zinnia", "japanese-beetles")["control_ladder"].insert(0, _rung("trap_cropping"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped forbidden", out)

    def test_a_banned_note_token_is_caught(self):
        snap, post = self._staged()
        r = _prob(post, "calendula", "aphids")["control_ladder"][1]
        r["note_seasoned"] += " Some grow it as a banker plant."
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("a shipped note mentions", out)

    def test_a_dropped_pheromone_warning_is_caught(self):
        snap, post = self._staged()
        r = _prob(post, "marigold", "japanese-beetles")["control_ladder"][0]
        for k in ("note_beginner", "note_seasoned"):
            r[k] = r[k].replace("pheromone", "scent").replace("Pheromone", "Scent")
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("without the pheromone-trap warning", out)

    def test_a_material_on_a_no_material_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "zinnia", "powdery-mildew")["control_ladder"].append(_rung("iron_phosphate_slug_bait"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("which its notes rule out", out)

    def test_a_vanished_new_id_is_caught_by_its_per_id_lookup(self):
        """Every new id doubles as a NO_MATERIAL or pheromone lookup key, so a rename always
        trips the specific 'lost its <id> problem' message; the generic did-not-ship branch was
        deleted as unreachable (the trap-round rule)."""
        snap, post = self._staged()
        _prob(post, "cosmos", "stem-canker")["id"] = "renamed-away"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("lost its stem-canker problem", out)

    def test_the_wrong_organism_id_shipping_is_caught(self):
        """Driven through marigold's aphids (no per-id lookup covers it), so only the
        taxon-shipped branch can answer for the wrong string appearing."""
        snap, post = self._staged()
        _prob(post, "marigold", "aphids")["id"] = "alternaria-leaf-spot"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("the wrong organism", out)

    def test_a_dropped_bystander_crop_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "borage"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_an_edited_bystander_crop_is_caught(self):
        snap, post = self._staged()
        _crop(post, "borage")["name"] = "MUTATED"
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

    def test_roster_grows_to_68_laddered(self):
        post = _post()
        n = sum(1 for c in post["crops"]
                if any("control_ladder" in p for fam in ("pests", "diseases")
                       for p in c.get(fam) or []))
        self.assertEqual(n, 68)


class SchemaPremise(unittest.TestCase):
    """The note pair must exist on every target, or every prose comparison goes vacuous."""

    def test_the_premise_holds_in_canonical(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_schema_premise(by))

    def test_check_REFUSES_a_target_missing_its_notes(self):
        pre = _pre()
        for fam in ("pests", "diseases"):
            for p in _crop(pre, "zinnia").get(fam) or []:
                if p.get("name") == "Aphids":
                    p["note_seasoned"] = ""
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("schema premise", out)


class Inversion(unittest.TestCase):
    """The companion crops ARE the trap/banker stands; the batch refuses the whole family."""

    def test_no_staged_ladder_carries_trap_cropping(self):
        batch = P.staged()
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                ms = [r["method"] for r in p.get("control_ladder") or []]
                self.assertNotIn("trap_cropping", ms, (slug, p["id"]))

    def test_no_staged_note_carries_banned_vocabulary(self):
        batch = P.staged()
        for slug in CROPS:
            for _, p in P.problems(batch[slug]):
                for r in p.get("control_ladder") or []:
                    blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                    for w in BANNED:
                        self.assertNotIn(w, blob, (slug, p["id"], r["method"]))

    def test_the_source_notes_DO_carry_the_content_the_ban_protects_against(self):
        """The ban is not vacuous: zinnia's and calendula's own records describe trap/banker
        value, so the unplaced content genuinely exists to creep back."""
        pre = _pre()
        z = _prob_by_name(pre, "zinnia", "Japanese beetles")
        self.assertIn("trap-crop", (z.get("note_seasoned") or "").lower())
        c = _prob_by_name(pre, "calendula", "Aphids")
        self.assertIn("banker", (c.get("note_seasoned") or "").lower())

    def test_check_REFUSES_a_trap_rung(self):
        def m(batch):
            _sprob(batch, "zinnia", "japanese-beetles")["control_ladder"].insert(
                0, _rung("trap_cropping"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("destroying the planting", out)

    def test_check_REFUSES_a_note_with_banned_vocabulary(self):
        def m(batch):
            r = _sprob(batch, "calendula", "aphids")["control_ladder"][1]
            r["note_seasoned"] += " It doubles as a sacrificial stand."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must not creep back", out)

    def test_check_REFUSES_a_dropped_pheromone_warning(self):
        def m(batch):
            r = _sprob(batch, "zinnia", "japanese-beetles")["control_ladder"][0]
            for k in ("note_beginner", "note_seasoned"):
                r[k] = r[k].replace("pheromone", "scent").replace("Pheromone", "Scent")
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no token to scan for once it is gone", out)

    def test_the_pheromone_warning_is_present_on_both_carriers(self):
        batch = P.staged()
        for slug in ("marigold", "zinnia"):
            p = _sprob(batch, slug, "japanese-beetles")
            r = next(r for r in p["control_ladder"] if r["method"] == "handpick")
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            self.assertIn("pheromone", blob, slug)


def _prob_by_name(data, slug, name):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("name") == name:
                return p
    raise AssertionError(f"{slug}/{name} not found")


class Ids(unittest.TestCase):
    def test_check_REFUSES_an_id_off_the_convention_table(self):
        def m(batch):
            _sprob(batch, "marigold", "gray-mold")["id"] = "botrytis-gray-mold"
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never re-derived from the name", out)

    def test_check_REFUSES_the_brassica_alternaria_reuse(self):
        """The wrong-string-PRESENT branch, driven with the right string still shipping: a
        different single-carrier problem takes the brassica id (table patched along), so only
        the taxon refusal can object."""
        def m(batch):
            _sprob(batch, "cosmos", "stem-canker")["id"] = "alternaria-leaf-spot"
        table = dict(P.ID_CONVENTION)
        table["Stem canker"] = "alternaria-leaf-spot"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("WRONG ORGANISM", out)

    def test_check_REFUSES_a_batch_losing_the_taxon_ruled_id(self):
        def m(batch):
            _sprob(batch, "zinnia", "zinnia-leaf-spots")["id"] = "zinnia-spots"
        table = dict(P.ID_CONVENTION)
        table["Alternaria and bacterial leaf spot"] = "zinnia-spots"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("requires id 'zinnia-leaf-spots'", out)

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
                    if p.get("id") == "whiteflies":
                        p["id"] = "whiteflies-renamed"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint wearing a reuse's name", out)

    def test_check_REFUSES_a_new_id_already_taken(self):
        pre = _pre()
        _crop(pre, "borage").setdefault("diseases", []).append(
            {"id": "stem-canker", "name": "Planted collision",
             "note_beginner": "x", "note_seasoned": "y"})
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("listed as new to this base", out)

    def test_the_gray_mold_string_is_shared_by_marigold_and_cosmos(self):
        batch = P.staged()
        self.assertEqual(_sprob(batch, "marigold", "gray-mold")["id"], "gray-mold")
        self.assertEqual(_sprob(batch, "cosmos", "gray-mold")["id"], "gray-mold")


class Alignment(unittest.TestCase):
    def test_the_correspondence_holds_on_the_real_batch(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_alignment(by, P.staged()))

    def test_no_identical_note_pair_exists_so_every_ladder_is_authored(self):
        """The measured fact the note-schema tool fix made visible: zero twins."""
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        keys = {}
        for slug in CROPS:
            for _, p in P.problems(by[slug]):
                k = (p.get("name"), P.advice_key(p))
                self.assertNotIn(k, keys, f"{slug} twins {keys.get(k)}")
                keys[k] = slug

    def test_check_REFUSES_a_ladder_copied_across_differing_prose(self):
        def m(batch):
            donor = _sprob(batch, "marigold", "aphids")
            _sprob(batch, "zinnia", "aphids")["control_ladder"] = copy.deepcopy(
                donor["control_ladder"])
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("given the other's source", out)


class Materials(unittest.TestCase):
    def test_every_disease_ladder_ends_cultural_or_physical(self):
        batch = P.staged()
        pre = _pre()
        cm = pre["control_methods"]
        for slug in CROPS:
            for fam, p in P.problems(batch[slug]):
                if fam != "diseases":
                    continue
                for r in p["control_ladder"]:
                    self.assertNotIn(cm[r["method"]]["tier"], ("soft_chemical", "conventional"),
                                     (slug, p["id"], r["method"]))

    def test_check_REFUSES_a_material_on_a_no_material_ladder(self):
        def m(batch):
            _sprob(batch, "cosmos", "powdery-mildew")["control_ladder"].append(
                _rung("iron_phosphate_slug_bait"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("its notes name no such material", out)

    def test_check_REFUSES_a_forbidden_method(self):
        def m(batch):
            _sprob(batch, "zinnia", "powdery-mildew")["control_ladder"].append(_rung("sulfur"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("names any fungicide", out)

    def test_the_bt_rung_keeps_the_butterfly_group_caution(self):
        batch = P.staged()
        p = _sprob(batch, "sweet-alyssum", "cabbageworms")
        r = next(r for r in p["control_ladder"] if r["method"] == "bt")
        self.assertIn("caterpillars as a group", r["note_seasoned"].lower())


class Echo(unittest.TestCase):
    def test_no_note_echoes_a_shipped_rung(self):
        pre = _pre()
        self.assertIsNone(P.check_no_shipped_echo(P.staged(), pre))

    def test_the_echo_scan_is_not_vacuous(self):
        pre = _pre()
        donor = _prob(pre, "tomatillo", "early-blight")
        shipped = donor["control_ladder"][0]["note_beginner"]

        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"][0]["note_beginner"] = shipped
        with _Patch("staged", _staged_with(m)):
            out = P.check_no_shipped_echo(P.staged(), pre)
        self.assertIsNotNone(out)
        self.assertIn("byte-identical to the shipped", out)

    def test_the_sentence_half_of_the_echo_scan_is_not_vacuous(self):
        pre = _pre()
        donor = _prob(pre, "tomatillo", "early-blight")
        long_sent = next(s for r in donor["control_ladder"]
                         for s in P.sentences(r["note_beginner"] + " " + r["note_seasoned"])
                         if len(s.split()) >= 10)

        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"][0]["note_beginner"] += \
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
        self.assertEqual(P.rung_count(batch), 84)

    def test_check_REFUSES_a_rung_count_off_the_read(self):
        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)

    def test_check_REFUSES_identical_registers(self):
        def m(batch):
            r = _sprob(batch, "cosmos", "aphids")["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_an_unknown_method(self):
        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"].append(_rung("ghost_method"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_a_duplicate_method(self):
        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"].append(_rung("water_spray"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice in one ladder", out)

    def test_check_REFUSES_a_tier_decrease(self):
        def m(batch):
            lad = _sprob(batch, "cosmos", "aphids")["control_ladder"]
            lad[0], lad[-1] = lad[-1], lad[0]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_an_applies_to_incoherent_rung(self):
        def m(batch):
            _sprob(batch, "cosmos", "powdery-mildew")["control_ladder"].insert(
                1, _rung("stem_collars"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        def m(batch):
            _sprob(batch, "cosmos", "aphids")["control_ladder"][0]["note_beginner"] += \
                " This never fails."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("copy hygiene", out)

    def test_hygiene_is_not_vacuous(self):
        self.assertIsNotNone(P.hygiene("this always works"))
        self.assertIsNotNone(P.hygiene("an em dash — here"))
        self.assertIsNone(P.hygiene("a clean sentence about flowers"))


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
