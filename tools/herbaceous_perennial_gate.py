#!/usr/bin/env python3
"""Herbaceous-perennial structural cert branch (asparagus GS arc, anchor pilot; later artichoke).
Fires ONLY for archetype == 'herbaceous_perennial' (a no-op otherwise). Imported + run by
whole_crop_gate.py as section A46. The calendar itself is validated by the frost_anchored annual
layer (A5/A24/A28) -- this gate owns the invariants unique to a no-replant perennial VEGETABLE:
the establishment lag, succession suppression, and per-region SUITABILITY honesty (a chill-
dependent crop that will not perennialize in the tropics is marked, not given a fake calendar).

See docs/superpowers/specs/2026-07-23-asparagus-herbaceous-perennial-archetype-design.md.
Scoped to archetype (not calendar_basis) so the herbaceous HERBS (chives/mint/bee-balm on
culinary_herb / companion_and_ornamental_flower, ruled 2026-07-05) stay untouched.
"""
# The roster's suitability vocabulary, all five values. Measured on canonical ea3636e7:
# fruits_reliably 292, marginal 180, unsuitable 165, survives_no_fruit 118, perennializes 25.
#
# WIDENED 2026-07-28 (artichoke GS arc) from the three asparagus happened to need. The gate was
# not ruling the other two out -- it had never seen them, and a crop joining this archetype could
# not reach for a value 17 other crops already publish. `survives_no_fruit` in particular carries
# a RULED display behavior (flagged ornamental-only: the plant lives and gives you no food,
# someone may still want it), which is exactly artichoke in the tropics -- UF/IFAS's mechanism is
# that plants stay vegetative and never initiate buds, so the plant thrives and gives no
# artichokes. Rating that `unsuitable` would hide a cell about a plant that grows perfectly well.
#
# `annual_only` is deliberately NOT here. It would fit artichoke's cold-region cells better than
# `marginal` does, but it is a frontend-visible vocabulary change with no renderer support, and
# design-decisions B.6 recorded it as an open finding rather than smuggling it in mid-arc.
SUITABILITY_ENUM = {"perennializes", "fruits_reliably", "marginal", "unsuitable",
                    "survives_no_fruit"}

# Values that must explain themselves. A cell that says the planting will not persist, will not
# grow, or will grow and never feed you is making a claim the grower is owed a reason for.
# `survives_no_fruit` belongs here for the same reason `unsuitable` does -- it is a stronger
# statement than `marginal`, not a weaker one, and without the note it reads as a bare downgrade.
NOTE_REQUIRED = {"marginal", "unsuitable", "survives_no_fruit"}


def herbaceous_perennial_violations(crop):
    """Return a list of violation strings ([] = clean). No-op unless archetype herbaceous_perennial."""
    if crop.get("archetype") != "herbaceous_perennial":
        return []
    V = []

    # 1. perennial flag (a herbaceous perennial is, definitionally, perennial).
    if crop.get("perennial") is not True:
        V.append(f"perennial must be true for a herbaceous_perennial crop; got {crop.get('perennial')!r}")

    # 2. permanent-bed lifecycle.
    if crop.get("lifecycle") not in ("perennial", "permanent"):
        V.append(f"lifecycle must be perennial|permanent for a herbaceous_perennial crop; "
                 f"got {crop.get('lifecycle')!r}")

    # 3. succession SUPPRESSED with a stated reason (a permanent bed is never succession-planted).
    sp = crop.get("succession_policy") or {}
    if sp.get("suitable") is not False:
        V.append(f"succession_policy.suitable must be false (a permanent bed is not succession-"
                 f"planted); got {sp.get('suitable')!r}")
    elif not sp.get("reason_seasoned"):
        V.append("succession_policy.reason_seasoned must explain why succession is unsuitable")

    # 4. establishment fields sane (the multi-year lag that distinguishes this archetype).
    yfh = crop.get("years_to_first_harvest")
    if not (isinstance(yfh, list) and yfh
            and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in yfh)
            and min(yfh) >= 1):
        V.append(f"years_to_first_harvest must be a non-empty numeric list with min >= 1 (a real "
                 f"establishment lag); got {yfh!r}")
    if not crop.get("years_to_full_production"):
        V.append(f"years_to_full_production must be non-empty; got {crop.get('years_to_full_production')!r}")
    pls = crop.get("productive_lifespan_years")
    if not (isinstance(pls, int) and not isinstance(pls, bool) and pls > 0):
        V.append(f"productive_lifespan_years must be a positive int; got {pls!r}")

    # 5/6. per region: no succession/second_planting tracks; per filled cell: suitability coherence.
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        for p in (r.get("plantings") or []):
            if isinstance(p, dict) and p.get("track") in ("succession", "second_planting"):
                V.append(f"{rk}: a permanent bed must not carry a {p.get('track')!r} planting track")
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            suit = cell.get("suitability")
            cal = cell.get("calendar") or []
            if suit is None and not cal:
                continue  # admission state: an unfilled shell cell
            if suit not in SUITABILITY_ENUM:
                V.append(f"{rk}.{z}: suitability {suit!r} not in {sorted(SUITABILITY_ENUM)}")
                continue
            if suit in NOTE_REQUIRED and not cell.get("suitability_note_seasoned"):
                V.append(f"{rk}.{z}: a {suit} cell must carry suitability_note_seasoned -- the "
                         f"reason the grower is owed (what actually limits the crop here), not a "
                         f"bare downgrade and not a fake calendar")
            if not cal:
                V.append(f"{rk}.{z}: a suitability-marked cell must carry a non-empty calendar "
                         f"(the A32 honesty floor -- mark unsuitable, still show the honest cycle)")

    # 7. permanent-bed rotation guidance present.
    if crop.get("rotation") in (None, "", []):
        V.append("rotation must be present (a permanent bed's no-rotate guidance)")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in herbaceous_perennial_violations(c):
            print(f"  {c.get('slug')}: {v}")
            total += 1
    print(f"herbaceous_perennial gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
