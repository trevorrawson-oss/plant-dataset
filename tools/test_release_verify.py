#!/usr/bin/env python3
"""Guards on release_verify's COLLATERAL check (section A).

WHY THIS EXISTS. The check was `changed == [a.slug]` -- exactly one crop, the pilot slug. Every
multi-crop promote therefore reported `1 CONCERN(S) -- block + review before promoting` no matter
how clean it was. Reproduced on batch 2's own shipped promote (`0754031d` -> `0e12689b`):

    CONCERN: crops changed = ['sweet-corn', 'field-corn', 'popcorn', 'flint-corn']
             (expected only cherry-tomato)

and STATE_HISTORY nonetheless records "release_verify clean" for that release, in four entries.
Nobody was being careless: the concern is benign every single time, which is precisely the problem.
A gate that always fires trains its reader to stop reading it, and then the one real collateral
change rides through under the same message. Protocol #6 requires this tool before every promote.

The fix is to let the promoter DECLARE the blast radius and have the tool verify that declaration
exactly. `--expect-changed` is not a suppression flag: declaring a crop that did NOT change is
itself a concern, so the declaration cannot be padded to make a run go quiet.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "release_verify.py")
CANON = os.path.join(REPO, "crops_data_final.json")


def _run(candidate, base, *extra):
    r = subprocess.run([sys.executable, TOOL, candidate, "--base", base, *extra],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def _section_a(out):
    lines = []
    for ln in out.splitlines():
        if ln.startswith("B. "):
            break
        lines.append(ln)
    return "\n".join(lines)


class CollateralDeclaration(unittest.TestCase):
    """Section A must accept a DECLARED multi-crop blast radius, and only that one."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="relver_")
        cls.base = os.path.join(cls.tmp, "base.json")
        with open(CANON, "rb") as f:
            raw = f.read()
        with open(cls.base, "wb") as f:
            f.write(raw)
        cls.data = json.loads(raw.decode("utf-8"))

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _candidate(self, slugs, name):
        d = json.loads(json.dumps(self.data))
        for c in d["crops"]:
            if c["slug"] in slugs:
                c["_touched_by_test"] = True
        p = os.path.join(self.tmp, f"{name}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        return p

    def test_single_crop_matching_slug_is_accepted(self):
        """The pre-existing behavior must not regress."""
        cand = self._candidate({"cherry-tomato"}, "one")
        _rc, out = _run(cand, self.base, "--slug", "cherry-tomato")
        a = _section_a(out)
        self.assertIn("only cherry-tomato changed", a)
        self.assertNotIn("CONCERN: crops changed", a)

    def test_multi_crop_WITHOUT_a_declaration_is_a_concern(self):
        """This is the batch-2 and batch-3 case, and it must still be refused undeclared."""
        cand = self._candidate({"cucumber", "pickling-cucumber"}, "two_undeclared")
        _rc, out = _run(cand, self.base, "--slug", "cucumber")
        self.assertIn("CONCERN: crops changed", _section_a(out))

    def test_multi_crop_WITH_an_exact_declaration_is_accepted(self):
        cand = self._candidate({"cucumber", "pickling-cucumber"}, "two_declared")
        _rc, out = _run(cand, self.base, "--slug", "cucumber",
                        "--expect-changed", "pickling-cucumber")
        a = _section_a(out)
        self.assertNotIn("CONCERN: crops changed", a)
        self.assertIn("declared", a)

    def test_declaring_a_crop_that_did_NOT_change_is_a_concern(self):
        """The escape hatch must not be paddable. Declaring extra slugs to quiet a run is the
        obvious abuse, and it would hide the very collateral this section exists to catch."""
        cand = self._candidate({"cucumber"}, "one_overdeclared")
        _rc, out = _run(cand, self.base, "--slug", "cucumber",
                        "--expect-changed", "pickling-cucumber,slicing-cucumber")
        self.assertIn("CONCERN: crops changed", _section_a(out))

    def test_an_UNDECLARED_crop_changing_is_still_a_concern(self):
        """The real collateral case: the declaration is right as far as it goes, but something
        else moved too."""
        cand = self._candidate({"cucumber", "pickling-cucumber", "basil"}, "three_partial")
        _rc, out = _run(cand, self.base, "--slug", "cucumber",
                        "--expect-changed", "pickling-cucumber")
        self.assertIn("CONCERN: crops changed", _section_a(out))

    def test_declaration_order_does_not_matter(self):
        cand = self._candidate({"cucumber", "pickling-cucumber", "slicing-cucumber"}, "three_ord")
        for decl in ("slicing-cucumber,pickling-cucumber", "pickling-cucumber,slicing-cucumber"):
            with self.subTest(decl=decl):
                _rc, out = _run(cand, self.base, "--slug", "cucumber", "--expect-changed", decl)
                self.assertNotIn("CONCERN: crops changed", _section_a(out))

    def test_whitespace_and_empties_in_the_declaration_are_tolerated(self):
        cand = self._candidate({"cucumber", "pickling-cucumber"}, "two_ws")
        _rc, out = _run(cand, self.base, "--slug", "cucumber",
                        "--expect-changed", " pickling-cucumber , ")
        self.assertNotIn("CONCERN: crops changed", _section_a(out))


if __name__ == "__main__":
    unittest.main(verbosity=2)
