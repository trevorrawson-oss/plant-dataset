"""rootstock_prose_gate_known -- the MEASURED waiver ledger and population for tools/rootstock_prose_gate.py (PLA-608).

Re-measured on canonical 5420479d (citrus/rootstock pass stop 1, PLA-625 ruling 2026-10-09), NOT copied from the
ticket. Each waiver is keyed on crop + field + name + the EXACT sentence carrying the name (the character): reword the
sentence and the name fails while the waiver reports STALE. Each carries its ticket and a one-line reason. A content
fix retires its waiver; the gate reports it STALE as it lands, and the entry is deleted in that same promote.

POPULATION is the measured set of crops carrying a `rootstock_options` key, BY IDENTITY: a crop leaving it refuses the
run (a strip-one-add-one swap cannot hold a count); a crop joining it is inspected and reported.
"""
TICKET = "PLA-608"
MEASURED_ON = "5420479d85bb8b65be62fa459fd97b8ce12dfdf9d3951e455be52aadc7a98063"
POPULATION = (
    "apple",
    "apricot",
    "avocado",
    "cherry-sour",
    "cherry-sweet",
    "fig",
    "grapefruit",
    "lemon",
    "lime",
    "mandarin-clementine",
    "mulberry",
    "nectarine",
    "olive",
    "orange-navel",
    "pawpaw",
    "peach",
    "pear-asian",
    "pear-european",
    "persimmon",
    "plum",
    "pomegranate",
)
# 19 waivers on 10 crops.
WAIVERS = [
    {"crop": "apple", "field": "container_notes.notes_beginner", "name": "M27", "sentence": "Only the smallest apple trees do well in pots, the ones grown on a dwarfing rootstock (ask the nursery for M9 or M27).", "ticket": "PLA-608", "reason": "NEW on 5420479d, found by the stop-1 container_notes widening: M27 is named for the smallest pots and apple's list has no M27 row. Add a sourced row or rephrase (content call)."},
    {"crop": "apple", "field": "container_notes.notes_seasoned", "name": "M27", "sentence": "Containers suit apple only on a true dwarfing rootstock (M9, or M27 for the smallest pots); a semi-dwarf or standard tree will outgrow any practical pot.", "ticket": "PLA-608", "reason": "NEW on 5420479d, found by the stop-1 container_notes widening: M27 is named for the smallest pots and apple's list has no M27 row. Add a sourced row or rephrase (content call)."},
    {"crop": "lemon", "field": "recommended_rootstock_note", "name": "macrophylla", "sentence": "Tristeza virus is a lemon problem rather than a rootstock one: lemon trees are susceptible to severe tristeza strains whatever the rootstock, and also to milder strains when grown on macrophylla or rough lemon.", "ticket": "PLA-608", "reason": "STANDING (ruling 2026-09-25, KEEP): the note is faithful to HS402's Tristeza sentence, which names macrophylla."},
    {"crop": "lemon", "field": "recommended_rootstock_note", "name": "rough lemon", "sentence": "Tristeza virus is a lemon problem rather than a rootstock one: lemon trees are susceptible to severe tristeza strains whatever the rootstock, and also to milder strains when grown on macrophylla or rough lemon.", "ticket": "PLA-608", "reason": "STANDING (ruling 2026-09-25, KEEP): the note is faithful to HS402's Tristeza sentence, which names rough lemon."},
    {"crop": "plum", "field": "rootstock_options[name=Guardian / Nemaguard (peach seedling, Southeast)].traits_seasoned", "name": "Lovell", "sentence": "Peach-seedling rootstocks used for plum in the Southeast, where Clemson recommends Nemaguard or Guardian in the Coastal Plain to resist root-knot nematodes (Lovell, Halford, or Guardian elsewhere to reduce bacterial canker).", "ticket": "PLA-608", "reason": "STANDING (ruling 2026-09-25, KEEP): an accurate report of Clemson; Lovell is a candidate row later (UC Davis plum page)."},
    {"crop": "plum", "field": "rootstock_options[name=Guardian / Nemaguard (peach seedling, Southeast)].traits_seasoned", "name": "Halford", "sentence": "Peach-seedling rootstocks used for plum in the Southeast, where Clemson recommends Nemaguard or Guardian in the Coastal Plain to resist root-knot nematodes (Lovell, Halford, or Guardian elsewhere to reduce bacterial canker).", "ticket": "PLA-608", "reason": "STANDING (ruling 2026-09-25, KEEP): an accurate report of Clemson's sentence naming Halford."},
    {"crop": "apricot", "field": "rootstock_options[name=Lovell (peach seedling)].traits_seasoned", "name": "Nemaguard", "sentence": "More tolerant of bacterial canker than the plum stocks or Nemaguard, and vigorous on well-drained ground, so it is a good choice where canker pressure is high.", "ticket": "PLA-566", "reason": "DEFERRED (ruling 2026-09-25): a comparison on the Lovell row; waived until PLA-566 re-authors apricot's rootstocks."},
    {"crop": "pear-asian", "field": "recommended_rootstock_note", "name": "quince", "sentence": "Note that quince, the dwarfing stock used for some European pears, is graft-incompatible with most Asian pears, so it is not an option here.", "ticket": "PLA-608", "reason": "STANDING handling case: quince is named in order to EXCLUDE it (graft-incompatible). Rewording the exclusion retires this waiver."},
    {"crop": "lime", "field": "recommended_rootstock_note", "name": "alemow", "sentence": "On the deep sands and calcareous rocklands where limes are often grown, UF/IFAS favors rough lemon, Volkamer lemon, alemow, or Rangpur lime; on neutral-to-low-pH soils, Swingle citrumelo adds foot-rot and tristeza resistance and some cold tolerance.", "ticket": "PLA-608", "reason": "PENDING the alemow row (ruling 1 refined 2026-09-25): ends when lime's sourced alemow row lands (promote 2)."},
    {"crop": "lime", "field": "recommended_rootstock_note", "name": "Rangpur lime", "sentence": "On the deep sands and calcareous rocklands where limes are often grown, UF/IFAS favors rough lemon, Volkamer lemon, alemow, or Rangpur lime; on neutral-to-low-pH soils, Swingle citrumelo adds foot-rot and tristeza resistance and some cold tolerance.", "ticket": "PLA-608", "reason": "PENDING the Rangpur fold (ruling 2026-09-25, stands): retires when Rangpur is folded into the rough lemon / Volkamer row."},
    {"crop": "lime", "field": "recommended_rootstock_note", "name": "own roots", "sentence": "Key lime is often grown on its own roots from seed, cuttings, or air-layers rather than grafted.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class, not in Part 1's table): Key lime 'on its own roots' with no own-root row. For ruling."},
    {"crop": "persimmon", "field": "rootstock_options[name=Diospyros virginiana (American persimmon)].traits_seasoned", "name": "own roots", "sentence": "Native D. virginiana is very cold-hardy and more tolerant of heavy, wet soils and root rot than kaki on its own roots, and it improves anchorage.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): a comparison, kaki 'on its own roots' vs on D. virginiana; no own-root row. For ruling."},
    {"crop": "persimmon", "field": "rootstock_options[name=Diospyros virginiana (American persimmon)].traits_beginner", "name": "own roots", "sentence": "Native persimmon roots are very cold-hardy and handle heavy, wet soil and root rot better than the Asian type on its own roots.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): a comparison, kaki 'on its own roots' vs on D. virginiana; no own-root row. For ruling."},
    {"crop": "mulberry", "field": "recommended_rootstock_note", "name": "from hardwood cuttings", "sentence": "Mulberries root readily from hardwood cuttings, so many are grown own-root; named cultivars are also grafted or budded onto seedling Morus alba or rubra, mainly for propagation, not to dwarf the tree.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): the note says many are grown own-root; the list holds only Morus seedling. For ruling."},
    {"crop": "mulberry", "field": "recommended_rootstock_note", "name": "own-root", "sentence": "Mulberries root readily from hardwood cuttings, so many are grown own-root; named cultivars are also grafted or budded onto seedling Morus alba or rubra, mainly for propagation, not to dwarf the tree.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): the note says many are grown own-root; the list holds only Morus seedling. For ruling."},
    {"crop": "mulberry", "field": "recommended_rootstock_note", "name": "own-root", "sentence": "On an own-root tree there is no graft union to keep above the soil, and any suckers are the same variety.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): the note says many are grown own-root; the list holds only Morus seedling. For ruling."},
    {"crop": "pawpaw", "field": "recommended_rootstock_note", "name": "ungrafted", "sentence": "An ungrafted seedling is a cheaper way to a tree, but expect variable fruit and a wait of about 5 to 8 years instead of around 4 for a grafted variety.", "ticket": "PLA-608", "reason": "NEW on 5420479d (own-root class): 'an ungrafted seedling' beside the grafted-seedling row only. For ruling."},
    {"crop": "grapefruit", "field": "recommended_rootstock_note", "name": "sour orange", "sentence": "Grapefruit grows vigorously and yields well on Swingle citrumelo, which resists Phytophthora and citrus nematode and tolerates the tristeza virus that killed off the once-standard sour orange rootstock for grapefruit.", "ticket": "PLA-612", "reason": "HELD (ruling 2026-09-25): grapefruit's note names sour orange; held until its rows are re-sourced (PLA-612, promote 1)."},
    {"crop": "grapefruit", "field": "recommended_rootstock_note", "name": "Sour orange", "sentence": "Sour orange still produces excellent grapefruit where tristeza is not a threat.", "ticket": "PLA-612", "reason": "HELD (ruling 2026-09-25): grapefruit's note names sour orange; held until its rows are re-sourced (PLA-612, promote 1)."},
]
