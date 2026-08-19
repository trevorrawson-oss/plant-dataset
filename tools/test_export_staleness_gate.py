#!/usr/bin/env python3
"""Guards for export_staleness_gate (PLA-258).

The defect this gate exists to catch, stated once: on 2026-08-19 the shipped app export
and the plant-astro submodule pin were BOTH built from canonical b0d01f13 (dataset commit
8a5398a, 2026-07-29), while canonical was 3bf8b4ce. Three content promotes -- including
PLA-202's 22 verbatim rewrites -- were absent from both surfaces, and nothing anywhere
could report that. The export was a BYTE-FAITHFUL projection of a stale canonical, so no
value check on the artifact could ever have found it: the only detectable signal is the
PROVENANCE of the bytes, which was not recorded at all.

Every guard below is built to fail on a real staleness shape, not on a synthetic one.
Mutation evidence: tools/mutate_export_staleness_suite.py.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_staleness_gate as gate


CANON_A = '{"crops":[{"slug":"a"}],"schema_version":"1"}'   # "current" canonical
CANON_B = '{"crops":[{"slug":"b"}],"schema_version":"1"}'   # an older canonical


def _sha(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout.strip()


def _git_or_none(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def _init_repo(path):
    os.makedirs(path, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "t")
    return path


def _make_dataset_repo(root):
    """A dataset repo with two canonical revisions: OLD (CANON_B) then CURRENT (CANON_A)."""
    ds = _init_repo(os.path.join(root, "plant-dataset"))
    canon = os.path.join(ds, "crops_data_final.json")
    with open(canon, "w") as f:
        f.write(CANON_B)
    _git(ds, "add", "crops_data_final.json")
    _git(ds, "commit", "-qm", "old canonical")
    old_commit = _git(ds, "rev-parse", "HEAD")
    with open(canon, "w") as f:
        f.write(CANON_A)
    _git(ds, "add", "crops_data_final.json")
    _git(ds, "commit", "-qm", "current canonical")
    cur_commit = _git(ds, "rev-parse", "HEAD")
    return ds, canon, old_commit, cur_commit


def _make_astro_repo(root, pinned_commit):
    """An astro repo whose `plant-dataset` path is a gitlink pinned at `pinned_commit`."""
    astro = _init_repo(os.path.join(root, "plant-astro"))
    with open(os.path.join(astro, "README.md"), "w") as f:
        f.write("astro\n")
    _git(astro, "add", "README.md")
    _git(astro, "update-index", "--add", "--cacheinfo", f"160000,{pinned_commit},plant-dataset")
    _git(astro, "commit", "-qm", "pin submodule")
    return astro


def _make_app(root, stamped_sha, artifact_bodies=None, artifact_keys=None):
    """An app repo carrying the four generated artifacts plus a provenance manifest.

    `stamped_sha`     -- what the manifest CLAIMS it was built from.
    `artifact_bodies` -- override an artifact's on-disk bytes (simulates a hand edit).
    `artifact_keys`   -- override the manifest's artifact key set (simulates drift).
    """
    app = os.path.join(root, "plant-app")
    bodies = dict(artifact_bodies or {})
    recorded = {}
    for rel in gate.APP_ARTIFACTS:
        body = bodies.get(rel, f"body-of-{rel}")
        full = os.path.join(app, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(body)
        recorded[rel] = _sha(body)
    if artifact_keys is not None:
        recorded = {k: recorded.get(k, _sha("x")) for k in artifact_keys}
    manifest = {
        "canonical_sha256": stamped_sha,
        "dataset_commit": "deadbeef",
        "built_at": "2026-08-19T00:00:00Z",
        "artifacts": recorded,
    }
    mpath = os.path.join(app, gate.APP_PROVENANCE)
    os.makedirs(os.path.dirname(mpath), exist_ok=True)
    with open(mpath, "w") as f:
        json.dump(manifest, f)
    return app, mpath


class _Fixture(unittest.TestCase):
    """A world where every surface is CURRENT. Each guard breaks exactly one thing."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, self.tmp, True)
        self.ds, self.canon, self.old_commit, self.cur_commit = _make_dataset_repo(self.tmp)
        self.canon_sha = _sha(CANON_A)
        self.astro = _make_astro_repo(self.tmp, self.cur_commit)
        self.app, self.manifest_path = _make_app(self.tmp, self.canon_sha)

    def run_gate(self, **over):
        kw = dict(canonical_path=self.canon, app_root=self.app,
                  astro_root=self.astro, dataset_root=self.ds)
        kw.update(over)
        return gate.all_violations(**kw)

    def rewrite_manifest(self, **changes):
        with open(self.manifest_path) as f:
            m = json.load(f)
        m.update(changes)
        with open(self.manifest_path, "w") as f:
            json.dump(m, f)


class TestPositiveControl(_Fixture):
    def test_a_fully_current_world_is_clean(self):
        """The control. If this is not 0, every RED below proves nothing."""
        self.assertEqual(self.run_gate(), [])

    def test_the_fixture_canonical_sha_is_actually_what_the_gate_computes(self):
        """Guards against the whole suite testing a hash the gate never produces."""
        self.assertEqual(gate.canonical_sha256(self.canon), self.canon_sha)


class TestE1AppProvenance(_Fixture):
    def test_a_stale_stamp_is_caught(self):
        """THE PLA-258 DEFECT: the artifact is internally consistent, but built from an
        older canonical. This is the shape that shipped for three weeks."""
        self.rewrite_manifest(canonical_sha256=_sha(CANON_B))
        v = self.run_gate()
        self.assertTrue(any("E1" in x for x in v), v)
        self.assertTrue(any(_sha(CANON_B)[:12] in x for x in v), v)

    def test_a_missing_manifest_is_caught_not_skipped(self):
        """An export with NO provenance is the pre-PLA-258 world. It must not read as
        current merely because there is nothing to contradict."""
        os.remove(self.manifest_path)
        v = self.run_gate()
        # Asserts the SPECIFIC condition, not merely that some E1 fired. The unreadable-
        # stamp guard reports the same family, so a loose `any("E1" ...)` here stays green
        # when this guard is deleted -- the mutation harness found exactly that.
        self.assertTrue(any("no provenance stamp" in x for x in v), v)

    def test_a_manifest_without_a_canonical_sha_is_caught(self):
        self.rewrite_manifest(canonical_sha256=None)
        self.assertTrue(any("E1" in x for x in self.run_gate()))

    def test_an_unparseable_manifest_is_caught_not_swallowed(self):
        with open(self.manifest_path, "w") as f:
            f.write("{not json")
        self.assertTrue(any("E1" in x for x in self.run_gate()))


class TestE2AppIntegrity(_Fixture):
    def test_a_hand_edited_artifact_is_caught(self):
        """The stamp cannot be the only evidence: an artifact edited after the build
        would otherwise carry a truthful-looking provenance record."""
        target = os.path.join(self.app, gate.APP_ARTIFACTS[0])
        with open(target, "w") as f:
            f.write("tampered")
        v = self.run_gate()
        self.assertTrue(any("E2" in x for x in v), v)

    def test_a_missing_artifact_is_caught(self):
        os.remove(os.path.join(self.app, gate.APP_ARTIFACTS[1]))
        self.assertTrue(any("E2" in x for x in self.run_gate()))

    def test_an_artifact_the_manifest_forgot_is_caught(self):
        """PLA-162's shape, at the export boundary. Iterating only what the manifest
        RECORDS makes a newly generated artifact invisible -- so the gate asserts the
        key sets are EQUAL before it compares any hash. A build that starts emitting a
        fifth file must fail here until it is stamped deliberately."""
        _, self.manifest_path = _make_app(
            self.tmp, self.canon_sha, artifact_keys=list(gate.APP_ARTIFACTS[:-1]))
        v = self.run_gate()
        self.assertTrue(any("E2" in x for x in v), v)
        self.assertTrue(any(gate.APP_ARTIFACTS[-1] in x for x in v), v)

    def test_an_artifact_the_manifest_invented_is_caught(self):
        _, self.manifest_path = _make_app(
            self.tmp, self.canon_sha,
            artifact_keys=list(gate.APP_ARTIFACTS) + ["src/data/ghost.json"])
        v = self.run_gate()
        self.assertTrue(any("E2" in x and "ghost" in x for x in v), v)


class TestE3AstroPin(_Fixture):
    def test_a_stale_submodule_pin_is_caught(self):
        """THE OTHER HALF OF PLA-258. Regenerating the app export while the site still
        serves a pin from three weeks ago moves the gap one step down the pipeline
        instead of closing it."""
        astro = _make_astro_repo(os.path.join(self.tmp, "stale"), self.old_commit)
        v = self.run_gate(astro_root=astro)
        self.assertTrue(any("E3" in x for x in v), v)

    def test_a_pin_at_a_commit_the_dataset_does_not_have_is_caught(self):
        """An unpushed or rewritten pin cannot be verified, and unverifiable is not green.
        The foreign commit is real (from an unrelated repo) rather than synthetic, so the
        gate is exercised on a well-formed gitlink it genuinely cannot resolve."""
        foreign = _init_repo(os.path.join(self.tmp, "foreign"))
        with open(os.path.join(foreign, "crops_data_final.json"), "w") as f:
            f.write('{"crops":[{"slug":"unrelated-history"}]}')
        _git(foreign, "add", "crops_data_final.json")
        _git(foreign, "commit", "-qm", "a history this repo has never seen")
        foreign_head = _git(foreign, "rev-parse", "HEAD")
        self.assertIsNone(_git_or_none(self.ds, "cat-file", "-e", foreign_head),
                          "fixture broken: the 'foreign' commit is resolvable in the dataset repo")
        astro = _make_astro_repo(os.path.join(self.tmp, "unknown"), foreign_head)
        v = self.run_gate(astro_root=astro)
        self.assertTrue(any("E3" in x for x in v), v)

    def test_a_repo_with_no_submodule_entry_is_caught(self):
        astro = _init_repo(os.path.join(self.tmp, "nosub"))
        with open(os.path.join(astro, "x"), "w") as f:
            f.write("x")
        _git(astro, "add", "x")
        _git(astro, "commit", "-qm", "no submodule")
        v = self.run_gate(astro_root=astro)
        # `git ls-tree` exits 0 with EMPTY stdout for an absent path, so the gitlink-shape
        # guard below also fires on this input. Asserting the specific message keeps the two
        # guards independently pinned instead of each masking the other's removal.
        self.assertTrue(any("records no" in x for x in v), v)


class TestUnmeasuredIsNotGreen(_Fixture):
    """The arc's recurring failure is an instrument that reports a zero over a population
    it never looked at. An absent repo is UNMEASURED and must say so."""

    def test_an_absent_app_repo_reports_unmeasured_not_clean(self):
        v = self.run_gate(app_root=os.path.join(self.tmp, "nope"))
        self.assertTrue(any("UNMEASURED" in x for x in v), v)

    def test_an_absent_astro_repo_reports_unmeasured_not_clean(self):
        v = self.run_gate(astro_root=os.path.join(self.tmp, "nope"))
        self.assertTrue(any("UNMEASURED" in x for x in v), v)

    def test_unmeasured_is_distinguishable_from_a_violation(self):
        """A caller must be able to tell 'I could not look' from 'I looked and it is
        stale' -- collapsing them is how a gate starts lying in either direction."""
        report = gate.report(canonical_path=self.canon,
                             app_root=os.path.join(self.tmp, "nope"),
                             astro_root=self.astro, dataset_root=self.ds)
        self.assertEqual(report["violations"], [])
        self.assertTrue(report["unmeasured"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
