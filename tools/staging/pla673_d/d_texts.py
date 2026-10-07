"""PLA-673 part D: the approved texts, VERBATIM (claude.ai; approved by Trevor, 2026-10-06), each sentence with its refs.
Ref keys: ("PP", n) = the pepper packet row n (packet_b2_pepper.md, numbered as posted); ("C", n) = the part C packet row n
(packet_partc.md); ("W", key) = a watermelon thinning quote below, from the pages hashed for the part D ruling (USU
2618f2f2, UMN 9e2a61b5) or already hashed (UGA C1035 12164061). Do not edit a sentence without a new ruling."""

W_URL = {
    "uga": "https://fieldreport.caes.uga.edu/publications/C1035/",
    "usu": "https://extension.usu.edu/yardandgarden/research/watermelon-in-the-garden",
    "umn": "https://extension.umn.edu/fruit/growing-melons-home-garden",
}
W = {  # key: (page, verbatim norm_text quote)
    "uga_sow": ("uga", "sow four to five seeds per hill at a depth of 1 in."),
    "uga_thin": ("uga", "a week after they have germinated, thin the seedlings to two per hill."),
    "usu_thin": ("usu", "after they have two leaves, thin to 2 plants per mound."),
    "umn_strong": ("umn", "after the seedlings emerge, choose the strongest plant in each group and remove the others."),
}

THIN = "thinning"
ROW = "planting_layout[id=row-none]"
LEAVES = [  # (crop, path, [(sentence, [ref, ...])])
    ("watermelon", f"{THIN}.tip_seasoned", [
        ("Sow four to five seeds per hill.", [("W", "uga_sow")]),
        ("Once seedlings have two leaves, about a week after they come up, thin to the strongest two plants per hill.",
         [("W", "usu_thin"), ("W", "uga_thin"), ("W", "umn_strong")]),
        ("In rows, thin to one plant every 24 to 48 inches.", [("C", 5), ("C", 6)]),
    ]),
    ("watermelon", f"{THIN}.tip_beginner", [
        ("Plant four or five seeds in each hill.", [("W", "uga_sow")]),
        ("When the seedlings have two leaves, about a week after they sprout, keep the two strongest in each hill and remove the rest.",
         [("W", "usu_thin"), ("W", "uga_thin"), ("W", "umn_strong")]),
        ("If you plant in rows, leave one plant every 24 to 48 inches.", [("C", 5), ("C", 6)]),
    ]),
    # free text (13 distinct values roster-wide, no enum, no consumer renders it): the ruling's free-text branch
    ("watermelon", f"{THIN}.method", [
        ("thin to two plants per hill", [("W", "usu_thin"), ("W", "uga_thin")]),
    ]),
]
# the row entry's figures and the crop-root mirror (value ops; evidence = the UF VH021 table header + row)
VALUES = [  # (crop, path, new, cited_at, [ref, ...])
    ("watermelon", f"{ROW}.in_row_inches", [24, 48], ROW, [("C", 5), ("C", 6)]),
    ("watermelon", f"{ROW}.row_spacing_inches", [60, 60], ROW, [("C", 5), ("C", 6)]),
    ("watermelon", "spacing_inches", [24, 48], ROW, [("C", 5), ("C", 6)]),   # mirror: first entry carrying in_row_inches
]

PB = "diseases[id=phytophthora-blight]"
PEPPER = [  # (path, [(sentence, [ref])]); identical on bell-pepper and banana-pepper
    (f"{PB}.symptoms_seasoned", [
        ("Symptoms usually start at the soil line in the roots and crown, though infection can occur anywhere splashing water throws soil onto the plant.", [("PP", 1)]),
        ("Crown lesions turn dark brown and extend up the stem until they girdle it and kill the plant.", [("PP", 2)]),
        ("In wet conditions, plants typically wilt and then die.", [("PP", 4)]),
        ("Infected fruit shows water-soaked areas that become covered with white, powdery to cottony mold.", [("PP", 3)]),
        ("It develops best with heavy rain or overhead irrigation, saturated soil and temperatures of 75 to 90°F.", [("PP", 9)]),
    ]),
    (f"{PB}.symptoms_beginner", [
        ("Look for a dark brown patch on the stem near the soil that spreads up and circles the stem.", [("PP", 1), ("PP", 2)]),
        ("In wet weather, the plant wilts and then dies.", [("PP", 4)]),
        ("Fruit can rot too, with wet-looking spots that turn white and fuzzy.", [("PP", 3)]),
        ("It's worst in warm weather with lots of rain and soggy soil.", [("PP", 9)]),
    ]),
    (f"{PB}.cause_seasoned", [
        ("Phytophthora capsici, a fungus-like oomycete (water mold).", [("PP", 11)]),
        ("It spreads rapidly through water, including rain and irrigation that splash infested soil onto plants and fruit.", [("PP", 12), ("PP", 14)]),
        ("Its oospores can persist in soil for more than 10 years.", [("PP", 15)]),
        ("Culls and plant debris can also become a significant source of the pathogen.", [("PP", 16)]),
        ("Saturated soil and warm temperatures favor it.", [("PP", 9)]),
    ]),
    (f"{PB}.cause_beginner", [
        ("A fungus-like organism that lives in the soil and spreads in water, especially splashing rain and irrigation.", [("PP", 11), ("PP", 12), ("PP", 14)]),
        ("It can survive in the soil for more than 10 years.", [("PP", 15)]),
        ("It does best in warm weather and soggy soil.", [("PP", 9)]),
    ]),
    (f"{PB}.organic_treatment_seasoned", [
        ("Home gardeners have no effective chemical control options, so control relies on resistant varieties and cultural practices.", [("PP", 21)]),
        ("Remove diseased plants and fruit from the garden.", [("PP", 18)]),
        ("Don't leave culls on the ground or near ponds or creeks.", [("PP", 19)]),
    ]),
    (f"{PB}.organic_treatment_beginner", [
        ("No spray works for this in a home garden, so prevention is what counts.", [("PP", 21)]),
        ("Pull diseased plants and rotted fruit and take them out of the garden.", [("PP", 18), ("PP", 19)]),
    ]),
    (f"{PB}.prevention_seasoned", [
        ("Choose resistant varieties; some bell, sweet and hot peppers have moderate resistance.", [("PP", 37), ("PP", 38)]),
        ("Plant on well-drained, level ground where water won't stand.", [("PP", 17)]),
        ("Use raised beds and plastic mulch whenever possible.", [("PP", 23)]),
        ("Irrigate moderately by drip, and avoid overhead watering, especially once fruit forms.", [("PP", 27), ("PP", 28)]),
        ("Don't irrigate from ponds or creeks, which may carry the pathogen.", [("PP", 39)]),
        ("The pathogen's broad host range, including eggplant, tomato, beans and most cucurbits, makes rotation much less effective.", [("PP", 33), ("PP", 35)]),
        ("Rotate to cereals such as corn or wheat, which are not hosts.", [("PP", 33), ("PP", 34)]),
    ]),
    (f"{PB}.prevention_beginner", [
        ("Choose a pepper variety with some resistance to this disease.", [("PP", 37), ("PP", 38)]),
        ("Plant where water drains away and doesn't pool.", [("PP", 17)]),
        ("Raised beds covered with plastic mulch help.", [("PP", 23)]),
        ("Water at the soil with a drip line, and don't overwater.", [("PP", 27)]),
        ("This disease also attacks eggplant, tomatoes, beans and most squash and melons, so moving peppers to a new spot helps less.", [("PP", 33), ("PP", 35)]),
        ("Corn and wheat don't get it, so they're good crops for that spot.", [("PP", 33), ("PP", 34)]),
    ]),
    (f"{PB}.control_ladder[method=improve_drainage].note_seasoned", [
        ("Plant on well-drained, level ground where water won't stand.", [("PP", 17)]),
        ("Use raised beds where possible.", [("PP", 23)]),
        ("Saturated soil favors the disease.", [("PP", 9)]),
    ]),
    (f"{PB}.control_ladder[method=improve_drainage].note_beginner", [
        ("Plant where water drains away and doesn't pool.", [("PP", 17)]),
        ("Raised beds help, because this disease does best in soggy soil.", [("PP", 23), ("PP", 9)]),
    ]),
    (f"{PB}.control_ladder[method=water_at_the_base].note_seasoned", [
        ("Irrigate moderately by drip and avoid overhead watering, especially once fruit forms.", [("PP", 27), ("PP", 28)]),
        ("Rain and overhead irrigation can splash infested soil onto developing fruit and infect it.", [("PP", 14)]),
    ]),
    (f"{PB}.control_ladder[method=water_at_the_base].note_beginner", [
        ("Water at the soil with a drip line, and don't overwater.", [("PP", 27)]),
        ("Splashing water can throw infected soil onto the peppers.", [("PP", 14)]),
    ]),
    (f"{PB}.control_ladder[method=splash_barrier_mulch].note_seasoned", [
        ("NC State recommends plastic mulch on raised beds where possible.", [("PP", 23)]),
        ("Infection can start anywhere splashing water throws soil onto the plant.", [("PP", 1), ("PP", 32)]),
    ]),
    (f"{PB}.control_ladder[method=splash_barrier_mulch].note_beginner", [
        ("Lay plastic mulch over a raised bed if you can.", [("PP", 23)]),
        ("Water splashing up from the soil can carry the disease onto the plant.", [("PP", 1), ("PP", 32)]),
    ]),
    (f"{PB}.control_ladder[method=crop_rotation].note_seasoned", [
        ("The pathogen's broad host range, including eggplant, tomato, beans and most cucurbits, makes rotation much less effective.", [("PP", 33), ("PP", 35)]),
        ("Oospores can persist in soil for more than 10 years.", [("PP", 15)]),
        ("If you rotate, rotate to cereals such as corn or wheat, which are not hosts.", [("PP", 34)]),
    ]),
    (f"{PB}.control_ladder[method=crop_rotation].note_beginner", [
        ("This disease attacks many garden crops and can live in the soil for more than 10 years, so rotating helps less.", [("PP", 33), ("PP", 35), ("PP", 15)]),
        ("If you rotate, plant corn or wheat in that spot, since they don't get it.", [("PP", 34)]),
    ]),
    (f"{PB}.control_ladder[method=garden_sanitation].note_seasoned", [
        ("Remove diseased plants and fruit from the garden, and don't leave culls on the ground or near ponds or creeks.", [("PP", 18), ("PP", 19)]),
        ("Culls and debris can become a significant source of the pathogen.", [("PP", 16)]),
    ]),
    (f"{PB}.control_ladder[method=garden_sanitation].note_beginner", [
        ("Pull any plant that wilts and dies, along with rotted fruit, and take them out of the garden.", [("PP", 18), ("PP", 4)]),
        ("Don't leave them lying on the ground.", [("PP", 19)]),
    ]),
]
PEPPERS = ("bell-pepper", "banana-pepper")
for _c in PEPPERS:
    for _p, _s in PEPPER:
        LEAVES.append((_c, _p, _s))

# the citation block of each edited leaf / value, as ruled (a list, in order)
SOURCES = {
    ("watermelon", THIN): ["usu_ext", "umn_ext", "uga_ext", "uf_ifas"],
    ("watermelon", ROW): ["uf_ifas"],
    ("bell-pepper", PB): ["ncsu_ext_phytophthora_blight_peppers", "umn_ext"],
    ("banana-pepper", PB): ["ncsu_ext_phytophthora_blight_peppers", "umn_ext"],
}
