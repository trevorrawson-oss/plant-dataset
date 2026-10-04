"""Usage: python3 tools/staging/housekeeping60/b14_scanner_equivalence_proof.py 7a115f0

B1-4 proof: the generic scanner reproduces both old scanners byte for byte (kickoff 60, ruling 5).

OLD = spacing_strings (cited_promote_common) and height_strings (promote 3) as committed at OLD_COMMIT, loaded
from git by source text. NEW = the working tree's cited_promote_common.spacing_strings / height_strings, which
must now be thin wrappers over distance_restatements. Inputs: promote 1's fixed list (its 113 staged crops) and
promote 3's (NEW_CROPS + BACKFILL_CROPS, 62), each on its promote's pre-state AND post-state; every crop run
through BOTH scanners (height in both spread modes). Output: one JSON blob per side; their sha256 must match.
"""
import ast, hashlib, json, os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OLD_COMMIT = sys.argv[1]
sys.path.insert(0, REPO + "/tools")
import promote_fixture  # noqa: E402
import cited_promote_common as NEW  # noqa: E402
import promote_pla10_planting_layout as P1  # noqa: E402
import promote_pla10_promote3 as P3  # noqa: E402


def show(path):
    return subprocess.run(["git", "-C", REPO, "show", f"{OLD_COMMIT}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def defs(src, names):
    t = ast.parse(src)
    return "\n\n".join(ast.get_source_segment(src, n) for n in t.body
                       if (isinstance(n, ast.FunctionDef) and n.name in names) or
                       (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names))


old_ns = {"re": re}
exec(defs(show("tools/cited_promote_common.py"), {"DIST", "SPACING_WORD", "SKIP_SUBTREES", "fmt", "spacing_strings"}),
     old_ns)
exec(defs(show("tools/promote_pla10_promote3.py"), {"HEIGHT_WORD", "WIDTH_WORD", "height_strings"}), old_ns)
assert "def distance_restatements" not in show("tools/cited_promote_common.py"), "OLD_COMMIT already generic"
assert NEW.spacing_strings is not old_ns["spacing_strings"]


def run(spacing, height):
    out = []
    p1_list = sorted(P1.load_stage(P1.STAGE)[0])
    p3_list = list(P3.NEW_CROPS + P3.BACKFILL_CROPS)
    for label, base, post, fixed in (("P1", P1.BASE_SHA, "cf1d480dfc926b226f63fde2fbdbc548e9d06487ed749e7431a06710431f2e49", p1_list),
                                     ("P3", P3.BASE_SHA, "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d", p3_list)):
        for state, sha in (("pre", base), ("post", post)):
            idx = {c["slug"]: c for c in json.loads(promote_fixture.pre_state(sha))["crops"]}
            for slug in fixed:
                c = idx[slug]
                out.append([label, state, slug, spacing(c), height(c, False), height(c, True)])
    return out


old = run(old_ns["spacing_strings"], old_ns["height_strings"])
# B3 (2026-10-03) made the WIDE scanner the default; B1-4's claim is about the NARROW one, so compare wide=False.
new = run(lambda c: NEW.spacing_strings(c, wide=False), lambda c, sp: NEW.height_strings(c, sp, wide=False))
ob, nb = json.dumps(old).encode(), json.dumps(new).encode()
hits = sum(len(r[3]) + len(r[4]) + len(r[5]) for r in old)
print(f"rows {len(old)} (crop x state), scanner hits {hits}")
print("old sha256", hashlib.sha256(ob).hexdigest())
print("new sha256", hashlib.sha256(nb).hexdigest())
print("BYTE-IDENTICAL" if ob == nb else "DIFFERENT")
sys.exit(0 if ob == nb else 1)
