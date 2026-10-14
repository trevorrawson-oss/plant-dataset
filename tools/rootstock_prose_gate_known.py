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
# 10 waivers on 6 crops. (19 measured on 5420479d; PLA-625 stop 2, ruling 1b, 2026-10-13, retired the 7 own-root
# waivers -- lime, persimmon x2, mulberry x3, pawpaw -- when own-root wording became a propagation mode, each proven STALE.
# PLA-625 citrus promote 1, 2026-10-13, retired grapefruit's two sour orange note waivers when the note was re-authored,
# each proven STALE on the post-state 2f67359e.)
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
]
# Retired BY CONTENT, kept by identity so a LANDED promote can replay against the set live in its era
# (rootstock_prose_gate.KNOWN_AT_ARMING; the A62 precedent, e47e58a): every post-state before the retiring promote still
# carries the sentence. Never re-waived: live gating uses WAIVERS alone. Waivers retired by a GATE change (the 7
# own-root, stop 2) are not listed: they fire on no earlier state either.
CLOSED = [
    {"crop": "grapefruit", "field": "recommended_rootstock_note", "name": "sour orange", "sentence": "Grapefruit grows vigorously and yields well on Swingle citrumelo, which resists Phytophthora and citrus nematode and tolerates the tristeza virus that killed off the once-standard sour orange rootstock for grapefruit.", "ticket": "PLA-612", "reason": "HELD (ruling 2026-09-25): grapefruit's note names sour orange; held until its rows are re-sourced (PLA-612, promote 1).", "closed_by": "PLA-625 citrus promote 1, 59010fe6 -> 2f67359e: note re-authored without sour orange"},
    {"crop": "grapefruit", "field": "recommended_rootstock_note", "name": "Sour orange", "sentence": "Sour orange still produces excellent grapefruit where tristeza is not a threat.", "ticket": "PLA-612", "reason": "HELD (ruling 2026-09-25): grapefruit's note names sour orange; held until its rows are re-sourced (PLA-612, promote 1).", "closed_by": "PLA-625 citrus promote 1, 59010fe6 -> 2f67359e: note re-authored without sour orange"},
]
