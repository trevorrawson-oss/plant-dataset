# Citation-integrity cleanup arc — kickoff

**Written:** 2026-07-29, at the close of the post-asparagus hardening pass.
**Canonical at writing:** `dd24b180` (`origin/main` + 4 unpushed commits; 128 crops / 121 certified).
**Run this in a FRESH session.** Everything needed is here, in `CURRENT_STATE.md`, and in
`docs/2026-07-29-hardening-session-outcomes.md`.

---

## 1. Why this arc, and why it is the important one

"T1-or-it-doesn't-ship" is the product's actual moat. **A bad citation is worse than a missing
one, because it looks verified.**

The evidence that started this: asparagus shipped with **4 bad citations out of ~21 sources (~19%)**,
and **all four survived an 11/11 T1 source-truth sample**. `unr_fs0261` is a real UNR Extension
fact sheet whose only mention of the crop is the string `"Stems - asparagus"` in a list of edible
plant parts. Even at 5% rather than 19%, the roster carries dozens of bad citations inside certified
data.

Two later passes made it worse, not better. This is not a hypothesis any more:

- The 2026-07-27 harvest sweep found three fresh instances of the same shape (`auburn_aces`, UNR
  3017, plus a near-miss stretching UC's "Central Coast" onto our north/south coast regions).
- The 2026-07-29 hardening pass found **six more, verified by direct fetch** (§6 below), including
  a **fabricated rationale** attributed to a real document and a **T2 retail chart served from a
  `ucanr.edu` URL**.

**Crucially, tier and claim-support are two different axes, and tier discipline cannot catch
claim-support failure.** All four asparagus defects were `tier: T1`,
`source_class: university_extension` — genuine land-grant documents cited for claims they do not
contain.

---

## 2. Read these first

| what | where |
|---|---|
| the arc's original framing | `docs/2026-07-27-state-of-play-and-next-steps.md` §5 |
| the six new verified instances + the design correction | `docs/2026-07-29-hardening-session-outcomes.md` |
| the tier model, measured rather than assumed | `docs/2026-07-27-source-tier-model-kickoff.md` |
| the WebFetch-PDF fabrication hazard | `asparagus.verification_status.open_findings` id `webfetch_pdf_summaries_are_not_sourcing` |
| standing rules (incl. the two added 2026-07-29) | `CLAUDE.md` |

---

## 3. The surface, measured (not estimated)

Measured against `dd24b180`. The earlier §5 estimate of "2,660 citation pairs" was **an order of
magnitude low** — it counted something narrower.

| quantity | value |
|---|---|
| `source_catalog` entries | **190** (181 T1, 9 T2) |
| catalog ids actually referenced | 165 (**25 never cited** — dead catalog rows) |
| referenced ids missing from the catalog | **0** (the catalog is complete w.r.t. references) |
| `anchoring_urls` (id, url) pairs across all crops | **29,447** |
| distinct URLs among them | **1,175** |
| **per-cell URLs that are a BARE HOST** | **1,576 pairs across 26 source ids** |

`source_class` distribution is 158 `university_extension`, 6 `extension_master_gardener_program`,
6 `commercial_seed_company`, 5 `horticultural_authority`, 3 `government_observation_network`, plus
singletons.

**Do not try to fetch 29,447 pairs.** Work the 1,175 distinct URLs, then weight the manual pass by
how many cells each URL carries.

---

## 4. THE DESIGN CORRECTION — read this before writing any script

The original plan proposed three tiers:

| tier | check | status after 2026-07-29 |
|---|---|---|
| A | does every cited URL resolve? | **INSUFFICIENT ALONE — see below** |
| B | does the document mention the crop at all? | still the best value-for-effort |
| C | does it support *this specific claim*? | manual, sampled, highest value |

**Tier A on its own is close to worthless here, and this is measured:** every portal-root defect
found in the hardening pass returns **HTTP 200**. `msu_ext`'s catalog root serves an Incapsula block
page (842 bytes, 80 chars of text) at 200. `ndsu_ext`, `sdsu_ext`, `umaine_ext`, `iastate_ext`,
`uconn_ext` and `mu_ext` all return 200 as institutional homepages. A liveness check passes all of
them and learns nothing.

Worse, tier A has a **false-negative** mode too: **UF/IFAS HS546 returns 410 while its content is
perfectly fine via archive.** "Dead but correct" and "live but wrong" are different defects and must
be classified separately — do not let a link-rot sweep delete a good citation.

---

## 5. START HERE — the bare-host pass. Zero fetching, one second, 1,576 pairs.

The single highest-value first move, and it needs no network at all. A URL with **no path** is a
domain root; it cannot support a crop-specific claim about planting dates or pest thresholds.

```bash
cd ~/plant-dataset && python3 - <<'PYEOF'
import json, re, collections
d=json.load(open('crops_data_final.json',encoding='utf-8'))
sc=d['source_catalog']; BARE=re.compile(r'https?://[^/]+/?$')
hits=collections.Counter(); crops=collections.defaultdict(set)
def walk(x, slug):
    if isinstance(x,dict):
        for k,v in x.items():
            if k=='anchoring_urls' and isinstance(v,dict):
                for sid,meta in v.items():
                    u=(meta or {}).get('url') if isinstance(meta,dict) else None
                    if u and BARE.fullmatch(u): hits[sid]+=1; crops[sid].add(slug)
            else: walk(v,slug)
    elif isinstance(x,list):
        for v in x: walk(v,slug)
for c in d['crops']: walk(c,c['slug'])
for sid,n in hits.most_common():
    print(f'{sid:26} {n:6d} cells {len(crops[sid]):4d} crops  {sc.get(sid,{}).get("url","")}')
print('TOTAL bare-host pairs:', sum(hits.values()))
PYEOF
```

Top of the list as of `dd24b180`:

| source id | cells | crops | url |
|---|---|---|---|
| `ucanr_ext` | 337 | 22 | `https://ucanr.edu` |
| `uc_mg` | 283 | 25 | `https://mg.ucanr.edu` |
| `tamu_agrilife` | 201 | 33 | `https://agrilifeextension.tamu.edu` |
| `uada_ext` | 141 | 28 | `https://www.uaex.uada.edu` |
| `ncsu_ext` | 99 | 26 | `https://content.ces.ncsu.edu` |
| `uariz_ext` | 91 | 13 | `https://extension.arizona.edu` |

**This is a TRIAGE list, not 1,576 defects — adjudicate, do not mass-edit.** Two honest
possibilities per row, and they need different treatment:

1. The bare host is an **institution pointer** and the actual document is identified elsewhere on
   the cell (in `source_note`, a `source_quote`, or the cell prose). Then the fix is to **repoint
   the URL at the document**, which is mechanical and safe.
2. The bare host is **all there ever was**, and no specific document was ever consulted. Then the
   cell's claim is **unsourced**, and that is a content finding, not a URL fix.

Telling those apart is the work. Note the distinction between the **catalog** URL and the
**per-cell** URL: 55 catalog rows carry a bare host, but only 26 ids are cited on cells with one —
and some ids (e.g. `ucanr_san_diego_mg`, `nmsu_chart`) have a *pathed* catalog URL while individual
cells still point at the root. Fix the cells, not just the catalog.

**A useful prior from the hardening pass:** `tamu_agrilife` was one of these, and its fix was case 1
— TAMU **EHT-066** was located, verified by pypdf, and it *supported the claim precisely*. So expect
a meaningful share of these to be repointable wins, not content failures.

---

## 6. The seed set — nine instances already verified by direct fetch

Do not re-derive these; they are confirmed and are the arc's starting worklist.

1. **`msu_ext` is cited on all five asparagus `northern_tier` cells and contains no crown timing.**
   The cell URL serves a real 25,784-character MSU article — genuine land-grant, cited for a claim
   it does not make. The same defect five times.
2. **Five ids resolve to portal roots** with zero crop content: `ndsu_ext`, `sdsu_ext`,
   `umaine_ext`, `iastate_ext`, `uconn_ext`. All HTTP 200.
3. **`uconn_ext` points at the wrong host entirely** — the real UConn asparagus fact sheet lives at
   `homegarden.cahnr.uconn.edu`, not the cited `ipm.cahnr.uconn.edu`.
4. **`sdsu_ext` is cited on asparagus z3 but its sentence is a z4 statement** ("mid-April through
   June") that argues for a start two weeks earlier than the z3 cell says — cited where it
   contradicts.
5. **`umaine_ext` on asparagus z4** is cited for a rule that *forbids* the z4 window (after-frost vs
   an Apr 20 start = last_spring − 11 days). Either drop it or record an explicit dissent.
6. **The `uc_ipm` URL on `ca_desert` z9/z10/z11 is UC IPM's ARCHIVED page**, self-labelled *"not
   actively maintained … All links have been removed"*. A live equivalent exists **and carries more**
   (a California-specific 3-4 week / 8-10 week harvest ramp).
7. **A T2 trap wearing a T1 host:** UC MG Riverside's own Flyers page links a "planting calendar"
   that is a **Grangetto's Farm & Garden Supply** retail chart sourced to "Digital Seed" — served
   from a `ucanr.edu` URL, image-only so pypdf returns 22 characters. The most citable-*looking* and
   least citable thing in the sweep.
8. **A FABRICATED RATIONALE, retracted 2026-07-29:** the "Fusarium-in-cold-wet-soil" argument
   attributed to UMaine Bulletin #2071 **is not in that document** (`"cold wet"`, `"cold, wet"`,
   `"wet soil"`, `"cold soil"` all occur **zero** times). This is the worst shape in the class: not a
   wrong URL but an invented claim with a real citation attached.
9. **25 catalog rows are never cited** by anything. Cheap to audit and either use or drop (precedent:
   `uaex_cardoon` was dropped outright rather than admitted uncited).

---

## 7. Traps — every one of these has already caused a real defect here

- **WebFetch summaries of PDFs are NOT sourcing.** A research agent *fabricated* a document title
  and supporting quotes ("Peak harvest typically occurs April through June") for a Contra Costa
  handbook containing **no asparagus content at all**, from a WebFetch summary of a PDF. Worse than
  garbling, because it invents. **Download + `pypdf`, or raw HTML via `urllib`. Quote only text you
  personally extracted.**
- **WebFetch's markdown parse of an HTML data TABLE silently shifts columns and blanks cells**,
  producing a plausible-but-wrong grid. It caused three fabrication-class resistance grades. Pull
  raw HTML, or cross-check a second fetch.
- **Drawn-bar charts have no text layer.** Several extension planting charts encode windows as
  graphics; `pypdf` returns crop names and month headers only. Reading bar geometry is legitimate
  and has been done twice here (`nmsu_chart`, `unlv_mg_svn`) — but validate against a known row
  first, and never guess a mark's position.
- **Image-only PDFs** return ~20 characters from `pypdf`. Render (e.g. `fitz` at 2x) and read, or
  discard.
- **Geography stretch.** Do not map a source's stated region onto ground it does not cover. Known
  near-miss: stretching UC's "Central Coast" onto our north/south coast regions.
- **Sentence confusion within one document.** UC ANR Pub 7234 contains *both* a crown window and a
  **seed** window; a cell once carried values matching the seed sentence. Distinguish
  seed / crown / transplant / harvest, and home-garden from commercial.
- **Bot shields are not absence.** `canr.msu.edu` serves Incapsula block pages inconsistently at
  HTTP 200. Retry, vary the path, and record "could not determine" rather than "does not exist."

---

## 8. The tier model — the correction everyone gets wrong

Measured: **all nine `T2` entries are the SEED-TRADE and folklore band** (Old Farmer's Almanac,
Johnny's, seed companies, a gardening blog). **County Master Gardener pages, county planting
calendars and extension charts are `T1`**, and the outreach band already sits at T1 via
`source_class`.

Getting this wrong is a documented failure mode here: an over-strict bar **does not produce
silence, it produces unsourced derivation.** A previous pass repeatedly downgraded usable county MG
sources and left cells unsourced that were sourceable — that is how the asparagus "honest gap" grew.
Also: the arc's own false rejection of `unlv_mg_svn` was reversed once someone checked the catalog —
it is T1 and cited by 67 crops.

**So: check `source_catalog` BEFORE accepting any agent's "this fails the tier bar."**

---

## 9. Discipline (this is where previous passes went wrong)

- **READ every finding. Do not count them.** A gate reported 38 findings on this exact surface and
  **exactly one was a defect.** A count is not evidence. This is the single most repeated lesson in
  this repo.
- **Measure before gating, and be willing not to ship the gate.** Two gates were built, measured and
  deliberately left unwired this month (`logref_count_scan.py`, the stale-quote check at 45 hits).
  A noisy gate gets ignored, which is worse than none.
- **When a check floods, narrow the CHECK, not its scope** (the 38 → 3 → 0 trajectory).
- **Re-verify the data before acting on any record that describes it**, and run the gate that
  already covers the claim first. New standing rule in `CLAUDE.md`; it cost a 16-document sourcing
  pass to learn.
- **Verify subagent findings before relaying them.** Relaying unread agent output is itself a logged
  defect here. Every claim in §6 above was re-fetched by the main session.
- **Promote via a guarded script**, never by hand: pin the pre-state by SHA (or per-string sha256),
  abort on drift, prove the footprint EXACT, keep JSON COMPACT. Four examples from 2026-07-29:
  `tools/promote_logref_corrections.py`, `promote_empty_unsuitable_calendars.py`,
  `promote_hardening_item2.py`, `promote_finding10_label.py`.
- **Do not smuggle content fixes into a citation pass.** A repointed URL is mechanical; a cell whose
  claim no source supports is a **content** finding. Split them, and surface the second kind.

---

## 10. Suggested sequence

1. **Bare-host triage (§5).** No network. Produces the worklist and probably several mechanical
   repoint wins. Start with the six biggest ids (1,152 of the 1,576 pairs).
2. **The nine seed instances (§6).** Already verified; decide repoint / drop / dissent-note per row,
   and handle the 25 uncited catalog rows.
3. **Tier B roster-wide:** for each of the 1,175 distinct URLs, fetch once (cache it) and grep for
   the crop name of every cell citing it. This is the mechanical pass that would have caught
   `unr_fs0261`. **Classify, do not auto-delete** — separate "dead but correct" from "live but
   wrong."
4. **Tier C, weighted sampling.** Prioritize cells whose claim rests on a **single** source — that is
   exactly where the asparagus 11/11 sample failed. This is the highest-value and only-manual tier.
5. **Only then** consider a gate, and only if the measurement supports one. A `url_health_gate.py`
   already exists — read it before writing anything new.

**Effort:** step 1 is an afternoon. Steps 3-4 are the real arc and will span sessions; treat each
batch as its own release with its own gauntlet and state trio.

## 11. Done when

Every cited URL is either **(a)** confirmed to resolve *and* to contain the crop, **(b)** repointed
at the document that does, **(c)** dropped with the dependent claim re-sourced or the cell honestly
downgraded, or **(d)** recorded as a dated, deliberate exception (archive-only, geometry-read,
cited-for-a-documented-absence). Plus: a written statement of what tier C sampled, what it did
**not** cover, and the measured defect rate — so the next pass knows the true residual risk rather
than inheriting a green light.
