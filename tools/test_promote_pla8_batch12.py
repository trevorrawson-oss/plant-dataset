#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_batch12.py (FALL FINISHERS). Base 1e4d0c06 (re-pinned after the trap_cropping round landed).

REPLAY-PINNED, so there is no RED phase; the evidence is the mutation harness
(tools/mutate_pla8_batch12_suite.py) plus the refusal-spec drivers here.
`VerifyPostIsDriven` is FIRST, eleventh time this arc.

THE BASE IS NOT A COMMIT. It is batch 11's replayed output, reached through
`promote_fixture.CHAIN`. `Fixture.test_base_is_reachable_and_is_batch_11s_output` pins that,
because if the chain ever resolves to something else every guard below is measuring the wrong
canonical.

THE NOVEL FAMILY IS `TaxonRulings`. Two of fava's problems have names whose obvious id is already
on the roster and belongs to a DIFFERENT ORGANISM. A guard that only required the right string
would stay green if a later pass ALSO added the wrong one, so each is pinned in both directions.

`ShippedEcho` is the second new family: brussels-sprouts is the sixth brassica authored against
five shipped siblings, and a copied-and-renamed ladder reads exactly like authored work. The
10-word threshold is measured, not guessed -- see the class docstring.

Frozen literals: the id convention, the taxon pairs, the per-crop counts and the no-material
ladders are restated here rather than imported from the promote's own tables.
"""
import copy, hashlib, json, os, sys, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_batch12 as P  # noqa: E402

POST_SHA = "7f5079aab0fa4167c87e1373b3d28d598bf2379e05e2f8e2047665eabb13b9c3"
BASE_SHA = "1e4d0c06ad28ed28642f64a3ae15b537bb7d14367b73280489ebde3befd311ae"

CROPS = ("broad-beans-fava", "brussels-sprouts", "parsley")
COUNTS = {"broad-beans-fava": (7, 33), "brussels-sprouts": (9, 49), "parsley": (6, 23)}
NEW_IDS = ("black-bean-aphid", "bean-seed-fly", "broad-bean-rust", "chocolate-spot",
           "crown-and-root-rot", "pea-and-bean-weevil")
# (right id, the wrong one a name-derived pass reaches for)
TAXON_PAIRS = (("pea-and-bean-weevil", "pea-weevil"), ("broad-bean-rust", "bean-rust"))
NO_MATERIAL = (("broad-beans-fava", "chocolate-spot"), ("broad-beans-fava", "broad-bean-rust"),
               ("broad-beans-fava", "downy-mildew"), ("brussels-sprouts", "black-rot"),
               ("parsley", "septoria-leaf-spot"))


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
    """Notes must be UNIQUE per call. A fixed placeholder makes two injected rungs byte-identical,
    so the within-batch duplicate-note check fires before whichever guard the test is driving."""
    _UNIQ[0] += 1
    n = _UNIQ[0]
    return {"method": m, "note_beginner": f"injected beginner {n}",
            "note_seasoned": f"injected seasoned {n}"}


class VerifyPostIsDriven(unittest.TestCase):
    """Every verify_post branch, doctored on the POST state. Written before the guards."""

    def _staged(self):
        pre = _pre()
        return pre, P.snapshot(pre), _post(pre)

    def test_trap_cropping_on_the_wrong_problem_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "parsley", "parsleyworm")["control_ladder"].insert(0, _rung("trap_cropping"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("reverse a conservation instruction", problem)

    def test_losing_the_trap_rung_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        p = _prob(post, *P.TRAP_OK)
        p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "trap_cropping"]
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("lost its trap_cropping rung", problem)

    def test_trap_rung_placement_guard_runs_on_the_post(self):
        """Moving it off index 1 keeps the ladder tier-legal (cultural before physical), so nothing
        else would notice; only this pin does."""
        pre, snap, post = self._staged()
        p = _prob(post, *P.TRAP_OK)
        lad = p["control_ladder"]
        rung = lad.pop(lad.index(next(r for r in lad if r["method"] == "trap_cropping")))
        lad.insert(0, rung)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("not 1", problem)

    def test_pyrethroid_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "brussels-sprouts", "harlequin-bug")["control_ladder"].append(
            _rung("pyrethroid"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("synthetic pyrethroid", problem)

    def test_handpick_scoping_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "broad-beans-fava", "black-bean-aphid")["control_ladder"].insert(
            0, _rung("handpick"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("tissue-removal target", problem)

    def test_timing_rung_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "brussels-sprouts", "clubroot")["control_ladder"].insert(
            0, _rung("planting_time_avoidance"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("unearned timing rung", problem)

    def test_banned_note_words_guard_runs_on_the_post(self):
        for word in ("trap crop", "sacrificial", "relocate", "diatomaceous"):
            pre, snap, post = self._staged()
            _prob(post, "parsley", "parsleyworm")["control_ladder"][0]["note_seasoned"] += (
                f" Try a {word} approach.")
            problem = P.verify_post(snap, post)
            self.assertIsNotNone(problem, word)
            self.assertIn("a note mentions", problem)

    def test_no_material_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "broad-beans-fava", "broad-bean-rust")["control_ladder"].append(_rung("sulfur"))
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("its prose rules out", problem)

    def test_taxon_required_id_guard_runs_on_the_post(self):
        """Branch 1 ALONE: the ruled id goes missing without the refused one appearing.

        The original version of this test renamed the problem straight to `pea-weevil`, which
        satisfies BOTH branches, and asserted `A or B`. Either branch could then be disabled with
        the other still answering, and the harness reported both as survivors. Assert one branch
        per test, and drive only that branch."""
        pre, snap, post = self._staged()
        _prob(post, "broad-beans-fava", "pea-and-bean-weevil")["id"] = "sitona-weevil"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("not on the roster", problem)

    def test_taxon_wrong_organism_guard_runs_on_the_post(self):
        """Branch 2 ALONE: the ruled id STAYS and a second problem also takes the refused one.

        The carrier must be a problem in NEITHER `TIMING_OK` NOR `NO_MATERIAL`, since both of those
        guards key on (slug, pid) and answer before the taxon loop -- renaming a member of either
        makes THAT guard fire instead. `root-rots-damping-off` is fava's only free problem."""
        pre, snap, post = self._staged()
        _prob(post, "broad-beans-fava", "root-rots-damping-off")["id"] = "pea-weevil"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("the wrong organism", problem)

    def test_parsleyworm_join_guard_runs_on_the_post(self):
        pre, snap, post = self._staged()
        _prob(post, "parsley", "parsleyworm")["id"] = "parsley-worm"
        with _Patch("HANDPICK_OK", P.HANDPICK_OK + ("parsley-worm",)):
            problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("dill's id", problem)

    def test_empty_post_ladder_is_caught(self):
        pre, snap, post = self._staged()
        _prob(post, "parsley", "aphids")["control_ladder"] = []
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("no ladder after promote", problem)

    def test_added_crop_is_caught_set_equality_first(self):
        pre, snap, post = self._staged()
        ghost = copy.deepcopy(post["crops"][0])
        ghost["slug"] = "ghost-crop"
        post["crops"].append(ghost)
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("crop set changed", problem)

    def test_added_method_is_caught(self):
        pre, snap, post = self._staged()
        post["control_methods"]["ghost"] = copy.deepcopy(post["control_methods"]["handpick"])
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("gained or lost a key", problem)

    def test_ANY_method_edit_is_caught_this_batch_mutates_none(self):
        """Stricter than its siblings: no key is exempt, because none is widened."""
        pre, snap, post = self._staged()
        post["control_methods"]["certified_clean_stock"]["best_use"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("mutates no catalog entry", problem)

    def test_bystander_crop_edit_is_caught(self):
        pre, snap, post = self._staged()
        _crop(post, "cabbage")["name"] = "MUTATED"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("touches only", problem)

    def test_source_edit_is_caught(self):
        pre, snap, post = self._staged()
        post["source_catalog"]["umn_ext"]["tier"] = "T2"
        problem = P.verify_post(snap, post)
        self.assertIsNotNone(problem)
        self.assertIn("source_catalog changed", problem)


class Fixture(unittest.TestCase):
    def test_base_is_reachable_and_is_batch_11s_output(self):
        raw = promote_fixture.pre_state(P.BASE_SHA)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), BASE_SHA)
        data = json.loads(raw)
        ids = {p["id"] for c in data["crops"] for _, p in P.problems(c) if p.get("id")}
        self.assertIn("parsleyworm", ids, "the base must already carry batch 11's dill mint")
        self.assertIn("stem-and-bulb-nematode", ids, "the base must be batch 11's output")
        self.assertIn("trap_cropping", data["control_methods"],
                      "the base must post-date the trap_cropping mint; brussels carries that rung")

    def test_post_sha_is_pinned_and_replayed(self):
        d = _post()
        self.assertEqual(hashlib.sha256(P.serialize(d)).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        """Prose legitimately contains ", ", so a substring scan is the wrong test. Round-trip
        against the canonical separators instead."""
        out = P.serialize(_post())
        expect = json.dumps(json.loads(out), ensure_ascii=False,
                            separators=(",", ":")).encode("utf-8")
        self.assertEqual(out, expect)
        self.assertFalse(out.endswith(b"\n"))

    def test_clean_batch_passes_check(self):
        self.assertIsNone(P.check(_pre()))

    def test_promote_is_idempotent_refusing(self):
        """Re-running on its own output must refuse: the crops are already laddered."""
        problem = P.check(_post())
        self.assertIsNotNone(problem)
        self.assertIn("already", problem)


class TaxonRulings(unittest.TestCase):
    """The novel family. Both directions, because requiring the right id alone stays green if a
    later pass also introduces the wrong one under a second problem."""

    def test_the_ruled_ids_are_the_ones_shipped(self):
        d = _post()
        fava = {p["id"] for _, p in P.problems(_crop(d, "broad-beans-fava"))}
        for right, wrong in TAXON_PAIRS:
            self.assertIn(right, fava)
            self.assertNotIn(wrong, fava)

    def test_the_refused_ids_belong_to_other_crops_and_other_organisms(self):
        """The refusal is not stylistic: the wrong strings are live on other crops."""
        base = _pre()
        owners = {}
        for c in base["crops"]:
            for _, p in P.problems(c):
                if p.get("id") in ("pea-weevil", "bean-rust"):
                    owners.setdefault(p["id"], []).append(c["slug"])
        self.assertEqual(sorted(owners["pea-weevil"]), ["snow-peas", "sugar-snap-peas"])
        self.assertEqual(sorted(owners["bean-rust"]),
                         ["dry-bean", "green-beans-bush", "pole-beans"])

    def _wrong_id_also_present(self, carrier_name, carrier_id, wrong):
        """The WRONG-ORGANISM branch, driven the way it would really fail: the ruled id stays and a
        later pass ALSO introduces the refused one on another problem. Renaming the ruled problem
        instead trips the "requires id" branch first, which is a different assertion.

        The convention table is patched alongside, because with it intact the id-convention loop
        answers before the taxon loop -- that layering is pinned by its own test below.
        """
        table = dict(P.ID_CONVENTION)
        table[carrier_name] = wrong

        def m(b):
            _sprob(b, "broad-beans-fava", carrier_id)["id"] = wrong
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("WRONG ORGANISM", problem)
        return problem

    def test_reusing_pea_weevil_is_refused(self):
        problem = self._wrong_id_also_present("Bean seed fly", "bean-seed-fly", "pea-weevil")
        self.assertIn("Sitona lineatus", problem)

    def test_reusing_bean_rust_is_refused(self):
        problem = self._wrong_id_also_present("Chocolate spot", "chocolate-spot", "bean-rust")
        self.assertIn("viciae-fabae", problem)

    def test_dropping_a_ruled_id_altogether_is_refused(self):
        """The other branch: the ruled id must be PRESENT, not merely un-contradicted."""
        table = dict(P.ID_CONVENTION)
        table["Broad bean rust"] = "fava-rust"

        def m(b):
            _sprob(b, "broad-beans-fava", "broad-bean-rust")["id"] = "fava-rust"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("requires id", problem)

    def test_the_taxon_guard_is_masked_by_the_convention_table_and_that_is_why_it_exists(self):
        """Pins the layering: with the table intact the convention loop answers first. The taxon
        guard is the backstop for the table itself being edited, not a duplicate of it."""
        def m(b):
            _sprob(b, "broad-beans-fava", "pea-and-bean-weevil")["id"] = "pea-weevil"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("ids are join keys", problem)

    def test_root_rots_damping_off_IS_reused_not_minted(self):
        """The third id in the same family, ruled the other way: reuse, not mint."""
        d = _post()
        p = _prob(d, "broad-beans-fava", "root-rots-damping-off")
        self.assertEqual(p["name"], "Root rots and seed decay")
        base = _pre()
        others = [c["slug"] for c in base["crops"]
                  for _, q in P.problems(c) if q.get("id") == "root-rots-damping-off"]
        self.assertEqual(sorted(others), ["snow-peas", "sugar-snap-peas"])


class CrossBatchJoin(unittest.TestCase):
    def test_parsley_reuses_dills_parsleyworm(self):
        d = _post()
        self.assertEqual(_prob(d, "parsley", "parsleyworm")["id"],
                         _prob(d, "dill", "parsleyworm")["id"])

    def test_parsleyworm_is_not_listed_as_new(self):
        self.assertNotIn("parsleyworm", P.NEW_IDS)

    def test_a_divergent_parsleyworm_id_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "parsleyworm")["id"] = "black-swallowtail-caterpillar"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("ids are join keys", problem)

    def test_parsley_dropping_the_shared_id_is_refused(self):
        """The check-side half. With the convention table intact the id loop answers first, so the
        table is patched alongside -- the same layering as the taxon guard: this is the backstop
        for a table edit, not a duplicate of the table."""
        table = dict(P.ID_CONVENTION)
        table["Parsleyworm (black swallowtail caterpillar)"] = "swallowtail-larvae"

        def m(b):
            _sprob(b, "parsley", "parsleyworm")["id"] = "swallowtail-larvae"
        with _Patch("ID_CONVENTION", table), _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("parsley does not carry", problem)

    def test_a_base_without_dills_mint_is_refused(self):
        """If the chain ever resolves to a canonical predating batch 11, this must fail loud."""
        pre = _pre()
        for _, p in P.problems(_crop(pre, "dill")):
            if p.get("id") == "parsleyworm":
                p["id"] = "something-else"
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("sitting on the wrong canonical", problem)


class IdConvention(unittest.TestCase):
    def test_every_problem_takes_its_table_id(self):
        d = _post()
        for slug in CROPS:
            for _, p in P.problems(_crop(d, slug)):
                self.assertEqual(p["id"], P.ID_CONVENTION[p["name"]], f"{slug}/{p['name']}")

    def test_new_ids_are_exactly_the_ones_new_to_the_base(self):
        base_ids = {p["id"] for c in _pre()["crops"] for _, p in P.problems(c) if p.get("id")}
        shipped = {p["id"] for slug in CROPS for _, p in P.problems(_crop(_post(), slug))}
        self.assertEqual(sorted(shipped - base_ids), sorted(NEW_IDS))

    def test_an_id_off_the_convention_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "aphids")["id"] = "parsley-aphids"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("ids are join keys", problem)

    def test_a_problem_name_missing_from_the_table_is_refused(self):
        """Branch 1: `want is None`. The id-divergence test drives branch 2 only, so this branch
        had no driver and survived its mutation."""
        table = {k: v for k, v in P.ID_CONVENTION.items() if k != "Aphids"}
        with _Patch("ID_CONVENTION", table):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not in the id-convention table", problem)

    def test_brussels_reuses_the_whole_brassica_convention(self):
        """Nine ids, zero mints: the payoff for laddering the family before its stragglers."""
        base_ids = {p["id"] for c in _pre()["crops"] for _, p in P.problems(c) if p.get("id")}
        d = _post()
        for _, p in P.problems(_crop(d, "brussels-sprouts")):
            self.assertIn(p["id"], base_ids, f"brussels-sprouts minted {p['id']!r}")

    def test_a_new_id_already_on_the_roster_is_refused(self):
        pre = _pre()
        _prob(pre, "cabbage", "clubroot")["id"] = "chocolate-spot"
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already on the roster", problem)


class ReadFixes(unittest.TestCase):
    def test_no_material_rung_on_the_five_ruled_ladders(self):
        d = _post()
        cm = d["control_methods"]
        for slug, pid in NO_MATERIAL:
            for r in _prob(d, slug, pid)["control_ladder"]:
                self.assertNotIn(cm[r["method"]]["tier"], P.MATERIAL_TIERS, f"{slug}/{pid}")

    def test_a_fungicide_on_a_no_material_ladder_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "septoria-leaf-spot")["control_ladder"].append(
                _rung("copper_fungicide"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("no home fungicide is available", problem)

    def test_broad_bean_rust_diverges_from_its_sibling_id_deliberately(self):
        """dry-bean's `bean-rust` CARRIES sulfur; this crop's prose refuses it. The divergence is
        the point, so pin both halves."""
        base = _pre()
        sib = [r["method"] for c in base["crops"] if c["slug"] == "dry-bean"
               for _, p in P.problems(c) if p.get("id") == "bean-rust"
               for r in p["control_ladder"]]
        self.assertIn("sulfur", sib)
        mine = [r["method"] for r in _prob(_post(), "broad-beans-fava",
                                           "broad-bean-rust")["control_ladder"]]
        self.assertNotIn("sulfur", mine)

    def test_the_tip_pinch_is_sanitation_not_handpick(self):
        lad = [r["method"] for r in _prob(_post(), "broad-beans-fava",
                                          "black-bean-aphid")["control_ladder"]]
        self.assertIn("garden_sanitation", lad)
        self.assertNotIn("handpick", lad)

    def test_dropping_the_pinch_rung_is_refused(self):
        def m(b):
            p = _sprob(b, "broad-beans-fava", "black-bean-aphid")
            p["control_ladder"] = [r for r in p["control_ladder"]
                                   if r["method"] != "garden_sanitation"]
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("primary control", problem)

    def test_the_seed_fly_note_carries_only_the_timing_mechanism(self):
        p = _prob(_post(), "broad-beans-fava", "bean-seed-fly")
        self.assertEqual([r["method"] for r in p["control_ladder"]], ["planting_time_avoidance"])
        blob = " ".join(r["note_beginner"] + " " + r["note_seasoned"]
                        for r in p["control_ladder"]).lower()
        for word in P.SEED_FLY_BANNED:
            self.assertNotIn(word, blob)

    def test_the_stripped_residue_clause_cannot_return(self):
        def m(b):
            _sprob(b, "broad-beans-fava", "bean-seed-fly")["control_ladder"][0]["note_seasoned"] += (
                " Let coarse residue or manure break down ahead of sowing.")
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("smuggles an unplaceable control", problem)

    def test_the_bt_rung_hedges_and_states_non_selectivity(self):
        p = _prob(_post(), "parsley", "parsleyworm")
        bt = [r for r in p["control_ladder"] if r["method"] == "bt"]
        self.assertEqual(len(bt), 1)
        for k in ("note_beginner", "note_seasoned"):
            low = bt[0][k].lower()
            self.assertTrue(any(h in low for h in P.BT_HEDGES), k)
            self.assertIn(P.BT_NONSELECTIVE, low, k)

    def test_an_unhedged_bt_rung_is_refused(self):
        def m(b):
            for r in _sprob(b, "parsley", "parsleyworm")["control_ladder"]:
                if r["method"] == "bt":
                    r["note_beginner"] = ("Bt is a bacterial spray for caterpillars and acts on "
                                          "caterpillars as a group. Apply it after hand-picking.")
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("lost its hedge", problem)

    def test_a_bt_rung_dropping_the_non_selectivity_warning_is_refused(self):
        def m(b):
            for r in _sprob(b, "parsley", "parsleyworm")["control_ladder"]:
                if r["method"] == "bt":
                    r["note_seasoned"] = "Seldom warranted on this crop, but it works when needed."
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("caterpillars as a group", problem)

    def test_timing_rungs_only_where_the_prose_recommends_the_shift(self):
        d = _post()
        got = set()
        for slug in CROPS:
            for _, p in P.problems(_crop(d, slug)):
                if any(r["method"] == "planting_time_avoidance" for r in p["control_ladder"]):
                    got.add((slug, p["id"]))
        self.assertEqual(got, set(P.TIMING_OK))

    def test_an_unearned_timing_rung_is_refused(self):
        def m(b):
            _sprob(b, "brussels-sprouts", "cabbage-root-maggot")["control_ladder"].insert(
                0, _rung("planting_time_avoidance"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not a recommendation", problem)

    def test_parsleys_relocation_stays_unplaced(self):
        """A documented exclusion from the trap-cropping round: the larvae end ALIVE."""
        d = _post()
        for slug in CROPS:
            for _, p in P.problems(_crop(d, slug)):
                for r in p["control_ladder"]:
                    low = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                    for word in P.NOTE_BANNED:
                        self.assertNotIn(word, low, f"{slug}/{p['id']}/{r['method']}")

    def test_brussels_carries_the_trap_cropping_rung_at_the_end_of_the_cultural_run(self):
        lad = [r["method"] for r in _prob(_post(), *P.TRAP_OK)["control_ladder"]]
        self.assertEqual(lad.index("trap_cropping"), P.TRAP_INDEX)
        self.assertEqual(lad[0], "garden_sanitation")
        self.assertEqual(lad[P.TRAP_INDEX + 1], "floating_row_cover")

    def test_the_trap_rung_names_cleome_or_mustard_and_restates_the_removal(self):
        """DESTROY_STATED: this crop's prose carries the removal step, so the rung must too, and it
        may use the attribution phrase the round's DIVERT_ONLY rungs are denied."""
        r = next(x for x in _prob(_post(), *P.TRAP_OK)["control_ladder"]
                 if x["method"] == "trap_cropping")
        blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
        self.assertIn("cleome", blob)
        self.assertIn("mustard", blob)
        self.assertIn("destroy", blob)
        self.assertIn("this crop's guidance", blob)
        self.assertIn("cautions", blob, "the deadline is pointed at, not restated")
        for wrong in ("nasturtium", "rapeseed", "collard"):
            self.assertNotIn(wrong, blob, "name only what this crop's own prose names")

    def test_trap_cropping_on_any_other_problem_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "parsleyworm")["control_ladder"].insert(0, _rung("trap_cropping"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("conservation", problem)

    def test_dropping_the_trap_rung_is_refused(self):
        def m(b):
            p = _sprob(b, "brussels-sprouts", "harlequin-bug")
            p["control_ladder"] = [r for r in p["control_ladder"] if r["method"] != "trap_cropping"]
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("rungs, expected", problem)

    def test_the_note_ban_exemption_is_scoped_to_that_one_rung(self):
        """The ban keeps parsley's conservation language out; it must not muzzle a real trap note."""
        self.assertEqual(P.NOTE_BAN_EXEMPT,
                         (("brussels-sprouts", "harlequin-bug", "trap_cropping"),))

        def m(b):
            _sprob(b, "brussels-sprouts", "cabbage-aphids")["control_ladder"][0]["note_seasoned"] += (
                " Use a trap crop.")
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("a note mentions", problem)

    def test_handpick_on_a_tissue_removal_target_is_refused_by_check(self):
        """The verify_post twin of this was driven; the check-side branch was not, and survived."""
        def m(b):
            _sprob(b, "broad-beans-fava", "black-bean-aphid")["control_ladder"].insert(
                0, _rung("handpick"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("catching free-living", problem)

    def test_a_pyrethroid_rung_is_refused_by_check(self):
        def m(b):
            _sprob(b, "brussels-sprouts", "harlequin-bug")["control_ladder"].append(
                _rung("pyrethroid"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("synthetic pyrethroid", problem)

    def test_brussels_uses_pyrethrin_never_the_synthetic(self):
        lad = [r["method"] for r in _prob(_post(), "brussels-sprouts",
                                          "harlequin-bug")["control_ladder"]]
        self.assertIn("pyrethrin", lad)
        self.assertNotIn("pyrethroid", lad)


class BasePremises(unittest.TestCase):
    def test_a_base_predating_the_trap_cropping_mint_is_refused(self):
        """INVERTED when the parallel round landed. Before, this refused a base CONTAINING the key,
        because the batch carried no rung and brussels would have shipped silently wrong. Now the
        rung exists, so a base WITHOUT the key would fail it as an unknown method."""
        pre = _pre()
        del pre["control_methods"]["trap_cropping"]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("predates the mint", problem)

    def test_the_catalog_is_untouched_end_to_end(self):
        pre = _pre()
        post = _post(pre)
        self.assertEqual(json.dumps(pre["control_methods"], sort_keys=True),
                         json.dumps(post["control_methods"], sort_keys=True))

    def test_an_already_laddered_crop_is_refused(self):
        pre = _pre()
        _crop(pre, "parsley")["pests"][0]["control_ladder"] = [_rung("handpick")]
        problem = P.check(pre)
        self.assertIsNotNone(problem)
        self.assertIn("already laddered", problem)


class ShippedEcho(unittest.TestCase):
    """brussels-sprouts is the SIXTH brassica; parsley the third umbellifer authored this week.

    THRESHOLD IS MEASURED, NOT GUESSED. Against this base the batch shares exactly two sentences
    with shipped notes: "Go easy on nitrogen fertilizer." (5 words, 9 occurrences in the base) and
    "Water the soil rather than the leaves." (7 words, 6 occurrences). Both are house phrasing. The
    four sentences parsley originally shared with cilantro each occurred ONCE, which is the
    signature of an echo of one specific crop rather than a house phrase; they were rewritten.
    """

    def test_no_note_is_byte_identical_to_a_shipped_one(self):
        self.assertIsNone(P.check_no_shipped_echo(P.staged(), _pre()))

    def test_the_surviving_shared_sentences_are_house_phrases(self):
        base = _pre()
        _, sent = P.shipped_notes(base)
        shared = []
        for slug in CROPS:
            for _, p in P.problems(json.loads(json.dumps(P.staged()[slug]))):
                for r in p["control_ladder"]:
                    for k in ("note_beginner", "note_seasoned"):
                        for s in P.sentences(r[k]):
                            if s in sent:
                                shared.append(s)
        self.assertTrue(shared, "expected the house phrases to still be shared")
        for s in shared:
            self.assertLess(len(s.split()), P.ECHO_MIN_WORDS, s)

    def test_a_copied_shipped_note_is_refused(self):
        base = _pre()
        donor = _prob(base, "cabbage", "harlequin-bug")["control_ladder"][0]["note_beginner"]

        def m(b):
            _sprob(b, "brussels-sprouts", "harlequin-bug")["control_ladder"][0]["note_beginner"] = donor
        with _Patch("staged", _staged_with(m)):
            problem = P.check(base)
        self.assertIsNotNone(problem)
        self.assertIn("byte-identical to the shipped", problem)

    def test_a_long_shared_sentence_is_refused(self):
        base = _pre()
        donor = None
        for s in P.sentences(_prob(base, "cabbage", "clubroot")["control_ladder"][0]["note_seasoned"]):
            if len(s.split()) >= P.ECHO_MIN_WORDS:
                donor = s
                break
        self.assertIsNotNone(donor, "the donor crop must supply a long enough sentence")

        def m(b):
            _sprob(b, "brussels-sprouts", "clubroot")["control_ladder"][0]["note_seasoned"] += " " + donor
        with _Patch("staged", _staged_with(m)):
            problem = P.check(base)
        self.assertIsNotNone(problem)
        self.assertIn("echo, not house phrasing", problem)

    def test_within_batch_duplicate_notes_are_refused(self):
        def m(b):
            donor = _sprob(b, "parsley", "aphids")["control_ladder"][0]["note_beginner"]
            _sprob(b, "broad-beans-fava", "black-bean-aphid")["control_ladder"][0]["note_beginner"] = donor
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("within this batch", problem)

    def test_shipped_notes_reader_tolerates_rungs_with_no_seasoned_register(self):
        """53 rungs across 5 early crops carry no note_seasoned and nothing gates the field.
        Indexing rather than .get() would crash the guard on data that is merely old."""
        base = _pre()
        missing = [1 for c in base["crops"] for _, p in P.problems(c)
                   for r in p.get("control_ladder") or [] if "note_seasoned" not in r]
        self.assertGreater(len(missing), 0, "if this is 0 the backfill happened; re-check the guard")
        whole, sent = P.shipped_notes(base)
        self.assertTrue(whole and sent)


class Twins(unittest.TestCase):
    """Both refusals shipped with no driver at all and survived their mutations."""

    def test_two_crops_with_identical_canonical_prose_are_refused(self):
        base = _pre()
        donor = _crop(base, "broad-beans-fava")
        target = _crop(base, "parsley")
        target["pests"] = copy.deepcopy(donor.get("pests") or [])
        target["diseases"] = copy.deepcopy(donor.get("diseases") or [])
        problem = P.check_not_twins({s: _crop(base, s) for s in CROPS}, P.staged())
        self.assertIsNotNone(problem)
        self.assertIn("TRUE TWIN", problem)

    def test_two_byte_identical_staged_files_are_refused(self):
        dg = P.staged_digests()
        dg["parsley"] = dg["broad-beans-fava"]
        with _Patch("staged_digests", lambda: dg):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("was copied", problem)


class SchemaCoverage(unittest.TestCase):
    def test_all_three_crops_use_the_classic_schema(self):
        base = _pre()
        for slug in CROPS:
            seen = set()
            for _, p in P.problems(_crop(base, slug)):
                seen |= set(p.keys())
            self.assertIn("organic_treatment_seasoned", seen, slug)
            self.assertNotIn("management_seasoned", seen, slug)

    def test_prose_fields_reach_the_advice_half_of_every_record(self):
        self.assertIsNone(P.check_schema_coverage({s: _crop(_pre(), s) for s in CROPS}))

    def test_a_prose_field_list_missing_the_advice_half_is_refused(self):
        with _Patch("PROSE_FIELDS", ("name", "severity", "cause_beginner", "cause_seasoned")):
            problem = P.check_schema_coverage({s: _crop(_pre(), s) for s in CROPS})
        self.assertIsNotNone(problem)
        self.assertIn("advice-bearing", problem)

    def _stripped_of_advice(self):
        base = _pre()
        for _, p in P.problems(_crop(base, "parsley")):
            for f in P.ADVICE_FIELDS:
                p.pop(f, None)
        return base

    def test_a_crop_with_no_advice_field_at_all_is_refused(self):
        """Branch 1 of check_schema_coverage. The PROSE_FIELDS test drives branch 2 only."""
        base = self._stripped_of_advice()
        problem = P.check_schema_coverage({s: _crop(base, s) for s in CROPS})
        self.assertIsNotNone(problem)
        self.assertIn("no advice-bearing prose field", problem)

    def test_the_twins_check_actually_CALLS_the_schema_coverage_check(self):
        """Calling check_schema_coverage directly cannot notice its call site being removed, which
        is how `problem = None` at the call site survived."""
        base = self._stripped_of_advice()
        problem = P.check_not_twins({s: _crop(base, s) for s in CROPS}, P.staged())
        self.assertIsNotNone(problem)
        self.assertIn("no advice-bearing prose field", problem)

    def test_a_crop_arriving_in_the_newer_schema_is_refused(self):
        base = _pre()
        for _, p in P.problems(_crop(base, "parsley")):
            p["management_seasoned"] = p.pop("organic_treatment_seasoned", "x")
        problem = P.check_schema_coverage({s: _crop(base, s) for s in CROPS})
        self.assertIsNotNone(problem)
        self.assertIn("classic", problem)


class Validate(unittest.TestCase):
    def test_counts_are_exact(self):
        d = _post()
        for slug, (np_, nr) in COUNTS.items():
            probs = P.problems(_crop(d, slug))
            self.assertEqual(len(probs), np_, slug)
            self.assertEqual(sum(len(p["control_ladder"]) for _, p in probs), nr, slug)

    def test_total_rungs(self):
        self.assertEqual(sum(n for _, n in COUNTS.values()), 105)

    def test_unknown_method_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "aphids")["control_ladder"][0]["method"] = "moon_phase_planting"
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("not in catalog", problem)

    def test_tier_decrease_is_refused(self):
        def m(b):
            p = _sprob(b, "parsley", "aphids")
            p["control_ladder"] = list(reversed(p["control_ladder"]))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("tiers decrease", problem)

    def test_applies_to_incoherence_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "septoria-leaf-spot")["control_ladder"].append(_rung("bt"))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("cannot reach type", problem)

    def test_identical_registers_are_refused(self):
        def m(b):
            r = _sprob(b, "parsley", "aphids")["control_ladder"][0]
            r["note_seasoned"] = r["note_beginner"]
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("registers are identical", problem)

    def test_empty_ladder_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "aphids")["control_ladder"] = []
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("EMPTY", problem)

    def test_duplicate_method_in_one_ladder_is_refused(self):
        def m(b):
            p = _sprob(b, "parsley", "aphids")
            p["control_ladder"].append(_rung(p["control_ladder"][-1]["method"]))
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("appears twice", problem)

    def test_a_wrong_rung_count_is_refused(self):
        def m(b):
            p = _sprob(b, "parsley", "aphids")
            p["control_ladder"] = p["control_ladder"][:-1]
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("rungs, expected", problem)

    def test_an_empty_note_is_refused(self):
        def m(b):
            _sprob(b, "parsley", "aphids")["control_ladder"][0]["note_seasoned"] = "   "
        with _Patch("staged", _staged_with(m)):
            problem = P.check(_pre())
        self.assertIsNotNone(problem)
        self.assertIn("missing or empty", problem)


if __name__ == "__main__":
    unittest.main(verbosity=2)
