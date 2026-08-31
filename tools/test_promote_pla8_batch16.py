#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch16.py. Base 098dd0b1 (batch 15's output, a commit).

REPLAY-PINNED; no RED phase claimed. Evidence is `VerifyPostIsDriven` + the mutation harness.
Every driver asserts its branch's ONE message.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch16 as P  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402

POST_SHA = "213cb1108cd4960add0a0f9d3a2bd73aee4f1108d6fa743c6ce6075fd5cc6c2f"

# FROZEN LITERALS -- restated, never derived from P.
CROPS = ("echinacea", "bee-balm", "chamomile", "borage", "sweet-pea")
NEW_IDS = ("eriophyid-mites", "rabbits-and-deer", "stalk-borer", "bee-balm-rust", "mealybugs",
           "caterpillars")
BANNED = ("trap crop", "trap-crop", "sacrificial", "banker", "decoy")
ROT_NAMES = ("Crown and root rot in wet soil", "Root and stem rot in wet soil",
             "Root, stem, and crown rots")


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


def _prob_by_name(data, slug, name):
    for fam in ("pests", "diseases"):
        for p in _crop(data, slug).get(fam) or []:
            if p.get("name") == name:
                return p
    raise AssertionError(f"{slug}/{name} not found")


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


def _strip_trap(r):
    for k in ("note_beginner", "note_seasoned"):
        r[k] = r[k].replace("trap", "lure").replace("Trap", "Lure")


class VerifyPostIsDriven(unittest.TestCase):
    def _staged(self):
        pre = _pre()
        return P.snapshot(pre), _post(pre)

    def test_an_emptied_ladder_is_caught(self):
        snap, post = self._staged()
        _prob(post, "chamomile", "gray-mold")["control_ladder"] = []
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("no ladder after promote", out)

    def test_a_forbidden_method_is_caught(self):
        """The inversion driver: trap_cropping on the crops other plantings use AS the trap."""
        snap, post = self._staged()
        _prob(post, "borage", "aphids")["control_ladder"].insert(0, _rung("trap_cropping"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped forbidden", out)

    def test_a_banned_note_token_is_caught(self):
        snap, post = self._staged()
        r = _prob(post, "borage", "aphids")["control_ladder"][1]
        r["note_seasoned"] += " Some grow it as a decoy stand."
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("a shipped note mentions", out)

    def test_an_unearned_material_is_caught(self):
        snap, post = self._staged()
        _prob(post, "echinacea", "powdery-mildew")["control_ladder"].append(
            _rung("iron_phosphate_slug_bait"))
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped unearned material", out)

    def test_a_lost_handpick_rung_is_caught(self):
        """Driven by RETYPING the rung, not deleting it: echinacea's beetle ladder is the single
        handpick rung, so deletion would trip the no-ladder branch instead."""
        snap, post = self._staged()
        r = _prob(post, "echinacea", "japanese-beetles")["control_ladder"][0]
        r["method"] = "water_spray"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped without its handpick rung", out)

    def test_a_stripped_lure_trap_warning_is_caught(self):
        snap, post = self._staged()
        _strip_trap(_prob(post, "echinacea", "japanese-beetles")["control_ladder"][0])
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("shipped without the lure-trap warning", out)

    def test_a_vanished_new_id_is_caught(self):
        """Batch 15 deleted this branch as unreachable because every new id doubled as a per-id
        lookup key; here only japanese-beetles does, so the shipped check is real protection."""
        snap, post = self._staged()
        _prob(post, "bee-balm", "stalk-borer")["id"] = "renamed-away"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("new id 'stalk-borer' did not ship", out)

    def test_the_wrong_join_key_shipping_is_caught(self):
        """Driven through echinacea's leaf-spots (no material, no per-id lookup covers it), so
        only the taxon-shipped branch can answer for the peas' string appearing."""
        snap, post = self._staged()
        _prob(post, "echinacea", "leaf-spots")["id"] = "root-rots-damping-off"
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("the wrong join key", out)

    def test_a_dropped_bystander_crop_is_caught(self):
        snap, post = self._staged()
        post["crops"] = [c for c in post["crops"] if c.get("slug") != "marigold"]
        out = P.verify_post(snap, post)
        self.assertIsNotNone(out)
        self.assertIn("crop set changed", out)

    def test_an_edited_bystander_crop_is_caught(self):
        snap, post = self._staged()
        _crop(post, "marigold")["name"] = "MUTATED"
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

    def test_check_REFUSES_a_missing_batch_crop(self):
        pre = _pre()
        pre["crops"] = [c for c in pre["crops"] if c.get("slug") != "borage"]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("no crop 'borage' in canonical", out)

    def test_check_REFUSES_a_staged_canonical_problem_count_mismatch(self):
        def m(batch):
            batch["chamomile"]["diseases"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("staged 5 problems, canonical 6", out)

    def test_roster_grows_to_73_laddered(self):
        post = _post()
        n = sum(1 for c in post["crops"]
                if any("control_ladder" in p for fam in ("pests", "diseases")
                       for p in c.get(fam) or []))
        self.assertEqual(n, 73)


class SchemaPremise(unittest.TestCase):
    """The note pair must exist on every target, or every prose comparison goes vacuous."""

    def test_the_premise_holds_in_canonical(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_schema_premise(by))

    def test_check_REFUSES_a_target_missing_its_notes(self):
        pre = _pre()
        _prob_by_name(pre, "chamomile", "Aphids")["note_seasoned"] = ""
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("schema premise", out)


class Inversion(unittest.TestCase):
    """Companions B holds the batch-15 inversion, plus the lure-trap anti-recommendation."""

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
        """The ban is not vacuous: borage's own aphid record describes banker AND decoy value,
        the reason 'decoy' joined the banned list this batch."""
        pre = _pre()
        b = _prob_by_name(pre, "borage", "Aphids")
        blob = ((b.get("note_beginner") or "") + " " + (b.get("note_seasoned") or "")).lower()
        self.assertIn("banker", blob)
        self.assertIn("decoy", blob)

    def test_check_REFUSES_a_trap_rung(self):
        def m(batch):
            _sprob(batch, "borage", "aphids")["control_ladder"].insert(0, _rung("trap_cropping"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("the companion inversion holds", out)

    def test_check_REFUSES_a_note_with_banned_vocabulary(self):
        def m(batch):
            r = _sprob(batch, "borage", "aphids")["control_ladder"][1]
            r["note_seasoned"] += " It doubles as a decoy stand."
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("must not creep back", out)

    def test_check_REFUSES_a_lost_handpick_rung(self):
        def m(batch):
            _sprob(batch, "echinacea", "japanese-beetles")["control_ladder"] = []
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("lost its handpick rung", out)

    def test_check_REFUSES_a_stripped_lure_trap_warning(self):
        def m(batch):
            _strip_trap(_sprob(batch, "echinacea", "japanese-beetles")["control_ladder"][0])
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no token to scan for once it is gone", out)

    def test_the_lure_trap_warning_is_present_in_both_registers(self):
        batch = P.staged()
        p = _sprob(batch, "echinacea", "japanese-beetles")
        r = next(r for r in p["control_ladder"] if r["method"] == "handpick")
        self.assertIn("trap", r["note_beginner"].lower())
        self.assertIn("trap", r["note_seasoned"].lower())

    def test_the_source_note_carries_the_anti_trap_advice(self):
        pre = _pre()
        p = _prob_by_name(pre, "echinacea", "Japanese beetles")
        blob = ((p.get("note_beginner") or "") + " " + (p.get("note_seasoned") or "")).lower()
        self.assertIn("trap", blob)


class Ids(unittest.TestCase):
    def test_check_REFUSES_a_name_off_the_convention_table(self):
        pre = _pre()
        _prob_by_name(pre, "echinacea", "Aphids")["name"] = "Aphid pressure"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("not in the id-convention table", out)

    def test_check_REFUSES_an_id_off_the_convention_table(self):
        def m(batch):
            _sprob(batch, "chamomile", "gray-mold")["id"] = "botrytis-gray-mold"
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("never re-derived from the name", out)

    def test_check_REFUSES_the_peas_rot_id_on_sweet_pea(self):
        """The wrong-string-PRESENT branch: gray-mold (single carrier) takes the peas' id with
        the table patched along, so only the taxon refusal can object."""
        def m(batch):
            _sprob(batch, "chamomile", "gray-mold")["id"] = "root-rots-damping-off"
        table = dict(P.ID_CONVENTION)
        table["Botrytis (gray mold)"] = "root-rots-damping-off"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("WRONG JOIN KEY", out)

    def test_check_REFUSES_a_batch_losing_the_taxon_ruled_id(self):
        def m(batch):
            for slug in ("echinacea", "borage", "sweet-pea"):
                _sprob(batch, slug, "root-and-stem-rots")["id"] = "root-and-stem-complex"
        table = dict(P.ID_CONVENTION)
        for name in ROT_NAMES:
            table[name] = "root-and-stem-complex"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("requires id 'root-and-stem-rots'", out)

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
                    if p.get("id") == "downy-mildew":
                        p["id"] = "downy-mildew-renamed"
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("mint wearing a reuse's name", out)

    def test_check_REFUSES_a_new_id_already_taken(self):
        pre = _pre()
        _crop(pre, "marigold").setdefault("diseases", []).append(
            {"id": "stalk-borer", "name": "Planted collision",
             "note_beginner": "x", "note_seasoned": "y"})
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("listed as new to this base", out)

    def test_the_rot_id_is_shared_by_all_three_carriers(self):
        batch = P.staged()
        for slug in ("echinacea", "borage", "sweet-pea"):
            self.assertEqual(_sprob(batch, slug, "root-and-stem-rots")["id"],
                             "root-and-stem-rots", slug)

    def test_bee_balm_rust_is_species_scoped_not_a_generic_rust(self):
        """The record names only Puccinia spp., so the id is crop-scoped; a later mint for the
        mint-family P. menthae stays free."""
        batch = P.staged()
        self.assertEqual(_sprob(batch, "bee-balm", "bee-balm-rust")["id"], "bee-balm-rust")
        pre = _pre()
        self.assertNotIn("rust", P.roster_ids(pre))


class Alignment(unittest.TestCase):
    def test_the_correspondence_holds_on_the_real_batch(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        self.assertIsNone(P.check_alignment(by, P.staged()))

    def test_no_identical_note_pair_exists_so_every_ladder_is_authored(self):
        pre = _pre()
        by = {c.get("slug"): c for c in pre["crops"]}
        keys = {}
        for slug in CROPS:
            for _, p in P.problems(by[slug]):
                k = (p.get("name"), P.advice_key(p))
                self.assertNotIn(k, keys, f"{slug} twins {keys.get(k)}")
                keys[k] = slug

    def test_check_REFUSES_identical_prose_with_different_ladders(self):
        pre = _pre()
        donor = _prob_by_name(pre, "echinacea", "Aphids")
        tgt = _prob_by_name(pre, "chamomile", "Aphids")
        for f in P.ADVICE_FIELDS:
            tgt[f] = donor[f]
        out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("identical prose ships one text set", out)

    def test_check_REFUSES_a_ladder_copied_across_differing_prose(self):
        def m(batch):
            donor = _sprob(batch, "echinacea", "aphids")
            _sprob(batch, "borage", "aphids")["control_ladder"] = copy.deepcopy(
                donor["control_ladder"])
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("given the other's source", out)


class Materials(unittest.TestCase):
    def test_every_disease_ladder_is_cultural_and_physical_only(self):
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

    def test_check_REFUSES_an_unearned_material(self):
        def m(batch):
            _sprob(batch, "echinacea", "powdery-mildew")["control_ladder"].append(
                _rung("iron_phosphate_slug_bait"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("scopes every material to the ladders that earn it", out)

    def test_check_REFUSES_a_forbidden_method(self):
        def m(batch):
            _sprob(batch, "sweet-pea", "powdery-mildew")["control_ladder"].append(_rung("sulfur"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no note names sulfur", out)

    def test_the_spinosad_rungs_keep_the_bee_framing(self):
        """The pollinator tension is resolved the chlorothalonil way: the material ships because
        the crop's notes name it, WITH the bee-caution framing in the seasoned register."""
        batch = P.staged()
        for pid in ("thrips", "caterpillars"):
            p = _sprob(batch, "sweet-pea", pid)
            r = next(r for r in p["control_ladder"] if r["method"] == "spinosad")
            self.assertIn("bee", r["note_seasoned"].lower(), pid)


class Echo(unittest.TestCase):
    def test_no_note_echoes_a_shipped_rung(self):
        pre = _pre()
        self.assertIsNone(P.check_no_shipped_echo(P.staged(), pre))

    def test_the_echo_scan_is_not_vacuous(self):
        pre = _pre()
        donor = _prob(pre, "tomatillo", "early-blight")
        shipped = donor["control_ladder"][0]["note_beginner"]

        def m(batch):
            _sprob(batch, "borage", "aphids")["control_ladder"][0]["note_beginner"] = shipped
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
            _sprob(batch, "borage", "aphids")["control_ladder"][0]["note_beginner"] += \
                " " + long_sent
        with _Patch("staged", _staged_with(m)):
            out = P.check_no_shipped_echo(P.staged(), pre)
        self.assertIsNotNone(out)
        self.assertIn("word sentence with", out)


class Shape(unittest.TestCase):
    def test_counts_match_the_read(self):
        batch = P.staged()
        for slug in CROPS:
            self.assertEqual(len(P.problems(batch[slug])), P.EXPECTED_PROBLEMS[slug], slug)
            n = sum(len(p.get("control_ladder") or []) for _, p in P.problems(batch[slug]))
            self.assertEqual(n, P.EXPECTED_RUNGS[slug], slug)
        self.assertEqual(P.rung_count(batch), 88)

    def test_check_REFUSES_a_missing_type(self):
        def m(batch):
            _sprob(batch, "chamomile", "aphids")["type"] = ""
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("missing id or type", out)

    def test_check_REFUSES_a_none_ladder(self):
        def m(batch):
            _sprob(batch, "borage", "powdery-mildew")["control_ladder"] = None
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("no control_ladder", out)

    def test_check_REFUSES_an_empty_ladder(self):
        def m(batch):
            _sprob(batch, "chamomile", "gray-mold")["control_ladder"] = []
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("control_ladder is EMPTY", out)

    def test_check_REFUSES_a_problem_count_off_the_read(self):
        """Parity is kept (the same problem leaves BOTH states) so only the expected-count
        branch can object."""
        pre = _pre()
        _crop(pre, "chamomile")["diseases"].pop()

        def m(batch):
            batch["chamomile"]["diseases"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(pre)
        self.assertIsNotNone(out)
        self.assertIn("5 problems, expected 6", out)

    def test_check_REFUSES_a_rung_count_off_the_read(self):
        def m(batch):
            _sprob(batch, "chamomile", "powdery-mildew")["control_ladder"].pop()
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("rungs, expected", out)

    def test_check_REFUSES_identical_registers(self):
        def m(batch):
            r = _sprob(batch, "chamomile", "aphids")["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("registers are identical", out)

    def test_check_REFUSES_a_missing_note(self):
        def m(batch):
            _sprob(batch, "chamomile", "aphids")["control_ladder"][0]["note_beginner"] = " "
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("missing or empty", out)

    def test_check_REFUSES_an_unknown_method(self):
        def m(batch):
            _sprob(batch, "chamomile", "aphids")["control_ladder"].append(_rung("ghost_method"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("not in catalog", out)

    def test_check_REFUSES_a_duplicate_method(self):
        def m(batch):
            _sprob(batch, "chamomile", "aphids")["control_ladder"].append(_rung("water_spray"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("appears twice in one ladder", out)

    def test_check_REFUSES_a_tier_decrease(self):
        def m(batch):
            lad = _sprob(batch, "chamomile", "aphids")["control_ladder"]
            lad[0], lad[-1] = lad[-1], lad[0]
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("tiers decrease", out)

    def test_check_REFUSES_an_applies_to_incoherent_rung(self):
        def m(batch):
            _sprob(batch, "chamomile", "powdery-mildew")["control_ladder"].insert(
                1, _rung("stem_collars"))
        with _Patch("staged", _staged_with(m)):
            out = P.check(_pre())
        self.assertIsNotNone(out)
        self.assertIn("cannot reach type", out)

    def test_check_REFUSES_prose_that_fails_hygiene(self):
        def m(batch):
            _sprob(batch, "chamomile", "aphids")["control_ladder"][0]["note_beginner"] += \
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
