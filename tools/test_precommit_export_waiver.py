#!/usr/bin/env python3
"""Drivers for the pre-commit hook's EXPORT_WAIVERS (PLA-581, ruled 2026-09-24).

The waiver is keyed on IDENTITY (the E1 app-provenance check, never E2) AND CHARACTER (the export
stamped at exactly d7b33682f992). Every driver here goes through the REAL `export_currency_concerns`
path against a SYNTHETIC plant-app stamp in a temp dir, so it never depends on the live app and does
not move when the app is rebuilt. SHIPS MUTATION-TESTED via mutate_precommit_export_waiver.py.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import precommit_release_verify as H  # noqa: E402
import export_staleness_gate as esg  # noqa: E402

FROZEN = "d7b33682f9926e3aef176ef8a1bb1f3191143957ca40c94e36433abd883a2798"  # the waived stamp
OTHER = "526788f2c34a7fe1c59e9427271c1d1738c6b6cce2c1d0524df715e4fc359659"
NOW = "83384c85d9daccc71b3d4a0da795872a761538b0e4d8e94b0d401a674a8a6cd6"


def make_app(root, stamped, drop_artifact=False):
    """A minimal plant-app whose provenance stamp says `stamped`, with every artifact present and
    hashed, so E2 is clean unless asked to break it."""
    arts = {}
    for rel in esg.APP_ARTIFACTS:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(rel.encode())
        arts[rel] = hashlib.sha256(rel.encode()).hexdigest()
    if drop_artifact:
        arts.pop(sorted(arts)[0])
    mp = os.path.join(root, esg.APP_PROVENANCE)
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    with open(mp, "w") as f:
        json.dump({"canonical_sha256": stamped, "artifacts": arts}, f)
    return root


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="exportwaiver_")
        self._index = H._index_bytes

    def tearDown(self):
        H._index_bytes = self._index
        shutil.rmtree(self.tmp, ignore_errors=True)

    def concerns(self, stamped, canonical_sha=NOW, **kw):
        """The hook's E1/E2 violations for an app stamped at `stamped`, with a staged canonical
        whose sha256 is `canonical_sha` (the index read is stubbed; nothing else is)."""
        app = make_app(os.path.join(self.tmp, "app"), stamped, **kw)
        real = esg.sha256_bytes
        esg.sha256_bytes = lambda b: canonical_sha
        H._index_bytes = lambda rel: b"{}" if rel == "crops_data_final.json" else None
        try:
            return H.export_currency_concerns(["crops_data_final.json"], app)
        finally:
            esg.sha256_bytes = real


class Waiver(Base):
    def test_the_known_stale_export_is_waived(self):
        v = self.concerns(FROZEN)
        self.assertEqual(len(v), 1, v)
        unwaived, waived, stale = H.apply_export_waivers(v)
        self.assertEqual(unwaived, [])
        self.assertEqual([n for _, n in waived], ["E1 app-provenance"])
        self.assertEqual(stale, [])

    def test_a_different_stale_sha_is_not_waived(self):
        """An export rebuilt at another SHA and still stale is a DIFFERENT fact: it blocks."""
        v = self.concerns(OTHER)
        unwaived, waived, _ = H.apply_export_waivers(v)
        self.assertEqual(waived, [])
        self.assertEqual(len(unwaived), 1)
        self.assertIn("526788f2c34a", unwaived[0])

    def test_e2_is_never_waived(self):
        """The waiver covers E1 at the frozen stamp. An E2 integrity failure riding along blocks."""
        v = self.concerns(FROZEN, drop_artifact=True)
        unwaived, waived, _ = H.apply_export_waivers(v)
        self.assertEqual([n for _, n in waived], ["E1 app-provenance"])
        self.assertTrue(unwaived and all(u.startswith("E2 ") for u in unwaived), unwaived)

    def test_a_current_export_has_nothing_to_waive_and_the_waiver_reads_stale(self):
        v = self.concerns(NOW)
        self.assertEqual(v, [])
        unwaived, waived, stale = H.apply_export_waivers(v)
        self.assertEqual((unwaived, waived, stale), ([], [], ["E1 app-provenance"]))

    def test_the_character_needs_the_whole_frozen_prefix(self):
        """A stamp sharing only the first 8 hex of the frozen SHA is not the frozen export."""
        near = FROZEN[:8] + "0" * 56
        unwaived, waived, _ = H.apply_export_waivers(self.concerns(near))
        self.assertEqual(waived, [])
        self.assertEqual(len(unwaived), 1)

    def test_the_waiver_carries_its_ticket_and_reason(self):
        w = H.EXPORT_WAIVERS["E1 app-provenance"]
        self.assertEqual(w["ticket"], "PLA-465")
        self.assertIn("378c7b9f", w["reason"])
        self.assertEqual(sorted(H.EXPORT_WAIVERS), ["E1 app-provenance"])


class Wiring(Base):
    """The hook's main(): the waiver decides the verdict. git, the roster arm and the regression arm
    are stubbed; the export arm returns the violation under test."""

    def run_main(self, violations):
        from unittest import mock
        fake = mock.Mock(stdout="crops_data_final.json\n")
        with mock.patch.object(H.subprocess, "run", return_value=fake), \
             mock.patch.object(H, "roster_claim_concerns", return_value=[]), \
             mock.patch.object(H, "_blob", return_value=os.path.join(self.tmp, "nope.json")), \
             mock.patch.object(H, "check", return_value=[]), \
             mock.patch.object(H, "export_currency_concerns", return_value=violations), \
             mock.patch.object(sys, "argv", ["hook"]):
            return H.main()

    def frozen_violation(self):
        return (f"E1 app-provenance: export was built from canonical {FROZEN[:12]} but canonical is "
                f"now {NOW[:12]}. The shipped artifact is STALE -- run `npm run build:guides` in x.")

    def test_main_passes_on_the_waived_export(self):
        self.assertEqual(self.run_main([self.frozen_violation()]), 0)

    def test_main_blocks_on_an_unwaived_export(self):
        other = self.frozen_violation().replace(FROZEN[:12], OTHER[:12])
        self.assertEqual(self.run_main([other]), 1)


if __name__ == "__main__":
    unittest.main()
