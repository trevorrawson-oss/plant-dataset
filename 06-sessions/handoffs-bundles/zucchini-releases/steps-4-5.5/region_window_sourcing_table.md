# Authored region windows (T1, A5 per-region). DTM 50-65 mid 55. Fall crop = count back DTM+~14d buffer from first frost.

## GEOMETRY MAP (per-region SOURCE finding; mixed, keyed continuous-vs-split)
- CONTINUOUS (succession_continuous): northern_tier(3-7), ca_interior(8-9), ca_north_coast(9-10), ca_south_coast(9-10), warm_arid(8)
- SPLIT (succession_spring+succession_fall, summer heat_pause): se_gulf(8-9), ca_desert(9-10), low_desert_az(9)
- INVERTED/bounded-continuous (succession_continuous, summer season_over): fl_peninsula(10-11)
- year_round vs bounded: hawaii_tropical(11) -> bounded-continuous default (NO CTAHR continuous statement found); flag for CC

## northern_tier (CONTINUOUS) -- UMN (primary) + UMD + iastate/cornell corroboration
Direct-sow after last frost once soil >=70F (UMN). start_indoors 3-4wk before last frost ONLY to gain time (short season -> z3-5 use it).
plant_out: after last_frost. harvest_start ~+55d (DTM mid). Fall replacement sown counting back from first frost (SVB/PM).
- z3 LF May15/FF Sep15 (120d): start_indoors ~Apr24; plant_out Jun1-Jun21 (soil-warm late); harvest Jul20-Sep10. (single continuous; succession tight)
- z4 LF May1/FF Oct1: SI Apr10; plant_out May20-Jun10; harvest Jul15-Sep25.
- z5 LF Apr15/FF Oct15: SI ~Mar25; plant_out May10-Jun20; harvest Jun30-Oct8.
- z6 LF Apr1/FF Oct31: plant_out Apr25-Jul1; harvest Jun20-Oct24. (SI optional)
- z7 LF Mar15/FF Nov15: plant_out Apr10-Jul15; harvest Jun5-Nov8. (SI optional)
succession_continuous: spring->mid/late-summer sowings (3wk cadence), capped by fall-frost runway (count back DTM).

## se_gulf (SPLIT) -- UGA B577 (Squash,bush 50-55d: SPRING Apr1-May15, FALL Aug1-20, middle GA) + C943
zone adj: z8 (~N GA edge) spring ~2wk later/fall ~2wk earlier; z9 (~S GA) spring ~2wk earlier/fall somewhat later.
- z8 LF Feb15/FF Dec1: spring plant_out Apr1-May15; spring harvest May25-Jul10 (heat wall + SVB/virus). FALL plant_out Aug1-Aug20; fall harvest Sep25-Nov5. heat_pause ~Jun15-Jul (mid-summer virus/heat gap). 
  NOTE: z8 LF is Feb15 in our table but UGA middle-GA spring is Apr; the Apr window is the SOURCE (soil-warm + frost-safe), NOT LF+offset. resolved_from records frost dates; window is source-set (A5).
- z9 LF Jan31/FF Dec15: spring plant_out Mar15-Apr30 (south GA earlier); spring harvest May5-Jun20. FALL plant_out Aug15-Sep5; fall harvest Oct10-Nov20.
succession_spring + succession_fall comma-lists.

## ca_interior (CONTINUOUS) -- UC ANR Pub 7245 + Sacramento/Santa Clara/Marin MG
Plant when soil >=70F (Sac MG); seed indoors March, set out mid-Apr through June, some to July (Marin/SC MG). Production through summer, taper fall on virus/whitefly. NO mid-summer no-plant gap -> continuous.
- z8 LF Feb15/FF Dec1: plant_out Apr1-Jul1; harvest May25-Oct (long). SI Mar.
- z9 LF Jan31/FF Dec15: plant_out Mar15-Jul1; harvest May10-Oct.
succession_continuous (Apr->early-July sowings, 3wk).

## ca_north_coast (CONTINUOUS, heat-LIMITED) -- Marin MG "Squash-Summer" (seed indoors Mar, plant mid-Apr-June, some to July; bears until fall cool; nights>55F) + UC ANR T13.2 N/NCoast
- z9 LF Jan31/FF Dec15: plant_out May1-Jul1 (cool coast, later start); harvest Jun25-Oct.
- z10 LF Jan15/FF Dec31: plant_out Apr15-Jul1; harvest Jun10-Nov.
succession_continuous. NO heat_pause (marine cool, not heat-stalled).

## ca_south_coast (CONTINUOUS) -- UC ANR T13.2 SCoast + LA County MG (wait til end Apr for squash) + Marin shape
- z9 LF Jan31/FF Dec15: plant_out Apr15-Jul1; harvest Jun10-Nov.
- z10 LF Jan15/FF Dec31: plant_out Apr1-Jul15; harvest May25-Nov (mild long).
succession_continuous. NO heat_pause.

## ca_desert (SPLIT) -- UC ANR 7245 (desert spring planted Dec-Jan; acreage reduced fall on virus/whitefly) + UC ANR T13.2 Desert Valleys
Imperial/Coachella: early-spring main crop, summer too hot (set/virus), fall crop.
- z9 LF Jan31/FF Dec15: spring plant_out Feb1-Mar15 (early, beat heat); spring harvest Apr1-Jun15 (heat ends it). FALL plant_out Sep1-Sep30; fall harvest Oct25-Dec10. heat_pause ~Jun15-Aug.
- z10 LF Jan15/FF Dec31: spring plant_out Jan15-Mar1; spring harvest Mar15-Jun. FALL plant_out Sep1-Oct1; fall harvest Oct25-Dec. heat_pause Jun-Aug.
succession_spring + succession_fall.

## warm_arid (CONTINUOUS at z8) -- NMSU Circular 457 / Dona Ana MG (Las Cruces) + TAMU far-west TX
S NM / W TX z8: single long warm season after spring frost, through to fall frost. (Higher elevation than low desert; not the Sonoran two-season; treat as continuous unless NMSU shows a split. NMSU statewide table = spring planting; no clean mid-summer no-plant gap documented for z8 high-desert -> continuous, like green-beans warm_arid z8 BRIDGE.)
- z8 LF Feb15/FF Dec1 (Las Cruces ~ Mar last frost): plant_out Apr1-Jun15 (soil-warm); harvest May25-Oct. SI Mar.
succession_continuous. (Flag: if CC's NMSU read shows a desert-style summer gap, may split; I read continuous.)

## low_desert_az (SPLIT) -- U of A AZ1005 Maricopa (Squash,Summer 60-90d: spring S Feb15-Mar15, fall S Aug-Sep) + AZ1615 Yuma + UA low-desert survival page
- z9 LF Jan31/FF Dec15: spring plant_out Feb15-Mar15 (can run to mid-Apr per UA survival page); spring harvest Apr10-Jun (heat/whitefly ends). FALL plant_out Aug15-Sep15; fall harvest Oct10-Nov25. heat_pause ~Jun-Aug (May-Aug too hot; whitefly).
succession_spring + succession_fall.

## fl_peninsula (INVERTED, bounded-continuous) -- UF/IFAS Gardening Solutions Summer Squash (N FL Feb-Apr + Aug-Sep; S/Central earlier-fall/winter) + VH021 + Manatee agent (warm Apr-Oct, summer Jun-Aug OFF-season)
Central/South FL (z10-11): grow the cool half, summer (Jun-Aug) is season_over.
- z10 LF Jan15/FF Dec31 (central): plant_out windows Feb-Mar + Aug15-Oct (two sowing windows, continuous cool-half growing); harvest spring Mar-Jun, fall Oct-Dec/Jan. summer Jun-Aug season_over.
  Treat as succession_continuous over the cool half (one inverted continuous window wrapping the winter), summer season_over (NOT heat_pause -- frost-free region uses season_over per locked rule).
- z11 LF none/FF none (south): plant_out Sep-Mar (winter growing season); harvest Nov-May; summer Jun-Aug season_over. resolved_from null (frost-free).
succession_continuous. resolved_from null at z11.

## hawaii_tropical (BOUNDED-CONTINUOUS default; z11 frost-free) -- UH CTAHR (B-91 / production guides)
No CTAHR statement found asserting CONTINUOUS year-round zucchini. Default = bounded-continuous, NOT year_round (onion/zinnia locked rule: frost-free z11 alone insufficient). Wet-season/pest caveat in notes.
- z11 LF none/FF none: plant_out bounded-continuous (state honestly: grown much of the year at elevation/drier leeward, pest/wet-season pressure); harvest year-following. resolved_from null.
succession_continuous. resolved_from null. calendar_basis cell note: NOT year_round (climate+source: no CTAHR continuous statement).
*** FLAG FOR CC: if CC's CTAHR fetch finds an explicit continuous/year-round zucchini statement, upgrade to year_round + log blocks_launch:false open finding. Default authored = bounded-continuous. ***
