#!/usr/bin/env python3
"""Guard suite for tools/promote_pla8_variety_ladder_delta.py (PLA-8 Round 2). Base 20a32c47.

REPLAY-PINNED, so there is NO RED PHASE and this suite does not claim one -- `pre` is rebuilt from
the pinned base via promote_fixture and `post` is the promote's OWN output, never live canonical.
(A suite whose `post` reads live canonical reddens on every future promote; that has already
recurred twice in this repo.) The non-vacuity evidence is the REACHABILITY family plus
tools/mutate_pla8_ladder_delta_suite.py.

WHAT IS DIFFERENT ABOUT THIS PROMOTE'S RISK. It adds a NESTED subtree to 22 variety records rather
than a scalar field to a crop, so the blast radius has to be measured at LEAF level: a crop-level
field comparison would see `varieties` change on two crops and call it a day, and would not notice
a rung quietly appearing on a 23rd variety. So BlastRadius walks every leaf path in both states and
asserts SET EQUALITY of the path sets before comparing a single value -- iterating `pre` alone makes
every addition invisible, which was all four PLA-162 defects.

The content is also GENERATED, which creates a vacuity trap of its own: a guard that recomputes its
expectation from the generator is comparing the generator to itself. The expected variety set is
therefore ENUMERATED as a literal below, never derived from the staged content.
"""
import copy
import hashlib
import json
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))

import promote_fixture  # noqa: E402
import promote_pla8_variety_ladder_delta as P  # noqa: E402

POST_SHA = "98ea96c446cbeed858efa56bbf5324a7dc2edd3e21bbe26bdaf4c51b90ac6aef"

# ENUMERATED, never derived from the staged content -- a guard that recomputes its expectation from
# the thing under test cannot fail. Adding a 23rd variety to staging must break this literal.
APPLE_VARIETIES = ("dorsett-golden", "anna", "ein-shemer", "zestar", "mcintosh", "liberty",
                   "empire", "honeycrisp", "gala", "golden-delicious", "jonagold", "mutsu",
                   "fuji", "granny-smith", "pink-lady", "dolgo")
STRAWBERRY_VARIETIES = ("honeoye", "earliglow", "jewel", "allstar", "albion", "tristar")
EXPECTED_OPS = 94
EXPECTED_ENTRIES = 62
GRADES = {"immune", "resistant", "tolerant", "susceptible"}


def _pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


def _content():
    return P.load_content()


def _post(pre=None):
    pre = pre if pre is not None else _pre()
    data = copy.deepcopy(pre)
    P.apply_to(data, _content())
    return data


def _leaves(o, path=""):
    """Every scalar leaf, by full path. The unit the blast radius is measured in."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _leaves(v, f"{path}[{i}]")
    else:
        yield path, o


def _strings():
    out = []
    for slug, per in _content().items():
        for vid, delta in per.items():
            for pid, e in delta.items():
                for r in e["rungs"]:
                    for k, v in r.items():
                        if k.startswith(("note_", "why_")):
                            out.append((f"{slug}/{vid}/{pid}/{r['method']}.{k}", v))
    return out


class Fixture(unittest.TestCase):
    def test_base_reconstructs_to_the_pinned_sha(self):
        self.assertEqual(hashlib.sha256(promote_fixture.pre_state(P.BASE_SHA)).hexdigest(),
                         P.BASE_SHA)

    def test_post_serializes_to_the_pinned_post_sha(self):
        out = P.serialize(_post())
        self.assertEqual(hashlib.sha256(out).hexdigest(), POST_SHA)

    def test_output_is_compact(self):
        # MUST go through the promote's own serializer -- a local json.dumps here made
        # this guard grade itself, and the harness caught an indent=1 mutation surviving.
        out = P.serialize(_post()).decode("utf-8")
        self.assertNotIn(', "', out)
        self.assertNotIn("\n", out)

    def test_staged_content_sha_is_pinned(self):
        raw = open(P.CONTENT, "rb").read()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), P.CONTENT_SHA)


class Reachability(unittest.TestCase):
    """The base really lacked what this creates. Without these, every guard below is vacuous."""

    def test_no_variety_anywhere_in_the_base_carries_a_ladder_delta(self):
        for c in _pre()["crops"]:
            for v in (c.get("varieties") or {}).get("recommended") or []:
                if isinstance(v, dict):
                    self.assertNotIn(P.DELTA_KEY, v, f"{c['slug']}/{v.get('id')}")

    def test_every_targeted_variety_gains_one(self):
        by = {c["slug"]: c for c in _post()["crops"]}
        for slug, ids in (("apple", APPLE_VARIETIES), ("strawberry", STRAWBERRY_VARIETIES)):
            got = {v["id"] for v in by[slug]["varieties"]["recommended"]
                   if isinstance(v, dict) and P.DELTA_KEY in v}
            self.assertEqual(got, set(ids), slug)

    def test_the_scope_is_exactly_the_enumerated_varieties(self):
        content = _content()
        self.assertEqual(sorted(content), ["apple", "strawberry"])
        self.assertEqual(sorted(content["apple"]), sorted(APPLE_VARIETIES))
        self.assertEqual(sorted(content["strawberry"]), sorted(STRAWBERRY_VARIETIES))

    def test_operation_and_entry_counts_are_pinned(self):
        content = _content()
        entries = sum(len(d) for per in content.values() for d in per.values())
        ops = sum(len(e["rungs"]) for per in content.values() for d in per.values()
                  for e in d.values())
        self.assertEqual(entries, EXPECTED_ENTRIES)
        self.assertEqual(ops, EXPECTED_OPS)


class BlastRadius(unittest.TestCase):
    def test_leaf_paths_added_are_exactly_the_delta_subtree(self):
        pre, post = _pre(), None
        post = _post(pre)
        pre_paths = {p for p, _ in _leaves(pre)}
        post_paths = {p for p, _ in _leaves(post)}
        # SET COMPARISON FIRST. Iterating pre alone makes every addition invisible (PLA-162).
        self.assertEqual(pre_paths - post_paths, set(), "leaf paths were DROPPED")
        added = post_paths - pre_paths
        self.assertTrue(added, "nothing was added -- the promote is a no-op")
        stray = [p for p in added if f".{P.DELTA_KEY}." not in p]
        self.assertEqual(stray, [], f"added leaves outside {P.DELTA_KEY}: {stray[:5]}")

    def test_no_pre_existing_leaf_changed_value(self):
        pre = _pre()
        post = _post(pre)
        a = dict(_leaves(pre))
        b = dict(_leaves(post))
        changed = [p for p in a if p in b and a[p] != b[p]]
        self.assertEqual(changed, [], f"{len(changed)} pre-existing leaves changed: {changed[:5]}")

    def test_top_level_tables_are_byte_identical(self):
        pre, post = _pre(), None
        post = _post(pre)
        self.assertEqual(set(pre), set(post))
        for k in pre:
            if k != "crops":
                self.assertEqual(pre[k], post[k], f"top-level {k} changed")

    def test_only_apple_and_strawberry_are_touched(self):
        pre = _pre()
        post = _post(pre)
        pre_by = {c["slug"]: c for c in pre["crops"]}
        post_by = {c["slug"]: c for c in post["crops"]}
        self.assertEqual(set(pre_by), set(post_by))
        touched = {s for s in post_by if pre_by[s] != post_by[s]}
        self.assertEqual(touched, {"apple", "strawberry"})

    def test_no_control_ladder_was_edited(self):
        pre = _pre()
        post = _post(pre)
        def ladders(d):
            return {(c["slug"], p.get("id")): p.get("control_ladder")
                    for c in d["crops"] for f in ("pests", "diseases")
                    for p in c.get(f) or [] if isinstance(p, dict) and "control_ladder" in p}
        a, b = ladders(pre), ladders(post)
        self.assertEqual(set(a), set(b))
        for k in a:
            self.assertEqual(a[k], b[k], f"{k}: parent ladder was edited")


class Referential(unittest.TestCase):
    def test_every_problem_id_is_laddered_on_its_crop(self):
        by = {c["slug"]: c for c in _pre()["crops"]}
        for slug, per in _content().items():
            lad = P._laddered(by[slug])
            for vid, delta in per.items():
                for pid in delta:
                    self.assertIn(pid, lad, f"{slug}/{vid}/{pid}")

    def test_every_drop_or_replace_targets_a_real_parent_rung(self):
        by = {c["slug"]: c for c in _pre()["crops"]}
        for slug, per in _content().items():
            lad = P._laddered(by[slug])
            for vid, delta in per.items():
                for pid, e in delta.items():
                    parent = {r["method"] for r in lad[pid]["control_ladder"]}
                    for r in e["rungs"]:
                        if r["op"] in ("drop", "replace"):
                            self.assertIn(r["method"], parent, f"{slug}/{vid}/{pid}")

    def test_every_resistance_basis_has_a_real_grade(self):
        by = {c["slug"]: c for c in _pre()["crops"]}
        for slug, per in _content().items():
            vs = {v["id"]: v for v in by[slug]["varieties"]["recommended"] if isinstance(v, dict)}
            for vid, delta in per.items():
                grades = vs[vid].get("resistance") or {}
                for pid, e in delta.items():
                    if e.get("basis") == "resistance":
                        self.assertIn(pid, grades, f"{slug}/{vid}/{pid}")
                        self.assertIn(grades[pid], GRADES)

    def test_a_drop_carries_why_and_never_note(self):
        for slug, per in _content().items():
            for vid, delta in per.items():
                for pid, e in delta.items():
                    for r in e["rungs"]:
                        if r["op"] == "drop":
                            self.assertIn("why_beginner", r, f"{slug}/{vid}/{pid}/{r['method']}")
                            self.assertNotIn("note_beginner", r)
                            self.assertNotIn("note_seasoned", r)


class Refusals(unittest.TestCase):
    """A guard that REFUSES a bad input while staying green is a refusal-spec pass, not vacuity."""

    def _mutate(self, fn):
        c = copy.deepcopy(_content())
        fn(c)
        return P.check(_pre(), c)

    def test_refuses_an_unknown_variety(self):
        self.assertIn("no variety", self._mutate(
            lambda c: c["apple"].__setitem__("ghost-apple", c["apple"]["liberty"])))

    def test_refuses_a_crop_outside_the_pilot(self):
        self.assertIn("outside the pilot scope", self._mutate(
            lambda c: c.__setitem__("celery", {"x": {}})))

    def test_refuses_an_unladdered_problem_id(self):
        self.assertIn("not a laddered problem id", self._mutate(
            lambda c: c["apple"]["liberty"].__setitem__("not-a-disease",
                                                        c["apple"]["liberty"]["apple-scab"])))

    def test_refuses_a_rung_method_absent_from_the_parent(self):
        def m(c):
            c["apple"]["liberty"]["apple-scab"]["rungs"][0]["method"] = "bird_netting"
        self.assertIn("is not in the parent ladder", self._mutate(m))

    def test_refuses_an_empty_delta(self):
        self.assertIn("empty", self._mutate(lambda c: c["apple"].__setitem__("liberty", {})))

    def test_refuses_a_resistance_basis_with_no_grade(self):
        """ISOLATED so the grade check is what fires.

        The first version copied albion's anthracnose delta onto `gray-mold`, and the suite caught
        it: gray-mold's ladder has no `resistant_varieties` rung, so the EARLIER parent-membership
        check refused first and this guard never ran. Green for the wrong reason is the vacuity
        that matters. `powdery-mildew` is laddered on strawberry AND opens on `resistant_varieties`,
        so a single-rung delta there passes every earlier check and leaves only the missing grade
        (albion is graded on anthracnose alone)."""
        def m(c):
            c["strawberry"]["albion"]["powdery-mildew"] = {
                "basis": "resistance",
                "rungs": [{"method": "resistant_varieties", "op": "replace",
                           "note_beginner": "x" * 60, "note_seasoned": "y" * 60}],
            }
        msg = self._mutate(m)
        self.assertIn("carries no grade", msg)
        self.assertNotIn("parent ladder", msg, "an earlier check fired; the guard is masked")

    def test_refuses_when_the_delta_already_exists(self):
        pre = _pre()
        P.apply_to(pre, _content())
        self.assertIn("already exists", P.check(pre, _content()))


class Mechanics(unittest.TestCase):
    def test_no_em_dash_en_dash_or_double_hyphen(self):
        for where, v in _strings():
            for bad in ("—", "–", "--"):
                self.assertNotIn(bad, v, where)

    def test_american_english(self):
        bad = ("colour", "flavour", "fertilise", "organise", "recognise", "realise", "centre",
               "metre", "mould", "grey", "sulphur", "practise", "licence", "defence", "labour")
        for where, v in _strings():
            for w in bad:
                self.assertIsNone(re.search(rf"\b{w}\b", v, re.I), f"{where}: {w}")

    def test_no_absolute_outcome_claims(self):
        for where, v in _strings():
            self.assertIsNone(
                re.search(r"\b(never|always|guaranteed|completely|totally|harmless)\b", v, re.I),
                where)

    def test_temperatures_render_as_degF(self):
        for where, v in _strings():
            for m in re.finditer(r"\b\d{2,3}\s*(?:degrees|deg)\b", v, re.I):
                self.fail(f"{where}: {m.group(0)!r} should be °F")

    def test_immune_wording_never_outruns_its_source(self):
        """UMN says 'immune'; Purdue says resistance is not immunity. Neither says 'cannot ever'."""
        for where, v in _strings():
            self.assertIsNone(re.search(r"cannot catch it at all|can never get|no chance of", v,
                                        re.I), where)

    def test_the_purdue_hedge_rides_every_resistant_and_tolerant_rung0(self):
        by = {c["slug"]: c for c in _pre()["crops"]}
        for slug, per in _content().items():
            vs = {v["id"]: v for v in by[slug]["varieties"]["recommended"] if isinstance(v, dict)}
            for vid, delta in per.items():
                for pid, e in delta.items():
                    grade = (vs[vid].get("resistance") or {}).get(pid)
                    if grade not in ("resistant", "tolerant"):
                        continue
                    r0 = [r for r in e["rungs"] if r["method"] == "resistant_varieties"]
                    if not r0:
                        continue
                    ns = r0[0].get("note_seasoned", "")
                    self.assertTrue(
                        "not immunity" in ns or "ratings differ" in ns,
                        f"{slug}/{vid}/{pid}: seasoned rung 0 carries neither the hedge nor a "
                        f"source-disagreement note")


class Register(unittest.TestCase):
    def test_beginner_and_seasoned_are_never_the_same_string(self):
        for slug, per in _content().items():
            for vid, delta in per.items():
                for pid, e in delta.items():
                    for r in e["rungs"]:
                        b = r.get("note_beginner") or r.get("why_beginner")
                        s = r.get("note_seasoned") or r.get("why_seasoned")
                        if b and s:
                            self.assertNotEqual(b, s, f"{slug}/{vid}/{pid}/{r['method']}")

    def test_no_generated_string_is_empty_or_stubby(self):
        for where, v in _strings():
            self.assertGreater(len(v.strip()), 40, where)


if __name__ == "__main__":
    unittest.main(verbosity=2)
