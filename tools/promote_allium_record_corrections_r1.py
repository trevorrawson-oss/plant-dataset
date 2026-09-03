#!/usr/bin/env python3
"""ALLIUM RECORD CORRECTIONS, ROUND 1. Base 3e408f58.

Three corrections the batch-24 source-truth pass established, each a claim that is WRONG rather
than merely uncited. Every quotation below was read first-hand this session.

1. SHALLOT / DOWNY MILDEW -- "tolerant varieties" sends the reader after something that does not
   exist. The PNW Plant Disease Management Handbook states flatly: "There are no resistant
   varieties." UC IPM's only named resistant cultivars are a few RED ONIONS ("for example, Calred")
   whose resistance "is active only in the flower stalks and not the leaves" -- the leaves being
   where a gardener sees the disease. The word "tolerant" appears in none of the five allium downy
   mildew documents read, and no resistant or tolerant SHALLOT is documented anywhere.
   The claim comes out, and two controls PNW gives that the record was missing go in: hold nitrogen
   back ("Avoid over-application of nitrogen as an overproduction of succulent leaves promotes
   disease") and eradicate volunteers ("Eradicate volunteer or wild Allium spp."). PNW also fixes
   the rotation figure: "Practice a 3-year or longer crop rotation if possible."

2. SHALLOT / WHITE ROT -- "20 to 30 years" is a FABRICATED figure. Six extension documents were
   read; they give 15+ (UMass), over 20 (UC IPM, twice), 20-40 (UMD, UMaine) and up to 40. **None
   says 20 to 30**, including both URLs cited for it. A web search SUMMARY asserts "20 to 30 years",
   which is the likely route in -- the same failure mode that put a sentence NC State never wrote
   into catalog round 10. Converges on UC IPM's exact published wording, "over 20 years", which is
   what leek already carries: one organism, one figure, one citation.

3. LEEK / RUST -- the entry is a UK picture wearing a US citation. Severity **high** while garlic
   rust ships **low** and chives rust carries none; "mid-summer into late autumn" and "damp, humid"
   while UC IPM says the pathogen "is active during cool weather conditions, between 57º and 75ºF"
   with the optimum "around 59ºF"; and a variety recommendation built from RHS's "Suppliers
   sometimes claim a degree of resistance", which is a marketing claim, not a finding. US evidence
   runs the other way on susceptibility -- UC IPM: "Leek, elephant garlic, and shallot are more
   resistant"; UMaine: "Leeks, shallots, and elephant garlic have not been found to be susceptible
   to rust strains present in North America" -- and the New England Vegetable Management Guide does
   not list rust among leek's diseases at all. The cited UF/IFAS leek guide contributes nothing: its
   entire rust content is that leek hosts rust and that undersowing with subterranean clover reduced
   incidence, advice the record does not carry.
   Severity drops to low, the weather framing inverts, the variety recommendation goes, "bin" (a
   British verb, hard rule) goes, and two controls both US sources name go IN: destroy volunteer
   alliums, and a 2-to-3-year rotation off infected ground. The entry ends up MORE useful, not less.
   Sources move from RHS + UF/IFAS to UC IPM + the PNW handbook, which between them support
   crowding, nitrogen and leaf wetness -- the three conditions RHS was carrying alone.

LIVENESS NOTE: `pnwhandbooks.org` returns 403 to an ordinary fetch, including this session's. It is
NOT dead; it reads through a text-extraction proxy. Anyone re-verifying `osu_ext` here with a naive
fetch will wrongly call it a dead URL. The dataset already cites this handbook on beet and chard.

SCOPE: 9 prose fields, 2 severity values, 2 source sets, across 3 problems on 2 crops. No rung, no
id, no type, no catalog, no other crop.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "3e408f5886f3f78dec3583bd0faa6c1f7c3b481c20039941112719193dc419ee"
VERIFIED = "2026-09-03"

TARGETS = (("shallot", "Downy mildew"), ("shallot", "White rot"), ("leek", "Leek rust"))

PROSE = {
 ("shallot", "Downy mildew", "management_beginner"): (
  "Give the plants room for air to move, water at the base so the leaves stay dry, rotate where you "
  "plant, and clear away sick leaves. Pick tolerant varieties if this is a regular problem for you.",
  "Give the plants room for air to move, water at the base so the leaves stay dry, and rotate where "
  "you plant. Clear away sick leaves and pull out any volunteer onions nearby, since they carry the "
  "disease over. Go easy on nitrogen, because soft, sappy growth suits it. There is no resistant "
  "variety to fall back on, so the growing conditions are the whole of the defense."),
 ("shallot", "Downy mildew", "management_seasoned"): (
  "Space for airflow, water at the base to keep foliage dry, rotate away from alliums, and remove "
  "infected debris; choose tolerant varieties where downy mildew is a recurring problem.",
  "Space for airflow, water at the base to keep foliage dry, and rotate away from alliums for three "
  "years or longer where the disease has occurred. Destroy infected debris, cull piles and volunteer "
  "alliums, and hold nitrogen back, since an overproduction of succulent leaves promotes it. No "
  "resistant variety is available, so every lever here is a growing-conditions one."),
 ("shallot", "White rot", "cause_seasoned"): (
  "A soilborne fungus (Sclerotium cepivorum) that attacks only alliums and favors cool, moist soil. "
  "Its sclerotia survive in the ground for 20 to 30 years, so once a bed is infested it stays "
  "infested.",
  "A soilborne fungus (Sclerotium cepivorum) that attacks only alliums and favors cool, moist soil. "
  "Its sclerotia survive in the ground for over 20 years, so once a bed is infested it stays "
  "infested."),
 ("leek", "Leek rust", "identification_beginner"): (
  "Bright orange spots and dusty pustules on the leaves, mostly from mid-summer into fall. Bad cases "
  "brown and shrivel the leaves.",
  "Bright orange spots and dusty bumps on the leaves, showing up in cool, damp stretches rather than "
  "in summer heat. A bad case browns and shrivels the older leaves. Leeks carry it better than "
  "garlic does, so it is usually a nuisance rather than a threat to the crop."),
 ("leek", "Leek rust", "identification_seasoned"): (
  "Bright orange pustules scattered on both leaf surfaces that break open to a dusty spore powder; "
  "severe infection shrivels leaves early and saps vigor, common from mid-summer into late autumn.",
  "Bright orange pustules scattered on the leaf surfaces, breaking open to a dusty spore powder; "
  "heavy infection yellows and shrivels older leaves and costs the plant growing time. Infection "
  "runs on cool conditions, roughly 57 to 75°F with the optimum near 59°F and several hours of leaf "
  "wetness, so it tracks cool damp spring and fall weather rather than midsummer. Leek is a host but "
  "a comparatively resistant one, less affected than garlic."),
 ("leek", "Leek rust", "management_beginner"): (
  "Give plants room so air moves between them, do not over-feed with nitrogen, pull off and bin "
  "badly spotted leaves, and clear away old leaves after harvest. Pick rust-tolerant varieties if "
  "you can.",
  "Give plants room so air moves between them and the leaves dry, go easy on nitrogen, and water at "
  "the soil line instead of over the tops. Pull out any volunteer onions or garlic nearby, since "
  "they carry the fungus over, and clear the old leaves out of the bed after harvest."),
 ("leek", "Leek rust", "management_seasoned"): (
  "Space plants for airflow, avoid excess nitrogen, balance feeding, remove and destroy badly "
  "infected leaves and post-harvest debris, and choose more rust-tolerant varieties where available.",
  "Space for airflow so foliage dries, hold nitrogen back, and irrigate at the soil line rather than "
  "over the leaves. Destroy volunteer alliums, and where rust has been a problem keep new allium "
  "plantings two to three years off that ground and separated from an infected planting. Clear crop "
  "debris at the end of the season. On leek the cultural steps usually carry it."),
 ("leek", "Leek rust", "cause_beginner"): (
  "A fungus that causes orange rust. It spreads in damp, humid weather and is worse when plants are "
  "crowded or pushed with too much nitrogen.",
  "A rust fungus. It gets going in cool, damp weather when the leaves stay wet, and it is worse "
  "where plants are crowded or pushed hard with nitrogen. Volunteer onions and garlic left in the "
  "ground carry it from one season to the next."),
 ("leek", "Leek rust", "cause_seasoned"): (
  "The fungus Puccinia porri (formerly P. allii); it is worse on crowded plants, in humid weather, "
  "and on nitrogen-rich, low-potassium soils.",
  "The rust fungus Puccinia porri (formerly P. allii). Cool temperatures and extended leaf wetness "
  "drive infection, and dense stands and heavy nitrogen both increase it. Spores travel on air, and "
  "volunteer alliums left in the ground carry the fungus between crops."),
}
SEVERITY = {("leek", "Leek rust"): ("high", "low")}
SOURCES = {
 ("shallot", "Downy mildew"): (
   ["usu_ext"], ["usu_ext", "osu_ext"],
   {"osu_ext": "https://pnwhandbooks.org/plantdisease/host-disease/onion-allium-cepa-downy-mildew"}),
 ("shallot", "White rot"): (
   ["umass_ext", "umd_ext"], ["umass_ext", "umd_ext", "uc_ipm"],
   {"uc_ipm": "https://ipm.ucanr.edu/agriculture/onion-and-garlic/white-rot/"}),
 ("leek", "Leek rust"): (
   ["rhs", "uf_ifas"], ["uc_ipm", "osu_ext"],
   {"uc_ipm": "https://ipm.ucanr.edu/agriculture/onion-and-garlic/rust/",
    "osu_ext": "https://pnwhandbooks.org/plantdisease/host-disease/garlic-allium-sativum-rust"}),
}
EXPECTED_PROSE = 9
EXPECTED_SEVERITY = 1
EXPECTED_SOURCE_SETS = 3

_VARIETY = re.compile(r"(?:rust[- ])?(?:tolerant|resistant)[- ]?variet(?:y|ies)", re.I)
_NEGATED = re.compile(r"\b(?:no|not|none|never|without|lack\w*)\b[^.]{0,60}$", re.I)


def recommends_a_variety(text):
    """TRUE only where the text RECOMMENDS choosing a tolerant or resistant variety.

    Naming one in order to say there is NONE is the opposite claim and must pass: PNW states
    outright "There are no resistant varieties", and telling the reader so is useful. An earlier
    version of this guard pattern-matched the words and refused this promote's own replacement
    text, which is a guard rejecting correct input -- as much a defect as one accepting bad input.
    """
    for m in _VARIETY.finditer(text or ""):
        if not _NEGATED.search(text[:m.start()]):
            return True
    return False


# Claims that must be GONE afterward, checked on the WHOLE target problem, not just the edited
# field. A correction that edits one register and leaves the claim standing in its sibling has
# moved the defect rather than fixed it.
RETIRED = (
 (("shallot", "Downy mildew"), recommends_a_variety,
  "a tolerant/resistant variety recommendation"),
 (("shallot", "White rot"), lambda t: bool(re.search(r"20\s*(?:to|-)\s*30", t or "")),
  "the fabricated 20-to-30-year figure"),
 (("leek", "Leek rust"), lambda t: bool(re.search(r"\bbin\b", t or "", re.I)),
  "the British verb 'bin'"),
 (("leek", "Leek rust"), recommends_a_variety, "the variety recommendation RHS never made"),
 (("leek", "Leek rust"),
  lambda t: bool(re.search(r"mid-summer|late autumn|\bautumn\b", t or "", re.I)),
  "the UK seasonal framing"),
)
BRITISH = (r"\bbin\b", r"colour", r"fortnight", r"whilst", r"\bautumn\b", r"mould", r"practise",
           r"favour", r"sulphur")
ABSOLUTES = ("always", "never", "completely", "totally", "harmless", "guaranteed", "eliminate",
             "eliminates")


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    return [p for f in ("pests", "diseases") for p in crop.get(f) or []]


def find_problem(data, slug, name):
    c = by_slug(data).get(slug)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % slug)
    hits = [p for p in problems(c) if p.get("name") == name]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %s has %d problems named %r, expected exactly 1"
                         % (slug, len(hits), name))
    return hits[0]


def snapshot(data):
    snap = {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + (str(k),))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + ("[%d]" % i,))
        else:
            snap[path] = node
    walk(data, ())
    return snap


def hygiene(s):
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    for w in ABSOLUTES:
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    for pat in BRITISH:
        if re.search(pat, s, re.I):
            bad.append("british:%s" % pat)
    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):
        bad.append("ladder vocabulary")
    if re.search(r"\d\s+°F", s):
        bad.append("spaced degF")
    return bad


# ------------------------------------------------------------------ guards
def check_pins(data):
    if len(PROSE) != EXPECTED_PROSE or len(SEVERITY) != EXPECTED_SEVERITY \
            or len(SOURCES) != EXPECTED_SOURCE_SETS:
        raise SystemExit("REFUSED: edit tables hold %d/%d/%d, expected %d/%d/%d"
                         % (len(PROSE), len(SEVERITY), len(SOURCES),
                            EXPECTED_PROSE, EXPECTED_SEVERITY, EXPECTED_SOURCE_SETS))
    for key in list(PROSE) + [k + ("",) for k in SEVERITY] + [k + ("",) for k in SOURCES]:
        if (key[0], key[1]) not in TARGETS:
            raise SystemExit("REFUSED: %s/%s is not a declared target" % (key[0], key[1]))
    for (slug, name, field), (before, after) in sorted(PROSE.items()):
        p = find_problem(data, slug, name)
        if p.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s does not match its pinned text; the record moved"
                             % (slug, name, field))
        if after == before:
            raise SystemExit("REFUSED: %s/%s/%s replacement is identical" % (slug, name, field))
        bad = hygiene(after)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s replacement: %s" % (slug, name, field,
                                                                    ", ".join(bad)))
    for (slug, name), (before, after) in sorted(SEVERITY.items()):
        got = find_problem(data, slug, name).get("severity")
        if got != before:
            raise SystemExit("REFUSED: %s/%s severity is %r, pinned %r" % (slug, name, got, before))
        if after not in ("low", "medium", "high"):
            raise SystemExit("REFUSED: %s/%s new severity %r is not a known value"
                             % (slug, name, after))
    for (slug, name), (before, after, anchors) in sorted(SOURCES.items()):
        p = find_problem(data, slug, name)
        if p.get("sources") != before:
            raise SystemExit("REFUSED: %s/%s sources are %r, pinned %r"
                             % (slug, name, p.get("sources"), before))
        if sorted(set(after)) != sorted(after) or not after:
            raise SystemExit("REFUSED: %s/%s new source list is empty or has duplicates"
                             % (slug, name))
        for sid in after:
            if sid not in data["source_catalog"]:
                raise SystemExit("REFUSED: %s/%s cites %r, which is not in source_catalog"
                                 % (slug, name, sid))
        for sid in anchors:
            if sid not in after:
                raise SystemExit("REFUSED: %s/%s anchors %r which is not in its new source list"
                                 % (slug, name, sid))


def check_retired_claims(data):
    """The claims must be gone from the WHOLE problem, not just the field that carried them. A
    correction that edits one register and leaves the claim standing in its sibling has moved the
    defect rather than fixed it."""
    left = []
    for (slug, name), still_present, label in RETIRED:
        p = find_problem(data, slug, name)
        for k, v in p.items():
            if isinstance(v, str) and still_present(v):
                left.append("%s/%s/%s still carries %s" % (slug, name, k, label))
    if left:
        raise SystemExit("REFUSED: %r" % left)
    return len(RETIRED)


def check_sources_retired(data):
    """RHS and the UF/IFAS leek guide must no longer be cited for leek rust, in `sources` or in
    `anchoring_urls`. Dropping one and leaving the other is the shape that keeps a dead citation
    alive."""
    p = find_problem(data, "leek", "Leek rust")
    stale = [s for s in ("rhs", "uf_ifas")
             if s in (p.get("sources") or []) or s in (p.get("anchoring_urls") or {})]
    if stale:
        raise SystemExit("REFUSED: leek/Leek rust still cites %r" % stale)


def apply_to(data):
    check_pins(data)
    for (slug, name, field), (_b, after) in PROSE.items():
        find_problem(data, slug, name)[field] = after
    for (slug, name), (_b, after) in SEVERITY.items():
        find_problem(data, slug, name)["severity"] = after
    for (slug, name), (_b, after, anchors) in SOURCES.items():
        p = find_problem(data, slug, name)
        p["sources"] = list(after)
        au = {k: v for k, v in (p.get("anchoring_urls") or {}).items() if k in after}
        for sid, url in anchors.items():
            au[sid] = {"url": url, "verified": VERIFIED}
        p["anchoring_urls"] = {k: au[k] for k in after if k in au}
    return data


def verify_post(pre, data):
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    want_owners = {(s, n) for s, n in TARGETS}

    def owner(k):
        """The (crop, problem name) a leaf path belongs to, or None."""
        if len(k) < 4 or k[0] != "crops" or k[2] not in ("pests", "diseases"):
            return None
        try:
            crop = data["crops"][int(k[1][1:-1])]
            return crop["slug"], crop[k[2]][int(k[3][1:-1])].get("name")
        except (ValueError, IndexError, KeyError):
            return None

    # `sources` is a LIST, so growing it adds path keys, and `anchoring_urls` gains a member. Both
    # are legitimate here; nothing else is. An earlier version allowed only anchoring_urls and the
    # promote refused itself on the source list.
    for k in added | dropped:
        if "anchoring_urls" not in k and "sources" not in k:
            raise SystemExit("REFUSED: a key was added or dropped outside sources/anchoring_urls: "
                             "%r" % (k,))
        if owner(k) not in want_owners:
            raise SystemExit("REFUSED: a key was added or dropped outside the declared targets: "
                             "%r" % (k,))
    changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
    n_prose = sum(1 for k in changed if k[-1] in {f for _s, _n, f in PROSE})
    if n_prose != EXPECTED_PROSE:
        raise SystemExit("REFUSED: %d prose leaves changed, expected %d" % (n_prose, EXPECTED_PROSE))
    for (slug, name, field), (_b, after) in PROSE.items():
        if find_problem(data, slug, name).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s did not receive its replacement"
                             % (slug, name, field))
    for (slug, name), (_b, after) in SEVERITY.items():
        if find_problem(data, slug, name).get("severity") != after:
            raise SystemExit("REFUSED: %s/%s severity was not set to %r" % (slug, name, after))
    for (slug, name), (_b, after, _a) in SOURCES.items():
        p = find_problem(data, slug, name)
        if p.get("sources") != list(after):
            raise SystemExit("REFUSED: %s/%s sources are %r, expected %r"
                             % (slug, name, p.get("sources"), list(after)))
        if list(p.get("anchoring_urls") or {}) != list(after):
            raise SystemExit("REFUSED: %s/%s anchoring_urls keys %r do not match its sources %r"
                             % (slug, name, list(p.get("anchoring_urls") or {}), list(after)))
    # NOTHING outside the three target problems may move.
    touched = {owner(k) for k in changed}
    if touched - want_owners:
        raise SystemExit("REFUSED: leaves changed outside the declared targets: %r"
                         % sorted(touched - want_owners))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; every id cited here already exists")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    pre = snapshot(data)
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data)
    check_catalog_untouched(before_cm, before_sc, data)
    retired = check_retired_claims(data)
    check_sources_retired(data)

    blob = serialize(data)
    print("leaves changed      : %d (%d prose, %d severity, %d source sets)"
          % (n, EXPECTED_PROSE, EXPECTED_SEVERITY, EXPECTED_SOURCE_SETS))
    print("retired claims gone : %d/%d" % (retired, len(RETIRED)))
    print("leek rust severity  : high -> low")
    print("base  SHA           : %s" % sha)
    print("post  SHA           : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
