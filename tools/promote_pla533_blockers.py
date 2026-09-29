#!/usr/bin/env python3
"""promote_pla533_blockers -- PLA-533 2a, seven blocking findings. Base 83384c85.

WHAT MOVES. Three crops, and within each only two things:
  1. verification_status.open_findings gains the spec's findings, APPENDED after the existing ones.
  2. verification_status.launch_ready_core and launch_ready_seasoned go True -> False.
Nothing else. verification_status.status does NOT move (PLA-466: a blocker drives the flags, never
the status, because status is the page gate). No value is edited, nulled or deleted here.

THE SEVEN (Trevor ruling 1, 2026-09-25; spec: tools/staging/pla533_blockers/spec.json):
  orange-navel         sulfur acidification, navel juice freezing, "best pot tree", 100-200+ lb yield
  grapefruit           mulched basin, sulfur acidification
  mandarin-clementine  sulfur acidification
HELD, and refused if they appear: orange-navel mulch (PLA-610 is a lead and orange-navel is already
blocked) and mandarin NPK 2-1-1 (drafted only; the re-author settles it).

Each finding quotes the dataset strings it covers and the T1 sentence that contradicts them. Each
carries the CLOSE CONDITION: only a clause-checked re-author resolves it; removing a citation never
does. Launch-ready moves 117 -> 114; certified stays 121.

WHY EACH GUARD EXISTS.
 1. PINNED BASE. The canonical bytes must hash to BASE_SHA, or nothing is written.
 2. PINNED PRE-STATE. Each target crop must be launch-ready on both flags, carry no live blocker, and
    still contain every dataset string its findings quote. A finding that quotes a string no longer
    there would record a defect that does not exist (the finding-21 lesson).
 3. EVIDENCE BY DIGEST. Every basis quote must occur in the cached bytes of the page it names, and
    that file must hash to its name. A quote the page does not carry is refused.
 4. SPEC SHAPE. Exactly 7, all blocks_launch true and status open, all carrying the close condition,
    only the three crops, never a HELD id, no id already present anywhere in the dataset.
 5. SET BEFORE VALUE. set(pre crops) == set(post crops) and the order is unchanged BEFORE anything is
    compared -- iterating pre alone makes a crop added in post invisible (PLA-162).
 6. BLAST RADIUS. Every other crop and every top-level key is byte-equal; inside a target crop only
    the two declared keys of verification_status differ.

Usage:
    promote_pla533_blockers.py --check                 # apply in memory, run every guard
    promote_pla533_blockers.py --out /path/scratch.json
    promote_pla533_blockers.py --expect-sha <sha>      # writes canonical, on approval
"""
import argparse
import copy
import hashlib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
SPEC = os.path.join(HERE, "staging", "pla533_blockers", "spec.json")
CACHE = os.path.join(HERE, ".evidence_cache")

BASE_SHA = "83384c85d9daccc71b3d4a0da795872a761538b0e4d8e94b0d401a674a8a6cd6"
CROPS = ("orange-navel", "grapefruit", "mandarin-clementine")
EXPECTED_FINDINGS = 7
HELD_IDS = ("orange_navel_mulched_basin_contradicted_pla533",
            "mandarin_clementine_npk_2_1_1_cites_hs132_pla533")
CLOSE_MARKERS = ("resolves ONLY when the named fields are re-authored",
                 "Removing, emptying or repointing a citation NEVER resolves it")
FLAGS = ("launch_ready_core", "launch_ready_seasoned")
DECLARED_VS_KEYS = ("open_findings",) + FLAGS


def refuse(msg):
    raise SystemExit(f"REFUSED: {msg}")


def staged(path=None):
    with open(path or SPEC, encoding="utf-8") as f:
        return json.load(f)


def check_base_sha(raw):
    got = hashlib.sha256(raw).hexdigest()
    if got != BASE_SHA:
        refuse(f"base sha mismatch: {got[:16]} != {BASE_SHA[:16]}")


def _page_text(sha):
    path = os.path.join(CACHE, f"{sha}.html")
    if not os.path.exists(path):
        refuse(f"evidence file {sha[:12]} missing from {CACHE}")
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest() != sha:
        refuse(f"evidence file {sha[:12]} does not hash to its name")
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def check_evidence(spec):
    for x in spec["findings"]:
        for sha, quote in x["evidence"]:
            if re.sub(r"\s+", " ", quote) not in _page_text(sha):
                refuse(f"{x['finding']['id']}: evidence quote not in cached bytes {sha[:12]}: {quote[:60]!r}")


def check_spec(spec):
    fs = spec["findings"]
    if len(fs) != EXPECTED_FINDINGS:
        refuse(f"expected {EXPECTED_FINDINGS} findings, spec carries {len(fs)}")
    for x in fs:
        f = x["finding"]
        if f.get("id") in HELD_IDS:
            refuse(f"{f.get('id')} is HELD by ruling and may not land")
        if x["crop"] not in CROPS:
            refuse(f"crop set: {x['crop']} is not one of {CROPS}")
        if f.get("blocks_launch") is not True or f.get("status") != "open":
            refuse(f"{f['id']} must block launch and be open")
        if not all(m in f.get("summary", "") for m in CLOSE_MARKERS):
            refuse(f"{f['id']} lacks the close condition")
    ids = [x["finding"]["id"] for x in fs]
    if len(set(ids)) != len(ids):
        refuse("duplicate finding id in spec")


def _at(crop, pointer):
    node = crop
    for part in pointer.strip("/").split("/"):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def apply_to(data, spec):
    check_spec(spec)
    bycrop = {c["slug"]: c for c in data["crops"]}
    existing = {f.get("id") for c in data["crops"]
                for f in c.get("verification_status", {}).get("open_findings", []) if isinstance(f, dict)}
    for x in spec["findings"]:
        if x["finding"]["id"] in existing:
            refuse(f"finding id already exists in the dataset: {x['finding']['id']}")
    for slug in CROPS:
        vs = bycrop[slug]["verification_status"]
        if any(vs.get(k) is not True for k in FLAGS):
            refuse(f"{slug}: launch_ready pre-state is not True on both flags")
        live = [f for f in vs.get("open_findings", [])
                if isinstance(f, dict) and f.get("blocks_launch") and f.get("status") != "resolved"]
        if live:
            refuse(f"{slug} already carries a live blocking finding")
    for x in spec["findings"]:
        crop = bycrop[x["crop"]]
        for pointer, fragment in x["field_quotes"]:
            try:
                val = _at(crop, pointer)
            except (KeyError, IndexError, TypeError):
                val = None
            if not isinstance(val, str) or fragment not in val:
                refuse(f"{x['finding']['id']}: quoted string not found at {x['crop']}{pointer}: {fragment!r}")
    for x in spec["findings"]:
        bycrop[x["crop"]]["verification_status"]["open_findings"].append(copy.deepcopy(x["finding"]))
    for slug in CROPS:
        for k in FLAGS:
            bycrop[slug]["verification_status"][k] = False
    return data


def check_post(pre, post, spec):
    P = [c["slug"] for c in pre["crops"]]
    Q = [c["slug"] for c in post["crops"]]
    if set(P) != set(Q) or P != Q:
        refuse("crop set changed between pre and post")
    if set(pre) != set(post):
        refuse("top-level key set changed")
    for k in pre:
        if k != "crops" and pre[k] != post[k]:
            refuse(f"top-level key {k} changed")
    for a, b in zip(pre["crops"], post["crops"]):
        slug = a["slug"]
        if slug not in CROPS:
            if a != b:
                refuse(f"collateral change on {slug}")
            continue
        if set(a) != set(b):
            refuse(f"{slug}: key set changed")
        for k in a:
            if k != "verification_status" and a[k] != b[k]:
                refuse(f"{slug}.{k} changed, outside the declared keys")
        va, vb = a["verification_status"], b["verification_status"]
        if set(va) != set(vb):
            refuse(f"{slug}: verification_status key set changed")
        for k in va:
            if k not in DECLARED_VS_KEYS and va[k] != vb[k]:
                refuse(f"{slug}.verification_status.{k} changed, outside the declared keys")
        if any(vb[k] is not False for k in FLAGS):
            refuse(f"{slug}: launch flags must both be false after the promote")
        want = [x["finding"] for x in spec["findings"] if x["crop"] == slug]
        if vb["open_findings"] != va["open_findings"] + want:
            refuse(f"{slug}: open_findings is not exactly the pre list plus the spec's findings")


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--out")
    g.add_argument("--expect-sha")
    args = ap.parse_args()
    raw = open(CANON, "rb").read()
    check_base_sha(raw)
    spec = staged()
    check_evidence(spec)
    pre = json.loads(raw)
    post = apply_to(copy.deepcopy(pre), spec)
    check_post(pre, post, spec)
    out = serialize(post)
    sha = hashlib.sha256(out).hexdigest()
    print(f"promote_pla533_blockers: {EXPECTED_FINDINGS} findings on {len(CROPS)} crops; post sha {sha}")
    if args.check:
        return
    if args.out:
        with open(args.out, "wb") as f:
            f.write(out)
        print(f"wrote {args.out}")
        return
    if sha != args.expect_sha:
        refuse(f"post sha {sha} != --expect-sha {args.expect_sha}")
    with open(CANON, "wb") as f:
        f.write(out)
    print(f"wrote {CANON}")


if __name__ == "__main__":
    main()
