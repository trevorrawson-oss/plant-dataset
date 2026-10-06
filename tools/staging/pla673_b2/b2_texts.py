"""PLA-673 part B2: the approved leaf texts, VERBATIM (claude.ai; approved by Trevor), each sentence with the packet rows
it maps to. Packet keys: B2 = the original B2 packet (67 rows), BS = the beginner-sibling packet (34), PS = the parsnip
packet (23), PP = the pepper packet (39). Round 1 (B2 rulings) gave eggplant 1-4 and the squash seasoned texts; round 2
(2026-10-06) replaced eggplant 5 with 5 + 6 and authored the rest. Do not edit a sentence without a new ruling."""

EGG = "diseases[id=phytophthora-blight]"
LEAVES = [  # (crop, path, [(sentence, [(packet, row), ...])])
    ("eggplant", f"{EGG}.prevention_seasoned", [
        ("Keeping soil moisture from getting excessive is a key strategy for managing Phytophthora.", [("B2", 10), ("B2", 11)]),
        ("Water often enough to keep the soil moist but not saturated.", [("B2", 22)]),
        ("Use drip irrigation rather than overhead watering, or water at the base of the plants and keep the leaves as dry as possible.", [("B2", 19), ("B2", 20)]),
        ("Don't plant eggplant where tomatoes, potatoes, peppers or eggplant grew in the last three years, since the pathogen survives in soil.", [("B2", 32), ("B2", 31)]),
        ("The pathogen's broad host range, which includes tomato, beans and most cucurbits, makes rotation much less effective.", [("BS", 7), ("PP", 33)]),
        ("Rotate to cereals such as corn or wheat, which are not hosts.", [("BS", 8), ("PP", 33)]),
    ]),
    ("eggplant", f"{EGG}.prevention_beginner", [
        ("Too much water in the soil makes this disease worse, so keep the soil moist but not soggy.", [("B2", 11), ("B2", 22)]),
        ("Water with a drip line if you can, or water at the base of the plants and keep the leaves dry.", [("B2", 19), ("B2", 20)]),
        ("Don't plant eggplant where tomatoes, potatoes, peppers or eggplant grew in the last three years.", [("B2", 32)]),
        ("This disease also attacks tomatoes, beans and most squash and melons, so rotating crops helps less against it.", [("BS", 7), ("PP", 33)]),
        ("Corn and wheat don't get it, so they are good crops to plant in that spot instead.", [("BS", 8), ("PP", 33)]),
    ]),
    ("pumpkin", "soil_prep_seasoned", [
        ("Choose a spot in full sun with well-drained soil.", [("B2", 35), ("B2", 36), ("B2", 38)]),
        ("Prepare it by tilling deeply and adding organic matter.", [("B2", 37)]),
        ("Add well-rotted manure or compost in spring or fall.", [("B2", 39)]),
        ("Skip fresh manure, which may carry harmful bacteria and increase weed problems.", [("B2", 40)]),
        ("Depending on how much manure or compost you add, you may not need extra fertilizer.", [("B2", 41)]),
        ("Plant in hills: raise the soil a few inches into a gentle mound to help drainage.", [("B2", 44)]),
    ]),
    ("pumpkin", "soil_prep_beginner", [
        ("Pick a sunny spot with soil that drains well.", [("B2", 35), ("B2", 36)]),
        ("Before planting, dig the soil deeply and mix in compost or well-rotted manure.", [("B2", 37), ("B2", 39)]),
        ("Don't use fresh manure, which can carry harmful bacteria and bring more weeds.", [("B2", 40)]),
        ("With enough compost or manure, you may not need extra fertilizer.", [("B2", 41)]),
        ("Plant in hills, raising the soil a few inches into a gentle mound so water drains away.", [("B2", 44)]),
    ]),
]
SQUASH_SEASONED = [
    ("Choose a spot with soil that holds moisture yet drains well.", [("B2", 38)]),
    ("Add well-rotted manure or compost in spring or fall.", [("B2", 39)]),
    ("Skip fresh manure, which may carry harmful bacteria and increase weed problems.", [("B2", 40)]),
    ("Depending on how much manure or compost you add, you may not need extra fertilizer.", [("B2", 41)]),
    ("Form raised beds, since these crops need good drainage.", [("B2", 46)]),
]
SQUASH_BEGINNER = [
    ("Choose a spot with soil that stays moist but drains well.", [("B2", 38)]),
    ("Mix in compost or well-rotted manure in spring or fall.", [("B2", 39)]),
    ("Don't use fresh manure, which can carry harmful bacteria and bring more weeds.", [("B2", 40)]),
    ("With enough compost or manure, you may not need extra fertilizer.", [("B2", 41)]),
    ("Build raised beds, since these plants need good drainage.", [("B2", 46)]),
]
for _s in ("butternut-squash", "acorn-squash", "spaghetti-squash"):
    LEAVES.append((_s, "soil_prep_seasoned", SQUASH_SEASONED))
    LEAVES.append((_s, "soil_prep_beginner", SQUASH_BEGINNER))

PD0 = "diseases[id=itersonilia-canker]"
PFD = "failure_diagnostics[id=canker]"
PGS = "growth_stages[id=established]"
LEAVES += [
    ("parsnip", f"{PD0}.prevention_seasoned", [
        ("Choose canker-resistant varieties.", [("PS", 1)]),
        ("Rotate parsnip with crops the pathogen doesn't infect.", [("PS", 4)]),
        ("Besides parsnip, it infects carrot, coriander and parsley, along with sunflower, aster and chrysanthemum.", [("PS", 5)]),
        ("Hill soil over the root shoulders throughout the season.", [("PS", 6)]),
        ("Control carrot rust fly, since its larvae can make roots more prone to infection.", [("PS", 7)]),
        ("Grow parsnips in loose, well-drained soil.", [("PS", 9)]),
        ("Cool, wet weather favors the disease, and it can be serious in late-harvested crops.", [("PS", 8), ("PS", 10)]),
        ("After harvest, dig old parsnip residue in deeply so it decomposes and less inoculum survives in the soil.", [("PS", 12)]),
    ]),
    ("parsnip", f"{PD0}.prevention_beginner", [
        ("Grow a variety that resists canker.", [("PS", 1)]),
        ("Rotate parsnips with crops this disease doesn't infect.", [("PS", 4)]),
        ("It also attacks carrots, parsley and cilantro.", [("PS", 5)]),
        ("Keep the tops of the roots covered with soil all season.", [("PS", 6)]),
        ("Control carrot rust fly, since its larvae can make roots easier to infect.", [("PS", 7)]),
        ("Cool, wet weather makes the disease worse, and it does the most damage in parsnips harvested late.", [("PS", 8), ("PS", 10)]),
        ("After harvest, dig old parsnip plants deep into the soil so they break down.", [("PS", 12)]),
    ]),
    ("parsnip", f"{PFD}.next_season_tip_seasoned", [
        ("Choose canker-resistant varieties.", [("PS", 1)]),
        ("Rotate with crops the pathogen doesn't infect, keeping carrot, coriander and parsley out of the rotation too.", [("PS", 4), ("PS", 5)]),
        ("Hill soil over the root shoulders throughout the season.", [("PS", 6)]),
        ("Control carrot rust fly.", [("PS", 7)]),
        ("Grow in loose, well-drained soil.", [("PS", 9)]),
        ("Dig old parsnip residue in deeply after harvest.", [("PS", 12)]),
        ("Fungicide sprays don't control root cankers.", [("PS", 13)]),
    ]),
    ("parsnip", f"{PFD}.next_season_tip_beginner", [
        ("Grow a canker-resistant variety.", [("PS", 1)]),
        ("Rotate parsnips with crops this disease doesn't infect.", [("PS", 4)]),
        ("Keep the tops of the roots covered with soil all season.", [("PS", 6)]),
        ("Control carrot rust fly.", [("PS", 7)]),
        ("Grow them in loose soil that drains well.", [("PS", 9)]),
        ("Bury old parsnip plants deep in the soil after harvest.", [("PS", 12)]),
        ("Sprays won't fix root canker.", [("PS", 13)]),
    ]),
    ("parsnip", f"{PGS}.user_action_seasoned", [
        ("Keep the soil evenly moist, since drought can split the roots.", [("PS", 15), ("PS", 14)]),
        ("Hill soil over the root shoulders through the season to help prevent canker.", [("PS", 6)]),
        ("Avoid excess nitrogen, which pushes leaf growth at the expense of the roots.", [("PS", 21)]),
        ("Some people get a skin rash from contact with parsnip leaves, especially on bright, sunny days.", [("PS", 22)]),
        ("Wear long sleeves, long pants and gloves when weeding or harvesting.", [("PS", 23)]),
    ]),
    ("parsnip", f"{PGS}.user_action_beginner", [
        ("Keep the soil evenly moist, because dry spells can make the roots split.", [("PS", 15), ("PS", 14)]),
        ("Keep the tops of the roots covered with soil to help prevent canker.", [("PS", 6)]),
        ("Don't overdo nitrogen fertilizer, which grows leaves at the expense of the roots.", [("PS", 21)]),
        ("Some people get a skin rash from touching parsnip leaves, especially on sunny days.", [("PS", 22)]),
        ("Wear long sleeves, long pants and gloves when weeding or harvesting.", [("PS", 23)]),
    ]),
]

# the citation block for each edited leaf: its sources, as ruled (a list, in order)
SOURCES = {
    ("eggplant", EGG): ["clemson_hgic", "ncsu_ext_phytophthora_blight_peppers"],
    # usu_ext REMOVED 2026-10-06 (Trevor, B2 go-condition 1): it came from the pre-state block, no ruled sentence cites
    # it, and its page (extension.usu.edu .../veg-list-root-crops) is a disease index that only names the disease.
    ("parsnip", PD0): ["umass_ext_itersonilia_canker", "clemson_hgic"],
    ("parsnip", PFD): ["umass_ext_itersonilia_canker", "clemson_hgic"],
    ("parsnip", PGS): ["umn_ext", "umass_ext_itersonilia_canker", "rhs"],
    ("pumpkin", "<soil_prep>"): ["uga_c1206_homegrown_pumpkins", "umn_ext"],
    ("butternut-squash", "<soil_prep>"): ["umn_ext"],
    ("acorn-squash", "<soil_prep>"): ["umn_ext"],
    ("spaghetti-squash", "<soil_prep>"): ["umn_ext"],
}
