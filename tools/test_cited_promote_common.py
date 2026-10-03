#!/usr/bin/env python3
"""cited_promote_common is the ONE home of the cited-promote evidence and diff helpers (housekeeping kickoff 60,
ruling 5, 2026-10-03).

Before: promote 1 (promote_pla10_planting_layout) held the originals inline, pla10_promote_common held a
byte-identical second copy, and promotes 2 and 3 imported the copy; four inspect.getsource tests pinned the copy
to the original. A frozen copy is a fork waiting to happen and a getsource pin tests text, not behavior.

After (this suite):
  1. every PLA-10 promote imports the shared helpers from cited_promote_common, and none redefines any SHARED
     name (function, class or constant) itself;
  2. no promote suite carries an inspect.getsource identity pin (the real-stage replays in
     test_pla10_promote_replays.py are the guard);
  3. pla10_promote_common is a pure re-export shim: every name in SHARED is the SAME object in both modules,
     and the shim defines nothing of its own;
  4. SHARED is the whole public surface: every top-level name cited_promote_common defines is in SHARED, so a
     helper added to the module and forgotten in the shim fails here by name;
  5. the module is a flat tools/ file whose name does not start with promote_ (the harnesses copy flat
     tools/*.py only, and promotes must not import promotes).
SHARED is a typed literal, never derived from the module it checks.
Run: python3 -m pytest tools/test_cited_promote_common.py -q
"""
import ast, os, re, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PROMOTES = ("promote_pla10_planting_layout.py", "promote_pla10_promote2.py", "promote_pla10_promote3.py")
SUITES = ("test_promote_pla10_planting_layout.py", "test_promote_pla10_promote2.py",
          "test_promote_pla10_promote3.py")
# Every top-level name cited_promote_common defines (functions, classes, constants), typed.
SHARED = (
    "PDF_TEXT_EXTRACTOR", "IDIOMS", "EVIDENCE_COLS",
    "sha256_bytes", "serialize", "compact", "leaf_diff", "norm_text", "_numbers", "quote_states", "pdf_text",
    "manifest", "Refused", "refuse", "DIST", "SPACING_WORD", "SKIP_SUBTREES", "SEG", "parse_path", "resolve",
    "fmt", "set_at", "spacing_strings",
    "TOL_FT", "_NUMWORDS", "_NUM", "_FT", "_IN", "_QTY", "_JOIN", "_POSTFIX", "_LABEL", "_VERB",
    "_num_val", "_ft_groups", "ft_endpoints_stated", "quote_states_ft",
)
IMPORT_RE = re.compile(r"(?m)^from cited_promote_common import \(")
PIN_RE = re.compile(r"assertEqual\(\s*inspect\.getsource\(")


def _src(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def _top_level_defs(src):
    out = set()
    for node in ast.parse(src).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out.add(node.name)
        elif isinstance(node, ast.Assign):
            out |= {t.id for t in node.targets if isinstance(t, ast.Name)}
    return out


class Consolidated(unittest.TestCase):
    def test_the_module_is_a_flat_non_promote_file(self):
        self.assertTrue(os.path.isfile(os.path.join(HERE, "cited_promote_common.py")))
        self.assertFalse("cited_promote_common".startswith(("promote_", "test_", "mutate_")))

    def test_every_promote_imports_the_shared_module(self):
        for p in PROMOTES:
            with self.subTest(promote=p):
                self.assertRegex(_src(p), IMPORT_RE)
                self.assertNotRegex(_src(p), r"(?m)^\s*(?:import|from)\s+pla10_promote_common\b")

    def test_no_promote_redefines_a_shared_name(self):
        for p in PROMOTES:
            with self.subTest(promote=p):
                self.assertEqual(sorted(_top_level_defs(_src(p)) & set(SHARED)), [])

    def test_no_suite_carries_a_getsource_pin(self):
        # An identity pin is an EQUALITY between two source texts; reading one function's source to assert
        # what it contains (promote 3's test_the_post_state_gates_run_armed) is not a pin and stays legal.
        for s in SUITES:
            with self.subTest(suite=s):
                self.assertNotRegex(_src(s), PIN_RE)

    def test_shared_is_the_whole_module_surface(self):
        defined = _top_level_defs(_src("cited_promote_common.py"))
        self.assertEqual(sorted(defined - set(SHARED)), [], "defined in the module, missing from SHARED")
        self.assertEqual(sorted(set(SHARED) - defined), [], "in SHARED, not defined by the module")

    def test_the_shim_reexports_every_name_by_identity(self):
        import cited_promote_common as M
        import pla10_promote_common as SHIM
        for name in SHARED:
            with self.subTest(name=name):
                self.assertIs(getattr(SHIM, name), getattr(M, name))

    def test_the_shim_defines_nothing_of_its_own(self):
        self.assertEqual(sorted(_top_level_defs(_src("pla10_promote_common.py"))), [])


if __name__ == "__main__":
    unittest.main()
