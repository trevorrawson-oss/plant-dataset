# GS Cross-Crop Field Addition — methodology proposal (v0)

**Status:** proposal, v0 — for the certification workstream to formalize. Not yet a runbook.
**Drafted:** 2026-06-30
**Origin:** surfaced during the plant-app "Seed Starting & Trays" feature design. The app needed a
structured germination-window field (`day_range_from_sow`) that is present on some crops and absent
on others — which exposed that we have no repeatable, gold-standard way to add **one field across
all crops**. This won't be the last new field a consumer asks for, so the process deserves a
template.

---

## 1. The gap this fills

The dataset already has a mature **per-crop** gold-standard arc (`verification_status.status =
"verified_gs_arc"`): a whole crop is authored/refit from T1 sources, modeled structurally on a
certified reference crop (e.g. radish pilot modeled on certified carrot), run through a Claude-Code
correction + biology-review loop, then certified. That arc is **horizontal** — *all fields for one
crop*.

What's missing is the **vertical** complement: a gold-standard arc for **one field (a column) added
across many crops**. Without a template, bots produce inconsistent shapes, the null/N-A rule is
applied unevenly, and crops certified before the field existed silently drift out of coverage.

This is the same rigor, rotated 90°.

## 2. The template — a "column GS arc"

1. **Field contract first.** Before any crop is touched, lock the field spec: name, shape/type
   (e.g. `day_range_from_sow: [min, max]` integer days from sow), units, semantics, allowed-null
   policy, and — critically — **when empty is *correct* vs. a gap**. This is the column's analog of
   "modeled on certified carrot."
2. **Diverse pilot, not just "a few."** Pick crops that stress the contract: a fast case, a slow
   case, and at least one where the field is **legitimately N/A** (so the pilot proves the honesty
   rule, not just the happy path). Run the same correction + review loop the per-crop arc uses.
3. **Bot rollout with a gate.** Two things the per-crop arc gets implicitly that a column arc must
   make explicit:
   - a **schema-validation test** (the field's shape is uniform everywhere it is present), and
   - a **coverage report** (present / legitimately-null / TODO), so partial rollout is visible,
     never silent.
4. **Honest partial coverage.** Consumers must read the field **gracefully** — render it where
   present, omit it where absent, never fabricate. A field may therefore land incrementally without
   breaking the app or website. (The plant-app spine already enforces this "no fabricated precision"
   discipline downstream.)
5. **Fold into the per-crop checklist.** Once a field is "standard," it joins the per-crop GS-arc
   definition so **newly-certified crops get it natively** — otherwise every new crop the bots
   certify reopens a backfill treadmill.

## 3. The key wrinkle — amending already-certified crops

Adding a column to a crop that was certified *before* the field existed must **not** re-open that
crop's whole certification. Record **per-field provenance** — a `field_additions` log entry or a
`verification_status` sub-entry carrying just the new column's source(s) and date — so e.g. adding
`day_range_from_sow` to certified-broccoli appends the column with its own T1 source without
invalidating broccoli's existing cert.

## 4. First candidate pilot: `day_range_from_sow`

A real, low-risk first instance of the template:

- **What it is:** `growth_stages[].day_range_from_sow = [min, max]` days from sow to that stage —
  for the germination stage, the "you should be seeing sprouts" window.
- **Coverage today (of the 31 app-certified crops):** ~12 have it (basil `[5,14]`, cherry-tomato
  `[5,10]`, beefsteak `[5,10]`, carrot `[0,21]`, radish `[0,7]`, onion `[7,21]`, …); the rest do
  not. Notably missing on tray-started annuals: **brussels-sprouts, cabbage, cauliflower, kale,
  broccoli, pumpkin, butternut-squash, zucchini, zinnia** — the number exists only as *prose* in
  the germination stage's `what_to_look_for` text ("in about 5 to 10 days…").
- **Why it's an easy pilot:** the value is already authored in prose, so it's a *structuring* job,
  not new research. Lift the prose number into the structured `day_range_from_sow`, sourced to the
  same T1 set already cited for the stage.
- **The legitimately-null case:** crops not started from seed by the user — perennials/trees grown
  from transplant/bare-root (apple, blueberry, etc.) have no from-sow germination window. (Note:
  *direct-sown* annuals like radish/beet still germinate from sow and DO carry the field — direct vs.
  tray is a `weeks_indoors` question, separate from whether `day_range_from_sow` applies.)

## 5. Out of scope / open for the cert session

- Exact storage of per-field provenance (`field_additions` log vs. `verification_status` sub-entry).
- Whether the schema-validation gate lives in the existing test tooling or a new check.
- Prioritized backlog of fields that want this treatment — tracked in `docs/field_addition_register.md`
  (germination window is entry #1, deferred until the roster is complete).

---

*Cross-ref: plant-app seed-trays design consumes `day_range_from_sow` (sprout window) and
`weeks_indoors` (ready-to-transplant), both read gracefully — present-or-omitted, never fabricated.*
