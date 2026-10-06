"""Mutation harness for tools/glossary_sense.py + its staged match spec (PLA-673 sense guard).

Each mutation edits a SCRATCH copy of the module or the spec, proves it applied (MUTATION-APPLIED: the bytes changed),
runs tools/test_glossary_sense.py there, and must REDDEN. Liveness: the clean copy must be GREEN (positive control) and
a sentinel mutation that breaks the population pin must redden, or the run exits HARNESS DEAD. A mutation counts as
CAUGHT only when a named test FAILS (rc 1, >= 1 failed); a collection error (rc 2, nothing ran) is BROKEN.
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MOD = "tools/glossary_sense.py"
SPEC = "tools/staging/pla673_674_prep/glossary_match.json"
TEST = "tools/test_glossary_sense.py"


def spec_sub(old, new, n):
    """A spec edit expected to hit exactly n copies of its anchor (exclusions sit in both terms' lists)."""
    return (SPEC, old, new, n)


def mod_sub(old, new):
    return (MOD, old, new, 1)


MUTATIONS = {
    # exclusion families (each pattern appears in BOTH terms' identical lists: mutate every copy, n=2)
    "drop-hill-hardy": spec_sub('"pattern": "\\\\bHill\\\\s+Hardy\\\\b"', '"pattern": "\\\\bXHill\\\\s+Hardy\\\\b"', 2),
    "drop-madalene": spec_sub('"pattern": "\\\\bMadalene\\\\s+Hill\\\\b"', '"pattern": "\\\\bXMadalene\\\\b"', 2),
    "drop-hill-country": spec_sub('"pattern": "\\\\bhill\\\\s+country\\\\b"', '"pattern": "\\\\bXhill\\\\s+country\\\\b"', 2),
    "drop-beverly-hills": spec_sub('"pattern": "\\\\bBeverly\\\\s+Hills\\\\b"', '"pattern": "\\\\bXBeverly\\\\b"', 2),
    "drop-mediterranean": spec_sub('"pattern": "\\\\bMediterranean\\\\s+hills\\\\b"', '"pattern": "\\\\bXMed\\\\b"', 2),
    "drop-hawaii": spec_sub('"id": "hawaii-hills", "pattern": "', '"id": "hawaii-hills", "pattern": "XX', 2),
    "drop-strawberry-system": spec_sub('"id": "strawberry-hill-system", "pattern": "', '"id": "strawberry-hill-system", "pattern": "XX', 2),
    "drop-raspberry": spec_sub('"crops": ["raspberry"]', '"crops": ["no-such-crop"]', 2),
    "drop-d8-pepper": spec_sub('"crops": ["bell-pepper", "banana-pepper", "eggplant"]', '"crops": ["no-such-crop"]', 2),
    "d8-reason-changed": spec_sub('"why": "unsupported claim, re-author pending (part B2)"', '"why": "mound sense"', 2),
    # term scopes
    "potato-to-hill-scope": spec_sub('"crops": ["potato", ', '"crops": [', 1),
    "hill-scope-gains-pepper": spec_sub('"zucchini-courgette", "yellow-summer-squash"]', '"zucchini-courgette", "yellow-summer-squash", "bell-pepper"]', 1),
    "hilling-forms-lose-noun": spec_sub('"forms": ["hill", "hills", "hilled", "hilling"]', '"forms": ["hilled", "hilling"]', 1),
    "hilling-forms-lose-hilled": spec_sub('"forms": ["hill", "hills", "hilled", "hilling"]', '"forms": ["hill", "hills", "hilling"]', 1),
    # refuse_on families
    "hilling-refuse-per-hill": spec_sub('"\\\\bper\\\\s+hill\\\\b", ', '', 1),
    "hilling-refuse-in-hills": spec_sub('"\\\\bin\\\\s+hills\\\\b", ', '', 1),
    "hill-refuse-verb": spec_sub('"refuse_on": ["\\\\bhill(ed|ing)?\\\\s+(a\\\\s+little\\\\s+)?(soil|up|mulch)\\\\b", ', '"refuse_on": [', 1),
    # module logic
    "exclusion-after-term": mod_sub("        if ex:\n", "        if ex and spec['_owner'].get(crop) is None:\n"),
    "exclusion-ignores-crop-filter": mod_sub('        if e.get("crops") and crop not in e["crops"]:\n            continue\n', ''),
    "no-refuse-on-unclassified": mod_sub("    if refuse and unclassified:", "    if False and unclassified:"),
    "no-floor": mod_sub("    if len(rows) < floor:", "    if False:"),
    "consumer-filter-lets-vs-in": mod_sub('if not keys or keys[0] == "verification_status":', 'if not keys:'),
    "consumer-filter-lets-sources-in": mod_sub('if k == "sources" or ', 'if '),
    "structural-keys-inspected": mod_sub('STRUCTURAL = frozenset({"id", "stage_id", "tip_id", "arrangement", "action", "active_stages"})',
                                         'STRUCTURAL = frozenset()'),
    "noun-detector-off": mod_sub('return form.lower() == "hill" and', 'return False and'),
    "no-exclusion-divergence-check": mod_sub('        elif m[0]["exclusions"] != exclusions:', '        elif False:'),
    "no-matcher-shape-check": mod_sub('if not isinstance(m, list) or len(m) != 1 or set(m[0]) != MATCHER_KEYS:', 'if not isinstance(m, list):'),
}
SENTINEL = ("sentinel-population-pin", mod_sub("DEFAULT_FLOOR = 200", "DEFAULT_FLOOR = 100000"))


def scratch():
    d = tempfile.mkdtemp(prefix="mut_glossary_")
    os.makedirs(os.path.join(d, "tools", "staging", "pla673_674_prep"))
    for f in (MOD, SPEC, TEST):
        shutil.copy(os.path.join(ROOT, f), os.path.join(d, f))
    os.symlink(os.path.join(ROOT, "crops_data_final.json"), os.path.join(d, "crops_data_final.json"))
    return d


def run(d):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", os.path.join(d, TEST)],
                       cwd=d, capture_output=True, text=True)
    m = re.search(r"(\d+) passed", p.stdout)
    f = re.search(r"(\d+) failed", p.stdout)
    return p.returncode, int(m.group(1)) if m else 0, int(f.group(1)) if f else 0, p.stdout[-300:]


def apply(d, mut):
    f, old, new, n = mut
    p = os.path.join(d, f)
    src = open(p, encoding="utf-8").read()
    if src.count(old) != n:
        raise SystemExit(f"HARNESS DEAD: anchor for {f} found {src.count(old)} times, expected {n}: {old[:70]!r}")
    out = src.replace(old, new)
    assert out != src
    open(p, "w", encoding="utf-8").write(out)
    print("    MUTATION-APPLIED")


def main():
    d = scratch()
    rc, passed, failed, tail = run(d)
    if rc != 0 or failed or passed < 60:
        raise SystemExit(f"HARNESS DEAD: positive control not green (rc {rc}, {passed} passed, {failed} failed)\n{tail}")
    print(f"positive control: clean copy GREEN ({passed} passed)")
    shutil.rmtree(d)
    caught, survived = [], []
    for name, mut in [SENTINEL] + list(MUTATIONS.items()):
        d = scratch()
        print(name)
        apply(d, mut)
        rc, passed, failed, tail = run(d)
        shutil.rmtree(d)
        red = rc == 1 and failed > 0  # a collection error (rc 2, nothing ran) is BROKEN, never a catch
        verdict = "CAUGHT" if red else ("BROKEN" if rc not in (0, 1) else "SURVIVED")
        print(f"    rc {rc}: {failed} failed, {passed} passed -> {verdict}")
        if name == SENTINEL[0] and not red:
            raise SystemExit("HARNESS DEAD: the sentinel did not redden")
        (caught if red else survived).append(name)
    print(f"\n{len(caught)}/{len(caught) + len(survived)} caught (incl. sentinel), {len(survived)} survived: {survived}")
    if survived:
        raise SystemExit(1)


main()
