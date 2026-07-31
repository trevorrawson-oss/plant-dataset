# The roster-wide bloom declaration must NOT run as planned

**Date:** 2026-07-30
**Canonical at writing:** `45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b` (UNTOUCHED this session)
**Tool built:** `tools/bloom_datum_scan.py` (+ `tools/test_bloom_datum_scan.py`, 22 tests)
**Corrects:** `docs/kickoffs/47-citation-arc-continuation-handoff.md` §2, item 1.

---

## 1. What the plan said

Kickoff 47 ranked one task first, ahead of all remaining document hunts:

> **ROSTER-WIDE BLOOM DECLARATION — do this first.** One documentation-only promote declaring the
> bloom offset as modeled across every crop that carries one.

Its licence was a single premise, stated as the arc's headline finding:

> **no extension service publishes BLOOM DATES.** Confirmed independently at two institutions —
> UAEX (hunt 1) and NC State (hunt 2, 31 mentions of "bloom", zero dates). No hunt will ever find a
> document for that.

## 2. The premise is false

Extension services publish bloom dates routinely. **22 documents at 12 institutions**, all of them
already cited in our own data, publish month-granular bloom timing. A sample, quoted from raw bytes:

| institution | published bloom timing |
|---|---|
| `apples.extension.org` | apple "will generally **bloom in mid-April**" (western NC); "in **mid-May**" (Minnesota) |
| UF/IFAS MG359 | blueberry 'Emerald' "normally reaches **full bloom** in Gainesville around **February 15**" |
| UF/IFAS CH093 | lime, "the heaviest **bloom** in Florida occurring **from February to April**" |
| UF/IFAS HS402 | lemon, "**blooming** may occur from **late December into March**" |
| UGA C997 | pomegranate, "**Bloom begins in April** and continues **through to June**" |
| Penn State | elderberry "**bloom in June through July**"; oregano "**blooms from July to September**"; thyme "**June and July**" |
| UMD | pawpaw, "its **blooms (March-May)**" |
| UMN | raspberry "begin to **bloom in late May or early June**"; strawberry "begin **flowering in mid-May** in southern Minnesota" |
| **NC State Plant Toolbox** | *Morus alba* "**Bloom Time**: Spring … **blossom in March to April**"; *Thymus vulgaris* "**from May to July**" |
| NMSU RR770 | lavender 'Compacta' "**flowering in mid-June**" |
| UC ANR (Ventura / Santa Clara / Sacramento) | blueberry "**bloom as early as January or February**"; "**bloom in late January through March**" |

**66 of our own bloom arms, across 16 crops, cite one of these documents.** Had the declaration run
as written, each would have received a finding asserting *"the quantity is absent from the
literature"* — against a document that publishes it, on the same URL the arm already carries.

## 3. How the premise went wrong: scope creep, twice

The two hunts were correct. Their conclusions were **document-scoped**, and were widened twice:

1. *The UAEX **fruit publication set** publishes no bloom date* → **verified, still stands.**
   Re-confirmed blind this session: the UAEX fruit-trees page classifies `MENTION_NO_DATE`.
2. *The NC State **Extension Gardener Handbook ch.15** publishes no bloom date* → **verified.**
3. → "**NC State** publishes no bloom date" — **false.** NC State's Plant Toolbox carries a
   structured **`Bloom Time`** field.
4. → "**no extension service** publishes bloom dates" — **false at 12 institutions.**

This is kickoff 47's own lesson 2 — *"never generalize a regional correction beyond the authority
that licensed it"* — recurring one level up, at the level of the arc's plan rather than a data cell.
Two documents' silence became an institution's, then the whole literature's.

The real finding survives, narrowed: **no source publishes the *offset-from-last-frost model* our
schema stores.** That is a statement about our encoding, not about the literature.

## 4. A live contradiction this surfaced

`apple` / `mid_atlantic` already carries `mid_atlantic_bloom_offset_undocumented`, which states the
NC State handbook "publishes NO bloom date for any fruit crop … repointing cannot fix an absent
quantity."

But that arm was **never sourced to the handbook**. It cites `ext_org_apples` —
`apples.extension.org/timing-of-apple-tree-bloom/` — which publishes apple bloom timing.

The declaration's *conclusion* may still hold (the page gives **western** NC, and `mid_atlantic` is
explicitly "Piedmont and Coastal Plain" — the Macon County problem already flagged for
`cherry-sour`). Its stated *reason* does not. **Surfaced, not changed** — canonical is untouched.

## 5. What the pass should target instead

`tools/bloom_datum_scan.py --report`, over all 401 bloom arms / 176 documents:

| bucket | arms | disposition |
|---|---|---|
| already declared | 23 | leave; but see §4 |
| own document **publishes** a bloom date | 146 flagged, **66 confirmed** after reading all 47 | **do NOT declare.** Several are repointable to a real datum |
| bloom discussed, **no date** | 138 | the declaration shape genuinely fits |
| bloom **never mentioned** by any cited document | 100 (**78 undeclared**) | **likely a real citation defect** — the `unr_fs0261` shape |
| undetermined (unfetchable/uncached) | 17 | **never absence** (lesson 7) |

The 78 undeclared *never-mentioned* arms are the highest-value slice — concentrated in `elderberry`
(11), `strawberry` (7), `lemon` (5), `lime`/`fig`/`mulberry` (4 each) — and they are a **defect**
class, not a declaration class. That is where the arc's actual yield has always been.

## 6. Two things found in passing

- **A third bloom encoding the handoff does not mention.** Kickoff 47 says "every tree fruit stores
  `bloom[0] = {from: last_frost, offset_days, window_days}`." True for tree fruit, but the roster
  holds **three** shapes: 243 `offset` arms, **145 `month_literal`** blooms (`bloom: ["April",
  "June"]`, 10 berry/herb crops) and **13 `synthesis_window`** arms (strawberry: `from: null` plus a
  literal `window` string and a `synthesis_note`). A declaration worded "a MODELED offset from the
  zone last-frost date" would be **factually wrong** on 158 of 401 arms.
- **A non-T1 source.** `lavender` / `hawaii_tropical` anchors on `westhawaiitoday.com` — a
  newspaper, not an extension service. Separate from this arc; flagged for the tier bar.

## 7. The tool

`tools/bloom_datum_scan.py` classifies each cited document: `PUBLISHES_TIMING` / `MENTION_NO_DATE` /
`NO_MENTION` / `UNDETERMINED`. It reuses hunt 2's fetch/cache layer (167 of 176 documents were
already cached; 9 fetched).

Built test-first, 22 tests, with the adversarial weight on **false CLEARS** — the scan reporting "no
bloom date" where one exists, which is the direction that authorises a false declaration. `May` is
both a month and a modal verb and is counted as a month only in explicit temporal context
(`in May`, `mid-May`, `May 15`), so *"a warm spell **may** cause the tree to bloom"* does not fire.

**Validated against known ground truth before being trusted:** it independently reproduces hunt 1's
UAEX result (`MENTION_NO_DATE`), and returns `UNDETERMINED` — not absence — for an uncached URL.

**It is deliberately over-inclusive.** Of 47 `PUBLISHES_TIMING` documents, **25 are artifacts**:
Clemson HGIC's site-wide tag cloud ("Harmful Algal **Blooms** … June … November"), page
`Updated:` metadata, and months belonging to *pruning*, *sowing*, *ripening* or *fertiliser* timing
rather than bloom. One is a genuine homonym — NC State's persimmon page describes the fruit's "waxy
**bloom**". Every one of the 47 was read; the 22 in §2 are what survived.

**Ships as a scan, never a gate** — for the same reason as `doc_mentions_crop_scan`: the verdict a
human needs is not the one the matcher can compute.
