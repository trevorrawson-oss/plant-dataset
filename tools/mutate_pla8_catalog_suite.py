#!/usr/bin/env python3
"""Mutation harness for the PLA-8 catalog-extension promote suite (PLA-215 convention).

WHY. `test_promote_pla8_catalog_extension.py` is replay-pinned and green from birth, so "31 tests
pass" is not evidence. This harness is. It corrupts the authored CONTENT and the PROMOTE one guard
family at a time and requires the suite to notice.

The sourcing families matter most here. An anchor URL pointing at the wrong document, or a hedge
quietly dropped from `cons`, is invisible to every structural gate in this repo -- shape checks
cannot see whether prose matches the paper it claims. Those guards are the reason this suite exists,
so they are the ones that most need proving.

LIVENESS DEFENSE: POSITIVE CONTROL (unmutated must pass), SENTINEL (a gutted apply_to must redden,
else HARNESS DEAD), and a MUTATION-APPLIED marker asserted in the staged file before it is graded.

Usage: python3 tools/mutate_pla8_catalog_suite.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SUITE = os.path.join(HERE, "test_promote_pla8_catalog_extension.py")
PROMOTE = os.path.join(HERE, "promote_pla8_catalog_extension.py")
CONTENT = os.path.join(HERE, "build_catalog_extension_content.py")
MARKER = "# MUTATION-APPLIED"

# (label, family, file, old, new)
MUTATIONS = [
    # ---- sourcing: the families no structural gate can see -------------------------------
    ("content: solarization anchored at the WRONG document", "sourcing", CONTENT,
     '"ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74145.html",',
     '"ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html",'),
    ("content: the nematode HEDGE dropped from cons", "sourcing", CONTENT,
     '"Less effective on nematodes than on fungi and weeds, because nematodes can move deeper "\n            "into the soil to escape the heat",',
     '"Highly effective on nematodes",'),
    ("content: reflective mulch loses its small-plant scope", "sourcing", CONTENT,
     "Use it while plants are small; it does less as the canopy closes over it.",
     "Use it all season for full protection of the planting."),
    ("content: a new source loses its document title (A54)", "sourcing", CONTENT,
     '"title": "Spider Mites / Home and Landscape / UC Statewide IPM Program (UC IPM)",', ""),
    ("content: a new source drops to T2", "sourcing", CONTENT,
     '"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html",\n        "source_class": "university_extension",\n        "trust_tier": "high",\n        "accessed": "2026-08",\n        "tier": "T1",',
     '"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html",\n        "source_class": "university_extension",\n        "trust_tier": "high",\n        "accessed": "2026-08",\n        "tier": "T2",'),
    # ---- scope ----------------------------------------------------------------------------
    ("content: a FOURTH method is appended", "scope", CONTENT,
     '# ---------------------------------------------------------------- applies_to corrections',
     '''NEW_METHODS["ghost_method"] = dict(NEW_METHODS["improve_drainage"])
# ---------------------------------------------------------------- applies_to corrections'''),
    ("content: a correction target is changed", "scope", CONTENT,
     '"handpick":          ("mollusk", "ucanr_ext_snails_slugs"),',
     '"handpick":          ("vertebrate", "ucanr_ext_snails_slugs"),'),
    ("content: the no-op horticultural_oil correction is reinstated", "scope", CONTENT,
     '    "even_watering":     ("mite", "ucanr_ext_spider_mites"),',
     '    "even_watering":     ("mite", "ucanr_ext_spider_mites"),\n    "horticultural_oil": ("mite", "ucanr_ext_spider_mites"),'),
    # ---- catalog shape --------------------------------------------------------------------
    ("content: a new method carries an invented tier", "shape", CONTENT,
     '"name": "Soil solarization",\n        "tier": "physical",',
     '"name": "Soil solarization",\n        "tier": "thermal",'),
    ("content: a new method loses a required key", "shape", CONTENT,
     '"best_use": (\n            "A bed with a known soil-borne problem, treated in the off season before replanting. "\n            "Most worthwhile where a nematode or root-rot history has already cost you a crop."\n        ),', ""),
    # ---- copy mechanics --------------------------------------------------------------------
    ("content: an em dash enters consumer copy", "mechanics", CONTENT,
     "costs almost nothing but it costs you the bed for a season.",
     "costs almost nothing — but it costs you the bed for a season."),
    ("content: a British spelling enters consumer copy", "mechanics", CONTENT,
     "Clear polyethylene sheeting from a hardware or garden store.",
     "Clear polyethylene sheeting from a hardware or garden centre."),
    ("content: registers collapse to near-verbatim", "mechanics", CONTENT,
     '"how_it_works_seasoned": (\n            "Transparent film, not black, laid over pre-moistened soil; wet soil conducts heat, so "',
     '"how_it_works_seasoned": (\n            "Cover damp, bare soil with clear plastic for four to six weeks in the hottest part of "'),
    # ---- promote logic ---------------------------------------------------------------------
    ("promote: a correction REPLACES the existing source", "blast", PROMOTE,
     'if src not in m["sources"]:\n            m["sources"].append(src)',
     'if True:\n            m["sources"] = [src]'),
    ("promote: the already-exists refusal is disabled", "refusal", PROMOTE,
     "if k in cm:\n            return f\"control_methods.{k} already exists; this promote creates it\"",
     "if False:\n            return \"\""),
    ("promote: the no-op-correction refusal is disabled", "refusal", PROMOTE,
     'if target in cm[k]["applies_to"]:', "if False:"),
    ("promote: output is no longer COMPACT", "mechanics", PROMOTE,
     'return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")',
     'return json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8")'),
    ("promote: a crop is touched as collateral", "blast", PROMOTE,
     '    data["source_catalog"].update(json.loads(json.dumps(new_sources)))',
     '    data["crops"][0]["name"] = "MUTATED"\n    data["source_catalog"].update(json.loads(json.dumps(new_sources)))'),
]

SENTINEL = ("SENTINEL: apply_to becomes a no-op", PROMOTE,
            "def apply_to(data):", "def apply_to(data):\n    return 0, 0")


def run(wd):
    r = subprocess.run([sys.executable, os.path.join(wd, os.path.basename(SUITE))],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout + r.stderr)[-300:]


def stage(path=None, old=None, new=None):
    wd = tempfile.mkdtemp(prefix="mutate_pla8cat_")
    # The staged suite must resolve shared helpers from the REAL tools dir while importing the
    # MUTATED module from this temp dir, so the path setup is rewritten explicitly.
    src = open(SUITE).read().replace(
        'REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
        'sys.path.insert(0, os.path.join(REPO, "tools"))',
        f'REPO = {REPO!r}\nsys.path.insert(0, os.path.join(REPO, "tools"))\n'
        f'sys.path.insert(0, {wd!r})')
    open(os.path.join(wd, os.path.basename(SUITE)), "w").write(src)
    for f in (PROMOTE, CONTENT):
        s = open(f).read()
        if path == f:
            if s.count(old) != 1:
                shutil.rmtree(wd)
                raise SystemExit(f"HARNESS DEAD: anchor not unique ({s.count(old)}x) in "
                                 f"{os.path.basename(f)}: {old[:70]!r}")
            s = s.replace(old, new + ("  " + MARKER if new else MARKER), 1)
        open(os.path.join(wd, os.path.basename(f)), "w").write(s)
    if path:
        back = open(os.path.join(wd, os.path.basename(path))).read()
        if MARKER not in back:
            shutil.rmtree(wd)
            raise SystemExit("HARNESS DEAD: MUTATION-APPLIED marker absent from the staged file")
    return wd


def main():
    print("=" * 78)
    print("MUTATION HARNESS -- PLA-8 catalog-extension promote suite")
    print("=" * 78)

    wd = stage(); ok, out = run(wd); shutil.rmtree(wd)
    if not ok:
        print("HARNESS DEAD: POSITIVE CONTROL fails.\n" + out); return 1
    print("positive control : GREEN\n")

    label, f, old, new = SENTINEL
    wd = stage(f, old, new); ok, _ = run(wd); shutil.rmtree(wd)
    if ok:
        print(f"HARNESS DEAD: {label} SURVIVED."); return 1
    print(f"sentinel         : RED as required ({label})\n")

    caught = survived = 0
    fam = {}
    for label, family, f, old, new in MUTATIONS:
        wd = stage(f, old, new); ok, out = run(wd); shutil.rmtree(wd)
        fam.setdefault(family, [0, 0])
        if ok:
            survived += 1; fam[family][1] += 1; print(f"  SURVIVED  [{family}] {label}")
        else:
            caught += 1; fam[family][0] += 1; print(f"  caught    [{family}] {label}")

    print("\n" + "-" * 78)
    for k in sorted(fam):
        c, s = fam[k]
        print(f"  {k:11s} {c} caught / {c + s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 78)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("\nRESULT: FAIL -- a guard family is unreachable or its test is vacuous."); return 1
    print("\nRESULT: PASS -- every guard family is reachable and every test is non-vacuous.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
