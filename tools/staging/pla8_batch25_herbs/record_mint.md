# PLA-8 BATCH 25 -- RECORD / SOURCE PASS: MINT

Reviewer: MINT record reviewer. Date of all fetches below: **2026-09-04**.
Canonical read-only, SHA `a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`. No file other than this
one was written. `crops_data_final.json` untouched.

Subject: `tools/staging/pla8_batch25_herbs/mint_source.json`, `pests[]` (3) and `diseases[]` (3).

---

## 0. READ-BEFORE-ACTING: what mint's own cert log already adjudicated

Per the "cert log already adjudicated the band" rule, I read `verification_status.verification_log_ref`
before hunting. It records the Batch-2 Wave-4 cert (2026-07-06) and is directly load-bearing here:

> "FIXES: dropped usu_ext from spider mites (USU names no mites; UC IPM does), ncsu_ext from
> verticillium wilt (NCSU lists only rust/leaf-spot; USU carries it), and uc_ipm from the
> flea-beetle/cutworm pest (UC IPM lists neither; USU does); de-named the 'mint root borer' (on
> neither cited page); struck the unanchored '(Connecticut Experiment Station and University of
> Illinois)' credits from the rust + powdery-mildew entries, keeping the valid NCSU / UC IPM parts.
> Puccinia menthae retained as textbook mint-rust."

Two things follow, and both are findings:

1. **The struck credit was not struck everywhere.** `Verticillium wilt.symptoms_seasoned` still reads
   "The Connecticut Experiment Station and Utah State both flag it for mint." The cert log says the
   Connecticut credit was removed from rust and powdery mildew; nobody checked verticillium. This is
   the "correct every field carrying an attribution" defect class, live in the record today. The
   Connecticut Agricultural Experiment Station is **not** in
   `source_catalog_admission.txt`. **STRIKE IT.**
2. **`Puccinia menthae` is on the record as admitted textbook knowledge, not as a sourced claim.** The
   cert log says "retained as textbook mint-rust", i.e. the binomial was never anchored. I confirmed
   below that neither cited document names it. **It is anchorable** -- see Mint rust.

Per the `verification_log_ref` convention this log must NOT be rewritten into current tense; if a
promote acts on this report it should APPEND a `[CORRECTION 2026-09-04: ...]` line, leaving the
original prose byte-for-byte.

---

## 1. RECORD GAP (flagged in the task): `severity` and `type` are ABSENT, not null

Measured, not asserted. On all 6 mint problems the keys `severity` and `type` **do not exist at all**
(`sorted(p.keys())` returns neither). Every other crop in batch 25 carries both on every problem:

| crop | problems | carry severity+type |
|---|---|---|
| lavender | 4 | 4 |
| lemongrass | 5 | 5 |
| oregano | 5 | 5 |
| rosemary | 5 | 5 |
| sage | 7 | 7 |
| thyme | 4 | 4 |
| **mint** | **6** | **0** |

### Roster-wide convention, computed from canonical (128 crops), not asserted

| organism | dominant `type` | counts | dominant `id` |
|---|---|---|---|
| aphids | `insect` | 85 insect / 1 pest / 1 null | `aphids` (59 crops) |
| spider mites | `mite` | 25 mite / 4 insect / 1 pest / 1 null | `spider-mites` (16), `two-spotted-spider-mite` (6) |
| cutworms | `insect` | 12 / 12 | `cutworms` (9) |
| flea beetles | `insect` | 35 insect / 1 null | `flea-beetles` (34) |
| rust (as a disease) | `fungal` | 24 fungal / 1 disease / 1 null | host-named, see §4f |
| verticillium wilt | `fungal` | 7 / 8 | `verticillium-wilt` (3), `fusarium-verticillium-wilt` (3) |
| powdery mildew | `fungal` | 36 / 36 | `powdery-mildew` (32 crops) |
| anthracnose | `fungal` | 19 fungal / 1 disease / 1 null | `anthracnose` (14 crops) |

### Proposed values for mint (with the reason, and after the splits recommended below)

| problem | severity | type | why |
|---|---|---|---|
| Aphids | `low` | `insect` | Cosmetic/contaminant on a cut-and-come-again herb; the water-jet rung usually ends it (USU, UC IPM 7404). Batch siblings oregano/thyme also `low`. |
| Spider mites | `low` | `mite` | Roster convention is `mite`, 25/31. Mint is grown wet, which is the mite defense; damage is only under drought stress. |
| Cutworms (split) | `low` | `insect` | Seedling/transplant-stage only; established mint outgrows it. |
| Flea beetles (split) | `low` | `insect` | USU's control is row cover; cosmetic shot-holing on a leaf crop. |
| Mint root borer (split) | `low` | `insect` | Real but rare in a home patch; UC IPM's damage measure is commercial oil yield. |
| Mint rust | `medium` | `fungal` | Defoliating and not curable in a culinary planting (RHS, WSU). Matches the roster's 18/32 rust records at `medium` and oregano's `Rust` at `medium`. |
| Verticillium wilt | `high` | `fungal` | This is the stand-limiting disease: no cure, soil-persistent as microsclerotia, managed only by site and renewal (UC IPM ANR 3457). |
| Powdery mildew (split) | `low` | `fungal` | Cosmetic on mint; peppermint and native spearmint "usually not seriously affected" (WSU). |
| Anthracnose (split) | `medium` | `fungal` | USU's control is rotate + remove plants + cut the whole patch to the ground in fall, which is a real cost. |

**BATCH-WIDE TYPING DEFECT found while computing this:** oregano, rosemary and thyme all type
**Spider mites as `insect`**, which is wrong (they are arachnids, and the roster convention is `mite`,
25/31; sage already gets it right). That is 3 records in this batch and 4 roster-wide. Reported, not
acted on -- it is outside mint.

---

## 2. Documents fetched, and documents that would not open

**Read successfully (2026-09-04):**

| catalog key | URL | what it gave |
|---|---|---|
| `usu_ext` | https://extension.usu.edu/yardandgarden/research/mint-in-the-garden | full "Problems with Growing Mint" section + both tables |
| `ncsu_ext` | https://plants.ces.ncsu.edu/plants/mentha-spicata/ | the whole "Insects, Diseases, and Other Plant Problems" field (one sentence pair) |
| `uc_ipm` | https://ipm.ucanr.edu/home-and-landscape/mint/ | the mint pest/disease listing |
| `uc_ipm` | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html | Pest Notes: Aphids, ANR Pub 7404, updated 07/2013 |
| `ucanr_ext_spider_mites` | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html | Pest Notes: Spider Mites, ANR Pub 7405, rev. 12/2011 |
| `uc_ipm` | https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html | Pest Notes: Powdery Mildew on Vegetables, ANR Pub 7406, updated 11/2008 |
| `uc_ipm` | https://ipm.ucanr.edu/agriculture/peppermint/ | the UC IPM peppermint (agriculture) section index |
| `uc_ipm` | https://ipm.ucanr.edu/agriculture/peppermint/verticillium-wilt/ | UC IPM PMG: Peppermint, ANR Pub 3457, Marcum & Davis, text updated 09/13 |
| `uc_ipm` | https://ipm.ucanr.edu/agriculture/peppermint/mint-root-borer/ | ANR Pub 3457, Tollerup, updated 08/2012 |
| `uc_ipm` | https://ipm.ucanr.edu/agriculture/peppermint/webspinning-spider-mites/ | ANR Pub 3457, Tollerup, updated 08/2012 |
| `rhs` | https://www.rhs.org.uk/disease/mint-rust | binomial, rhizome overwintering, host range, no-fungicide statement |
| `wsu_ext` (see caveat) | https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/MintrustA.doc | Johnson, D.A., "Management of Rust on Mint", WSU Plant Pathology -- read in full, byte-level |
| `wsu_ext` (see caveat) | https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/PowderyMildewMint.doc | Johnson, D.A., "Managing Powdery Mildew on Mint", WSU Plant Pathology |

**CATALOG-ADMISSION CAVEAT on the two WSU documents.** Catalog key `wsu_ext` is
"Washington State University Extension / https://extension.wsu.edu". These two files sit on
`s3.wp.wsu.edu` (WSU's WordPress asset host, site 2195 = WSU Plant Pathology), authored by
Dennis A. Johnson, WSU Extension plant pathologist. The catalog **already uses that exact host** for
`wsu_em051e` (`https://s3.wp.wsu.edu/uploads/sites/2073/...`) and `wsu_em057e`, so the host is not
novel to this catalog. I read them as admissible under `wsu_ext` but the promote pass should confirm
that rather than take it from me. They are commercial mint-crop documents; see the ladder notes for
where that limits their use.

**Would not open -- these are NOT absence findings (brief rule 5):**

| URL | result | tried |
|---|---|---|
| https://pnwhandbooks.org/plantdisease/host-disease/peppermint-spearmint-mentha-spp-rust | HTTP 403 | 2 paths (`/host-disease/...`, `/node/3382/print`) |
| https://extension.oregonstate.edu/catalog/em-9299-... (IPM strategic plan, OR/WA/ID mint) | HTTP 403 | 1 |
| https://extension.oregonstate.edu/gardening/techniques/how-recognize-signs-verticillium-wilt | HTTP 403 | 1 |
| http(s)://extension.cropsciences.illinois.edu/fruitveg/pdfs/1221.pdf (U of I RPD 1221, MINT RUST) | TLS: "unable to verify the first certificate" | 2 (http and https) |
| https://apsjournals.apsnet.org/doi/... (all APS full texts) | HTTP 403 | 3 |

`curl` is not permitted in this environment, so I could not retry with a second user-agent. These five
documents are almost certainly the best remaining evidence on this crop (`pnwhandbooks` in particular
is the definitive mint-disease reference for the US mint belt, and Illinois RPD 1221 is a dedicated
mint-rust fact sheet). **A follow-up with working fetch should open them before this crop's ladder is
finalized.** I did not treat their contents as unknown-because-absent anywhere below.

---

## 3. PESTS

---

## Aphids [pests] -- severity <ABSENT>, type <ABSENT>
STATUS: **SOURCED-OK**
ORGANISM: umbrella -- multiple aphid species; **no binomial in either cited document.** USU writes only
"Green or black soft-bodied insects"; UC IPM's mint page lists the bare word "Aphids". UC IPM Pest
Notes 7404 is a multi-species note. Resolve to "several aphid species", do not invent a binomial.
ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/mint-in-the-garden -- verified 2026-09-04
  > "Aphids | Green or black soft-bodied insects that feed on leaves. Foliage curls, yellows or becomes stunted. | Use insecticidal soaps, registered insecticides or spray plant with a forceful jet of water to dislodge the insects."
- `uc_ipm` https://ipm.ucanr.edu/home-and-landscape/mint/ -- verified 2026-09-04
  > Invertebrates: "Aphids" (listed for mint, alongside Leafhoppers, Spider Mites, Thrips)
- `uc_ipm` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html (ANR Pub 7404, updated 07/2013) -- verified 2026-09-04
  > "High levels of nitrogen fertilizer favor aphid reproduction, so never use more nitrogen than necessary."
  > "Aphids may transmit viruses from plant to plant on certain vegetable and ornamental plants."
  > "Knock aphid populations off plants by shaking the plant or spraying it with a strong stream of water."
  > "Apply these materials with a high volume of water, usually a 1 to 2% oil solution in water, and target the underside of leaves as well as the top."
  > "Don't apply them to drought-stressed plants or when it is very hot."
  > "Check your plants regularly for aphids—at least twice a week when plants are growing rapidly—in order to catch infestations early."
  > "Avoid the use of broad-spectrum insecticides that can be toxic to natural enemies."

RECORD CLAIMS THAT HOLD:
- Clusters on growing tips and leaf undersides; curled foliage -- USU ("Foliage curls, yellows or becomes stunted") + 7404.
- "one of the pests UC IPM lists for mint" -- **verbatim true**; UC IPM's mint page lists Aphids.
- "breed fast, especially on soft growth from too much fertilizer" / "avoid overfeeding" -- 7404 nitrogen sentence.
- "can spread plant viruses" -- 7404 virus sentence.
- "Blast them off with a strong spray of water" -- USU jet-of-water clause + 7404.
- "insecticidal soap" -- USU names insecticidal soaps directly for mint.
- "covering leaf undersides" -- 7404 coverage sentence.
- "conserve ladybugs, lacewings, and parasitoid wasps" -- 7404 names lady beetles, lacewings, syrphid fly larvae, tiny parasitic wasps.
- "check new growth often" -- 7404 twice-a-week monitoring sentence.

RECORD CLAIMS WITH NO ANCHOR:
- "**neem oil**" (beginner + seasoned). USU names only "insecticidal soaps, registered insecticides"; UC IPM 7404 speaks of "oils and soaps" generically. I did not surface a sentence in either cited document naming neem for mint. **Not proven absent** -- 7404 has a fuller oil paragraph I did not get transcribed in full -- but as of this pass neem on mint is unverified. Verify or generalize to "a horticultural oil".
- "sometimes with **curled, sticky** foliage" -- the honeydew/stickiness limb. USU carries "curls" but not sticky; 7404 covers honeydew in a passage I did not capture verbatim. Verify.
- "honeydew and the insects themselves **contaminate a crop eaten fresh**" -- no cited document says this about mint. Reasonable, unanchored.
- "**Rinse cut sprigs well before use.**" -- unanchored advice. Harmless, but it is a food-handling instruction with no document behind it.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **Monitoring cadence is published**: "at least twice a week when plants are growing rapidly" (7404). That is a real monitoring rung.
- **A soap/oil safety limit is published and the record omits it**: "Don't apply them to drought-stressed plants or when it is very hot" (7404). Mint is exactly the herb a gardener sprays in a hot dry spell.
- USU's own control list for mint puts **"registered insecticides"** in the same breath as soap; a least-invasive-first ladder should note USU is not ordering these by invasiveness.
- The strong-water-spray rung is doubly anchored (USU *and* 7404) and is the correct rung 1 for a crop eaten fresh.

---

## Spider mites [pests] -- severity <ABSENT>, type <ABSENT>
STATUS: **SOURCED-OK**
ORGANISM: ***Tetranychus urticae*** (twospotted spider mite), per UC IPM
`https://ipm.ucanr.edu/agriculture/peppermint/webspinning-spider-mites/` (ANR Pub 3457). Pest Notes 7405
also names Pacific spider mite and strawberry spider mite as landscape species. The record's phrase
"Twospotted and related spider mites" is therefore correct and now has a document behind the binomial.
ANCHORS:
- `uc_ipm` https://ipm.ucanr.edu/home-and-landscape/mint/ -- verified 2026-09-04
  > Invertebrates: "Spider Mites"
- `ucanr_ext_spider_mites` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html (ANR Pub 7405, rev. 12/2011) -- verified 2026-09-04
  > "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants adjacent to dusty roadways"
  > "Plants under water stress also are highly susceptible"
  > "Spider mites reproduce rapidly in hot weather and commonly become numerous in June through September"
  > "regular, forceful spraying of plants with water often will reduce spider mite numbers adequately"
  > "apply a water spray or mist to the undersides of leaves at least once a day"
  > "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F"
  > "Oils and soaps must contact mites to kill them, so excellent coverage...is essential, and repeat applications may be required"
  > "Spider mites frequently become a problem after applying insecticides"
  > "Check the undersides of leaves for mites, their eggs, and webbing; you'll need a hand lens to identify them"
  > "Be sure mites are present before you treat"
- `uc_ipm` https://ipm.ucanr.edu/agriculture/peppermint/webspinning-spider-mites/ -- verified 2026-09-04
  > "*Tetranychus urticae*"
  > "Feeding damage appears on the upper surface of leaves as silvery or dry spots. Heavy infestations cause leaves to turn bronze in color and drop."
  > "Populations increase quickly during the hot and dry periods between June and August."
  > "*Neoseiulus fallacis*" (the released predatory mite)

RECORD CLAIMS THAT HOLD:
- Stippling / speckling / "dull, sandy, or bronzed" -- UC IPM peppermint page ("silvery or dry spots"; "turn bronze in color and drop").
- Webbing on undersides -- 7405.
- "worst in hot, dry weather", "dusty" -- 7405, both sentences, verbatim.
- "drought stress invites mites" / "keep mint evenly moist" -- 7405 water-stress sentences. This is the record's best line and it is well anchored.
- "not true insects" -- consistent with 7405 (Pest Notes treats mites as distinct from insects).
- Hosing the undersides -- 7405, including the daily cadence.
- Insecticidal soap / miticidal oil to undersides -- 7405 coverage sentence.
- "which UC IPM lists for mint" -- **verbatim true.**
- "conserve predatory mites" -- 7405 natural-enemies sentence; UC IPM names *Neoseiulus fallacis* for mint specifically.

RECORD CLAIMS WITH NO ANCHOR:
- "**minute pirate bugs**" (seasoned, organic_treatment). 7405 names natural enemies generally and UC IPM's mint page names *N. fallacis*; I did not surface a sentence naming minute pirate bugs. Unverified; either anchor it or reduce to "predatory mites".
- "rinse dusty foliage in hot spells" -- 7405 supports washing to remove dust for trees/vines ("Mid-season washing of trees and vines with water to remove dust"); the mint-scale version is an extrapolation. Fine, but note the source is about trees and vines.

RECORD CLAIMS THAT ARE WRONG: none found.

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **The published safety limit on the soft-chemical rung**: "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F" (7405). The record recommends soap/oil in exactly the hot dry conditions where 7405 says not to. **This belongs on the ladder rung, not buried.**
- **Pesticide-induced outbreak** is published: "Spider mites frequently become a problem after applying insecticides"; "Carbaryl, some organophosphates, and some pyrethroids apparently also favor spider mites" (7405). A least-invasive-first ladder should carry this as the reason the conventional rung can backfire.
- **A confirm-before-you-treat rung is published**: "Be sure mites are present before you treat"; "you'll need a hand lens" (7405).
- **A numeric threshold and a biological rung exist** (commercial, so disclose the context): treat at "five mites per leaf or more"; release *N. fallacis* "at 2000 per acre when approximately 20% of sampled leaves have at least 1 spider mite" (UC IPM ANR 3457). Per-acre release rates are not home-garden actionable; the *presence* of a named commercially-available predatory mite for mint is.

---

## Cutworms, mint flea beetles, and root-feeding pests [pests] -- severity <ABSENT>, type <ABSENT>
STATUS: **SOURCED-WEAK** as written (the bundle mixes one sourced limb, one over-named limb, and one
limb sourced nowhere in the record but findable at T1 -- **UNSOURCED-FOUND**).
ORGANISM: umbrella -- three unrelated organisms:
- Cutworms: umbrella, no binomial in any cited document (USU writes only "Cutworm").
- Flea beetle: **USU names only "Flea Beetle", with no species.** The record's "**mint** flea beetles"
  adds a species identity USU does not give. The mint flea beetle is a real animal
  (*Longitarsus waterhousei*) but I found it **only** on non-admitted hosts (pnwpest.org, uspest.org,
  bugwood, and the 403'd pnwhandbooks page); the OSU Extension catalog page that would carry it
  (EM 9299, OR/WA/ID mint IPM strategic plan) returned 403. **No catalog-admitted document names it.**
- Root feeders: ***Fumibotys fumalis*** (mint root borer), per
  `https://ipm.ucanr.edu/agriculture/peppermint/mint-root-borer/`.
ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/mint-in-the-garden -- verified 2026-09-04
  > "Flea Beetle | Small, shiny black beetles that chew tiny holes in leaves. | Control with registered insecticides or cover plants in spring with row covers."
  > "Cutworm | Larvae feed at or below ground and sever stems of seedlings or plants. | Protect individual plants with a collar or trap, use registered insecticides."
- `uc_ipm` https://ipm.ucanr.edu/agriculture/peppermint/mint-root-borer/ (ANR Pub 3457, Tollerup, updated 08/2012) -- verified 2026-09-04
  > "*Fumibotys fumalis*"
  > "Larvae feed on leaves for 2 to 4 days then drop to the soil surface and burrow into a rhizome."
  > "Larvae bore into and feed on rhizomes of peppermint. Economic loss is due to decreased oil yield, reduced quality of oil, and shorter productive expectancy of mint stands."
  > "In October, larvae leave the rhizomes to overwinter in hibernacula just below the surface (2–4 cm below). Larvae pupate in spring."
  > "Adult mint root borers start emerging between early and mid-June, with peak emergence occurring from mid- to late July."
  > "Sample for mint root borer larvae from September through October."
  > "Consider a postharvest treatment if two or more larvae are found per sample."
  > "Parasitic nematodes can be released through irrigation at 2 billion infective juveniles per acre."
  > "Tillage can be effective in late fall or spring when the mint root borer is overwintering or before adults emerge in June. Rotation with a non-host crop is also a possibility."

RECORD CLAIMS THAT HOLD:
- "Young shoots cut off at the soil line" -- USU cutworm row, verbatim in substance ("sever stems of seedlings").
- "notched or shot-holed leaves" -- USU flea beetle row ("chew tiny holes in leaves").
- "cardboard collars on new transplants" -- USU cutworm row ("Protect individual plants with a collar or trap").
- "row cover on new plantings" -- USU flea beetle row ("cover plants in spring with row covers").
- "Utah State lists flea beetles and cutworms among mint's insect pests" -- **verbatim true.**
- "grubs feeding on the roots and rhizomes" / "root and rhizome larvae" -- **TRUE, and now anchorable**, but to `uc_ipm`'s mint root borer page, which the record does not cite.

RECORD CLAIMS WITH NO ANCHOR:
- "**mint** flea beetles" (appears in `name`, `cause_beginner`, `symptoms_seasoned`, `cause_seasoned`).
  The species-level identity is on no admitted document. This is the same defect class the cert log
  fixed once already when it "de-named the 'mint root borer'". **Either de-name to "flea beetles"
  (which is what USU supports and what the roster's `flea-beetles` id means) or find an admitted
  anchor for *Longitarsus waterhousei*.** Per "match the taxon not the common name": on a home mint
  patch the flea beetle a gardener actually sees is more likely a drifting *Epitrix* or *Phyllotreta*
  than the peppermint-field specialist.
- "**root-feeding pests**" as a source-backed category on the *cited* pages -- it is on none of them.
  The cert log de-named the organism but **left the claim standing**, which is a de-naming that did not
  finish. The fix is not to delete it: it is to cite the UC IPM page that carries it.
- "**hose or handpick flea beetles**" -- USU offers only registered insecticides or row cover.
- "**Handpick cutworms at dusk**" -- the dusk timing is on no cited page.
- "dividing and resetting a tired patch in fresh ground breaks root-pest cycles" -- the *idea* is
  anchored for the root borer (UC IPM: "Rotation with a non-host crop is also a possibility"; tillage
  timed to the overwintering stage). The mint-division framing is the record's own.
- "**On a home planting numbers are usually modest.**" -- an unanchored severity judgment. It is
  probably right, but it is doing severity's job in prose.

RECORD CLAIMS THAT ARE WRONG: none outright false; the defect is over-specificity and mis-citation,
not falsity.

**RECOMMENDATION: SPLIT THIS BUNDLE INTO THREE.** These three organisms share no ladder rung. The
roster already carries `cutworms` (9 crops) and `flea-beetles` (34 crops) as shared ids -- keeping mint's
three organisms fused denies both joins and forces a fourth, mint-only id that duplicates 43 existing
records. Proposed: `cutworms`, `flea-beetles`, `mint-root-borer`.

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **Mint root borer phenology is fully published** and is the whole basis of a cultural ladder:
  larvae in rhizomes through the season, leave rhizomes in **October** to overwinter 2-4 cm below the
  surface, pupate in spring, adults emerge **early-to-mid June** with peak **mid-to-late July**, one
  generation a year. That gives a gardener two exact windows (late fall / pre-June) for the physical rung.
- **A biological rung is published for the root borer**: parasitic (entomopathogenic) nematodes,
  applied through irrigation. Note the catalog already admits `pnw_handbook_epn`
  (PNW Handbooks -- Entomopathogenic Nematodes) which is the home-scale companion for that rung.
- **Tillage timing is published**: "late fall or spring when the mint root borer is overwintering or
  before adults emerge in June."
- **A monitoring method with a threshold exists** ("Sample ... from September through October";
  "two or more larvae ... per sample"), commercially scaled but conceptually usable.
- USU's flea beetle rung is **row cover in spring**, a genuine physical rung the record softens into
  "row cover on new plantings".

---

## 4. DISEASES

---

## Mint rust [diseases] -- severity <ABSENT>, type <ABSENT>
STATUS: **SOURCED-WEAK** as cited (the two cited documents establish that rust is a mint disease and
describe it, but carry **none** of the three load-bearing claims the task asked about) --> upgrades to
**SOURCED-OK** if the two catalog-admitted anchors I found are added.
ORGANISM: ***Puccinia menthae***, per `rhs` https://www.rhs.org.uk/disease/mint-rust and per
`wsu_ext` Johnson, "Management of Rust on Mint". **Neither cited document names it.**

ANCHORS -- what the CITED documents actually say:

- `ncsu_ext` https://plants.ces.ncsu.edu/plants/mentha-spicata/ -- verified 2026-09-04.
  The **entire** "Insects, Diseases, and Other Plant Problems" field is three sentences:
  > "Fungal diseases are common diseases in spearmint. Two main diseases are rust and leaf spot. The plant spreads aggressively."

  I ran a second, differently-worded fetch specifically to guard against a truncated parse ("a clean
  zero can be your own parser"). Result on the second read: the page does **not** contain the words
  *Puccinia*, *anthracnose*, *powdery mildew*, *verticillium*, *aphid* or *spider mite* anywhere; its
  only use of "rhizome" is about the plant spreading ("it also spreads by rhizomes", "Soil barriers can
  restrain rhizomatous spread"), not about a pathogen.

  **Answering the task question directly: YES, NC State's mentha-spicata page lists rust among mint
  diseases -- and NO, it does not name *Puccinia menthae*.** The record's parenthetical "(NC State lists
  rust among the main mint diseases)" is exactly, verbatim, correct. The record's placement of
  "*Puccinia menthae*" in the same sentence as that credit is not.

- `usu_ext` https://extension.usu.edu/yardandgarden/research/mint-in-the-garden -- verified 2026-09-04.
  > "Mint Rust | Small whitish, slightly raised spots that turn reddish orange or brown on underside of leaves. | Avoid wet leaves overnight. Use drip irrigation or apply overhead water before mid-day."

  and, from the section preamble:
  > "Most diseases can be minimized or eliminated by appropriate watering and ensuring proper sunlight to plants. Consider drip irrigation as an excellent method to provide regular water and keep foliage dry. As the mint grows and multiplies, thinning or dividing may be essential to maintain healthy plants."

  **Answering the task question directly: NO. USU's mint-in-the-garden page does NOT carry the
  rhizome-overwintering claim.** I asked for it three ways. The page's only "hard to get rid of"
  sentence is about the plant, not the fungus: "Once established it is very hard to eradicate", which
  sits under Aggressive Growth. The page contains no mention of rhizome or root survival by any pathogen.

ANCHORS -- catalog-admitted documents that DO carry the missing claims:

- `rhs` https://www.rhs.org.uk/disease/mint-rust -- verified 2026-09-04
  > "*Puccinia menthae*"
  > "*Puccinia menthae* completes its entire life cycle on one plant host and produces resting spores to pass through winter."
  > "In garden mint, the general consensus was that the fungus grows into the rhizomes, where it spends the winter"
  > "It is known that resting spores present in the soil or contaminating the outside of the rhizomes can infect new shoots in spring."
  > "Mint rust infects several mint species as well as some related plants including marjoram and savory."
  > "Plants affected - Garden mints, marjoram and savory"
  > "Pale and distorted shoots in spring"
  > "Dusty orange pustules on the stems and leaves. These may be followed by dusty yellow or black pustules"
  > "Large areas of leaf tissue die and plants may lose leaves"
  > "Remove affected plants promptly before the black resting spores are formed and contaminate the soil."
  > "No fungicides with activity against mint rust are available for use on mint or other herbs that will be used for culinary purposes."

- `wsu_ext` https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/MintrustA.doc -- Johnson, D. A., Plant
  Pathologist, Washington State University. Read in full from the file bytes. Verified 2026-09-04.
  > "Mint rust, caused by the fungus *Puccinia menthae*, infects Scotch spearmint and Native spearmint in central Washington."
  > "Rust is first seen in early spring and appears as compact series of light-yellow blister-like pustules, called aecia, on plant stems and leafstalks."
  > "Early spring infections are systemic in spearmint and infected plants are twisted and distorted, and stems easily break."
  > "Rust spreads by air-borne spores from aecia during late spring to nearby plants and produce golden to cinnamon brown pustules, called (uredinia) on stems the undersides of leaves."
  > "the disease is recycled every 8 to 10 days when favored by moisture on foliage from rain, dew or sprinkler irrigation."
  > "When these pustules become numerous, the infected leave curl, turn yellow and then brown, and drop from plants."
  > "In late summer and fall, pustules on mint stubble and foliage become dark chocolate brown. This is the overwintering stage (telia) of the rust fungus and is the source of new infections the following spring."
  > "Rust from escaped mint and non-cultivated mint can also be a source of rust infection in the spring."
  > "Wet, cloudy weather and prolong leaf wetness from irrigation, dew, and rainfall favor rust development."
  > "Defoliation and a reduction in essential oil content of mint plants results from severe rust infection."
  > "Such rust outbreaks are usually initiated from systemic infections and pustules on rhizomes and stem cuttings used in propagation."
  > "Rust on rhizomes can be eliminated by immersing rhizomes in water at 113 F (34 C) for 10 minutes before planting."
  > "Source materials should be inspected and be rust-free before propagating stem cuttings."
  > "Monitor stem cuttings closely for rust and discard infected plants promptly."

RECORD CLAIMS THAT HOLD:
- "orange, yellow, or rust-brown ... pustules on the undersides of the leaves **and on the stems**" -- RHS ("Dusty orange pustules on the stems and leaves") and WSU ("uredinia) on stems the undersides of leaves"). Note the *stems* limb is anchored only in RHS/WSU; USU says undersides only.
- "orange to brown powdery pustules on leaf undersides, stems, and petioles" -- WSU ("on plant stems and leafstalks").
- "Badly affected leaves curl, brown, and drop" / "defoliation in a bad year" -- WSU verbatim; RHS "Large areas of leaf tissue die and plants may lose leaves".
- "(NC State lists rust among the main mint diseases)" -- **verbatim true**, NCSU.
- "warm humid crowding drives it" / "avoid wetting the foliage" -- USU ("Avoid wet leaves overnight"), WSU ("Wet, cloudy weather and prolong leaf wetness ... favor rust development").
- "water at the soil line" -- USU ("Use drip irrigation ... keep foliage dry").
- "thin and space plants for airflow" -- USU ("thinning or dividing may be essential to maintain healthy plants") plus the drip/dry-foliage sentence.
- "start a fresh planting from clean, rust-free cuttings" / "propagate only from rust-free plants" -- **strongly anchored** by WSU ("Source materials should be inspected and be rust-free before propagating stem cuttings"; "Monitor stem cuttings closely for rust and discard infected plants promptly").
- "**There is no reliable home cure once it is established.**" -- **ANCHORED, once you use RHS**:
  "No fungicides with activity against mint rust are available for use on mint or other herbs that will
  be used for culinary purposes." That is the precise, defensible form of the claim, and it is *stronger*
  than the record's phrasing because it says *why*. **Recommend rewording to track RHS.** As written
  ("no reliable home cure") it is currently anchored to nothing the record cites.

RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):
- "***Puccinia menthae***, the classic mint rust" and "The rust fungus *Puccinia menthae*" -- true, but
  **on neither cited document.** Anchor to `rhs` and/or `wsu_ext`, or drop the binomial.
- "**It overwinters in the rhizomes, so an infected patch reinfects itself**" (seasoned) and "**lives over
  on the roots and rhizomes from year to year**" (beginner) -- **NOT on either cited page.** The claim is
  *partly* supportable and needs rewriting rather than deleting, because the two admitted documents that
  address it **do not agree**:
  - RHS supports it but **hedges**: "the general consensus **was** that the fungus grows into the
    rhizomes, where it spends the winter" -- past tense, reported as consensus, and RHS immediately
    distinguishes what is *known*: "resting spores present in the soil **or contaminating the outside of
    the rhizomes** can infect new shoots in spring."
  - WSU **locates overwintering elsewhere**: "pustules on mint **stubble and foliage** become dark
    chocolate brown. This is the overwintering stage (telia) ... and is the source of new infections the
    following spring", plus escaped/wild mint as a second reservoir. WSU brings rhizomes in only for
    *propagation* ("systemic infections and pustules on rhizomes and stem cuttings used in propagation")
    and treats the rhizome contamination as **removable** by hot water.
  **This matters for the ladder.** The record's flat "it overwinters in the rhizomes" is the reason the
  record advises "start over in a new spot", i.e. the most invasive cultural rung. WSU's account supports
  a *much* cheaper rung first: **clear the stubble and fallen leaves in fall**, and take clean cuttings.
  Recommended rewrite: "It carries over on last year's stubble and fallen leaves, and on the rhizomes and
  cuttings you propagate from, so an untended patch reinfects itself each spring" -- which both documents
  support, and which unlocks the correct least-invasive rung.
- "**rusty leaves are not good to eat**" (beginner, symptoms) -- **NO CATALOG-ADMITTED ANCHOR.** This is
  the consumption/safety-adjacent claim the task flagged, and it is the weakest sentence in the record.
  - RHS: I asked directly; the page **contains no statement about eating affected leaves.**
  - USU, NCSU, UC IPM, WSU: nothing on edibility of rusted foliage.
  - The only extension-branded text I found is an **Ask Extension** answer (Hennepin County, Minnesota;
    asked 2019-08-21, answered 2019-08-22), https://ask.extension.org/kb/faq.php?id=590968:
    > Q: "I have rust on my mint plant. Can I still dry it to make tea? Is there a way to get rid of the rust and still keep the plant safe to harvest for tea?"
    > A: "mint leaves with rust should not be eaten. This would imply that such leaves should not be used to make tea."
    > A: "a plant showing rust on its leaves should be cut back to soil level and not used."
    > A: "Once a plant is infected with rust, it cannot be removed."
  - **`ask.extension.org` is not in `source_catalog_admission.txt`.** The catalog admits one scoped
    extension.org key (`ext_org_apples`, apples.extension.org) but no general Ask Extension key. It is
    also a single volunteer/Master Gardener response, not a peer-reviewed fact sheet -- a weaker artifact
    than anything else cited on this crop.
  - **RECOMMENDATION: soften.** Two safe rewrites, both fully anchored: (i) drop the edibility framing and
    keep RHS's action -- "remove affected leaves promptly, before the dark resting spores form"; or
    (ii) state the practical truth -- "there is no fungicide cleared for rust on herbs you are going to
    eat, so the answer is to cut the affected growth out" (RHS, verbatim-backed). Do **not** ship a
    do-not-eat absolute on a single un-admitted Q&A answer. If Trevor wants the do-not-eat line kept, it
    becomes a **catalog-addition decision** on `ask.extension.org`, not a silent anchor.
- "pale spots on the **upper surface**" -- closest admitted text is RHS "Pale and distorted shoots in
  spring", which is about shoots, not upper leaf surfaces. Unverified; soften or drop.
- "cut a badly infected patch to the ground" / "mow or cut a heavily infected patch to the ground and
  clear the debris" -- **not** on the cited pages for rust. USU carries "prune healthy plants to the
  ground in fall" but as the **anthracnose** control, not rust. RHS says "Remove affected plants
  promptly". Re-cite, or move the cut-to-ground rung to anthracnose where USU actually puts it.

RECORD CLAIMS THAT ARE WRONG:
- Nothing is flatly false, but one is **misleadingly implied**: "*Puccinia menthae*, the classic mint
  rust: ... (NC State lists rust among the main mint diseases)". Read normally, that sentence credits the
  binomial to NC State. NC State does not publish it. **This is a mis-pointed key of the exact kind the
  batch-24 source-truth pass was created to catch.**

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **A hot-water physical rung is published**: "Rust on rhizomes can be eliminated by immersing rhizomes in
  water at 113 F (34 C) for 10 minutes before planting" (WSU). Renders as **113°F**. This is a genuine,
  home-doable, non-chemical rung that sits *below* "start over somewhere else" on the invasiveness scale,
  and the record's ladder currently has nothing between "pick off leaves" and "abandon the patch".
- **The disease has a published recycle interval**: "recycled every 8 to 10 days when favored by moisture
  on foliage" (WSU). That sets the scouting cadence.
- **There is a distinct, recognizable early-spring stage**: systemic infection producing plants that are
  "twisted and distorted, and stems easily break", with yellow blister-like **aecia** on stems and
  leafstalks, arising from sparse but high-value early sources of inoculum (WSU). Rogueing *those few
  plants* in early spring is the highest-leverage rung on this crop and the record does not mention it.
- **A second reservoir exists outside the patch**: "Rust from escaped mint and non-cultivated mint can
  also be a source" (WSU). Mint escapes constantly, which makes this unusually relevant for a home garden.
- **RHS gives a timing constraint on removal**: "Remove affected plants promptly **before the black
  resting spores are formed** and contaminate the soil."
- **RHS names the host range**, and it is wider than mint: "several mint species as well as some related
  plants including **marjoram and savory**". See §4f.
- **The chemical rung is closed for this crop by label, not by efficacy** (RHS). Note for the conventional
  disclosure: WSU names Rally 40W, Headline and Amistar, but that is a **commercial mint-oil crop**
  document with 7- to 30-day preharvest intervals; none of that transfers to a home herb pot, and the
  ladder must say so rather than reproducing it.

---

## §4f CROSS-CHECK (mint vs oregano rust)

**The question:** is there evidence that *Puccinia menthae* races are host-specialized such that the mint
race does not infect oregano and vice versa -- and are `mint-rust` and `oregano-rust` correctly two ids,
or one problem wearing two names?

### (a) Can the specialization claim be anchored in a catalog-admitted T1 source? **No.**

I checked every plausible admitted route: `rhs`, `usu_ext`, `ncsu_ext`, `uc_ipm` (both the home-and-landscape
mint page and the whole `agriculture/peppermint` section), `wsu_ext`, and attempted `osu_ext` and
`uiuc_ext`/`illinois_ext`. **No admitted document states the mint/oregano cross-inoculation result.**

Worse for the record: the one admitted source that speaks to host range at all says something close to the
**opposite** at species level. `rhs`, https://www.rhs.org.uk/disease/mint-rust, verified 2026-09-04:

> "Mint rust infects several mint species as well as some related plants including **marjoram and savory**."
> "Plants affected - Garden mints, **marjoram** and savory"

Marjoram is *Origanum majorana* -- an **Origanum**. So the only catalog-admitted document on this question
puts *P. menthae* on the oregano genus and draws **no race distinction whatsoever**.

**What CAN be anchored at T1 in the catalog is the principle**, from `wsu_ext`, Johnson, "Management of
Rust on Mint", verified 2026-09-04:

> "Two principal types of races of *P. menthae* have been recognized. One type infects Native spearmint but not peppermint and is called native spearmint rust; the other, peppermint rust, infects peppermint but not Native spearmint."
> "Both groups of races infect Scotch spearmint, but native spearmint rust is more aggressive on Scotch spearmint than is peppermint rust."

That is a T1 extension document establishing that *P. menthae* is a **race-structured, host-specialized
pathogen whose races fail to cross even between two species of Mentha**. It does not mention Origanum. It
makes the mint/oregano result *plausible and consistent*, but it does not *state* it.

### (b) The mint/oregano result itself: **JOURNAL-ONLY**, and read only at abstract level

Full citations, all confirmed against Crossref metadata (2026-09-04):

1. **Stiles, C. M., and Rayside, P. A. 2006.** "Host Range of Rust Isolates on Oregano and Mint in Florida."
   *Plant Health Progress* **7**(1), article 21. DOI **10.1094/PHP-2006-0417-01-RS**. Publisher: Scientific
   Societies (APS). This is the Florida cross-inoculation study. Reported result: two distinct
   *P. menthae* populations, one infecting oregano / sweet marjoram / Greek oregano, one infecting spearmint
   only; the oregano isolate infected no *Mentha* sp., and the mint isolate infected neither peppermint nor
   any *Origanum*. "This is the first report of *P. menthae* on oregano in Florida."
2. **Koike, S. T., Subbarao, K. V., Roelfs, A. P., Hennen, J. F., and Tjosvold, S. A. 1998.** "Rust Disease
   of Oregano and Sweet Marjoram in California." *Plant Disease* **82**(10):1172. DOI
   **10.1094/PDIS.1998.82.10.1172C**. This is the California study; *P. menthae* on commercial
   *Origanum vulgare* and *Origanum majorana* in coastal California, 1996-1997.
3. **Johnson, D. A. 1995.** "Races of *Puccinia menthae* in the Pacific Northwest and Interaction of Latent
   Period of Mints Infected with Rust Races." *Plant Disease* **79**(1):20. DOI **10.1094/PD-79-0020**.
   Eleven races from 17 collections over 5 years. (Same author as the WSU extension document above, which
   is that paper's extension form -- which is why the WSU doc is usable and the paper is not needed.)
4. **Solano-Báez, A. R., Beltrán-Peña, H., Victoria-Arellano, A. D., Tovar-Pedraza, J. M.,
   Flores-Moctezuma, H. E., and Márquez-Licona, G. 2026.** "First Report of *Puccinia menthae* Causing Leaf
   Rust on Oregano (*Origanum vulgare*) in Mexico." *Plant Disease* **110**(2):538. DOI
   **10.1094/PDIS-07-25-1423-PDN**.

**Honesty flag, and it is important.** `apsjournals.apsnet.org` returned **HTTP 403 on every attempt**. I
have the bibliographic metadata from Crossref (which I did read directly), but the *host-range sentences*
above come from **search-engine renderings of those abstracts, not from a document I opened**. Under brief
rule 2 that is not a read. **I am reporting the specialization result as a strong, converging lead from
four independent journal records, not as something I verified in the source.** Anyone acting on it should
open the APS full texts.

### (c) VERDICT: **TWO ids is correct.** They are one pathogen species wearing two host-race names.

**Two ids, on three grounds:**

1. **Roster precedent, computed from canonical.** The dataset already gives one rust pathogen distinct
   per-host ids **across host genera**: `garlic-rust`, `chives-rust` and `leek-rust` are three separate ids
   for *Puccinia* rust on three *Allium* crops (leek's record even names *P. porri*, "formerly *P. allii*").
   `bee-balm-rust` is a fourth host-named Lamiaceae rust id. Shared rust ids appear only **within a single
   host genus**: `common-rust` across the four *Zea* crops, `orange-rust` across raspberry and blackberry
   (*Rubus*). *Mentha* and *Origanum* are different genera, so precedent puts them in the "separate id" class.
   **Counter-example, disclosed:** `white-rust` is shared across spinach and three brassicas even though
   spinach's record names *Albugo occidentalis* and the brassicas' name *Albugo candida* -- that is one id
   spanning **two different pathogen species**. That is a pre-existing latent id defect in canonical, not a
   precedent to copy, and it is worth its own finding.
2. **The id is a join key and management differs.** A problem `id` is what `varieties[].resistance` and
   `varieties[].ladder_delta` point at. If the races do not cross -- which the WSU document establishes
   *within* Mentha at T1, and the four journal records extend to Origanum -- then a gardener's oregano is
   **not** an inoculum source for their mint and vice versa. Fusing the ids would license a shared
   "remove nearby infected hosts" rung that is wrong in both directions, and would make any future
   resistance grade on a mint cultivar silently apply to oregano.
3. **The two records anchor to disjoint document sets.** `mint-rust` anchors to USU / NCSU / RHS / WSU, all
   mint documents. Oregano's `Rust` currently anchors to **nothing** (`sources: null`), and oregano's own
   cert log records that this entry was deliberately pulled apart from mint's:
   > "renamed 'Mint rust'->'Rust' and dropped the mint-family over-specificity"
   Re-fusing them would undo a ruled cert decision.

**The caveat the ladder must respect.** They are **one pathogen species**, *Puccinia menthae*. Nothing may
say or imply that oregano rust is a different fungus -- that is false, and `rhs` (the only admitted source
on host range) explicitly puts marjoram in *P. menthae*'s host list. The accurate framing is *"the same rust
species, in host-specialized strains"*, and even that is currently journal-only for the mint/oregano pair.
**Recommendation: neither record's consumer prose should assert anything about cross-infection between mint
and oregano until a catalog-admitted source carries it.** Keep two ids for the join and ladder reasons
above; keep the prose silent on the cross-host question; and **register the pair in
`tools/problem_id_registry.json` under `deliberately_distinct`** (it is not there today -- I checked; the
registry currently holds no mint, oregano, marjoram or Lamiaceae entries, and its only rust entry is
`white-rust`) so the PLA-449 collision guard does not later flag `mint-rust` / `oregano-rust` as a
near-duplicate pair, and so the reason survives the decision.

Also note, for the oregano reviewer: **`rhs`'s mint-rust page is a live, catalog-admitted T1 anchor for
oregano's currently-unsourced `Rust` entry**, via the marjoram/savory host-range sentence -- with the
caveat that RHS is describing *Origanum majorana*, not *O. vulgare*, and the "sibling-pathed is a lead, not
a verdict" rule applies.

---

## Verticillium wilt [diseases] -- severity <ABSENT>, type <ABSENT>
STATUS: **SOURCED-WEAK**, with one **WRONG** attribution live in the prose.
ORGANISM: ***Verticillium dahliae***, per `uc_ipm`
https://ipm.ucanr.edu/agriculture/peppermint/verticillium-wilt/. The cited document (USU) gives no binomial;
the record's hedge "a soilborne *Verticillium*" is therefore honest as written, and can now be sharpened.
ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/mint-in-the-garden -- verified 2026-09-04
  > "Verticillium Wilt | Leaf yellowing starting at the margin and they eventually curl up and die. | Rotate planting areas, remove infected plants, and do not over fertilize plants."
- `uc_ipm` https://ipm.ucanr.edu/agriculture/peppermint/verticillium-wilt/ (UC IPM Pest Management Guidelines: Peppermint, UC ANR Publication 3457; D.B. Marcum, R.M. Davis; text updated 09/13) -- verified 2026-09-04
  > "*Verticillium dahliae*"
  > "The fungus survives between crops and through winter as hardened fungal bodies called microsclerotia, which are pinhead size and barely visible."
  > "Rotation to crops that do not encourage reproduction of *V. dahliae* for a minimum of five years"
  > avoid: "mint, potatoes, or strawberry"; avoid: "potato and red clover"
  > acceptable: "grass hays (orchardgrass, fescue, or timothy), corn, sudangrass, alfalfa, cereals, onions, and garlic"
  > use "only rootstock certified to be free of *V. dahliae*"
  > "Minimize cultivation to avoid spreading microsclerotia"
  > "cleaning all equipment and vehicles entering mint fields and cleaning shoes"
  > "Regularly inspect all fields"
- `ncsu_ext` https://plants.ces.ncsu.edu/plants/mentha-spicata/ -- verified 2026-09-04: the word
  *verticillium* **does not appear**. (Consistent with the cert log, which already dropped `ncsu_ext` from
  this entry. Re-verified rather than assumed.)

RECORD CLAIMS THAT HOLD:
- "lower leaves yellow and wilt" / "Leaf yellowing" -- USU, verbatim in substance.
- "soil-borne fungus that clogs the plant's water-conducting tissue" -- standard and consistent with UC IPM's *V. dahliae* framing.
- "**it builds up in the ground**" / "persists in soil for years" -- UC IPM microsclerotia sentence + the five-year rotation minimum. **Strongly anchored, at the UC IPM URL the record does not cite.**
- "**there is no cure for an infected plant, so remove it**" / "no spray cure" -- consistent with both: USU's control is rotate + remove + don't over-fertilize; UC IPM's management list is entirely cultural (certified rootstock, sanitation, minimized cultivation, rotation, resistant selections, fall flaming). **Neither document offers any chemical control**, which is the honest form of the claim.
- "move the patch to fresh ground every few years" / "rotate the mint bed on a multi-year cycle" -- USU ("Rotate planting areas") + UC IPM's five-year minimum.
- "propagate disease-free cuttings" / "Plant clean stock" -- UC IPM ("only rootstock certified to be free of *V. dahliae*").
- "do not follow ... **potatoes** ... or **strawberries**" -- UC IPM names exactly these: "Do not rotate to mint, potatoes, or strawberry."

RECORD CLAIMS THAT ARE WRONG:
- "**The Connecticut Experiment Station and Utah State both flag it for mint.**" (`symptoms_seasoned`).
  The Connecticut Agricultural Experiment Station is **not in the source catalog**, is not cited in
  `sources` or `anchoring_urls`, and mint's own cert log says this credit class was struck on 2026-07-06
  ("struck the unanchored '(Connecticut Experiment Station and University of Illinois)' credits from the
  rust + powdery-mildew entries"). It was missed here. **This is a live fabricated-attribution defect and
  must be struck.** The Utah State half is true and should be kept: USU does list Verticillium Wilt for mint.

RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):
- "do not follow **tomatoes**" (beginner) / "avoid ground that grew **tomatoes**, potatoes, **eggplant**, or
  strawberries" (seasoned). **UC IPM's mint rotation guidance names mint, potatoes, strawberry and red
  clover -- it does not name tomato or eggplant.** They are certainly *V. dahliae* hosts in general, but no
  document cited by or found for **mint** says to avoid following them. Either anchor to a general
  *V. dahliae* host-range document (`ncsu_ext` publishes "Verticillium Wilt of Tomato and Eggplant" at
  content.ces.ncsu.edu, which I did **not** open in this pass) or trim to the three UC IPM names.
- "**often on just one side of a stem**" (beginner) and "**one-sided branch development**" (seasoned) --
  on neither USU nor the UC IPM peppermint page. The UC IPM peppermint page's symptom text is thin
  ("wilting and plant death"). One-sidedness is a real and well-known *Verticillium* sign, but I could not
  anchor it for mint in an admitted document; the sources that carry it in detail are the 403'd OSU
  Extension verticillium page and the 403'd PNW handbook. **Not proven absent -- unverified.**
- "**slow, bronze-cast spring growth**" -- same status: unanchored in this pass, findable in the unreachable
  documents.
- "**stunted, off-color plants**" and "whole shoots or plants dying back in warm weather" -- partially
  covered by USU's yellow/curl/die sentence; the warm-weather timing is unanchored.
- "**It does not wash off**" -- rhetorical, unanchored, harmless.
- "the disease that most limits mint's longevity" / "shortens the life of a mint patch" -- a strong claim
  with no document behind it on the cited pages. UC IPM's root-borer page independently uses "shorter
  productive expectancy of mint stands" for a *different* pest, so the superlative is doing unearned work.
  Soften to "one of the diseases that shortens the life of a mint patch", or anchor it.
- "infects many crops (tomato, potato, strawberry, other mints)" -- see above; potato/strawberry/mint yes, tomato unanchored here.

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **A published non-host rotation list**: "grass hays (orchardgrass, fescue, or timothy), corn, sudangrass,
  alfalfa, cereals, **onions, and garlic**" (UC IPM). The record tells a gardener what *not* to plant and
  never what they *can*. Onions, garlic and corn are all home-garden crops -- this converts a dead-end
  warning into an actionable cultural rung.
- **The five-year figure**: "a minimum of five years" (UC IPM). The record says "every few years", which is
  materially shorter than the published minimum and is the kind of soft-number drift that makes advice wrong.
- **The survival structure has a name and a size**: microsclerotia, "pinhead size and barely visible" (UC IPM)
  -- and the reason cultivation spreads it ("Minimize cultivation to avoid spreading microsclerotia"). That
  is a physical-rung fact: do not rototill through an infected patch.
- **Sanitation on tools and shoes** is published: "cleaning all equipment and vehicles entering mint fields
  and cleaning shoes" (UC IPM). The shoe clause scales down to a home garden exactly.
- **USU adds a fertility rung the record drops**: "**do not over fertilize plants**".
- **Resistant/tolerant selections exist**: UC IPM names "Murray or Todds" in place of Black Mitcham in
  infested fields. **Disclose the limit**: these are commercial peppermint clones, not garden-centre plants,
  so this is a "resistance exists in the crop" note, not a buy-this recommendation.
- UC IPM's "annual fall burning (flaming)" is a commercial mint-field practice and should **not** be carried
  onto a home ladder.

---

## Powdery mildew and anthracnose (leaf spot) [diseases] -- severity <ABSENT>, type <ABSENT>
STATUS: **WRONG (as a bundle).** Split into two. Limb by limb:
- **anthracnose limb: SOURCED-OK** to `usu_ext`.
- **powdery mildew limb: SOURCED-WEAK / mis-attributed.** `usu_ext` does **not** mention powdery mildew at
  all, and the `uc_ipm` anchor is a *link*, not a supporting document. A real T1 mint-specific anchor exists
  and is not cited (`wsu_ext`) -- so **UNSOURCED-FOUND** for that limb.
ORGANISM: two unrelated fungi.
- Anthracnose on mint: no binomial in any admitted document I read. USU writes only "Anthracnose". (The
  literature name is *Sphaceloma menthae*; I found it **only** on non-admitted hosts and did **not** confirm
  it in an admitted document -- do not put it in the record on my say-so.)
- Powdery mildew on mint: per `wsu_ext`, "A name commonly applied to powdery mildew on mint is
  ***Erysiphe cichoracearum***" -- and that same document warns the name is unsettled (the species has been
  split into 20+, and "several species of powdery mildews attack members of the mint family (Lamiaceae) in
  the Pacific Northwest", at least two previously unknown to science). **Do not hard-name the mint powdery
  mildew fungus in the record.**
ANCHORS:
- `usu_ext` https://extension.usu.edu/yardandgarden/research/mint-in-the-garden -- verified 2026-09-04
  > "Anthracnose | Small water soaked spots on leaves and stems. | Rotate planting areas, remove diseased plants, and prune healthy plants to the ground in fall."
  > "Most diseases can be minimized or eliminated by appropriate watering and ensuring proper sunlight to plants. Consider drip irrigation as an excellent method to provide regular water and keep foliage dry."
  > The page contains **no mention of powdery mildew.** (Asked directly, twice.)
- `uc_ipm` https://ipm.ucanr.edu/home-and-landscape/mint/ -- verified 2026-09-04
  > Plant Diseases: "Powdery Mildew on Vegetables" -- **the only disease listed for mint**, and it is a link out.
- `uc_ipm` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html (Pest Notes: Powdery Mildew on Vegetables, ANR Pub 7406, updated 11/2008) -- verified 2026-09-04
  > hosts covered: "artichoke, beans, beets, carrot, cucumber, eggplant, lettuce, melons, parsnips, peas, peppers, pumpkins, radicchio, radishes, squash, tomatillo, tomatoes, and turnips" -- **mint is not in the list, and no herb is.**
  > "Moderate temperatures (60° to 80°F) and shady conditions generally are the most favorable for powdery mildew development."
  > "Unlike many diseases, powdery mildew doesn't require moist conditions to grow"
  > "Spores of some powdery mildew fungi are killed and germination is inhibited by water on plant surfaces for extended periods."
  > "**Overhead sprinkling may help reduce powdery mildew because spores are washed off the plant.**"
  > "sulfur products have been used to manage powdery mildew for centuries but are only effective when applied before disease symptoms appear."
  > "use a horticultural oil...or one of the plant-based oils such as neem oil or jojoba oil...to eradicate mild to moderate powdery mildew infections."
- `wsu_ext` https://s3.wp.wsu.edu/uploads/sites/2195/2014/06/PowderyMildewMint.doc -- Johnson, D. A., Plant Pathologist, WSU, Pullman WA. Verified 2026-09-04
  > "Powdery mildew appears on mint leaves, stems, and petioles as a powdery, white to gray coating of fungal mycelium and spores."
  > "Infections consist of discrete circular colonies of up to ½ inch in diameter and can become numerous, coalesce and spread over the entire plant."
  > "Colonies turn gray with age." / "Leaves may turn yellow and drop with severe infections."
  > "Scotch spearmint can be severely damaged while peppermint and native spearmint are usually not seriously affected."
  > "The disease is most severe on young, succulent plants such as those resulting from heavy nitrogen fertilization and irrigation."
  > "Powdery mildew is often severe on mint grown in the greenhouse due to humid, shady conditions."
  > "Overwinter of the powdery mildews that infect mint are thought to be infected mint plants, stubble and wild hosts of the mint family."
  > "**Powdery mildew is generally not a problem in mint irrigated with overhead sprinklers from a center pivot system.**"
  > "**when the overhead sprinkler irrigation is ceased for more than a few days, powdery mildew can increase very rapidly due to the humidity in the plant canopy.**"
  > "Timing of application is very important because once powdery mildew becomes established it is very hard to control."
  > "Initial applications of sulfur are usually made when plants are 4 to 6 inches tall."
  > "Sulfur should not be applied if temperatures will exceed 90F within 3 days after application."
- `ncsu_ext` https://plants.ces.ncsu.edu/plants/mentha-spicata/ -- verified 2026-09-04: the words
  *anthracnose* and *powdery mildew* **do not appear**. NCSU says only "Two main diseases are rust and
  **leaf spot**."

### THE FINDING THAT MATTERS: the two halves of this bundle need OPPOSITE moisture management

The record's shared advice is "water at the soil line to keep the leaves dry", "keep the foliage dry",
"avoid overhead watering". That is correct for anthracnose and rust. **It is wrong for powdery mildew**, and
both admitted documents say so in plain words:

- UC IPM 7406: "Unlike many diseases, powdery mildew doesn't require moist conditions to grow"; "Spores of
  some powdery mildew fungi are killed and germination is inhibited by water on plant surfaces for extended
  periods"; "**Overhead sprinkling may help reduce powdery mildew because spores are washed off the plant.**"
- WSU: "Powdery mildew is **generally not a problem** in mint irrigated with overhead sprinklers"; stopping
  overhead irrigation for a few days makes it "increase very rapidly".

Bundling these two problems into one record forces one prevention string, and the string currently shipped
tells a gardener to do the thing that **favors** the powdery mildew half. This is the same defect class as
the PLA-8 conventional-disclosure arc (wrong advice on live rungs), and it is not fixable inside the bundle
-- the bundle *is* the defect.

### On the task's "already exists as separate ids" question

- **The sources treat these as SEVERAL problems, not one.** No single document lists them together: USU
  carries anthracnose and **not** powdery mildew; UC IPM carries powdery mildew and **not** anthracnose;
  NCSU carries neither by name. There is no document anywhere that treats them as one mint problem.
- **Management differs, and in the moisture dimension it is directly contradictory** (above). It also
  differs in cultivar susceptibility (WSU: powdery mildew is a Scotch-spearmint problem, peppermint and
  native spearmint "usually not seriously affected"), in the fertility driver (powdery mildew worse under
  heavy nitrogen), in siting (powdery mildew worse in shade and greenhouses; anthracnose worse in prolonged
  leaf wetness), and in the soft-chemical rung (sulfur/oil work on powdery mildew; USU offers no spray at all
  for anthracnose, only rotate/remove/cut to the ground in fall).
- **RECOMMENDATION: split, and reuse the existing shared ids** -- `powdery-mildew` (already on 32 crops,
  100% typed `fungal`) and `anthracnose` (already on 14 crops, 19/21 typed `fungal`). A fused mint-only id
  would be a third id duplicating both, and would join to neither. Re-cite on split: `powdery-mildew` ->
  `uc_ipm` (mint page listing) + `wsu_ext` (the mint-specific document); `anthracnose` -> `usu_ext`.

RECORD CLAIMS THAT HOLD:
- "white, powdery dust on the leaves and stems" -- WSU, verbatim in substance ("powdery, white to gray coating ... on mint leaves, stems, and petioles").
- "white powdery patches that brown and shrivel heavy foliage" -- WSU ("Leaves may turn yellow and drop with severe infections"); "brown and shrivel" is a stretch on "yellow and drop".
- "listed for mint by UC IPM" (powdery mildew) -- **true as a listing**: UC IPM's mint page does list it. See the wrongness note below for what that listing does and does not establish.
- "dark sunken spots and blotches on leaves and stems" (anthracnose) -- USU ("Small water soaked spots on leaves and stems"); "sunken" and "blotches" are the record's additions.
- "Utah State ... list[s] leaf-spotting fungi for mint" -- true (USU: Anthracnose).
- "spread in crowded, humid plantings and on wet foliage, worse where air does not move" -- true of anthracnose (USU's drip/dry-foliage preamble) and of powdery mildew's shade/greenhouse driver (UC IPM 7406, WSU), though not via the same mechanism.
- "Remove affected leaves" / "thin the planting" -- USU preamble.
- "drip irrigation and avoiding overnight leaf wetness are the practical controls Utah State recommends" -- **verbatim true for Utah State**, and correctly attributed. (USU: "Consider drip irrigation..."; and, on the Mint Rust row, "Avoid wet leaves overnight.")

RECORD CLAIMS THAT ARE WRONG:
- "**and NC State list[s] leaf-spotting fungi for mint**" -- NC State says "**leaf spot**", generically, with
  no organism and no anthracnose. Attributing *anthracnose* to NC State overstates a one-word entry. Also
  note `ncsu_ext` is **not** in this entry's `sources` array, yet the seasoned prose credits NC State -- an
  attribution with no matching key, the same shape as the verticillium defect above.
- "**water at the base rather than overhead**" / "keep the foliage dry" **applied to powdery mildew** --
  contradicted verbatim by UC IPM 7406 and WSU (quoted above). This is wrong advice on the powdery-mildew
  half of the bundle.
- "Heavily spotted **or coated** leaves are not good to eat" -- the "coated" (powdery mildew) half carries the
  same consumption claim as the rust entry, with the same absence of any anchor. Same recommendation: soften.

RECORD CLAIMS WITH NO ANCHOR (verbatim from the record):
- The `sources: ["uc_ipm","usu_ext"]` array as it stands: **`usu_ext` anchors the anthracnose half only, and
  `uc_ipm` anchors the powdery mildew half only.** Neither source supports the entry as a whole. On split,
  each key lands on the right record.
- The `uc_ipm` anchor for powdery mildew is the mint page's **link** to Pest Notes 7406, and 7406's own host
  list is vegetables -- artichoke through turnip -- with **no herb in it**. So the anchor establishes "UC IPM
  lists powdery mildew as a mint problem" and establishes **nothing at all** about powdery mildew *on mint*.
  This is a "right document, wrong claim" case: the general biology in 7406 is sound, but the document is not
  about this host. **The WSU mint document is the anchor this limb actually needs.**
- "anthracnose or leaf spot" as synonyms -- USU lists Anthracnose; NCSU lists leaf spot; no document says
  they are the same thing.
- "shear a badly affected patch to force clean regrowth" -- close to USU's anthracnose control but not the
  same instruction; USU says "prune healthy plants to the ground **in fall**", which is a seasonal sanitation
  step, not a mid-season shear-to-regrow.

LADDER-RELEVANT FACTS THE RECORD DOES NOT CARRY:
- **USU's anthracnose control is a three-part cultural rung the record loses**: "Rotate planting areas, remove
  diseased plants, and **prune healthy plants to the ground in fall**." The fall cut-to-ground is the single
  most actionable anthracnose step on this crop and it is currently attached to the wrong entry (the record
  puts a cut-to-ground under *rust*, where no source puts it).
- **Cultivar susceptibility is published for powdery mildew**: "Scotch spearmint can be severely damaged
  while peppermint and native spearmint are usually not seriously affected" (WSU). That is a resistance
  signal that could hang off `varieties[].resistance`.
- **A fertility driver is published**: powdery mildew "most severe on young, succulent plants such as those
  resulting from heavy nitrogen fertilization and irrigation" (WSU) -- the same go-easy-on-nitrogen rung the
  aphid entry already uses.
- **A siting driver is published**: "often severe on mint grown in the greenhouse due to humid, shady
  conditions" (WSU); "shady conditions generally are the most favorable" (7406). Relevant because mint is the
  one herb this dataset sends into part shade.
- **Overwintering is published**: "infected mint plants, stubble and wild hosts of the mint family" (WSU) --
  the same fall-sanitation rung as rust and anthracnose. Three of mint's diseases share one cheap cultural
  rung (clear the stubble in fall) and the record never says so.
- **A soft-chemical rung is published with its limits**: sulfur, "only effective when applied before disease
  symptoms appear" (7406); "Initial applications of sulfur are usually made when plants are 4 to 6 inches
  tall"; "Sulfur should not be applied if temperatures will exceed 90F within 3 days after application" (WSU).
  Renders as **90°F**. Also horticultural/neem/jojoba oil to "eradicate mild to moderate ... infections" (7406)
  -- one of the few *eradicant* soft rungs in the whole dataset.
- **The commercial fungicides named by WSU (Amistar, Headline, Quadris, Rally) must not be carried onto a
  home ladder** -- they come with 7- to 30-day preharvest intervals on an oil crop, and mint at home is cut and
  eaten the same day.

---

## 5. Other findings on this record (reported, not acted on)

1. **UC IPM lists two mint pests the record does not carry at all**: **Leafhoppers** and **Thrips**
   (https://ipm.ucanr.edu/home-and-landscape/mint/). Both are catalog-admitted at the entry level
   (`ucanr_ext_thrips` is already a catalog key). Sage in this same batch carries `Leafhoppers`. This is a
   coverage gap, not an error.
2. **UC IPM also lists "Cold Injury and Frost Damage" and "Common Environmental Disorders of Vegetables"**
   for mint under Environmental Disorders. Out of scope for `pests[]`/`diseases[]`, noted for completeness.
3. **`verification_log_ref` needs a `[CORRECTION 2026-09-04: ...]` append**, not a rewrite, if any of this is
   acted on: the log asserts the Connecticut credit was struck, and one instance survived.
4. **Consumer-copy check: mint's problem prose is CLEAN.** Programmatic scan of all 12 prose fields across
   all 6 problems found: no em dashes, no en dashes, no mid-sentence capitalized "Plant", no bare-`F`
   temperatures, no British spellings. (Note that any new prose from this report's WSU quotes must convert
   "113 F", "90F" -> `113°F`, `90°F`.)
5. **No problem on any batch-25 crop carries an `id` yet** -- that is the batch's minting job, not a mint-specific gap. Flagged because the §4f verdict depends on ids that do not exist yet.

---

## SUMMARY

**Counts by STATUS (6 entries as currently structured):**

| STATUS | count | entries |
|---|---|---|
| SOURCED-OK | 2 | Aphids; Spider mites |
| SOURCED-WEAK | 3 | Cutworms/mint flea beetles/root-feeding pests (mixed: 1 sourced limb, 1 over-named limb, 1 UNSOURCED-FOUND limb); Mint rust (upgrades to SOURCED-OK with `rhs` + `wsu_ext` added); Verticillium wilt (upgrades with `uc_ipm` peppermint added; one WRONG attribution to strike) |
| WRONG | 1 | Powdery mildew and anthracnose (leaf spot) -- wrong **as a bundle** |
| UNSOURCED-NOT-FOUND | 0 | -- |
| JOURNAL-ONLY | 0 entries, **1 cross-crop claim** | the mint/oregano race specialization (§4f) |

**Restated after the two recommended splits (9 entries):** SOURCED-OK 6 (aphids, spider mites, cutworms,
flea beetles, mint root borer, anthracnose), SOURCED-WEAK 3 (mint rust, verticillium wilt, powdery mildew --
all three upgrade to OK on the source swaps named above; every anchor needed is already in the catalog).

**Zero entries are unsourceable.** Every claim I could not anchor on a cited page, I anchored on a
catalog-admitted page the record does not yet cite -- with exactly one exception, below. The hunt found T1
support at `rhs`, `wsu_ext` and three unused `uc_ipm` URLs.

### The single most important finding

**The bundled entry "Powdery mildew and anthracnose (leaf spot)" ships advice that is wrong for half of
itself.** Its shared prevention string tells the gardener to "water at the base rather than overhead" and
"keep the foliage dry" -- correct for anthracnose, and the exact opposite of what both admitted sources say
about powdery mildew: UC IPM 7406, "Overhead sprinkling may help reduce powdery mildew because spores are
washed off the plant"; WSU, "Powdery mildew is generally not a problem in mint irrigated with overhead
sprinklers from a center pivot system", and stopping that irrigation for a few days lets it "increase very
rapidly". Compounding it, neither cited source actually supports the entry as a whole: `usu_ext` never
mentions powdery mildew, and the `uc_ipm` anchor resolves to Pest Notes 7406, whose host list runs artichoke
to turnip and **contains no herb**. **This cannot be fixed inside the bundle. Split it into the existing
shared ids `powdery-mildew` and `anthracnose`, and re-anchor the powdery mildew half to the WSU
mint-specific document.**

### Runners-up, in order

2. **Mint rust's three load-bearing claims are carried by neither cited document** -- the binomial
   *Puccinia menthae*, the rhizome overwintering, and "no reliable home cure" are on **neither** NC State nor
   Utah State. All three are anchorable today at `rhs` (+ `wsu_ext`), and the overwintering claim should be
   **rewritten, not just re-cited**: RHS hedges it ("the general consensus **was**"), WSU puts overwintering
   on **stubble and fallen foliage** instead, and the difference changes the ladder -- it puts "clear the
   stubble in fall" and a **113°F / 10-minute hot-water rhizome dip** below "start over in a new spot", where
   the record currently has nothing.
3. **A fabricated attribution is live**: Verticillium wilt still reads "The Connecticut Experiment Station
   and Utah State both flag it for mint", eight weeks after mint's own cert log recorded striking that exact
   credit from the neighboring entries. Strike it.
4. **"Rusty leaves are not good to eat" has no catalog-admitted anchor.** The only extension-branded text is
   a 2019 Ask Extension answer from Hennepin County, Minnesota, on a domain the catalog does not admit. This
   is a consumption claim: soften it to RHS's actual, stronger point -- there is no fungicide cleared for
   rust on culinary herbs, so the answer is to cut the affected growth out -- or file `ask.extension.org` as
   a catalog-addition decision. Do not ship the absolute on that evidence.
5. **§4f: `mint-rust` and `oregano-rust` should be TWO ids -- of ONE pathogen species.** The host
   specialization is **JOURNAL-ONLY** (four APS records, all cited in full in §4f; all 403'd on read, so the
   host-range sentences are abstract-level leads, not verified reads). No catalog-admitted source carries it,
   and the only admitted source on host range -- `rhs` -- says *Puccinia menthae* also infects **marjoram**
   (*Origanum majorana*) and savory, with no race distinction. Keep two ids for the join-key and ladder
   reasons; keep both records' consumer prose **silent** on cross-infection; register the pair in
   `tools/problem_id_registry.json` under `deliberately_distinct` (it is not there now).
6. **The record gap the task flagged is real and total**: `severity` and `type` are **absent keys**, not
   nulls, on all 6 mint problems, uniquely in this batch (30/30 problems on the other six crops carry both).
   Proposed values, with roster-computed justification, are in §1. While computing them I found a
   **batch-wide typing defect**: oregano, rosemary and thyme type **Spider mites as `insect`**; the roster
   convention is `mite` (25/31), and sage already gets it right.

**Five documents that should be read before mint's ladder is finalized and that I could not open**
(403 or TLS, not absence): the PNW Plant Disease Management Handbook mint-rust and mint-verticillium pages,
OSU Extension EM 9299 (OR/WA/ID mint IPM strategic plan), OSU Extension's verticillium recognition page, and
University of Illinois Extension RPD No. 1221 "MINT RUST". Four of the five bear directly on claims I marked
unverified above (one-sided verticillium symptoms, bronze spring growth, and the mint flea beetle's species
identity).
