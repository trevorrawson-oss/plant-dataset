# 61 - Phase C quote packets (housekeeping kickoff 60)

**Written 2026-10-04 by the housekeeping session (Claude Code), read-only.** Canonical `b331e5f2` (== LATEST.txt),
main at `6e444f3` (Phase B landed: 84b7efe, 4df569b, 7a115f0, ff62491, 671e169, 1250f3a, b1e1f1a, 0687c56, 6e444f3).
Nothing here is authored: Trevor (claude.ai) writes every replacement string; Claude Code applies them under the
full ceremony (EVIDENCE + decision rows, independent source-truth review, `--expect-sha b331e5f2`).

**How to read a packet.** Per touched leaf: the path, its CURRENT text verbatim, every claim split out, and per claim
MAPPED (a verbatim sentence, in `norm_text` form, from the HASHED bytes of a page CITED ON THE CROP, with source id,
url and sha256) or **NO HASHED CITED PAGE STATES IT**. Every sha256 was recomputed over the bytes; every quote was
machine-checked as a substring of its page's hashed text. Pages cited but not hashed are listed per crop: they cannot
support a claim this session.

**THE RULE for every leaf we edit (ruled 2026-10-03):** every claim in the leaf is either mapped to a hashed page
cited on the crop, or cut. No partial verification of a touched leaf.

| # | packet | item (ruling) | what the packet found |
| -- | -- | -- | -- |
| 1 | chives.md | A5 / ruling 7 | recommended[0] is "Common Chives", the species type -> the note follows NCSU 1 to 1.5 ft (no support row). "8 to 14 inches", "tidy", "pom-pom", "extremely", "workhorse" are on no hashed page. Bloom: UMN late May/June and Wisc mid spring to early summer support "late spring"; Illinois says mid-summer (both quoted). |
| 2 | sweet-corn.md | A5 / ruling 8 | TAMU EHT-044 ("after the plants are up, thin them to 1 foot apart") is to be HASHED in Phase C; thin_to_inches [12,12]. "3 to 4 inches tall", "a few inches tall" and every snip / soil-line / spare-the-roots claim are on no page. **WSU (cited) advises against thinning corn at all** ("plant large seeds such as beans, corn, and squash at the recommended row spacing to avoid having to thin the stand later"): authoring input, per ruling. |
| 3 | broad-beans-fava.md | A5 / ruling 9 | "rows 18 to 30" is in this one leaf only; no hashed page gives any fava row figure (cut, ruled). Most other claims in the leaf are on no hashed page (listed). "4 to 6" vs "3 to 5" is routed to PLA-625, not resolved. |
| 4 | watermelon.md | A5 / ruling 10 + scope ruling | Clemson's "a rule of thumb is to allow 24 square feet per plant." for the decision row (the clause is dropped). "8 to 12 feet" vine run: on no hashed cited page; it sits in 6 leaves (the named 3 + first_year_note_seasoned, growth_stages[2].user_action_seasoned, tips_by_stage.vining[0].text_seasoned, soil_prep_beginner), all in scope. |
| 5 | tomatillo.md | PLA-652 / ruling 11 | det_indet: every growth-habit sentence from hashed USU, NCSU, UMN, UCANR Alameda, SDSU; OSU EC1333 is NOT cited on tomatillo (context only). days_to_maturity [65,100] is SDSU's (re-anchor). **days_to_maturity_mid 80: no hashed page states it; the field has no schema definition and behaves as an authored typical figure on 33 of 91 crops, with no midpoint rounding rule; recommendation: null with reason** (B2). "cherry tomatillo" (failure_diagnostics[5], both registers): unsupported. The log_ref sentence for the [CORRECTION] is quoted exactly. |
| 6 | lavender.md | live conflict (B3 classification) | Finding (a): USU supports the FIELD [18,24] ("space lavender plants 18-24 inches apart"); "2 to 3 feet" is on no hashed page (NC State / OSU pages the prose credits are cited, NOT hashed). 6 leaves. |
| 7 | basil.md | live conflict | (a): UMN supports [6,12]; "12-18 inches" on no hashed page. 2 leaves. |
| 8 | jalapeno.md | live conflict | (a) for the prose ("24 to 36" on no page); the FIELD [24,24] itself is narrower than five hashed cited pages -> **PLA-625** (ruled). |
| 9 | brussels-sprouts.md | live conflict | (c): ISU supports the field rows 24-30, hashed WSU's table the prose 24-36 -> **PLA-625** (ruled). |
| 10 | oregano.md | live conflict + ruling (rgv) | (a): UF supports [10,12]; "up to 18 inches" on no page. **regions.rgv: 5 leaves credit TAMU with 10-12 in, which is TAMU's THYME row; its oregano row reads "space 8-10 in."** (rows quoted side by side). |

**Routed elsewhere (ruled; written to Linear at close-out):** jalapeno and brussels-sprouts fields -> PLA-625 with
the quotes; the 14 scope-dependent spacing conflicts (radish daikon x10, raspberry black/purple x2, spring-onion clumps,
swiss-chard UMN transplants) -> PLA-625 (daikon and black/purple raspberry also PLA-12); the 39 real heights on
crops with no authored figure (mostly vine runs) -> PLA-625; variety figures with no hashed support -> PLA-12.
