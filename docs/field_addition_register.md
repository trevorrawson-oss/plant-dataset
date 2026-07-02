# Field-Addition Register — the live queue for cross-crop field additions

**What this is:** the standing, tracked queue of new fields to add across the crop roster, plus the
status and **trigger condition** for each. Consult this **before** adding any field that spans crops.
It is the "track" that makes the cross-crop field-addition process visible instead of buried.

**Method:** follow `docs/gs_cross_crop_field_addition_v0.md` (the "column GS arc" template — contract
first → diverse pilot incl. a legitimately-N/A case → bot rollout with a schema-validation gate +
coverage report → fold into the per-crop checklist OR run as a post-roster column pass; amend
already-certified crops with per-field provenance, never a full re-cert).

**Standing principle (load-bearing):** **run a column pass against a STABLE / complete roster, not
mid-certification.** Adding a datapoint while crops are still being certified re-opens already-done
crops *and* bolts the field onto in-flight ones — a moving target. Prefer: finish the roster, then
one clean column pass.

---

## Register

| # | Field | Status | Trigger | Approach | Consumer / notes |
|---|---|---|---|---|---|
| 1 | `growth_stages[].day_range_from_sow` (germination "expect sprouts in ~N days" window) | **deferred** | full crop roster (~123) certified | single **post-roster column pass** (NOT folded into the per-crop checklist this round) | plant-app **seed trays** reads it for the sprout-window line; it **graceful-omits** where absent, so the feature is **not blocked** — the line lights up when this lands. The number is already authored in each germination stage's prose ("in about 5 to 10 days…"), so this is a *structuring* job, not new research. Present today on ~12 of 31 app-certified crops; missing on tray-started annuals (brussels, cabbage, cauliflower, kale, broccoli, pumpkin, butternut, zucchini, zinnia). Legitimately-N/A: crops not grown from seed (perennials/trees — bare-root/nursery). |

*(Add a row when a consumer needs a new cross-crop field. Keep status/trigger current.)*

---

## To adopt (cert session)

1. **Surface it where it'll be seen** — add a one-line pointer to plant-dataset `CLAUDE.md` (the file
   every cert session auto-loads), e.g.:

   ```markdown
   ## Adding a cross-crop field
   Before adding any field across crops, follow `docs/gs_cross_crop_field_addition_v0.md` and check
   `docs/field_addition_register.md` (live queue + trigger conditions). Run column passes against a
   stable roster, never mid-certification.
   ```

2. **Graduate the method** from `gs_cross_crop_field_addition_v0.md` (proposal) to `_v1_0` once adopted.
3. **Commit** this register + the note on your terms (left untracked by the plant-app session that
   drafted them — origin: the seed-trays feature design, 2026-06-30).
