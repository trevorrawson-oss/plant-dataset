# PLA-462 scoping report -- artichoke's and asparagus's four-key problem entries

**Date:** 2026-09-06. **Lane:** Claude Code, read-only. **Canonical:** `72371c02`, unchanged.
Nothing authored, nothing backfilled; three questions answered.

## a) Deliberate or drift? Both, at different times, and neither cert record says so

**The shape was authored at cert, not eroded afterwards.** The full revision trace of both crops'
problem arrays:

| revision | date | artichoke | asparagus |
|---|---|---|---|
| initial commit | 2026-05-13 | 3 entries, 7 keys (cause, symptoms, prevention, severity, type, organic_treatment, name) | 4 entries, same 7 keys |
| schema 2.7 | 2026-05-25 | + `audience` | + `audience` |
| register split | 2026-06-01 | 12 keys: every prose field in both registers | same |
| author-fresh pivot `c371c62` | 2026-06-08 | **0 entries** (120 non-GS crops reset) | **0 entries** |
| GS cert `ced0499` / `da25947` | 2026-07-28 / 2026-07-24 | **11 entries, 4 keys: id, type, name, control_ladder** | **5 entries, 4 keys** |
| today | | unchanged | unchanged |

So the pre-pivot draft prose existed and was deliberately discarded with the other 120 crops, and
the two herbaceous-perennial GS certs re-authored the pest section from scratch as **name plus
ladder**, with the organism in the display name because no `cause_*` field was authored to hold it.
`control_methods` already existed at those certs (37 methods), which is why these two are the only
crops whose ladders PREDATE PLA-8 and were authored from source reads rather than restated from
prose. The asparagus cert entry in STATE_HISTORY records the design in passing ("Fuller IPM: added a
cutworm insect ladder + a purple-spot disease ladder to the beetle/rust/Fusarium set"); neither
crop's `verification_log_ref` mentions the pest section at all (0 sentences on artichoke, 2 incidental
on asparagus).

**Against the standard it is drift.** The gold-standard arc checklist v2.0, Appendix A, lists
`pests` / `diseases` prose as `symptoms`, `cause`, `organic_treatment`, `prevention` with `severity`
and `type`, and `gs_exemplar_finding_004` makes a missing `cause_beginner` a Step 8 finding. The two
certs departed from that field set and no record of the departure exists. PLA-8 then set the
roster-wide standard at prose PLUS ladder (the other 897 entries carry 8 to 16 keys, 13 to 16 on
every laddered entry authored since), and nothing reconciled the two earlier certs to it.

**Verdict: a deliberate authoring choice at cert that is undocumented, and drift against both the
checklist that governed the cert and the standard PLA-8 later set.** There is no documented variant
to point at, so the honest classification is backfill.

## b) Does any gate skip these entries silently? Yes, by construction, and it was proved by injection

Read: the anchoring-completeness walk in `whole_crop_gate` (section F) keys on
`isinstance(srcs, list) and srcs`, so an entry with NO `sources` key and an entry with an EMPTY
`sources` array are both skipped; the source-tier walk (section E) only validates ids that ARE
cited; `control_ladder_gate` checks `control_methods` sources, not problem entries;
`register_completeness_gate` rules on prose fields that are PRESENT and cannot see absent ones;
`perennial_gate` checks `pollination.sources` only. **No gate requires a problem entry to carry
`sources`, `cause`, `symptoms`, `prevention` or `severity` at all.**

Proved on a scratch copy of canonical, artichoke's gray-mold entry, `whole_crop_gate artichoke`:

| injection | result |
|---|---|
| A. as shipped (no `sources` key) | PASS, 0 violations |
| B. `sources: []` | PASS, 0 violations |
| C. `sources: ["not-a-catalog-id"]` | 2 violations (source-tier, anchoring) |
| D. bogus id with an anchoring dict | 1 violation (source-tier) |
| E. `sources: ["uc_ipm"]`, no anchor | 1 violation (anchoring) |
| F. `cause_*` prose added, still no `sources` | PASS, 0 violations |

C, D and E prove the instrument is live for the shape it checks; A, B and F prove the shape it
does not check. **A problem entry can carry full prose with no source and pass every gate.** This is
the fifth instrument-blindness finding of the arc, after the microgreen `name` key, the
list-versus-dict variety walk, the collision suite's stale pin, and the promote suites reading the
live registry.

Recommendation for the fix, not for now: when the 16 entries are backfilled, arm a
problem-entry-level floor the way A57 was armed for ladders (every entry on a certified crop carries
`sources` non-empty and the register prose), measured green on the backfilled roster before wiring,
and grep every caller first, since 29 promote suites replay historical states where such a floor is
correctly violated.

## c) What does the backfill cost? Two sessions

The 16 entries need, per entry: `cause`, `symptoms`, `prevention` in both registers (6 strings),
`severity`, `audience`, `sources` and `anchoring_urls` against T1 reads. That is 96 register strings
plus 16 sourced records, at the per-crop verification bar, on two crops whose `source_set` already
holds 21 and 26 catalogued sources including UC IPM's artichoke and asparagus guideline sets.

Comparable measured work: batch 25 (7 herbs, 36 problems, 22 unsourced records brought to sourced,
293 changed leaves, catalog admission) took one session plus a second promote. This is 16 problems
on 2 crops, no ladders to author, but every prose field from nothing, and two things batch 25 did
not have:

1. **A new promote shape.** Every PLA-8 promote ADDED `id`, `type` and `control_ladder` to entries
   whose prose it carried byte-for-byte. This one adds prose to entries whose ladders already exist,
   so the promote must also prove the new prose agrees with the shipped rungs (a ladder restated
   from prose that did not exist yet cannot be checked the usual way round).
2. **The independent source-truth pass** the playbook requires, which on batch 24 sent 71% of the
   content back.

Estimate: **one session** to fan out two authoring agents, read, promote, suite and harness;
**half to one session** for the independent source-truth pass and any re-authoring it demands.
**Call it two sessions, its own slot**, sequenced before PLA-453 (blocked on this for these two
crops) and before PLA-12 (its consumer), and after PLA-457 (which touches none of these entries).
