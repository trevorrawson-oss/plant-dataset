# PLA-8 -- batch 13, the spring fruiting set: outcome

Written 2026-08-30. Base `ee0f54a3` (the disease_escape_sowing backfill); output `b6d36611`.
Crops: cayenne-pepper, habanero, banana-pepper, bell-pepper, eggplant. 54 problems, 264 rungs,
roster laddered 53 -> 58, catalog untouched at 60. Ordered per Trevor's ruling today: spring
fruiting next; the Companion & Pollinator override was proposed and DECLINED (the 2026-08-26
demand ruling stands).

## 1. WHAT SHIPPED

One promote (`tools/promote_pla8_batch13.py`), commit `0d45e67`, COMMIT_FOR registered `27a8c85`'s
sibling (`b6d36611` -> `0d45e67`). Five authoring agents ran in parallel (~5.5 min each); the
orchestrator merged, read all 528 register strings, and shipped the read's rulings as guards.

## 2. THE TWIN STRUCTURE, MEASURED

The batch partitions by byte-identical advice prose: **{cayenne, habanero} share 9 problems,
{banana, bell} share 8** (plus their ECB pair under two names), and **the hornworm advice text is
identical on all five crops**. Identical prose ships ONE rung text set (the batch-2 corn
precedent), with the correspondence pinned in both directions. The proof the second direction is
real: **eggplant's flea-beetle prose differs from cayenne's by one word** ("outgrow" vs "can
outgrow"), so eggplant keeps its own texts, and a driver asserts the pair differs. The five agents
independently converged on identical METHOD sequences for every identical-prose group (the allium
id story again); only their note texts differed, and the read picked one prose-faithful set per
group (habanero's weevil note had introduced facts; cayenne's hornworm Bt note had introduced
"peppers are a secondary host"; bell's hornworm set glosses frass and won).

## 3. TWO WRONG-ORGANISM TRAPS, CAUGHT BEFORE PINNING

- **`bacterial-spot`, NOT `bacterial-leaf-spot`.** All four peppers' disease is Xanthomonas,
  which jalapeno (the laddered family sibling) already carries as `bacterial-spot`. The
  name-derived id exists on the roster and names the WRONG organism: cilantro's
  `bacterial-leaf-spot` is *Pseudomonas syringae* pv. *coriandricola*. All five authoring agents
  minted the wrong string; the convention table pins the right one, and the wrong one is refused
  in both directions.
- **`southern-bacterial-wilt`, NOT `bacterial-wilt`.** Eggplant's cause prose names *Ralstonia
  solanacearum* (soilborne, water/tool-spread). The roster's `bacterial-wilt` is *Erwinia
  tracheiphila*, carried in cucumber beetles' guts. Same pea-weevil shape as batch 12, verified
  against both records' own cause prose.

Other joins verified by organism before reuse: jalapeno's eight shared ids; the corns'
`european-corn-borer` (bell's single-organism problem AND banana's combined name, the
lead-organism convention that shipped `carrot-rust-fly`); the tomatoes' `blossom-end-rot`;
strawberry's `verticillium-wilt` (its own prose names eggplant as a host); `cutworms`,
`spider-mites`. New to the roster: `colorado-potato-beetle`, `eggplant-lace-bug`,
`phomopsis-blight`, `southern-blight`, `southern-bacterial-wilt`.

## 4. THE READ'S RULINGS (all shipped as guards)

1. **Pre-plant cultivation is NOT `off_season_tillage`.** The cutworm prose cultivates BEFORE
   planting; the method means a finished bed worked after harvest. Cayenne's agent used the key
   and flagged it; habanero's refused the same advice as a gap; habanero was right. Rung dropped,
   advice recorded unplaced, key refused on cutworms. The hornworm ladders keep it: fall tillage
   of pupae is the method's own worked example.
2. **Weevil weed hosts belong to `weed_host_control`.** banana/bell used the precise key; cayenne/
   habanero had folded the nightshades into sanitation, following the pre-r7 jalapeno exemplar.
   Aligned to the catalog's own distinction on all four; the flea-beetle weeds stay IN sanitation
   deliberately (overwintering SHELTER, not host-relatives).
3. **Trap cropping is divert-only on all three carriers** (cayenne/habanero/eggplant flea
   beetles): the prose is a lure with no removal step, so the rungs route removal through the
   method's cautions and are forbidden the "this crop's guidance" attribution. banana/bell prose
   names no trap planting; their ladders are refused the key.
4. **No unnamed material becomes a rung.** Copper lands only where prose names copper:
   bacterial-spot x4, anthracnose on cayenne/habanero ONLY (banana/bell's anthracnose prose says
   "a labeled fungicide", unnamed, and their ladders end cultural). 26 ladders carry no
   soft_chemical/conventional rung at all, each on its own prose.
5. **`bt` refused on Colorado potato beetle**: the prose names the tenebrionis strain; the
   catalog's key means the kurstaki caterpillar spray with caterpillar cautions. Filed as a
   catalog gap alongside CPB's straw-mulch-as-obstacle advice.
6. **No timing or escape key earned**: the flea-beetle "delay planting until warm" advice is
   transplant vigor; `planting_time_avoidance` and `disease_escape_sowing` are refused
   batch-wide. (The mint from this morning found no pickup here; its five-crops-for-free note
   was checked and does not apply to this batch's prose.)
7. **Two shipped-rung echoes rewritten**: the aphid water_spray seasoned note was byte-identical
   to jalapeno's shipped rung (independent convergence plus one propagation), and a 17-word
   beneficial_predators sentence echoed slicing-cucumber's. Both rewritten distinctly per prose
   family; the echo guard's 10-word threshold now has its own vacuity driver.
8. Hygiene fixes at the read: "not completely safe" -> the source's own hedge "not immune";
   "never dries out badly" and "reduces rather than eliminates" reworded off the token list.

## 5. VERIFICATION

- Suite `tools/test_promote_pla8_batch13.py`: **64/64 under both runners.** Replay-pinned from
  the committed base; no RED phase claimed.
- Harness `tools/mutate_pla8_batch13_suite.py`: **37 injected, 37 caught, 0 survived (run 3).**
  Preflight 38/38; positive control GREEN (after the harness learned batch-12's staging-sandbox
  stage(), without which the staged promote reads a nonexistent path); sentinel RED. **Run 2
  returned ONE real survivor**: the applies_to-coherence branch had no driver -- the gate
  contract test checks the post DATA, which is coherent, so disabling the CHECK stayed green.
  Driver added (exclusion_fencing on a fungal problem), caught on rerun. Four driver-message
  mismatches during suite bring-up were themselves masked-branch findings: the alignment guard
  answers before validate_batch on aligned problems, and the NO_MATERIAL lookup answers before
  the taxon-shipped check, so those drivers were retargeted to reach their branches in isolation.
- Gauntlet on the applied state: gate_all **121/121**, control_ladder_gate **0**,
  register_completeness **PASS**, whole_crop_gate PASS on all five, release_verify **clean** vs
  `ee0f54a3` (only the 5 declared crops changed, methods/sources byte-identical).

## 6. FILED, NOT FIXED

- **eggplant's hornworm `anchoring_urls.ncsu_ext` points at the Clemson URL** (identical to the
  `clemson_hgic` entry) -- the mis-pointed-key defect class, found by the authoring agent.
  Source-truth pass material, not this batch's edit.
- **jalapeno's phytophthora/anthracnose ladders use `straw_mulch`** where this batch (and the
  catalog since r7) uses `splash_barrier_mulch` for the same advice -- a sibling divergence
  created by the mint postdating jalapeno's certification. Reconciliation candidate.
- **`kaolin_clay`'s best_use is tree-fruit-scoped** while five flea-beetle ladders now use it on
  prose that names kaolin -- the known "best_use narrower than shipped use" class (batch 3
  measured 11 of 49).
- **Catalog gaps re-confirmed by this batch**: no key for clean/inspected TRANSPLANTS against an
  insect that travels on them (pepper weevil; certified_clean_stock is disease/nematode-scoped);
  no generic labeled-spray key (by design); no staking/fruit-elevation key; no
  transplant-vigor key; bt covers kurstaki only (tenebrionis gap); mulch-as-walking-barrier
  (CPB) unplaceable.
- **Prose tensions**: southern blight's "bury crop debris deeply or remove it" conflicts with the
  catalog's destroy-don't-bury caution (rungs assert only removal); eggplant vs jalapeno hornworm
  sizes disagree (4 in. vs 3.5 in.); banana/bell phytophthora prose omits resistant varieties
  while jalapeno's names them.

## 7. NEXT

Remaining after batch 13: 63 crops / 447 problems, ~13 batches. The spring-fruiting arc
continues: okra + tomatillo + the melons (cantaloupe, honeydew, watermelon) are the natural batch
14, and **the melons mint `mancozeb`** (uaiKey=30, already read: water H, bees low, acute L,
Prop 65 + EPA) -- growth, not audit debt. Microgreens and Companion & Pollinator stay LAST.
