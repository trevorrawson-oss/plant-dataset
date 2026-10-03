# 60 - Housekeeping session: after PLA-10, before the citrus pass

**Kickoff from claude.ai, 2026-10-03.** Saved verbatim below by the housekeeping session (Claude Code).

---

HOUSEKEEPING SESSION — plant-dataset, after PLA-10, before the citrus pass
Kickoff from claude.ai, 2026-10-03. Save as docs/kickoffs/<next free number>-housekeeping-kickoff.md; ask before committing it.

START STATE (stop on any mismatch)
- plant-dataset main == origin/main == e15bce3
- crops_data_final.json sha256 prefix b331e5f2, matching LATEST.txt
- git status in full, pasted. Expected untracked, not ours: .codex/, AGENTS.md, two root files, old staging dirs. Leave them alone and out of every commit. Anything else unexpected: stop.
- Read first: PLA-10's closing comment (2026-10-03) and PLA-544's 2026-09-30 close-out.

THE BAR (unchanged)
Tools: TDD, RED before GREEN, mutation harness with 0 survivors, CLAUDE.md's affected-set rule, ask before every commit. Data: every figure quoted from hashed page bytes (raw bytes, two user agents, PDFs via pinned pypdf), one EVIDENCE row per (field, source), a decision row for every judgment, an independent source-truth review before landing, canonical written only with --expect-sha. Stage by explicit path. Push only on Trevor's go.

SHAPE: three phases, a stop after each. Phase A is read-only. If a phase outgrows the session, stop at a clean commit boundary and carry the rest by name.

PHASE A — MEASURE (no deletions, edits or commits)

A1. Stale staging and the 07-29 doc. For tools/staging/shards (07-22), pla140_umn_ext_prep (08-20), pla6_year_trio (08-22), pla8_batch18_citrus (08-31) and docs/2026-07-29-establishment-path-encoding-question.md:
- Tracked or untracked. An untracked dir has no git copy; deleting it is unrecoverable.
- File inventory: what each is, size, sha256.
- For every hunt record, evidence manifest, hashed page, EVIDENCE or decision TSV: name the other copy by path and SHA (committed elsewhere, git history, a record doc, Linear), or say "only copy". Byte-compare; do not infer from names.
- Any test, tool or doc that references the path (grep). A reference makes deletion a tools change.
- The 07-29 doc: is its question answered (which ruling, where) or still open?
- Proposed disposition per item (delete / commit to a records location / keep), one line of reason each.

A2. PLA-544 pin inventory, measured. PLA-544's close-out NAMED the canonical-SHA pins at 00dda31c (groups A to D) without re-measuring them, and the canonical has since moved to c5fc3d13, cf1d480d, 31b766e8 and b331e5f2.
- Every group A, group B and borderline entry: the SHA it names today, pass/fail on b331e5f2, and if it moved during PLA-10, which promote moved it and whether that data commit records the re-measure (D8 task 8).
- run_test_tree.WAIVERS: per entry, the population it is red at (the PLA-544 convention).
- The vacuity side finding: confirm test_build_rgv_promote.py and test_build_corn_family_patch.py still return early and pass having inspected nothing; scan for any other early-return-pass suites; propose a fix (report SKIP, or assert against the replay).
One table. No re-pins in Phase A.

A3. Helper consolidation, measure first. Locate the three byte-identical copies of the promote evidence/diff helpers (promotes 1, 2, 3) and their identity-pin tests: each function, its callers, sha256 per copy. Report what tools/pla10_promote_common.py already holds (T4 lives there) and where the restatement scanners live (height_strings in promote 3, spacing_strings in promotes 1 and 2). Propose:
- An arc-neutral module name (the citrus pass and PLA-534 will import it).
- Whether pla10_promote_common moves into it or re-exports from it.
- The replay proof: each promote's suite and replay must reproduce its post-state canonical (cf1d480d, 31b766e8, b331e5f2) byte for byte after the move.

A4. From the PLA-10 D2 ruling (2026-09-29): find where PLA-7's D3 note lives (Linear description, repo doc, or both) and whether the correction (artichoke and asparagus are `row`, not `block`) is appended. Same check for the stale planting_layout_gate docstring. Report done or not done, with location.

A5. Four prose-vs-figure items. For each: leaf path(s) and current text, the authored figure beside it, the pages cited on the crop, and the bearing page sentence quoted from hashed bytes.
- chives: the "8 to 14 inches" variety note, below the 1 ft floor. Support it (hashed quote on a T1 page cited on the crop, the edamame rule) or edit it.
- sweet corn: the thinning text (TAMU "1 foot") vs ISU/UMN in-row 8-12.
- fava: "rows 18 to 30", uncited.
- watermelon: the 24 sq ft rule beside Clemson's 5-6 ft in-row.
Disposition per item: support / edit (proposed text, one claim per sentence, each mapped to a page sentence) / route to PLA-625 by name. Do not author. If no T1 page carries a figure, say so; do not fill the gap.

STOP. Phase A goes back as one report with the rulings needed, numbered.

PHASE B — TOOLS (after rulings; one commit per step, ask before each)
B1. Consolidation as ruled. RED first: a test that fails until every promote imports the shared module and the identity pins are gone. Retire the pins in the same change. Harness over the shared module; 0 survivors. An unreachable guard is reported and ruled on, never silently removed (PLA-10 promote 1 precedent). Replay proof as ruled.
B2. PLA-653 as the ticket asks. Report STALE only for a waived test collected this run; otherwise print "waived test not in population (not run)". Add the dropped-population-check mutation to mutate_run_test_tree.py and verify it RED. Do not touch the cache-coverage waiver.
B3. PLA-655, on the shared module. Measure the widened scanner's population over promote 3's fixed list before arming it. Positive control: the ticket's misses, including the word-number and "12+ ft" leaves. Check spacing_strings for the same blind spot. Add a mechanical guard on EVIDENCE_RESTATEMENT_SUPPORT.tsv (bytes present at the hashed sha, MANIFEST url == row url, url cited on the crop, leaf marked `agrees`); meaning stays with review.
B4. PLA-659, on the shared module. Fixtures from the two hashed pages; split "3 1⁄2" from glued "31⁄2"; positive control on a plain decimal.
B5. The vacuity fix, if ruled in.
B6. Re-pins from A2, if any, each with its rows read, never a bare literal edit.

PHASE C — DATA (only for A5 items ruled support or edit)
One small promote from b331e5f2 with the full ceremony above: --expect-sha b331e5f2, release checks, gate_all, and the canonical-SHA pin re-measure in the data commit. Run B3's widened scanner over the edited crops, then hand-sweep them anyway. Then LATEST.txt and the state files per their protocol. Consumer bumps are not this session; record what app and site will need.

OUT OF SCOPE
- PLA-630: its own session. It changes the runner that certifies this work.
- PLA-651, 652, 654: consumer sessions.
- The six uada_ext leads: PLA-625.
- The plant-app art-brief reconcile: Trevor's.

CLOSE-OUT
A dated comment on PLA-10 that answers its carried-forward list item by item. Also comment on PLA-544 (the measured inventory) and on each ticket landed (653, 655, 659). List every commit SHA. Push on Trevor's go.

---

ADDENDUM to the housekeeping kickoff (claude.ai, 2026-10-03)
Add PLA-652 to the session.
A6 (Phase A, read-only): run the prose-identity crosstab of det_indet across the 6 crops that carry it (detail_beginner and detail_seasoned), per the ticket. Report every byte-identical or near-identical pair, not just tomatillo/cherry-tomato. For tomatillo, list its cited pages (USU, NCSU, UMN, UCANR Alameda, SDSU) and quote from hashed bytes the sentences that bear on growth habit. Do not author.
Phase C: if ruled, tomatillo's two registers are re-authored in the same small promote as the A5 items, under the same ceremony, dual-register, no em dashes, independent source-truth review.

---

HOUSEKEEPING — PHASE A RULINGS (Trevor via claude.ai, 2026-10-03)

Phase A accepted. A3's correction to the kickoff premise is taken: promote 1 holds the originals, pla10_promote_common holds a byte-identical second copy, and promotes 2 and 3 already import it.

1. A1.
- shards/: commit the 19 subagent reports to records, then delete the rest. Reports are cheap to keep and deletion is unrecoverable.
- pla6_year_trio/ and pla8_batch18_citrus/: delete.
- pla140_umn_ext_prep/: commit the README and round2_claim_sites.md to records. Don't commit the 3 JSONs; add the rebuild command from 8118eaa to the README instead. Confirm PLA-140's status, and if it's open, comment there with the records path and the 58-place count.
- Records location: use the repo's existing records convention if one exists, otherwise docs/records/<YYYY-MM-DD>-<name>/.
- The 07-29 doc: commit it at its current path, since 8 tracked kickoffs reference that path.
- One docs commit for all of this, staged by explicit path. Ask before committing.

2. 07-29: yes. File it in Linear (Backlog) as an open decision, with the measurement (artichoke tokens in 38 of 39 cells, asparagus 0 of 39), the doc path, and the note that avocado and olive need the answer. Don't rule the question.

3. A2 labels.
- A pin's SHA label means "last moved at" and is never edited on a re-verify. Editing tests on every promote churns tools/ for no information.
- Each promote's data commit message records "re-verified at <sha>" for every live pin.
- Yes, the five never-named suites and the A44 pin ("121 crops, 135 entries") join the re-measure list.
- The list becomes a committed registry rather than a doc. Add a completeness test: any test in tools/ containing a canonical-SHA literal or live population literal must appear in the registry. That is the instrument that would have caught the A44 miss. TDD + harness, with the A44 pin's omission as the positive control.

4. B5 vacuity, all in:
- source_catalog (both tests): replay from 060b91b8.
- rgv_harness: injection on a copy of broccoli.
- corn_family: pytest.skip.
- rgv_build: replay, with a COMMIT_FOR pin to the commit where its real inputs exist in git. If they aren't recoverable from git, pytest.skip instead. Never fabricate inputs.
- bare_host_scan: pin SOLE by identity.
- Fix 0 is in: a skip that never reaches the VERDICT is the same vacuity class.
- Fix 0 and PLA-653 both edit run_test_tree. Land them in one runner commit, each change with its own RED and mutation driver, and run the full tree once for that commit.

5. B1.
- Taken as proposed: cited_promote_common.py, the re-export shim with underscore names and the identity test, and the order (promotes 2 and 3 first, promote 1 last in its own commit).
- Replace the getsource pins with the three real-stage replay tests asserting cf1d480d, 31b766e8 and b331e5f2 (RED first).
- No source-hash pins. They freeze code without testing behavior and would churn on B3 and B4 immediately. The replays are the guard.
- In scope: extract the 16-line evidence block, and unify spacing_strings and height_strings into one generic scanner, both behavior-preserving. Prove it: both old scanners' outputs on promote 1's and promote 3's fixed lists equal the generic scanner's, byte for byte. B3 (PLA-655) then widens the generic scanner once, for both.
- Time the affected set before starting, as you proposed.

6. A4: yes. Append to PLA-7's and PLA-581's descriptions, at the sentences you found: "[CORRECTION 2026-10-03, per the PLA-10 D2 ruling of 2026-09-29: artichoke and asparagus are `row`, not `block`; see docs/superpowers/specs/2026-09-21-pla581-critical-warnings-field-shape.md §13 item 1.]" Leave the original text byte for byte. Use insert_after, and verify each write from the returned payload.

7-11. PHASE C PROCESS: prose is authored in claude.ai, not in this session. After Phase B, send one quote packet per item: leaf path, current text, and every relevant sentence from hashed bytes (source id, url, sha256). I write the strings and you apply them. Then the ceremony as written: EVIDENCE and decision rows, an independent source-truth review, --expect-sha b331e5f2.
Rule for every leaf we edit: every claim in the leaf is either mapped to a hashed page cited on the crop, or cut. No partial verification of a touched leaf.

7. chives: if recommended[0] describes the common or species type, the note follows NCSU (1 to 1.5 feet) and matches the crop figure, so no support row is needed. If it names a cultivar, quote whichever hashed page states that cultivar's height; if none does, cut the height clause. The "late spring" bloom claim is in scope under the touched-leaf rule.

8. sweet corn:
- Hash TAMU EHT-044 in Phase C under the full ceremony and keep it. It is the only page that speaks to thinning.
- thin_to_inches must be a figure a cited page states for thinning: TAMU's 1 foot, as [12,12], with a decision row noting it sits at the top of the ISU/UMN in-row 8 to 12.
- ISU and UMN stay cited for the in-row figure, not for thinning.
- Cut "3 to 4 inches tall" and the snip sentences unless a hashed page cited on the crop states them.

9. fava: cut the "rows 18 to 30" clause. Route both of these to PLA-625: the UMass hash and the commercial-guide question, and the "4 to 6" vs "3 to 5" question. Prose and the authored spacing field move together or not at all, so no prose change to a figure the field doesn't carry.

10. watermelon:
- Drop the 24 sq ft clause. It is supported, but per PLA-10 D4, area per plant is calculated from spacing, never written as a second figure, and Clemson's 24 sq ft belongs to its 6x4 / 8x3 scheme, not the authored spacing. Record a decision row quoting Clemson.
- "Vine runs 8 to 12 feet": support it from a hashed page already cited on the crop, or cut it. No new hunt.

11. tomatillo (PLA-652): yes.
- Re-author both registers in Phase C. Re-anchor det_indet to the hashed USU, NCSU, UMN, UCANR and SDSU pages.
- Use only pages cited on the crop. If OSU isn't cited, it doesn't enter the text; quote it in the packet only as context for the sprawling/bushy split.
- In this promote:
  - days_to_maturity: re-anchor if a hashed tomatillo page states the authored figure. If the figure differs, stop and report.
  - failure_diagnostics[5]: verify "cherry tomatillo" or cut it.
  - Append a [CORRECTION] line to the cert log, original untouched.
- File, not in this promote: cherry-tomato's unsourced Tumbling Tom and Patio Choice claims, as a ticket with your measurement.

12. Kickoff 60: commit now, docs only, including the PLA-652 addendum, staged by explicit path.

Order: the docs commits (12, then 1), the Linear writes (2, 6), Phase B as ruled, then the quote packets. Ask before each commit. Push on Trevor's go.
