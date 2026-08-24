#!/usr/bin/env python3
"""PLA-8 catalog r2: mint off_season_tillage + certified_clean_stock, narrow prune_out_infection,
repoint the two artichoke rungs the narrowing would otherwise strand. Base 6b295d44.

Rationale, the source reads, and every edit: tools/build_pla8_catalog_r2_content.py

WHAT MOVES. `control_methods` 43 -> 45. `prune_out_infection` keeps its applies_to, its sources and
its fire-blight worked example; three of its strings change so it states the ACTION that defines it
(cut beyond the visible margin into clean tissue) and names `garden_sanitation` as the home of the
other action. On artichoke, one rung's METHOD KEY moves (curly-dwarf -> certified_clean_stock, prose
untouched) and one rung is DROPPED with its content merged into the garden_sanitation rung above it.

`garden_sanitation` IS DELIBERATELY NOT TOUCHED. Narrowing it away from in-season removal would
break ~14 of its 42 rungs on 7 already-certified crops. See the content module.

NO source is minted; both anchors for each mint were fetched and READ on 2026-08-24.

REFUSALS: base SHA mismatch; a mint that already exists; a missing/empty required field; a bad
tier; a source absent from source_catalog or not T1; anchoring_urls not matching sources; a
narrowing whose `old` text is not present EXACTLY; an artichoke rung that is not the expected
method at the expected index; a merge whose `old` text does not match; and a post-state in which
`prune_out_infection` is reachable from any rung other than the two that genuinely cut back into
clean tissue.

Guard suite:      tools/test_promote_pla8_catalog_r2.py
Mutation harness: tools/mutate_pla8_cr2_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_catalog_r2.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "6b295d440a8d4bfbad240c0cbf1bfdc83ccad1059c2d615ac8f9f5765e9d69ca"

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
REQ = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
       "best_use", "pros", "cons", "sources", "anchoring_urls")

# After this promote, exactly these rungs may name prune_out_infection. Both genuinely cut back
# beyond the margin into clean tissue; everything else that used the key did not.
PRUNE_SURVIVORS = {("apple", "fire-blight"), ("artichoke", "botrytis-gray-mold")}


def content():
    import build_pla8_catalog_r2_content as B
    return B


def _crop(data, slug):
    for c in data["crops"]:
        if c.get("slug") == slug:
            return c
    return None


def _problem(data, slug, pid):
    c = _crop(data, slug)
    if c is None:
        return None
    for fam in ("pests", "diseases"):
        for p in c.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    return None


def prune_sites(data):
    """Every (slug, problem id) whose ladder names prune_out_infection."""
    out = set()
    for c in data["crops"]:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                for r in p.get("control_ladder") or []:
                    if r.get("method") == "prune_out_infection":
                        out.add((c.get("slug"), p.get("id")))
    return out


def check(data):
    B = content()
    cm, sc = data["control_methods"], data["source_catalog"]

    for k, m in B.NEW_METHODS.items():
        if k in cm:
            return f"control_methods.{k} already exists; this promote creates it"
        if m["tier"] not in TIERS:
            return f"{k}: bad tier {m['tier']!r}"
        for f in REQ:
            if not m.get(f):
                return f"{k}: missing/empty {f!r}"
        for s in m["sources"]:
            if s not in sc:
                return f"{k}: source {s!r} not in source_catalog"
            if sc[s].get("tier") != "T1":
                return f"{k}: source {s!r} is not T1"
        if set(m["anchoring_urls"]) != set(m["sources"]):
            return f"{k}: anchoring_urls keys do not match sources"

    key = B.NARROW["key"]
    if key not in cm:
        return f"{key} missing; nothing to narrow"
    for field in ("best_use", "how_it_works_beginner", "how_it_works_seasoned"):
        old = B.NARROW[field]["old"]
        if old not in cm[key][field]:
            return f"{key}.{field}: expected text not present; already narrowed, or it changed"

    for e in B.ARTICHOKE:
        p = _problem(data, "artichoke", e["id"])
        if p is None:
            return f"artichoke/{e['id']} not found"
        lad = p.get("control_ladder") or []
        if e["rung"] >= len(lad):
            return f"artichoke/{e['id']}: no rung at index {e['rung']}"
        if lad[e["rung"]].get("method") != e["from"]:
            return (f"artichoke/{e['id']} rung {e['rung']}: expected {e['from']!r}, "
                    f"found {lad[e['rung']].get('method')!r}")
        if e["to"] is not None and e["to"] not in B.NEW_METHODS and e["to"] not in cm:
            return f"artichoke/{e['id']}: target method {e['to']!r} will not exist"

    m = B.ARTICHOKE_MERGE
    p = _problem(data, "artichoke", m["id"])
    if p is None:
        return f"artichoke/{m['id']} not found for merge"
    if (p["control_ladder"][m["rung"]].get(m["field"]) or "") != m["old"]:
        return f"artichoke/{m['id']} rung {m['rung']}.{m['field']}: text does not match exactly"

    unexpected = prune_sites(data) - PRUNE_SURVIVORS - {("artichoke", e["id"]) for e in B.ARTICHOKE}
    if unexpected:
        return f"prune_out_infection is used at unexpected sites, review before narrowing: {sorted(unexpected)}"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    B = content()
    cm = data["control_methods"]
    cm.update(json.loads(json.dumps(B.NEW_METHODS)))

    key = B.NARROW["key"]
    for field in ("best_use", "how_it_works_beginner", "how_it_works_seasoned"):
        spec = B.NARROW[field]
        cm[key][field] = cm[key][field].replace(spec["old"], spec["new"], 1)

    m = B.ARTICHOKE_MERGE
    p = _problem(data, "artichoke", m["id"])
    p["control_ladder"][m["rung"]][m["field"]] = m["new"]

    # descending index so a drop cannot shift a later target
    for e in sorted(B.ARTICHOKE, key=lambda x: -x["rung"]):
        p = _problem(data, "artichoke", e["id"])
        lad = p["control_ladder"]
        if e["to"] is None:
            lad.pop(e["rung"])
        else:
            lad[e["rung"]]["method"] = e["to"]
    return len(B.NEW_METHODS)


def verify_post(data):
    B = content()
    cm = data["control_methods"]
    for k in B.NEW_METHODS:
        if k not in cm:
            return f"{k} did not land"
    key = B.NARROW["key"]
    if "garden sanitation" not in cm[key]["best_use"].lower():
        return f"{key}.best_use does not name garden sanitation, so the two are not disambiguated"
    if "clean tissue" not in cm[key]["best_use"].lower():
        return f"{key}.best_use does not state the defining action"
    left = prune_sites(data)
    if left != PRUNE_SURVIVORS:
        return f"prune_out_infection rung set is {sorted(left)}, expected {sorted(PRUNE_SURVIVORS)}"
    # the mints must not claim each other's action
    if "till" in cm["certified_clean_stock"]["how_it_works_beginner"].lower():
        return "certified_clean_stock strays into tillage"
    if "seed" in cm["off_season_tillage"]["best_use"].lower():
        return "off_season_tillage strays into planting stock"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != a.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr)
        return 1
    data = json.loads(raw.decode("utf-8"))

    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    before = len(data["control_methods"])
    n = apply_to(data)

    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 catalog r2 -- two mints, one narrowing, the artichoke repoint")
    print(f"  control_methods {before} -> {len(data['control_methods'])}  (+{n})")
    print(f"  narrowed        prune_out_infection (3 strings; applies_to and sources unchanged)")
    print(f"  artichoke       curly-dwarf rung 1 -> certified_clean_stock; "
          f"bacterial-crown-rot rung 1 DROPPED, content merged into rung 0")
    print(f"  prune_out_infection now reachable from: {sorted(prune_sites(data))}")
    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
