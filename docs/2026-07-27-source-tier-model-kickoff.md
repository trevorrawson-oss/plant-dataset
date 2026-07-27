# Source-tier model — kickoff

**Date:** 2026-07-27
**Origin:** the artichoke GS arc (#121) hit the tier bar three times in one session and got it wrong
twice. This documents what the model actually is, what broke, and what to change.
**Read with:** `docs/2026-07-26-artichoke-gs-arc-kickoff.md` §R3/R4,
`docs/2026-07-26-post-asparagus-hardening-kickoff.md`.

---

## 0. Why this exists

Three separate tier judgments were made during the artichoke arc. Two were wrong, and **both errors
ran in the same direction: rejecting sources the dataset already trusts.** That direction matters —
an over-strict bar does not produce silence, it produces *unsourced derivation*, which is less
honest than the citation it replaced.

The corrections came from Trevor supplying URLs, not from the process catching itself.

---

## 1. What the model actually is (measured, not assumed)

Canonical `34025ee3`, 174 catalog entries.

| field | values | who reads it |
|---|---|---|
| `tier` | `T1` × 165, `T2` × 9 | **gate E — the only gate-enforced axis** |
| `trust_tier` | `high` × 166, `standard` × 8 | nothing |
| `source_class` | **17 distinct values** | nothing |

Gate E's rule is one line, and it is the whole enforcement surface:

```python
not_t1 = sorted(s for s in cited if s in cat and cat[s].get("tier") != "T1")
for s in not_t1: fail(f"source-tier: {s} tier={cat[s].get('tier')}")
```

### 1a. `T2` does not mean what its name suggests

All nine T2 entries, in full: `almanac`, `johnny_seeds`, `harvest_to_table`, `seed_savers`,
`hudson_valley`, `tomato_growers`, `australian_seed`, `kitchen_garden_seeds`, `hoss_tools`.

Six are `commercial_seed_company`. **T2 is the seed-trade and folklore band** — Old Farmer's
Almanac, Johnny's, a gardening blog. None is cited by any crop; they are catalogued but unusable.

**Consequence, and this is the trap:** "loosen gate E to allow T2" — which this arc proposed and
nearly built — would not admit extension outreach. It would admit **Johnny's Selected Seeds**. That
is concretely harmful here: Johnny's is the documented origin of the widely-copied "10 days at
45-50°F" artichoke vernalization figure that the peer-reviewed UMaine trial contradicts (303 hours
→ 3-33% flowering; 550 hours → 68-100%). The change would have licensed citing the number the
research disproves.

### 1b. The "missing middle band" is not missing

The band this arc claimed did not exist — extension-published but not peer-reviewed — **is already
admitted at T1**, carried by `source_class` rather than by tier:

| source_class | count | example |
|---|---|---|
| `extension_master_gardener_program` | 6 | `ucanr_marin_mg`, `nmsu_donaana_mg`, **`unlv_mg_svn`** |
| `extension_master_gardener` | 1 | `ucanr_mg_monterey_santacruz` |
| `cooperative_extension_community` | 1 | `ext_org_apples` |
| `horticultural_authority` | 5 | `rhs` (T1), `piedmont_mg` (T1), `almanac` (**T2**) |

Note the last row: `horticultural_authority` spans **both** tiers. Same class, different tier, no
recorded rule for which is which. That is the actual inconsistency in the model.

---

## 2. The three tier judgments this arc made, and how they went

| # | source | this arc's call | correct call | how it was caught |
|---|---|---|---|---|
| 1 | `uaex_cardoon` (AR ornamentals column, "does not promote, support or recommend" disclaimer) | admitted at T2 → gate E bounced it → dropped | **probably right** to drop; the disclaimer is disqualifying regardless of tier | gate E |
| 2 | LSU AgCenter artichoke page | dropped — URL 404'd | **wrong**; the address was self-constructed, the document exists | Trevor supplied the URL |
| 3 | `unlv_mg_svn` (Southern Nevada MG planting guide) | rejected as "volunteer-authored, fails the tier rule" | **wrong** — it is `tier: T1`, cited by **67 crops**, admitted 2026-07-21 explicitly to "back the nevada per-crop annual windows" | Trevor supplied a UNR URL that led back to it |

### The process defect, stated plainly

**Research agents make tier judgments without consulting the catalog, and the orchestrator relays
them without verifying.** In case 3 a subagent applied a stricter bar than the dataset's own
recorded admission decision, and I acted on it — removing a source that 67 other crops cite, then
authoring a *derived* window in its place and, worse, publishing the false claim that "University of
Nevada Extension does not recommend artichoke."

That is the asparagus failure mode inverted. Asparagus cited a document that did not support its
claim; this arc refused a document that did.

**The cheap fix is procedural, not architectural:** before any agent reports a source as
tier-rejected, check whether it is already in `source_catalog`. The catalog is the authority on
admission; it had already ruled.

---

## 3. What to change

### 3.1 Renumber the bands (Trevor's call, 2026-07-27)

Current `T2` is folklore and seed trade. Move it to **`T3`** and free `T2` for the band that
actually needs a name:

| tier | means | examples | gate E |
|---|---|---|---|
| **T1** | peer-reviewed or numbered extension publication, USDA, peer-reviewed literature | UC ANR 7221, USU fact sheets, UNR FS-13-05, VCE 438-108 | allow |
| **T2** | extension-**published**, not peer-reviewed: county MG charts, extension news, outreach columns | `unlv_mg_svn`, `ucanr_marin_mg`, the Marin grow sheet | allow, with §3.2 |
| **T3** | common practice, folklore, seed trade, almanacs | `johnny_seeds`, `almanac`, `harvest_to_table` | **deny** |

This is a **migration**, not a flag flip: the 9 current T2 entries move to T3, and the ~8 outreach
entries currently sitting at T1 move down to T2. Both moves must be paired with gate work or the
roster breaks — several of those T1 outreach entries are cited by dozens of crops.

⚠️ **Sequencing hazard:** demoting `unlv_mg_svn` from T1 to T2 while gate E still denies non-T1
would instantly fail 67 crops. Gate E must accept T2 **before** the migration runs, in that order,
with `gate_all` green between each step.

### 3.2 Guardrails so T2 does not become the default path

Both carried from the asparagus session's review, and both are right:

1. **Tier stays OFF `resolution_method`.** They are orthogonal axes — *how* a value was reached
   (direct / derived / adjacent-zone) versus *what backs it* (T1 / T2). You can have T1-derived and
   T2-direct. Collapsing them into one string destroys the cross-product. The gate joins
   `cell.sources` against `catalog[id].tier` instead.
2. **A T2 citation requires a recorded, failed T1 search.** "I could not find T1" becomes checkable
   rather than assertable. Otherwise T2 is the path of least resistance the moment it is legal.

### 3.3 What would actually have caught asparagus — the higher-value half

**Correction to this arc's own diagnosis, verified against the catalog:** the asparagus failure was
*not* a T2 laundered as T1. All four bad sources are `tier: T1`, `source_class: university_extension`,
genuine land-grant documents, correctly tiered. PlantVillage was **never a catalog entry** — it
appears three times in canonical, all inside the open finding that documents its retirement. It
bypassed the citation system rather than passing through it.

**Tier discipline would have caught none of the four.** The failure was a correctly-tiered document
cited for a claim it does not contain — `unr_fs0261` is a real UNR fact sheet whose only mention of
the crop is `"Stems - asparagus"` in a list.

So the complementary arc, and the more valuable one:

**Claim-support verification across all ~1,153 cited URLs.** Two tiers of it are automatable:
does the URL resolve, and does the fetched document mention the crop at all. Neither proves the
claim, but both are cheap and both would have flagged `unr_fs0261` on asparagus immediately. This
arc's own URL check already earned its keep twice in one session (one self-constructed 404, one
dead archive link).

---

## 4. Acceptance bar

1. `T3` band exists; the 9 seed-trade/folklore entries migrated to it; gate E denies T3.
2. Gate E accepts T2 **before** any T1→T2 demotion runs; `gate_all` green between every step.
3. Outreach entries reclassified T1→T2, with `citable_for` naming the document class.
4. Tier is **not** written into `resolution_method`.
5. A T2 citation carries a recorded failed-T1 search on the cell.
6. TDD RED before GREEN on every gate change; prove a T3 source still bounces.
7. A written rule for which `horticultural_authority` entries sit at which tier — the class
   currently spans two tiers with no recorded basis.
8. Agent research briefs updated: **check `source_catalog` before reporting a source as
   tier-rejected.**
9. `docs/methodology-and-sourcing.md` updated with the three-band definition.

## 5. Explicitly out of scope

- The claim-support verification sweep (§3.3) — related, larger, deserves its own arc.
- Roster-wide `suitability` rollout — see the post-asparagus hardening kickoff, Item 4.
