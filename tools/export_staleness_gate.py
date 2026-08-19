#!/usr/bin/env python3
"""export_staleness_gate -- does every downstream surface serve the CURRENT canonical? (PLA-258)

WHAT THIS EXISTS TO CATCH, precisely. On 2026-08-19 the shipped app bundle
(`assets/data/guides.dataset`) was a byte-exact projection of canonical `b0d01f13`
(dataset commit `8a5398a`, 2026-07-29), and plant-astro's submodule was pinned to that
same commit. Canonical was `3bf8b4ce`. Three content promotes -- PLA-155/199 catalog work,
PLA-202's 22 verbatim rewrites, PLA-253's Bt safety rewrite -- were live in canonical and
absent from BOTH consumer surfaces, for three weeks, silently.

THE REASON NOTHING COULD REPORT IT: the export was FAITHFUL. Every byte of it was a correct
projection of the canonical it was built from. No value check, no schema check, no diff
against the app's own expectations could ever have found the defect, because the artifact
was not corrupt -- it was OLD. Staleness is a property of PROVENANCE, and provenance was
not recorded anywhere. `build-guides-data.mjs` wrote the bytes and forgot where they came
from.

So the gate's first requirement is a stamp (`assets/data/dataset-provenance.json`, written
by the build script), and its second is to never trust the stamp alone.

  E1 APP-PROVENANCE  the app's manifest records a canonical SHA, and it is the current one.
  E2 APP-INTEGRITY   every artifact still hashes to what the manifest recorded, and the
                     manifest's artifact key set is EXACTLY the known build outputs.
  E3 ASTRO-PIN       plant-astro's recorded submodule pin resolves, in this repo's history,
                     to a commit whose crops_data_final.json IS the current canonical.

E2's key-set equality is not decoration. `build-guides-data.mjs` emits FOUR artifacts, and
the three besides `guides.dataset` are built from TOP-LEVEL dataset keys, not from crops:
`control-methods.json` comes from `control_methods` + `source_catalog`. PLA-253 changed
`control_methods.bt` and PLA-199 changed `source_catalog` titles -- neither of which alters
`guides.dataset` by a single byte. A gate that watched only the big file would have called
both promotes shipped. Iterating only what the manifest RECORDS repeats PLA-162's defect at
a new boundary, so the sets are compared before any hash is.

WHY E3 IS IN THE SAME GATE AND NOT A SEPARATE ONE. Wiring app regeneration without wiring
the site pin moves the gap one step down the pipeline: the export becomes current and the
website still serves the old canonical, because astro reads `plant-dataset/crops_data_final
.json` from the submodule at build time (`src/lib/dataset.ts`) and Netlify checks out the
PINNED commit. One canonical, two consumers, one question -- so one gate.

UNMEASURED IS NOT GREEN. If a consumer repo is not on this disk, the gate says so in its
own channel rather than returning a clean zero over a surface it never opened. That is the
distinction this arc has paid for repeatedly (`docs/` PLA-160, PLA-138): an instrument that
cannot justify its zero is worse than no instrument, because the zero gets believed.

Usage:
  export_staleness_gate.py [--canonical PATH] [--app-root PATH] [--astro-root PATH] [--json]
Exit 0 clean, 1 stale/unmeasured.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

DEFAULT_CANONICAL = os.path.join(REPO, "crops_data_final.json")
DEFAULT_APP_ROOT = os.path.join(os.path.expanduser("~"), "plant-app")
DEFAULT_ASTRO_ROOT = os.path.join(os.path.expanduser("~"), "plant-astro")

# The provenance stamp the app's build script writes, relative to the app root.
APP_PROVENANCE = os.path.join("assets", "data", "dataset-provenance.json")

# Every artifact `scripts/build-guides-data.mjs` generates from the canonical. Adding an
# output to that script without adding it here is a DELIBERATE act that fails this gate
# until both sides agree -- which is the point. The export boundary grows on purpose or
# not at all.
APP_ARTIFACTS = (
    os.path.join("assets", "data", "guides.dataset"),
    os.path.join("src", "data", "region-chill.json"),
    os.path.join("src", "data", "variety-index.json"),
    os.path.join("src", "data", "control-methods.json"),
)

# The submodule path inside plant-astro that carries this repo.
ASTRO_SUBMODULE_PATH = "plant-dataset"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(path=None):
    return sha256_file(path or DEFAULT_CANONICAL)


def _git(repo, *args):
    """stdout of a git command, or None if it failed. Never raises: a gate that dies on a
    detached HEAD or a missing repo teaches people to skip it."""
    try:
        r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    except OSError:
        return None
    return r.stdout.decode("utf-8", "replace").strip() if r.returncode == 0 else None


# ---------------------------------------------------------------- E1 + E2 (the app)

def app_violations(app_root, canonical_sha):
    """(violations, unmeasured). E1 provenance, E2 integrity."""
    if not os.path.isdir(app_root):
        return [], [f"UNMEASURED app: no repo at {app_root} -- export currency NOT checked"]

    mpath = os.path.join(app_root, APP_PROVENANCE)
    if not os.path.exists(mpath):
        return ([f"E1 app-provenance: no provenance stamp at {APP_PROVENANCE}. The export "
                 f"cannot say which canonical it was built from, so it cannot be shown "
                 f"current. Run `npm run build:guides` in {app_root}."], [])
    try:
        with open(mpath) as f:
            manifest = json.load(f)
        if not isinstance(manifest, dict):
            raise ValueError("provenance stamp is not an object")
    except (ValueError, OSError) as e:
        return [f"E1 app-provenance: {APP_PROVENANCE} is unreadable ({e}). Treated as "
                f"absent, never as current."], []

    V = []
    stamped = manifest.get("canonical_sha256")
    if not stamped or not isinstance(stamped, str):
        V.append(f"E1 app-provenance: stamp carries no canonical_sha256 "
                 f"(got {stamped!r}); provenance unproven.")
    elif stamped != canonical_sha:
        V.append(f"E1 app-provenance: export was built from canonical {stamped[:12]} but "
                 f"canonical is now {canonical_sha[:12]}. The shipped artifact is STALE -- "
                 f"run `npm run build:guides` in {app_root}.")

    # E2. Key sets FIRST -- comparing only the keys the manifest happens to list makes a
    # newly emitted artifact invisible (PLA-162's defect, at the export boundary).
    recorded = manifest.get("artifacts")
    if not isinstance(recorded, dict):
        V.append(f"E2 app-integrity: stamp carries no artifacts map (got {type(recorded).__name__}).")
        return V, []

    expected = set(APP_ARTIFACTS)
    got = set(recorded)
    for missing in sorted(expected - got):
        V.append(f"E2 app-integrity: build output {missing} is generated but NOT stamped. "
                 f"An unstamped artifact can go stale invisibly.")
    for extra in sorted(got - expected):
        V.append(f"E2 app-integrity: stamp records {extra}, which is not a known build "
                 f"output. Add it to APP_ARTIFACTS deliberately or stop stamping it.")

    for rel in sorted(expected & got):
        full = os.path.join(app_root, rel)
        if not os.path.exists(full):
            V.append(f"E2 app-integrity: stamped artifact {rel} is missing from disk.")
            continue
        actual = sha256_file(full)
        if actual != recorded[rel]:
            V.append(f"E2 app-integrity: {rel} hashes {actual[:12]} but the stamp recorded "
                     f"{str(recorded[rel])[:12]}. It was changed after the build, so the "
                     f"provenance stamp no longer describes it.")
    return V, []


# ---------------------------------------------------------------- E3 (the website)

def astro_violations(astro_root, dataset_root, canonical_sha):
    """(violations, unmeasured). The pin Netlify actually builds is the one RECORDED in
    astro's HEAD tree, not whatever happens to be checked out in the local worktree."""
    if not os.path.isdir(astro_root):
        return [], [f"UNMEASURED astro: no repo at {astro_root} -- site currency NOT checked"]

    entry = _git(astro_root, "ls-tree", "HEAD", ASTRO_SUBMODULE_PATH)
    if not entry:
        return [f"E3 astro-pin: plant-astro HEAD records no `{ASTRO_SUBMODULE_PATH}` entry. "
                f"The site's dataset source cannot be identified."], []
    parts = entry.split()
    if len(parts) < 3 or parts[0] != "160000":
        return [f"E3 astro-pin: `{ASTRO_SUBMODULE_PATH}` in plant-astro HEAD is not a "
                f"submodule gitlink (mode {parts[0] if parts else '?'})."], []
    pinned = parts[2]

    blob = None
    try:
        r = subprocess.run(["git", "-C", dataset_root, "show", f"{pinned}:crops_data_final.json"],
                           capture_output=True)
        if r.returncode == 0:
            blob = r.stdout
    except OSError:
        blob = None

    if blob is None:
        return [f"E3 astro-pin: plant-astro pins dataset commit {pinned[:12]}, which this "
                f"repo cannot resolve (unpushed, rewritten, or unfetched). An unverifiable "
                f"pin is not a current pin."], []

    pinned_sha = sha256_bytes(blob)
    if pinned_sha != canonical_sha:
        desc = _git(dataset_root, "log", "-1", "--format=%h %ad %s", "--date=short", pinned) or pinned[:12]
        return [f"E3 astro-pin: the site builds from dataset commit {desc}, whose canonical "
                f"is {pinned_sha[:12]}; canonical is now {canonical_sha[:12]}. The website "
                f"serves STALE content until the submodule is bumped in plant-astro."], []
    return [], []


# ---------------------------------------------------------------- report

def report(canonical_path=None, app_root=None, astro_root=None, dataset_root=None):
    canonical_path = canonical_path or DEFAULT_CANONICAL
    app_root = app_root or DEFAULT_APP_ROOT
    astro_root = astro_root or DEFAULT_ASTRO_ROOT
    dataset_root = dataset_root or REPO

    canonical_sha = canonical_sha256(canonical_path)
    av, au = app_violations(app_root, canonical_sha)
    sv, su = astro_violations(astro_root, dataset_root, canonical_sha)
    return {
        "canonical_sha256": canonical_sha,
        "violations": av + sv,
        "unmeasured": au + su,
    }


def all_violations(canonical_path=None, app_root=None, astro_root=None, dataset_root=None):
    """Violations AND unmeasured, in one list, for callers that must not pass either.

    They stay separable via `report()`; they are combined here because for a RELEASE the
    two have the same consequence -- you cannot assert the surfaces are current."""
    r = report(canonical_path, app_root, astro_root, dataset_root)
    return r["violations"] + r["unmeasured"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--canonical", default=DEFAULT_CANONICAL,
                    help="canonical to measure against (default: this repo's working tree)")
    ap.add_argument("--app-root", default=DEFAULT_APP_ROOT)
    ap.add_argument("--astro-root", default=DEFAULT_ASTRO_ROOT)
    ap.add_argument("--dataset-root", default=REPO)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = report(a.canonical, a.app_root, a.astro_root, a.dataset_root)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"canonical: {r['canonical_sha256'][:12]}")
        for v in r["violations"]:
            print("VIOLATION:", v)
        for u in r["unmeasured"]:
            print("UNMEASURED:", u)
        print(f"export_staleness_gate: {len(r['violations'])} violation(s), "
              f"{len(r['unmeasured'])} unmeasured")
    sys.exit(1 if (r["violations"] or r["unmeasured"]) else 0)


if __name__ == "__main__":
    main()
