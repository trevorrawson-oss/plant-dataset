# §B online URL-liveness sweep -- finish the 114 cleanly

**Goal:** run the deferred **online half of §B** -- fetch every distinct cited URL, classify it live vs
dead/redirect/logo-PDF/bare-homepage, repoint the real offenders, ship a `url_health_gate --online`
mode, and then (only then) backfill the 57 legacy `zones{}` nulls. This is the last data-quality item
on the 114; when it lands, the roster's citations are verified-live end to end.

This is a **big, network-heavy session** (~1,053 distinct URLs). Budget context accordingly; it is the
whole reason to run it in a fresh chat.

---

## Position (2026-07-06, at kickoff)
- Canonical **`8e568c5b`** (full: `8e568c5b5db43879b292ffdaf955641eca56f3e03a84c096b26abdbb5fea5743`).
- `origin/main` == **`6100c2d`** (everything through the pet_safe rollout is pushed + in sync).
- Everything else post-114 is DONE: §A pet_safe (pilot + full rollout, 39 warnings / 75 safe),
  §C spelled-degrees + gate hardening, §B **offline** non-null-URL gate.
- Not this session: the plant-astro icon (Trevor's, other repo); §D `rhs` tier; §E design-case archetypes.

## Read first (ground truth, before acting)
- `CURRENT_STATE.md` (live surface + SESSION PROTOCOL) and `STATE_HISTORY.md` (top entries: the pet_safe
  rollout arc + the §B/§C offline pass). Confirm canonical is current:
  `shasum -a 256 crops_data_final.json` == `LATEST.txt` (`8e568c5b...`); `git log -1`; `git status -sb`.
- `docs/superpowers/specs/2026-07-06-degrees-url-offline-pass-design.md` -- the §B/§C design; §8 defines
  this online sweep as the follow-on and the `url_health_gate --online` mode.
- `tools/url_health_gate.py` -- the **offline** non-null-URL gate already shipped (live-layer clean). The
  `--online` mode is the new build here.

## Scope (measured on `8e568c5b`)
- **20,265 anchoring-url entries dedupe to 1,053 DISTINCT URLs** across **131 distinct hosts**.
- Of the 1,053: **131 are the `source_catalog` "spine"** (one canonical URL per catalogued source) and
  **968 are per-cell deep-links** (e.g. `plants.ces.ncsu.edu/plants/<species>/`, aspca plant pages) --
  these are where the specific claim actually lives.
- **57 null-url cells, ALL in the legacy `zones{}` layer** (the live `regions{}` layer is clean). Do NOT
  backfill them until the sources are repointed (see below).

## Known offenders (start here -- surfaced across the certify arc)
- **`uga_b577`** -> `https://secure.caes.uga.edu/.../b577plantingchart.pdf` -- the **dead B577 PDF**;
  18 of the 57 legacy nulls point at this key. Repoint to a live UGA planting-chart page or drop it.
- **`ucanr_ext`** -> bare `https://ucanr.edu` (lime's roster-wide CA/HI regional anchor). Repoint to a
  live UC ANR page that carries the claim, or accept as a regional-anchor homepage (see gotcha).
- **`sdsu_ext`** -> bare `https://extension.sdstate.edu` (tomato line). Same call.
- **Citrus TAMU** `AZ-403` / aggie-hort redirect-loops (grapefruit/mandarin/lime open_findings).
- **Generic-cucumber `B577` logo-PDF** (slicing/pickling).
- (FIXED earlier, keep as the pattern) the UNR `extension.unr.edu -> naes.unr.edu/dfi` 302 on microgreens.

## Approach (prioritized -- do NOT blindly fetch 1,053 cold)
1. **Extract + dedupe** the 1,053 distinct URLs (walk `anchoring_urls[*].url` + `source_catalog[*].url`).
   Group by host (131). Write the worklist to a scratch JSON (slug/path/url/host).
2. **Tier the sweep:**
   - (a) The **known offenders** above -- classify + fix first.
   - (b) The **131 catalog "spine" URLs** -- the canonical source homepages; quick health pass.
   - (c) The **968 deep-links**, host-grouped -- a healthy host (ncsu, aspca, most `.edu`) mostly means
     healthy deep-links; concentrate on hosts that 404/redirect.
3. **Classify** each: live / 404 / cross-host redirect / logo-or-empty PDF / bare-homepage. WebFetch
   returns cross-host redirects RATHER than following them -- re-fetch the returned URL (build that into
   the loop). Cache-friendly: WebFetch caches 15 min/URL.
4. **Fix offenders** SHA-guarded, per crop: repoint to a live page that actually carries the claim, or
   soften/drop the citation. Recompute `source_set` + re-gate (source-tier gate E) on any change.
5. **Build `url_health_gate --online`** (TDD): the offline structural half stays the pre-commit gate; the
   `--online` mode does the network liveness pass out-of-band (never in the pre-commit hook). Inject a
   known-dead URL into a scratch copy; confirm `--online` flags it.
6. **THEN backfill the 57 legacy `zones{}` nulls** -- once `uga_b577` etc. are repointed, fill from the
   corrected `source_catalog` URLs (or drop the dead ones). Not before (would spread the dead PDF).

## Companion cleanups (optional, same session -- also "finish the 114")
- **onion photoperiod latitude fan** (a §C leftover Trevor flagged): `onion.photoperiod.explainer_seasoned`
  gives long-day ">38 to 39°N", short-day "<35°N", intermediate "32 to 42°N" -- the intermediate band
  overshoots into long-day territory (42°N) and overlaps both. **Trevor to confirm the fix**; if yes,
  verify onion day-length-by-latitude against a T1 extension source and tighten (likely intermediate
  ~32-38°N), SHA-guarded onion-only. (The `°N` notation itself is correct -- only the numbers.)
- **§D `rhs` source-tier** (sage + broad-beans-fava): answered in principle by §A's ASPCA precedent (a
  non-`.edu` domain authority is admissible for the claim it is the authority on). For sage, NCSU already
  co-states the pruning caution verbatim, so `rhs` is droppable there with zero loss; re-check
  broad-beans-fava's RHS-only claims for a clean `.edu` substitute before deciding.

## Hard rules (unchanged)
- READ-ONLY on `crops_data_final.json` until an explicit promote; interim work on a scratch copy.
- Canonical stays COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline).
- Gate by EXIT CODE. Any new/`--online` gate is TDD (RED before GREEN).
- SHA-guard every promote (assert exactly the intended slugs changed); Trevor confirms every push + any
  plant-astro bump.
- Research via **WebFetch/WebSearch ONLY** -- never curl/wget/pdftotext. **NEVER** `dangerouslyDisableSandbox`.
- **Main-loop work; no subagent dispatch** (the standing unreliable-dispatch flag). If you do batch, treat
  any 0-tool-call agent output as INVALID and re-do in the main loop.

## Gotchas
- **Bare homepages are NOT all offenders.** Of 24 distinct bare-homepage URLs, most are legitimate regional
  calendar anchors (`ipm.ucanr.edu`, `hgic.clemson.edu`, `edis.ifas.ufl.edu`). The offenders are bare
  homepages on a SPECIFIC claim (lime's `ucanr.edu`), not the regional-calendar roots. Classify by role.
- WebFetch had transient network blocks earlier in the arc; if it's blocked, fall back to domain-constrained
  WebSearch and note it. Expect to pace the 1,053 across many turns.
- Don't orphan a load-bearing claim: verify the substitute URL carries the claim before removing the old one.
