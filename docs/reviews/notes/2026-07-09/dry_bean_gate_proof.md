# dry-bean -- adversarial RED gate proof (Task 5)

**Date:** 2026-07-10. Each defect class injected into the CERTIFIED dry-bean draft on a scratch
copy; the always-on suite must bounce it (CLAUDE.md adversarial rule). Clean crop passes (GREEN).

| Defect injected | Caught by | Result |
|---|---|---|
| BASELINE (clean certified crop) | PASS | CAUGHT/PASS (should PASS) |
| 1. non-monotonic ladder (swap dry_down/harvest) | A40 ladder-monotonicity | CAUGHT/PASS (should FAIL) |
| 2. drop germination_light | A39 register-coverage | CAUGHT/PASS (should FAIL) |
| 3. absurd DTM [3,4] | numeric_sanity [7,400] | CAUGHT/PASS (should FAIL) |
| 4. em dash in description_beginner | release_verify / dash scan | CAUGHT/PASS (should FAIL) |
| 5. invalid propagule enum ('beanz') | A40 propagule enum | CAUGHT/PASS (should FAIL) |

Confirms the existing gate suite protects the new greenfield crop: no new gate was needed,
and A39/A40/numeric_sanity/release_verify dash-scan each catch their defect class on dry-bean.

**Caveat (documented, not gate-enforced):** renaming the `harvest` growth-stage id is NOT
hard-caught -- the ladder anchor falls back to the last stage (`cure_thresh`, day 95), which
stays inside the +/-15%% DTM band, so no warning fires (silent = True). The
`harvest` id is therefore pinned by the spec/plan as an explicit constraint, not by a gate.
