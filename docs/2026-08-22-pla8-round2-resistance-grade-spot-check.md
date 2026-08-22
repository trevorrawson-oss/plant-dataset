# PLA-8 Round 2 -- resistance-grade spot check (the R0-INVERTED prerequisite)

**Date:** 2026-08-22
**Canonical:** `20a32c47...` (unchanged; this pass wrote no dataset byte)
**Why:** the corrected Layer 1 turns 37 `susceptible` grades into consumer-facing NEGATIVE claims
("this variety is not resistant to X"). A wrong grade becomes a wrong sentence on a live guide page,
so the grades had to be checked before that class is generated.

## VERDICT: no wrong grade found. R0-INVERTED is safe to generate.

---

## 1. Ledger vs shipped: 62/62 exact

`tools/staging/resistance_sources.md` records per-grade provenance with the source row quoted.
Parsed and reconciled against canonical:

| check | result |
| -- | -- |
| ledger graded pairs | 62 |
| shipped graded pairs | 62 |
| in ledger, not shipped | **0** |
| shipped, not in ledger | **0** |
| grade disagreements | **0** |
| `susceptible` grades carrying ledger evidence | **37 of 37** |

**No grade was defaulted.** 33 of the 37 susceptible grades cite two or three independent tables
(Cornell Apple Variety Database + Purdue BP-132-W, often + Cornell Khan Lab); the remaining 4 cite a
named single table row.

> **Parser caution for anyone re-running this.** My first reconciliation reported 6 grade
> disagreements and 13 set mismatches. **All 13 were my own bug**: five ledger headings carry a
> trailing annotation (`## gala  (DOCUMENTED-SUSCEPTIBLE SHOWCASE for apple scab)`), and an
> end-anchored `^##\s+([a-z0-9-]+)\s*$` skipped them, bleeding their bullets onto the previous
> variety -- which is why an *apple* appeared to carry red-stele grades. Match `^##\s+([a-z0-9-]+)\b`
> and reset the variety at each `# APPLE` / `# STRAWBERRY` / `# N/A branch audit` boundary.

## 2. Independent verification against the live sources

Fetched raw and parsed **by cell structure, never by markdown reflow** (a markdown parse of an HTML
table silently shifts columns -- the defect this very ledger caught once already).

**Cornell Apple Variety Database** (133,830 bytes, 330 rows). Header confirmed as
`Name | Fire blight | Apple Scab | Powdery Mildew | Cedar Apple Rust | Leaf Spots`.

- **The three least-corroborated grades verified EXACTLY**, including the blank cells that caused the
  original defect: `Dorsett Golden`, `Anna` and `Ein Shemer` each read Apple Scab = `Susceptible`
  with Fire blight **blank**. The ledger's own correction ("the earlier Susceptible fire-blight grade
  misread the adjacent apple-scab/leaf-spots Susceptible into the blank fire-blight cell") holds.
- Gala, Golden Delicious, Fuji, Granny Smith, Pink Lady, Jonagold, Empire, McIntosh all verified.
- `Honeycrisp` and `Mutsu` are **not in this table** (Mutsu is listed as `Mutsu (Crispin)`);
  Honeycrisp's four grades rest on Purdue/Khan, not the primary DB.

**UMN Extension, apple scab page** -- the single most consequential grade in the dataset, and the
only `immune` anywhere in it, verified **verbatim and live**:

> "Immune to apple scab: Dayton, Freedom, **Liberty**, McShay, Pixie Crunch, Pristine, Redfree,
> William's Pride."

The same page independently states the Layer-1 DROP rule itself:

> "**Do not use fungicides: On apple and crabapple varieties that are resistant or immune to apple
> scab.**"

That is a T1 extension source stating the delta mechanism in its own words, not merely the grade.

**Purdue BP-132-W** (268,918 bytes, read with pypdf -- WebFetch cannot decode PDFs).
Legend `VR/R/MR/MS/S/VS`. **Column order verified empirically rather than assumed**: the leaflet's
intro prose lists the diseases as *scab, fire blight, powdery mildew, juniper rusts*, but the table's
real order is *scab, fire blight, **rusts**, **mildew***. Proof: Empire `VS R R S` and Jonagold
`S VS R S` match the Cornell DB on all four columns under that order and contradict it under the
prose order. The ledger's stated column order was right.

## 3. The one real finding: 6 grades rest on a SPLIT primary cell

The ledger's omit rule says a grade is omitted "when a single table's cell is internally split (e.g.
'Resistant, Susceptible')". Six shipped grades sit on Cornell cells that are split across the
resistant/susceptible line, and the ledger quoted them in **abbreviated** form (recording
`"Resistant"` where the live cell reads `"Resistant1; Susceptible2, 3"`).

Adjudicated against the second primary table:

| variety | disease | shipped | live Cornell cell | Purdue | verdict |
| -- | -- | -- | -- | -- | -- |
| mcintosh | fire-blight | susceptible | `Moderately Susceptible1,2; Moderately Susceptible4; Susceptible7,9; Resistant7,8` | S | **corroborated** |
| mcintosh | powdery-mildew | tolerant | `Moderately Resistant1; Susceptible2, 3` | MR | **corroborated** |
| liberty | fire-blight | tolerant | `Moderately Resistant1,2,3,4,9; Moderately Susceptible4; Resistant5,6,7,8` | R | conservative (softer call kept) |
| liberty | powdery-mildew | resistant | `Resistant1; Susceptible2, 3` | R | **corroborated** |
| empire | fire-blight | tolerant | `Moderately Resistant1,2,3,4,9; Moderately Susceptible4; Intermediate5; Resistant7,8` | R | conservative (softer call kept) |
| jonagold | fire-blight | susceptible | `Highly Susceptible1,4, 7,9; Moderately Susceptible2,4; Resistant8` | VS | **corroborated** |

**Every one is independently corroborated.** The two "conservative" rows are the ledger choosing
`tolerant` where Purdue supports `resistant` -- erring toward KEEPING a control step, which is the
safe direction for an IPM ladder.

**So the grades are sound; the defect is transcription fidelity and a rule stated more strictly than
it was practised.** These cells are multi-reference compilations (footnote digits mark different
published sources), not the bare `"Resistant, Susceptible"` two-value split the omit rule's example
describes. Recorded, not silently fixed.

**Recommend:** amend the omit rule to distinguish a bare split cell (omit) from a multi-reference
compilation (adjudicate by the second table, record the split verbatim). Do NOT retro-edit the six
grades -- they are corroborated, and the two conservative ones are conservative in the right
direction.

## 4. Consequence for the delta classes

- **liberty / powdery-mildew** was the only split cell driving a **DROP** of a control step; Purdue
  rates it `R`, so the drop stands.
- Only **2 of the 37 R0-INVERTED** claims (mcintosh + jonagold fire-blight) rest on a split cell, and
  both are corroborated `S` / `VS`.

**R0-INVERTED, R0-SATISFIED, DROP and SOFTEN are all cleared to generate.**

## 5. Noted in passing, not acted on

- **UMN lists Honeycrisp under "Resistant to apple scab"; we ship `tolerant`** (from Purdue's `MR`).
  A defensible conservative call, but it is a live source disagreement on a variety the primary
  Cornell table does not cover at all. Worth a look during authoring.
- UMN corroborates `zestar` and `mcintosh` scab as susceptible ("Very likely to be infected").
