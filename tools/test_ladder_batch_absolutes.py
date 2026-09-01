#!/usr/bin/env python3
"""`ladder_batch verify`'s absolute-claim vocabulary must COVER every promote's own `hygiene()`.

WHY THIS EXISTS. Batch 22 shipped with three flat "never" absolutes live in the SOURCE prose of its
three crops, and the step whose job is to report copy-hygiene problems reported zero. The cause was
not a bug in either check: it was that `ladder_batch.py`'s list was
`(always|guaranteed|completely|totally|harmless)` while every batch-17-to-22 promote's `hygiene()`
was `("always", "never", "completely", "harmless", "guaranteed")`. **"never" was in one and not the
other**, and the two read as the same check, so nobody compared them.

The asymmetry that matters is one-directional. `verify` runs FIRST, on a scratch merge, and is what
a session trusts before spending a read. A promote's `hygiene()` runs later and refuses. So:

  * `verify` MISSING a word the promote bans  -> the batch looks clean, then its own promote refuses
    it (annoying), or the word sits in SOURCE prose that no promote inspects (what happened).
  * `verify` having a word no promote bans    -> harmless; verify is advisory.

Hence the assertion is COVERAGE, not equality: `ABSOLUTE_WORDS` must be a superset of every list.

The promote corpus is READ FROM SOURCE rather than imported, because promote scripts are frozen
records pinned by `COMMIT_FOR` and importing 28 of them would couple this test to all of them
(`docs/promote_suite_mutation_convention.md`; and see the standing rule that promotes must not
import promotes). Re-deriving from source also means a NEW promote with a new word is picked up
without anyone remembering to register it.
"""
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)
import ladder_batch as LB  # noqa: E402

# The two shapes a promote's hygiene list is written in, across the corpus:
#   for w in ("always", "never", "completely", "harmless", "guaranteed"):
#   re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I)
TUPLE_FORM = re.compile(r'for w in \(([^)]*)\):')
REGEX_FORM = re.compile(r'\\b\(\?:((?:always|never)[a-z|?]*)\)\\b')
WORD = re.compile(r'"([a-z]+)"')


def promote_files():
    return sorted(f for f in os.listdir(TOOLS)
                  if f.startswith("promote_") and f.endswith(".py"))


def lists_in(path):
    """Every absolute-word list this promote defines, as sets of bare words."""
    src = open(os.path.join(TOOLS, path)).read()
    out = []
    for m in TUPLE_FORM.finditer(src):
        words = set(WORD.findall(m.group(1)))
        if "guaranteed" in words or "harmless" in words:
            out.append(words)
    for m in REGEX_FORM.finditer(src):
        words = {w.rstrip("?") for w in m.group(1).split("|")}
        # `eliminates?` is a stem with an optional suffix; keep the stem.
        out.append({w for w in words if w})
    return out


class AbsoluteVocabularyIsReconciled(unittest.TestCase):

    def test_the_corpus_scan_finds_something(self):
        """ANTI-VACUITY. A regex that matched nothing would make every assertion below pass."""
        found = {f: lists_in(f) for f in promote_files()}
        nonempty = {f: L for f, L in found.items() if L}
        self.assertGreaterEqual(len(nonempty), 20,
                                "expected the hygiene list in most promote scripts; the source "
                                "scan has stopped matching and every check here is vacuous")

    def test_ladder_batch_covers_every_promotes_hygiene_list(self):
        """The one-directional coverage rule. This is the assertion that would have caught the
        batch-22 gap on the day `wet_foliage_discipline`-era promotes added "never"."""
        mine = {w.lower() for w in LB.ABSOLUTE_WORDS}
        gaps = {}
        for f in promote_files():
            for words in lists_in(f):
                missing = {w for w in words if w not in mine and not any(
                    w.startswith(m) or m.startswith(w) for m in mine)}
                if missing:
                    gaps.setdefault(f, set()).update(missing)
        self.assertEqual(gaps, {},
                         "ladder_batch.ABSOLUTE_WORDS does not cover these promote hygiene words, "
                         "so `verify` will call prose clean that a promote then refuses: %r" % gaps)

    def test_never_is_in_the_vocabulary(self):
        """The specific word that was missing, pinned by name so a future edit cannot drop it
        silently. Three flat "never" absolutes in batch 22's source prose went unreported."""
        self.assertIn("never", [w.lower() for w in LB.ABSOLUTE_WORDS])

    def test_the_check_actually_fires_on_never(self):
        """Pin the BEHAVIOUR, not just the constant -- the constant is only useful if the regex
        built from it reaches the text."""
        pat = re.compile(r"\b(%s)\b" % "|".join(LB.ABSOLUTE_WORDS), re.I)
        self.assertTrue(pat.search("Water at the soil line, never overhead, so leaves stay dry."))
        self.assertTrue(pat.search("Never leave tomato debris in the garden over winter."))
        self.assertTrue(pat.search("It is Always worth checking."))
        self.assertIsNone(pat.search("Water at the soil line rather than overhead."))

    def test_word_boundaries_hold(self):
        """`never` must not fire inside `nevertheless`, and `always` must not fire inside a longer
        token. A naive substring check would flood."""
        pat = re.compile(r"\b(%s)\b" % "|".join(LB.ABSOLUTE_WORDS), re.I)
        self.assertIsNone(pat.search("Nevertheless the vines recovered."))
        self.assertIsNone(pat.search("The alwayson sensor is unrelated."))


if __name__ == "__main__":
    unittest.main(verbosity=2)
