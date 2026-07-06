# §B/§C offline pass -- spelled-degrees cleanup + non-null-URL gate -- design spec

**Date:** 2026-07-06
**Author:** Claude Code (brainstorming session, Trevor-ratified decisions inline)
**Status:** design approved; ready for implementation plan (writing-plans)
**Backlog items:** post-114 §C (spelled-degrees -> `°F` + gate C/D hardening) + the OFFLINE half of §B
(non-null-URL gate). The §B **online liveness sweep** is explicitly deferred to a follow-on (below).

---

## 1. Goal

One roster-wide **offline** pass that (a) normalizes user-facing spelled temperature forms to `°F`,
(b) hardens the gate so spelled temps can't regress, and (c) adds an offline **non-null-URL** gate --
without touching the network. The network-heavy URL liveness sweep is a separate, later effort.

## 2. Scope scan findings (2026-07-06, offline)

**§C spelled-degrees -- 11 real crops + 1 trap.**
- Genuine temperature fixes (convert to `°F`): **beefsteak-tomato, bok-choy, cherry-tomato, grape-tomato,
  roma-tomato, lettuce-leaf, orange-navel, pear-european, raspberry, strawberry, tomatillo** (~117 hits;
  forms like "90 degrees", "50 F", "17 degrees Fahrenheit", "70 to 80 degrees", "60-65 degrees").
- **onion is a FALSE POSITIVE:** its "38 to 39 degrees" / "below 35 degrees" / "32 to 42 degrees" are
  **latitudes** (day-length / photoperiod context), NOT temperatures. Do NOT convert. (Trevor: "don't
  want to leave that hanging" -- onion is handled in THIS pass by *clarifying* the phrasing to read
  unambiguously as latitude, and the hardened gate excludes latitude so it can't false-flag.)
- green-beans-bush (named in the kickoff) did NOT surface in the scan -- re-verify it during the sweep.

**§B URL health -- the live layer is already clean; the nulls are legacy.**
- 20,224 anchoring-url *entries* dedupe to **1,030 distinct URLs** (the rest is region/zone-cell replication).
- **57 null URLs -- every one in the legacy `zones{}` layer** (7 source keys: `uga_b577`, `sdsu_ext`,
  `mu_ext`, `cornell_ext`, `uf_ifas_nwdistrict`, `uc_mg`, `uf_ifas_south_cal`). The current `regions{}`
  layer has **zero** nulls; gate F excludes `zones{}` by definition.
- **"Fill the nulls from source_catalog" would be LESS accurate, not more:** 18 of the 57 are `uga_b577`,
  whose catalog URL is the exact **dead B577 PDF** the kickoff flags; `mu_ext`/`sdsu_ext`/`uc_mg` are bare
  homepages. Backfilling would spread a dead link + three bare roots into 57 cells. The accurate fix is to
  repoint the *sources* to live pages -- the deferred liveness sweep's job.
- 24 distinct bare-homepage URLs, mostly legitimate regional/extension roots used as calendar anchors.

## 3. Ratified decisions (Trevor, 2026-07-06)

1. **Scope: offline pass now; defer the online liveness sweep.** This pass = §C fixes + gate hardening +
   the offline non-null-URL gate. The 1,030-URL WebFetch liveness sweep is a separate follow-on session
   (large fan-out; WebFetch has been flaky per the standing flags).
2. **Leave the legacy `zones{}` nulls alone.** Do not backfill them (would spread the dead `uga_b577`).
   Scope the non-null-URL gate to the LIVE layers (`regions{}` + claim/top), excluding legacy `zones{}`.
   Log the 57 nulls (esp. `uga_b577`) as work for the liveness sweep.
3. **onion: clarify, don't convert.** Its degree references are latitude; make them read unambiguously as
   latitude; the gate excludes latitude/angle forms.

## 4. §C -- spelled-degrees normalization contract

**Target (user-facing strings ONLY -- `is_backend(key, path)` false):** convert spelled temperature forms
to the canonical `°F` (CLAUDE.md render rule; American English; no em dashes):

| Found | Becomes |
|---|---|
| `90 degrees` | `90°F` |
| `50 F` (bare, no degree sign) | `50°F` |
| `17 degrees Fahrenheit` | `17°F` |
| `70 to 80 degrees` | `70 to 80°F` |
| `60-65 degrees` | `60-65°F` |

**Do NOT convert (leave or clarify):**
- **Latitude / angle:** onion's `38 to 39 degrees` etc. are latitude. Clarify to `38 to 39°N` (and the
  `35 degrees` / `32 to 42 degrees` siblings likewise) -- **NOT** `°F`. `°N` is confirmed SAFE against the
  existing gate D (its `_DEGF_RE` only matches `degrees F` / `deg F` / `° F`, none of which `°N` triggers),
  and once onion is the only latitude case is clarified, no bare "NN degrees" latitude text remains.
- Backend / non-rendered fields (`is_backend` true) -- CONSUMER copy only.
- Any string already carrying `°F` correctly.

Each converted crop is a normal content edit; batch them into one SHA-guarded promote (§7).

## 5. §C -- gate hardening (so spelled temps can't regress)

The current check is `whole_crop_gate` C/D (line ~730): `_DEGF_RE =
\bdegrees?\s*F\b | \bdeg\.?\s*F\b | °\s+F`. It is too NARROW -- it catches `degrees F` / `deg F` / `° F`
but MISSES `90 degrees`, bare `50 F`, and `17 degrees Fahrenheit` (the forms that actually shipped).

**Harden it** (extend `_DEGF_RE` in `whole_crop_gate` C/D, and the equivalent scan in `release_verify` --
the plan pins both via TDD) to also flag, in a user-facing string:
- `\d+\s*(?:to\s*\d+\s*)?degrees?\b` (a number followed by spelled "degrees"), and
- a bare `\b\d{2,3}\s*F\b` (a temperature number followed by a lone `F`, no degree sign).

The corrected `°F` forms do NOT match either branch (`70 to 80°F` has no "degrees"; `50°F` has `°`
between the digits and `F`), so the fix passes cleanly.

- **Latitude/angle exclusion (belt-and-suspenders):** also skip `°[NS]`, `degrees?\s*[NS]\b`,
  `degrees?\s+(of\s+)?latitude`. After onion is clarified to `°N` no bare-degrees latitude text remains,
  so this exclusion is future-proofing, not load-bearing.
- **TDD (RED before GREEN):** inject `"warms to 70 degrees"` and `"nights below 50 F"` into a scratch cell
  -> the gate bounces; inject `"grows above about 38°N"` and `"the ideal 70 to 80°F range"` -> the gate
  PASSES (no false flag). Confirm all 11 converted crops + clarified onion pass after the edit.

## 6. §B -- offline non-null-URL gate

New `tools/url_health_gate.py`, gated by **exit code**, **offline only** (never hits the network):

- **Check:** for every crop, every `anchoring_urls[key]` in the **LIVE layers** -- `regions{}` and the
  claim/top-level layer (e.g. `storage.anchoring_urls`, `pet_safe.anchoring_urls`, `*_anchoring_urls`) --
  has a **non-null, non-empty `url`**. The legacy `zones{}` layer is **EXCLUDED** (matches gate F's
  scoping).
- **Report:** counts of live-layer anchoring entries checked + any null offenders (0 expected -- the live
  layer is already clean, so this is regression-prevention).
- **Network liveness is OUT of scope here** -- reserved for a future `--online` mode (documented stub;
  the pre-commit gate stays offline).
- **TDD (RED before GREEN):** inject `{"url": null}` into a `regions{}` cell of a scratch copy -> bounces;
  a `zones{}`-only null -> does NOT bounce (legacy excluded); the clean canonical -> exit 0.

## 7. Promote

- Only the corrected **§C crop slugs** change in `crops_data_final.json` (11 temperature crops + onion's
  latitude clarification). The gates (`url_health_gate.py`, the hardened temperature scan) + their tests
  are tooling.
- **SHA-guarded:** build from the current base SHA, assert EXACTLY the intended §C slugs changed (all
  other crops + every top-level key byte-identical), re-check the canonical SHA before `cp` and commit.
- Canonical stays COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline).
- Full release suite: `whole_crop_gate` on the changed slugs (0), `url_health_gate` (0),
  `register_completeness` (0), `release_verify` per slug (0 NEW concerns vs base). State trio. Trevor
  confirms the push.

## 8. Out of scope / follow-on

- **The §B online liveness sweep** (its own session): WebFetch the 1,030 distinct URLs, classify
  live / 404 / redirect-loop / logo-or-empty-PDF / bare-homepage-on-a-specific-claim, repoint the real
  offenders (`uga_b577` dead PDF, the citrus TAMU redirect loops, lime's bare `ucanr.edu`, the generic
  cucumber B577 logo-PDF), and only then (if still wanted) backfill the legacy `zones{}` nulls. The
  `url_health_gate --online` mode is built there.
- The §D `rhs` tier ruling (already answered in principle by the §A ASPCA decision -- a non-`.edu`
  authority is admissible for the claim it is the authority on; apply to sage / broad-beans-fava later).

## 9. Hard-rule compliance

- READ-ONLY on `crops_data_final.json` until the §7 promote; interim work on a scratch copy.
- Gate by EXIT CODE, never by grepping output.
- Any new/hardened gate is TDD: RED before GREEN (the injections in §5, §6).
- SHA-guard the promote (assert exactly the §C slugs changed); canonical COMPACT; Trevor confirms push.
- Research via WebFetch/WebSearch ONLY -- never curl/wget/pdftotext. NEVER `dangerouslyDisableSandbox`.
- No em dashes in consumer copy; American English; temps render as `°F`; "plant" lowercase.
