# Remediation Corrections Log (accumulate during gate work, fix in ONE pass at the end)

**Purpose.** The gate-hardening arc (B1..B5) stays READ-ONLY on `crops_data_final.json`.
Each gate surfaces data tensions as a byproduct; we LOG them here instead of fixing them
one-off. After the gates are built, claude.ai authors all corrections in ONE source-verified
authoring batch (Tier-1 extension sources), Claude Code promotes + gates, and we update
`CURRENT_STATE.md` / `STATE_HISTORY.md` once.

**Two-for-one.** Several corrections UNLOCK a stronger gate (the data tension is the only
reason the gate had to be loosened). Those are flagged "GATE-UNLOCK" -- after the fix lands,
tighten the named gate.

**Process per remediation session:** append what your gate surfaced; do NOT edit the JSON.

---

## From B1 (A24 annual calendar token placement) -- 2026-06-25

All are display-vs-calendar tensions in CERTIFIED crops. Not biology-wrong, not gate-blocking.
A24 deliberately does NOT flag cold-pause-on-harvest precisely because these cells would
false-positive. **GATE-UNLOCK:** once corrected, add a cold-pause-on-core-harvest rule to
`annual_calendar_violations` (A24).

| Crop / cell | Tension | Correction question + source to check |
|---|---|---|
| `broccoli` northern_tier.z5 | harvest `"May 26 - Oct 29"` (continuous) but calendar Jul = `cold_pause` | Split harvest display into spring + fall windows matching the calendar; is the summer gap `cold_pause` or heat-driven (`heat_pause`/`growing`)? Source: northern-tier extension broccoli calendar (UMN/USU). |
| `broccoli` northern_tier.z6 | harvest `"May 12 - Nov 14"` but calendar Jul = `cold_pause` | same as z5 |
| `broccoli` northern_tier.z7 | harvest `"Apr 26 - Dec 4"` but calendar Jun/Jul/Aug = `cold_pause` | same as z5 (3-month summer gap; continuous Apr-Dec harvest is wrong for z7) |
| `beefsteak-tomato` ca_south_coast.z9 | harvest `"Jul - Dec"` but calendar Dec = `cold_pause` | AMBIGUOUS direction: mild coastal SoCal rarely hard-freezes in Dec, so the `cold_pause` token may be the error (harvest really runs through Dec) rather than the display. Resolve with UC ANR before fixing. |

Note: the broccoli summer-gap relabel touches the `heat_pause` layer -- coordinate with B3
(heat_pause backing) so a relabel to `heat_pause` ships WITH its backing, not before.

---

## From the audit §3 (the ~14 MINOR date nits, 2026-06-25) -- to merge into the same batch

Same-season, ~3-6 weeks, none severe (0 wrong-season across 64 sampled cells).

| Crop / cell | Nit | Source |
|---|---|---|
| `onion` fl_peninsula z10/z11 | North-FL Sep-Dec window applied to South FL; the Nov-Dec tail is ~1-2 months late for S-FL bulbing (UF-IFAS South lists "Oct") | UF-IFAS South FL EP452 |
| `beefsteak-tomato` se_gulf z8 | Sep `plant` token ~6-8 weeks past UGA's fall window (Jun15-Jul15) and inconsistent with its own plant_out (Jul 1-20) | UGA C963 |
| `green-beans-bush` northern z3 | Jul 15 back-edge sow matures ~1 week before Sep 15 frost; UMN caps northern-MN beans at end of June (~2-3 wks optimistic) | UMN |
| `carrot` northern z3 | Apr-Jun plant tokens have no corresponding summer harvest window (only the Jul sowing reaches Sep-Oct); Apr token early for z3 cold soil | UMN/USU |
| low-desert AZ warm crops (tomato, beans) | fall succession set ~3-5 weeks later than AZ1005's Jul-Aug | UA AZ1005 |

---

## From B3 / B4 / B5 -- (append as those gates surface tensions)

_(empty -- fill in during the B3/B4/B5 session)_
