#!/usr/bin/env python3
"""control_ladder_gate -- the IPM pest/disease control-ladder honesty engine (spec 2026-07-22).

SOFT + standalone (overwinter_hardiness / variety_detail pattern) through the pilot; HARD-FLIPS into
whole_crop_gate A39 + gate_all when the roster-wide rollout reaches full coverage (INV-1).

  CATALOG   -- every control_methods entry has the required keys, a valid tier, non-empty pros/cons,
               and T1 catalogued sources.
  LADDER    -- every control_ladder is referentially sound, monotonic by tier (softest-first), and
               applies_to-coherent with the problem's `type`.
  IDENTITY  -- every pest/disease carries a unique kebab `id` within its crop.
Short ladders are VALID (a cultural-only ladder must pass); the gate never requires reaching `conventional`.

Usage: control_ladder_gate.py [PATH] [--coverage]
"""
import json, os, re, sys

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
TIER_RANK = {t: i for i, t in enumerate(TIERS)}

# type -> the applies_to targets that legitimately apply to it
TYPE_TARGETS = {
    "insect":        {"insect_soft_bodied", "insect_chewing", "insect_boring", "insect_general"},
    "mite":          {"mite", "insect_general"},
    "mollusk":       {"mollusk"},
    "fungal":        {"fungal_foliar", "fungal_soilborne", "disease_general"},
    "bacterial":     {"bacterial", "disease_general"},
    "viral":         {"viral", "disease_general"},
    "physiological": {"physiological"},
    "nematode":      {"nematode"},
}
UNIVERSAL_TARGET = "any"   # cultural/physical practices that apply broadly
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_REQ_METHOD = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
               "best_use", "pros", "cons", "sources", "anchoring_urls")


def load(path):
    with open(path) as f:
        return json.load(f)


def catalog(data):
    return data.get("control_methods") or {}


def _problems(crop):
    return list(crop.get("pests") or []) + list(crop.get("diseases") or [])


def catalog_violations(data):
    V = []
    cat = catalog(data)
    srcs = data.get("source_catalog") or {}
    for mid, m in cat.items():
        for k in _REQ_METHOD:
            if k not in m or m[k] in (None, "", [], {}):
                V.append(f"control_methods/{mid}: missing/empty required key '{k}'")
        if m.get("tier") not in TIER_RANK:
            V.append(f"control_methods/{mid}: invalid tier {m.get('tier')!r}")
        for s in (m.get("sources") or []):
            if s not in srcs:
                V.append(f"control_methods/{mid}: source '{s}' not in source_catalog")
            elif srcs[s].get("tier") != "T1":
                V.append(f"control_methods/{mid}: source '{s}' is not T1")
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            V.append(f"control_methods/{mid}: anchoring_urls keys do not match sources")
    return V


def ladder_violations(data, crop):
    V = []
    cat = catalog(data)
    slug = crop.get("slug", "?")
    for p in _problems(crop):
        pid = p.get("id") or p.get("name") or "?"
        ladder = p.get("control_ladder")
        if ladder is None:
            continue
        ranks, ptype = [], p.get("type")
        for rung in ladder:
            mid = rung.get("method")
            m = cat.get(mid)
            if m is None:
                V.append(f"{slug}/{pid}: control_ladder references unknown method '{mid}'")
                continue
            ranks.append(TIER_RANK[m["tier"]])
            targets = set(m.get("applies_to") or [])
            if UNIVERSAL_TARGET not in targets and ptype in TYPE_TARGETS:
                if not (targets & TYPE_TARGETS[ptype]):
                    V.append(f"{slug}/{pid}: method '{mid}' (applies_to {sorted(targets)}) "
                             f"does not fit problem type '{ptype}'")
        if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):
            V.append(f"{slug}/{pid}: control_ladder is not softest-first (tier ranks {ranks})")
    return V
