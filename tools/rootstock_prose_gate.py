#!/usr/bin/env python3
"""rootstock_prose_gate -- PLA-608 Part 2: a rootstock NAMED in prose must be a row in that crop's own list.

THE RULE (PLA-608, ruled 2026-09-25; built in the citrus/rootstock pass stop 1, PLA-625 ruling 2026-10-09). On every crop
carrying a `rootstock_options` field, a rootstock named in
  * `recommended_rootstock_note`,
  * any row's `traits_seasoned`, `traits_beginner` or `what_to_ask_nursery`, or
  * any string leaf of `container_notes` (added by the stop-1 ruling: PLA-626's close-out found plum's two
    "St. Julien or Marianna" container strings OUTSIDE Part 1's table, so this class went unseen once already)
must resolve to a row of that crop's `rootstock_options`. If it does not, the gate fails, by name.
`recommended_rootstock` itself is NOT read: a rule that it must equal a row name belongs to PLA-589 and is HELD until each
recommendation is T1-verified (stop-1 ruling). Region cells, varieties and every other field are out of scope.

NAME RESOLUTION (the table below; PLA-608's synonym and family relations).
  * STOCKS: one id per rootstock, with every spelling that names it (synonyms: same stock). A ROW's name is read with
    the same matcher, so a row "Carrizo / Swingle citrumelo (trifoliate hybrids)" holds carrizo AND swingle.
  * FAMILIES: a family TERM in prose ("trifoliate types", "a Gisela", "OHxF") resolves if ANY member is a row, or if a
    row's own name carries the term. A MEMBER named in prose resolves only to itself.
  * SELECTION_OF: a species stock named in prose also resolves when a row holds a named selection of it (Flying Dragon
    is a selection of trifoliate orange, so "a dwarfing selection of trifoliate orange" on a Flying Dragon row resolves).
    It is one-way: Flying Dragon named on a crop whose only trifoliate row is the species FAILS.
  * OWN ROOT: an authored EMPTY list (`[]`) is the own-root statement (PLA-464), so "own roots" / "ungrafted" /
    "from cuttings" resolve there. On a crop that HAS rows, own-root prose must resolve to an own-root row.
  * NOT_ROOTSTOCKS: cultivar names that sit in rootstock prose (cherry-sour's North Star and Meteor, PLA-608's second
    handling case) are listed so they are never read as stocks. Decided at build time over a waiver (the ticket's
    preference): a cultivar is never a rootstock, so no sentence should carry a waiver for it.
  * Overlaps resolve longest-match-first, so "Swingle citrumelo" is one name, not swingle + the citrumelo family.

STATED LIMIT, printed on every run: names on no list pass silently. The gate cannot see a rootstock its table does not
know; a new row name in the data is NOT automatically a known name (test_rootstock_prose_gate pins every row name in
the live data to a table entry, so adding a row with an unknown name fails there).

WAIVERS: identity AND character. Each entry in rootstock_prose_gate_known.py is keyed on crop + field + name + the
exact SENTENCE carrying the name, with its ticket and a one-line reason. The sentence is the character: a waived name
whose sentence is reworded (pear-asian's "not an option" wording removed) no longer matches, so the name FAILS and the
waiver reports STALE. A waiver that stops firing is reported STALE and fails the run, never left as standing
permission.

POPULATION (derived, never fixed). Inspected = every crop with a `rootstock_options` key, counted from the data. The
gate REFUSES on zero, on any crop of the measured population (KNOWN_POPULATION, 21 on 5420479d) that has lost the
field (identity, so a strip-one-add-one swap cannot hold the count), and if it inspected fewer crops than carry the
field. A crop that GAINS the field is inspected (the floor moves with the data) and reported as new.

Usage: rootstock_prose_gate.py [PATH]      exit 1 on a violation or STALE waiver, 2 on a refused population
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rootstock_prose_gate_known as _K  # noqa: E402  -- the measured waiver ledger and population

LIMIT_LINE = "stated limit: names on no list pass silently (the gate sees only rootstocks its table knows)"

# ---------------------------------------------------------------- THE TABLE
# Built from every rootstock_options row name in canonical's history (414 commits touching crops_data_final.json on
# e449afd: 51 distinct names) plus the outside stocks the rootstock prose and the cited UF/IFAS pages name.
# Patterns are regexes; (?-i:...) marks a case-sensitive name that is also an ordinary English word.
STOCKS = {
    # citrus
    "sour_orange": [r"sour[- ]orange", r"Citrus\s+aurantium", r"C\.\s*aurantium"],
    "trifoliate_orange": [r"trifoliate[- ]orange", r"Poncirus\s+trifoliata", r"Citrus\s+trifoliata",
                          r"C\.\s*trifoliata", r"(?-i:Rubidoux)"],
    "flying_dragon": [r"Flying\s+Dragon(?:\s+trifoliate)?"],
    "carrizo": [r"Carrizo(?:\s+citrange)?"],
    "swingle": [r"Swingle(?:\s+citrumelo)?"],
    "rough_lemon": [r"rough\s+lemon", r"Citrus\s+jambh[iu]ri", r"C\.\s*jambh[iu]ri"],
    "volkamer": [r"Volkamer(?:\s+lemon)?", r"(?:Citrus|C\.)\s*volkameriana", r"volkameriana"],
    "alemow": [r"alem[eo]?ow", r"(?:Citrus|C\.)\s*macrophylla", r"macrophylla"],
    "rangpur": [r"Rangpur(?:\s+lime)?", r"(?:Citrus|C\.)\s*limonia"],
    "cleopatra": [r"Cleopatra(?:\s+mandarin)?"],
    # stone fruit
    "myrobalan": [r"Myrobalan(?:\s+29C)?", r"(?:Prunus|P\.)\s*cerasifera"],
    "marianna_2624": [r"Marianna\s+2624"],
    "st_julien": [r"St\.?\s+Julien(?:\s+A)?", r"(?:Prunus|P\.)\s*insititia"],
    "citation": [r"(?-i:Citation)", r"P\.\s*salicina\s*x\s*P\.\s*persica"],
    "lovell": [r"Lovell"],
    "halford": [r"Halford"],
    "guardian": [r"(?-i:Guardian)"],
    "nemaguard": [r"Nemaguard"],
    "apricot_seedling": [r"apricot\s+seedlings?"],
    "mazzard": [r"Mazzard", r"(?:Prunus|P\.)\s*avium"],
    "mahaleb": [r"Mahaleb"],
    "colt": [r"(?-i:Colt)"],
    "gisela_5": [r"Gisela\s*5"],
    "gisela_6": [r"Gisela\s*6"],
    # pome fruit
    "m9": [r"(?-i:M\.?\s?9)\b"],
    "m26": [r"(?-i:M\.?\s?26)\b"],
    "m27": [r"(?-i:M\.?\s?27)\b"],
    "m7": [r"(?-i:M\.?\s?7)\b"],
    "mm106": [r"(?-i:MM\.?\s?106)\b"],
    "mm111": [r"(?-i:MM\.?\s?111)\b"],
    "ohxf_87": [r"OHxF\s*87"],
    "ohxf_97": [r"OHxF\s*97"],
    "ohxf_333": [r"OHxF\s*333"],
    "quince": [r"(?:Provence\s+)?quince(?:\s+(?-i:[AC]))?\b"],
    "pear_seedling": [r"(?-i:Bartlett)\s*/\s*(?-i:Winter\s+Nelis)\s+seedlings?", r"(?-i:Bartlett)\s+seedlings?",
                      r"(?-i:Winter\s+Nelis)\s+seedlings?"],
    "betulifolia": [r"(?:Pyrus\s+|P\.\s*)?betul(?:i|ae)folia"],
    "calleryana": [r"(?:Pyrus\s+|P\.\s*)?calleryana"],
    # other trees
    "kaki_seedling": [r"(?:Diospyros|D\.)\s*kaki(?:\s*\(?seedlings?\)?)?", r"kaki\s+seedlings?"],
    "date_plum": [r"(?:Diospyros|D\.)\s*lotus", r"date-plum"],
    "american_persimmon": [r"(?:Diospyros|D\.)\s*virginiana", r"American\s+persimmon"],
    "morus_seedling": [r"Morus\s+(?:alba\s+|rubra\s+)?seedlings?(?:\s*\((?:alba|rubra)(?:\s+or\s+(?:alba|rubra))?\))?",
                       r"(?:Morus|M\.)\s*(?:alba|rubra)\s+seedlings?",
                       r"seedlings?\s+(?:of\s+)?(?:Morus|M\.)\s*(?:alba|rubra)(?:\s+or\s+(?:alba|rubra))?"],
    "pawpaw_seedling": [r"pawpaw\s+seedlings?(?:\s*\(grafted\))?", r"Asimina(?:\s+triloba)?\s+seedlings?"],
    "apple_seedling": [r"apple\s+seedlings?"],
    "own_root": [r"own[- ]roots?(?:ed)?", r"own-rooted", r"ungrafted", r"cutting-grown",
                 r"from\s+(?:hardwood\s+)?cuttings?"],
    "genetic_dwarf": [r"genetic\s+dwarfs?"],
}
# family -> (terms that name the family itself, members). A member named in prose resolves only to itself.
FAMILIES = {
    "trifoliate": ([r"trifoliate(?:\s+(?:types?|selections?|stocks?|rootstocks?))?", r"Poncirus"],
                   {"trifoliate_orange", "flying_dragon"}),
    "trifoliate_hybrid": ([r"trifoliate(?:[- ]orange)?[- ]hybrids?", r"citranges?", r"citrumelos?"],
                          {"carrizo", "swingle"}),
    "peach_seedling": ([r"peach\s+seedlings?(?:\s+(?:stocks?|rootstocks?))?"],
                       {"lovell", "halford", "guardian", "nemaguard"}),
    "marianna": ([r"Marianna"], {"marianna_2624"}),
    "gisela": ([r"Gisela"], {"gisela_5", "gisela_6"}),
    "malling": ([r"Malling", r"(?-i:M)-series", r"(?-i:MM)-series"], {"m9", "m26", "m27", "m7", "mm106", "mm111"}),
    "ohxf": ([r"OHxF", r"Old\s+Home\s*(?:x|×)\s*Farmingdale"], {"ohxf_87", "ohxf_97", "ohxf_333"}),
}
SELECTION_OF = {"flying_dragon": "trifoliate_orange"}
# A row whose WHOLE name is one of these is read as that stock (apple's row is named just "seedling"; a bare "seedling"
# in prose is not a stock name, so it is not in STOCKS).
ROW_NAME_ALIASES = {"seedling": "apple_seedling"}
# An authored EMPTY list is the own-root statement (PLA-464: fig, pomegranate, avocado and olive carry `[]`, own-root
# by design), so own-root prose resolves there. On a crop WITH rows, own-root prose must resolve to an own-root row.
OWN_ROOT = "own_root"
NOT_ROOTSTOCKS = [r"(?-i:North\s+Star)", r"(?-i:Meteor)"]   # cherry-sour cultivars named in its rootstock prose

ROW_FIELDS = ("traits_seasoned", "traits_beginner", "what_to_ask_nursery")
NOTE_FIELD = "recommended_rootstock_note"
CITE = re.compile(r"(^sources$|^anchoring_urls$|_sources$|_anchoring_urls$|provenance)")
SENT = re.compile(r"(?<=[.!?])\s+(?=[\"'(A-Z0-9])")


def _compile():
    pats = []   # (regex, kind, id)
    for sid, ps in STOCKS.items():
        pats += [(re.compile(rf"\b(?:{p})", re.I), "stock", sid) for p in ps]
    for fid, (terms, _m) in FAMILIES.items():
        pats += [(re.compile(rf"\b(?:{p})", re.I), "family", fid) for p in terms]
    pats += [(re.compile(rf"\b(?:{p})\b", re.I), "cultivar", None) for p in NOT_ROOTSTOCKS]
    return pats


PATTERNS = _compile()


def names_in(text):
    """[(start, end, kind, id, matched)] non-overlapping, longest match first."""
    if not isinstance(text, str):
        return []
    cands = []
    for rx, kind, nid in PATTERNS:
        for m in rx.finditer(text):
            if m.end() > m.start():
                cands.append((m.start(), m.end(), kind, nid, m.group(0)))
    cands.sort(key=lambda c: (-(c[1] - c[0]), c[0]))
    taken, out = [], []
    for c in cands:
        if any(c[0] < e and s < c[1] for s, e in taken):
            continue
        taken.append((c[0], c[1]))
        out.append(c)
    return sorted(out)


def sentence_at(text, pos):
    start = 0
    for m in SENT.finditer(text):
        if m.start() >= pos:
            return text[start:m.start()].strip()
        start = m.end()
    return text[start:].strip()


def row_index(crop):
    """(stocks held by the crop's rows, family terms carried in row names)."""
    stocks, fams = set(), set()
    rows = crop.get("rootstock_options")
    if rows == []:
        stocks.add(OWN_ROOT)
    for r in rows or []:
        n = r.get("name") if isinstance(r, dict) else None
        if isinstance(n, str) and n.strip().lower() in ROW_NAME_ALIASES:
            stocks.add(ROW_NAME_ALIASES[n.strip().lower()])
        for _s, _e, kind, nid, _t in names_in(n):
            if kind == "stock":
                stocks.add(nid)
            elif kind == "family":
                fams.add(nid)
    return stocks, fams


def resolves(kind, nid, stocks, fams):
    if kind == "stock":
        return nid in stocks or any(SELECTION_OF.get(s) == nid for s in stocks)
    if kind == "family":
        return nid in fams or bool(FAMILIES[nid][1] & stocks)
    return True


def _leaves(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            if CITE.search(k):
                continue
            yield from _leaves(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _leaves(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def fields(crop):
    """[(field identity, text)] -- every string the rule reads on this crop."""
    out = []
    if isinstance(crop.get(NOTE_FIELD), str):
        out.append((NOTE_FIELD, crop[NOTE_FIELD]))
    for i, r in enumerate(crop.get("rootstock_options") or []):
        if not isinstance(r, dict):
            continue
        label = f"rootstock_options[name={r.get('name')}]" if r.get("name") else f"rootstock_options[{i}]"
        for f in ROW_FIELDS:
            if isinstance(r.get(f), str):
                out.append((f"{label}.{f}", r[f]))
    out += list(_leaves(crop.get("container_notes"), "container_notes"))
    return out


def scan_crop(crop):
    """(mentions, fields_inspected). mention = dict(crop, field, name, kind, id, sentence, resolved)."""
    stocks, fams = row_index(crop)
    fl = fields(crop)
    ms = []
    for field, text in fl:
        for s, _e, kind, nid, t in names_in(text):
            if kind == "cultivar":
                continue
            ms.append({"crop": crop.get("slug"), "field": field, "name": t, "kind": kind, "id": nid,
                       "sentence": sentence_at(text, s), "resolved": resolves(kind, nid, stocks, fams)})
    return ms, len(fl)


def waiver_key(m):
    return (m["crop"], m["field"], m["name"], m["sentence"])


KNOWN = {(w["crop"], w["field"], w["name"], w["sentence"]): w for w in _K.WAIVERS}
KNOWN_POPULATION = frozenset(_K.POPULATION)


def has_field(crop):
    return "rootstock_options" in crop


def crop_violations(crop, known=None):
    """Per-crop half (whole_crop_gate A64): unresolved, unwaived names on this crop. No-op without the field."""
    if not has_field(crop):
        return []
    known = KNOWN if known is None else known
    ms, _n = scan_crop(crop)
    return [f"{m['crop']} {m['field']}: names '{m['name']}' ({m['kind']} {m['id']}), which resolves to no row of "
            f"its rootstock_options. Add the row (sourced) or rephrase the prose; a waiver is keyed on the exact "
            f"sentence: \"{m['sentence']}\""
            for m in ms if not m["resolved"] and waiver_key(m) not in known]


def roster(data, known=None):
    """dict(carrying, inspected, fields, mentions, matched, unresolved, violations, stale, new_crops, lost_crops)."""
    known = KNOWN if known is None else known
    crops = data.get("crops", []) if isinstance(data, dict) else []
    carrying = [c for c in crops if has_field(c)]
    inspected, nfields, mentions, V = 0, 0, [], []
    for c in carrying:
        ms, n = scan_crop(c)
        inspected += 1
        nfields += n
        mentions += ms
        V += crop_violations(c, known)
    fired = {waiver_key(m) for m in mentions if not m["resolved"]}
    stale = sorted(k for k in known if k not in fired)
    slugs = {c.get("slug") for c in carrying}
    return {"carrying": len(carrying), "inspected": inspected, "fields": nfields, "mentions": len(mentions),
            "matched": sum(1 for m in mentions if m["resolved"]),
            "unresolved": [m for m in mentions if not m["resolved"]], "violations": V, "stale": stale,
            "new_crops": sorted(slugs - KNOWN_POPULATION), "lost_crops": sorted(KNOWN_POPULATION - slugs)}


def refusal(r):
    if r["carrying"] == 0 or r["inspected"] == 0:
        return "inspected 0 crops carrying rootstock_options"
    if r["lost_crops"]:
        return (f"{len(r['lost_crops'])} crop(s) of the measured population no longer carry rootstock_options "
                f"({', '.join(r['lost_crops'])}); the floor is by identity, so a swap cannot hold the count")
    if r["inspected"] < r["carrying"]:
        return f"inspected {r['inspected']} of {r['carrying']} crops carrying rootstock_options"
    return None


def stale_lines(stale, known=None):
    known = KNOWN if known is None else known
    return [f"STALE waiver ({known[k]['ticket']}): {k[0]} {k[1]} '{k[2]}' no longer fires on that exact sentence. "
            f"Delete it from rootstock_prose_gate_known.py in the commit that retires it." for k in stale]


def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(HERE), "crops_data_final.json")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    r = roster(data)
    for v in r["violations"]:
        print("VIOLATION:", v)
    for s in stale_lines(r["stale"]):
        print(s)
    print(f"rootstock_prose_gate: inspected {r['inspected']} crops carrying rootstock_options (of {r['carrying']}), "
          f"{r['fields']} fields, {r['mentions']} rootstock names ({r['matched']} matched a row); "
          f"{len(r['unresolved'])} unresolved, {len(r['unresolved']) - len(r['violations'])} waived by identity; "
          f"{len(r['violations'])} violation(s), {len(r['stale'])} stale waiver(s)")
    if r["new_crops"]:
        print(f"  new to the population (inspected): {', '.join(r['new_crops'])}")
    print(f"  {LIMIT_LINE}")
    why = refusal(r)
    if why:
        print(f"rootstock_prose_gate: REFUSED -- {why}. A check that inspected nothing is not a pass.")
        return 2
    return 1 if (r["violations"] or r["stale"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
