"""PLA-673 approved definitions (claude.ai, approved by Trevor 2026-10-05), VERBATIM, each sentence with the packet
quotes it maps to (P1 = packet 1, P2 = packet 2, numbered as posted; S = SUPPLEMENT below, the three sentences the
2026-10-05 round-2 re-authoring cites). Round 2 (Trevor, 2026-10-05): hill beginner 2 -> 2 + 2b; hill seasoned + 2b;
hilling beginner 4 -> 4 + 4b; hilling seasoned 7 replaced. Sources are document-level ids only (STOP 2, option (a) widened). Read by the glossary promote stage and its
evidence check. Do not edit a sentence here without a new ruling."""
DEFINITIONS = {
    "hill": {
        "term": "hill",
        "definition_beginner": [
            ("A hill is a small group of seeds planted together in one spot.", "P1", [16, 9, 35]),
            ("Once the seedlings come up, you remove the weaker ones and keep the strongest one to three plants.", "P1", [47, 10, 18, 4]),
            ("Snip or pinch off the extras instead of pulling them, so you don't disturb the roots of the plants you keep.", "S", ["S1", "S2"]),
            ("Some guides raise the soil into a low mound for each hill so extra water drains away.", "P1", [8, 20, 1]),
            ("Others treat a hill as just the group of plants, with no mound.", "P1", [13]),
            ("The distance between hills is measured from one planted group to the next.", "P1", [3, 36]),
        ],
        "definition_seasoned": [
            ("Hill: several seeds sown together in one spot, with the spots set at regular intervals.", "P1", [16]),
            ("After emergence, each hill is thinned to its strongest plants: one or two in NC State's handbook, two or three in the CSU and Purdue guides, and one to three in NMSU's.", "P1", [18, 10, 4, 47]),
            ("Clip or pinch the extras rather than pulling them, to avoid damaging the roots of the seedlings that stay (NC State, CSU).", "S", ["S1", "S2"]),
            ("Sources differ on whether a hill is raised.", "P1", [8, 20, 1, 13, 46]),
            ("CSU uses hills or mounds to drain excess water away from seedlings.", "P1", [8]),
            ("UGA's pumpkin guide raises the soil a few inches into a gentle mound for drainage.", "P1", [20]),
            ("Purdue forms a low, broad hill about 8 to 10 inches high.", "P1", [1]),
            ("UGA's home gardening bulletin defines a hill as a cluster of plants rather than a mound of soil.", "P1", [13]),
            ("NMSU sows each hill in a hole made with a hoe.", "P1", [46]),
            ("Hill spacing is the distance from one hill to the next.", "P1", [3, 36]),
        ],
        "sources": ["ncsu_ext_handbook_vegetable", "csu_ext_cucurbits_07609", "purdue_ext_ho8wa", "nmsu_ext_cr457",
                    "uga_c1206_homegrown_pumpkins", "uga_b577_home_gardening", "umn_ext_cucumbers"],
    },
    "hilling": {
        "term": "hilling",
        "definition_beginner": [
            ("Hilling means piling soil up around plants as they grow.", "P2", [1, 14]),
            ("Potatoes are hilled so the potatoes growing near the surface stay covered, because light turns them green.", "P2", [2]),
            ("Leeks are hilled to grow a longer white stem.", "P2", [13, 16]),
            ("Some carrot varieties push the tops of their roots up out of the soil.", "P2", [12, "S3"]),
            ("Hilling soil around them keeps the roots from turning green.", "P2", [12]),
            ("Very tall corn can be hilled to help keep it from blowing over.", "P2", [18]),
            ("The mound you build around potato plants is also called a hill.", "P2", [8]),
        ],
        "definition_seasoned": [
            ("Hilling: drawing soil or compost up around growing plants, usually several times a season.", "P2", [14, 4, 15]),
            ("For potato, UMN starts when stems are about a foot tall and hills once or twice more, building six to eight inches of soil in total.", "P2", [4, 5]),
            ("Hilling keeps shallow tubers out of the light so they don't turn green.", "P2", [2]),
            ("More buried main stem also means more stolons.", "P2", [3]),
            ("NMSU keeps at least three-quarters of the foliage above the soil line.", "P2", [11]),
            ("Leeks get 2 to 3 inches of soil two or three times a season for a longer blanched shaft (USU).", "P2", [15, 16]),
            ("On carrot varieties that push their root tops out of the soil, hilling keeps the roots from turning green (UMN).", "P2", [12, "S3"]),
            ("On very tall heirloom dent corn, hilling plus wider spacing helps keep plants from blowing over (Clemson).", "P2", [18]),
            ("The trench method replaces mounding: plant in a shallow trench or furrow and fill it in as plants grow (UMN, NMSU).", "P2", [6, 7, 13, 10]),
            ("The hilled mound on potatoes is itself called a hill.", "P2", [8]),
            ("Planting \"in hills\" is a different practice, even though NC State's handbook calls it hilling too.", "P1", [15, 16]),
        ],
        "sources": ["umn_ext_potatoes", "umn_ext_carrots_parsnips", "umn_ext_leeks", "usu_ext_leeks", "nmsu_ext_cr457",
                    "clemson_hgic_homegrown_grits", "ncsu_ext_handbook_vegetable"],
    },
}

# The supplementary quotes (not in packets 1/2): (key, source page key in build_packets.SRC, verbatim norm_text quote).
SUPPLEMENT = {
    "S1": ("ncsu", "pinch or cut out seedlings rather than pulling them out of the soil to avoid potentially damaging nearby root systems."),
    "S2": ("csu", "clip plants during thinning to avoid disturbing the roots nearby seedlings."),
    "S3": ("umn_carrot", "some carrot varieties will push the tops of the roots up out of the soil."),
}
