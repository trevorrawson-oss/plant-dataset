# PLA-673 part D promote bundle (base aaf004a2)

One promote covers three things:
- **Peppers (PLA-688):** the `diseases[id=phytophthora-blight]` entry, re-authored whole from NC State's factsheet. It is identical on bell-pepper and banana-pepper.
- **Watermelon's row entry:** re-sourced to UF VH021, with its crop-root mirror.
- **Watermelon's thinning leaves:** re-authored in both registers (part D ruling, option a).

The bundle also updates the shared match fixture.

## Run (Trevor's go; Claude Code runs it)

```
python3 tools/promote_pla673_d.py --check
python3 tools/promote_pla673_d.py --expect-sha 5420479d85bb8b65be62fa459fd97b8ce12dfdf9d3951e455be52aadc7a98063
```

The post SHA `5420479d` is pinned three ways, and they agree:
- build_stage.py's INDEPENDENT minimal apply (no promote code);
- the promote's `--out`;
- the suite's `POST_SHA`.

## Contents

| file | what |
|---|---|
| `d_texts.py` | the approved texts, VERBATIM, each sentence mapped to packet rows (PP pepper, C part C) or to the watermelon thinning quotes (W); the ruled sources per citation block |
| `build_stage.py` | writes ops.json / EVIDENCE.tsv / DECISIONS.tsv; prints the independent post SHA |
| `ops.json` | 50 ops: prose 39, value 3, sources 4, anchors 4 |
| `EVIDENCE.tsv` | 176 rows; every quote proven a substring of the cached page bytes |
| `DECISIONS.tsv` | 12 rows: the layout-consensus rule; the thinning cut and the `method` set (free text); `to_spacing` kept; per pepper: sources removed, fixed copper omitted, the drainage-as-response claim cut, the rung id kept |
| `derive_promote.py` | the asserted edit list that derived `tools/promote_pla673_d.py` from `promote_pla673_b2.py` |

## What changes

**Watermelon.**
- `planting_layout[id=row-none]`: in_row [60,72] → [24,48]; rows [72,96] → [60,60]; sources [clemson_hgic] → [uf_ifas].
- Crop-root `spacing_inches` [60,72] → [24,48], the mirror of the first entry carrying `in_row_inches`. `row_spacing_inches` [96,96] stays: it mirrors the default hill entry.
- `thinning.tip_seasoned` / `tip_beginner`: 3 + 3 sentences.
- `thinning.method` "snip extras at soil line" → "thin to two plants per hill".
- Thinning sources [usu_ext, umn_ext] → [usu_ext, umn_ext, uga_ext, uf_ifas].

**Peppers (each).**
- 57 sentences across symptoms, cause, organic treatment and prevention, in both registers, plus the 5 control-ladder rungs. The part D block said 58; the approved text has 57.
- Sources [ncsu_ext, clemson_hgic] → [ncsu_ext_phytophthora_blight_peppers, umn_ext].

**Pages.** USU watermelon (2618f2f2, browser UA only) and UMN melons (9e2a61b5) hashed: MANIFEST +2. No catalog change.

## Tools landing with the data commit

- `promote_pla673_d.py` (guards B V P D E A C R M G, plus I identical entries and X mirror).
- `test_promote_pla673_d.py` (47 tests) and `mutate_promote_pla673_d.py` (**41/41 caught**, sentinel red, positive control green).
- `promote_fixture.py`: `aaf004a2 → 6bce088` (pin-only).
- `test_glossary_sense.py`:
  - live pins 225 → 224 (103 hill / 60 hilling / 61 none);
  - the D8 test now pins an EMPTY pepper/eggplant population;
  - NEW: the shared fixture runs against the canonical glossary (35 cases, sha pinned);
  - NEW: every `refuse_on` pattern drives exactly its sole case, or is waived as unreachable.
- `live_pin_registry.py` and its test: population 67/26/70/48.
- `test_problem_id_collision_gate.py` re-pinned to 5420479d; the gate's output is byte-identical to aaf004a2.

## Match fixture

`../pla673_674_prep/glossary-match.fixture.json`: **sha256 `e075f0f8e915aff14b106b0cd29b5132ab7cbf5060db8d136dc9ab07dbb61f84`** (5,620 B, 35 cases; was 990eac25, 32 cases).

**Pepper case.** `none-pepper-beds-or-hills-pending-b2` becomes `pepper-prevention-reauthored-part-d`, with the new sentence and expect `[]`.

**Three new cases**, each the sole case of its `refuse_on` pattern:
- `refuse-in-hills-on-potato` → `\bin\s+hills\b`
- `refuse-hills-spaced-on-carrot` → `\bhills?\s+(spaced|apart)\b`
- `refuse-seeds-in-each-hill-on-sweet-corn` → `\bseeds?\s+(in|to)\s+(a|each)\s+hill\b`

With the two that were already covered (`hill(ed|ing)? soil|up|mulch` → pumpkin, `per hill` → corn), **5 of 7 patterns are exercised alone**.

**Two patterns are UNREACHABLE as a sole cause:** the hill term's `\bhilled\b` and `\bhilling\b`.
- The hill term's forms are only hill / hills.
- Any sentence those patterns match also holds a hilled / hilling occurrence, which refuses on its form whatever the pattern says.
- No exclusion span covers those words.
- So no refuse-only case can ever fail when either is removed. The test waives the pair by identity and fails as STALE if that ever changes.

These need a ruling. The options are to remove the two dead patterns (a glossary change), or to extend the fixture shape with per-occurrence refusal expectations.

## Checks

- Evidence: 176 rows, all proven against hashed bytes (the promote's guard E reads every one).
- Dual register: all 10 pairs differ, with 0 shared sentences in any pair.
- A62: the waiver set is unchanged at 2663. Every block part D touches was already cited.
- Gates on 5420479d:
  - promote gate step: whole_crop_gate PASS on the 3 crops, gate_all PASS;
  - release_verify clean (only the 3 declared crops; catalog unchanged);
  - doc_roster_claim_gate 0 with the LATEST line below;
  - export staleness: E1 red until `build:guides` reruns after the promote, E3 the astro pin.

## Proposed LATEST.txt

```
SHA: 5420479d85bb8b65be62fa459fd97b8ce12dfdf9d3951e455be52aadc7a98063
Date: 2026-10-06
Session: PLA-673 PART D LANDED: aaf004a2 -> 5420479d. Pepper Phytophthora blight entry (PLA-688) re-authored whole from NC State's factsheet, identical on bell-pepper and banana-pepper (57 sentences per crop; sources ncsu_ext_phytophthora_blight_peppers + umn_ext; the ncsu_ext index page and clemson_hgic off the entry; fixed copper omitted, home gardens have no effective chemical option). Watermelon row entry re-sourced to UF VH021 only, in_row [24,48], rows [60,60], crop-root spacing_inches mirror [24,48] (RULED: one T1 source inside the consensus of the cited sources; Clemson 60-72 x 72-96 and OSU 60 x 72 recorded as the wide end). Watermelon thinning re-authored in both registers (four to five seeds per hill, thin to the strongest two at two leaves, 24 to 48 inches in rows; USU, UMN hashed; method 'thin to two plants per hill'). 176 evidence rows. Sense guard 224 leaves (103 hill / 60 hilling / 61 none); match fixture e075f0f8 (35 cases; 5 of 7 refuse_on patterns exercised alone, the 2 hill-term ones unreachable). A62 waiver set unchanged at 2663. Certified 121, launch-ready 114. Record: tools/staging/pla673_d/, Linear DECISIONS section 14; PLA-700 filed (rung label, catalog level).
```
