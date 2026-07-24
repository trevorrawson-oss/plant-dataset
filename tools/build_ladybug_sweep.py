#!/usr/bin/env python3
"""build_ladybug_sweep.py -- roster-wide consumer-copy convention fix: "lady beetle" -> "ladybug".

Trevor's common-tongue rule ([[consumer-copy-common-tongue]]): use the everyday word a home
gardener says. Whole-substring replace of the two case variants across EVERY string value in the
canonical (the plural falls out because the trailing 's' sits outside the matched substring:
"lady beetles" -> "ladybugs"). Deterministic; re-dumps COMPACT (separators=(",",":"),
ensure_ascii=False, no trailing newline). READ the count it prints before trusting it.

Usage: build_ladybug_sweep.py [--write]   (default: dry-run, reports count only)
"""
import json, sys

PATH = "crops_data_final.json"
REPLACEMENTS = [("Lady beetle", "Ladybug"), ("lady beetle", "ladybug")]


def fix(s):
    for a, b in REPLACEMENTS:
        s = s.replace(a, b)
    return s


def walk(obj, counter):
    if isinstance(obj, dict):
        return {k: walk(v, counter) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, counter) for v in obj]
    if isinstance(obj, str):
        new = fix(obj)
        if new != obj:
            counter[0] += 1
        return new
    return obj


def main():
    write = "--write" in sys.argv
    with open(PATH) as fh:
        data = json.load(fh)
    counter = [0]
    out = walk(data, counter)
    # sanity: no residual "lady beetle" anywhere (case-insensitive)
    dumped = json.dumps(out, separators=(",", ":"), ensure_ascii=False)
    residual = dumped.lower().count("lady beetle")
    print(f"strings changed: {counter[0]} | residual 'lady beetle': {residual} | "
          f"'ladybug' count: {dumped.lower().count('ladybug')}")
    assert residual == 0, "residual 'lady beetle' remains -- aborting"
    assert dumped.count("\n") == 0 and "\\u" not in dumped, "not compact / escaped-unicode"
    assert len(out["crops"]) == len(data["crops"]), "crop count changed"
    if write:
        with open(PATH, "w") as fh:
            fh.write(dumped)
        print("WROTE canonical (compact, no trailing newline)")
    else:
        print("dry-run (pass --write to apply)")


if __name__ == "__main__":
    main()
