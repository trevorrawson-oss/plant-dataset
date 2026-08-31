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
  status   how far the rollout has got, and the family cut to batch by
  families the family cut on its own: which remaining crops SHARE PROSE

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
    cmd_families(a, todo=todo)


# ---------------------------------------------------------------- families
def problem_name(p):
    """A problem's name under EITHER schema.

    113 certified crops carry `name`; the 8 microgreens crops carry `name_beginner`/`name_seasoned`
    and no `name` at all. The first version of this grouping read only `name`, so all 8 returned
    None, collided on a signature of empties, and were reported as one 'twin group' -- a real
    grouping arrived at for a bogus reason. Read both shapes.
    """
    return p.get("name") or p.get("name_seasoned") or p.get("name_beginner")


def prose_key(p):
    """Identity of a problem's SOURCED PROSE. Two crops sharing this share the read.

    THREE schemas now: the classic crops carry `organic_treatment_*`/`prevention_*`, the
    microgreens carry `management_*`/`description_*`, and the 10 Companion & Pollinator crops
    carry `note_beginner`/`note_seasoned` ONLY. Reading only the classic pair silently EXCLUDED
    the microgreens once; before the note fallback the companions reduced to (name, None, None)
    and same-named problems on different companion crops collided as FALSE TWINS (measured
    2026-08-30 ahead of batch 15).
    """
    return (problem_name(p),
            p.get("organic_treatment_beginner") or p.get("management_beginner")
            or p.get("note_beginner"),
            p.get("prevention_beginner") or p.get("description_beginner")
            or p.get("note_seasoned"))


# The fields a rung is RESTATED FROM, under either schema (classic crops carry
# `organic_treatment_*`/`prevention_*`; the 8 microgreens carry `management_*`/`description_*`).
# `anchoring_urls` and `sources` are deliberately NOT here: they are provenance, and a divergence
# there is a sourcing defect to log, not a reason to refuse a propagation.
PROSE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "management_beginner", "management_seasoned",
                "description_beginner", "description_seasoned",
                "note_beginner", "note_seasoned")

_ABSENT = "\x00absent"   # distinct from an explicit null, which is distinct from ""
_NULL = "\x00null"


def prose_signature(crop):
    """Identity of a crop's ENTIRE sourced problem set, IN ORDER.

    WHAT THIS REPLACED, and why it mattered. The signature here used to be
    `tuple(sorted(problem_name(p) for ...))` -- problem NAMES ONLY, not one character of prose. Any
    two crops naming the same problems grouped as a "twin group", and the printed advice told the
    session that identical prose meant it could author one crop and propagate the ladders
    mechanically onto the siblings.

    Measured against canonical `c13ddea5`, NOT ONE of the ten reported groups was a true twin:
    collards/kale 28.7% of fields identical, beefsteak/cherry-tomato 55.4%, the three cucumbers
    72.7%. The corns of batch 2 measured 96.2% with all twelve differences on a single problem, so
    that shipped propagation was sound -- which is the trap. The group was picked for a reason that
    had nothing to do with prose and came out right anyway, so the method read as proven.

    Applied to the cucumbers the same propagation was a content defect in both directions:
    pickling-cucumber's prose names wilt-tolerant County Fair and CMV-resistant varieties, where
    cucumber's and slicing-cucumber's name non-bitter varieties and assert no resistance at all.
    Copy either way and you erase a sourced control or invent one.

    ORDER IS PART OF THE IDENTITY, deliberately. Propagation is index-wise (see
    `promote_pla8_batch2.py`), so two crops carrying the same problems in a different order are NOT
    propagate-safe even though their prose SETS match. Sorting here would report them as twins and
    hand the next session an index-shifted copy. Grouping for cheap READING is a weaker claim and is
    measured separately, by `prose_key` below.
    """
    sig = []
    for _f, p in problems(crop):
        # every name field explicitly, NOT problem_name()'s fallback chain: that chain returns the
        # first of name/name_seasoned/name_beginner that is set, so two crops whose `name_beginner`
        # differs while `name_seasoned` matches would be declared TRUE TWINS and propagated across.
        row = [(problem_name(p) or "?").lower()]
        for k in ("name", "name_beginner", "name_seasoned"):
            v = p.get(k, _ABSENT)
            row.append(_NULL if v is None else v)
        for k in PROSE_FIELDS:
            v = p.get(k, _ABSENT)
            if v is None:
                v = _NULL
            row.append(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True))
        sig.append(tuple(row))
    return tuple(sig)


def family_cut(todo):
    """Split crops into TRUE twin groups (byte-identical problem prose) and singletons.

    Returns (twins, singles): twins is a list of slug-lists, longest first; singles a list of slugs.
    """
    import collections
    groups = collections.defaultdict(list)
    for c in todo:
        groups[prose_signature(c)].append(c["slug"])
    twins = sorted((v for v in groups.values() if len(v) > 1), key=len, reverse=True)
    singles = sorted(v[0] for v in groups.values() if len(v) == 1)
    return twins, singles


def cross_sibling_conflicts(src, out):
    """Siblings whose SOURCE PROSE agrees but whose authored LADDERS do not.

    `src`: {slug: [problem_dict, ...]} -- the crops' existing sourced prose, in order.
    `out`: {slug: [[method, ...], ...]} -- the authored ladder method sequences, same order.
    Returns a list of read rows, most-shared-prose first. It REPORTS; it never refuses.

    WHY. Batch 3's one real defect was cucumber and slicing-cucumber carrying byte-identical
    `prevention_seasoned` on Cucumber beetles while one keyed it to `resistant_varieties` and the
    other refused. Same input, different output. Every gate passed both ladders, because each is
    independently valid; the defect is only visible ACROSS crops, and only exists because family
    batches author siblings separately. It was caught by a hand-built side-by-side, which does not
    scale across the ~34 batches left.

    THE SIGNAL IS IDENTICAL INPUT WITH DIFFERENT OUTPUT, and the threshold is deliberately ONE
    shared field, not all of them. On the real case `prevention_seasoned` matched while both
    `organic_treatment_*` fields differed, so requiring full agreement would have missed it.

    A REPORTED ROW IS NOT A DEFECT. pickling-cucumber correctly carries `resistant_varieties` on
    bacterial-wilt where its siblings do not: its prose claims wilt TOLERANCE and theirs claim only
    reduced beetle attraction. The row exists so that divergence gets ADJUDICATED rather than
    happening silently, and the evidence travels with it.
    """
    rows = []
    slugs = sorted(src)
    for i, a in enumerate(slugs):
        for b in slugs[i + 1:]:
            pa, pb = src[a], src[b]
            la, lb_ = out.get(a) or [], out.get(b) or []
            for idx in range(min(len(pa), len(pb))):
                x, y = pa[idx], pb[idx]
                if problem_name(x) != problem_name(y):
                    continue
                same, diff = [], []
                for k in PROSE_FIELDS:
                    if k not in x and k not in y:
                        continue
                    (same if x.get(k) == y.get(k) else diff).append(k)
                if not same:
                    continue          # nothing shared: a different ladder is expected, not a signal
                ma = la[idx] if idx < len(la) else []
                mb = lb_[idx] if idx < len(lb_) else []
                if ma == mb:
                    continue
                rows.append({
                    "a": a, "b": b, "index": idx, "problem": problem_name(x),
                    "only_in_a": sorted(set(ma) - set(mb)),
                    "only_in_b": sorted(set(mb) - set(ma)),
                    "identical_fields": same,
                    "differing_fields": diff,
                    "ladder_a": ma, "ladder_b": mb,
                })
    rows.sort(key=lambda r: (-len(r["identical_fields"]), r["a"], r["b"], r["index"]))
    return rows


def cmd_families(a, todo=None):
    """Group the remaining crops by SHARED PROSE, because that is what makes a batch cheap.

    WHY THIS REPLACED 'fewest problems first'. That ordering optimised batch SIZE and destroyed
    batch COHERENCE: it is what produced batch 1 as heirloom-tomato + jalapeno + swiss-chard +
    basil + fig -- five unrelated crops, 38 problems, and ZERO shared prose, so five separate
    source sets had to be read from scratch.

    WHY IT NOW REPORTS TWO DIFFERENT THINGS. The first version grouped on problem NAMES and printed
    one verdict, "twin group", carrying one instruction: propagate the ladders mechanically. Those
    are two separate claims and only the weaker one was ever true.

      SHARED-NAME FAMILY -- the same problems by name. Makes the READ cheap, because the sourcing
      overlaps and the siblings can be compared side by side. Says NOTHING about propagation.
      TRUE TWIN -- byte-identical problem prose, in order. THIS is the group where one crop can be
      authored and the ladders copied, because every rung restates prose the sibling also carries.

    See `prose_signature` for the measurement that separated them, and what the conflation would
    have cost on the cucumbers.
    """
    import collections
    if todo is None:
        d = load()
        cert = [c for c in d["crops"]
                if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
        todo = [c for c in cert if not laddered(c)]

    by = {c["slug"]: c for c in todo}
    twins, _singles = family_cut(todo)
    twinned = {s for g in twins for s in g}

    # the weaker, read-cheapness grouping: same problem names, prose not necessarily identical
    named = collections.defaultdict(list)
    for c in todo:
        named[tuple(sorted((problem_name(p) or "?").lower() for _f, p in problems(c)))].append(c["slug"])
    families = sorted((v for v in named.values() if len(v) > 1), key=len, reverse=True)
    in_family = {s for g in families for s in g}
    singles = sorted(s for s in by if s not in in_family)

    # how much prose is shared, so the payoff is stated rather than asserted
    shared = collections.defaultdict(list)
    for c in todo:
        for _f, p in problems(c):
            k = prose_key(p)
            if all(k):
                shared[k].append(c["slug"])
    dupes = sum(len(v) for v in shared.values() if len(v) > 1)
    total = sum(len(problems(c)) for c in todo)

    def identity(group):
        """Fraction of problem fields byte-identical across a group, against its first member."""
        g = sorted(group)
        base = by[g[0]]
        tot = ide = 0
        for other in g[1:]:
            o = by[other]
            for f in ("pests", "diseases"):
                for i, p in enumerate(base.get(f) or []):
                    arr = o.get(f) or []
                    q = arr[i] if i < len(arr) else {}
                    for k in PROSE_FIELDS:
                        if k in p or k in q:
                            tot += 1
                            ide += (p.get(k) == q.get(k))
        return 100.0 * ide / max(tot, 1)

    print("BATCH BY FAMILY -- crops that SHARE PROSE share the read.")
    print(f"  {dupes} of {total} problem-instances ({100*dupes//max(total,1)}%) are byte-identical "
          f"to a problem on another remaining crop.")
    print(f"  distinct problems left to READ: ~{len(shared)}, against {total} instances.\n")

    print(f"TRUE TWINS ({len(twins)} groups, {sum(len(v) for v in twins)} crops) -- byte-identical "
          f"prose. ONE authoring pass, propagate mechanically, and make the promote ASSERT it:")
    if not twins:
        print("  (none on the current roster)")
    for v in twins:
        n = len(problems(by[v[0]]))
        print(f"  {len(v)}x  {n:2d} problems each   {', '.join(sorted(v))}")

    partial = [g for g in families if not set(g) <= twinned]
    print(f"\nSHARED-NAME FAMILIES ({len(partial)} groups, {sum(len(g) for g in partial)} crops) -- "
          f"same problems, DIFFERENT prose. The read is cheap because sourcing overlaps and the")
    print("  siblings compare side by side, but EACH CROP NEEDS ITS OWN AUTHORING PASS. The percent"
          " is\n  the share of problem fields that match; the gap is where a copied rung would "
          "invent or erase a claim:")
    for g in partial:
        n = len(problems(by[sorted(g)[0]]))
        print(f"  {len(g)}x  {n:2d} problems each   {identity(g):5.1f}% identical   "
              f"{', '.join(sorted(g))}")

    print(f"\nSINGLETONS ({len(singles)}) -- no sibling at all. "
          f"Batch these by CATEGORY so sourcing overlaps:")
    cat = collections.defaultdict(list)
    for s in singles:
        cat[by[s].get("category", "?")].append(s)
    for k in sorted(cat):
        print(f"  {k:28s} {', '.join(sorted(cat[k]))}")
    print("\nTake a TRUE TWIN first if one exists: that is the only group where the read is one "
          "problem set\nplus a mechanical equality check. Otherwise take a shared-name family and "
          "author every member.")


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
            if v["tier"] != tier:
                continue
            lines.append(f"  {k:28s} applies_to={sorted(v['applies_to'])}")
            # FULL best_use, NEVER truncated. This was `[:150]` and that slice was the mechanical
            # cause of the arc's recurring method-meaning mismatches. The house pattern writes the
            # disambiguation as a trailing "Distinct from <the confusable neighbour>" clause, and
            # 37 of 55 best_use fields ran past 150 characters, so SIX methods lost that clause
            # entirely and `weed_host_control` was cut mid-word at "Disti|nct from garden
            # sanitation". Measured 2026-08-26 against canonical 4a239eef. The methods the
            # authoring passes actually confused -- off_season_tillage, prompt_harvest,
            # sound_sowing_practice, wet_foliage_discipline -- are exactly the truncated ones.
            lines.append(f"      MEANS: {v['best_use']}")
            # CAUTIONS reached the brief nowhere before this. 41 strings across 29 of 55 methods
            # were invisible at authoring time, including sulfur's 90degF limit, copper's aquatic
            # toxicity, Bt killing all lepidoptera and spinosad's bee toxicity. Batch 5's read
            # recorded that those cautions were missing from crop prose without knowing why: an
            # author cannot carry a caution they were never shown.
            for c in (v.get("cautions") or []):
                lines.append(f"      CAUTION: {c}")
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
                # FULL best_use, never truncated -- same defect as cmd_prepare's `[:150]`
                # (fixed in 603f4f8). The house pattern puts the disambiguation in a TRAILING
                # "Distinct from X" clause, so a cut here removes exactly the sentence that
                # decides whether a rung matches its method.
                print(f"      METHOD MEANS: {cm[m]['best_use']}")
                print(f"      RUNG SAYS   : {r.get('note_beginner','')[:104]}")
    print(f"\n  {len(seen)} crop/method pairs to compare.")

    # ---- CROSS-SIBLING: identical source prose, different authored ladder --------------------
    # The mechanical half of the read. Batch 3's only real defect was cucumber and
    # slicing-cucumber sharing a byte-identical prevention_seasoned while one keyed it to
    # resistant_varieties and the other refused. Every gate passed both; it is visible only across
    # crops. Found by hand there; found here from now on.
    srcp = {c["slug"]: [p for _f, p in problems(c)] for c in changed}
    outp = {c["slug"]: [[r["method"] for r in (p.get("control_ladder") or [])]
                        for _f, p in problems(c)] for c in changed}
    rows = cross_sibling_conflicts(srcp, outp)
    print("\n=== CROSS-SIBLING LADDER CONFLICTS (identical prose, different ladder) ===")
    if not rows:
        print("  none. Either the batch has no siblings sharing prose, or they agree.")
    else:
        print(f"  {len(rows)} to ADJUDICATE. A row is not automatically a defect: a divergence is")
        print("  correct when the two crops' prose makes different CLAIMS. It is a defect when the")
        print("  prose they share is the prose the differing rung would be built from.\n")
        for r in rows:
            print(f"  --- {r['problem']}   [{r['a']} vs {r['b']}]")
            if r["only_in_a"]:
                print(f"      only in {r['a']}: {r['only_in_a']}")
            if r["only_in_b"]:
                print(f"      only in {r['b']}: {r['only_in_b']}")
            print(f"      identical ({len(r['identical_fields'])}): {', '.join(r['identical_fields'])}")
            if r["differing_fields"]:
                print(f"      differing: {', '.join(r['differing_fields'])}")

    print("\n" + ("VERIFY: structural checks PASS" if ok else "VERIFY: FAILURES ABOVE"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("families")
    p = sub.add_parser("prepare"); p.add_argument("--crops", required=True); p.add_argument("--out", required=True)
    p = sub.add_parser("merge");   p.add_argument("--out", required=True)
    p = sub.add_parser("verify");  p.add_argument("--out", required=True)
    a = ap.parse_args()
    return {"status": cmd_status, "prepare": cmd_prepare, "families": cmd_families,
            "merge": cmd_merge, "verify": cmd_verify}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
