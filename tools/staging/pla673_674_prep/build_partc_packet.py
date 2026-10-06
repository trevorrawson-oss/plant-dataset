"""PLA-673 part C prep (read-only): the watermelon row-entry re-author packet. Every hashed T1 in-row / between-row figure
for watermelon (the 5a table), each table row quoted WITH its header so the column reading is proven, plus every consumer
leaf that restates the current row figures. Every quote proven against its hashed bytes (build_packets.locate)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_packets as bp  # noqa: E402

SRC = {  # key: (url, label, cited on watermelon?)
    "clemson": ("https://hgic.clemson.edu/factsheet/watermelon/", "Clemson HGIC Watermelon [clemson_hgic] (the CURRENT row entry's source)", True),
    "wsu": ("https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf", "WSU Home Vegetable Gardening in Washington, table 4 [wsu_ext]", True),
    "uf": ("https://edis.ifas.ufl.edu/publication/VH021", "UF/IFAS VH021 Florida Vegetable Gardening Guide, table 1 [uf_ifas]", True),
    "vt": ("https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "VCE 426-331, table 5 [vt_ext]", True),
    "osu": ("https://ir.library.oregonstate.edu/downloads/v979v342w", "OSU Growing Your Own planting chart [osu_ext]", True),
    "cr457b": ("https://pubs.nmsu.edu/_circulars/CR457B/", "NMSU Circular 457-B [nmsu_ext_cr457b]", False),
    "b577chart": ("https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf", "UGA B577 Home Garden Planting Chart [uga_b577]", False),
    "c1035": ("https://fieldreport.caes.uga.edu/publications/C1035/", "UGA C1035 [uga_ext] (the hill entry's source)", True),
    "cr457": ("https://pubs.nmsu.edu/_circulars/CR457.pdf", "NMSU Circular 457 [nmsu_ext_cr457, staged mint]", False),
}
ROWS = [  # (src, kind, quote)
    ("clemson", "between rows", "seeds or transplants should be planted in rows spaced 6 to 8 feet apart."),
    ("clemson", "in-row", "plants should be spaced 5 to 6 feet apart within the row."),
    ("wsu", "header", "distance between plants (inch) distance between rows (inch)"),
    ("wsu", "row: 24-36 in / 48-60 in", "watermelon 1-11⁄2 24-36 48-60"),
    ("uf", "header", "spacing (inches) seed depth (inches) transplant ability 5 plant family 6 north central south plants rows"),
    ("uf", "row: 24-48 in / 60 in", "watermelon late mar-apr july-aug jan-mar dec-mar 40 3-5 80-100 (60-90) 24-48 60"),
    ("vt", "header", "crop distance between plants in row distance between rows"),
    ("vt", "row: 3-4 ft / 5-10 ft", "watermelon 3-4 ft 5-10 ft"),
    ("osu", "header", "distance between rowsc distance apart in the row"),
    ("osu", "row: rows 72 in / in-row 60 in", "watermelons 4 weeks not suitable may not suitable may 6 plants 72\" 60\""),
    ("cr457b", "header", "distance between plants in rows (in.) distance between rows (in.)"),
    ("cr457b", "row: 24-36 in / 72-96 in", "watermelon 82 1 24-36 72-96"),
    ("b577chart", "header", "distance between rows distance between plants depth to plant"),
    ("b577chart", "row: rows 10 ft / plants 8-10 ft (hill scale)", "watermelon 80-90 mar. 20-may 1 not recommended 1 oz. 10 ft 8-10 ft"),
    ("c1035", "hills (context: the default layout)", "plant watermelon from seed in small hills with a spacing of 8 ft on all sides."),
    ("cr457", "room to spread (context)", "watermelons require more room to spread than cantaloupes-at least 8-10 ft."),
]


def main(path):
    sha = {k: next((s for s, us in bp.MAN.items() if u in us), None) for k, (u, _, _) in SRC.items()}
    w = next(c for c in bp.DATA["crops"] if c["slug"] == "watermelon")
    row = next(e for e in w["planting_layout"] if e["id"] == "row-none")
    out = ["# PLA-673 part C packet: watermelon row-entry re-author", "",
           "Read-only on canonical `350eda38`. **Nothing changed, nothing authored.** Every quote is `norm_text`, machine-checked as a "
           "substring of the page's hashed bytes; each table row is quoted WITH its header so the column reading is proven.", "",
           "## The entry today", "",
           f"`planting_layout[id=row-none]`: in_row_inches {row['in_row_inches']}, row_spacing_inches {row['row_spacing_inches']}, "
           f"sources {row['sources']} (Clemson HGIC). Crop-root mirror `spacing_inches` = {w['spacing_inches']} (the row entry's "
           f"in-row figure; `row_spacing_inches` = {w['row_spacing_inches']} mirrors the DEFAULT hill entry).", "",
           "## Hashed T1 in-row and between-row figures", "",
           "| # | page | cited on watermelon | kind | verbatim (norm_text) | location |", "| -- | -- | -- | -- | -- | -- |"]
    n = 0
    for src, kind, quote in ROWS:
        u, label, cited = SRC[src]
        q, loc = bp.locate(sha[src], u, quote)
        n += 1
        out.append(f"| {n} | {label} `{sha[src][:8]}` | {'yes' if cited else 'NO'} | {kind} | \"{q}\" | {loc} |")
    out += ["", "## Summary (in-row x between rows)", "",
            "| page | in-row | rows | per plant |", "| -- | -- | -- | -- |",
            "| Clemson (entry) | 60-72 in | 72-96 in | 30-48 sq ft |",
            "| WSU | 24-36 in | 48-60 in | 8-15 sq ft |",
            "| UF VH021 | 24-48 in | 60 in | 10-20 sq ft |",
            "| VT 426-331 | 36-48 in | 60-120 in | 15-40 sq ft |",
            "| OSU chart | 60 in | 72 in | 30 sq ft |",
            "| NMSU CR457B (not cited) | 24-36 in | 72-96 in | 12-24 sq ft |",
            "| UGA B577 chart (not cited) | 96-120 in | 120 in | hill scale |",
            "", "Per-plant area is in-row x rows, arithmetic, not a source figure. Hills today (C1035, 8 ft x 8 ft at 2 plants) = 32 sq ft per plant.", "",
            "## Consumer leaves that restate the row figures (crop, field, register)", "",
            "| crop | field | register | text |", "| -- | -- | -- | -- |",
            f"| watermelon | thinning.tip_seasoned | seasoned | \"{w['thinning']['tip_seasoned']}\" |", "",
            "Numeric (non-prose) carriers of the same figures: `planting_layout[id=row-none].in_row_inches` [60,72] and `.row_spacing_inches` "
            "[72,96]; the crop-root mirror `spacing_inches` [60,72] (consumers read it through the layout reader). No other watermelon consumer "
            "leaf states a row figure: the soil_prep leaves state the HILL figure (8 ft on all sides, C1035), and the rest of the distance-bearing "
            "leaves are depth, water, pot size or yield. The `thinning.tip_seasoned` icebox clause (24 to 36 inches) matches WSU and NMSU CR457B, "
            "not Clemson."]
    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"{path}: {n} quotes, all proven against hashed bytes")


main(sys.argv[1])
