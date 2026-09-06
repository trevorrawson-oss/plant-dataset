# PLA-457 -- the sulfur/oil interval: PREPARED AND HELD

**Date:** 2026-09-06. **Lane:** Claude Code. **Canonical:** `72371c02`, **UNCHANGED**. The promote
is written, mutation-tested and gauntleted against a scratch post-state (`e4e55a14`); it has not
been applied. Ruling: Trevor, 2026-09-06, on the ticket.

## 1. The ruling

**30 days, scoped, deferring to the product label.** Copy does not state a bare interval; it names
what the interval applies to (growing-season use, green tissue present, elemental or wettable
sulfur) and points at the oil product's label as the controlling document. Methodology entry:
`~/Documents/plant-project/05-methodology/current/conditional_claims_scope_v1_0.md` (where a T1
claim is conditional, the condition is part of the claim).

## 2. The T1 reads, all by direct extraction, none from a search summary

| source | read | says |
|---|---|---|
| UC IPM PN 7405, Spider Mites | page fetched | "Don't apply sulfur within 30 days of an oil spray." |
| Purdue BP-69-W, Using Organic Fungicides (Beckerman) | PDF extracted, 4 pages | "Do not use sulfur if you have applied an oil spray within the last month -- the combination is phytotoxic (plant-killing)." Also "Always check product labels", and the summer-oil versus dormant-oil distinction. |
| EPA label 61842-30, Lime-Sulfur Solution Agricultural Fungicide (2023-02-27) | PDF extracted, 17 pages | "DO NOT use this product within 30 days of an oil spray at any stage other than dormant (deciduous only) unless prior experience in your immediate area has shown that shorter intervals will not result in phytotoxic injury." and "Allow 30 days between oil and Lime-Sulfur Solution Agricultural Fungicide sprays in the growing season, as injury may occur." The same label PRESCRIBES lime sulfur plus oil in dormant and delayed-dormant programs, which is what reconciles WSU's combined spray with everyone else's prohibition. |
| UC IPM, Lime Sulfur (home and landscape) | page fetched | "Lime sulfur is a product no longer available to home and garden users." No date on the page; the "~2017-18" in the ruling is NOT confirmed by direct read and nothing authored depends on it. |
| UC IPM PN 7406, Powdery Mildew on Vegetables | page fetched | "do not apply it within 2 weeks of an oil spray". The `sulfur` entry's anchor was faithful; the ruling moves to the conservative scoped figure. |

Every read confirmed. The `horticultural_oil` misquote is real: it said 2 weeks citing a page that
says 30 days.

## 3. The reach is 20 notes on 10 crops, not 15

The ticket's 15 came from a strict scan: sulfur AND oil AND a duration in one sentence. Five more
sentences state the interval with a pronoun for the rung's own material ("keep it two weeks from any
oil spray" on a sulfur rung): apple/apple-scab, oregano/powdery-mildew, sage/powdery-mildew,
strawberry/two-spotted-spider-mite, cherry-sweet/black-cherry-aphid. The widened net is a guard in
the promote, pinned at 22 statements (20 notes + 2 cautions) before and 22 after, none under 30
days, every one scoped and deferring to the label. mint's "30 days of harvest" is a pre-harvest
interval and is excluded by its harvest clause, not by its words.

| crop | notes | crop | notes |
|---|---|---|---|
| apple | 3 | oregano | 2 (the two-interval inconsistency; both now 30 days) |
| apricot | 3 | plum | 4 |
| cherry-sour | 1 | sage | 2 |
| cherry-sweet | 1 | strawberry | 2 |
| grape-tomato | 1 | lemongrass | 1 |

Three of the 20 already said 30 days (oregano oil, sage oil, lemongrass); they are rewritten for
the scope and the label deferral, which the ruling requires of every statement.

## 4. What the promote changes

| target | change |
|---|---|
| `source_catalog` | +1: `purdue_ext_bp69w`, T1, pathed, titled (A54 run on the probe) |
| `control_methods.horticultural_oil` | cautions[1] rewritten to the scoped 30-day claim; `purdue_ext_bp69w` added to sources and anchors; PN 7405 (already cited) is now quoted correctly |
| `control_methods.sulfur` | cautions[1] rewritten likewise; `purdue_ext_bp69w` and `ucanr_ext_spider_mites` (PN 7405) added; PN 7406 stays for its other claims |
| 20 rung notes | exactly one sentence replaced in each, found by exact match; registers stay distinct; no other rung, entry, crop, method or catalog entry moves |

No other `control_methods` entry states a sulfur/oil interval (`biofungicide` mentions both
materials with no interval). Confirmed by the same net.

## 5. Guards, and what the harness proved

`tools/promote_pla457_sulfur_oil_interval.py`, suite `tools/test_promote_pla457_sulfur_oil_interval.py`,
harness `tools/mutate_pla457_sulfur_oil_interval_suite.py`, spec `tools/staging/pla457_sulfur_oil_interval/spec.json`.

| guard | what it refuses |
|---|---|
| the widened net, pre | a statement count other than 22, or one the spec does not rewrite |
| the widened net, post | any surviving sub-30-day statement, any statement without 30 days + label + a growth-stage scope, a count other than 22 |
| scoped claim | a bare interval, a missing scope, a sub-30 figure alongside, a claim without the figure (four regexes, four drivers) |
| hygiene, lift | em/en dash, absolutes, ladder vocabulary; a six-word PROSE run shared with an anchor sentence (digit-bearing runs exempt, the batch-27 precedent) |
| pre-state | an old sentence not found exactly once, a caution not found, a catalog id that exists, a non-T1 or bare-host or untitled source, an anchor url that differs from the catalog |
| oregano | the two rungs disagreeing afterwards |
| registers | identical or reworded pairs on touched rungs |
| catalog gates | A54 and `control_ladder_gate.all_violations`, IMPORTED and run on the post-state (the catalog-round-10 lesson) |
| blast radius | sets before values; exactly 20 note leaves, 2 cautions, sources/anchors on 2 methods, 1 catalog id; roster, untouched crops, other methods, existing catalog entries byte-identical |

Suite **69/69**. Harness **53 injected / 53 caught / 0 survived / 0 broken**, anchors 53/53,
positive control green, sentinel reddened. One driver was repaired on the way: it named a rung the
ladder did not have, errored before the guard ran, and the harness counted its mutation as caught
for the wrong reason; it now picks the rung by the property under test. Two guards were refined by
their own first refusals: the lift guard refused "30 days of an oil spray" (the figure; digit runs
are now exempt), and the scope guard refused a lemongrass sentence that lacked the growth-stage
clause (the sentence was fixed, not the guard).

## 6. The gauntlet, on the scratch post-state `e4e55a14`

| check | result |
|---|---|
| `whole_crop_gate` on the 10 crops | PASS x10 |
| `gate_all` | PASS, 121/121, run on the scratch post-state |
| `control_ladder_gate` | 0 / 0 |
| `source_catalog_title_gate` (A54) | exit 0 |
| `register_completeness_gate` | PASS |
| `variety_resistance_gate` | 0 |
| `release_verify --base <72371c02> --slug oregano --expect-changed <9> --ref lettuce-leaf` | section A clean: exactly the 10 declared crops, `source_catalog` +1 and `control_methods` as declared, lettuce-leaf byte-identical. One section-E concern (`rgv: novel region keys vs lettuce-leaf: ['plantings_provenance']`) is PRE-EXISTING: the same command on the live canonical with no base reports it, and oregano's region cells are byte-identical across the two states. With `--slug apple` the only concerns are the known false novel-key report from comparing a tree's `chill_basis_*` against an annual reference. |
| full `tools/` tree | run on the CURRENT canonical with the new suite present; see the Linear close-out |

## 7. What is held

The write to `crops_data_final.json`. To apply after approval:

```
python3 tools/promote_pla457_sulfur_oil_interval.py --expect-sha e4e55a14be8c4f32dca69e6ab23b742c31d2236dd742f5230ae425835ff260aa
```

then the state trio, the collision-suite re-measure (no id moves, so the figures should hold at
36 / 24 / 12; re-measure anyway per playbook 5a), `COMMIT_FOR` registration of `e4e55a14`, and the
plant-app export rebuild.
