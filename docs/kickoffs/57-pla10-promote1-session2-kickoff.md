# 57 - PLA-10 promote 1, SESSION 2 of 3: stage the 93 row crops (kickoff prompt)

Paste the block below into a fresh Claude Code session in `~/plant-dataset`. It assumes no memory of session 1.

---

```
plant-dataset: PLA-10 promote 1, SESSION 2 of 3. This session STAGES crop
data for the promote; it does NOT run the promote and does NOT write
crops_data_final.json. Canonical stays READ-ONLY throughout.

PREFLIGHT (CLAUDE.md, CURRENT_STATE.md SESSION PROTOCOL): git fetch origin;
branch must be main; git rev-parse HEAD origin/main identical; report the
branch. Expected base: canonical c5fc3d13 (== LATEST.txt), and main carrying
4275113 plus the five session-1 commits:
  f9fca38 docs(pla10): §11 rows folded into the spec
  4a6ab59 docs(claude-md): a tools/ logic change runs the AFFECTED SET
          (supersedes 4275113's full-tree rule)
  f6de39a tooling(pla10): promote 1 tools (A44 list rewrite, unarmed; A62
          planting_layout family; R5/W5 migration waivers; is_microgreen on
          zone_independent; promote_pla10_planting_layout.py + suite + harness)
  a0ff6a4 docs(pla10): worklist 56 (+ .tsv)
  642f772 docs(pla10): spec corrections + W5's R5 widening
(and the session-1 kickoff commit that adds this file). If any is absent,
STOP. Check Linear STATUS fields before trusting issue bodies (PLA-10).

READ FIRST: docs/kickoffs/56-pla10-promote1-authoring-worklist.md in full
(§1.1 lanes, §2 rulings, §3 spec corrections, §4 the 93 rows, §4.1 the 47
flagged rows) and its .tsv; the docstring of
tools/promote_pla10_planting_layout.py (the stage format and every guard);
docs/specs/pla10-field-shape.md §1.1, §1.6, §2.4, §3, §9, §10.1.

RULINGS IN FORCE (Trevor, 2026-10-01; not reopened):
W1 Author the page's figure; adjudicate restatements in the same promote;
   each a decision row quoting the page. A sowing distance is never the
   in-row figure where the page also states a thinned or final spacing.
W2 A stated minimum authors as [x,x] with "minimum" in the decision row,
   UNLESS another cited page for the crop states a range (range wins,
   minimum noted). A minimum-only row figure stays not_authored unless the
   sentence is a recommendation.
W3 Accept a group-scoped page where it names the crop's group and the
   species is shared (habanero on UMD; citrus on HS132). Hunt first for
   dry-bean, field-corn, nectarine; if the hunt fails, accept the sibling
   page with the scope recorded. Same species is not a waiver case.
W4 pomegranate: never author a figure the page disowns. sweet-pea's
   trellis density is promote 2's. cherry-sweet keeps R1's finding.
W5 R5 eligibility = "no CITABLE page after a recorded hunt". Eligible (13):
   bok-choy, rosemary, mulberry, borage, cosmos, sweet-alyssum, bee-balm,
   viola, echinacea, cherry-sour, pomegranate, sweet-pea, cherry-sweet.
   Waiver terms: in_row byte-equal to today's spacing_inches, listed by
   name, shrink-only. NCSU Toolbox "Available Space To Plant" is a
   footprint, never a spacing.
W6 One page per entry; a span from two clauses of ONE page is fine; a
   value joined from two pages moves to one page's figure (W1).

THREE LANES, IN PARALLEL (worklist 56 §1.1):
A (mechanical, fan-out): the 46 AGREES rows. Read agents in batches; per
  crop: fetch the page from RAW BYTES (two user agents), write
  tools/.evidence_cache/<sha256>.<ext>, check the quote is a substring of
  the hashed bytes, write the crop's stage file
  (tools/staging/pla10_promote1/crops/<slug>.json). Agents RETURN their
  MANIFEST.tsv and EVIDENCE.tsv rows; they do not write those files. No
  judgment calls: a missing quote or a changed page moves the crop to B.
B (judgment, serial, main session): the 47 flagged rows of §4.1 under
  W1-W6, each a decision row quoting the page; plus lane A hand-overs and
  lane C results.
C (hunts, ONE subagent): recorded hunts for cosmos, sweet-alyssum,
  echinacea, cherry-sour, pomegranate, sweet-pea, cherry-sweet (W5) and
  dry-bean, field-corn, nectarine (W3). Per crop: pages tried, what each
  states, FOUND / NOT FOUND. Write the record to
  tools/staging/pla10_promote1/HUNTS.md. field-corn's result goes to
  session 3 (it owns the corn). A W5 NOT FOUND is a waiver candidate,
  filled in the data commit, not here.
ISOLATION: each lane writes only its own crops' stage files. EVIDENCE.tsv
and tools/.evidence_cache/MANIFEST.tsv are appended by ONE writer, the main
session merging agent output; never written concurrently.

STAGE RULES (the promote enforces them; read its docstring): one entry
per crop unless the page forks; ids pinned at first authoring
(row-none, block-none, hill-none); sources must be catalog ids the crop
already cites with that url in anchoring_urls; every numeric field has an
EVIDENCE row whose quote states an endpoint (inches or feet); the 11
crops carrying spacing_inches_anchoring_urls need retired_anchor
(moved | {"dropped": reason}); a crop whose spacing moves lists every
restatement the scanner flags (restatements: agrees | edited, with edits).
Check progress with:
  python3 tools/promote_pla10_planting_layout.py --check
It REFUSES on the fixed list until all 113 are staged; read which crops
remain. NOTHING LANDS UNTIL ALL 113 ARE STAGED: no promote, no canonical
write, no arming in this session.

NOT THIS SESSION: the 20 session-3 crops (hills, corn, the five D1 blend
repairs + spaghetti's decision row, apple, artichoke, asparagus), the
microgreens, any canonical write, any gate arming, support entries,
heights, trellis spacings.

TESTS: changes under tools/ run the AFFECTED SET (CLAUDE.md, 4a6ab59), not
the full tree. Staging data under tools/staging/ is not tools logic.

HAND-OFF TO SESSION 3: stage files for the 93, merged EVIDENCE.tsv +
MANIFEST.tsv, HUNTS.md, a --check run showing only the 20 session-3 crops
missing, the list of crops whose figure moves (they owe restatement
adjudication), and the R5 waiver candidates with their recorded hunts.
Session 3 stages the 20, runs the independent source-truth review, the
gauntlet, arms the gates and lands the data commit (worklist 56 §8).

COMMITS: ask Trevor before each commit. The stage files, HUNTS.md and the
evidence bytes are data under tools/staging/ and tools/.evidence_cache/,
not tools logic (no test run beyond the promote's --check).
CLOSE: dated section on PLA-10 (crops staged per lane, decision rows,
hunt outcomes, what session 3 inherits). Push only on Trevor's go.
```
