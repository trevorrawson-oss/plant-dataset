#!/usr/bin/env python3
"""sourced_block_ratchet_gate -- the PLA-607 IDENTITY RATCHET over every NAMED sourced block type.

THE RULE (PLA-607, Trevor 2026-09-25/30). On a CERTIFIED crop, a block that carries authored
content and whose citation slot is missing, null, or [] is UNCITED. Today's uncited blocks are
waived BY IDENTITY (crop | path | field) in sourced_block_ratchet_known.py. Any uncited block
NOT in that set fails and prints itself by name. The population may shrink, never grow, and a
swap (close one, break another) fails, because the check is set membership, not a count.

WHY §F CANNOT DO THIS. whole_crop_gate §F fires only on a NON-EMPTY `sources` list, so emptying
`sources` removes a block from its population instead of failing it. Measured on a scratch clone
of cabbage (PLA-607's injection table): §F's leaf count FALLS 147 -> 146 and the gate still
PASSES. §F asks "did you anchor what you cited?"; this gate asks "should this have been cited?".
§F is unchanged (PLA-533 ruling 3).

ARMED BY NAME. Only the block types in BLOCK_TYPES are ratcheted. A sourced field is not covered
until it is named, and naming it is part of adding it: the DISCOVERY guard fails on any
`sources` / `*_sources` / `anchoring_urls` / `*_anchoring_urls` key on a certified crop whose
block is neither named, ruled out (EXCLUDED), nor a recorded anchor-only field (ANCHOR_ONLY).

WHAT COUNTS.
  * A block that is ABSENT or NULL is not uncited: it states nothing.
  * A block that carries authored content (any non-empty value outside its citation keys) with a
    citation slot that is missing, null, [], or a list holding no non-empty string is UNCITED.
    [] never counts as cited.
  * Items of varieties.recommended[] and container_notes.plants_per_pot.readings[] are covered
    by their PARENT block's sources when they carry none of their own: the parent cites the list.
    Every other item family has no parent citation slot, so each item stands alone.

IDENTITY. Keyed items use their pinned key (pests/diseases/growth_stages `id`, rootstock_options
and varieties.recommended `name`), so a reorder does not move them. Unkeyed items use their index.
LIMITATIONS, recorded (2026-09-30):
  1. In an INDEX-keyed family, deleting a waived item and appending a new uncited one can land the
     new one on a waived index. The keyed families cannot be defeated that way.
  2. An identity waiver pins WHICH block is uncited, not WHAT it says. New authored content added
     to an already-waived uncited block (a new sentence in a waived `watering`) stays silent. The
     pot-size sub-rule below is the one place this is closed for a specific field: plum's
     container_notes is waived uncited, and giving it a min_pot_gallons fails there and nowhere
     else (proved at the entry point in test_gate_citation_ratchets_a62_a63.py).

THE CONTAINER POT-SIZE RULE (folded in from container_citation_floor_gate, PLA-533 ruling 1,
2026-09-22). A certified crop stating container_notes.min_pot_gallons with no sources OR no
anchoring URL: KNOWN four, CEILING 4, may go down, never up. It is stricter than the general
ratchet on this one field (the anchors half), so it stays a named sub-rule, not a second gate.

Usage: sourced_block_ratchet_gate.py [PATH]      exit 1 on a violation, 2 on a refused population
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CERTIFIED = "verified_gs_arc"

# ---------------------------------------------------------------- THE NAMED LIST
# Top-level dict blocks whose citation slot is their own `sources` key.
DICT_BLOCKS = (
    "bolting", "container_notes", "fertilizer", "harvest_stop_rule", "heat_threshold_temp_f",
    "indoor_cycle", "pet_safe", "ph", "photoperiod", "pollination", "rotation", "soil",
    "start_method", "storage", "succession_policy", "thinning", "varieties", "watering",
    "winter_hardiness", "yield_expectations",
)
# Crop-root claims cited through a `<name>_sources` sibling: name -> the keys that carry the claim.
SIBLING_BLOCKS = {
    "description": ("description_beginner", "description_seasoned"),
    "harvest_ready": ("harvest_ready_beginner", "harvest_ready_seasoned"),
    "harvest_urgency": ("harvest_urgency",),
    # PLA-10 promote 3 (spec §4.3, plan 58 §8 T5): one crop-root pair cites BOTH height fields.
    "mature_dimensions": ("mature_height_ft", "mature_spread_ft"),
    # PLA-674 (2026-10-05): the soil_prep citation pair, written on every crop record by the PLA-673 glossary promote
    # (null = not assessed, D13; watermelon backfilled). Named here so the keys are not UNNAMED; see SOIL_PREP_ARMED.
    "soil_prep": ("soil_prep_beginner", "soil_prep_seasoned"),
    # PLA-608 ruling 2 (2026-09-25, anchoring partner amended the same day) + the PLA-625 stop-1 ruling (2026-10-09): the
    # rootstock-note citation pair, NAMED in the rootstock_prose_gate tools commit so its keys are never UNNAMED. The
    # fields land with citrus promote 1 (null everywhere, three-state contract, register entry); see the flag below.
    "recommended_rootstock_note": ("recommended_rootstock_note",),
}
# A named sibling block whose ratchet is behind a flag. NAMED from the tools commit (so its keys are never
# UNNAMED), RATCHETED only once its flag flips, in the data commit that writes the siblings: armed on a
# canonical whose PLA-465 heights carry no sibling yet, each of the 16 would fail as a NEW uncited block.
# test_sourced_block_ratchet_gate pins the flag to the data (armed iff a certified crop carries the key).
# ARMED 2026-10-03 in the commit that wrote b331e5f2 (PLA-10 promote 3: 59 certified crops carry the pair).
MATURE_DIMENSIONS_ARMED = True
# soil_prep: NAMED 2026-10-05 (PLA-673 glossary promote), ARMED 2026-10-06 in the PLA-673 part B2 data commit, as ruled:
# the waiver set is the 35 certified crops whose soil_prep prose carries a null citation after B2's backfill; the five
# cited before arming are CLOSED (era identities, sourced_block_ratchet_known.py). Landed promotes that replay an earlier
# post-state pass soil_prep_armed=False or known=KNOWN_AT_ARMING, the mature_dimensions precedent.
SOIL_PREP_ARMED = True
# recommended_rootstock_note: NAMED 2026-10-09 (PLA-608 Part 2's tools commit), NOT ARMED. It flips in the promote that
# writes the pair (citrus promote 1), with that promote's measured waiver set: armed today, every certified crop's
# authored note would fail as a NEW uncited block. test_sourced_block_ratchet_gate pins the flag to the data.
RECOMMENDED_ROOTSTOCK_NOTE_ARMED = False
# List families: name -> (locator, identity key or None for index, parent block covering it or None)
ITEM_FAMILIES = {
    "pests": (("pests",), "id", None),
    "diseases": (("diseases",), "id", None),
    "growth_stages": (("growth_stages",), "id", None),
    "failure_diagnostics": (("failure_diagnostics",), None, None),
    "notifications": (("notifications",), None, None),
    "weather_triggers": (("weather_triggers",), None, None),
    "rootstock_options": (("rootstock_options",), "name", None),
    "varieties.recommended": (("varieties", "recommended"), "name", "varieties"),
    "container_notes.plants_per_pot.readings": (("container_notes", "plants_per_pot", "readings"),
                                                None, "container_notes"),
    "verification_status.field_additions": (("verification_status", "field_additions"), None, None),
    # PLA-10 promote 1 (spec §1.6, §10.1): each (arrangement, support) entry is the ONE citation of its
    # spacing figures; the crop-root spacing_inches is a gated mirror with no sources of its own (A44).
    # The pre-promote string form is not a list, so it is skipped, as it always was.
    "planting_layout": (("planting_layout",), "id", None),
}
# tips_by_stage.<stage>[]: one block type whose stage key is open-ended per crop.
TIPS = "tips_by_stage"

# RULED OUT (Trevor, 2026-09-30). Not silently: each carries its reason.
EXCLUDED = {
    "companions": "provenance DEFERRED (PLA-607; 323 [] slots on 59 crops)",
    "zones": "the legacy zones{} tree, ruled LEAVE; read by plant-astro",
    "regions": "region cells are modeled by design; not in the ratchet",
}
# Anchored claims with NO sources slot. Recorded, not ratcheted: §F cannot see them either, and
# each needs a sources home before it can join the named list. PLA-10 promote 1 gave spacing_inches
# that home (planting_layout entries, named above) and retired spacing_inches_anchoring_urls.
ANCHOR_ONLY = (
    "<crop>.anchoring_urls",
    "days_to_maturity_anchoring_urls",
    "days_to_maturity_mid_anchoring_urls",
    "det_indet.anchoring_urls",
    "germination_temp_f_anchoring_urls",
    "sunlight_hours_anchoring_urls",
    "weeks_indoors_anchoring_urls",
)

CITE_KEYS = ("sources", "anchoring_urls")

# ---------------------------------------------------------------- PLA-10 R5 MIGRATION WAIVERS
# The only way a planting_layout entry ships uncited: a crop on the R5 hunt list whose hunt found no page,
# while the entry's in_row_inches byte-equals the pre-promote spacing_inches. See the module docstring.
import planting_layout_migration_known as _M  # noqa: E402
MIGRATION_ELIGIBLE = _M.ELIGIBLE
MIGRATION_WAIVERS = _M.WAIVERS


def _compact(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)


def migration_verdict(crop, ident):
    """None if `ident` is not a planting_layout entry identity under a migration waiver; otherwise
    (waived: bool, why: str)."""
    slug = crop.get("slug")
    w = MIGRATION_WAIVERS.get(slug)
    m = re.fullmatch(rf"{re.escape(str(slug))}\|planting_layout\[id=([^\]]+)\]\|sources", ident)
    if w is None or m is None or m.group(1) != w.get("entry_id"):
        return None
    if slug not in MIGRATION_ELIGIBLE:
        return False, (f"{ident}: a migration waiver on {slug}, which is not on the R5 hunt list "
                       f"{list(MIGRATION_ELIGIBLE)}; only those crops may ship an uncited entry")
    e = next((x for x in (crop.get("planting_layout") or []) if isinstance(x, dict)
              and x.get("id") == w["entry_id"]), None)
    have = _compact(e.get("in_row_inches")) if e is not None else None
    if have != _compact(w.get("in_row_inches")):
        return False, (f"{ident}: the R5 migration waiver holds only while in_row_inches is byte-equal to "
                       f"the pre-promote spacing_inches {_compact(w.get('in_row_inches'))}; got {have}. "
                       f"A changed figure is a new claim: cite it.")
    return True, ""


# ---------------------------------------------------------------- THE POPULATION FLOOR
# MEASURED 2026-09-30 on 00dda31c: 7063 named blocks on 121 certified crops. The floor sits below
# it so a legitimate shrink passes; a run inspecting fewer than this REFUSES: "0 inspected,
# 0 violations" is not a pass.
MIN_INSPECTED = 6500

# ---------------------------------------------------------------- THE POT-SIZE SUB-RULE
POT_FIELD = "min_pot_gallons"
POT_CEILING = 4
POT_KNOWN = (
    "dry-bean",           # 5 gal (also recommended 5, depth 8) -- sibling of green-beans-bush
    "green-beans-bush",   # 5 gal (also recommended 5, depth 8) -- found via PLA-580's slice
    "grapefruit",         # 20 gal -- sibling of orange-navel
    "orange-navel",       # 15 gal
)


sys.path.insert(0, HERE)
import sourced_block_ratchet_known as _K  # noqa: E402  -- the measured waiver set, a .py module (see its docstring)

_KNOWN_DOC = {"ticket": _K.TICKET, "measured_on": _K.MEASURED_ON, "count": _K.COUNT,
              "identities": list(_K.IDENTITIES)}
KNOWN = frozenset(_K.IDENTITIES)
CLOSED = tuple(_K.CLOSED)
# The waiver set as it stood at arming (00dda31c), before any closure: what a LANDED promote replays against, because
# its post-state predates the citations that closed CLOSED (PLA-10 promotes 1-3). Live gating always uses KNOWN.
KNOWN_AT_ARMING = KNOWN | frozenset(CLOSED)
# The ERA SWITCH (2026-10-06, PLA-673 B2; hardened the same day at Trevor's go-condition 2). A landed promote that
# replays an earlier post-state through gate_all / whole_crop_gate (subprocesses: no `known=` argument reaches A62) sets
# SBR_KNOWN_AT_ARMING to THAT FILE'S sha256. The gate binds it to the file it gates (bind_era, called first thing by
# whole_crop_gate and gate_all) and accepts it ONLY if the SHA is a registered replay post-state below, equals the
# gated file's sha256, and is NOT the live canonical. Anything else raises EraRefused, and a switch that is set but
# never bound raises at first use: setting it in a live run can never let current data pass against an older waiver
# set. The pre-commit hook strips it from its gate runs (tools/test_era_switch_safety.py).
ERA_ENV = "SBR_KNOWN_AT_ARMING"
ERA_POST_STATES = {   # post-state sha256 -> the landed promote whose replay gates it
    "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a": "PLA-673 glossary promote (fbe11bc)",
    "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e": "housekeeping 60 Phase C promote (367c702)",
}
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
_ERA_BOUND = None


class EraRefused(Exception):
    """The era switch was set where it may not apply. Gates print it and exit 2."""


def _sha_file(path):
    import hashlib
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def bind_era(path, canonical=None):
    """Bind the era switch to the file being gated. Returns the bound SHA, or None when the switch is unset."""
    global _ERA_BOUND
    _ERA_BOUND = None
    v = os.environ.get(ERA_ENV)
    if v is None:
        return None
    if v not in ERA_POST_STATES:
        raise EraRefused(f"{ERA_ENV}={v[:16]!r} is not a registered replay post-state SHA "
                         f"(registered: {sorted(s[:8] for s in ERA_POST_STATES)})")
    got = _sha_file(path)
    if got != v:
        raise EraRefused(f"{ERA_ENV}={v[:8]} is not the gated file ({path} is {got[:8]})")
    canonical = CANON if canonical is None else canonical
    if os.path.exists(canonical) and _sha_file(canonical) == v:
        raise EraRefused(f"{ERA_ENV}={v[:8]} is the live canonical; live data is always gated against the live set")
    _ERA_BOUND = v
    return v


def _default_known():
    v = os.environ.get(ERA_ENV)
    if v is None:
        return KNOWN
    if v != _ERA_BOUND:
        raise EraRefused(f"{ERA_ENV} is set but not bound to the gated file (bind_era was not called, or refused)")
    return KNOWN_AT_ARMING


def certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def has_content(v):
    """A value that states something: not None, not an empty string/list/dict."""
    if v is None:
        return False
    if isinstance(v, (str, list, dict)):
        return bool(v)
    return True


def carries_content(block):
    """A block carries authored content if anything outside its citation keys is non-empty."""
    if isinstance(block, dict):
        return any(has_content(v) for k, v in block.items() if k not in CITE_KEYS)
    return has_content(block)


def is_cited(slot):
    """Cited = a list holding at least one non-empty string. Missing, null, [] never count."""
    return isinstance(slot, list) and any(isinstance(s, str) and s.strip() for s in slot)


def _get(crop, locator):
    node = crop
    for k in locator:
        if not isinstance(node, dict):
            return None
        node = node.get(k)
    return node


def _item_label(item, i, key):
    if key and isinstance(item, dict) and isinstance(item.get(key), str) and item[key].strip():
        return f"[{key}={item[key]}]"
    if key and isinstance(item, str) and key == "name" and item.strip():
        return f"[{key}={item}]"
    return f"[{i}]"


def blocks(crop, mature_dimensions_armed=None, soil_prep_armed=None, recommended_rootstock_note_armed=None):
    """Every NAMED block on this crop that carries authored content: [(identity, cited)]."""
    if mature_dimensions_armed is None:
        mature_dimensions_armed = MATURE_DIMENSIONS_ARMED
    if soil_prep_armed is None:
        soil_prep_armed = SOIL_PREP_ARMED
    if recommended_rootstock_note_armed is None:
        recommended_rootstock_note_armed = RECOMMENDED_ROOTSTOCK_NOTE_ARMED
    slug = crop.get("slug")
    out = []

    def add(path, field, cited):
        out.append((f"{slug}|{path}|{field}", cited))

    for name in DICT_BLOCKS:
        b = crop.get(name)
        if isinstance(b, dict) and carries_content(b):
            add(name, "sources", is_cited(b.get("sources")))
    for name, carriers in SIBLING_BLOCKS.items():
        if name == "mature_dimensions" and not mature_dimensions_armed:
            continue
        if name == "soil_prep" and not soil_prep_armed:
            continue
        if name == "recommended_rootstock_note" and not recommended_rootstock_note_armed:
            continue
        if any(has_content(crop.get(k)) for k in carriers):
            add(name, f"{name}_sources", is_cited(crop.get(f"{name}_sources")))
    for name, (loc, key, parent) in ITEM_FAMILIES.items():
        items = _get(crop, loc)
        if not isinstance(items, list):
            continue
        parent_cited = parent is not None and is_cited((crop.get(parent) or {}).get("sources"))
        for i, it in enumerate(items):
            if not carries_content(it):
                continue
            own = it.get("sources") if isinstance(it, dict) else None
            add(name + _item_label(it, i, key), "sources", is_cited(own) or parent_cited)
    tips = crop.get(TIPS)
    if isinstance(tips, dict):
        for stage, items in tips.items():
            if not isinstance(items, list):
                continue
            for i, it in enumerate(items):
                if carries_content(it):
                    own = it.get("sources") if isinstance(it, dict) else None
                    add(f"{TIPS}.{stage}[{i}]", "sources", is_cited(own))
    return out


def uncited(crop, mature_dimensions_armed=None, soil_prep_armed=None, recommended_rootstock_note_armed=None):
    return sorted(ident for ident, cited in blocks(crop, mature_dimensions_armed, soil_prep_armed,
                                                   recommended_rootstock_note_armed) if not cited)


# ---------------------------------------------------------------- DISCOVERY
def _norm(path):
    return re.sub(r"\[\d+\]", "[]", path)


def _named_patterns():
    pats = set(DICT_BLOCKS)
    pats |= {f"{loc_name}[]" for loc_name in ITEM_FAMILIES}
    return pats


def unnamed_fields(crop):
    """Citation keys on this crop that sit on no named, excluded, or anchor-only block."""
    named = _named_patterns()
    sib_keys = {f"{n}_sources" for n in SIBLING_BLOCKS} | {f"{n}_anchoring_urls" for n in SIBLING_BLOCKS}
    found = set()

    def walk(node, path, top):
        if isinstance(node, dict):
            for k, v in node.items():
                child = f"{path}.{k}" if path else k
                if top and k in EXCLUDED:
                    continue
                is_cite = k in CITE_KEYS or k.endswith("_sources") or k.endswith("_anchoring_urls")
                if is_cite:
                    parent = _norm(path) if path else "<crop>"
                    if path == "" and k in sib_keys:
                        pass
                    elif path == "" and k in ANCHOR_ONLY:
                        pass
                    elif k in CITE_KEYS and (parent in named or re.fullmatch(rf"{TIPS}\.[^.\[]+\[\]", parent)):
                        pass
                    elif k in CITE_KEYS and f"{parent}.{k}" in ANCHOR_ONLY:
                        pass
                    else:
                        found.add(f"{parent}.{k}" if path else k)
                    continue
                walk(v, child, False)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", False)

    walk(crop, "", True)
    return sorted(found)


# ---------------------------------------------------------------- POT SUB-RULE
def pot_uncited(crop):
    if not certified(crop):
        return False
    cn = crop.get("container_notes")
    cn = cn if isinstance(cn, dict) else {}
    if cn.get(POT_FIELD) is None:
        return False
    return not (cn.get("sources") or []) or not (cn.get("anchoring_urls") or {})


# ---------------------------------------------------------------- VERDICTS
def crop_violations(crop, mature_dimensions_armed=None, known=None):
    """Per-crop half (whole_crop_gate A62). No-op off certified: the waivers cover certified only."""
    if not certified(crop):
        return []
    V = []
    known = _default_known() if known is None else known
    for ident in uncited(crop, mature_dimensions_armed):
        mv = migration_verdict(crop, ident)
        if mv is not None:
            if not mv[0]:
                V.append(mv[1])
            continue
        if ident not in known:
            V.append(f"NEW uncited block {ident}: it carries authored content and its citation "
                     f"slot is missing, null or []. Cite it. The PLA-607 ratchet waives only the "
                     f"blocks uncited on {_KNOWN_DOC['measured_on'][:8]}, by identity.")
    for f in unnamed_fields(crop):
        V.append(f"UNNAMED sourced field {f}: a citation key on a block the PLA-607 ratchet does "
                 f"not name. Naming it is part of adding it: add it to BLOCK_TYPES (or, with a "
                 f"recorded reason, to EXCLUDED / ANCHOR_ONLY) in sourced_block_ratchet_gate.py.")
    if pot_uncited(crop) and crop.get("slug") not in POT_KNOWN:
        V.append(f"{crop.get('slug')}: states container_notes.{POT_FIELD} with no sources and/or "
                 f"no anchoring url, and is NOT one of the {POT_CEILING} known uncited crops. The "
                 f"PLA-533 floor is a RATCHET: this population may shrink, never grow.")
    return V


def roster(data, mature_dimensions_armed=None, known=None):
    """(certified_count, inspected, live_uncited, violations, stale, pot_live)."""
    cert = [c for c in data.get("crops", []) if certified(c)]
    inspected, live, V = 0, [], []
    for c in cert:
        bl = blocks(c, mature_dimensions_armed)
        inspected += len(bl)
        live.extend(i for i, ok in bl if not ok)
        V.extend(crop_violations(c, mature_dimensions_armed, known))
    pot_live = sorted(c["slug"] for c in cert if pot_uncited(c))
    if len(pot_live) > POT_CEILING:
        V.append(f"uncited {POT_FIELD} population is {len(pot_live)}, ratchet ceiling is "
                 f"{POT_CEILING}: {pot_live}")
    stale = sorted((_default_known() if known is None else known) - set(live))
    return len(cert), inspected, sorted(live), V, stale, pot_live


def refusal(n_cert, inspected):
    if n_cert == 0:
        return "inspected 0 certified crops"
    if inspected < MIN_INSPECTED:
        return f"inspected {inspected} blocks, below the declared floor {MIN_INSPECTED}"
    return None


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    n_cert, inspected, live, V, stale, pot_live = roster(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"sourced_block_ratchet_gate: {len(V)} violation(s); inspected {inspected} named blocks "
          f"on {n_cert} certified crops; {len(live)} uncited, {len(KNOWN)} waived by identity; "
          f"pot-size sub-rule {len(pot_live)}/{POT_CEILING}")
    if stale:
        print(f"  CLOSED since arming ({len(stale)}): drop from sourced_block_ratchet_known.py "
              f"in the commit that cites them: " + ", ".join(stale[:20])
              + (" ..." if len(stale) > 20 else ""))
    why = refusal(n_cert, inspected)
    if why:
        print(f"sourced_block_ratchet_gate: REFUSED -- {why}. A check that inspected nothing is "
              f"not a pass.")
        return 2
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
