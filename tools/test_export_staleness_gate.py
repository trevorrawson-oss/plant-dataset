#!/usr/bin/env python3
"""Guards for export_staleness_gate, the INFORMATIONAL consumer-pin report (PLA-713).

What the ruling requires, and what each class below pins:
  * E1 (app) and E3 (astro) report how many dataset commits each consumer's pin is behind
    origin/main                                                   -> TestBehindCount
  * the pinned commit is read from each consumer repo's ORIGIN, never a local checkout or
    export                                                        -> TestReadsOriginNotCheckout
  * neither ever fails a commit or push: a STALE pin produces a report and exit 0
                                                                  -> TestStalePinReportsAndNeverFails
  * a pin that cannot be read is UNMEASURED, never "0 behind" (the PLA-258 lesson kept)
                                                                  -> TestUnmeasured

Every fixture is a real git repo: a dataset repo with an origin/main ref, and per consumer a bare
"origin" carrying a gitlink at the consumer's path. Mutation evidence:
tools/mutate_export_staleness_suite.py.
"""
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_staleness_gate as gate

CANON_OLD = '{"crops":[{"slug":"b"}]}'
CANON_NEW = '{"crops":[{"slug":"a"}]}'


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def _init(path, bare=False):
    os.makedirs(path, exist_ok=True)
    _git(path, "init", "-q", *(["--bare"] if bare else []))
    if not bare:
        _git(path, "config", "user.email", "t@example.com")
        _git(path, "config", "user.name", "t")
    return path


def _commit_file(repo, name, body, msg):
    with open(os.path.join(repo, name), "w") as f:
        f.write(body)
    _git(repo, "add", name)
    _git(repo, "commit", "-qm", msg)
    return _git(repo, "rev-parse", "HEAD")


def _consumer(root, name, branch, path, pinned):
    """A bare ORIGIN whose `branch` pins `pinned` at `path`, plus the working clone that pushed it.
    Returns (origin url, working clone)."""
    origin = _init(os.path.join(root, f"{name}-origin.git"), bare=True)
    work = _init(os.path.join(root, f"{name}-work"))
    _git(work, "checkout", "-qb", branch)
    with open(os.path.join(work, "README.md"), "w") as f:
        f.write(name)
    _git(work, "add", "README.md")
    _git(work, "update-index", "--add", "--cacheinfo", f"160000,{pinned},{path}")
    _git(work, "commit", "-qm", "pin")
    _git(work, "push", "-q", origin, f"HEAD:refs/heads/{branch}")
    return origin, work


class _World(unittest.TestCase):
    """Dataset history: c_old (CANON_OLD) -> c_new (CANON_NEW) -> c_tool (tooling only, same canonical).
    origin/main = c_tool. Both consumers pin c_tool unless a test says otherwise."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, self.tmp, True)
        self.ds = _init(os.path.join(self.tmp, "plant-dataset"))
        self.c_old = _commit_file(self.ds, gate.CANONICAL, CANON_OLD, "old canonical")
        self.c_new = _commit_file(self.ds, gate.CANONICAL, CANON_NEW, "new canonical")
        self.c_tool = _commit_file(self.ds, "tool.py", "x = 1\n", "tooling only")
        _git(self.ds, "update-ref", gate.DATASET_REF, self.c_tool)

    def consumer(self, pinned, check="E1", label="app", branch="feat/community-foundation",
                 path="vendor/plant-dataset"):
        url, work = _consumer(self.tmp, f"{label}-{pinned[:7]}-{len(os.listdir(self.tmp))}",
                              branch, path, pinned)
        return (check, label, url, branch, path), work

    def row(self, consumer):
        r = gate.report(consumers=[consumer], dataset_root=self.ds, fetch=False)
        self.assertEqual(len(r["consumers"]), 1)
        return r["consumers"][0]

    def cli(self, consumers):
        """Run main() against fixture consumers. Returns (rc, stdout)."""
        saved = (gate.CONSUMERS, gate.REPO)
        gate.CONSUMERS, gate.REPO = tuple(consumers), self.ds
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                rc = gate.main(["--no-fetch"])
        finally:
            gate.CONSUMERS, gate.REPO = saved
        return rc, buf.getvalue()


class TestConsumerTable(unittest.TestCase):
    def test_the_consumers_are_the_ruled_pins(self):
        """PLA-713: the app pins vendor/plant-dataset on feat/community-foundation; the site pins
        plant-dataset on main. A path or branch typo would report on a ref nothing ships from."""
        self.assertEqual(gate.CONSUMERS, (
            ("E1", "app", "https://github.com/trevorrawson-oss/plant-app.git",
             "feat/community-foundation", "vendor/plant-dataset"),
            ("E3", "astro", "https://github.com/trevorrawson-oss/plant-astro.git",
             "main", "plant-dataset"),
        ))

    def test_every_consumer_is_reported(self):
        """The population the report inspected is the whole table: a row per consumer, none dropped."""
        tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, tmp, True)
        nowhere = [(c[0], c[1], os.path.join(tmp, "absent.git"), c[3], c[4]) for c in gate.CONSUMERS]
        r = gate.report(consumers=nowhere, dataset_root=tmp, fetch=False)
        self.assertEqual([x["check"] for x in r["consumers"]], ["E1", "E3"])
        self.assertEqual(r["measured"] + r["unmeasured"], 2)


class TestBehindCount(_World):
    def test_control_a_current_pin_is_zero_behind(self):
        """The control: if this is not 0 / identical, every count below proves nothing."""
        c, _ = self.consumer(self.c_tool)
        r = self.row(c)
        self.assertTrue(r["measured"], r)
        self.assertEqual((r["pinned"], r["head"], r["behind"], r["ahead"]),
                         (self.c_tool, self.c_tool, 0, 0))
        self.assertTrue(r["canonical_same"])

    def test_a_pin_two_commits_back_is_two_behind_with_a_different_canonical(self):
        r = self.row(self.consumer(self.c_old)[0])
        self.assertEqual((r["behind"], r["ahead"]), (2, 0))
        self.assertFalse(r["canonical_same"])

    def test_a_tooling_only_gap_is_behind_but_canonical_identical(self):
        """One commit behind, but the bytes the consumer serves are the same: the report must say so,
        or every tooling commit reads as a data drift."""
        r = self.row(self.consumer(self.c_new)[0])
        self.assertEqual(r["behind"], 1)
        self.assertTrue(r["canonical_same"])

    def test_a_pin_off_origin_main_is_flagged(self):
        """A pin on a side branch (never landed) is not 'N behind' alone: it has commits main lacks."""
        _git(self.ds, "checkout", "-qb", "side", self.c_new)
        side = _commit_file(self.ds, "side.txt", "s", "side only")
        r = self.row(self.consumer(side)[0])
        self.assertEqual((r["behind"], r["ahead"]), (1, 1))
        self.assertIn("NOT on", r["note"])

    def test_the_text_line_carries_the_count(self):
        r = self.row(self.consumer(self.c_old)[0])
        line = gate.format_row(r)
        self.assertIn("2 dataset commit(s) behind", line)
        self.assertIn("canonical differs", line)


class TestReadsOriginNotCheckout(_World):
    def test_an_unpushed_local_pin_is_ignored(self):
        """The consumer's local clone moves its pin to c_tool and does NOT push. What ships is origin's
        pin (c_old), so the report must say 2 behind, not 0."""
        c, work = self.consumer(self.c_old)
        _git(work, "update-index", "--cacheinfo", f"160000,{self.c_tool},{c[4]}")
        _git(work, "commit", "-qm", "local bump, unpushed")
        r = self.row(c)
        self.assertEqual((r["pinned"], r["behind"]), (self.c_old, 2))

    def test_the_branch_named_is_the_branch_read(self):
        """origin carries the pin on `feat/community-foundation`; a second branch pinning something
        else must not leak in."""
        c, work = self.consumer(self.c_old)
        _git(work, "checkout", "-qb", "other")
        _git(work, "update-index", "--cacheinfo", f"160000,{self.c_tool},{c[4]}")
        _git(work, "commit", "-qm", "other branch")
        _git(work, "push", "-q", c[2], "HEAD:refs/heads/other")
        self.assertEqual(self.row(c)["pinned"], self.c_old)


class TestStalePinReportsAndNeverFails(_World):
    """Ruling item 5: a stale consumer pin produces a report and no failure."""

    def test_a_stale_pin_exits_zero_and_says_how_far_behind(self):
        app, _ = self.consumer(self.c_old)
        astro, _ = self.consumer(self.c_new, check="E3", label="astro", branch="main",
                                 path="plant-dataset")
        rc, out = self.cli([app, astro])
        self.assertEqual(rc, 0, out)
        self.assertIn("E1 app (feat/community-foundation:vendor/plant-dataset): pin "
                      f"{self.c_old[:7]}, 2 dataset commit(s) behind", out)
        self.assertIn(f"E3 astro (main:plant-dataset): pin {self.c_new[:7]}, 1 dataset commit(s) behind", out)
        self.assertIn("2 measured, 0 unmeasured", out)

    def test_an_unmeasured_pin_also_exits_zero(self):
        c = ("E1", "app", os.path.join(self.tmp, "absent.git"), "main", "vendor/plant-dataset")
        rc, out = self.cli([c])
        self.assertEqual(rc, 0, out)
        self.assertIn("E1 UNMEASURED", out)

    def test_the_cli_entry_point_exits_zero_as_a_process(self):
        """The script as the shell runs it, stale or not: rc 0 (main()'s return reaches sys.exit)."""
        r = subprocess.run([sys.executable, os.path.abspath(gate.__file__), "--help"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        src = open(gate.__file__).read()
        self.assertIn("    sys.exit(main())", src)


class TestUnmeasured(_World):
    def assertUnmeasured(self, r, fragment):
        self.assertFalse(r["measured"], r)
        self.assertIsNone(r["behind"], r)
        self.assertIn(fragment, r["note"])

    def test_an_unreachable_origin_is_unmeasured_not_zero(self):
        c = ("E1", "app", os.path.join(self.tmp, "absent.git"), "main", "vendor/plant-dataset")
        self.assertUnmeasured(self.row(c), "could not fetch")

    def test_a_branch_without_the_gitlink_is_unmeasured(self):
        c, _ = self.consumer(self.c_tool)
        c = c[:4] + ("not/the/path",)
        self.assertUnmeasured(self.row(c), "records no")

    def test_a_path_that_is_not_a_gitlink_is_unmeasured(self):
        c, _ = self.consumer(self.c_tool)
        c = c[:4] + ("README.md",)
        self.assertUnmeasured(self.row(c), "not a submodule gitlink")

    def test_a_pin_this_repo_cannot_resolve_is_unmeasured(self):
        foreign = _init(os.path.join(self.tmp, "foreign"))
        f_head = _commit_file(foreign, gate.CANONICAL, '{"crops":[]}', "unrelated history")
        self.assertUnmeasured(self.row(self.consumer(f_head)[0]), "not in this repo's history")

    def test_no_origin_main_ref_is_unmeasured(self):
        c, _ = self.consumer(self.c_tool)
        _git(self.ds, "update-ref", "-d", gate.DATASET_REF)
        self.assertUnmeasured(self.row(c), "has no")

    def test_unmeasured_is_counted_apart_from_measured(self):
        good, _ = self.consumer(self.c_tool)
        bad = ("E3", "astro", os.path.join(self.tmp, "absent.git"), "main", "plant-dataset")
        r = gate.report(consumers=[good, bad], dataset_root=self.ds, fetch=False)
        self.assertEqual((r["measured"], r["unmeasured"]), (1, 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
