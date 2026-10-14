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
B2 = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"     # PLA-673 part B2 post-state
PART_D = "5420479d85bb8b65be62fa459fd97b8ce12dfdf9d3951e455be52aadc7a98063"  # PLA-673 part D post-state
VALUES = ["1", LIVE_SHA, AFBD, GLOSS, B2, PART_D]   # the old flag, the live SHA, every registered replay (none is this
                                                    # file unless canonical IS one, and then it is live: refused too)


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


@pytest.mark.parametrize("slug", ["grapefruit", "orange-navel"])
def test_a_registered_replay_gates_A62_A63_A64_against_their_era_sets(slug, tmp_path):
    """END TO END, the subprocess path the landed promotes take (2026-10-14, PLA-625 citrus promote 1): B2's post-state
    predates promote 1, which closed six identities across A62, A63 and A64 on these two crops. Unset, the live sets
    flag them; set and bound to the file, all three gates use their era sets and the crop passes."""
    import promote_fixture
    p = tmp_path / "b2_post.json"
    p.write_bytes(promote_fixture.pre_state(B2))
    env = {k: v for k, v in os.environ.items() if k != G.ERA_ENV}
    r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, str(p)], capture_output=True,
                       text=True, cwd=REPO, env=env)
    out = r.stdout + r.stderr
    assert r.returncode == 1, out[-400:]
    for gate in ("sourced-block-ratchet: NEW uncited block", "bare-host: NEW sole bare-host citation"):
        assert gate in out, gate
    assert ("rootstock-prose: grapefruit" in out) == (slug == "grapefruit")
    rc, out = _run("whole_crop_gate.py", slug, str(p), env_value=B2)
    assert rc == 0 and "GATE: PASS" in out, out[-400:]


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
