# Southeast Alaska panhandle region -- design spec

**Date:** 2026-07-20
**Kickoff:** `docs/kickoffs/30-se-alaska-panhandle-region.md` (roadmap item 7)
**Base canonical:** `e1e01c47` (corn family shipped) / dataset `main` @ `67fe7ed` (== `origin/main`)
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md` -- the only
**NEW-REGION** ruling of the five Tier-2 belts.
**Precedent arcs:** RGV (`2026-07-13-rgv-subtropical-tx-region-design.md`, frost-FREE) and maritime
PNW (`2026-07-14-maritime-pnw-region-design.md`, frost-ANCHORED). This region is frost-anchored, so
**PNW is the structural template** and this spec is written as "same as PNW except..." wherever that
holds. The places it does NOT hold are section 4.4 and 4.5, and they are the reason this arc exists.

**Trevor's standing ruling (2026-07-16, restated 2026-07-20):** roadmap items 7-11 are all **full new
regions**, not candidates awaiting a second go/no-go. This spec proceeds on that basis.

---

## 1. Product goal

Author a real Southeast Alaska panhandle region (`se_alaska`, the maritime Alexander Archipelago
strip from Ketchikan north through Juneau, z7-8) so the panhandle's ZIPs stop riding generic
frost-anchored zone dates that are not merely imprecise here but **wrong in kind**: they present
unprotected outdoor tomato culture as ordinary, and they would endorse an apple variety list bred for
a growing season 45+ days longer than Ketchikan's.

This is the third new authored region and the first whose justification is a **suitability-class**
divergence rather than a window-shape one.

## 2. Why SE Alaska needs its own region (and why it is not a colder PNW)

The ruling's finding, compressed. Two of three basket crops diverge at the class level, and both
divergences share one root cause: **the zone number encodes winter minimum temperature, and in the
maritime panhandle that number is decoupled from the thing that actually binds -- a short, cool,
cloudy GROWING season.**

- **Warm-season annuals need protection, full stop.** Three independent UAF Cooperative Extension
  sources converge: a statewide guide ("few garden sites are warm enough to grow good tomatoes"), the
  belt's own variety publication HGA-00231 (whose tomato section is headed "perform better in a high
  tunnel or under row cover"), and a controlled Palmer trial where "adjacent plots outside gave almost
  no yields." The naive deriver renders a perfectly ordinary single-cycle outdoor annual. Its basic
  operating premise, not its window length, is what the sources contradict.
- **Apple's real recommended variety list shares ZERO overlap with the canonical one.** UAF recommends
  Yellow Transparent, Pristine, William's Pride, Gravenstein, Lodi, Tydeman's Early, Sansa, Silken,
  Akane -- very-early July-August ripeners. The canonical 16 (Dorsett Golden through Dolgo) are
  predominantly September-November ripeners. The binding constraint is ripening time, a mechanism this
  dataset does not model for apple; applied naively, the chill logic would read AK's abundant chill and
  default toward `fruits_reliably` off the wrong list.
- **Cool-season annuals are fine** (kale thrives, no protection), the familiar
  under-representation-only shape.

**Not a colder shade of PNW.** The ruling cross-referenced this dataset's own `pnw` cells directly:
PNW z8 cherry-tomato runs a full outdoor season with an explicit "no special early-variety caution is
needed here" note, and PNW z8 apple is `fruits_reliably` off the canonical list. Both are the
**opposite** of what UAF documents for the AK panhandle. PNW is the right belt to compare against and
the wrong belt to inherit from.

## 3. Scope -- Option A, full roster-wide (forced, not chosen)

`coverage_floor_gate` A31 derives its region roster from `zone_span_gate.EXPECTED_SPANS`. The moment
`se_alaska` enters `EXPECTED_SPANS`, every certified region-carrying crop needs a `se_alaska` cell or
A31 fails it. A partial region would reintroduce borrowed data under a real region label, which is the
exact dishonesty a new region exists to retire.

**Roster confirmed against canonical `e1e01c47`** (128 crops / 119 certified; **111 region-carrying**,
up from PNW's 108 -- the 3 corn crops certified since):

| Crop class (`calendar_basis`) | Count | SE Alaska reality | Gate floor |
|---|---|---|---|
| `frost_anchored` annuals | 82 | **Split by season-class.** Cool-season: thrives, no protection, long harvest tail. Warm-season: protected culture required or recommended (the new field, 4.4) | A31 + A32 (real calendar) |
| `perennial_chill_gated` fruit | 14 | Chill is abundant and NOT the constraint; ripening time is. Apple + the very-early stone/pome set are the honest-`marginal`-with-a-variety-steer case (4.5); most of the rest fall to `survives_no_fruit` / `unsuitable` | A31 + **A3** (A32 exempt) |
| `perennial_evergreen` (citrus) | 5 | `unsuitable`, cold-decided. The easiest class in the arc | A31 (A32 exempt) |
| `perennial_woody_ornamental` (herbs) | 5 | Cold + wet edge; expect `grown_as: annual` / container treatment on several (the existing `northern_tier` z3 idiom, already in the schema) | A31 + A32 |
| `berries_woody` | 4 | Genuinely strong: the panhandle is real berry country (UAF lists currants, raspberries, blueberries) | A31 + A32 |
| `perennial_herbaceous` (strawberry) | 1 | Real, sourced; UAF lists strawberry for SE Alaska | A31 + A32 |

The 8 certified microgreens carry no `regions` block at all and are out of scope; the 9 uncertified
shells are exempt (the same certified-only rule `gate_all` and A45 use).

## 4. Data model

### 4.1 Region id and label

`region_id: "se_alaska"` (the `se_gulf` naming precedent: compass prefix, lowercase, underscore).
Label: **"Southeast Alaska: the maritime panhandle"**, following the `pnw` label idiom
("Maritime Pacific Northwest: Puget Sound and Willamette Valley").

### 4.2 Zone span -- `["7", "8"]` (the one genuinely contested call in this spec)

**Decision: span both zones.** The ruling researched z8 (Ketchikan) because that was the belt the
Tier-2 sweep handed it. Building only z8 would ship a region that describes the panhandle and covers
almost none of it. The real ZIP distribution, read from plant-app's `zip-zones.json`:

| AK zone | ZIPs | Panhandle ZIP3s (998/999) | Non-panhandle ZIP3s (995/996 Southcentral + Kodiak) |
|---|---|---|---|
| 8 | 13 | 6 | 7 |
| 7 | 36 | 22 | 14 |

z8-only delivers **6 real panhandle ZIPs** and leaves Juneau (99801, the state capital and the
panhandle's largest community) and Sitka on generic dates. Both are z7 per the ruling's own sourcing,
which places Ketchikan alone among the three panhandle centers in z8. Spanning z7-8 covers **28**
panhandle ZIPs and matches the belt as a climate rather than as a zone artifact. The frost data for
z7 is available from the same NWS AJK "Last Spring Freeze" table the ruling already extracted
(Juneau Airport and Sitka Airport both appear in it).

**Two consequences to carry forward:**

1. **A ZIP3 fence is mandatory, not optional** -- and it is a bigger deal here than for RGV or PNW.
   Naive state+zone matching pulls 21 non-panhandle AK ZIPs (995xx Southcentral, 996xx including
   Kodiak) into a panhandle calendar. Kodiak in particular is maritime and superficially similar but
   is a different belt with its own UAF treatment. Fence `se_alaska` to **ZIP3 998 and 999**. Section 9.
2. **z7 overlaps `northern_tier`'s span** (`["3".."7"]`). This is fine for A45 (spans are per-region)
   and fine in-app (region matching is state-scoped, and `northern_tier` is not ZIP-resolved at all --
   see 9.2). Flag it in the build so nobody reads the overlap as a defect.

### 4.3 Frost-anchored resolution -- the standard model, same as PNW

The panhandle has a real winter, so cells are ordinary frost-anchored cells and the standard deriver
applies. **No new `calendar_basis`, no deriver change, no hand-authoring** (the RGV Hawaii-shape does
not apply).

- `resolution_method: "frost_anchored_resolved"`.
- `resolved_from: {last_frost, first_frost}`. **z8 (Ketchikan) is already sourced by the ruling:
  last frost Apr 22, first frost ~Oct 30** (NWS AJK 38-year station table + NOAA NCEI's independent
  191-day growing-season figure, cross-checked arithmetically). **z7 (Juneau/Sitka) is a build
  sourcing task** from the same NWS AJK product.
- Authored month windows; `calendar[]` derived by `tools/annual_calendar.py` with
  `calendar_basis = "frost_anchored"`.
- **`cold_pause` is legitimate here** (as in PNW, unlike RGV). Relax that check in
  `region_cell_audit.py`, which is already parametrized for exactly this.
- **No `heat_pause` anywhere in this region.** Summer is the growing window; it is simply short and
  cool. Nevada/Utah's heat-abort shape has no analog here.

**A precision caveat to carry into the prose, not bury:** Ketchikan's last-frost standard deviation is
15.2 days, one of the widest in the NWS table (Juneau 12.4, Sitka 12.3). The authored windows should
read as genuinely variable rather than falsely precise. This is a `region_notes_seasoned` job.

### 4.4 NEW conditional field: `protected_culture` (the reason this is a region, part 1)

**The problem.** The annual archetype has no `suitability` field -- A32 forces a calendar, and honesty
has always lived in calendar shape plus prose. For PNW's marginal melons that was enough, because the
question was *how well*, not *whether*. Here the question is whether the crop is an outdoor crop at
all, and three T1 sources say it is not. Prose alone would let the app render an ordinary outdoor
tomato calendar with a caveat buried in a notes field, which is the naive lie in better handwriting.

**The design.** A per-zone conditional field on frost-anchored cells, flat, following the established
`grown_as` / `recommended_type` idiom exactly (a value plus dual-register notes, declared where real
and omitted everywhere else):

```
"protected_culture": "required" | "recommended",
"protected_culture_methods": ["high_tunnel" | "row_cover" | "greenhouse" | "cold_frame", ...],
"protected_culture_note_seasoned": "...",
"protected_culture_note_beginner": "..."
```

- **Omitted, not null, when it does not apply** -- matching `grown_as` (186 cells) and
  `recommended_type` (124 cells), which appear only where they are true.
- **`required` vs `recommended`** is the load-bearing distinction: `required` means the T1 evidence
  says unprotected culture fails (tomato, pepper, eggplant, cucumber, melon, basil); `recommended`
  means it works outdoors but protection materially extends or secures it.
- **The authored calendar must describe the PROTECTED season** when the value is `required`. A tunnel
  season starts earlier and runs later than the outdoor one; authoring outdoor windows next to a
  "you need a tunnel" note would leave the two halves of the cell contradicting each other.
- **Region-generic, rolled out only where evidenced.** The field is not `se_alaska`-specific by
  construction. `northern_tier` z3-4 almost certainly qualifies for several crops and the existing
  dataset already carries 27 "high tunnel" and 619 "row cover" prose mentions with nowhere structured
  to put the fact. That backfill is explicitly a FOLLOW-ON, not this arc (CLAUDE.md: run column passes
  against a stable roster, one at a time).

**Gate: A46 `protected_culture_gate`** (next free A-number). Conditional-field gate, **not** an A39
presence field -- the `planting_layout` / A44 precedent, which the gate file itself documents as the
model for exactly this shape. Rules: value in the 2-enum; `protected_culture_methods` present,
non-empty, all members in the 4-enum; both dual-register notes present and non-empty whenever the
field is declared; the field appears only on cells whose crop is `calendar_basis: frost_anchored`;
`sources` present on the cell. TDD: RED first, on a scratch copy, one injected defect per rule.

### 4.5 NEW conditional field: `recommended_varieties` (the reason this is a region, part 2)

**The problem.** Apple's canonical `variety_detail` list is global. In the panhandle it is the wrong
list -- not marginally, but with zero overlap against UAF's own. The app renders variety cards from
`variety_detail`, so a `se_alaska` apple cell that says nothing structured would actively steer users
toward September-November ripeners that do not finish in a 191-day season.

**The design.** Per-zone, flat, directly parallel to the existing `recommended_type` / `type_note_*`
pair that already does regional variety-class steering for blueberry (northern_highbush vs rabbiteye),
raspberry, blackberry, and elderberry:

```
"recommended_varieties": ["Yellow Transparent", "Pristine", ...],
"variety_note_seasoned": "...",
"variety_note_beginner": "..."
```

- **Names, not references.** Entries are T1-sourced variety names and are explicitly NOT required to
  exist in the crop's `variety_detail` array. Requiring that would drag a variety-authoring arc into a
  region build. The gate must not enforce a cross-reference; the app must not assume one (section 9).
- **Scoped to the tree/berry perennial classes** in this arc, where "which cultivar" is the difference
  between fruit and no fruit.
- **`suitability` still carries the verdict.** The honest apple call for the panhandle is `marginal`
  with a variety steer, not `fruits_reliably`: apples do fruit here, but only from a variety set the
  canonical list does not contain. **A3 permits this** -- verified by reading
  `tools/perennial_gate.py`: `marginal` and `fruits_reliably` differ only in requiring a calendar, and
  the chill direction-split fires solely on `survives_no_fruit`. The abundant chill band will not
  force a `fruits_reliably` call.

**Gate: A47 `region_variety_steer_gate`** -- shape-only, same conditional pattern as A46: list of
non-empty unique strings, both dual-register notes present when declared, cell `sources` present,
no `variety_detail` cross-reference requirement.

### 4.6 The mechanism this arc deliberately does NOT build

The ruling's sharpest observation is that ripening-season length is unmodeled for apple. **The schema
already has the right mechanism and it is already gated:** `gating_factors: ["heat_accumulation"]` plus
a per-zone `heat_summer_basis` enum (`high` / `adequate` / `marginal` / `insufficient`), with A3
enforcing "`insufficient` cannot be `fruits_reliably`." It ships today on 3 citrus crops
(orange-navel, mandarin-clementine, grapefruit).

Extending `heat_accumulation` to the 14 chill-gated deciduous trees is very likely the right long-term
answer. **It is out of scope here**, and deliberately so: adding `heat_accumulation` to a crop's
crop-level `gating_factors` makes it heat-gated in *every* region, so A3 would immediately demand
`heat_summer_basis` on that crop's cells across all 12 existing regions. That is a second roster-wide
column landing on top of a region column, against CLAUDE.md's standing rule of one column pass at a
time against a stable roster.

**Register it as a queued follow-on arc** (field register, new row). Doing so is what lets this spec
use `marginal` + `recommended_varieties` for apple honestly rather than as a workaround: the verdict
is correct today, and the mechanism that would let the gate *derive* it is scheduled rather than
hand-waved.

### 4.7 Top-level touch-points

- `zone_span_gate.EXPECTED_SPANS`: add `se_alaska: ["7", "8"]`. **No `DONORS` entry** -- authored
  fresh, nothing cloned.
- `region_chill_delivered.se_alaska`: bands for z7 and z8 (4.8).
- `region_chill_delivered_provenance`: the band's source note.
- `coverage_floor_gate.CANONICAL_REGIONS` / `CANONICAL_ZONES`: auto-derived from `EXPECTED_SPANS`, no
  edit.
- `source_catalog`: register the UAF Cooperative Extension sources. The ruling deliberately left this
  undone ("formal registration happens only if/when this belt is actually built") -- this is the arc
  that does it. Expect a new `uaf_ext` (or similarly-keyed) catalog entry.

### 4.8 `region_chill_delivered.se_alaska` -- a real risk, flagged not guessed

The band is **user-displayed** in plant-astro ("your area banks ~X chill hours"), so it must be sourced
in the same chill model as its neighbors (`pnw` z8 `[968, 1950]`, `northern_tier` z7 `[700, 1200]`,
z3 `[1000, 1600]`).

**The ruling searched for a Ketchikan or SE-Alaska chill figure and did not find one.** That is
recorded there as an honest gap and it is the single largest sourcing risk in this arc. A cool
maritime climate accumulates chill generously, and this dataset's own `northern_tier` z3 cell already
states the mechanism verbatim ("Chill is abundant, so the tree blooms every spring; the bloom is
simply too exposed"), so the *direction* is not in doubt. The magnitude still needs a source.

**Build order:** hunt the band FIRST, before authoring the 14 tree cells. If no T1 AK figure exists,
stop and bring the fallback options to Trevor rather than picking a number -- this is a displayed
figure, and A3's `survives_no_fruit` split reads its low end. Note that apple's `min_variety_chill`
floor is 100 hours (Dorsett Golden / Ein Shemer), so any plausible band clears it, which means the
split will never force an empty apple calendar here.

## 5. Viability taxonomy (the honest per-class call)

- **Cool-season annuals** (brassicas, greens, roots, peas, cool herbs). The strong axis. Long cool
  season, long harvest tails, no protection. The one real gap the ruling found is
  under-representation: naive kale gets a 4-week harvest window against a real season that runs for
  months. Author the tail. UAF's HGA-00231 greens/roots sections are the source.
- **Warm-season annuals** (tomato, pepper, eggplant, cucumber, melon, squash, basil, corn, okra, sweet
  potato). `protected_culture: required` for the ones UAF puts under cover; the calendar describes the
  tunnel season. For the far-out ones (okra, sweet potato, melon, the corn family) expect the honest
  answer to be a very short protected window or a frank "does not finish here" prose treatment. There
  is no `suitability` field to lean on, so this is calendar shape + `protected_culture` + notes.
- **Chill-gated trees (14).** Chill is abundant; ripening time binds. Apple is the flagship case:
  `marginal` + `recommended_varieties` off UAF's list. Cherry, plum, and pear need their own T1 calls
  (UAF's "Growing Tree Fruits in Alaska" covers apples, cherries, plums, and pears specifically).
  Expect `survives_no_fruit` or `unsuitable` for the warm-season set (peach, apricot, nectarine, fig,
  persimmon, pomegranate, pawpaw, mulberry) -- **sourced per crop, never assumed.**
- **Citrus (5).** `unsuitable`, empty calendars, cold-decided. A3 requires an empty calendar for
  `unsuitable`, which is the trivially correct answer here.
- **Woody herbs (5).** Cold and wet. Expect `grown_as: annual` or container treatment on rosemary,
  lavender, and possibly sage, mirroring the existing `northern_tier` z3 thyme cell. Lavender in
  particular wants the dry summer the panhandle emphatically does not have (the exact inverse of the
  PNW rain-shadow story).
- **Berries (4) + strawberry (1).** Genuinely strong and a real regional pleasure; UAF lists them for
  SE Alaska. Author with confidence and real notes.

## 6. Sourcing (T1)

UAF Cooperative Extension Service is the institution. The ruling already located and text-extracted
the core set:

- **HGA-00231, "Recommended Variety List for Southeastern Alaska"** -- the belt's own dedicated
  publication and the primary source for both new fields. Tomato under cover; the apple variety list;
  greens and berries listed plainly.
- **"16 Easy Steps to Gardening in Alaska"** (HGA-00134) -- statewide baseline.
- **"Hoop Houses in Alaska"** -- protected-culture framing and the Palmer trial result.
- **"Growing Tree Fruits in Alaska"** + the "It Grows in Alaska" blog -- apple/cherry/plum/pear
  framing and the winter-hardiness-then-ripening priority order.
- **NWS AJK "Last Spring Freeze"** + **NOAA NCEI Ketchikan LCD** -- frost dates, z8 done and z7 to
  extract.

**Gaps to hunt in build:** the chill band (4.8), z7 frost normals, and per-crop windows for anything
HGA-00231 does not cover. **T1-or-it-doesn't-ship holds.** Where a crop has no clean T1 window, author
conservatively and flag it; never fabricate.

**PDF-extraction gotcha (now confirmed three arcs running):** WebFetch's summarizer cannot decode these
PDFs. Re-extract locally with `pypdf` from the binary WebFetch already cached, **in the controller
env** -- subagent sandboxes block network and PDF tooling.

## 7. Rollout mechanics -- author off-canonical, promote atomically

The PNW toolchain is already region-generic and needs no new generalization:

- `tools/region_harness.py` -- off-canonical per-crop gate harness. Pass `se_alaska`.
- `tools/region_cell_audit.py` -- anomaly detector. Pass `se_alaska`; `cold_pause` allowed (the
  frost-anchored setting, as PNW).
- `tools/build_region_promote.py` -- atomic-promote emitter.

Both new gates (A46, A47) must be written **RED-first against a scratch copy** and wired into
`whole_crop_gate` before any authoring lands, so the new fields are gated from their first cell rather
than retrofitted.

SDD execution, class-batched: cool-season annuals -> warm-season annuals (the `protected_culture`
batch) -> trees (the `recommended_varieties` batch) -> berries + herbs + strawberry. Fresh-subagent
content review per batch; per-crop harness gate; scratch dry-run; one atomic SHA-guarded promote
(`EXPECTED_SPANS` + 111 cells + chill band + provenance + `source_catalog` additions landing together
-- a partial land leaves A31/A3 failing). Canonical stays COMPACT.

**Concurrency:** this repo runs concurrent sessions against one checkout. Explicit-pathspec `git add`,
`git status` before commit, `git show --stat` after (memory
`subagent-resumability-and-concurrent-git-safety`). Consider an isolated worktree, as the corn arc did.

## 8. Verification (TDD, per session protocol)

Green gate is not a clean release. Before promote:

- `whole_crop_gate` full suite + `tools/gate_all.py` -> **119/119** certified.
- **A46 + A47 RED proofs** on a scratch copy, one injected defect per rule, documented in
  `docs/reviews/notes/<date>/se_alaska_red_proof.md`.
- `tools/zone_span_gate.py` (A45) -> 0, with `se_alaska: ["7","8"]` in `EXPECTED_SPANS`.
- `coverage_floor_gate` (A31) -> all 111 carry `se_alaska`; the standalone count reads the 9
  uncertified shells (benign, as in RGV/PNW).
- A3 -> the tree split coheres with the `se_alaska` chill band; every `unsuitable` cell empty.
- `chill_gate` -> 0. `calendar_coherence` -> 0. `timing_spine` -> 0.
- `release_verify` -> section A collateral is the known roster-wide false positive; the pre-commit
  backstop `precommit_release_verify.py` is the binding multi-crop regression gate.
- Per-batch source-truth sample against the cited UAF table.
- Independent byte-diff footprint audit: exactly 111 `regions.se_alaska` + chill band + provenance +
  `source_catalog` additions; 0 other keys; count 128; COMPACT.

## 9. App handoff (dataset-only arc)

### 9.1 The standard items

- `REGION_STATES.se_alaska = ['AK']`.
- **The 998/999 ZIP3 fence** (4.2) -- the mirror of RGV's 785xx and PNW's west-side fence, but
  load-bearing here: without it, 21 Southcentral and Kodiak ZIPs get a panhandle calendar.
- `regions.json` row + `SHORT_REGION_LABEL.se_alaska`.

### 9.2 The blocker the app side must fix first (NEW finding, 2026-07-20)

**`plant-app/src/lib/zones.ts` only resolves regions for zones >= 8** (`isWarmZone`), and only for
regions flagged `isWarm: true` in `regions.json`. Consequences:

- A `se_alaska` region spanning z7-8 would deliver **only its z8 half** in-app until this is
  generalized -- Juneau and Sitka would still get generic dates.
- Flagging `se_alaska` as `isWarm: true` to work around it would be a lie in a user-facing taxonomy
  ("warm climate region") about a place that is not warm.
- **The same bug already strands `northern_tier`**, which carries real authored z3-7 data for the whole
  roster and `isWarm: false`, and therefore never ZIP-resolves at all. Every cold-zone user in the
  dataset's coverage is on generic dates today despite the data existing.

The fix is to **decouple "has an authored region" from "is a warm-climate region"** -- `isWarm` should
drive labeling and chip presentation, not whether region resolution runs. That is a plant-app change,
sized independently of this arc, and it unlocks `northern_tier` as a bonus. **Write it up as its own
plant-app kickoff and add it to roadmap item 2**; it is a precondition for this region delivering its
z7 half, not a blocker on the dataset build.

### 9.3 The variety-card caveat

`recommended_varieties` (4.5) names varieties that are deliberately absent from `variety_detail`. The
app and plant-astro must render them as a named steer, not as links to detail cards that do not exist.
Call this out explicitly in the handoff (memory `dataset-shape-change-breaks-frontends`: grep consumers
and build plant-astro after any bump).

No plant-astro bump from this session (memory `plant-astro-bump-owned-by-astro-session`).

## 10. Non-goals

- No new `calendar_basis`, no deriver change.
- No `heat_accumulation` extension to deciduous trees (4.6) -- registered as a follow-on.
- No `protected_culture` backfill to `northern_tier` or anywhere else (4.4) -- follow-on column pass.
- No variety-detail authoring for the UAF apple set.
- No re-authoring of existing regions; `se_alaska` is purely additive.
- No plant-app or plant-astro code changes here.

## 11. Risks / open items

1. **The chill band has no located source (4.8).** Highest sourcing risk; hunt it first, escalate
   rather than guess.
2. **z7 frost normals** still need extraction from the NWS AJK table (mechanical, low risk).
3. **Two new fields plus two new gates in one arc.** Real scope. Mitigation: both follow an existing
   flat conditional-field idiom with a working precedent (A44/`planting_layout`), both are shape-only
   gates, and both are RED-proofed before authoring. If either proves contentious in build, the
   fallback is prose-only in `suitability_note_*` / `zone_notes` -- but the spec's position is that
   prose-only reproduces the exact dishonesty the NEW-REGION ruling identified, so the fallback should
   be escalated to Trevor, not taken silently.
4. **Small absolute ZIP count** (28 panhandle ZIPs). This region is a correctness and authority play,
   not a volume play, and the roadmap has already accepted that framing. Worth stating plainly in the
   release notes so nobody later reads the effort-to-ZIP ratio as a mistake.
5. **Per-crop T1 coverage for 111 crops from one belt publication.** HGA-00231 is strong but will not
   cover everything. Expect a meaningful tail of conservatively-authored, flagged cells. That is the
   honest outcome, not a failure.
6. **z7/`northern_tier` span overlap** (4.2) -- benign, but document it so it is not later read as a
   defect.

## 12. Acceptance criteria / definition of done

- `se_alaska` authored + certified across the 111 roster; `zone_span = ["7", "8"]`.
- A46 + A47 written RED-first, wired into `whole_crop_gate`, RED proofs documented.
- A45 / A31 / A32 / A3 + `gate_all` 119/119 + `chill_gate` 0 + `calendar_coherence` 0 +
  `release_verify` clean + pre-commit backstop no-regression.
- Footprint EXACT (111 `regions.se_alaska` + chill band + provenance + `source_catalog` additions;
  0 other keys; count 128; COMPACT).
- State trio updated (CURRENT_STATE.md regenerate + prose slots, STATE_HISTORY.md prepend, LATEST.txt
  bump); roadmap item 7 -> SHIPPED; field register rows added (the region column, `protected_culture`,
  `recommended_varieties`, and the queued `heat_accumulation` follow-on).
- plant-app kickoff written: `REGION_STATES.se_alaska`, the 998/999 fence, the variety-card caveat,
  and **the `isWarm` decoupling** (9.2) as its own item.
- Dataset committed + PUSHED (Trevor confirms push); NO plant-astro bump from this session.

Then item 7 closes and the region program is down to items 8-11 (mid-Atlantic, mid-South, Nevada,
Utah -- all now full region builds per Trevor's 2026-07-16 ruling) plus item 6 (Puerto Rico, a product
call) and item 2 (the app-side cleanup).
