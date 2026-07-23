# Variety disease-resistance matrices: T1 provenance (apple + strawberry)

Every grade below traces to a real, fetched Tier-1 extension source (verified `2026-07-23`). Absence
is honest silence: a (variety, disease) pair is graded ONLY when a fetched T1 source states a level
for that exact named cultivar. A variety with no fetched T1 grade carries no `resistance` key at all.

## Enum-mapping rule (the 6-point extension scale to the 4-value grade enum)

Extension tables rate on a 6-point ordinal scale (Very/Highly Resistant, Resistant, Moderately
Resistant, Moderately Susceptible, Susceptible, Very/Highly Susceptible). Mapped monotonically:

- **immune** -- ONLY when a T1 source uses the literal word "immune" (or "not susceptible" / "no
  infection"). "Highly/Very Resistant" is NOT immune.
- **resistant** <- "Very Resistant" / "Highly Resistant" / "Resistant".
- **tolerant** <- "Moderately Resistant" / "Intermediate" (the source's exact wording is recorded per grade).
- **susceptible** <- "Moderately Susceptible" / "Susceptible" / "Very (Highly) Susceptible". The
  "moderately" qualifier is noted per grade; the divide falls between Moderately Resistant (tolerant)
  and Moderately Susceptible (susceptible).

A grade is OMITTED (honest silence) when the two primary T1 tables disagree ACROSS the
resistant/susceptible line, or when a single table's cell is internally split (e.g. "Resistant,
Susceptible").

---

## Sources catalogued for this content

- **`cornell_ext`** -- Cornell Apple Variety Database, "Disease Susceptibility Ranking of Apples."
  https://blogs.cornell.edu/applevarietydatabase/disease-susceptibility-of-common-apples/ (fetched
  2026-07-23). Columns: Fire blight, Apple Scab, Powdery Mildew, Cedar Apple Rust, Leaf Spots. The
  PRIMARY apple matrix source (all four diseases, one page). Some cells compile multiple references
  and show a range or split (e.g. "Resistant, Susceptible"); those are treated per the omit rule.
  - New sub-id proposed at promote: `cornell_ext_apple_disease` (page sub-id under the catalogued T1
    parent `cornell_ext`), URL as above, verified 2026-07-23.
- **`cornell_ext` (Khan Lab)** -- Cornell, Khan Lab (Cornell AgriTech, Geneva), "Apple Scab
  Susceptibility of Common Cultivars." https://blogs.cornell.edu/khanlab/extension/apple-scab-susceptibility-of-common-cultivars/
  (fetched 2026-07-23). Categories: Very Resistant, Resistant, Moderately Resistant, Moderately
  Susceptible, Susceptible, Very Susceptible. Used to CORROBORATE the scab column.
  - Companion page (fire blight): https://blogs.cornell.edu/khanlab/extension/fire-blight-susceptibility-of-common-apple-cultivars/
    (fetched 2026-07-23) -- corroborates the fire-blight column (compiled multi-reference cells).
  - New sub-id proposed at promote: `cornell_ext_apple_scab` / `cornell_ext_apple_fireblight`.
- **`purdue_ext`** -- Purdue Extension, BP-132-W, Janna Beckerman, "Disease Susceptibility of Common
  Apple Cultivars." https://www.extension.purdue.edu/extmedia/BP/BP-132-W.pdf (fetched 2026-07-23 as
  PDF; text extracted with pypdf in-controller, since WebFetch cannot decode PDFs). Legend: VR=Very
  Resistant, R=Resistant, MR=Moderately Resistant, MS=Moderately Susceptible, S=Susceptible, VS=Very
  Susceptible, N/A=Data not available. Columns: Apple scab, Fire Blight, Juniper rusts (= cedar-apple
  rust and relatives), Powdery Mildew. The SECOND independent apple table. Note the publication's own
  caution: "resistance is not immunity. Even highly resistant varieties can succumb to any disease
  under extreme environmental conditions and stress."
  - `purdue_ext` is a NEW T1 source id (Purdue University Cooperative Extension). Add at promote with
    the URL above, verified 2026-07-23.
- **`umn_ext`** -- UMN Extension, "Apple scab of apples and crabapples."
  https://extension.umn.edu/plant-diseases/apple-scab (fetched 2026-07-23). Supplies the explicit
  "immune" wording for Liberty (already catalogued T1).
- **`umd_ext`** -- (via UMaine here) see strawberry section.
- **`umaine_ext`** -- UMaine Cooperative Extension, Bulletin #2184, "Strawberry Varieties for Maine."
  https://extension.umaine.edu/publications/2184e/ (fetched 2026-07-23). PRIMARY strawberry red-stele
  / verticillium source (already catalogued T1).
- **`mu_ext`** -- MU Extension, G6135, "Home Fruit Production: Strawberry Cultivars and Their
  Culture." https://extension.missouri.edu/publications/g6135 (fetched 2026-07-23). CORROBORATES
  strawberry red-stele / verticillium (already catalogued T1).
- **`cornell_ext` (berries)** -- Cornell, "Red Stele Root Rot of Strawberry."
  https://blogs.cornell.edu/livegpath/gallery/strawberries/red-stele-root-rot-of-strawberry/ (fetched
  2026-07-23). CORROBORATES the strawberry red-stele resistant-variety list.
  - New sub-id proposed at promote: `cornell_ext_strawberry_redstele`.
- **`ncsu_ext`** -- NC State Extension, "Anthracnose Fruit Rot of Strawberry."
  https://content.ces.ncsu.edu/anthracnose-fruit-rot-of-strawberry (fetched 2026-07-23). Sole source
  for Albion anthracnose (already catalogued T1).

---

# APPLE

Legend shorthand below: DB = Cornell Apple Variety Database; Khan = Cornell Khan Lab page;
Purdue = BP-132-W; UMN = UMN apple-scab page.

## dorsett-golden
- **apple-scab: susceptible** <- DB row "Dorsett Golden | Susceptible [fire blight] | Susceptible
  [apple scab] | (blank) | (blank)"; Khan lists Dorsett Golden under "Susceptible."
- **fire-blight: susceptible** <- DB row, fire-blight cell "Susceptible" (single-source, DB only).
- Undocumented (omitted): cedar-apple-rust, powdery-mildew (DB cells blank; Purdue does not list this
  low-chill cultivar).

## anna
- **apple-scab: susceptible** <- DB row "Anna | Susceptible | Susceptible | (blank) | (blank)"; Khan
  lists Anna under "Susceptible."
- **fire-blight: susceptible** <- DB fire-blight cell "Susceptible" (DB only).
- Undocumented (omitted): cedar-apple-rust, powdery-mildew (DB blank; not in Purdue).

## ein-shemer
- **apple-scab: susceptible** <- DB row "Ein Shemer | Susceptible | Susceptible | (blank) | (blank)";
  Khan lists Ein Shemer under "Susceptible."
- **fire-blight: susceptible** <- DB fire-blight cell "Susceptible" (DB only).
- Undocumented (omitted): cedar-apple-rust, powdery-mildew (DB blank; not in Purdue).

## zestar
- **apple-scab: susceptible** <- Khan "Moderately Susceptible"; Purdue "MS"; UMN lists Zestar!(TM)
  under "Very likely to be infected by apple scab." (Mapping: Moderately Susceptible -> susceptible;
  UMN's "very likely" is the stronger read, so susceptible is well-supported.)
- **fire-blight: susceptible** <- DB "Moderately Susceptible; Susceptible"; Purdue "MS."
- **cedar-apple-rust: susceptible** <- DB "Susceptible"; Purdue "S."
- **powdery-mildew: resistant** <- DB "Resistant"; Purdue "R."

## mcintosh
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Very Susceptible"; Purdue "S"; UMN
  lists McIntosh under "Very likely to be infected by apple scab."
- **fire-blight: susceptible** <- DB "Moderately Susceptible"; Purdue "S." (Mapping: MS -> susceptible.)
- **cedar-apple-rust: resistant** <- DB "Highly Resistant"; Purdue juniper-rusts "VR."
- **powdery-mildew: tolerant** <- DB "Moderately Resistant"; Purdue "MR." (Mapping: Moderately
  Resistant -> tolerant. Source wording: "Moderately Resistant.")

## liberty
- **apple-scab: immune** <- UMN apple-scab page, verbatim: "Immune to apple scab: Dayton, Freedom,
  Liberty, McShay, Pixie Crunch, Pristine, Redfree, William's Pride." (Explicit "immune" wording, so
  the immune grade is warranted; DB rates it "Highly Resistant" and Khan "Very Resistant," which are
  consistent but weaker, so UMN's literal "immune" is the governing source.) Agrees with the variety
  `disease_notes` ("Immune to apple scab") and `note_seasoned` ("Scab-immune Cornell cultivar").
- **fire-blight: tolerant** <- DB "Moderately Resistant"; Khan majority "Moderately Resistant."
  (Mapping: Moderately Resistant -> tolerant. Purdue rates "R"/resistant -- a degree difference on the
  resistant side; tolerant is the conservative call from the primary DB.)
- **cedar-apple-rust: resistant** <- DB "Highly Resistant"; Purdue "VR."
- **powdery-mildew: resistant** <- DB "Resistant"; Purdue "R."

## empire
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Very Susceptible"; Purdue "VS."
- **fire-blight: tolerant** <- DB "Moderately Resistant." (Mapping: Moderately Resistant -> tolerant;
  Purdue rates "R," resistant side, degree difference. Source wording: "Moderately Resistant.")
- **cedar-apple-rust: resistant** <- DB "Resistant"; Purdue "R."
- **powdery-mildew: susceptible** <- DB "Susceptible"; Purdue "S."

## honeycrisp
- **apple-scab: tolerant** <- DB "Moderately Resistant"; Khan "Moderately Resistant"; Purdue "MR."
  (Mapping: Moderately Resistant -> tolerant. NOTE: UMN's list instead calls Honeycrisp(TM) "Resistant
  to apple scab" -- a T1 degree difference, both on the resistant side; tolerant is the conservative
  read from the three tables that agree on "Moderately Resistant." This is why Honeycrisp is NOT the
  scab-susceptible showcase -- Gala is.)
- **fire-blight: tolerant** <- DB "Moderately Resistant" (Purdue "R," resistant-side degree diff).
- **cedar-apple-rust: susceptible** <- DB "Susceptible"; Purdue "S."
- **powdery-mildew: susceptible** <- DB "Susceptible"; Purdue "S."

## gala  (DOCUMENTED-SUSCEPTIBLE SHOWCASE for apple scab)
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Very Susceptible"; Purdue "VS." The
  classic scab-susceptible standard.
- **fire-blight: susceptible** <- DB "Highly Susceptible"; Purdue "VS."
- **cedar-apple-rust: susceptible** <- DB "Susceptible" (the precise cedar-apple-rust column; Purdue's
  broader "Juniper rusts" cell is "R--S," which includes susceptibility -- consistent).
- Undocumented (omitted): **powdery-mildew** -- DB cell is internally split ("Resistant, Susceptible")
  and Purdue is "MS"; the split fails the omit rule, so no grade (honest silence within a graded variety).

## golden-delicious
- **apple-scab: susceptible** <- DB "Susceptible"; Khan "Susceptible"; Purdue "S."
- **fire-blight: susceptible** <- DB "Moderately Susceptible"; Purdue "S."
- **cedar-apple-rust: susceptible** <- DB "Susceptible"; Purdue "S."
- **powdery-mildew: susceptible** <- DB "Highly Susceptible"; Purdue "VS."

## jonagold
- **apple-scab: susceptible** <- DB "Susceptible"; Khan "Susceptible"; Purdue "S."
- **fire-blight: susceptible** <- DB "Highly Susceptible"; Purdue "VS."
- **cedar-apple-rust: resistant** <- DB "Resistant"; Purdue "R."
- **powdery-mildew: susceptible** <- DB "Susceptible"; Purdue "S."

## mutsu
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Very Susceptible"; Purdue "VS."
- **fire-blight: susceptible** <- DB "Highly Susceptible"; Purdue "VS."
- **cedar-apple-rust: susceptible** <- DB "Susceptible"; Purdue "S."
- **powdery-mildew: susceptible** <- DB "Susceptible"; Purdue "S."

## fuji
- **apple-scab: susceptible** <- DB "Susceptible"; Khan "Susceptible"; Purdue "S."
- **fire-blight: susceptible** <- DB "Moderately Susceptible, Highly Susceptible"; Purdue "VS."
- **cedar-apple-rust: susceptible** <- DB "Susceptible" (precise cedar-apple-rust column; Purdue
  juniper-rusts "R--VS" includes susceptibility -- consistent).
- Undocumented (omitted): **powdery-mildew** -- DB cell internally split ("Resistant, Highly
  Susceptible"); even though Purdue is "R," the DB split fails the omit rule, so no grade.

## granny-smith
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Susceptible"; Purdue "S."
- **fire-blight: susceptible** <- DB "Highly Susceptible"; Purdue "VS."
- **powdery-mildew: susceptible** <- DB "Highly Susceptible"; Purdue "VS."
- Undocumented (omitted): **cedar-apple-rust** -- FLAGGED T1 CONFLICT. DB "Highly Susceptible" vs
  Purdue juniper-rusts "R" (Resistant) disagree across the resistant/susceptible line, so no grade.

## pink-lady
- **apple-scab: susceptible** <- DB "Highly Susceptible"; Khan "Very Susceptible"; Purdue "VS."
- **fire-blight: susceptible** <- DB "Moderately Susceptible, Highly Susceptible"; Purdue "VS."
- **cedar-apple-rust: resistant** <- DB "Resistant"; Purdue "R."
- **powdery-mildew: resistant** <- DB "Resistant"; Purdue "R."

## dolgo  (crabapple pollinizer)
- **apple-scab: resistant** <- DB "Resistant"; Khan "Resistant" (Purdue "S-R" range; the two clean
  "Resistant" ratings govern).
- **cedar-apple-rust: tolerant** <- DB "Moderately Resistant"; Purdue juniper-rusts "MR." (Mapping:
  Moderately Resistant -> tolerant.)
- **powdery-mildew: resistant** <- DB "Resistant"; Purdue "R."
- Undocumented (omitted): **fire-blight** -- FLAGGED T1 CONFLICT. DB "Moderately Susceptible" vs
  Purdue "R" (Resistant) disagree across the resistant/susceptible line, so no grade.

---

# STRAWBERRY

## honeoye  (DOCUMENTED-SUSCEPTIBLE case)
- **red-stele: susceptible** <- UMaine 2184, verbatim: "Susceptible to red stele and no known
  resistance to verticillium." MU G6135: "not resistant to red stele or verticillium wilt." Agrees
  with `note_seasoned` ("red stele and verticillium take hold").
- **verticillium-wilt: susceptible** <- UMaine "no known resistance to verticillium"; MU "not
  resistant to ... verticillium wilt"; reinforced by the variety note. (Grades the documented lack of
  resistance plus the note's explicit "take hold" as susceptibility.)
- Undocumented (omitted): gray-mold, anthracnose, powdery-mildew (MU calls it "tolerant of most
  foliage diseases" -- too non-specific to grade any single foliar disease id).

## earliglow
- **red-stele: resistant** <- UMaine "resistant to red stele and verticillium wilt"; Cornell red-stele
  page names Earliglow among "Varieties resistant to red stele and also Verticillium wilt." Agrees
  with `note_seasoned` ("good resistance to red stele and verticillium").
- **verticillium-wilt: resistant** <- UMaine "... and verticillium wilt"; Cornell "... also
  Verticillium wilt."
- Undocumented (omitted): gray-mold, anthracnose, powdery-mildew (MU's "resistance to leaf and root
  diseases" is non-specific).

## jewel  (DOCUMENTED-SUSCEPTIBLE case)
- **red-stele: susceptible** <- UMaine "No known resistance to red stele or verticillium wilt"; MU "no
  resistance to red stele or verticillium wilt." Agrees with `note_seasoned` ("red stele and
  verticillium can set in").
- **verticillium-wilt: susceptible** <- UMaine + MU, same wording.
- Undocumented (omitted): gray-mold, anthracnose, powdery-mildew.

## allstar
- **red-stele: resistant** <- UMaine "Resistant to red stele and verticillium"; Cornell red-stele page
  names Allstar among "Other varieties resistant to red stele"; MU "resistant to red stele and
  verticillium wilt." Agrees with `note_seasoned` ("Resistant to both red stele and verticillium wilt").
- **verticillium-wilt: resistant** <- UMaine + MU, same wording.
- Undocumented (omitted): gray-mold, anthracnose, powdery-mildew.

## albion  (DOCUMENTED-SUSCEPTIBLE case, anthracnose axis)
- **anthracnose: susceptible** <- NC State, "Anthracnose Fruit Rot of Strawberry," verbatim: "The
  disease can be especially destructive to susceptible California strawberry cultivars (e.g. Chandler,
  Camarosa, Albion) when grown on black plastic." (The graded id is the generic `anthracnose`; NC
  State documents the FRUIT-ROT phase specifically. No contradiction with the variety note, which
  makes no disease claim.)
- Undocumented (omitted): gray-mold, powdery-mildew, red-stele, verticillium-wilt. NOTE: UC-derived
  descriptions call Albion Verticillium-resistant, but that surfaced only in non-T1 aggregators and a
  UC plant patent, not a fetched T1 extension page, so it is NOT graded (T1-only honesty).

## tristar
- **red-stele: resistant** <- UMaine "Resistant to red stele and verticillium wilt"; Cornell red-stele
  page names Tristar among "Other varieties resistant to red stele"; MU "resistant to red stele and
  verticillium wilt." Consistent with `note_seasoned` ("vigorous and disease-resistant").
- **verticillium-wilt: resistant** <- UMaine + MU, same wording.
- Undocumented (omitted): gray-mold, anthracnose, powdery-mildew.

---

# N/A branch audit (which pairs / varieties carry no grade, and why)

## Fully-absent varieties (NO `resistance` key at all)
- **Strawberry: seascape** -- no fetched T1 extension page grades it on any of the five strawberry
  disease ids (UMaine "Not listed"; MU no mention; Cornell red-stele list does not reference it; NC
  State anthracnose page does not name it). Honest silence.
- **Strawberry: ozark-beauty** -- no fetched T1 grade (MU does not mention it; not in Cornell red-stele
  list; not in UMaine 2184; not on the NC State anthracnose page). Honest silence.
- **Strawberry: quinault** -- no fetched T1 grade on any of the five ids. Honest silence.
- **Apple: NONE.** All 16 apple varieties carry at least an apple-scab grade, because the Cornell
  Apple Variety Database grades every one of them (the low-chill trio Anna / Dorsett Golden /
  Ein Shemer are genuine rows -- verified against neighboring rows -- with fire blight = Susceptible
  and apple scab = Susceptible, other columns blank). Manufacturing an "absent" apple by suppressing
  real Cornell grades would violate the honesty model, so apple does not exercise the fully-absent
  branch. The pilot-level requirement is met by strawberry (seascape / ozark-beauty / quinault).

## Undocumented (variety, disease) pairs within GRADED varieties (key omitted, never defaulted)
- Apple low-chill trio (anna, dorsett-golden, ein-shemer): cedar-apple-rust + powdery-mildew omitted
  (DB cells blank; not in Purdue).
- gala: powdery-mildew omitted (DB cell split "Resistant, Susceptible").
- fuji: powdery-mildew omitted (DB cell split "Resistant, Highly Susceptible").
- granny-smith: cedar-apple-rust omitted (FLAGGED T1 conflict: DB "Highly Susceptible" vs Purdue "R").
- dolgo: fire-blight omitted (FLAGGED T1 conflict: DB "Moderately Susceptible" vs Purdue "R").
- All strawberry graded varieties: gray-mold / anthracnose / powdery-mildew omitted where no per-variety
  T1 grade exists (the red-stele + verticillium axis is the documented one; the fruit-rot/foliar axes
  are genuinely sparse per-variety, as expected -- not a gap to fill).

## Note-vs-table observations flagged (not silent picks)
1. **granny-smith cedar-apple-rust** -- Cornell DB "Highly Susceptible" vs Purdue "R" (Resistant):
   direct T1-vs-T1 conflict across the resistant/susceptible line. Left UNGRADED rather than picking a
   side. (Neither contradicts variety prose, which makes no rust claim.)
2. **dolgo fire-blight** -- Cornell DB "Moderately Susceptible" vs Purdue "R": T1-vs-T1 conflict across
   the line. Left UNGRADED.
3. **honeycrisp apple-scab** -- UMN "Resistant to apple scab" vs Cornell DB/Khan/Purdue "Moderately
   Resistant." A degree difference (both resistant-side, not a resistant/susceptible flip). Graded the
   conservative `tolerant`; recorded here for transparency.
4. No graded value CONTRADICTS a variety's `disease_notes` / `note_seasoned` prose. Liberty
   (immune scab) and the strawberry red-stele/verticillium grades match their prose exactly.
