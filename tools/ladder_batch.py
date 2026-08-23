#!/usr/bin/env python3
"""The ladder-rollout batch runner. Everything a session needs to run one 5-crop batch.

READ docs/ladder_batch_playbook.md FIRST -- it is the procedure; this is the tooling.

The rollout is ~22 remaining batches of ~5 crops. Before this existed, each batch meant
hand-rolling the same four steps and re-deriving the same decisions from a chat transcript. This
script makes the mechanical parts one command each, so the only expensive step left is the one that
should be expensive: READING the authored prose.

  prepare  pick/accept 5 crops, emit the catalog brief + per-crop inputs + the bot prompts
  merge    fold the bots' JSON back onto a scratch canonical
  verify   run the real gates on the merge, plus the checks that catch what gates cannot
  status   how far the rollout has got

WHY EACH STEP EXISTS, in defects that actually happened:
  * `prepare` regenerates the brief FROM CANONICAL every time. Batch 1 was authored against a
    37-method catalog that grew to 43 mid-batch; a stale brief silently produces ladders that omit
    controls the crop's own prose names.
  * `merge` REUSES EXISTING PROBLEM IDS when a crop already has them. Ids are join keys for
    `varieties[].resistance` and `ladder_delta`; two authoring passes over the same crops produced
    `leafminer` vs `beet-spinach-leafminer`. See CLAUDE.md's hard rule.
  * `verify` includes METHOD-MEANING checks. The worst defect of batch 1 passed every gate and every
    mutation harness: `bottom_watering` means "water from below, in trays" and twelve rungs used it
    to mean "water at the base, outdoors". No structural gate can see that. This step cannot see it
    either -- but it prints what a human must compare.

Usage:
  python3 tools/ladder_batch.py status
  python3 tools/ladder_batch.py prepare --crops a,b,c,d,e [--out DIR]
  python3 tools/ladder_batch.py merge   --out DIR
  python3 tools/ladder_batch.py verify  --out DIR
"""
import argparse
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANON = os.path.join(REPO, "crops_data_final.json")


def load():
    return json.load(open(CANON))


def problems(crop):
    return [(f, p) for f in ("pests", "diseases")
            for p in crop.get(f) or [] if isinstance(p, dict)]


def laddered(crop):
    return any("control_ladder" in p for _f, p in problems(crop))


# ---------------------------------------------------------------- status
def cmd_status(a):
    d = load()
    cert = [c for c in d["crops"]
            if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    done = [c for c in cert if laddered(c)]
    todo = [c for c in cert if not laddered(c)]
    n_prob = sum(len(problems(c)) for c in todo)
    print(f"catalog methods        : {len(d['control_methods'])}")
    print(f"certified crops        : {len(cert)}")
    print(f"  laddered             : {len(done)}  {sorted(c['slug'] for c in done)}")
    print(f"  remaining            : {len(todo)}   ({n_prob} problems)")
    print(f"  batches of 5 left    : {round(len(todo) / 5 + 0.49)}")
    print()
    print("next candidates (fewest problems first, so a batch is a readable size):")
    for c in sorted(todo, key=lambda c: len(problems(c)))[:12]:
        print(f"    {c['slug']:22s} {len(problems(c)):2d} problems   {c.get('category','')}")


# ---------------------------------------------------------------- prepare
def cmd_prepare(a):
    from control_ladder_gate import TYPE_TARGETS
    d = load()
    cm = d["control_methods"]
    by = {c["slug"]: c for c in d["crops"]}
    crops = [s.strip() for s in a.crops.split(",") if s.strip()]
    for s in crops:
        if s not in by:
            raise SystemExit(f"ABORT: no crop {s!r}")
        if laddered(by[s]):
            raise SystemExit(f"ABORT: {s} is already laddered; re-laddering changes shipped ids")
    os.makedirs(a.out, exist_ok=True)

    # -- the brief, ALWAYS regenerated from canonical --------------------------------
    lines = [f"# CONTROL-METHOD CATALOG -- the ONLY {len(cm)} methods a rung may name.",
             "# Ladder order is by tier: cultural < physical < biological < soft_chemical < conventional.",
             ""]
    for tier in ("cultural", "physical", "biological", "soft_chemical", "conventional"):
        lines.append(f"## {tier}")
        for k, v in sorted(cm.items()):
            if v["tier"] == tier:
                lines.append(f"  {k:28s} applies_to={sorted(v['applies_to'])}")
                lines.append(f"      MEANS: {v['best_use'][:150]}")
        lines.append("")
    lines.append("# problem.type -> applies_to targets that legitimately fit it.")
    lines.append("# A rung is INVALID unless its method's applies_to includes 'any' OR overlaps this set.")
    for t, s in sorted(TYPE_TARGETS.items()):
        lines.append(f"  {t:15s} {sorted(s)}")
    brief = os.path.join(a.out, "brief_catalog.md")
    open(brief, "w").write("\n".join(lines))

    total = 0
    for s in crops:
        c = by[s]
        slim = {"slug": s, "name": c.get("name"), "category": c.get("category"),
                "pests": c.get("pests", []), "diseases": c.get("diseases", [])}
        json.dump(slim, open(os.path.join(a.out, f"{s}_source.json"), "w"),
                  indent=1, ensure_ascii=False)
        total += len(problems(c))

    est = total * 3.7
    print(f"prepared {len(crops)} crops in {a.out}")
    print(f"  brief         : {brief}  ({len(cm)} methods)")
    print(f"  problems      : {total}")
    print(f"  expect approx : {est:.0f} rungs, {est*2:.0f} register strings to READ")
    if est * 2 > 400:
        print("  ^^ WARNING: over ~400 strings is where reading becomes skimming. Consider fewer crops.")
    print()
    print("Now launch ONE authoring agent per crop with the prompt in")
    print("  docs/ladder_batch_playbook.md  (section 2), substituting the crop slug.")
    print(f"Each agent writes {a.out}/out_<slug>.json")


# ---------------------------------------------------------------- merge
def cmd_merge(a):
    d = load()
    by = {c["slug"]: c for c in d["crops"]}
    outs = sorted(f for f in os.listdir(a.out) if f.startswith("out_") and f.endswith(".json"))
    if not outs:
        raise SystemExit(f"ABORT: no out_*.json in {a.out}")
    reused = minted = rungs = 0
    for f in outs:
        slug = f[4:-5]
        o = json.load(open(os.path.join(a.out, f)))
        crop = by[slug]
        for fam in ("pests", "diseases"):
            src = o.get(fam, [])
            if len(src) != len(crop.get(fam, [])):
                raise SystemExit(f"ABORT: {slug}/{fam} length {len(src)} != canonical "
                                 f"{len(crop.get(fam, []))}; the bot dropped or added a problem")
            for i, add in enumerate(src):
                tgt = crop[fam][i]
                # ID STABILITY (CLAUDE.md hard rule): an existing id is a join key. Never overwrite.
                if isinstance(tgt.get("id"), str) and tgt["id"]:
                    if tgt["id"] != add["id"]:
                        print(f"  id REUSED (bot proposed a different one): {slug}/{tgt['id']} "
                              f"(bot said {add['id']!r})")
                    reused += 1
                else:
                    tgt["id"] = add["id"]; minted += 1
                tgt["type"] = add["type"]
                tgt["control_ladder"] = add["control_ladder"]
                rungs += len(add["control_ladder"])
    out = os.path.join(a.out, "scratch_canonical.json")
    json.dump(d, open(out, "w"), separators=(",", ":"), ensure_ascii=False)
    print(f"merged {len(outs)} crops -> {out}")
    print(f"  ids minted {minted} | ids reused {reused} | rungs {rungs}")


# ---------------------------------------------------------------- verify
def cmd_verify(a):
    import re
    scratch = os.path.join(a.out, "scratch_canonical.json")
    if not os.path.exists(scratch):
        raise SystemExit("ABORT: run `merge` first")
    print("=== GATES (structural) ===")
    ok = True
    for tool in ("control_ladder_gate.py", "variety_resistance_gate.py",
                 "variety_ladder_delta_gate.py", "register_completeness_gate.py"):
        r = subprocess.run([sys.executable, os.path.join(REPO, "tools", tool), scratch],
                           capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        print(f"  {tool:34s} {last[:60]}")
        ok &= r.returncode == 0
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "gate_all.py"), scratch],
                       capture_output=True, text=True)
    print(f"  {'gate_all.py':34s} {(r.stdout.strip().splitlines() or ['?'])[-1][:60]}")
    ok &= r.returncode == 0

    d = json.load(open(scratch))
    cm = d["control_methods"]
    base = load()
    changed = [c for c in d["crops"]
               if c != next(x for x in base["crops"] if x["slug"] == c["slug"])]

    print("\n=== COPY HYGIENE (new rung prose only) ===")
    strs = [(f"{c['slug']}/{p.get('id')}", r[k])
            for c in changed for _f, p in problems(c) if p.get("control_ladder")
            for r in p["control_ladder"] for k in r if k.startswith("note_")]
    BR = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre", "mould",
          "grey", "labour", "practise")
    checks = {
        "em/en dash": lambda t: re.search(r"[—–]", t),
        "double hyphen": lambda t: "--" in t,
        "absolute claim": lambda t: re.search(
            r"\b(always|guaranteed|completely|totally|harmless)\b", t, re.I),
        "spaced degF": lambda t: re.search(r"\s°F", t),
        "British spelling": lambda t: any(re.search(rf"\b{w}\b", t, re.I) for w in BR),
    }
    print(f"  strings: {len(strs)}")
    for name, fn in checks.items():
        hits = [w for w, t in strs if fn(t)]
        print(f"    {name:18s} {len(hits)}" + (f"   e.g. {hits[0]}" if hits else ""))
        ok &= not hits

    print("\n=== METHOD-MEANING: what a human must compare (NO GATE CAN DO THIS) ===")
    print("  The worst defect of batch 1 passed every gate AND its mutation harness:")
    print("  `bottom_watering` MEANS 'water from below, in trays'; twelve rungs used it to mean")
    print("  'water at the base, outdoors'. Read each pair below and ask: is the RUNG describing")
    print("  the ACTION the METHOD describes, or a different action that merely sounds similar?\n")
    seen = set()
    for c in changed:
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                m = r["method"]
                if (c["slug"], m) in seen:
                    continue
                seen.add((c["slug"], m))
                print(f"  --- {c['slug']}/{p.get('id')} :: {m}")
                print(f"      METHOD MEANS: {cm[m]['best_use'][:104]}")
                print(f"      RUNG SAYS   : {r.get('note_beginner','')[:104]}")
    print(f"\n  {len(seen)} crop/method pairs to compare.")
    print("\n" + ("VERIFY: structural checks PASS" if ok else "VERIFY: FAILURES ABOVE"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    p = sub.add_parser("prepare"); p.add_argument("--crops", required=True); p.add_argument("--out", required=True)
    p = sub.add_parser("merge");   p.add_argument("--out", required=True)
    p = sub.add_parser("verify");  p.add_argument("--out", required=True)
    a = ap.parse_args()
    return {"status": cmd_status, "prepare": cmd_prepare,
            "merge": cmd_merge, "verify": cmd_verify}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
