# Berry variety gate: adversarial RED proof on real strawberry shape

Task 3 of the berry variety pilot (strawberry, the 5th variety archetype). CLAUDE.md requires
every new gate to be adversarially stress-tested: inject the defect class into a scratch copy,
confirm it bounces, before the gate is trusted.

## Setup

The berry gate (`tools/variety_detail_gate.py`, committed Task 1, `berry_group` dispatch
committed Task 2) was proven against an in-memory scratch strawberry crop built from the real
canonical strawberry's 9 variety names, rewritten to the flat berry schema with minimal
placeholder prose (`hero_description="h"`, `note_beginner="b"`, `note_seasoned="s"`; real
authoring is Task 4/5).

- 4 varieties `bearing_habit="june_bearing"`: Honeoye, Earliglow, Jewel, Allstar
- 3 varieties `bearing_habit="day_neutral"`: Albion, Seascape, Tristar
- 2 varieties `bearing_habit="everbearing"`: Ozark Beauty, Quinault
- Crop-level: `variety_archetype:"berry"`, `berry_group:"strawberry"`, `days_to_maturity:[]`
- Exactly one `is_reference:true` (Albion)
- Each variety: `id` (slug of name), `name`, `bearing_habit`, `maturity_class`
  (early/mid), `use:"fresh"`, `confidence_tier:"T1"`, `sources:["ucanr_ext_8256"]`,
  `hero_description`, `note_beginner`, `note_seasoned`

Green baseline: `variety_violations(scratch_strawberry) == []`, confirmed before injecting any
defect.

Canonical `crops_data_final.json` was read-only throughout (only the real strawberry's variety
names were read, to seed realistic fixture data); nothing was written back to it. Canonical SHA
before and after this task: `8dd4ac4c3b543bfbb3779fcf4fcafe0d4f34f3942476c6b21272e5c687d21503`
(matches `LATEST.txt`), unchanged. Working tree was clean before and after (aside from this note).

Harness: `/private/tmp/berry_red_proof.py` (re-runnable, `python3 /private/tmp/berry_red_proof.py`).

## Results: 8/8 defect classes bounce

| # | Defect class | Mutation | Expected substring | Result |
|---|---|---|---|---|
| 1 | `bearing_habit` is a cane value under strawberry group | Honeoye `bearing_habit="summer_bearing"` | `bearing_habit` | BOUNCED (1 violation) |
| 2 | missing required field | drop `hero_description` on Earliglow | `hero_description` | BOUNCED (1 violation) |
| 3 | bad enum | Jewel `maturity_class="everbearing"` | `maturity_class` | BOUNCED (1 violation) |
| 4 | two references | Seascape also `is_reference:true` (alongside Albion) | `exactly one` | BOUNCED (1 violation) |
| 5 | duplicate id | Tristar `id` set equal to Allstar's `id` | `duplicate variety id` | BOUNCED (1 violation) |
| 6 | chill field not allowed for strawberry | Ozark Beauty `chill_hours_required:800` | `chill_hours_required not allowed` | BOUNCED (1 violation) |
| 7 | invalid crop-level `berry_group` | crop `berry_group:"vine"` | `berry_group` | BOUNCED (10 violations: the crop-level `berry_group` message plus all 9 varieties' `bearing_habit` failing against an empty valid-habit set for an unknown group) |
| 8 | reserved cane crop with strawberry-shaped habits | crop `berry_group:"cane"`, varieties left as june_bearing/day_neutral/everbearing | `bearing_habit` and `for berry_group 'cane'` | BOUNCED (9 violations, one per variety, each message containing both required substrings) |

Every assertion checked both that the violation list was non-empty AND that the expected
substring(s) were present in the joined violation text (non-vacuous).

Full harness output:

```
BASELINE: green scratch strawberry -> 0 violations (as expected)
DEFECT 1 (bearing_habit=summer_bearing (cane value under strawberry group)): BOUNCED, 1 violation(s), substrings ['bearing_habit'] all present -- PASS
DEFECT 2 (drop hero_description): BOUNCED, 1 violation(s), substrings ['hero_description'] all present -- PASS
DEFECT 3 (maturity_class=everbearing (bad enum)): BOUNCED, 1 violation(s), substrings ['maturity_class'] all present -- PASS
DEFECT 4 (two varieties is_reference:true): BOUNCED, 1 violation(s), substrings ['exactly one'] all present -- PASS
DEFECT 5 (duplicate variety id): BOUNCED, 1 violation(s), substrings ['duplicate variety id'] all present -- PASS
DEFECT 6 (chill_hours_required=800 under strawberry group): BOUNCED, 1 violation(s), substrings ['chill_hours_required not allowed'] all present -- PASS
DEFECT 7 (berry_group=vine (invalid crop-level value)): BOUNCED, 10 violation(s), substrings ['berry_group'] all present -- PASS
DEFECT 8 (berry_group=cane (reserved) with strawberry-habit varieties): BOUNCED, 9 violation(s), substrings ['bearing_habit', "for berry_group 'cane'"] all present -- PASS

8/8 defect classes bounced (all PASS). Green baseline confirmed clean.
```

## Conclusion

The berry gate correctly rejects all 8 targeted defect classes on a real-shaped strawberry crop
(4 june-bearing, 3 day-neutral, 2 everbearing varieties), while the correctly-shaped scratch
crop passes clean. Task 3's RED proof is satisfied; the gate is trusted for Task 4 authoring.
