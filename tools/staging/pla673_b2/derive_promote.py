"""Derive tools/promote_pla673_b2.py from tools/promote_pla666_row_figures.py by targeted, asserted edits (each anchor
must match exactly once). Kept beside the stage as the record of what was changed from the template."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.abspath(os.path.join(HERE, "..", ".."))
s = open(os.path.join(TOOLS, "promote_pla666_row_figures.py"), encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


head_end = s.index("import argparse")
s = '''#!/usr/bin/env python3
"""promote_pla673_b2 -- PLA-673 part B2: the unsupported-claim leaves re-authored from hashed packets, both registers
(eggplant's Phytophthora prevention, the four squash soil_prep leaves with their PLA-674 citation backfill, and parsnip's
three hilling leaves), two document-level ids, and A62 armed on soil_prep. Base 3ccc25f1 (PLA-673 glossary, fbe11bc).

Nothing here authors a value. The texts are claude.ai's, approved by Trevor (B2 rounds 1-2, 2026-10-06), each sentence
mapped to rows of the posted packets (B2, BS, PS, PP); the eggplant rotation follows the ruled precedence rule (a
pathogen-specific T1 page governs a multi-disease rotation paragraph). The stage (tools/staging/pla673_b2/build_stage.py)
carries them; this promote applies them and REFUSES unless every one is backed. Derived from promote_pla666_row_figures
(copied, not imported: promotes must not import promotes; tools/staging/pla673_b2/derive_promote.py records the edits).

INPUT (tools/staging/pla673_b2/):
  ops.json       [{"crop", "path", "kind", "old", "new", "cited_at", "reason"}]. kind: prose (a consumer string),
                 sources / anchors (a citation block's lists; a growth_stages entry may gain them, old "<absent>";
                 the crop-root soil_prep pair is addressed as soil_prep_sources / soil_prep_anchoring_urls), catalog
                 (a NEW source_catalog entry). cited_at names the block whose sources / anchoring_urls cite the leaf;
                 "<soil_prep>" names the crop-root soil_prep_sources / soil_prep_anchoring_urls pair.
  EVIDENCE.tsv   EVIDENCE_COLS; entry_id = the leaf path, value = the sentence, quote = the hashed page sentence.
  DECISIONS.tsv  crop, path, decision, reason.

GUARDS (check_post): the PLA-666 set (B blast radius, V values, P prose, D decisions, E evidence, A anchors, C catalog)
plus:
  R  dual register: an edited *_seasoned leaf's *_beginner sibling is edited too (and the reverse), and the two are
     never byte-identical.
  S  spacing: no edited soil_prep leaf restates a spacing (the wide restatement scanner); the spacing fields carry it.
  M  sense guard: the glossary's own `match` classifies the post roster with nothing unclassified, population pinned.
  G  gates on the post-state: whole_crop_gate on every edited crop (the gate's own PASS verdicts), then gate_all (A62
     armed on soil_prep: the waiver set is the live one) with its population reported.
A STAGE THAT NAMES NO OP REFUSES.

Usage:
  promote_pla673_b2.py --check
  promote_pla673_b2.py --out /path/scratch.json
  promote_pla673_b2.py --expect-sha <post sha>           # writes canonical, on approval only
"""
''' + s[head_end:]
rep('STAGE = os.path.join(HERE, "staging", "pla666_row_figures")', 'STAGE = os.path.join(HERE, "staging", "pla673_b2")')
rep('BASE_SHA = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"  # Housekeeping 60 Phase C, 367c702',
    'BASE_SHA = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"  # PLA-673 glossary, fbe11bc')
rep('KINDS = ("prose", "value", "anchors", "sources", "catalog", "orthography")', 'KINDS = ("prose", "anchors", "sources", "catalog")')
rep('''from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  height_strings, leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes,
                                  spacing_strings)''', '''from cited_promote_common import (EVIDENCE_COLS, Refused, cached_quote, cited_urls, compact, fmt,  # noqa: E402
                                  leaf_diff, manifest, refuse, resolve, serialize, sha256_bytes, spacing_strings)
import glossary_sense  # noqa: E402''')
rep('''# orthography: a spelling-only edit, exempt from the touched-leaf rule (ruling 1, Trevor, 2026-10-05; the Housekeeping
# 60 Phase C guard). `new` must be `old` with exactly these substitutions applied, and a DECISIONS row
# "orthography-only" must say the claims were NOT reviewed (so a spelling fix cannot read as verification).
ORTHOGRAPHY = {"Dorman Red": "Dormanred"}
''', '''SOIL_PREP = "<soil_prep>"
# The sense guard's population on the post-state (the glossary's 232 on 3ccc25f1, less the 7 B2 leaves that no longer
# carry a hill-word: eggplant's prevention_seasoned and the three squash soil_prep pairs).
HILL_POPULATION = 225
''')
rep('''def _block(root, path):
    """The block a cited_at path names, on `root`, or None."""
    v = _value(root, path)''', '''def _block(root, path):
    """The block a cited_at path names, on `root`, or None. "<soil_prep>" is the crop-root sibling pair."""
    if path == SOIL_PREP:
        return {"sources": root.get("soil_prep_sources"), "anchoring_urls": root.get("soil_prep_anchoring_urls")}
    v = _value(root, path)''')
rep('''        if op["kind"] in ("prose", "orthography"):
            _prose_ok(op["new"], tag)
        if op["kind"] == "orthography":                      # guard O
            fixed = op["old"]
            for wrong, right in ORTHOGRAPHY.items():
                fixed = fixed.replace(wrong, right)
            if op["new"] != fixed:
                refuse(f"{tag}: an orthography op may only apply {ORTHOGRAPHY}")''', '''        if op["kind"] == "prose":
            _prose_ok(op["new"], tag)''')
rep('''        if op["kind"] in ("value", "prose") and op["new"] is None and (op["crop"], op["path"]) not in decided:
            refuse(f"op {i} {op['crop']} {op['path']}: a null value needs a DECISIONS row")
        if op["kind"] == "orthography" and "orthography-only" not in decided.get((op["crop"], op["path"]), ()):
            refuse(f"op {i} {op['crop']} {op['path']}: an orthography op needs an orthography-only DECISIONS row")
''', '')   # a null prose value is refused by guard P before guard D: no unreachable null-decision check
rep('''        if d["crop"] != CATALOG and d["crop"] not in pidx:''', '''        if d["crop"] not in (CATALOG, "<roster>") and d["crop"] not in pidx:''')
rep('''        if op is None or op["kind"] not in ("prose", "value"):''', '''        if op is None or op["kind"] != "prose":''')
rep('''        if op["kind"] in ("prose", "value") and op["new"] is not None and (op["crop"], op["path"]) not in rows_for:''',
    '''        if op["kind"] == "prose" and op["new"] is not None and (op["crop"], op["path"]) not in rows_for:''')
rep('''        blk_path = op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None''',
    '''        blk_path = (SOIL_PREP if op["path"] == "soil_prep_anchoring_urls" else
                    op["path"].rsplit(".", 1)[0] if op["path"].endswith(".anchoring_urls") else None)''')
a = s.index('    # guard G: the restatement scanner')
b = s.index('    return n\n\n\ndef gate_post')
s = s[:a] + '''    # guard R: dual register (both edited together; never byte-identical)
    edited = {(op["crop"], op["path"]) for op in ops if op["kind"] == "prose"}
    for crop, path in sorted(edited):
        for a_suf, b_suf in (("_seasoned", "_beginner"), ("_beginner", "_seasoned")):
            if path.endswith(a_suf):
                twin = path[: -len(a_suf)] + b_suf
                if (crop, twin) not in edited:
                    refuse(f"{crop} {path}: re-authored without its {b_suf[1:]} sibling {twin} (dual-register rule)")
                if _value(qidx[crop], path) == _value(qidx[crop], twin):
                    refuse(f"{crop} {path}: byte-identical to {twin} (dual-register rule)")
                n["register_pairs"] += 1
    # guard S: no edited soil_prep leaf restates a spacing (the spacing fields carry it)
    for crop, path in sorted(edited):
        if path.startswith("soil_prep_") and path in set(spacing_strings(qidx[crop])):
            refuse(f"{crop} {path}: restates a spacing")
    # guard M: the glossary's own match classifies the post roster
    try:
        res = glossary_sense.classify_dataset(post, glossary_sense.build_spec(post["glossary"]), floor=HILL_POPULATION)
    except glossary_sense.Refused as e:
        refuse(f"glossary match on the post roster: {e}")
    if res.inspected != HILL_POPULATION:
        refuse(f"glossary match inspected {res.inspected} consumer leaves, not {HILL_POPULATION}")
    n["hill_inspected"] = res.inspected
''' + s[b:]
rep('n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "scanner_hits": 0}',
    'n = {"ops": len(ops), "evidence_rows": 0, "decisions": len(dec), "register_pairs": 0, "hill_inspected": 0}')
rep('''    if passed != len(slugs):
        refuse(f"whole_crop_gate printed {passed} PASS verdicts for {len(slugs)} crops")
    return passed''', '''        if passed != len(slugs):
            refuse(f"whole_crop_gate printed {passed} PASS verdicts for {len(slugs)} crops")
        r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), p], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode != 0:
        refuse(f"gate_all rc={r.returncode}: {out[-600:]}")
    m = re.search(r"gate_all: ran whole_crop_gate on (\\d+) certified crop", out)
    certified = sum(1 for c in post["crops"] if (c.get("verification_status") or {}).get("status") == "verified_gs_arc")
    if not m or int(m.group(1)) != certified or certified == 0:
        refuse(f"gate_all did not report its population ({m.group(1) if m else 'none'} vs {certified} certified)")
    return passed''')
rep('''    print(f"  inspected         {n['ops']} ops on {n['gated_crops']} crops; {n['evidence_rows']} evidence rows; "
          f"{n['decisions']} decisions; {n['scanner_hits']} edited leaves the wide scanner flags (evidenced)")''',
    '''    print(f"  inspected         {n['ops']} ops; whole_crop_gate PASS on {n['gated_crops']} edited crops, then gate_all PASS; "
          f"{n['evidence_rows']} evidence rows; {n['decisions']} decisions; {n['register_pairs']} register-pair checks; "
          f"match inspected {n['hill_inspected']} consumer leaves")''')
for left in ("orthograph", "ORTHOGRAPHY", "height_strings", '"value"', "scanner_hits"):
    assert left not in s, left
open(os.path.join(TOOLS, "promote_pla673_b2.py"), "w", encoding="utf-8").write(s)
print("wrote tools/promote_pla673_b2.py")
