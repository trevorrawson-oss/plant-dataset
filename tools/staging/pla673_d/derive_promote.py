"""Derive tools/promote_pla673_d.py from tools/promote_pla673_b2.py by targeted, asserted edits (each anchor must match
exactly once). Kept beside the stage as the record of what was changed from the template."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.abspath(os.path.join(HERE, "..", ".."))
s = open(os.path.join(TOOLS, "promote_pla673_b2.py"), encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


head_end = s.index("import argparse")
s = '''#!/usr/bin/env python3
"""promote_pla673_d -- PLA-673 part D: the pepper Phytophthora blight entry re-authored whole from NC State's factsheet
(PLA-688; bell-pepper and banana-pepper, identical), watermelon's row entry re-sourced to UF VH021 (the layout consensus
ruling) with its crop-root mirror, and watermelon's thinning leaves re-authored in both registers. Base aaf004a2 (B2,
6bce088).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (part D rulings, 2026-10-06), each sentence
mapped to rows of the posted packets (PP pepper, C part C) or to the watermelon thinning quotes (W). The stage
(tools/staging/pla673_d/build_stage.py) carries them; this promote applies them and REFUSES unless every one is backed.
Derived from promote_pla673_b2 (copied, not imported: promotes must not import promotes;
tools/staging/pla673_d/derive_promote.py records the edits).

INPUT (tools/staging/pla673_d/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kind: prose (a consumer string), value (a
                 numeric layout figure or its crop-root mirror), sources / anchors (a citation block's lists), catalog (a
                 NEW source_catalog entry; none staged here). cited_at names the block whose sources / anchoring_urls cite
                 the leaf or value.
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, value = the sentence (or the JSON value), quote = the hashed
                 page sentence.
  DECISIONS.tsv  crop, path, decision, reason.

GUARDS (check_post): B blast radius, V values, P prose, D decisions, E evidence (prose AND value ops), A anchors,
C catalog, R dual register, M sense guard (population pinned), plus:
  I  identical entries: every crop in IDENTICAL carries a byte-identical post value at each path IDENTICAL names
     (the pepper entry is ruled identical on both peppers).
  X  mirror: a staged crop-root `spacing_inches` equals the post `in_row_inches` of the first planting_layout entry
     carrying one, default first (spec §1.6 item 7; planting_layout_gate re-checks it roster-wide in gate_all).
  G  gates on the post-state: whole_crop_gate on every edited crop, then gate_all with its population reported.
A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla673_d.py --check
  promote_pla673_d.py --out /path/scratch.json
  promote_pla673_d.py --expect-sha <post sha>           # writes canonical, on approval only
"""
''' + s[head_end:]
rep('STAGE = os.path.join(HERE, "staging", "pla673_b2")', 'STAGE = os.path.join(HERE, "staging", "pla673_d")')
rep('BASE_SHA = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"  # PLA-673 glossary, fbe11bc',
    'BASE_SHA = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"  # PLA-673 part B2, 6bce088')
rep('KINDS = ("prose", "anchors", "sources", "catalog")', 'KINDS = ("prose", "value", "anchors", "sources", "catalog")')
rep('''                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes, spacing_strings)''',
    '''                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes)''')
a = s.index('SOIL_PREP = "<soil_prep>"')
b = s.index('HILL_POPULATION = 225\n') + len('HILL_POPULATION = 225\n')
s = s[:a] + '''# The sense guard's population on the post-state: 225 on aaf004a2, less the two pepper prevention_seasoned leaves (no
# hill-word after the re-author), plus watermelon's thinning.method ("thin to two plants per hill").
HILL_POPULATION = 224
# guard I: paths whose post value must be byte-identical across the named crops (ruled: the pepper entry is identical)
IDENTICAL = {("bell-pepper", "banana-pepper"): ("diseases[id=phytophthora-blight]",)}
''' + s[b:]
rep('''    """The block a cited_at path names, on `root`, or None. "<soil_prep>" is the crop-root sibling pair."""
    if path == SOIL_PREP:
        return {"sources": root.get("soil_prep_sources"), "anchoring_urls": root.get("soil_prep_anchoring_urls")}
    v = _value(root, path)''', '''    """The block a cited_at path names, on `root`, or None."""
    v = _value(root, path)''')
rep('''        if op is None or op["kind"] != "prose":''', '''        if op is None or op["kind"] not in ("prose", "value"):''')
rep('''        if op["kind"] == "prose" and op["new"] is not None and (op["crop"], op["path"]) not in rows_for:''',
    '''        if op["kind"] in ("prose", "value") and (op["crop"], op["path"]) not in rows_for:''')
rep('''        blk_path = (SOIL_PREP if op["path"] == "soil_prep_anchoring_urls" else
                    op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None)''',
    '''        blk_path = op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None''')
rep('''    # guard S: no edited soil_prep leaf restates a spacing (the spacing fields carry it)
    for crop, path in sorted(edited):
        if path.startswith("soil_prep_") and path in set(spacing_strings(qidx[crop])):
            refuse(f"{crop} {path}: restates a spacing")
''', '''    # guard I: ruled-identical entries are byte-identical on the post-state
    for crops, ipaths in IDENTICAL.items():
        for ip in ipaths:
            vals = {compact(_value(qidx[c], ip)) for c in crops}
            if len(vals) != 1:
                refuse(f"{ip}: not identical across {list(crops)} (ruled identical)")
            n["identical"] += 1
    # guard X: a staged crop-root spacing_inches mirrors the first entry carrying in_row_inches, default first
    for op in ops:
        if op["kind"] == "value" and op["path"] == "spacing_inches":
            entries = sorted(qidx[op["crop"]].get("planting_layout") or [], key=lambda e: not e.get("default"))
            src = next((e for e in entries if e.get("in_row_inches") is not None), None)
            if src is None or compact(src["in_row_inches"]) != compact(qidx[op["crop"]]["spacing_inches"]):
                refuse(f"{op['crop']} spacing_inches {qidx[op['crop']]['spacing_inches']!r} is not the mirror "
                       f"{(src or {}).get('in_row_inches')!r}")
            n["mirrors"] += 1
''')
rep('n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0}',
    'n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0,\n'
    '         "identical": 0, "mirrors": 0}')
rep('''          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; {n['register_pairs']} register-pair checks; "''',
    '''          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; {n['register_pairs']} register-pair checks; "
          f"{n['identical']} identical-entry checks; {n['mirrors']} mirror checks; "''')
for left in ("SOIL_PREP", "soil_prep", "spacing_strings", "guard S"):
    assert left not in s, left
open(os.path.join(TOOLS, "promote_pla673_d.py"), "w", encoding="utf-8").write(s)
print("wrote tools/promote_pla673_d.py")
