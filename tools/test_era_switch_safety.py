"""The era switch (SBR_KNOWN_AT_ARMING) can never let LIVE data pass against an older waiver set (Trevor, PLA-673 B2
go-condition 2, 2026-10-06).

  whole_crop_gate / gate_all: with the switch set to anything that is not the gated file's own registered historical
    SHA, they REFUSE (rc 2, no PASS verdict), and they refuse BEFORE gating, so no partial verdict prints. The live
    canonical is never a valid era file.
  pre-commit hook: strips the switch from the gate subprocesses it runs (it always gates against the live set), and
    refuses a gate run that printed no verdict, so a refusing or crashing gate never reads as "no violations".
Mutation harness: tools/mutate_era_switch_safety.py.
"""
import hashlib, os, subprocess, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
sys.path.insert(0, HERE)
import precommit_release_verify as H  # noqa: E402
import sourced_block_ratchet_gate as G  # noqa: E402

LIVE_SHA = hashlib.sha256(open(CANON, "rb").read()).hexdigest()
AFBD = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"
GLOSS = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"
VALUES = ["1", LIVE_SHA, AFBD, GLOSS]   # the old flag, the live SHA, both registered replays (neither is this file
                                        # unless canonical IS one, and then it is the live canonical: refused too)


def _run(script, *args, env_value):
    env = dict(os.environ, **{G.ERA_ENV: env_value})
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True,
                       cwd=REPO, env=env)
    return r.returncode, r.stdout + r.stderr


@pytest.mark.parametrize("value", VALUES)
def test_whole_crop_gate_refuses_the_switch_on_live_data(value):
    rc, out = _run("whole_crop_gate.py", "eggplant", CANON, env_value=value)
    assert rc == 2, out[-400:]
    assert "ERA SWITCH REFUSED" in out
    assert "GATE: PASS" not in out and "GATE:" not in out


@pytest.mark.parametrize("value", ["1", LIVE_SHA])
def test_gate_all_refuses_the_switch_on_live_data(value):
    rc, out = _run("gate_all.py", CANON, env_value=value)
    assert rc == 2, out[-400:]
    assert "ERA SWITCH REFUSED" in out
    assert "gate_all: PASS" not in out and "ran whole_crop_gate" not in out


def test_the_hook_strips_the_switch_from_its_gate_runs(monkeypatch):
    """With the switch set in the committer's shell, the hook's gate run is the LIVE gate: it prints a verdict."""
    monkeypatch.setenv(G.ERA_ENV, "1")
    seen = {}
    real = subprocess.run

    def spy(cmd, **k):
        seen["env"] = k.get("env")
        return real(cmd, **k)
    monkeypatch.setattr(H.subprocess, "run", spy)
    H.gate_violations(CANON, "eggplant")          # raises if the gate refused (no verdict)
    assert seen["env"] is not None and G.ERA_ENV not in seen["env"]


def _fake_gate(tmp_path, body):
    p = tmp_path / "fake_gate.py"
    p.write_text(body, encoding="utf-8")
    return str(p)


def test_the_hook_refuses_a_gate_run_with_no_verdict(tmp_path, monkeypatch):
    monkeypatch.setattr(H, "GATE", _fake_gate(tmp_path, "import sys\nprint('ERA SWITCH REFUSED: x')\nsys.exit(2)\n"))
    with pytest.raises(RuntimeError, match="no GATE verdict"):
        H.gate_violations(CANON, "eggplant")


def test_the_hook_still_reads_a_violation_verdict(tmp_path, monkeypatch):
    """Positive control for the refusal above: a gate that DID gate (verdict printed) is read, violations kept."""
    monkeypatch.setattr(H, "GATE", _fake_gate(
        tmp_path, "import sys\nprint('  VIOLATION: x')\nprint('GATE: 1 VIOLATION(S)')\nsys.exit(1)\n"))
    assert H.gate_violations(CANON, "eggplant") == {"VIOLATION: x"}
