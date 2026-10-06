# PLA-673 part C packet: watermelon row-entry re-author

Read-only on canonical `350eda38`. **Nothing changed, nothing authored.** Every quote is `norm_text`, machine-checked as a substring of the page's hashed bytes; each table row is quoted WITH its header so the column reading is proven.

## The entry today

`planting_layout[id=row-none]`: in_row_inches [60, 72], row_spacing_inches [72, 96], sources ['clemson_hgic'] (Clemson HGIC). Crop-root mirror `spacing_inches` = [60, 72] (the row entry's in-row figure; `row_spacing_inches` = [96, 96] mirrors the DEFAULT hill entry).

## Hashed T1 in-row and between-row figures

| # | page | cited on watermelon | kind | verbatim (norm_text) | location |
| -- | -- | -- | -- | -- | -- |
| 1 | Clemson HGIC Watermelon [clemson_hgic] (the CURRENT row entry's source) `77feea89` | yes | between rows | "seeds or transplants should be planted in rows spaced 6 to 8 feet apart." | char 69970 |
| 2 | Clemson HGIC Watermelon [clemson_hgic] (the CURRENT row entry's source) `77feea89` | yes | in-row | "plants should be spaced 5 to 6 feet apart within the row." | char 70043 |
| 3 | WSU Home Vegetable Gardening in Washington, table 4 [wsu_ext] `7378f653` | yes | header | "distance between plants (inch) distance between rows (inch)" | p. 10, char 17514 |
| 4 | WSU Home Vegetable Gardening in Washington, table 4 [wsu_ext] `7378f653` | yes | row: 24-36 in / 48-60 in | "watermelon 1-11⁄2 24-36 48-60" | p. 11, char 21621 |
| 5 | UF/IFAS VH021 Florida Vegetable Gardening Guide, table 1 [uf_ifas] `7ff585e6` | yes | header | "spacing (inches) seed depth (inches) transplant ability 5 plant family 6 north central south plants rows" | char 19776 |
| 6 | UF/IFAS VH021 Florida Vegetable Gardening Guide, table 1 [uf_ifas] `7ff585e6` | yes | row: 24-48 in / 60 in | "watermelon late mar-apr july-aug jan-mar dec-mar 40 3-5 80-100 (60-90) 24-48 60" | char 23790 |
| 7 | VCE 426-331, table 5 [vt_ext] `52fda56c` | yes | header | "crop distance between plants in row distance between rows" | char 18894 |
| 8 | VCE 426-331, table 5 [vt_ext] `52fda56c` | yes | row: 3-4 ft / 5-10 ft | "watermelon 3-4 ft 5-10 ft" | char 21338 |
| 9 | OSU Growing Your Own planting chart [osu_ext] `f2fdb1d6` | yes | header | "distance between rowsc distance apart in the row" | p. 1, char 172 |
| 10 | OSU Growing Your Own planting chart [osu_ext] `f2fdb1d6` | yes | row: rows 72 in / in-row 60 in | "watermelons 4 weeks not suitable may not suitable may 6 plants 72" 60"" | p. 1, char 4160 |
| 11 | NMSU Circular 457-B [nmsu_ext_cr457b] `cb59fcd1` | NO | header | "distance between plants in rows (in.) distance between rows (in.)" | char 10296 |
| 12 | NMSU Circular 457-B [nmsu_ext_cr457b] `cb59fcd1` | NO | row: 24-36 in / 72-96 in | "watermelon 82 1 24-36 72-96" | char 13302 |
| 13 | UGA B577 Home Garden Planting Chart [uga_b577] `a9ed2655` | NO | header | "distance between rows distance between plants depth to plant" | p. 1, char 90 |
| 14 | UGA B577 Home Garden Planting Chart [uga_b577] `a9ed2655` | NO | row: rows 10 ft / plants 8-10 ft (hill scale) | "watermelon 80-90 mar. 20-may 1 not recommended 1 oz. 10 ft 8-10 ft" | p. 1, char 2472 |
| 15 | UGA C1035 [uga_ext] (the hill entry's source) `12164061` | yes | hills (context: the default layout) | "plant watermelon from seed in small hills with a spacing of 8 ft on all sides." | char 97845 |
| 16 | NMSU Circular 457 [nmsu_ext_cr457, staged mint] `25dbbeb4` | NO | room to spread (context) | "watermelons require more room to spread than cantaloupes-at least 8-10 ft." | p. 16, char 71853 |

## Summary (in-row x between rows)

| page | in-row | rows | per plant |
| -- | -- | -- | -- |
| Clemson (entry) | 60-72 in | 72-96 in | 30-48 sq ft |
| WSU | 24-36 in | 48-60 in | 8-15 sq ft |
| UF VH021 | 24-48 in | 60 in | 10-20 sq ft |
| VT 426-331 | 36-48 in | 60-120 in | 15-40 sq ft |
| OSU chart | 60 in | 72 in | 30 sq ft |
| NMSU CR457B (not cited) | 24-36 in | 72-96 in | 12-24 sq ft |
| UGA B577 chart (not cited) | 96-120 in | 120 in | hill scale |

Per-plant area is in-row x rows, arithmetic, not a source figure. Hills today (C1035, 8 ft x 8 ft at 2 plants) = 32 sq ft per plant.

## Consumer leaves that restate the row figures (crop, field, register)

| crop | field | register | text |
| -- | -- | -- | -- |
| watermelon | thinning.tip_seasoned | seasoned | "Sow three to four seeds per hill and thin to the strongest two once they have a true leaf or two. Snip the extras off at soil line rather than pulling, so you do not disturb the roots of the keepers. In rows, thin to one plant every 24 to 36 inches for icebox types and 5 to 6 feet for full-size vines." |

Numeric (non-prose) carriers of the same figures: `planting_layout[id=row-none].in_row_inches` [60,72] and `.row_spacing_inches` [72,96]; the crop-root mirror `spacing_inches` [60,72] (consumers read it through the layout reader). No other watermelon consumer leaf states a row figure: the soil_prep leaves state the HILL figure (8 ft on all sides, C1035), and the rest of the distance-bearing leaves are depth, water, pot size or yield. The `thinning.tip_seasoned` icebox clause (24 to 36 inches) matches WSU and NMSU CR457B, not Clemson.