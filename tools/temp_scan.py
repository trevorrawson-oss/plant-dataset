#!/usr/bin/env python3
"""Shared spelled-temperature scanner + fixer (post-114 §C). ONE source of truth, imported by
whole_crop_gate (C/D) and release_verify (D). Flags/rewrites spelled temperature forms that should
render as the canonical °F; EXCLUDES latitude/angle 'degrees'.

The old per-gate regex (\\bdegrees?\\s*F\\b|\\bdeg\\.?\\s*F\\b|°\\s+F) was too narrow -- it missed
'90 degrees', bare '50 F', and 'degrees Fahrenheit' (all of which shipped). This widens it.
"""
import re

# spelled temperature forms
_TEMP_RES = [
    re.compile(r"\d+\s*(?:to\s*\d+\s*)?degrees?\b", re.I),  # '90 degrees', '70 to 80 degrees'
    re.compile(r"\bdegrees?\s*F\b", re.I),                  # 'degrees F' (old form, no number)
    re.compile(r"\bdeg\.?\s*F\b", re.I),                    # 'deg F' / 'deg. F'
    re.compile(r"°\s+F"),                                   # '° F' (space between ° and F)
    re.compile(r"\b\d{2,3}\s*F\b"),                         # bare '50 F' (no degree sign)
]
# EXPLICIT latitude/angle adjacency: a match immediately followed by one of these is NOT temperature
# (e.g. "45 degrees north", the clarified "38 to 39°N"). A bare "38 to 39 degrees" with no N/S marker
# is intentionally NOT excluded -- it is ambiguous and SHOULD be flagged so a human clarifies it to °N.
# NOTE: `\s+` (not `\s*`) before the N/S token -- otherwise `degrees?` + `[NS]` matches the trailing
# 's' of a plain "degrees" and wrongly excludes every temperature.
_LAT_TOKEN = re.compile(r"°\s*[NS]\b|degrees?\s+(?:[NS]\b|north|south|of\s+latitude|latitude)", re.I)


def spelled_temp_hits(s):
    """Return a list of offending temperature fragments in s ([] = clean). Skips only EXPLICIT
    latitude/angle adjacency (°N, "degrees north/latitude")."""
    if not isinstance(s, str):
        return []
    hits = []
    for rx in _TEMP_RES:
        for m in rx.finditer(s):
            i, j = m.start(), m.end()
            if _LAT_TOKEN.search(s[i:j + 12]):
                continue
            hits.append(m.group())
    return hits


# fixer: a number (or range) + 'degrees[ F/Fahrenheit]' -> '<n>°F'; bare '<n> F' -> '<n>°F'
_CONV_DEGREES = re.compile(r"(\d+(?:\s*(?:to|-|–)\s*\d+)?)\s*degrees?(?:\s*Fahrenheit|\s*F)?\b", re.I)
_CONV_BARE_F = re.compile(r"\b(\d{2,3})\s*F\b")


def convert_temps(s):
    """Rewrite spelled temperature forms in s to canonical °F. Skips latitude/angle; idempotent."""
    if not isinstance(s, str):
        return s

    def repl_deg(m):
        after = s[m.end():m.end() + 12]
        if re.match(r"\s*(?:[NS]\b|north|south|latitude)", after, re.I):
            return m.group(0)
        return m.group(1) + "°F"

    out = _CONV_DEGREES.sub(repl_deg, s)
    out = _CONV_BARE_F.sub(lambda m: m.group(1) + "°F", out)
    return out


if __name__ == "__main__":
    import json
    import sys
    from field_classification import is_backend
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    inspected = 0   # user-facing strings actually examined -- the population

    def walk(o, pat, slug):
        global total, inspected
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if not is_backend(k, pat):
                    if isinstance(v, str):
                        inspected += 1
                        for h in spelled_temp_hits(v):
                            print(f"  {slug} {p}: {h!r}")
                            total += 1
                    elif isinstance(v, list):
                        for i, x in enumerate(v):
                            if isinstance(x, str):
                                inspected += 1
                                for h in spelled_temp_hits(x):
                                    print(f"  {slug} {p}[{i}]: {h!r}")
                                    total += 1
                walk(v, p, slug)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]", slug)

    # A check that cannot distinguish "inspected and clean" from "inspected nothing"
    # is not a check (CLAUDE.md, 2026-09-22). This scan printed only its hit count, so
    # a clean roster and an EMPTY one produced the same line. The floor is set well
    # below the measurement on 526788f2 so ordinary authoring never trips it.
    MIN_STRINGS = 50000
    for c in data["crops"]:
        walk(c, "", c.get("slug", "?"))
    print(f"spelled-temp scan: {total} user-facing hit(s) across {inspected} "
          f"user-facing string(s) in {len(data['crops'])} crop(s)")
    if inspected < MIN_STRINGS:
        print(f"  REFUSED (VACUOUS): inspected {inspected} strings, floor is {MIN_STRINGS}. "
              f"A scan that inspected nothing must not report a clean run.")
        sys.exit(2)
    sys.exit(1 if total else 0)
