#!/usr/bin/env python3
"""Artichoke GS arc -- the 39 region/zone cells.

DESIGN: docs/2026-07-26-artichoke-design-decisions.md. Read B.0 (the mechanism) and B.6
(the suitability vocabulary) before changing any rating here.

THE RULE EVERY CELL OBEYS. Every non-`unsuitable` cell carries BOTH `plant_out` (A47) and
`harvest` (A48). That is the asparagus defect, closed at the data layer rather than trusted
to a gate: asparagus passed 120/120 with zero of both.

CALENDAR TOKENS ARE AUTHORED SO THE CELLS PASS A24/A34/A37 ON THEIR OWN MERITS, WITHOUT the
herbaceous_perennial carve-outs. That is the binding criterion in design-decisions B.2: the
A24 exemption exists because a DORMANT CROWN is planted into cold ground, and artichoke in
cold regions plants a LIVE VERNALIZED TRANSPLANT instead -- the exact case A24 protects. So
every calendar here shows a real `plant` token in its real planting month, and `indoors`
where seed is genuinely started under protection. Verify with tools/carveout_dependency_audit.py.

SUITABILITY, per B.6 -- the enum answers "does the PLANTING PERSIST", not "is it worth growing":
  perennializes     -> the stand persists and crops for years (winter minima above the 14-15F
                       crown-kill line, summers that do not chronically devernalize)
  marginal          -> crops, but the planting does not persist: annual culture, or a short-lived
                       or protected stand
  survives_no_fruit -> the plant grows and never buds. Ornamental only.
  unsuitable        -> do not plant; ONLY where there is no crop AND no plant worth having

LOAD-BEARING: because vernalization is QUANTITATIVE (57-74% bud set with NO cold at all,
Rutgers FS044), an "insufficient chill" argument CANNOT carry `unsuitable`.

REVISED 2026-07-28 -- AND IT WAS NOT STRONG ENOUGH TO CARRY `unsuitable` EITHER. The tropical
cells were originally rated `unsuitable` on UF/IFAS's statement that in Florida "bud formation
must be artificially induced". That sentence is real and it does rule out a CROP. It says nothing
against the PLANT, and the same publication reports the other half of its own experiment:

    "untreated plants remained vegetative until the end of the growing season"     -- HS1289

The untreated plants did not fail. They grew, in Florida, all season, and simply never bolted --
which is `survives_no_fruit` exactly, a value with a ruled display behavior (flagged
ornamental-only: the plant lives and gives you no food, someone may still want it) and 118 cells
of roster precedent. HS1289 also describes what you actually get, in the same paragraph: a rosette
of "arching, deeply toothed, silvery, woolly green leaves that are normally 20 to 32 inches long".
That is a plant people grow on purpose.

Rating it `unsuitable` hid a cell about a plant that grows perfectly well, and told a grower
nothing where it could have told them something true. Seven cells move: hawaii_tropical z10-z13,
fl_peninsula z10/z11, se_gulf z10.

`ca_desert` z11 STAYS `unsuitable`, and the difference is the whole point of keeping both values.
It is not an agronomic verdict at all -- no California desert ground reaches zone 11, so the cell
is VACANT. There is no plant to describe because there is nobody standing there.

CONSEQUENCE AT THE GATE LAYER, since these cells now carry a calendar and are no longer exempt:
A47 REQUIRES plant_out on them (someone may want the foliage, so tell them when to plant it) and
A48 EXEMPTS them from harvest (there is no food; inventing a window would be a false promise).
That asymmetry is deliberate and is pinned by tests in both gates' suites.
"""

# ---------------------------------------------------------------- calendars
# TOKEN CHOICES, and why heat_pause is absent from this crop:
#   cold_pause -- the winter off-season of an annual, and the dormant winter of a perennial. This
#                 is the roster convention (tomato/pepper northern_tier show cold_pause Nov-Mar).
#   season_over -- a SUMMER gap where the crop has been pulled or is finished. Used instead of
#                 heat_pause deliberately. A shown heat_pause is a THERMAL CLAIM that A28 requires
#                 to be BACKED per cell (months + basis_seasoned + sources), and Trevor's standing
#                 rule is that a new crop's summer gaps stay season_over until a backed heat_pause
#                 is authored at variety-pass. The sources here support a BUD-QUALITY ceiling
#                 ("tolerant of temperatures above 86F, but the quality of the edible flower bud is
#                 reduced") -- they do NOT say vegetative growth stalls. Showing heat_pause would
#                 assert a stop nothing supports, which is the asparagus desert-fern trap.
#   plant / indoors -- authored honestly wherever a real transplant or a real indoor sowing
#                 happens. These are what make A24/A34 pass WITHOUT the archetype carve-outs.
CP, HV, GR, PL, IN, SO = ("cold_pause", "harvest", "growing", "plant", "indoors", "season_over")


def cal(*tok):
    assert len(tok) == 12, len(tok)
    return list(tok)


# The cold-region annual cycle: seed indoors -> vernalize -> set out -> grow -> late-summer buds
# -> killed by hard frost. `indoors` is honest here (VCE: greenhouse transplants, direct seeding
# explicitly rejected) and it is what makes A34 pass without the carve-out.
NORTH_Z3 = cal(CP, CP, IN, IN, IN, PL, GR, HV, HV, CP, CP, CP)
NORTH_Z4 = cal(CP, CP, IN, IN, PL, GR, GR, HV, HV, CP, CP, CP)
NORTH_Z5 = cal(CP, CP, IN, IN, PL, GR, GR, HV, HV, HV, CP, CP)
NORTH_Z6 = cal(CP, IN, IN, PL, PL, GR, HV, HV, HV, HV, CP, CP)
NORTH_Z7 = cal(CP, IN, IN, PL, PL, GR, HV, HV, HV, HV, CP, CP)

MIDATL_Z7 = cal(CP, IN, PL, PL, GR, GR, GR, HV, HV, HV, CP, CP)
MIDATL_Z8 = cal(IN, IN, PL, PL, GR, GR, GR, HV, HV, HV, CP, CP)

# Mid-South: same spring-annual shape as the mid-Atlantic, one notch earlier, and the summer is
# the limiting factor rather than the winter (see the notes -- Southside-Virginia heat rule).
MIDSOUTH_Z7 = cal(CP, IN, PL, PL, GR, GR, GR, HV, HV, HV, CP, CP)
MIDSOUTH_Z8 = cal(IN, IN, PL, PL, GR, GR, HV, HV, HV, CP, CP, CP)

# Warm arid inland z8: spring-set annual, in the ground all summer and cropping in fall. NOT the
# Texas fall model -- inland z8 winter minima sit below the 25F floor TAMU itself sets, so an
# overwintering fall planting is not defensible here. Summer is `growing`, not a pause: the plant
# is present and vegetative; it is BUD QUALITY the heat limits, and that shows up as the fall
# harvest window, not as a stop.
WARMARID_Z8 = cal(IN, IN, PL, PL, GR, GR, GR, GR, GR, HV, HV, CP)

# Nevada Mojave: z8 spring-set; z9/z10 Las Vegas Valley take the low-desert fall model (mild
# winter, hot summer), so the plant grows through winter, crops in spring, and is pulled.
NEVADA_Z8 = cal(CP, IN, PL, PL, GR, GR, HV, HV, SO, SO, CP, CP)
NEVADA_Z9 = cal(IN, PL, PL, GR, HV, HV, SO, SO, SO, SO, IN, IN)
NEVADA_Z10 = cal(IN, PL, PL, GR, HV, HV, SO, SO, SO, SO, IN, IN)

# Utah Dixie z8: USU puts artichoke in hardy Group A; the Washington County sheet puts St George's
# hardy window at Feb 15 - Mar 15. Combining the two is OUR arithmetic -- see resolution_method.
UTAHDIXIE_Z8 = cal(IN, PL, PL, GR, GR, GR, GR, GR, GR, HV, HV, CP)

# Maritime PNW. OSU EM 9027 gives Region 2 (western valleys) Aug-Nov AND April-June; WSU's own
# cycle is transplant end of April -> harvest mid-Sep to mid-Oct. z9 (Puget/coastal warm edge)
# clears the crown-kill line and perennializes; z8 does not reliably.
PNW_Z8 = cal(CP, IN, IN, PL, PL, GR, GR, GR, HV, HV, CP, CP)
PNW_Z9 = cal(GR, GR, GR, PL, PL, GR, GR, GR, HV, HV, HV, GR)

# California interior valleys: UC's July set-out, cropping through the cool months, and then --
# REVISED 2026-07-28 -- CARRIED, not pulled.
#
# The April token used to be `season_over`, which asserted that the planting ENDS every spring.
# That is the annual reading, and two UC sources do frame it that way (UCCE Contra Costa "Grow as
# annual"; the Tulare/Kings chart's row label is literally "Artichoke (annual)"). But the same
# Contra Costa sheet says in its next breath that the "plant may winter over if temperature stays
# above 25 F", and the binding constraint in the valley is not the winter at all.
#
# THE LIMITING FACTOR IS SUMMER WATER DEMAND, with heat as the thing the water buys relief from --
# not heat acting directly. Texas A&M states both halves: artichokes "are deep-rooted and require
# adequate moisture when growing and producing fruit", and "in the summer, irrigation will help
# keep temperatures down in the crop canopy to prevent bud opening". A big-canopy, deep-rooted
# plant carried through a valley summer is a large and unforgiving water bill; met, the stand
# persists for several years, and unmet it dies. That is a SHORT-LIVED PERENNIAL, and it is why
# the same ground produces one gardener's multi-year clump and the neighbour's dead crown.
#
# The rating stays `marginal` -- persistence that depends on generous irrigation is the textbook
# marginal case -- so only the April token and the reason change. Everything the annual sources
# support (the July set-out, the cool-season harvest, the seed route) is unchanged and still cited.
CAINT_Z8 = cal(HV, HV, HV, GR, IN, IN, PL, GR, GR, GR, HV, HV)
CAINT_Z9 = cal(HV, HV, HV, GR, IN, IN, PL, GR, GR, GR, HV, HV)

# California coast -- the crop's home ground. Perennial, cut back after the spring peak, second
# crop in fall. UC ANR 7221: peak March-April; VRIC: two crops per year on the cool coast.
CANORTH_Z9 = cal(HV, HV, HV, HV, HV, GR, GR, PL, PL, PL, HV, HV)
CANORTH_Z10 = cal(HV, HV, HV, HV, HV, GR, GR, PL, PL, PL, HV, HV)
CASOUTH_Z9 = cal(HV, HV, HV, HV, GR, GR, PL, PL, GR, HV, HV, HV)
CASOUTH_Z10 = cal(HV, HV, HV, HV, GR, GR, PL, PL, GR, HV, HV, HV)
CASOUTH_Z11 = cal(HV, HV, HV, HV, GR, GR, PL, PL, GR, HV, HV, HV)

# California desert + Arizona low desert: annual, set in the fall, cropped through winter/spring,
# gone before the heat. UCCE Imperial: "seldom marketable after early April."
CADESERT_Z9 = cal(HV, HV, HV, HV, SO, SO, SO, PL, PL, PL, GR, HV)
CADESERT_Z10 = cal(HV, HV, HV, HV, SO, SO, SO, PL, PL, PL, GR, HV)
LOWDESERT_Z9 = cal(PL, PL, PL, GR, HV, HV, SO, SO, SO, SO, IN, IN)
LOWDESERT_Z10 = cal(GR, GR, GR, GR, HV, HV, SO, SO, PL, PL, GR, GR)

# Gulf: LSU's October transplant, spring crop, then summer disease takes them out.
SEGULF_Z8 = cal(GR, GR, HV, HV, HV, SO, IN, IN, PL, PL, PL, GR)
SEGULF_Z9 = cal(GR, HV, HV, HV, HV, SO, IN, IN, PL, PL, PL, GR)
RGV_Z9 = cal(HV, HV, HV, SO, SO, SO, SO, IN, PL, PL, GR, GR)
RGV_Z10 = cal(HV, HV, HV, SO, SO, SO, SO, IN, PL, PL, GR, GR)

# The A32 honesty floor for the one genuinely `unsuitable` cell (ca_desert z11, VACANT GROUND):
# an honest all-growing strip, no window, and a note that dominates. A47/A48 exempt it by design.
ALL_GROWING = [GR] * 12

# ORNAMENTAL-ONLY calendars (survives_no_fruit). These carry a real `plant` token because the
# planting is real -- what is absent is the harvest, and no `harvest` token appears anywhere in
# either strip. That is the honest depiction: a grower puts a plant in the ground, it grows, and
# nothing is ever picked.
#
# FLORIDA / the peninsular Gulf. UF/IFAS HS1289: "In Florida, annual culture between October and
# May is recommended to avoid the hot and wet summer" + "Seedlings should be transplanted in the
# field no later than mid-November." The summer is `season_over` rather than `growing` because
# that is what the source says happens -- the planting is finished by the heat and the wet, not
# carried through it. A one-season foliage plant, and the note says so.
TROPICS_FL = cal(GR, GR, GR, GR, GR, SO, SO, SO, SO, PL, PL, GR)

# HAWAII. No season_over, because nothing here ends the plant: there is no cold season and no
# hot-and-wet break in the way Florida has one, so the rosette simply persists. The planting
# window is the cool half of the year and it is a CONVENIENCE, not a requirement -- the plant is
# not waiting for anything, it establishes more easily out of the hottest months. Stated in the
# note rather than implied by the strip.
TROPICS_HI = cal(PL, PL, GR, GR, GR, GR, GR, GR, GR, GR, PL, PL)

# ---------------------------------------------------------------- shared prose
_MECH_HEAT = ("bud quality falls off above 86°F, when the bracts open early and the heart "
              "turns tough and bitter")
_MECH_CROWN = ("the crown suffers severe loss below about 15°F even under mulch, so the "
               "planting does not carry over")
_MECH_DEVERN = ("summer heat can reverse accumulated chilling, so fewer plants set buds")

# The ornamental-only core, shared by all seven survives_no_fruit cells. Per-cell additions carry
# the part that is NOT shared, because a blanket note is a claim about every cell it lands on
# (kickoff R6, learned when a "both routes to dormancy fail" note went out across the asparagus
# unsuitable cells and was false for the arid ones).
_ORN_S = (
    "Artichoke will grow on this ground and it will not crop on it, and the reason is narrow "
    "rather than general. The part you eat is an immature flower bud, and bud initiation needs a "
    "run of hours below 50°F that this climate never banks. UF/IFAS ran that experiment in "
    "Florida and reported both halves of it: plants sprayed with gibberellic acid formed buds, "
    "while the untreated ones stayed leafy right through to the end of the season and never "
    "bolted at all. Those plants did not struggle or die, they simply never flowered. Spraying a growth regulator on a "
    "schedule is a commercial operation rather than a garden one, so plan on the plant and not "
    "on the crop. What the plant gives you is genuinely worth having: UF/IFAS describes the "
    "rosette as arching, deeply toothed, silvery, woolly leaves 20 to 32 inches long.")
_ORN_B = (
    "You can grow artichoke here, but you will not get artichokes. The part you eat is a flower "
    "bud, and the plant only makes buds after a stretch of genuinely cool weather that this "
    "climate does not get, so it stays a large leafy rosette instead. That rosette is silver, "
    "deeply cut, and up to about two and a half feet across, which is why people grow this plant "
    "for looks alone in warm climates. Plant it for the foliage and grow something else for "
    "dinner. If you have your heart set on eating one, grow it in a pot you can move somewhere "
    "cool for a few weeks.")


def _annual_note_s(where, extra=""):
    return ("Grow artichoke as an annual here and plan to replant: " + where + " " + extra).strip()


# ---------------------------------------------------------------- the cells
# Each entry: (suitability, calendar, plant_out, harvest, resolution_method, sources, notes,
#              suitability_note_seasoned, suitability_note_beginner)
# `sources` are ids that must exist in source_catalog; anchoring_urls are attached by the builder
# from SOURCE_URLS so that every cited id resolves to the SPECIFIC document carrying the claim.

CELLS = {}


def C(region, zone, suitability, calendar, plant_out, harvest, method, sources,
      notes=None, note_s=None, note_b=None, start_indoors=None):
    """start_indoors BACKS an `indoors` calendar token. A calendar that shows `indoors` with no
    start_indoors window is the asparagus defect in miniature -- the app renders "start seed now"
    and has no date to give. whole_crop_gate's indoors-run-backing rule enforces it; every
    `indoors` run below is backed."""
    CELLS.setdefault(region, {})[zone] = dict(
        suitability=suitability, calendar=calendar, plant_out=plant_out, harvest=harvest,
        resolution_method=method, sources=sources, notes=notes, start_indoors=start_indoors,
        suitability_note_seasoned=note_s, suitability_note_beginner=note_b)


# ======================= northern_tier (z3-7) -- annual culture =======================
_N_S = ["umaine_2075", "umass_nevmg", "umaine_highmoor"]
C("northern_tier", "3", "marginal", NORTH_Z3,
  "Jun 1 - Jun 20 (vernalized transplants, replant each year)", "Aug - Sep",
  "mechanism_derived_beyond_published_range", _N_S,
  start_indoors="Mar 15 - Apr 15",
  notes=("Start seed indoors in March, give the seedlings three weeks near 40°F once they "
         "have four to six true leaves, and set them out when frost is done. Buds follow roughly "
         "60 to 100 days after transplanting, which lands them in late summer just ahead of the "
         "first hard freeze."),
  note_s=("This is the coldest ground artichoke is worth attempting on, and it sits beyond the "
          "published record: the northernmost documented trials are in central Maine, upstate "
          "New York and Connecticut, and no extension service publishes a zone 3 protocol. The "
          "arithmetic is what makes it tight rather than impossible, since 60 to 100 days from "
          "transplanting has to fit inside a season that often runs only 90 to 100 frost-free "
          "days. Winter kill is not in question here, " + _MECH_CROWN + ", so treat every "
          "planting as a one-season crop."),
  note_b=("You can grow artichoke here, but treat it as an experiment rather than a staple. Start "
          "seed indoors in March, chill the seedlings for about three weeks, and plant out once "
          "frost is past. Expect a small late-summer crop of modest buds, and expect the plants "
          "to die over winter. Choose a variety bred for first-year cropping, such as Imperial "
          "Star, since the older perennial types often produce nothing at all in year one."))

C("northern_tier", "4", "marginal", NORTH_Z4,
  "May 20 - Jun 10 (vernalized transplants, replant each year)", "Aug - Sep",
  "mechanism_derived_beyond_published_range", _N_S,
  start_indoors="Mar 10 - Apr 10",
  notes=("Sow indoors in March, vernalize the seedlings, and transplant once frost risk passes in "
         "late May. Harvest opens in August and runs until a hard freeze ends it."),
  note_s=("Artichoke crops here as an annual and does not overwinter: " + _MECH_CROWN + ", and "
          "the measured field results are blunt about it, with upstate New York recording zero "
          "survivors under six inches of straw. The season is long enough for the 60 to 100 day "
          "window from transplanting, so a real crop is realistic, but the buds run small. Maine "
          "trials found most buds under three inches even in a good year."),
  note_b=("Grow it as an annual. Start seed indoors, chill the young plants, set them out after "
          "the last frost, and pull them when winter kills them. You should get buds in late "
          "summer, though most will be smaller than supermarket artichokes."))

C("northern_tier", "5", "marginal", NORTH_Z5,
  "May 20 - Jun 10 (vernalized transplants, replant each year)", "Aug - Oct",
  "extension_regional_guide", _N_S,
  start_indoors="Mar 10 - Apr 10",
  notes=("This is the best-documented cold-region cycle: seed sown in the last third of March, "
         "seedlings chilled about three weeks near 40°F at the four to six leaf stage, "
         "transplanted late May to mid June, first buds from mid August, and harvest continuing "
         "into early October until a hard freeze."),
  note_s=("Artichoke is a genuine annual crop on this ground and a genuine failure as a perennial: "
          "University of Maine runs multi-year trials here and grows it from transplants every "
          "year precisely because the plants are not cold-hardy enough to survive the winter "
          "reliably. Expect 10 to 20 buds per plant, most under three inches, with only two or "
          "three primaries large enough to look like store artichokes."),
  note_b=("A good annual crop here, but you replant every year. The one step people skip is the "
          "cold treatment: young plants need about three weeks in a refrigerator or cold frame "
          "before they go outside, or many of them never form buds at all. Harvest from August "
          "until frost kills the plants."))

C("northern_tier", "6", "marginal", NORTH_Z6,
  "Apr 20 - May 20 (vernalized transplants, replant each year)", "Jul - Oct",
  "extension_regional_guide", _N_S,
  start_indoors="Feb 15 - Mar 20",
  notes=("Start seed indoors in February, chill the seedlings, and set them out from late April. "
         "The longer season pulls first harvest forward into July and lets picking run into "
         "October on secondary buds."),
  note_s=("Annual culture is the reliable route. Cornell reports that transplanting before "
          "mid-May supplies enough natural chilling in upstate New York without a cooler, though "
          "controlled vernalization still buys earlier and more uniform budding. Overwintering is "
          "the doubtful part rather than the cropping: " + _MECH_CROWN + ", and mulch alone has "
          "repeatedly failed in trials."),
  note_b=("Grow it as an annual and you will do well. Set out chilled transplants in late April "
          "or early May and start picking in July. Some gardeners try to carry plants through "
          "winter under deep mulch; it occasionally works and usually does not, so plan on "
          "replanting."))

C("northern_tier", "7", "marginal", NORTH_Z7,
  "Apr 10 - May 10 (vernalized transplants, replant each year)", "Jul - Oct",
  "extension_regional_guide", _N_S + ["cornell_ext"],
  start_indoors="Feb 10 - Mar 15",
  notes=("Set chilled transplants out in April. First buds arrive in July, and light picking of "
         "secondary buds continues into October."),
  note_s=("The warm edge of annual culture and the cold edge of any perennial attempt. Sources "
          "disagree about this exact band: a Maine bulletin calls artichoke hardy in zone 7 and "
          "warmer, Cornell puts it at zone 6 with good mulch, while the measured crown-kill "
          "temperature of about 15°F corresponds to warmer ground than either claim. Given "
          "that spread, plan an annual crop and treat any overwintering success as a bonus."),
  note_b=("Plant chilled transplants in April for a July through October harvest. Plants "
          "sometimes survive the winter here if you cut them back and mulch deeply, and a "
          "second-year plant crops earlier, so it is worth trying. Do not count on it."))

# ======================= mid_atlantic (z7-8) -- VCE 438-108 =======================
_MA_S = ["vce_438_108", "ncsu_ext"]
C("mid_atlantic", "7", "marginal", MIDATL_Z7,
  "Mar 25 - Apr 30 (vernalized transplants, replant each year)", "Aug - Sep",
  "extension_regional_guide", _MA_S,
  start_indoors="Feb 1 - Feb 28",
  notes=("Virginia Cooperative Extension sets transplants from late March through April so the "
         "young plants pick up their chilling outdoors, in the field, in the weeks right after "
         "planting. Buds start 60 to 100 days later and the crop concentrates from mid August "
         "through September."),
  note_s=("This region has its own extension crop profile and it rules artichoke an annual: the "
          "chilling happens after planting, from roughly 190 to 240 hours at or below 50°F, "
          "which is why the planting date is pinned to the last frost rather than chosen for "
          "convenience. Overwintering has been measured rather than guessed, and it is poor: 30 "
          "to 40 percent survival at Blacksburg under hooped vented plastic plus a floating row "
          "cover, and few plants at all under straw, a single cover, or plastic alone. Expect 15 "
          "to 25 percent of plants to stay barren even when chilling is adequate."),
  note_b=("Set out transplants in late March or April, a week or two before your last frost date. "
          "That early planting is deliberate: the cool spring weather right after planting is "
          "what makes the plant form buds. Cover them if a hard freeze threatens. Pick from "
          "mid August into September, then pull the plants."))

C("mid_atlantic", "8", "marginal", MIDATL_Z8,
  "Mar 1 - Apr 15 (vernalized transplants, replant each year)", "Aug - Sep",
  "extension_regional_guide", _MA_S,
  start_indoors="Jan 15 - Feb 28",
  notes=("The same Virginia annual system, run a few weeks earlier to match the earlier last "
         "frost on the coastal plain. Sow indoors in January or February, six to seven weeks "
         "ahead of the intended transplant date."),
  note_s=("Warm enough that summer heat, not winter, is the binding constraint: Virginia "
          "Cooperative Extension recommends the middle and upper Piedmont and the mountains for "
          "this crop and advises against the state's southern tier outright, because "
          + _MECH_HEAT + ". " + _MECH_DEVERN.capitalize() + ", which is the same mechanism seen "
          "in New Jersey trials where black plastic mulch cut yields by heating the roots."),
  note_b=("Plant early, from March into mid April, and give the plants some afternoon shade if "
          "you can. The enemy here is summer heat, which makes buds open early and turn tough. "
          "Harvest in August and September, then replant next spring."))

# ======================= mid_south (z7-8) -- NO regional source =======================
_MS_S = ["vce_438_108"]
C("mid_south", "7", "marginal", MIDSOUTH_Z7,
  "Mar 20 - Apr 25 (vernalized transplants, replant each year)", "Aug - Sep",
  "mechanism_derived_no_regional_source", _MS_S,
  start_indoors="Feb 1 - Feb 28",
  notes=("No extension service in Arkansas, Oklahoma, Tennessee or Missouri lists artichoke, so "
         "this window is carried over from the Virginia annual system at a matching last-frost "
         "date rather than lifted from a regional chart."),
  note_s=("Worth stating plainly: none of the four state extension services in this region "
          "publishes an artichoke planting date, variety list or crop profile. Missouri's "
          "perennial-vegetable category contains only asparagus and rhubarb, and Oklahoma "
          "recommends cardoon, the leaf-stalk form of the same species, while listing no "
          "artichoke at all. Treat artichoke as a spring-planted annual here and expect summer "
          "heat to shorten the crop; wet winters are hard on any plant left in the ground."),
  note_b=("Your state extension service does not cover artichoke, so treat this as a trial. Set "
          "out chilled transplants in early spring and pick in late summer. Do not expect plants "
          "to survive the winter, and do not be surprised if a wet winter rots any that try."))

C("mid_south", "8", "marginal", MIDSOUTH_Z8,
  "Mar 1 - Apr 10 (vernalized transplants, replant each year)", "Jul - Sep",
  "mechanism_derived_no_regional_source", _MS_S,
  start_indoors="Jan 15 - Feb 20",
  notes=("Planted a few weeks earlier than the zone 7 side to get bud set done before the "
         "summer heat arrives. No regional extension source publishes an artichoke window."),
  note_s=("The same regional gap applies, and the heat constraint is sharper here. Virginia's "
          "extension profile declines to recommend annual artichoke in its own hottest counties "
          "because " + _MECH_HEAT + ", and this ground is hotter still. Plant as early as frost "
          "protection allows so that buds form before midsummer."),
  note_b=("Plant as early in spring as you can protect the young plants, because artichoke wants "
          "to make its buds while the weather is still cool. Pick from July, and pull the plants "
          "when summer finishes them."))

# ======================= warm_arid (z8) -- NM + west TX =======================
_WA_S = ["tamu_eht065"]
C("warm_arid", "8", "marginal", WARMARID_Z8,
  "Mar 1 - Apr 10 (vernalized transplants, replant each year)", "Oct - Nov",
  "mechanism_derived_no_regional_source", _WA_S,
  start_indoors="Jan 15 - Feb 20",
  notes=("New Mexico State publishes nothing on artichoke and Texas A&M's fall-planted system is "
         "written for Central Texas, so this is a spring-set annual matched to the region's own "
         "frost dates. Growth stalls through the hottest weeks and resumes for a fall crop."),
  note_s=("Two separate reasons this is not the Texas fall system. Winter minima on inland zone 8 "
          "ground sit below the 25°F floor Texas A&M itself sets for the crop, so a planting "
          "left in the ground over winter is at real risk, and New Mexico State Extension does "
          "not list artichoke among its vegetables at all, its perennial-vegetable section naming "
          "only asparagus and rhubarb. Summer is the other limit, since " + _MECH_HEAT + " and "
          "the dry air opens buds faster still."),
  note_b=("Plant in early spring and give the plants shade and steady water through the worst of "
          "the summer. They will mostly sit still in the heat and then grow again in fall, which "
          "is when you pick. Expect to replant each year."))

# ======================= nevada (z8-10) -- documented absence =======================
_NV_S = ["unlv_mg_svn", "unr_ext_fs1305", "uariz_ext_az1005"]
C("nevada", "8", "marginal", NEVADA_Z8,
  "Mar 1 - Apr 10 (vernalized transplants, replant each year)", "Jul - Aug",
  "adjacent_zone_derived", _NV_S,
  start_indoors="Jan 15 - Feb 28",
  notes=("The higher, colder end of the Mojave belt. The southern Nevada Master Gardener chart's "
         "February-to-March artichoke window is written for the valley floor, so it is pushed back "
         "here to clear the later frost, with harvest following in mid summer."),
  note_s=("Nevada Extension covers this crop in two places: a Master Gardener planting chart for "
          "southern Nevada that gives artichoke a February through late March window, and a Moapa "
          "and Virgin Valleys variety guide recommending Green Globe, Imperial Star and Violetta. "
          "Neither addresses this colder, higher ground specifically, so the window is shifted from "
          "the valley figure rather than read off it. Both limits bite here: " + _MECH_CROWN
          + " on the hardest nights, and " + _MECH_HEAT + " through the summer."),
  note_b=("Plant a few weeks later than the Las Vegas valley floor, once hard frost is done, and "
          "pick in midsummer. Expect to replant each year."))

C("nevada", "9", "marginal", NEVADA_Z9,
  "Feb 1 - Mar 31 (transplants, replant each year)", "May - Jun",
  "extension_regional_guide", _NV_S,
  start_indoors="Dec 1 - Jan 15",
  notes=("The southern Nevada Master Gardener planting chart lists artichoke as a cool-season crop "
         "for early February through late March. Unlike most of the cool-season list it gets no "
         "fall window, so this is a single spring planting that crops in late spring and is "
         "finished by the summer heat. Start seed indoors around the turn of the year."),
  note_s=("This is the Las Vegas Valley, and the spring timing is the point: the chart gives "
          "artichoke a February to March window and no autumn one, which matches the University of "
          "Arizona's Maricopa County calendar setting transplants from mid January through March "
          "on comparable ground. Nevada Extension separately recommends Green Globe, Imperial Star "
          "and Violetta for the state's low desert, noting Imperial Star will produce in its first "
          "year from seed, typically one or two primary buds of three or four inches plus five to "
          "seven smaller side buds. Rated as an annual because no source says the planting persists "
          "here, and " + _MECH_HEAT + " once summer arrives."),
  note_b=("Plant in February or March, not fall, and start seed indoors around New Year. You should "
          "cut buds in May and June, then the summer heat ends it and you start again next winter. "
          "Green Globe, Imperial Star and Violetta are the varieties Nevada Extension suggests, and "
          "expect one or two full-size buds per plant plus a handful of smaller ones."))

C("nevada", "10", "marginal", NEVADA_Z10,
  "Feb 1 - Mar 31 (transplants, replant each year)", "May - Jun",
  "extension_regional_guide", _NV_S,
  start_indoors="Dec 1 - Jan 15",
  notes=("The warmest, most frost-free pockets of the belt, on the same spring-planted chart "
         "window as the valley floor."),
  note_s=("Same sourced spring window as the adjacent zone, and warm enough that frost is rarely "
          "the limit, which puts the whole question on summer heat and on whether the winter banks "
          "enough cool hours to set buds. Bud initiation does happen here, but " + _MECH_DEVERN
          + ", so expect a lighter and less uniform set than a coastal climate gives."),
  note_b=("Plant in February or March for a late-spring harvest. Summer heat ends the crop, so do "
          "not try to carry plants through it."))

# ======================= utah_dixie (z8) =======================
_UD_S = ["usu_ext_artichoke", "usu_washco_dates"]
C("utah_dixie", "8", "marginal", UTAHDIXIE_Z8,
  "Feb 15 - Mar 15 (vernalized transplants, replant each year)", "Oct - Nov",
  "two_source_derived_frost_anchored", _UD_S,
  start_indoors="Jan 1 - Jan 31",
  notes=("Utah State places artichoke in its hardy Group A, to be set out three to four weeks "
         "before the frost-free date, and the Washington County sheet puts the St George hardy "
         "window at February 15 to March 15 against a March 30 last frost. Combining those two "
         "gives this window. Start seed indoors in early January."),
  note_s=("This window is assembled from two Utah State documents rather than read off one, and "
          "that matters: the statewide planting-date fact sheet explicitly says its dates do not "
          "apply to Washington County, and the county material it points to never mentions "
          "artichoke, even though it does list rhubarb, asparagus and chives. So no source states "
          "an artichoke date for this ground. Utah State's own summer caution applies directly, "
          "that hot weather while the flower stalk is forming often leaves the plant with none, "
          "and this is the hottest corner of the state."),
  note_b=("Start seed indoors in early January and set the plants out in late February. That "
          "early date is the whole trick, because artichoke needs cool weather to form buds and "
          "St George warms up fast. Expect to replant each year; heavy mulch sometimes carries a "
          "plant through winter, but summer is the bigger problem."))

# ======================= pnw (z8-9) =======================
_PNW_S = ["osu_oregon_veg", "wsu_em057e", "osu_ext"]
C("pnw", "8", "marginal", PNW_Z8,
  "Apr 1 - Jun 15 (transplants or crown divisions)", "Sep - Oct",
  "extension_regional_guide", _PNW_S,
  start_indoors="Feb 15 - Mar 31",
  notes=("Oregon State's home-garden guide gives the western valleys an April to June window "
         "using crown pieces, and Washington State's own cycle transplants at the end of April "
         "for a mid September to mid October harvest. Oregon State recommends deliberately "
         "targeting the late-summer and early-fall crop, since midsummer heat pushes bud stalks "
         "up too fast and quality suffers."),
  note_s=("The plant often survives here and sometimes does not, which is exactly what marginal "
          "means: Oregon State's vegetable breeder describes western Oregon artichokes as "
          "short-lived perennials that need cutting back and mulching, and warns that in colder "
          "winters they may not survive even mulched. That matches the physiology, since "
          + _MECH_CROWN + " and zone 8 winters reach into that range. Plan on three to four "
          "productive years at best, then divide or replant."),
  note_b=("One of the better climates for this crop outside California. Plant in spring, cut the "
          "plant back and mulch it heavily in fall, and it will often come back for another "
          "year or three. Harvest in September and October. A hard winter will still kill it, so "
          "do not be surprised."))

C("pnw", "9", "perennializes", PNW_Z9,
  "Apr 1 - Jun 15 (transplants or crown divisions, one-time planting)", "Sep - Nov",
  "adjacent_zone_derived", _PNW_S,
  notes=("The warm maritime edge, in the Puget lowlands and the immediate coast. Set plants in "
         "spring, cut back and mulch after the fall harvest, and the same crowns carry on."),
  note_s=("Winter minima on this ground stay above the roughly 15°F line where crowns are "
          "lost even under mulch, so the planting persists rather than needing yearly renewal, "
          "and the cool maritime summer avoids the heat that ends the crop inland. No source "
          "addresses zone 9 separately from zone 8 here, so the rating is extended from the "
          "adjacent zone within the same region on the basis of winter minimum alone."),
  note_b=("This is good artichoke ground. Plant once, cut back and mulch each fall, and harvest "
          "each September through November for several years before dividing the clump."))

# ======================= ca_interior (z8-9) =======================
_CAI_S = ["uc_mg_t132", "uc_anr_7221", "tamu_eht065"]
_CAI_WATER = (
    "The thing that decides it here is summer water, not summer heat acting on its own. Artichoke "
    "is deep-rooted and wants steady moisture whenever it is growing or carrying buds, and Texas "
    "A&M spells out how the two are connected: in summer, irrigation keeps temperatures down "
    "inside the crop canopy and that is what stops buds opening early. A full-sized plant asked "
    "to hold a large canopy through a valley summer is a serious and unforgiving water bill. Meet "
    "it and the same crowns carry on for several years; miss it and the plant is gone. That is "
    "why one garden on this ground has a standing clump and the garden next door lost theirs.")
C("ca_interior", "8", "marginal", CAINT_Z8,
  "Jul 1 - Jul 31 (transplants, shoots, or root divisions)", "Nov - Mar",
  "extension_regional_guide", _CAI_S,
  start_indoors="May 1 - Jun 15",
  notes=("University of California's statewide planting table gives the interior valleys a July "
         "window, and its footnote is explicit that artichoke goes in as transplants, shoots or "
         "roots rather than seed. Plants size up through fall and crop through the cool months, "
         "then hold through the following summer on irrigation rather than being pulled."),
  note_s=("A short-lived perennial on this ground rather than either a one-season annual or a "
          "permanent bed. " + _CAI_WATER + " University of California sources split four ways on "
          "this region, from a July set-out to a December sowing with a March transplant, and one "
          "UC home-garden leaflet says outright that planting is not recommended in the interior "
          "valleys. Two of them do call it an annual, but the same sheet that says so also notes "
          "the plant may winter over wherever temperatures stay above 25°F, and the leaflet that "
          "declines to recommend it is specifically about perennial root-division culture rather "
          "than about the crop. No source publishes how long a stand actually lasts in the "
          "Central Valley. The only sourced figure, five to ten years, describes commercial "
          "coastal California and is longer than this ground gives, so expect fewer years than "
          "that and divide or replace when yield falls off."),
  note_b=("Plant in July, which feels wrong but is right: the plants grow through fall and give "
          "you buds through the cool months. You do not have to pull them afterwards. The catch "
          "is water, because carrying a big plant through a valley summer takes a lot of it, and "
          "that summer watering is also what keeps the buds from opening too fast. On steady deep "
          "irrigation, ideally drip, the same plants will crop for several years. Let them dry "
          "out one hot week and you will be starting over."))

C("ca_interior", "9", "marginal", CAINT_Z9,
  "Jul 1 - Jul 31 (transplants, shoots, or root divisions)", "Nov - Mar",
  "extension_regional_guide", _CAI_S,
  start_indoors="May 1 - Jun 15",
  notes=("The valley floor proper. Same July planting, with harvest opening a little earlier and "
         "running through winter into early spring, and the same summer carry on irrigation."),
  note_s=("The same short-lived perennial pattern, and the water demand is sharper on the valley "
          "floor because the summers are hotter and longer. " + _CAI_WATER + " Winter is not the "
          "constraint here: it is mild enough that a plant left in the ground comes through it "
          "easily. What a surviving plant then faces is the next valley summer, and that, not the "
          "frost, is what sets how long a stand lasts. No Central Valley figure for stand life is "
          "published anywhere, so none is given."),
  note_b=("Set plants out in July for a winter and early-spring harvest, and keep them. They will "
          "crop again for several years if you water them properly through summer, which on this "
          "ground means deep, regular irrigation rather than an occasional soak. Summer drought "
          "is what kills them here, not winter."))

# ======================= ca_north_coast (z9-10) -- the home ground =======================
_CNC_S = ["uc_mg_t132", "uc_anr_7221", "uc_ipm"]
C("ca_north_coast", "9", "perennializes", CANORTH_Z9,
  "Aug 1 - Dec 31 (root divisions or offshoots, one-time planting)", "Nov - May",
  "extension_regional_guide", _CNC_S,
  notes=("The classic coastal system. Plant rooted offshoots or crown divisions from late summer "
         "into winter, six to eight inches deep. Peak production runs March into May, and cutting "
         "the plants back after the spring peak brings a second, lighter crop in late fall."),
  note_b=None, note_s=None)

C("ca_north_coast", "10", "perennializes", CANORTH_Z10,
  "Aug 1 - Dec 31 (root divisions or offshoots, one-time planting)", "Nov - May",
  "extension_regional_guide", _CNC_S,
  notes=("The same coastal cycle on the warmer, more frost-free strip, with harvest opening a few "
         "weeks earlier. Cut back after the spring peak and withhold water for several weeks to "
         "time the fall crop."))

# ======================= ca_south_coast (z9-11) =======================
_CSC_S = ["uc_mg_t132", "uc_anr_7221"]
C("ca_south_coast", "9", "perennializes", CASOUTH_Z9,
  "Jul 1 - Aug 31 (transplants, shoots, or root divisions, one-time planting)", "Oct - Apr",
  "extension_regional_guide", _CSC_S,
  notes=("Southern coastal California runs on a winter-cropping calendar. Set plants in midsummer "
         "and harvest from October through April, which is why the region supplies the winter "
         "market. University of California sources give this district three different windows, "
         "from May to July, July to August, and October to December; the midsummer setting is the "
         "one two of the three support."))

C("ca_south_coast", "10", "perennializes", CASOUTH_Z10,
  "Jul 1 - Aug 31 (transplants, shoots, or root divisions, one-time planting)", "Oct - Apr",
  "extension_regional_guide", _CSC_S,
  notes=("The same winter-cropping cycle on the warmest coastal ground. Frost is rare enough that "
         "bud damage is the exception rather than the rule."))

C("ca_south_coast", "11", "perennializes", CASOUTH_Z11,
  "Jul 1 - Aug 31 (transplants, shoots, or root divisions, one-time planting)", "Oct - Apr",
  "adjacent_zone_derived", _CSC_S,
  notes=("Essentially frost-free coastal ground. Extended from the adjacent zone within the same "
         "region, under a University of California window whose stated scope is San Luis Obispo "
         "County and south with no zone exclusion."))

# ======================= ca_desert (z9-11) =======================
_CD_S = ["uc_anr_7221", "ucce_imperial_artichoke"]
C("ca_desert", "9", "marginal", CADESERT_Z9,
  "Aug 15 - Oct 15 (transplants or direct-sown seed, replant each year)", "Dec - Apr",
  "extension_regional_guide", _CD_S,
  notes=("The Imperial and Coachella valley system, and it is strictly annual. Fields go in from "
         "late August through October and crop from December through April. University of "
         "California Cooperative Extension in Imperial County notes that desert artichokes are "
         "started from direct-sown seed or from transplants, with almost none raised from the "
         "mother-plant cuttings the coast relies on."),
  note_s=("Rated as an annual rather than perennializing because the planting genuinely does not "
          "carry over: this is a one-season crop pulled before summer, and University of "
          "California Cooperative Extension states that desert artichokes are seldom marketable "
          "after early April because warm weather toughens the buds. " + _MECH_HEAT.capitalize()
          + ", and a desert summer is far past that line. The winter crop itself is reliable and "
          "commercially important, so this is a limit on persistence, not on productivity."),
  note_b=("Plant in late summer or early fall for a winter and early-spring harvest, and pull the "
          "plants when the weather turns hot. This is a cool-season crop here, the opposite of "
          "how most people picture artichokes."))

C("ca_desert", "10", "marginal", CADESERT_Z10,
  "Aug 15 - Oct 15 (transplants or direct-sown seed, replant each year)", "Dec - Apr",
  "extension_regional_guide", _CD_S,
  notes=("The same low-desert winter system on the valley floor."),
  note_s=("Same annual cycle and same reason for the rating as the adjacent zone: the crop is "
          "productive through winter and finished by the heat, so the planting does not persist. "
          + _MECH_HEAT.capitalize() + "."),
  note_b=("A winter crop here. Plant in early fall, pick from December through spring, then "
          "start over next fall."))

C("ca_desert", "11", "unsuitable", ALL_GROWING,
  None, None, "vacant_ground", _CD_S,
  note_s=("No California desert ground actually reaches zone 11, so this cell is effectively "
          "vacant rather than a real growing situation. Where a climate is both frost-free and "
          "extremely hot, artichoke gets neither the cool spell that starts bud formation nor "
          "relief from the heat that ruins the buds it does set. Cooler desert ground a zone or "
          "two down does grow a good winter crop; see the zone 9 and zone 10 entries."),
  note_b=("There is no real California desert ground in this zone, so there is nothing to plant "
          "here. If you are in the low desert, look at the zone 9 or zone 10 guidance instead, "
          "where artichoke is a genuine winter crop."))

# ======================= low_desert_az (z9-10) =======================
_LD_S = ["uariz_ext_az1005", "uariz_ext_az1615"]
C("low_desert_az", "9", "marginal", LOWDESERT_Z9,
  "Jan 15 - Mar 31 (transplants, replant each year)", "May - Jun",
  "extension_regional_guide", ["uariz_ext_az1005"],
  start_indoors="Nov 1 - Dec 14",
  notes=("University of Arizona's Maricopa County calendar marks artichoke for transplanting from "
         "mid January through March, with seed sown from early November to mid December, and "
         "gives four to six months to harvest."),
  note_s=("The two Arizona low-desert calendars genuinely differ, and this cell follows the "
          "cooler Phoenix-side one rather than averaging them. Artichoke crops well here as a "
          "cool-season annual and then stops: " + _MECH_HEAT + ", and a Phoenix summer is far "
          "past that. The planting does not persist through it."),
  note_b=("Set transplants out in late winter for a late-spring harvest, then let the plants go "
          "when summer arrives. Start seed indoors in November if you are growing your own."))

C("low_desert_az", "10", "marginal", LOWDESERT_Z10,
  "Sep 1 - Oct 31 (transplants or direct-sown seed, replant each year)", "May - Jun",
  "extension_regional_guide", ["uariz_ext_az1615"],
  notes=("University of Arizona's Yuma calendar puts artichoke in from September through October "
         "and harvests it in May and June, running the plant through the whole mild winter."),
  note_s=("The Yuma end of the low desert plants in fall rather than late winter, which is the "
          "opposite end of the Arizona range and is followed here because Yuma is this zone's "
          "ground. One caution on the source: its header says the dates are for seed unless "
          "otherwise noted, but the same table gives asparagus an eight-inch planting depth, "
          "which is a crown depth, so the seed-unless-noted rule is not perfectly applied to "
          "perennials in that chart. Either way the crop is finished by early summer, since "
          + _MECH_HEAT + "."),
  note_b=("Plant in early fall for a late-spring harvest. The plants grow all winter, crop in "
          "May and June, and are done when the real heat comes."))

# ======================= se_gulf (z8-10) =======================
_SG_S = ["lsu_agcenter_3634", "tamu_eht065", "uf_ifas_hs1289"]
C("se_gulf", "8", "marginal", SEGULF_Z8,
  "Oct 1 - Nov 10 (nursery or own-grown transplants, replant each year)", "Mar - May",
  "extension_regional_guide", _SG_S,
  start_indoors="Jul 15 - Aug 15",
  notes=("LSU AgCenter plants artichoke from October into early November, setting a containerized "
         "transplant no deeper than its root ball and spacing plants at least 3 feet apart. If you "
         "are raising your own, sow about twelve weeks ahead, around mid July for an October "
         "planting. Plants grow through the mild winter and crop in spring."),
  note_s=("Louisiana is the only Gulf state whose extension service covers artichoke at all, since "
          "Georgia, Alabama, Mississippi and South Carolina do not list it, and LSU is candid that "
          "the planting does not persist: technically a perennial, but often lost over the summer "
          "to disease, so it advises growing it long-term only if you will tend it through the "
          "summer and otherwise simply treating it as an annual. Winter is not the constraint in "
          "this band; unlike peninsular Florida these winters bank the 250 to 500 hours below 50°F "
          "that bud initiation needs, so the crop sets without artificial help. Summer heat and "
          "humidity are what end it."),
  note_b=("Plant in October or early November for a spring harvest, and set the plant no deeper "
          "than the pot it came in. Most plants die out over the following summer from disease, so "
          "plan to replant each autumn rather than keeping a permanent bed."))

C("se_gulf", "9", "marginal", SEGULF_Z9,
  "Oct 1 - Nov 10 (nursery or own-grown transplants, replant each year)", "Feb - May",
  "extension_regional_guide", _SG_S,
  start_indoors="Jul 15 - Aug 15",
  notes=("The same LSU fall-planted system on milder ground, with harvest opening a few weeks "
         "earlier."),
  note_s=("Same cycle and the same limit as the zone 8 side, on LSU's guidance, though the "
          "cool-hour supply is thinner here so expect a less uniform set. LSU's framing is to "
          "treat the plant as an annual unless you intend to tend it through the summer, because "
          "summer disease rather than winter cold is what finishes it. LSU also says artichoke "
          "thrives in zone 7 and higher, but that is a claim about growing well rather than about "
          "the planting surviving, and the same page qualifies it two paragraphs later."),
  note_b=("A fall-planted, spring-harvested crop. Replant every autumn. Do not expect a permanent "
          "bed to survive the summer."))

C("se_gulf", "10", "survives_no_fruit", TROPICS_FL,
  "Oct 1 - Nov 15 (transplants, foliage only)", None,
  "extension_regional_guide", ["uf_ifas_vh021", "uf_ifas_hs1289"],
  notes=("Set transplants from October to mid November, which is UF/IFAS's own Florida window and "
         "the last date it gives for getting seedlings into the field. The rosette fills out "
         "through the cool months and is finished by the hot, wet summer."),
  note_s=(_ORN_S + " Two things are specific to this end of the Gulf rather than general. The "
          "planting is a single cool season and not a standing one, because UF/IFAS recommends "
          "the October to May cycle precisely to dodge a summer whose heat and wet drive disease "
          "and pests, so expect to replant rather than to keep a permanent clump. And the "
          "documented absence is real: artichoke is missing entirely from the Florida vegetable "
          "gardening guide, whose alphabetical planting table runs straight past where it would "
          "sit, and a UF/IFAS county guide footnotes that globe artichokes, asparagus and rhubarb "
          "are not well adapted to Florida. Read that as the food verdict it is, not as a verdict "
          "on whether the plant will grow."),
  note_b=(_ORN_B + " Plant in October or early November and enjoy the leaves through winter and "
          "spring. The summer heat and rain will finish the plant off, so start again next fall "
          "if you liked it."))

# ======================= rgv (z9-10) =======================
_RGV_S = ["tamu_agrilife", "tamu_eht065"]
C("rgv", "9", "marginal", RGV_Z9,
  "Sep 1 - Oct 31 (transplants or crown divisions, replant each year)", "Jan - Mar",
  "mechanism_derived_no_regional_source", _RGV_S,
  start_indoors="Aug 1 - Aug 31",
  notes=("No Texas publication gives a Rio Grande Valley artichoke date. This window follows the "
         "Texas A&M statewide fall system, shifted earlier for a subtropical winter, and crops "
         "before the spring heat."),
  note_s=("Texas A&M covers artichoke statewide but every Valley-specific document omits it, "
          "including both editions of the Lower Rio Grande Valley vegetable crops guide and the "
          "Valley homeowner vegetable guide. The one Texas sentence touching this coast says "
          "a few home gardeners on the Texas coast do grow it, from crown divisions, seeing a first "
          "harvest roughly a year later, and it gives no month. Rated a workable annual rather than "
          "unsuitable on the strength of that positive statement, but the cool hours here are "
          "few and " + _MECH_DEVERN + ", so expect an uneven set."),
  note_b=("Texas extension does not publish a Valley planting date for artichoke, so this is a "
          "trial. Plant in early fall and hope for a late-winter crop. Some plants may not form "
          "buds at all, because our winters barely get cool enough to trigger them."))

C("rgv", "10", "marginal", RGV_Z10,
  "Sep 1 - Oct 31 (transplants or crown divisions, replant each year)", "Jan - Mar",
  "mechanism_derived_no_regional_source", _RGV_S,
  start_indoors="Aug 1 - Aug 31",
  notes=("The same derived fall-set cycle on the warmest Valley ground."),
  note_s=("Warmer still, and the cool-hour supply that drives bud formation is correspondingly "
          "thinner, so a larger share of plants may stay vegetative. No Texas source addresses "
          "this ground for the crop. " + _MECH_HEAT.capitalize() + ", which closes the season "
          "early."),
  note_b=("Worth a try rather than a plan. Plant in early fall for a possible late-winter "
          "harvest, and accept that some plants will make leaves and never make buds."))

# ======================= fl_peninsula (z10-11) =======================
_FL_S = ["uf_ifas_vh021", "uf_ifas_hs1289"]
_FL_NOTES = ("Set transplants from October to mid November, the window UF/IFAS publishes for "
             "Florida and the last date it gives for getting seedlings into the field. The "
             "rosette fills out through the cool months and the hot, wet summer ends it.")
_FL_S_EXTRA = (
    " This is UF/IFAS's own ground, so the evidence here is direct rather than borrowed. The "
    "planting is a single cool season rather than a standing one, because the recommended "
    "October to May cycle exists specifically to dodge a summer whose heat and wet drive disease "
    "and pests. Artichoke is also absent entirely from the Florida vegetable gardening guide, "
    "whose alphabetical planting table runs straight past where it would sit, and a UF/IFAS "
    "county guide footnotes that globe artichokes, asparagus and rhubarb are not well adapted to "
    "Florida. That is a verdict on the crop, and it is correct; it is not a verdict on whether "
    "the plant will grow, and the same service's trial answers that question the other way.")
_FL_B_EXTRA = (" Plant in October or early November and enjoy the leaves through winter and "
               "spring. Summer heat and rain will finish the plant off, so start again next fall "
               "if you liked it.")
for _z in ("10", "11"):
    C("fl_peninsula", _z, "survives_no_fruit", TROPICS_FL,
      "Oct 1 - Nov 15 (transplants, foliage only)", None,
      "extension_regional_guide", _FL_S,
      notes=_FL_NOTES,
      note_s=_ORN_S + _FL_S_EXTRA,
      note_b=_ORN_B + _FL_B_EXTRA)

# ======================= hawaii_tropical (z10-13) =======================
# NOT the Florida calendar. Florida's summer `season_over` is a sourced event -- UF/IFAS ends the
# planting there deliberately. Hawaii has no equivalent break, so the strip runs `growing` all
# year and the plant simply persists. Copying Florida's shape here would have imported a summer
# die-off that no source claims for Hawaii, which is the R6 blanket-note error in calendar form.
_HI_S = ["uf_ifas_hs1289"]
for _z in ("10", "11", "12", "13"):
    C("hawaii_tropical", _z, "survives_no_fruit", TROPICS_HI,
      "Nov 1 - Feb 28 (transplants, foliage only)", None,
      "mechanism_derived_no_regional_source", _HI_S,
      notes=("Plant out in the cooler half of the year, which makes establishment easier rather "
             "than making budding possible. Once rooted the rosette simply persists, since "
             "nothing in this climate ends it."),
      note_s=(_ORN_S + " Two caveats specific to here. No Hawaii extension source addresses "
              "artichoke at all, so both the rating and the window rest on the physiology plus "
              "the nearest documented parallel, which is peninsular Florida. And the planting "
              "window is a convenience rather than a requirement: the plant is not waiting for a "
              "season, it simply establishes more easily out of the hottest months, so a "
              "November to February setting is a preference and not a deadline. Unlike Florida "
              "there is no hot wet break that ends the planting, so expect the rosette to persist "
              "and to keep making leaves indefinitely."),
      note_b=(_ORN_B + " Plant in the cooler months if you can, though it is not critical here. "
              "Once it takes hold it will just keep growing."))


def total_cells():
    return sum(len(v) for v in CELLS.values())


if __name__ == "__main__":
    # Mirrors A47/A48 exactly, including where they DIVERGE: `unsuitable` is exempt from both,
    # `survives_no_fruit` is exempt from harvest only (no food to promise) and still owes a
    # plant_out (someone may want the foliage). Keep this in step with the two gates -- a stale
    # self-check that says "clean" while the gate says otherwise is worse than no self-check.
    NO_PLANT_OUT = {"unsuitable"}
    NO_HARVEST = {"unsuitable", "survives_no_fruit"}
    print(f"regions {len(CELLS)}  cells {total_cells()}")
    bad = 0
    for r, zs in CELLS.items():
        for z, c in zs.items():
            s = c["suitability"]
            flag = ""
            if s not in NO_PLANT_OUT and not c["plant_out"]:
                flag = "  !! MISSING plant_out (A47)"
            elif s not in NO_HARVEST and not c["harvest"]:
                flag = "  !! MISSING harvest (A48)"
            elif s in NO_HARVEST and c["harvest"]:
                flag = "  !! harvest on a no-food cell (A48 would not catch this)"
            bad += bool(flag)
            print(f"  {r}.{z:<3} {s:<18} {str(c['plant_out'])[:46]:<46}"
                  f" {str(c['harvest'])[:16]:<16}{flag}")
    import collections
    print("  suitability:", dict(collections.Counter(
        c["suitability"] for zs in CELLS.values() for c in zs.values())))
    print(f"  field-floor problems: {bad}")


# =============================================================================================
# ANNUAL_ONLY -- applied 2026-07-28, after plant-app landed the display state
# =============================================================================================
#
# 22 of the 25 `marginal` cells are not really "marginal" at all: artichoke crops WELL on them
# and simply does not persist, so the grower replants each season. `marginal` answers "does the
# planting persist" with a shrug, which undersells a dependable annual crop. `annual_only` says
# the true thing, and it is the value the arc wanted at cert and declined ONLY because no
# renderer knew it (design-decisions B.6, open_findings `artichoke-annual-only-suitability-
# declined`). plant-app now renders it with its own display state and a "Replant each year" flag
# (commit bc2c809), so the block is gone.
#
# THE THREE THAT STAY `marginal` ARE THE POINT OF DOING THIS BY HAND. Not every non-persistent
# cell is an annual one:
#   pnw z8          -- a SHORT-LIVED PERENNIAL. Oregon State's breeder describes western Oregon
#                      artichokes as short-lived perennials needing cut-back and mulch, good for
#                      three to four productive years. The plant IS carried over; it just does
#                      not last. That is genuinely marginal, not annual.
#   ca_interior z8  -- SHORT-LIVED PERENNIAL limited by summer WATER DEMAND (see the calendar
#   ca_interior z9     note above). Met, the same crowns crop for several years; missed, the
#                      plant dies. Persistence that depends on the gardener is the textbook
#                      marginal case, and calling it annual would erase the reframe this arc
#                      made deliberately two passes ago.
# Flattening all 25 would have been one line and would have re-broken ca_interior.
ANNUAL_ONLY_CELLS = {
    ("northern_tier", "3"), ("northern_tier", "4"), ("northern_tier", "5"),
    ("northern_tier", "6"), ("northern_tier", "7"),
    ("mid_atlantic", "7"), ("mid_atlantic", "8"),
    ("mid_south", "7"), ("mid_south", "8"),
    ("warm_arid", "8"),
    ("nevada", "8"), ("nevada", "9"), ("nevada", "10"),
    ("utah_dixie", "8"),
    ("ca_desert", "9"), ("ca_desert", "10"),
    ("low_desert_az", "9"), ("low_desert_az", "10"),
    ("se_gulf", "8"), ("se_gulf", "9"),
    ("rgv", "9"), ("rgv", "10"),
}

# CROSS-CHECK, not a derivation. The explicit set above is the source of truth (a substring rule
# would drift silently the first time someone rewords a plant_out), but every cell in it must
# ALSO carry the arc's own "replant each ..." marker in its plant_out, and no cell outside it may.
# If those two ever disagree, the data and the intent have come apart and this file refuses to load.
def _apply_annual_only():
    derived = {(rk, z) for rk, zs in CELLS.items() for z, c in zs.items()
               if c["suitability"] == "marginal" and "replant each" in (c["plant_out"] or "")}
    assert derived == ANNUAL_ONLY_CELLS, (
        f"annual_only set disagrees with the plant_out marker.\n"
        f"  in set but not marked: {sorted(ANNUAL_ONLY_CELLS - derived)}\n"
        f"  marked but not in set: {sorted(derived - ANNUAL_ONLY_CELLS)}")
    for rk, z in ANNUAL_ONLY_CELLS:
        assert CELLS[rk][z]["suitability"] == "marginal", f"{rk}.{z} is not marginal"
        assert CELLS[rk][z]["suitability_note_seasoned"], f"{rk}.{z} has no seasoned note"
        CELLS[rk][z]["suitability"] = "annual_only"


_apply_annual_only()
