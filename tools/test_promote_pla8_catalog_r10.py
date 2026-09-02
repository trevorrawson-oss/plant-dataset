#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_catalog_r10.py. Base e6c986e3 (batch 23, a commit).

REPLAY-PINNED; no RED phase is claimed. The evidence these guards are LIVE is `VerifyPostIsDriven`
plus tools/mutate_pla8_catalog_r9_suite.py.

WHAT IS NEW versus r7 and r8, whose guard shape this INVERTS:

* r7 and r8 both asserted "no existing method is touched". This round touches one on purpose, so
  `WideningIsAdditive` drives the opposite protection: one method changes, `applies_to` only gains,
  and **every claim the method already made survives** -- 86 shipped rungs were authored against
  that text.
* `UnblocksItsCase` drives an assertion neither prior round needed: a widening whose target does not
  actually reach its case is a no-op that reads as progress. Legality is re-derived from
  `TYPE_TARGETS`, not inferred from the target string.
* `MainIsWiredToTheGuards` is carried forward from r8, where the harness proved a suite can drive
  every branch of `check` and still not prove `main` CALLS it.
"""
import copy, hashlib, json, os, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_fixture  # noqa: E402
import promote_pla8_catalog_r10 as P  # noqa: E402
import build_pla8_catalog_r10_content as C  # noqa: E402
import control_ladder_gate as CLG  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

POST_SHA = "c24d7754e9d708b09169b5b8979f1f63bdd35b14cd77e0adf86ba03b88870c6f"
KEY = "certified_clean_stock"


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _post(pre=None):
    d = copy.deepcopy(pre if pre is not None else _pre())
    P.apply_to(d)
    return d


class _Patch:
    def __init__(self, name, value, mod=C):
        self.n, self.v, self.m = name, value, mod

    def __enter__(self):
        self.old = getattr(self.m, self.n)
        setattr(self.m, self.n, self.v)
        return self

    def __exit__(self, *exc):
        setattr(self.m, self.n, self.old)
        return False


def _wide(**over):
    w = copy.deepcopy(C.WIDENINGS)
    for key, (field, value) in over.items():
        w[key][field] = value
    return w


def _run_main(path, apply_=False):
    argv = sys.argv
    sys.argv = ["promote_pla8_catalog_r10.py", path] + (["--apply"] if apply_ else [])
    try:
        P.main()
    finally:
        sys.argv = argv


def _prob(data, slug, pid):
    crop = next(c for c in data["crops"] if c.get("slug") == slug)
    for fam in ("pests", "diseases"):
        for p in crop.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    raise AssertionError(f"{slug}/{pid} not found")


# ---------------------------------------------------------------- liveness first
class VerifyPostIsDriven(unittest.TestCase):
    def test_clean_apply_passes(self):
        pre = _pre()
        d = copy.deepcopy(pre)
        snap = P.snapshot(d)
        P.apply_to(d)
        self.assertIsNone(P.verify_post(snap, d))

    def test_a_second_method_changing_is_caught(self):
        """THE core inversion: r8 forbade ANY method change; this round permits exactly one."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"]["garden_sanitation"]["tier"] = "physical"
        msg = P.verify_post(snap, d)
        self.assertIn("methods changed", msg)
        self.assertIn("garden_sanitation", msg)

    def test_a_minted_method_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"]["ghost_method"] = {"name": "Ghost"}
        self.assertIn("method SET changed", P.verify_post(snap, d))

    def test_a_dropped_method_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        del d["control_methods"]["garden_sanitation"]
        self.assertIn("method SET changed", P.verify_post(snap, d))

    def test_an_undeclared_source_catalog_addition_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["source_catalog"]["ghost_src"] = {"name": "G", "tier": "T1"}
        self.assertIn("expected exactly", P.verify_post(snap, d))

    def test_a_DROPPED_source_catalog_entry_is_caught(self):
        """r9 could compare source_catalog as one blob because it added nothing. This round adds
        one, so a drop has to be caught on its own; a blob comparison cannot tell add from drop."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        del d["source_catalog"]["cornell_ext"]
        self.assertIn("source_catalog DROPPED", P.verify_post(snap, d))

    def test_a_MODIFIED_existing_source_catalog_entry_is_caught(self):
        """The set comparison passes when an existing entry is edited in place, so the per-key value
        comparison is what carries this. Editing a source's url under a widening would silently
        repoint every claim that cites it."""
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["source_catalog"]["cornell_ext"] = dict(d["source_catalog"]["cornell_ext"],
                                                  url="https://example.invalid/moved")
        self.assertIn("was MODIFIED", P.verify_post(snap, d))

    def test_a_crop_change_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["crops"][0]["slug"] = "mutated-crop"
        self.assertIn("a crop changed", P.verify_post(snap, d))


class Fixture(unittest.TestCase):
    def test_pre_state_matches_base_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_is_this_promotes_own_output(self):
        self.assertEqual(hashlib.sha256(P.serialize(_post())).hexdigest(), POST_SHA)

    def test_base_sha_is_enforced(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(b'{"crops":[]}')
        try:
            with self.assertRaises(SystemExit) as cm:
                _run_main(path)
            self.assertIn("base SHA", str(cm.exception))
        finally:
            os.unlink(path)

    def test_nothing_is_minted(self):
        pre, post = _pre(), _post()
        self.assertEqual(len(post["control_methods"]), len(pre["control_methods"]))
        self.assertEqual(len(post["control_methods"]), P.EXPECTED_METHOD_COUNT)

    def test_clean_check_passes(self):
        self.assertIsNone(P.check(_pre()))


class WideningIsAdditive(unittest.TestCase):
    """37 shipped rungs point at this method. A widening is additive or it is a rewrite."""

    def test_the_93_existing_rungs_are_real(self):
        pre = _pre()
        n = sum(1 for c in pre["crops"] for fam in ("pests", "diseases")
                for p in c.get(fam) or [] if isinstance(p, dict)
                for r in p.get("control_ladder") or [] if r["method"] == KEY)
        self.assertEqual(n, 93)

    def test_applies_to_only_gains(self):
        pre, post = _pre(), _post()
        before = pre["control_methods"][KEY]["applies_to"]
        after = post["control_methods"][KEY]["applies_to"]
        self.assertEqual(before, ["viral", "bacterial", "fungal_foliar", "fungal_soilborne",
                                  "disease_general", "nematode"])
        self.assertEqual(after, ["viral", "bacterial", "fungal_foliar", "fungal_soilborne",
                                 "disease_general", "nematode", "insect_general"])
        for t in before:
            self.assertIn(t, after)

    def test_losing_an_existing_target_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"][KEY]["applies_to"] = ["bacterial"]
        self.assertIn("LOST applies_to", P.verify_post(snap, d))

    def test_gaining_an_undeclared_target_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        # a target NOT already present, or this appends a no-op and verify_post sees no gain
        d["control_methods"][KEY]["applies_to"].append("mollusk")
        self.assertIn("expected exactly", P.verify_post(snap, d))

    def test_every_surviving_claim_is_present_after(self):
        post = _post()
        blob = " ".join(P.prose_of(post["control_methods"][KEY])).lower()
        for f in C.MUST_SURVIVE[KEY]:
            self.assertIn(f.lower(), blob, f)

    def test_the_must_survive_table_itself_is_pinned(self):
        """A COVERAGE assertion, not an overlap one. Iterating whatever the table happens to hold
        cannot notice an entry being deleted from it -- the loop simply checks fewer things and
        stays green, which is how a guard hollows out one line at a time."""
        self.assertEqual(set(C.MUST_SURVIVE), {KEY})
        self.assertEqual(set(C.MUST_SURVIVE[KEY]),
                         {"tested or treated seed", "cuttings, crowns or divisions",
                          "Basil downy mildew is seed-borne", "gelatinous exudate in water",
                          "Artichoke curly dwarf",
                          "stem and bulb nematode arrives inside infected garlic cloves",
                          "seed-borne foliar and vascular pathogens",
                          "Set once, at purchase or propagation", "pathogen-tested",
                          "steam or hot-water treated"})

    def test_dropping_a_surviving_claim_is_refused_at_check(self):
        w = _wide(certified_clean_stock=("set_fields", dict(
            C.WIDENINGS[KEY]["set_fields"],
            best_use="Steady soil moisture, and half of common scab control on potatoes.")))
        with _Patch("WIDENINGS", w):
            self.assertIn("drops the existing claim", P.check(_pre()))

    def test_dropping_a_surviving_claim_is_caught_post_too(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        m = d["control_methods"][KEY]
        for f in ("how_it_works_beginner", "how_it_works_seasoned", "best_use"):
            m[f] = "Hold the soil evenly moist through the season."
        m["pros"] = ["Cheap"]
        m["cons"] = ["Preventive"]
        m["cautions"] = ["Test first"]
        self.assertIn("rewrote rather than added", P.verify_post(snap, d))

    def test_a_fragment_the_method_never_said_is_refused_as_vacuous(self):
        """ANTI-VACUITY: a MUST_SURVIVE fragment absent from the CURRENT text would pass trivially
        the moment the new text happened to contain it, while guarding nothing."""
        with _Patch("MUST_SURVIVE", {KEY: ("a phrase this method has never contained",)}):
            self.assertIn("never said", P.check(_pre()))

    def test_must_survive_may_not_name_an_unwidened_method(self):
        with _Patch("MUST_SURVIVE", dict(C.MUST_SURVIVE, garden_sanitation=("x",))):
            self.assertIn("does not widen", P.check(_pre()))

    def test_sources_only_gain(self):
        pre, post = _pre(), _post()
        before = pre["control_methods"][KEY]["sources"]
        after = post["control_methods"][KEY]["sources"]
        for s in before:
            self.assertIn(s, after)
        self.assertEqual(sorted(set(after) - set(before)), sorted(C.NEW_SOURCES))

    def test_dropping_a_source_is_caught(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        d["control_methods"][KEY]["sources"] = ["clemson_hgic", "osu_ext"]
        self.assertIn("dropped source", P.verify_post(snap, d))


class UnblocksItsCase(unittest.TestCase):
    """A widening whose target does not reach its case is a no-op that reads as progress."""

    def test_the_case_was_genuinely_blocked_before(self):
        pre = _pre()
        weevil = _prob(pre, "sweet-potato", "sweet-potato-weevil")
        self.assertEqual(weevil["type"], "insect")
        self.assertEqual(set(TYPE_TARGETS["insect"])
                         & set(pre["control_methods"][KEY]["applies_to"]), set())

    def test_the_case_is_reachable_after(self):
        post = _post()
        weevil = _prob(post, "sweet-potato", "sweet-potato-weevil")
        self.assertTrue(set(TYPE_TARGETS[weevil["type"]])
                        & set(post["control_methods"][KEY]["applies_to"]))

    def test_all_eight_declared_cases_are_unblocked(self):
        """The UNBLOCKS table is the round's claim about what it achieves. Every entry is checked,
        not just the first: a table-driven guard that stops at one entry is the r9 lesson."""
        post = _post()
        self.assertEqual(len(C.UNBLOCKS), 8)
        for slug, pid in C.UNBLOCKS:
            prob = _prob(post, slug, pid)
            self.assertTrue(set(TYPE_TARGETS[prob["type"]])
                            & set(post["control_methods"][KEY]["applies_to"]),
                            "%s/%s still blocked" % (slug, pid))

    def test_a_no_op_widening_is_refused(self):
        """Target the wrong vocabulary term and the method still cannot reach the weevil."""
        pre = _pre()
        snap = P.snapshot(pre)
        with _Patch("WIDENINGS", _wide(certified_clean_stock=("add_targets", ["mollusk"]))):
            d = _post(pre)
            self.assertIn("no-op", P.verify_post(snap, d))

    def test_a_missing_unblock_target_is_refused(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        with _Patch("UNBLOCKS", (("sweet-potato", "no-such-problem"),)):
            self.assertIn("not on the roster", P.verify_post(snap, d))

    def test_a_missing_unblock_crop_is_refused(self):
        pre = _pre()
        snap = P.snapshot(pre)
        d = _post(pre)
        with _Patch("UNBLOCKS", (("no-such-crop", "sweet-potato-weevil"),)):
            self.assertIn("not on the roster", P.verify_post(snap, d))


class Shape(unittest.TestCase):
    def test_widening_count_is_pinned(self):
        with _Patch("WIDENINGS", {}):
            self.assertIn("expected 1", P.check(_pre()))

    def test_new_source_count_is_pinned(self):
        """r9 REFUSED any new source. This round adds exactly one, so the refusal becomes a count."""
        with _Patch("NEW_SOURCES", {}):
            self.assertIn("declares 0 new sources, expected 1", P.check(_pre()))

    def test_a_new_source_that_already_exists_is_refused(self):
        # count stays 1, or the count guard fires first and this branch is never reached
        entry = dict(next(iter(C.NEW_SOURCES.values())), id="cornell_ext")
        with _Patch("NEW_SOURCES", {"cornell_ext": entry}):
            self.assertIn("already exists in source_catalog", P.check(_pre()))

    def test_a_non_t1_new_source_is_refused(self):
        """Asserts the WHOLE sentence. "is not T1" is emitted by BOTH the new-source check and the
        cited-source check, so the short fragment let either branch satisfy the other's driver and
        the mutation survived."""
        bad = copy.deepcopy(C.NEW_SOURCES)
        sid = next(iter(bad))
        bad[sid]["tier"] = "T2"
        with _Patch("NEW_SOURCES", bad):
            self.assertIn("new source %r is not T1" % sid, P.check(_pre()))

    def test_a_bare_host_new_source_is_refused(self):
        """A citation must point at the DOCUMENT that carries the claim. A bare host returns 200 and
        passes every url check while supporting nothing, which is the vce_426_331 shape."""
        bad = copy.deepcopy(C.NEW_SOURCES)
        bad[next(iter(bad))]["url"] = "https://ipm.ucanr.edu"
        with _Patch("NEW_SOURCES", bad):
            self.assertIn("BARE HOST", P.check(_pre()))

    def test_a_titleless_minted_source_is_refused_BEFORE_the_gauntlet(self):
        """THE DEFECT THIS ROUND ACTUALLY SHIPPED ONCE. The first apply passed this suite and a
        49-mutation harness, then took gate_all from 121/121 to 0/121, because A54 is a ROSTER gate
        reading source_catalog and no promote guard covered it. The gate function is imported, so
        the promote refuses exactly what the gauntlet would."""
        bad = copy.deepcopy(C.NEW_SOURCES)
        bad[next(iter(bad))].pop("title")
        with _Patch("NEW_SOURCES", bad):
            self.assertIn("would fail A54 at the gauntlet", P.check(_pre()))

    def test_the_minted_title_was_read_off_the_document(self):
        """A54's whole point: a title inferred from the id or URL is the defect. Assert the shipped
        title matches the document's own heading and its sibling's shape, not the slug."""
        t = C.NEW_SOURCES["ucanr_ext_raspberry_crown_borer"]["title"]
        self.assertTrue(t.startswith("Raspberry Crown Borer / Caneberries / "), t)
        self.assertIn("UC Statewide IPM Program (UC IPM)", t)
        self.assertNotIn("raspberry-crown-borer", t)   # the slug, i.e. URL inference

    def test_the_shipped_catalog_passes_A54_after_apply(self):
        from source_catalog_title_gate import title_violations
        self.assertEqual(title_violations(_post()["source_catalog"]), [])

    def test_a_new_source_without_citable_for_is_refused(self):
        bad = copy.deepcopy(C.NEW_SOURCES)
        bad[next(iter(bad))].pop("citable_for")
        with _Patch("NEW_SOURCES", bad):
            self.assertIn("has no citable_for", P.check(_pre()))

    def test_a_non_https_new_source_is_refused(self):
        bad = copy.deepcopy(C.NEW_SOURCES)
        bad[next(iter(bad))]["url"] = "http://ipm.ucanr.edu/agriculture/caneberries/x/"
        with _Patch("NEW_SOURCES", bad):
            self.assertIn("url is not https", P.check(_pre()))

    def test_widening_an_absent_method_is_refused(self):
        with _Patch("WIDENINGS", {"no_such_method": C.WIDENINGS[KEY]}):
            self.assertIn("not in the catalog", P.check(_pre()))

    def test_a_target_already_present_is_refused(self):
        with _Patch("WIDENINGS", _wide(certified_clean_stock=("add_targets", ["viral"]))):
            self.assertIn("already applies to", P.check(_pre()))

    def test_a_target_outside_the_vocabulary_is_refused(self):
        with _Patch("WIDENINGS", _wide(certified_clean_stock=("add_targets", ["storage_rot"]))):
            self.assertIn("outside the gate vocabulary", P.check(_pre()))

    def test_an_unknown_source_is_refused(self):
        with _Patch("WIDENINGS", _wide(certified_clean_stock=("add_sources", ["ghost_ext"]))):
            self.assertIn("neither in source_catalog nor declared", P.check(_pre()))

    def test_a_non_t1_EXISTING_source_is_refused(self):
        """The add_sources tier check, distinct from the NEW_SOURCES tier check above."""
        pre = _pre()
        pre["source_catalog"]["cornell_ext"] = dict(pre["source_catalog"]["cornell_ext"], tier="T2")
        with _Patch("WIDENINGS", _wide(certified_clean_stock=(
                "add_sources", list(C.NEW_SOURCES) + ["cornell_ext"]))):
            w = copy.deepcopy(C.WIDENINGS)
            w[KEY]["add_sources"] = list(C.NEW_SOURCES) + ["cornell_ext"]
            w[KEY]["add_anchors"] = dict(C.WIDENINGS[KEY]["add_anchors"],
                                         cornell_ext={"url": "https://x.cornell.edu/a/b",
                                                      "verified": "2026-09-02"})
            with _Patch("WIDENINGS", w):
                self.assertIn("is not T1", P.check(pre))

    def test_a_source_without_an_anchor_is_refused(self):
        with _Patch("WIDENINGS", _wide(certified_clean_stock=(
                "add_sources", list(C.NEW_SOURCES) + ["cornell_ext"]))):
            self.assertIn("has no anchoring_url", P.check(_pre()))

    def test_an_anchor_for_an_undeclared_source_is_refused(self):
        w = _wide(certified_clean_stock=("add_anchors", dict(
            C.WIDENINGS[KEY]["add_anchors"],
            umn_ext={"url": "https://extension.umn.edu/x", "verified": "2026-09-02"})))
        with _Patch("WIDENINGS", w):
            self.assertIn("not a declared source", P.check(_pre()))

    def test_a_non_https_anchor_is_refused(self):
        w = copy.deepcopy(C.WIDENINGS)
        w[KEY]["add_anchors"][next(iter(C.NEW_SOURCES))]["url"] = "http://ipm.ucanr.edu/x"
        with _Patch("WIDENINGS", w):
            self.assertIn("is not https", P.check(_pre()))

    def test_an_undated_anchor_is_refused(self):
        w = copy.deepcopy(C.WIDENINGS)
        w[KEY]["add_anchors"][next(iter(C.NEW_SOURCES))]["verified"] = "2026"
        with _Patch("WIDENINGS", w):
            self.assertIn("no valid verified date", P.check(_pre()))

    def test_hygiene_violation_in_new_prose_is_refused(self):
        w = copy.deepcopy(C.WIDENINGS)
        w[KEY]["set_fields"]["best_use"] = "Clean stock never lets the weevil in."
        with _Patch("WIDENINGS", w):
            self.assertIn("copy hygiene", P.check(_pre()))

    def test_hygiene_reaches_the_LIST_valued_fields(self):
        """set_fields carries lists (pros, cons) here, unlike r9 where every replaced field was a
        string. A hygiene loop that does not flatten silently never scans them."""
        w = copy.deepcopy(C.WIDENINGS)
        w[KEY]["set_fields"]["pros"] = ["This completely stops the problem."]
        with _Patch("WIDENINGS", w):
            self.assertIn("copy hygiene", P.check(_pre()))

    def test_hygiene_is_not_vacuous(self):
        w = copy.deepcopy(C.WIDENINGS)
        w[KEY]["set_fields"] = {}
        with _Patch("WIDENINGS", w):
            self.assertIn("would be vacuous", P.check(_pre()))

    def test_shipped_new_prose_is_clean(self):
        w = C.WIDENINGS[KEY]
        strs = []
        for v in w["set_fields"].values():
            strs.extend(v if isinstance(v, list) else [v])
        self.assertGreaterEqual(len(strs), 8)
        for s in strs:
            self.assertIsNone(P.hygiene(s), s[:60])

    def test_each_banned_shape_is_caught(self):
        """Carried from r8 and omitted here on the first pass, which left SIX hygiene branches with
        no driver at all. `test_shipped_new_prose_is_clean` cannot see a disabled branch, because
        clean prose stays clean either way."""
        for bad, frag in (("It never dries out.", "absolute"),
                          ("Hold it at 55 °F for a week.", "spaced degF"),
                          ("Hold it at 55 F for a week.", "bare F"),
                          ("Water evenly -- then check.", "double hyphen"),
                          ("A dash — here.", "em or en dash"),
                          ("Keep the bed **moist**.", "markdown"),
                          ("The colour of the skin sets.", "British"),
                          ("Cured bulbs are safe.", "bare safety claim"),
                          ("Inspect the Plant before buying.", "capital Plant")):
            got = P.hygiene(bad)
            self.assertIsNotNone(got, bad)
            self.assertIn(frag.split()[0].lower(), str(got).lower(), bad)

    def test_clean_prose_passes_hygiene(self):
        self.assertIsNone(P.hygiene("Hold the soil evenly moist while the roots are sizing."))

    def test_prose_of_includes_the_list_fields(self):
        """`pros`, `cons` and `cautions` are lists. If prose_of skipped them, every MUST_SURVIVE
        fragment living only in a list would go unchecked."""
        got = P.prose_of({"best_use": "a string", "pros": ["a pro"], "cons": ["a con"],
                          "sources": ["ignored"], "applies_to": ["ignored"], "tier": "ignored"})
        self.assertIn("a pro", got)
        self.assertIn("a con", got)
        self.assertNotIn("ignored", got)

    def test_the_new_prose_names_the_new_mechanism(self):
        """The prose is what scopes a widening the type vocabulary cannot. If the generalization is
        not visible to a reader, the round shipped a permission and no explanation."""
        post = _post()
        blob = " ".join(P.prose_of(post["control_methods"][KEY])).lower()
        self.assertIn("raspberry crown borer", blob)
        self.assertIn("pest-free", blob)
        self.assertIn("insects that overwinter inside crowns, slips and roots", blob)

    def test_the_disease_only_framing_is_GONE_from_the_reader_facing_text(self):
        """The whole reason this round amends prose: a reader on a weevil entry was being told to
        look for certified DISEASE-free seed. Assert the old framing is actually gone, not merely
        that new words were added."""
        post = _post()
        m = post["control_methods"][KEY]
        self.assertNotIn("not already carrying the disease", m["how_it_works_beginner"])
        self.assertNotIn("certified disease-free, pathogen-tested", m["find_it_beginner"])
        self.assertIn("certified disease-free or pest-free", m["find_it_beginner"])


class MainIsWiredToTheGuards(unittest.TestCase):
    """Carried from r8, where the harness proved a suite can drive every branch of `check` and still
    not prove `main` CALLS it."""

    def _fixture(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "wb") as fh:
            fh.write(promote_fixture.pre_state(P.BASE_SHA))
        return path

    def test_main_refuses_what_check_refuses(self):
        path = self._fixture()
        try:
            with _Patch("WIDENINGS", _wide(certified_clean_stock=("add_targets", ["storage_rot"]))):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("outside the gate vocabulary", str(cm.exception))
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_main_refuses_what_verify_post_refuses(self):
        path = self._fixture()
        real = P.apply_to

        def wrapped(data):
            out = real(data)
            data["crops"][0]["slug"] = "mutated-by-the-driver"
            return out
        try:
            with _Patch("apply_to", wrapped, mod=P):
                with self.assertRaises(SystemExit) as cm:
                    _run_main(path)
            self.assertIn("a crop changed", str(cm.exception))
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)

    def test_main_applies_the_pinned_post_sha(self):
        path = self._fixture()
        try:
            _run_main(path, apply_=True)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), POST_SHA)
        finally:
            os.unlink(path)

    def test_a_clean_dry_run_writes_nothing(self):
        path = self._fixture()
        try:
            _run_main(path)
            self.assertEqual(hashlib.sha256(open(path, "rb").read()).hexdigest(), P.BASE_SHA)
        finally:
            os.unlink(path)


class GateContract(unittest.TestCase):
    def test_control_ladder_gate_clean_on_post(self):
        self.assertEqual(CLG.all_violations(_post()), [])

    def test_no_existing_rung_becomes_illegal(self):
        """A widening can only ADD legality, but assert it rather than reasoning about it."""
        post = _post()
        cm = post["control_methods"]
        for c in post["crops"]:
            for fam in ("pests", "diseases"):
                for p in c.get(fam) or []:
                    if not isinstance(p, dict):
                        continue
                    for r in p.get("control_ladder") or []:
                        ap = cm[r["method"]]["applies_to"]
                        if "any" in ap:
                            continue
                        self.assertTrue(set(TYPE_TARGETS.get(p.get("type"), ())) & set(ap),
                                        f"{c['slug']}/{p.get('id')}/{r['method']}")

    def test_no_crop_gains_or_loses_a_rung(self):
        def rungs(d):
            return sum(len(p.get("control_ladder") or [])
                       for c in d["crops"] for f in ("pests", "diseases")
                       for p in c.get(f) or [] if isinstance(p, dict))
        self.assertEqual(rungs(_pre()), rungs(_post()))

    def test_one_serializer(self):
        d = _post()
        self.assertEqual(P.serialize(d), json.dumps(
            d, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
