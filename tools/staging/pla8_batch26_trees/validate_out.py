#!/usr/bin/env python3
"""validate_out -- per-crop validator handed to each batch-26 authoring agent.

Run:  python3 tools/staging/pla8_batch26_trees/validate_out.py <crop-slug>

It checks the things a promote guard will check later, so an agent finds them while fixing is cheap.
It is NOT the promote suite; passing here does not mean the batch passes.

NOTE TO AGENTS: if this validator is itself wrong, fix it on disk and say that you did. Batch 24's
equivalent was wrong twice (it demanded one crop's declared identity from every single-crop run, and
a length mismatch skipped a whole loop so an early refusal count was a floor, not a count).
Tooling handed to a fan-out gets exercised harder than its author exercised it.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CANON = os.path.join(REPO, "crops_data_final.json")
PINS = os.path.join(HERE, "pinned_ids.json")

# IMPORT the gate's tables; never retype them. A retyped copy of this exact table diverged from the
# real gate in two ways on first writing: it omitted `physiological` and `vertebrate`, and it failed
# OPEN on an unrecognized type where control_ladder_gate fails CLOSED. Retyping gate logic has
# caused bugs in this repo before.
sys.path.insert(0, os.path.join(REPO, "tools"))
from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET, TIER_RANK  # noqa: E402

TIER_ORDER = dict(TIER_RANK)


def fail(msgs, m):
    msgs.append(m)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: validate_out.py <crop-slug>")
    crop = sys.argv[1]
    out_path = os.path.join(HERE, f"out_{crop}.json")
    if not os.path.exists(out_path):
        sys.exit(f"missing {out_path}")

    data = json.load(open(CANON, encoding="utf-8"))
    cm = data["control_methods"]
    canon = {c["slug"]: c for c in data["crops"]}[crop]
    pins_all = json.load(open(PINS, encoding="utf-8"))
    pins = pins_all[crop]
    out = json.load(open(out_path, encoding="utf-8"))

    msgs = []
    if out.get("crop") != crop:
        fail(msgs, f"crop field is {out.get('crop')!r}, expected {crop!r}")

    for field in ("pests", "diseases"):
        canon_entries = canon.get(field) or []
        out_entries = out.get(field) or []
        pin_rows = {r["name"]: r for r in pins.get(field, [])}

        # COVERAGE, BOTH DIRECTIONS -- against the PIN TABLE, which is this batch's TARGET state.
        # Comparing output names against CANONICAL names was WRONG and is fixed here (2026-09-04,
        # mint authoring agent): pinned_ids.json splits four bundles, renames three entries and
        # retires two, so a canonical-name walk reports every split limb as EXTRA and every bundle
        # as MISSING. On mint that is 5 spurious refusals against correct output. Canonical is
        # still walked, below, for provenance -- the side the pin walk cannot see.
        pin_names = set(pin_rows)
        out_names = [e.get("name") for e in out_entries]
        if len(out_names) != len(set(out_names)):
            fail(msgs, f"{field}: duplicate names in output")
        for n in sorted(pin_names - set(out_names)):
            fail(msgs, f"{field}: MISSING problem {n!r} (pinned target, absent from output)")
        for n in sorted(set(out_names) - pin_names):
            fail(msgs, f"{field}: EXTRA problem {n!r} (not in the pin table)")

        # PROVENANCE. Every CANONICAL entry must be accounted for by the pin table: kept under its
        # own name, named inside some row's `from` (RENAME from 'X' / SPLIT n/m from 'X'), or
        # listed in the pin table's `_retired`. Without this, silently dropping a canonical problem
        # would pass, which is exactly what the old canonical walk was there to prevent.
        retired = {r.get("name") for r in pins_all.get("_retired") or []
                   if r.get("crop") == crop and r.get("field") == field}
        claimed = set(pin_names) | retired
        for r in pins.get(field, []):
            claimed.update(re.findall(r"'([^']+)'", r.get("from") or ""))
        for e in canon_entries:
            if e["name"] not in claimed:
                fail(msgs, f"{field}: canonical problem {e['name']!r} is accounted for by no pin row "
                           f"(not kept, not renamed/split from, not retired)")

        for e in out_entries:
            name = e.get("name")
            row = pin_rows.get(name)
            if row is None:
                fail(msgs, f"{field}/{name!r}: no pin row")
                continue
            if e.get("id") != row["id"]:
                fail(msgs, f"{field}/{name!r}: id {e.get('id')!r} != pinned {row['id']!r}")

            # PINNED-BUT-UNCHECKED FIELDS (added 2026-09-04, oregano authoring agent).
            # `type` and `severity` are pinned in pinned_ids.json and were read from the PIN below
            # to check ladder legality, but the OUTPUT's own values were never compared to them.
            # That is the batch-24 unpinned-target-field failure mode: MEASURED here by mutation,
            # a file that reverted oregano's `spider-mites` type from the pinned `mite` back to
            # `insect` -- the exact defect adjudication A1 exists to fix, and the one that makes
            # `even_watering` and `sulfur` illegal -- validated GREEN, because the ladder was
            # still being checked against the pin's `mite` while the record shipped `insect`.
            for pinned_field in ("type", "severity"):
                if pinned_field in row and e.get(pinned_field) != row[pinned_field]:
                    fail(msgs, f"{field}/{name!r}: {pinned_field} {e.get(pinned_field)!r} "
                               f"!= pinned {row[pinned_field]!r}")

            ptype = row.get("type")

            ladder = e.get("control_ladder")
            if not isinstance(ladder, list) or not ladder:
                # `[]` is not `None`: an empty ladder once passed every gate. Refuse it here.
                fail(msgs, f"{field}/{name!r}: control_ladder must be a non-empty list")
                continue

            last_tier = -1
            seen_methods = set()
            for i, rung in enumerate(ladder):
                where = f"{field}/{name!r}/rung{i}"
                method = rung.get("method")
                if method not in cm:
                    fail(msgs, f"{where}: unknown method {method!r}")
                    continue
                if method in seen_methods:
                    fail(msgs, f"{where}: method {method!r} repeated within this ladder")
                seen_methods.add(method)

                tier = cm[method].get("tier")
                ti = TIER_ORDER.get(tier, -1)
                if ti < last_tier:
                    fail(msgs, f"{where}: tier {tier!r} follows a higher tier (ladder must be least-invasive-first)")
                last_tier = max(last_tier, ti)

                # Same semantics as control_ladder_gate: `any` is universal; an unrecognized type
                # FAILS CLOSED rather than silently skipping the coherence check.
                applies = set(cm[method].get("applies_to") or [])
                if UNIVERSAL_TARGET not in applies:
                    if ptype not in TYPE_TARGETS:
                        fail(msgs, f"{where}: problem type {ptype!r} is not a recognized type "
                                   f"(applies_to coherence cannot be checked)")
                    elif not (applies & TYPE_TARGETS[ptype]):
                        fail(msgs, f"{where}: method {method!r} applies_to {sorted(applies)} "
                                   f"does not reach type {ptype!r}")

                for reg in ("note_beginner", "note_seasoned"):
                    t = rung.get(reg)
                    if not isinstance(t, str) or not t.strip():
                        fail(msgs, f"{where}: {reg} missing or empty")
                        continue
                    if "—" in t or "–" in t:
                        fail(msgs, f"{where}: {reg} contains an em/en dash")
                    if re.search(r"\d\s*°\s*C(?![a-z])", t) and "°F" not in t:
                        fail(msgs, f"{where}: {reg} gives °C with no °F")
                    if re.search(r"(?<![.!?\"'\w])[Pp]lant Pro", t) is None and re.search(r"(?<=[a-z] )Plant\b", t):
                        fail(msgs, f"{where}: {reg} capitalizes 'Plant' mid-sentence")
                nb, ns = rung.get("note_beginner") or "", rung.get("note_seasoned") or ""
                if nb and nb.strip() == ns.strip():
                    fail(msgs, f"{where}: the two registers are byte-identical")

    if msgs:
        print(f"REFUSED: {len(msgs)} problem(s)\n")
        for m in msgs:
            print("  - " + m)
        return 1
    total = sum(len(r.get("control_ladder") or []) for f in ("pests", "diseases") for r in out.get(f) or [])
    print(f"OK: {crop} validates. "
          f"{len(out.get('pests') or [])} pests + {len(out.get('diseases') or [])} diseases, {total} rungs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
