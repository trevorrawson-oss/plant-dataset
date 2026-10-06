"""PLA-673 part B2 round 2 packets (2026-10-06): pepper Phytophthora entry, parsnip's three seasoned leaves, and the
beginner siblings of all 10 B2 leaves. Every quote is proven against its hashed bytes (build_packets.locate); verdicts
are by reading. Nothing authored."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_packets as bp  # noqa: E402

U = {
    "ncsu_pb": ("https://content.ces.ncsu.edu/phytophthora-blight-of-peppers", "NC State, Phytophthora Blight of Peppers (Quesada-Ocampo; 2018, rev. 2023) [ncsu_ext_phytophthora_blight_peppers, PROPOSED mint]"),
    "clem_pep": ("https://hgic.clemson.edu/factsheet/pepper/", "Clemson HGIC Pepper [clemson_hgic]"),
    "umn_pep": ("https://extension.umn.edu/vegetables/growing-peppers", "UMN Growing peppers [umn_ext]"),
    "clem_egg": ("https://hgic.clemson.edu/factsheet/eggplant-insect-pests-diseases/", "Clemson HGIC Eggplant insect pests & diseases [clemson_hgic]"),
    "umass": ("https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/carrot-parsnip-itersonilia-canker", "UMass Carrot & Parsnip, Itersonilia Canker (2013) [umass_ext_itersonilia_canker, PROPOSED mint]"),
    "umn_cp": ("https://extension.umn.edu/vegetables/growing-carrots-and-parsnips", "UMN Growing carrots and parsnips [umn_ext]"),
    "clem_root": ("https://hgic.clemson.edu/factsheet/carrot-beet-radish-parsnip/", "Clemson HGIC Carrot, Beet, Radish & Parsnip [clemson_hgic]"),
    "rhs": ("https://www.rhs.org.uk/vegetables/parsnips/grow-your-own", "RHS Parsnips: grow your own [rhs]"),
    "c1206": ("https://fieldreport.caes.uga.edu/publications/C1206/homegrown-pumpkins/", "UGA C1206 Homegrown Pumpkins [uga_c1206_homegrown_pumpkins]"),
    "umn_pk": ("https://extension.umn.edu/vegetables/pumpkins-and-winter-squash", "UMN Pumpkins and winter squash [umn_ext]"),
}
SHA = {k: next(s for s, us in bp.MAN.items() if u in us) for k, (u, _l) in U.items()}

# ---------------------------------------------------------------- reusable quotes
NC = {
    "pathogen": "phytophthora blight is caused by the fungal-like oomycete pathogen phytophthora capsici ( figure 1 ).",
    "oospores": "the pathogen may overwinter in the soil when it forms oospores, which are survival structures that can persist for over 10 years.",
    "water_spread": "the pathogen can spread rapidly via water and can contaminate irrigation ponds and creeks.",
    "hosts": "the host range of p. capsici is very broad including bell pepper, hot pepper, eggplant, tomato, snap bean, lima bean, and most cucurbits.",
    "rotation_weak": "the broad host range of p. capsici significantly reduces the efficacy of crop rotation as a control method, however, cereal crops (corn, wheat) are not hosts of p. capsici .",
    "soil_line": "since p. capsici is a soilborne pathogen, symptoms usually first develop at the soil line in the roots and crown, however, infection can occur at any plant part where water splashes soil onto the plant.",
    "crown_fruit": "the most common symptoms on peppers are crown rot and fruit rot.",
    "wilt": "under wet conditions, disease tends to manifest itself as wilting of the plants ( figure 2 ) followed by plant death.",
    "girdle": "as the disease progresses crown lesions become dark brown and extend upward to girdle the stem causing plant death ( figure 3 ).",
    "fruit_splash": "pepper fruits can become infected when rain and overhead irrigation splash infested soil onto emerging fruits.",
    "fruit_rot": "fruit rot appears as water-soaked areas that eventually become covered with white powdery to cottony mold ( figure 4 ).",
    "conditions": "optimal conditions for disease development are: excessive rainfall or overhead irrigation saturated soils warm temperatures (75 to 90°f)",
    "debris": "culls and debris can also become a significant source of inoculum that can infest the soil and surface irrigation water if culls are next to irrigation ponds or creeks.",
    "resistant": "plant resistant varieties.",
    "resistant_some": "there are some bell, sweet, and hot peppers with moderate resistance to p. capsici.",
    "drainage": "plant in field with good drainage and even terrain that will not promote having standing water for prolonged periods of time.",
    "raised": "use raised beds and plastic mulch whenever possible.",
    "drip": "irrigate moderately from a well via drip, and avoid overhead irrigation especially once fruit is present.",
    "remove": "remove diseased fruit or plants away from the field.",
    "culls": "do not leave culls in the field or near surface irrigation water sources (ponds, creeks).",
    "rotate_cereals": "rotate to crops that are not hosts of p. capsici (cereals).",
    "home": "home gardeners have no chemical control options that are effective and need to rely completely on host resistance and cultural strategies for disease control.",
    "organic": "the only omri labeled active ingredients that have some efficacy against p. capsici are fixed copper formulations.",
}
UM = {
    "cause": "itersonilia canker, also called black canker, is caused by itersonilia perplexans .",
    "late": "itersonilia canker of parsnip can be a serious disease, especially in late harvested crops.",
    "cankers": "on roots, cankers formmainly on the crown and shoulder, although lateral roots may be affected.",
    "wet": "disease development is enhanced by cool, wet weather.",
    "resistant": "select and plant resistant cultivars.",
    "rotate": "rotate parsnip with non-host crops.",
    "fly": "control carrot rust fly as larvae can predispose roots to infection.",
    "fungicide": "fungicide sprays are not effective for control of root cankers.",
    "cover": "cover the shoulder of parsnips with soil throughout the growing season.",
    "plow": "reduce soilborne inoculum by deep plowing to enhance decomposition of parsnip residue.",
    "hosts": "the pathogen also affects carrot, coriander, parsley, chrysanthemum, aster, sunflower and wild plants.",
}

PEPPER = [  # (field(s), claim, verdict, [(src, quote, scope)])
    ("symptoms_seasoned / _beginner", "dark lesions at or near the soil line girdle the stem", "STATED",
     [("ncsu_pb", NC["soil_line"], ""), ("ncsu_pb", NC["girdle"], "")]),
    ("symptoms_seasoned / _beginner", "'water-soaked' stem lesions", "PARTIAL: NCSU calls the STEM lesions dark brown; 'water-soaked' is its word for FRUIT rot", [("ncsu_pb", NC["fruit_rot"], "fruit")]),
    ("symptoms_seasoned / _beginner", "the plant wilts and collapses suddenly", "STATED (wilting then death); 'suddenly' NOT STATED", [("ncsu_pb", NC["wilt"], "")]),
    ("symptoms_seasoned", "sometimes a white cottony growth", "STATED for FRUIT ('white powdery to cottony mold'); not stated for stems", [("ncsu_pb", NC["fruit_rot"], "fruit")]),
    ("symptoms_seasoned / _beginner", "roots rot; fruit rot", "STATED (crown rot, fruit rot; 'root and crown rot' in the fungicide section)", [("ncsu_pb", NC["crown_fruit"], ""), ("ncsu_pb", NC["soil_line"], "")]),
    ("symptoms_seasoned", "fruit develops a FIRM, white-mold rot", "PARTIAL: white mold STATED; 'firm' NOT STATED (NCSU: 'water-soaked areas')", [("ncsu_pb", NC["fruit_rot"], "")]),
    ("symptoms_seasoned / _beginner; cause_*", "flares in warm, wet, poorly drained / soggy ground, after heavy rain", "STATED (excessive rainfall or overhead irrigation, saturated soils, 75 to 90°F); 'flooding' NOT STATED", [("ncsu_pb", NC["conditions"], "")]),
    ("symptoms_seasoned ('the most serious' / banana 'among the most serious') / _beginner ('one of the worst')", "rank among pepper diseases", "NOT STATED on any hashed cited page", []),
    ("cause_seasoned / _beginner", "Phytophthora capsici, a water mold (mold-like)", "STATED ('fungal-like oomycete')", [("ncsu_pb", NC["pathogen"], "")]),
    ("cause_seasoned / _beginner", "spreads in splashing and running water; moves fast", "STATED", [("ncsu_pb", NC["water_spread"], ""), ("ncsu_pb", NC["soil_line"], ""), ("ncsu_pb", NC["fruit_splash"], "")]),
    ("cause_seasoned / _beginner", "survives in soil and debris for years", "STATED (oospores persist over 10 years; culls and debris are inoculum)", [("ncsu_pb", NC["oospores"], ""), ("ncsu_pb", NC["debris"], "")]),
    ("cause_seasoned", "worst on heavy or poorly drained ground and in low spots that stay wet", "STATED as the drainage / standing-water advice", [("ncsu_pb", NC["drainage"], "")]),
    ("organic_treatment_* / control_ladder garden_sanitation", "remove and destroy affected plants and fruit promptly", "STATED (remove from the field; no culls left); 'destroy' / 'promptly' not worded", [("ncsu_pb", NC["remove"], ""), ("ncsu_pb", NC["culls"], "")]),
    ("organic_treatment_* / control_ladder improve_drainage", "improve drainage immediately (as the response)", "PARTIAL: drainage is STATED as PREVENTION (site choice), not as a response after infection", [("ncsu_pb", NC["drainage"], "")]),
    ("organic_treatment_*", "no effective home-garden cure; control is preventive", "STATED for home gardeners (no effective chemical option; resistance + cultural). Organic growers: fixed copper has 'some efficacy'", [("ncsu_pb", NC["home"], ""), ("ncsu_pb", NC["organic"], "organic growers")]),
    ("prevention_* / control_ladder improve_drainage", "raised, well-drained beds", "STATED", [("ncsu_pb", NC["raised"], ""), ("ncsu_pb", NC["drainage"], "")]),
    ("prevention_seasoned ('or hills') / _beginner ('or mounds')", "hills / mounds", "NOT STATED (raised BEDS only)", []),
    ("prevention_* / control_ladder improve_drainage", "avoid low spots that stay wet", "STATED (even terrain, no standing water)", [("ncsu_pb", NC["drainage"], "")]),
    ("prevention_* / control_ladder water_at_the_base", "water at the soil rather than overhead", "STATED (drip; avoid overhead, especially once fruit is present)", [("ncsu_pb", NC["drip"], ""), ("umn_pep", "avoid overhead sprinkling.", "UMN")]),
    ("prevention_* / control_ladder water_at_the_base", "do not overwater", "STATED ('irrigate moderately')", [("ncsu_pb", NC["drip"], "")]),
    ("prevention_seasoned / control_ladder splash_barrier_mulch", "mulch to limit splash", "PARTIAL: PLASTIC mulch STATED (with raised beds); splash as the route STATED; the mulch-limits-splash link is not worded", [("ncsu_pb", NC["raised"], ""), ("ncsu_pb", NC["soil_line"], ""), ("umn_pep", "soil splashed up onto the leaves can contain disease spores.", "UMN, overhead-watering paragraph")]),
    ("prevention_* / control_ladder crop_rotation", "rotate away from peppers and other susceptible crops for at least three to four years ('several years' in beginner)", "PARTIAL / QUALIFIED: NCSU says the broad host range makes rotation WEAK and names only cereals as non-hosts; no year count on any hashed page", [("ncsu_pb", NC["rotation_weak"], ""), ("ncsu_pb", NC["rotate_cereals"], ""), ("ncsu_pb", NC["hosts"], "")]),
    ("prevention_seasoned", "keep fruit up off saturated soil", "NOT STATED; NCSU states the route (splashed soil infects fruit)", [("ncsu_pb", NC["fruit_splash"], "")]),
    ("(absent from the entry)", "resistant varieties; no surface water for irrigation", "STATED on NCSU; the entry does not carry them (an author's call)", [("ncsu_pb", NC["resistant"], ""), ("ncsu_pb", NC["resistant_some"], ""), ("ncsu_pb", "do not use surface water (ponds, creek) for irrigation since it may be infested.", "")]),
]

PARSNIP = [  # (leaf, claim, verdict, quotes)
    ("diseases[0].prevention_seasoned + failure_diagnostics[3].next_season_tip_seasoned", "choose resistant varieties", "STATED", [("umass", UM["resistant"], ""), ("rhs", "resistant to canker.", "RHS variety rows ('Albion', 'Gladiator', 'Picador')")]),
    ("same", "named: Avonresister, Cobham Improved Marrow", "NOT STATED on any hashed cited page (RHS names Albion, Gladiator, Picador)", []),
    ("same", "rotate out of the carrot family for two to three years (fd[3]: three years)", "PARTIAL: rotation to NON-HOSTS STATED; hosts include carrot, coriander, parsley (carrot family) and chrysanthemum, aster, sunflower; NO year count", [("umass", UM["rotate"], ""), ("umass", UM["hosts"], "")]),
    ("same", "hill soil over the shoulders through the season", "STATED", [("umass", UM["cover"], "")]),
    ("same", "control carrot rust fly", "STATED", [("umass", UM["fly"], "")]),
    ("same", "avoid waterlogged / overly wet beds", "PARTIAL: cool, wet WEATHER favors it; waterlogged beds not worded. Clemson: parsnips need well-drained soil", [("umass", UM["wet"], ""), ("clem_root", "similar to carrots, they need a loose, well-drained soil, and weeds should be controlled.", "parsnip paragraph")]),
    ("diseases[0] only", "harvest before very late in cold wet spells", "PARTIAL: 'especially in late harvested crops' STATED; 'cold wet spells' timing not worded", [("umass", UM["late"], ""), ("umass", UM["wet"], "")]),
    ("same", "bury old parsnip residue by deep cultivation to lower inoculum", "STATED", [("umass", UM["plow"], "")]),
    ("failure_diagnostics[3] only", "fungicides do not control root cankers", "STATED", [("umass", UM["fungicide"], "")]),
    ("growth_stages[2].user_action_seasoned", "maintain even moisture to prevent cracking", "STATED (RHS: evenly moist to avoid splitting; UMN: drought splits roots)", [("rhs", "more mature plants are fairly drought tolerant, but to avoid the roots splitting , keep the soil evenly moist.", ""), ("umn_cp", "a drought can also cause split roots.", "")]),
    ("growth_stages[2]", "about 1 inch per week", "NOT STATED on any hashed page cited on parsnip", []),
    ("growth_stages[2]", "hill a little soil or mulch over the shoulders to suppress canker", "STATED for SOIL (UMass); 'or mulch' NOT STATED", [("umass", UM["cover"], "")]),
    ("growth_stages[2]", "... and greening", "NOT STATED for parsnip: UMN's greening sentence is about carrot varieties that push up", [("umn_cp", "some carrot varieties will push the tops of the roots up out of the soil.", "carrots"), ("umn_cp", "hilling soil around these plants will keep the roots from turning green.", "carrots")]),
    ("growth_stages[2]", "feeding is rarely needed", "NOT STATED; Clemson says to sidedress root crops at 4 in. (tension); UMN warns excess nitrogen favors leaves", [("clem_root", "sidedress fertilize these root crops when plants are 4 inches tall.", "carrot/beet/radish/parsnip page"), ("umn_cp", "excessive nitrogen fertilization can also contribute to lots of leaf growth at the expense of root growth.", "")]),
    ("growth_stages[2]", "wear gloves and long sleeves among the foliage in bright sun; sap can cause a skin rash", "STATED (UMN: rash from contact with the LEAVES on bright sunny days; long pants, sleeves, gloves). 'Sap' is not UMN's word", [("umn_cp", "some people develop a rash from contact with parsnip leaves, particularly on bright sunny days.", ""), ("umn_cp", "wear long pants, long sleeves and gloves when weeding or harvesting parsnips.", "")]),
]

SQ_PAGES = ("c1206", "umn_pk")
BEGINNER = [  # (crop, field, claim, verdict vs its pages, vs the seasoned leaf (round 2), quotes)
    ("eggplant", "diseases[3].prevention_beginner", "raised beds or mounds so water drains away", "NOT STATED on Clemson eggplant; NCSU (pepper page; eggplant is a named host) says raised beds", "seasoned (ruled B2) drops raised beds: must be re-authored", [("ncsu_pb", NC["raised"], "pepper page")]),
    ("eggplant", "diseases[3].prevention_beginner", "avoid wet low spots", "PARTIAL (excess soil moisture)", "seasoned keeps 'excessive moisture'", [("clem_egg", "avoiding excessive soil moisture is an important strategy for managing phytophthora diseases .", "")]),
    ("eggplant", "diseases[3].prevention_beginner", "water at the soil", "STATED", "kept", [("clem_egg", "if unable to drip irrigate, direct water to the base of the plants and avoid wetting the leaves as much as possible.", "")]),
    ("eggplant", "diseases[3].prevention_beginner", "keep fruit off soggy ground", "NOT STATED", "seasoned drops it: must be re-authored", []),
    ("eggplant", "diseases[3].prevention_beginner", "rotate away from peppers, tomatoes (and squash)", "peppers/tomatoes STATED (3 years). SQUASH: Clemson says rotate WITH cucurbits; NCSU says most cucurbits are P. capsici hosts and only cereals are non-hosts. T1 SOURCES CONFLICT", "the ruled seasoned sentence 5 says rotate WITH squash and melons: CONFLICT TO RULE before either register lands", [("clem_egg", "avoid planting eggplant where tomatoes, potatoes, peppers, or eggplant (all members of the solanaceae family) were planted within the last three years.", ""), ("clem_egg", "instead, rotate with cucurbits (squash, zucchini, melons, and cantaloupe), brassicas (collards, kale, cabbage, turnips, and broccoli), grasses (sweet corn and grains), alliums (onions, garlic, and leeks), etc.", ""), ("ncsu_pb", NC["hosts"], ""), ("ncsu_pb", NC["rotate_cereals"], "")]),
    ("bell-pepper / banana-pepper", "diseases[1].prevention_beginner", "raised beds (STATED) or mounds (NOT STATED) so water drains away", "see the pepper packet", "seasoned HELD (re-author pending)", [("ncsu_pb", NC["raised"], "")]),
    ("bell-pepper / banana-pepper", "diseases[1].prevention_beginner", "avoid wet low spots; water at the soil; do not overwater", "STATED", "", [("ncsu_pb", NC["drainage"], ""), ("ncsu_pb", NC["drip"], "")]),
    ("bell-pepper / banana-pepper", "diseases[1].prevention_beginner", "rotate away from peppers for several years", "QUALIFIED: NCSU says rotation is weak against this host range; no year count", "", [("ncsu_pb", NC["rotation_weak"], "")]),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "a sunny spot", "pumpkin: STATED (C1206); squash: NOT STATED on UMN", "squash seasoned CUT full sun: re-author the three squash", [("c1206", "site selection and preparation like most vegetables, pumpkins do best when grown in full sunlight conditions.", "pumpkins")]),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "rich, well-drained soil", "well-drained STATED; 'rich' not worded", "kept", [("umn_pk", "the soil should be moisture retentive yet well-drained.", "")]),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "mix in plenty of compost before planting", "PARTIAL: compost or well-rotted manure in spring or fall (UMN); 'plenty' not worded", "seasoned adds the fresh-manure caution", [("umn_pk", "you can improve your soil by adding well-rotted manure or compost in spring or fall.", "")]),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "large, hungry plant", "NOT STATED", "seasoned dropped it", []),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "low hills or mounds which warm up and drain better", "pumpkin: mound for drainage STATED (C1206); squash: raised BEDS (UMN); 'warm up' NOT STATED", "seasoned: pumpkin hills, squash raised beds; no warming", [("c1206", "planting in hills simply means raising the soil up a few inches into a gentle mound, which helps to ensure proper drainage.", "pumpkins"), ("umn_pk", "forming raised beds will ensure good drainage, which these crops require.", "")]),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "SPACING and VINE RUN (8 ft hills / 2-3 ft in rows 5-6 ft / vines 6-20 ft / bush closer)", "spacing STATED elsewhere (C1206, UMN); vine-run figures NOT STATED", "CUT from all four seasoned leaves by ruling (the spacing fields carry it): must be cut here too", []),
    ("pumpkin / butternut / acorn / spaghetti", "soil_prep_beginner", "heavy or wet soil: build the mounds up higher so water drains away", "PARTIAL: raised beds/mounds for drainage STATED; 'higher on heavy soil' not worded", "", [("umn_pk", "forming raised beds will ensure good drainage, which these crops require.", "")]),
    ("parsnip", "diseases[0].prevention_beginner", "resistant variety; mound soil over shoulders; carrot rust fly; clear and bury old plants", "STATED (UMass)", "pending Trevor's seasoned re-author", [("umass", UM["resistant"], ""), ("umass", UM["cover"], ""), ("umass", UM["fly"], ""), ("umass", UM["plow"], "")]),
    ("parsnip", "diseases[0].prevention_beginner", "not the same bed for two to three years (parsnips or relatives)", "PARTIAL: non-host rotation STATED; years NOT STATED", "", [("umass", UM["rotate"], ""), ("umass", UM["hosts"], "")]),
    ("parsnip", "diseases[0].prevention_beginner", "avoid soggy soil", "PARTIAL: cool, wet weather; well-drained soil", "", [("umass", UM["wet"], "")]),
    ("parsnip", "failure_diagnostics[3].next_season_tip_beginner", "resistant variety; soil over shoulders; rust fly; avoid soggy soil; sprays do not fix root canker", "STATED, except 'soggy' (PARTIAL)", "", [("umass", UM["fungicide"], "")]),
    ("parsnip", "failure_diagnostics[3].next_season_tip_beginner", "three years", "NOT STATED", "", []),
    ("parsnip", "growth_stages[2].user_action_beginner", "steady watering so roots do not crack", "STATED (RHS)", "", [("rhs", "more mature plants are fairly drought tolerant, but to avoid the roots splitting , keep the soil evenly moist.", "")]),
    ("parsnip", "growth_stages[2].user_action_beginner", "about 1 inch a week", "NOT STATED", "", []),
    ("parsnip", "growth_stages[2].user_action_beginner", "pull a little soil or mulch over the root tops as they show", "SOIL STATED (UMass, for canker); mulch NOT STATED", "", [("umass", UM["cover"], "")]),
    ("parsnip", "growth_stages[2].user_action_beginner", "usually need no feeding", "NOT STATED; Clemson says sidedress root crops at 4 in. (tension)", "", [("clem_root", "sidedress fertilize these root crops when plants are 4 inches tall.", "")]),
    ("parsnip", "growth_stages[2].user_action_beginner", "gloves and long sleeves on a sunny day; sap can give a rash", "STATED (leaves; bright sunny days)", "", [("umn_cp", "some people develop a rash from contact with parsnip leaves, particularly on bright sunny days.", "")]),
]


def table(rows, out, n, cols):
    out += ["| # | " + " | ".join(cols) + " | page | verbatim (norm_text) | location |", "| -- " * (len(cols) + 4) + "|"]
    for row in rows:
        *meta, quotes = row
        if not quotes:
            n += 1
            out.append(f"| {n} | " + " | ".join(str(m) for m in meta) + " | -- | (no hashed sentence) | -- |")
            continue
        for src, q, scope in quotes:
            qq, loc = bp.locate(SHA[src], U[src][0], q)
            n += 1
            out.append(f"| {n} | " + " | ".join(str(m) for m in meta) + f" | {src} `{SHA[src][:8]}`{(' (' + scope + ')') if scope else ''} | \"{qq}\" | {loc} |")
    out.append("")
    return n


def pages(keys):
    return ["| key | page | sha256 |", "| -- | -- | -- |"] + [f"| {k} | {U[k][1]}: {U[k][0]} | `{SHA[k]}` |" for k in keys] + [""]


def main(out_dir):
    B = {c["slug"]: c for c in bp.DATA["crops"]}
    # pepper
    e = B["bell-pepper"]["diseases"][1]
    o = ["# PLA-673 B2: pepper Phytophthora blight entry (bell + banana)", "",
         "Read-only on canonical `3ccc25f1`. Every claim in the WHOLE `diseases[id=phytophthora-blight]` entry (identical on both "
         "peppers except symptoms_seasoned: bell 'the most serious', banana 'among the most serious'). Primary source: NC State's "
         "Phytophthora Blight of Peppers factsheet, linked from the ncsu_ext anchor's index page and hashed into MANIFEST for this "
         "packet. Quotes are norm_text, proven against the hashed bytes. **Nothing authored.**", "", "## Pages", ""] + pages(["ncsu_pb", "umn_pep", "clem_pep"])
    o += ["## The entry today (bell-pepper)", ""]
    for k in ("symptoms_seasoned", "symptoms_beginner", "cause_seasoned", "cause_beginner", "organic_treatment_seasoned",
              "organic_treatment_beginner", "prevention_seasoned", "prevention_beginner"):
        o.append(f"* `{k}`: {e[k]}")
    for st in e["control_ladder"]:
        o.append(f"* `control_ladder[{st['method']}]`: seasoned: {st['note_seasoned']} / beginner: {st['note_beginner']}")
    o += ["", "## Claims", ""]
    n = table(PEPPER, o, 0, ["field", "claim", "verdict"])
    o += ["## Headlines", "", "* **The disease's own factsheet weakens the rotation claim:** 'the broad host range of p. capsici significantly reduces the efficacy of crop rotation', with cereals the only named non-hosts; no page gives three to four years.",
          "* **Host range includes eggplant and most cucurbits** (this bears on EGGPLANT's ruled rotation sentence, see the beginner packet).",
          "* Not stated: hills / mounds, the disease rank ('most serious'), 'firm' fruit rot, keep fruit off saturated soil, a year count.",
          "* Stated and absent from the entry: resistant varieties; no surface water for irrigation."]
    open(os.path.join(out_dir, "packet_b2_pepper.md"), "w").write("\n".join(o)); print("pepper", n)
    # parsnip
    p = B["parsnip"]
    o = ["# PLA-673 B2: parsnip's three hilling leaves (seasoned)", "",
         "Read-only on canonical `3ccc25f1`. Every claim in `diseases[0].prevention_seasoned`, `failure_diagnostics[3].next_season_tip_seasoned` "
         "and `growth_stages[2].user_action_seasoned` (no citation block today), from ALL hashed pages cited on parsnip plus the UMass canker "
         "factsheet (cited on parsnip, hashed into MANIFEST for this packet). **Nothing authored.**", "", "## Pages", ""] + pages(["umass", "umn_cp", "clem_root", "rhs"])
    o += ["## The leaves today", "",
          f"* `diseases[0].prevention_seasoned`: {p['diseases'][0]['prevention_seasoned']}",
          f"* `failure_diagnostics[3].next_season_tip_seasoned`: {p['failure_diagnostics'][3]['next_season_tip_seasoned']}",
          f"* `growth_stages[2].user_action_seasoned`: {p['growth_stages'][2]['user_action_seasoned']}", "", "## Claims", ""]
    n = table(PARSNIP, o, 0, ["leaf", "claim", "verdict"])
    o += ["## Headlines", "", "* Hilling (soil over the shoulders) is STATED by UMass for canker. 'Or mulch' and 'greening' (a carrot sentence) are not.",
          "* NOT STATED: Avonresister / Cobham Improved Marrow (RHS names Albion, Gladiator, Picador), any rotation year count, 1 inch per week, 'feeding rarely needed' (Clemson says sidedress root crops at 4 in.).",
          "* The other hashed pages cited on parsnip (OSU chart, WSU) state none of these claims for parsnip."]
    open(os.path.join(out_dir, "packet_b2_parsnip.md"), "w").write("\n".join(o)); print("parsnip", n)
    # beginner
    o = ["# PLA-673 B2: beginner siblings of the 10 B2 leaves", "",
         "Read-only on canonical `3ccc25f1`. Each beginner sibling, claim by claim, against the SAME pages as its seasoned leaf, and against the "
         "seasoned text as ruled in B2 (dual-register rule: never less true than the seasoned leaf). **Nothing authored.**", "", "## The leaves today", ""]
    for slug, path in (("eggplant", ("diseases", 3, "prevention_beginner")), ("bell-pepper", ("diseases", 1, "prevention_beginner")),
                       ("banana-pepper", ("diseases", 1, "prevention_beginner")), ("pumpkin", ("soil_prep_beginner",)),
                       ("butternut-squash", ("soil_prep_beginner",)), ("acorn-squash", ("soil_prep_beginner",)),
                       ("spaghetti-squash", ("soil_prep_beginner",)), ("parsnip", ("diseases", 0, "prevention_beginner")),
                       ("parsnip", ("failure_diagnostics", 3, "next_season_tip_beginner")), ("parsnip", ("growth_stages", 2, "user_action_beginner"))):
        v = B[slug]
        for k in path:
            v = v[k]
        o.append(f"* **{slug}** `{'.'.join(map(str, path))}`: {v}")
    o += ["", "## Pages", ""] + pages(["clem_egg", "ncsu_pb", "c1206", "umn_pk", "umass", "umn_cp", "clem_root", "rhs"]) + ["## Claims", ""]
    n = table(BEGINNER, o, 0, ["crop", "field", "claim", "verdict", "vs the seasoned leaf"])
    o += ["## Must change in the same promote (dual-register rule)", "",
          "* **eggplant**: 'raised beds or mounds' and 'keep fruit off soggy ground' (dropped from the seasoned leaf; not on Clemson eggplant). **Rotation: the T1 sources CONFLICT on cucurbits** (Clemson: rotate WITH cucurbits; NCSU: most cucurbits are P. capsici hosts, rotate to cereals). The ruled seasoned sentence 5 sides with Clemson; the beginner says the opposite. A ruling is needed before either lands.",
          "* **all four squash**: the spacing and vine-run sentences (cut from the seasoned leaves by ruling); 'warm up' (not stated); 'large, hungry' (not stated). **butternut / acorn / spaghetti**: 'sunny spot' (cut from their seasoned leaves: only the pumpkin publication states full sun).",
          "* **peppers**: held with their seasoned leaves (pepper packet).",
          "* **parsnip**: re-authored with Trevor's seasoned parsnip texts; not stated today: the year counts, 1 inch a week, mulch, no feeding."]
    open(os.path.join(out_dir, "packet_b2_beginner.md"), "w").write("\n".join(o)); print("beginner", n)


main(sys.argv[1])
