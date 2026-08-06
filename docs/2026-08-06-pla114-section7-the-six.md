# PLA-114 §7 — the six, and the harvest arms left bare on purpose

**2026-08-06. Canonical `bce8bcc7` -> `c0136fb9`.** Seven UC ids minted, Lazaneo admitted under
the existing San Diego id, four CA `plant_out` arms repointed, F5 amended by append, three
findings filed. **No consumer prose moved.**

Reproduce:

```bash
python3 -m pytest tools/test_promote_pla114_six.py -q     # 35 passed, 15 mutations caught
python3 tools/cited_claim_scan.py lemon --proximity 200
```

---

## 1. Two work-order inputs were wrong, and verification came before the build

Both were flagged as weaker-chain and both were checked from bytes before anything was written.

**The UC IPM bloom months HOLD.** They had been read off a rendered screenshot, with the bar
edges called out as least certain — specifically whether Bloom ends mid-April or end of April.
Re-derived from raw HTML, the `Bloom period` row shades both half-month cells of March and
**exactly one** half-cell of April. Mar – mid-Apr is correct as read. The same parse confirms the
`Harvest` row is generic citrus (Jan–May plus mid-Nov–Dec), which is why it must not be read as
lemon's harvest.

**AZ1001 does NOT say "Aug 1 – Feb 15".** Two errors, one on top of the other:

- Its URL in the mint table 403s in **both** plain and browser user-agent modes, while the host
  root returns 200 — path-specific, not a bot policy. The working path is
  `extension.arizona.edu/sites/extension.arizona.edu/files/pubs/az1001.pdf` (100,891 b, 6 pages,
  confirmed *AZ 1001*, Maurer, April 1998).
- Its harvest chart carries month headers and variety labels in the text layer with **no dates** —
  the spans are drawn as vector marks. Read from those marks the way campaign C read AZ1005,
  Eureka and Lisbon each carry marks in **fourteen half-month cells**: Jan-1st through Feb-2nd and
  Aug-1st through Dec-2nd. The last marked cell is the **second** half of February, so the window
  is **August through February**. That is the bar-edge error the work order predicted for UC IPM,
  landing on AZ1001 instead.

The instrument was validated against controls rather than trusted: Minneola tangelo Dec-2nd–Feb,
Marsh grapefruit Nov-2nd–May, Nagami kumquat Oct–Mar, Ponderosa 24 of 24 year-round (which matches
the work order). Distinct, plausible, not a constant. And since `harvest` strings are month-granular
touch-sets, the day-precise form was never the right shape anyway.

## 2. 62 cached non-documents purged, and the tool that would have believed them

`tools/.doc_cache` held **48 `FETCHFAIL` stubs written by our own fetcher** (47-byte files whose
entire content is `\x00FETCHFAIL HTTPError: HTTP Error 403: Forbidden`) plus **10 Incapsula
challenge pages**. Every one of them read as CACHED and would scan clean — an absence manufactured
by our own fetcher rather than by the network, which is
[[waf-block-pages-cached-as-absence]] arriving from the inside.

`cited_claim_scan` now classifies these `NOT-A-DOCUMENT` and routes them to UNDETERMINED, with a
mutation test that poisons a cited URL and asserts the absence becomes unreportable.

**None of lemon's 29 cited URLs was affected**, so F1 and F5's document scoping is unchanged. The
check was run before drawing that conclusion, not assumed.

## 3. What the promote refuses to write, and why that is the substance

Documents were **found** for the `low_desert_az`, `ca_desert` and `ca_south_coast` harvest arms and
deliberately **not** cited.

Those arms are not date strings. They compute from `bloom_start + 240/+300`, and bloom is itself
MODELED. So the displayed value is produced by the model, not by any document:

- **Repointing** would credit a document for a value it did not produce — the F1 defect exactly.
- **Re-deriving the offsets** from the documents would be worse: it pushes a sourced absolute
  window through an unsourced anchor and then cites the document for the composite. Same defect,
  more arithmetic.

So they stay bare, and the reason is filed as a **user-facing content finding**, not as citation
hygiene.

### The consequence — and the overstatement the source-truth sample caught

| region | sources say | offset arm computes | zone `harvest` string |
|---|---|---|---|
| `low_desert_az` | AZ1001: **Aug–Feb**, ~7 months | ~60 days | "Nov - Mar (Eureka bears year-round)" |
| `ca_south_coast` | Mauk: *"bears year round on the coast"* | ~90 days | "Nov - Mar (and scattered year-round; heaviest late winter to spring)" |

The first draft of this finding said a grower is shown a harvest season **roughly five months too
short**. **The source-truth sample refuted that before it shipped.** There are *two* reader-facing
harvest surfaces, and the zone-level `harvest` string is separately authored, broadly consistent
with the sources, and several cells carry an explicit year-round caveat. The alarming version was
not established.

Canonical was **restored to base and the promote re-run with corrected text**, rather than shipping
the overstatement and appending a correction to it — the finding record is append-only once it
lands, so the cheap moment to fix it was before the commit, not after.

What survives is narrower and still worth fixing: the two surfaces disagree, the offset-derived one
is narrower than every source read, and `low_desert_az`'s string **omits August through October** —
three months AZ1001 marks for both cultivars. Both surfaces render: `harvest_start`/`harvest_end`
drive plant-astro's `SuccessionCard`, `TodayCommunityCard` and `PlantingCalendarCard`.

**Internal corroboration needing no document at all:** lime shares all nine of lemon's regions and
is described by the same sources as the same ever-bearing habit, yet lime is modeled at a **180-day
span in eight of them** while lemon runs 60 to 125.

This is the third claim this session that verification corrected before it reached the record, after
the HS402 reversal and the fourteen-string prose reversal. The pattern is consistent: the mechanical
step (here, protocol #6's source-truth sample) is what catches the confident narrative.

## 4. Bloom stays modeled everywhere, including where a chart exists

UC IPM's timing chart is admitted to the catalog and cited by **no cell**. Its entry reads
*"CITABLE ONLY FOR THE MAIN BLOOM OF CENTRAL VALLEY CITRUS GENERALLY, NEVER FOR LEMON'S BLOOM"*.

It is a commercial Pest Management Guideline covering citrus dominated by navels and mandarins, and
four independent sources describe lemon as ever-bearing (Mauk: Improved Meyer *"bears year round"*;
Santa Clara: Eureka *"some fruit year-round"*; Marin: *"lemons and limes are considered
ever-bearing"*; SLO: flowers and fruit in spring, summer and fall). Filling a discrete Mar–mid-Apr
window would assert a bloom for the crop repeatedly named as the exception — the same error as
reading lemon off the generic Harvest row, or off Lazaneo's ranking.

Three UC counties **place** that bloom by timing work around it (Sacramento *"in March before
bloom"*, Santa Clara *"February or March before bloom"*, SLO *"just before spring bloom"*).
Placing is not publishing.

## 5. What was written

| | |
|---|---|
| minted | `ucce_riverside_citrus_qa`, `uc_mg_marin_citrus`, `ucce_kern_kc9382`, `uc_ipm_citrus_timings`, `ucce_placer_nevada_31_018c`, `uc_mg_sacramento_gn127`, `uc_mg_santa_clara_citrus` |
| admitted, no new id | Lazaneo under existing `ucanr_san_diego_mg` — same host as the catalogued turnip source |
| `plant_out` repointed | `ca_interior` → Kern KC9382 · `ca_north_coast` → Marin · `ca_south_coast` → Lazaneo + Mauk · `ca_desert` → Mauk |
| left bare | `low_desert_az` `plant_out` (AZ1001 publishes no planting date, #14 still open) |
| F5 | amended **by append** — a seventh document, and 26 °F is **two** institutions not one |
| findings | 3 filed: two modeled declarations with absences enumerated, plus the held-back harvest finding |

Two catalog entries carry explicit bars, because both documents are right for one claim and wrong
for another: **Lazaneo must not be cited for the hardiness ranking** (it puts grapefruit more tender
than true lemon — an outlier 6 to 1 against 8100, 31-018C, LSU, AZ1001, KC9382 and Mauk), and
**UC IPM must not be cited as lemon's bloom**. Both bars are mutation-tested.

`ucce_placer_nevada_31_018c` records that it is **not independent** of the Meyer 22 °F figure lemon
already cites (Fake & Norton, `134971.pdf`) — same author, same ladder, one lineage.

## 6. Guards

35, RED before GREEN, **15 mutations all caught, none vacuous**. The load-bearing ones are the
negative guards, because this promote's substance is what it declines to write: repointing a
held-back harvest arm, citing UC IPM on a bloom arm, repointing `low_desert_az` `plant_out`,
minting Lazaneo as a new id, and stripping either catalog bar.

One mutation initially read as a vacuous guard and was not — the *mutation* targeted a phrase F5
does not contain, so `replace` was a no-op. A mutation that does not mutate proves nothing about
the guard; it only proves the mutation was wrong.

**Gauntlet:** `whole_crop_gate` PASS · `gate_all` 121/121 · `release_verify` no new concerns
(catalog +7, only the four CA regions changed, dash and spelled-degrees scan clean) · COMPACT
preserved.

## 7. The archetype finding — PLA-151

The diagnosis is done and filed at the `evergreen_fruit_tree` level, **not** at lemon and **not** at
"trees". It does not block this promote, which leaves the affected arms bare.

- **Crop-level `harvest` is `None` on all 21 tree crops**, so these arms are the *only* harvest
  surface. Nothing coarser renders if they are wrong.
- **All 478 tree harvest arms anchor on `bloom_start`**, with zero exceptions. Correct for a
  determinate deciduous fruit; the wrong instrument for an evergreen ever-bearing one, doubly so
  when bloom is itself modeled.
- **The lime control needs no document**: same nine regions, same ever-bearing habit per the same
  sources, 180 days against lemon's 60–125. It establishes **inconsistency, not direction** — it
  does not prove lemon is the wrong one, and lime's 180 is not validated by it. Direction comes
  from the documents, which describe *longer* seasons, not shorter.
- **No schema change is required.** `absolute` (156 arms), `year_round` (7) and `date` (19) anchors
  already exist; `cherry-tomato` / `hawaii_tropical` is the working precedent, carrying
  `from: "year_round"` with a `synthesis_note_seasoned` explaining the absent season-end boundary.
- **Scope**: 7 evergreen crops (avocado and olive have no harvest arms); the suspect set is
  9 lemon cells plus `orange-navel` `rgv`, all at ≤120-day spans. **Deciduous is explicitly not
  implicated** — its short spans are correct.

`ca_interior`'s modeled declaration cross-references PLA-151 and says plainly that **"modeled" is a
provenance claim, not a correctness one**: at a 95-day span the cell may be both unsourced *and* too
narrow, which are separate defects with separate fixes. An unqualified declaration would have read
as modeled-and-therefore-fine.

## 8. Still open on PLA-114

**Hunt #14's `plant_out` and `bloom`** (AZ1001 publishes neither) and the three harvest arms, bare
by decision until PLA-151 is worked. The two pears remain deferred to the UC fruit-tree read.
