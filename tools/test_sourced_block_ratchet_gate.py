#!/usr/bin/env python3
"""Tests for sourced_block_ratchet_gate -- the PLA-607 identity ratchet over every NAMED sourced
block type, with the PLA-533 container pot-size ratchet folded in.

TDD: written and run RED before the module existed (ModuleNotFoundError, 2026-09-30).

THE RULE (PLA-607; Trevor 2026-09-25 and 2026-09-30). On a CERTIFIED crop, a block carrying
authored content whose citation slot is missing, null or [] is UNCITED. Today's uncited blocks are
waived BY IDENTITY; any other uncited block fails and names itself. A block that is absent or null
is not uncited. companions / zones / regions are RULED OUT. launch_ready is untouched (§G).

MEASURED 2026-09-30 on canonical 00dda31c: 7063 named blocks inspected on 121 certified crops,
2634 uncited, on all 121. The ticket's "98 slots on 57 crops" is the SLOT-PRESENT subset ([] or
null); the fourth absence state, a missing key, is the other 2536, and it is the one a naive key
walk misses. The 98 is reconciled inside the 2634 by an independent walk below.
"""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sourced_block_ratchet_gate as G  # noqa: E402

CANON = os.path.join(REPO, "crops_data_final.json")
SHA = "00dda31cc6616b9ea865f04fe0ce97fb1fb5d821f0c94724d3a03dbad8c8dd8e"
VICTIM = "cabbage"          # storage / watering / varieties / pests are cited on it
POT_KNOWN = ("dry-bean", "grapefruit", "green-beans-bush", "orange-navel")

# Per-family uncited counts on 00dda31c, enumerated as literals, never computed from the gate.
FAMILY_COUNTS = {
    # growth_stages 613 -> 612: PLA-673 B2 cited parsnip|growth_stages[id=established]
    "growth_stages[]": 612, "notifications[]": 458, "tips_by_stage.*[]": 312,
    "weather_triggers[]": 289, "failure_diagnostics[]": 251, "description": 108,
    "harvest_urgency": 108, "start_method": 101, "succession_policy": 86,
    "varieties.recommended[]": 77, "pests[]": 54, "diseases[]": 50, "harvest_ready": 26,
    "watering": 17, "bolting": 13, "container_notes": 12, "varieties": 12, "fertilizer": 11,
    "pollination": 9, "rotation": 8, "verification_status.field_additions[]": 3, "thinning": 3,
    "soil": 2, "storage": 2, "yield_expectations": 2, "ph": 2,
    "soil_prep": 35,   # armed 2026-10-06 (PLA-673 B2): the 35 null-citation crops, measured on aaf004a2
}


def canon():
    with open(CANON, encoding="utf-8") as f:
        return json.load(f)


_CANON = canon()


def fresh():
    return copy.deepcopy(_CANON)


def by(data):
    return {c["slug"]: c for c in data["crops"]}


def family_of(ident):
    _slug, path, _field = ident.split("|")
    t = re.sub(r"\[[^\]]*\]", "[]", path)
    return re.sub(r"^tips_by_stage\.[^\[]+", "tips_by_stage.*", t)


def violations(data):
    return G.roster(data)[3]


def cite(block):
    block["sources"] = ["umn_ext"]
    block["anchoring_urls"] = {"umn_ext": {"url": "https://extension.umn.edu/x",
                                           "verified": "2026-09-30"}}


# claim keys of each crop-root sibling, typed here (independent of the gate's SIBLING_BLOCKS)
SIBLING_CLAIM_KEYS = {
    "description": ("description_beginner", "description_seasoned"),
    "harvest_ready": ("harvest_ready_beginner", "harvest_ready_seasoned"),
    "harvest_urgency": ("harvest_urgency",),
    "mature_dimensions": ("mature_height_ft", "mature_spread_ft"),
    "soil_prep": ("soil_prep_beginner", "soil_prep_seasoned"),
    "recommended_rootstock_note": ("recommended_rootstock_note",),
}


# ------------------------------------------------------------------------------------ pins
class PinsAreTheMeasurement(unittest.TestCase):
    def test_waiver_file_is_the_measured_population(self):
        self.assertEqual(G._KNOWN_DOC["measured_on"], SHA)
        # 2634 at arming (00dda31c); 2630 after housekeeping 60 Phase C cited 4 waived blocks (afbd4113);
        # 2629 after PLA-666 cited raspberry|start_method (350eda38); 2664 after PLA-673 B2 ARMED soil_prep with its
        # 35 measured null-citation crops (aaf004a2): growth by arming a newly named block type, ruled; the same
        # promote cited parsnip|growth_stages[id=established] (-1): 2629 + 35 - 1 = 2663
        self.assertEqual(G._KNOWN_DOC["count"], 2663)
        self.assertEqual(len(G.KNOWN), 2663)
        self.assertEqual(len(G._KNOWN_DOC["identities"]), 2663, "duplicate identities")

    def test_the_named_list_is_what_was_ruled(self):
        self.assertEqual(set(G.DICT_BLOCKS), {
            "bolting", "container_notes", "fertilizer", "harvest_stop_rule",
            "heat_threshold_temp_f", "indoor_cycle", "pet_safe", "ph", "photoperiod",
            "pollination", "rotation", "soil", "start_method", "storage", "succession_policy",
            "thinning", "varieties", "watering", "winter_hardiness", "yield_expectations"})
        self.assertEqual(set(G.SIBLING_BLOCKS), {"description", "harvest_ready", "harvest_urgency",
                                                 "mature_dimensions", "soil_prep", "recommended_rootstock_note"})
        # PLA-608 ruling 2 (2026-09-25) + PLA-625 stop-1 ruling (2026-10-09): the rootstock-note pair, NAMED in the
        # rootstock_prose_gate tools commit; the fields land with citrus promote 1 (null everywhere).
        self.assertEqual(G.SIBLING_BLOCKS["recommended_rootstock_note"], ("recommended_rootstock_note",))
        # PLA-674 (2026-10-05): the soil_prep citation pair, named in the glossary promote's tools commit.
        self.assertEqual(G.SIBLING_BLOCKS["soil_prep"], ("soil_prep_beginner", "soil_prep_seasoned"))
        # PLA-10 promote 3 (spec §4.3, plan 58 §8 T5): one crop-root pair cites both height fields.
        self.assertEqual(G.SIBLING_BLOCKS["mature_dimensions"], ("mature_height_ft", "mature_spread_ft"))
        self.assertEqual(set(G.ITEM_FAMILIES), {
            "pests", "diseases", "growth_stages", "failure_diagnostics", "notifications",
            "weather_triggers", "rootstock_options", "varieties.recommended",
            "container_notes.plants_per_pot.readings", "verification_status.field_additions",
            "planting_layout"})
        self.assertEqual(G.ITEM_FAMILIES["planting_layout"], (("planting_layout",), "id", None))

    def test_the_three_ruled_exclusions_and_only_those(self):
        """RULED 2026-09-30: out of the named list, each with its reason recorded."""
        self.assertEqual(set(G.EXCLUDED), {"companions", "zones", "regions"})
        for k, why in G.EXCLUDED.items():
            self.assertTrue(why.strip(), k)

    def test_anchor_only_fields_are_the_measured_seven(self):
        """Eight in the tools commit; PLA-10 promote 1 retired spacing_inches_anchoring_urls (its
        anchors moved into planting_layout entries, a named family)."""
        self.assertEqual(set(G.ANCHOR_ONLY), {
            "<crop>.anchoring_urls", "days_to_maturity_anchoring_urls",
            "days_to_maturity_mid_anchoring_urls", "det_indet.anchoring_urls",
            "germination_temp_f_anchoring_urls",
            "sunlight_hours_anchoring_urls", "weeks_indoors_anchoring_urls"})

    def test_pot_sub_rule_pins_are_the_folded_four(self):
        """Folded in from container_citation_floor_gate (PLA-533 ruling 1). Literals, never computed."""
        self.assertEqual(G.POT_CEILING, 4)
        self.assertEqual(tuple(sorted(G.POT_KNOWN)), POT_KNOWN)
        self.assertEqual(len(G.POT_KNOWN), G.POT_CEILING)

    def test_floor_is_below_the_measured_population(self):
        """Measured 7063 on 00dda31c. The floor is a literal, never derived from the run it bounds."""
        self.assertEqual(G.MIN_INSPECTED, 6500)


# ------------------------------------------------------- PLA-10 promote 3: the mature_dimensions sibling (T5)
def _sib(c, sid="ncsu_ext", url="https://plants.ces.ncsu.edu/plants/solanum-melongena/"):
    c["mature_dimensions_sources"] = [sid]
    c["mature_dimensions_anchoring_urls"] = {sid: {"url": url, "verified": "2026-10-02"}}


NULL_CROP = "carrot"


class MatureDimensionsSibling(unittest.TestCase):
    """spec §4.3: `mature_dimensions_sources` / `_anchoring_urls` cite mature_height_ft + mature_spread_ft.
    NAMED now (so the keys are not UNNAMED), RATCHETED only once MATURE_DIMENSIONS_ARMED flips, in the data
    commit that writes the siblings: armed on today's canonical, the 16 PLA-465 heights (no sibling yet)
    would each fail as a NEW uncited block and redden gate_all (gates arm off the data)."""

    # The injection victim: a certified crop with NO authored height (re-homed eggplant -> carrot 2026-10-03:
    # promote 3 authors eggplant, so an injected height there was already cited and the FAILS tests went green).
    def setUp(self):
        self.assertIsNone(by(_CANON)[NULL_CROP].get("mature_height_ft"))
        self.assertIsNone(by(_CANON)[NULL_CROP].get("mature_spread_ft"))

    def test_the_flag_matches_the_data(self):
        carrying = any("mature_dimensions_sources" in c for c in _CANON["crops"] if G.certified(c))
        self.assertEqual(G.MATURE_DIMENSIONS_ARMED, carrying,
                         "MATURE_DIMENSIONS_ARMED flips in the SAME commit that writes the siblings, never before")

    def test_the_sibling_keys_are_not_UNNAMED(self):
        d = fresh()
        _sib(by(d)[NULL_CROP])
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        self.assertEqual(G.unnamed_fields(by(d)[NULL_CROP]), [])

    def test_an_UNNAMED_height_citation_key_FAILS(self):
        """A key spelled per field (or misspelled) is not the ruled pair: naming is part of adding."""
        for k in ("mature_height_ft_sources", "mature_dimension_sources", "mature_spread_ft_anchoring_urls"):
            d = fresh()
            by(d)[NULL_CROP][k] = ["ncsu_ext"] if k.endswith("_sources") else {}
            v = violations(d)
            self.assertTrue(any(f"UNNAMED sourced field {k}" in m for m in v), (k, v))

    def test_armed_a_height_with_no_sibling_FAILS_by_name(self):
        d = fresh()
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        v = G.roster(d, mature_dimensions_armed=True)[3]
        self.assertTrue(any(f"{NULL_CROP}|mature_dimensions|mature_dimensions_sources" in m for m in v), v)

    def test_armed_a_spread_alone_with_no_sibling_FAILS(self):
        d = fresh()
        by(d)[NULL_CROP]["mature_spread_ft"] = [1, 2]
        v = G.roster(d, mature_dimensions_armed=True)[3]
        self.assertTrue(any(f"{NULL_CROP}|mature_dimensions|" in m for m in v), v)

    def test_armed_an_EMPTY_sibling_FAILS(self):
        d = fresh()
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        by(d)[NULL_CROP]["mature_dimensions_sources"] = []
        v = G.roster(d, mature_dimensions_armed=True)[3]
        self.assertTrue(any(f"{NULL_CROP}|mature_dimensions|" in m for m in v), v)

    def test_armed_a_cited_height_passes(self):
        d = fresh()
        for c in d["crops"]:
            if G.certified(c) and (c.get("mature_height_ft") or c.get("mature_spread_ft")):
                _sib(c)
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        _sib(by(d)[NULL_CROP])
        n, insp, live, V, stale, pot = G.roster(d, mature_dimensions_armed=True)
        self.assertEqual(V, [])

    def test_armed_the_live_canonical_cites_every_authored_height(self):
        """Positive control on the population (re-pointed 2026-10-03, promote 3's data commit; it was the
        pre-backfill control that exactly the 16 PLA-465 crops failed armed). Armed on the live canonical, every
        certified crop with an authored height or spread carries a CITED mature_dimensions block, none is
        uncited, and the population is at least the 59 promote 3 cites (43 new + 16 backfill; a floor, never
        derived from the run)."""
        V = G.roster(_CANON, mature_dimensions_armed=True)[3]
        self.assertEqual([m for m in V if "|mature_dimensions|" in m], [])
        want = {c["slug"] for c in _CANON["crops"] if G.certified(c)
                and (c.get("mature_height_ft") is not None or c.get("mature_spread_ft") is not None)}
        cited = {i.split("|")[0] for c in _CANON["crops"] if G.certified(c)
                 for i, ok in G.blocks(c, True) if "|mature_dimensions|" in i and ok}
        self.assertGreaterEqual(len(want), 59)
        self.assertEqual(cited, want)

    def test_unarmed_an_uncited_height_is_not_failed(self):
        """Re-pointed 2026-10-03 (promote 3's data commit): it read the LIVE canonical unarmed, which went vacuous
        once every live height is cited (the always-armed mutation survived it). An injected uncited height must
        fail armed and be invisible unarmed: the replayed promotes 1 and 2 rely on the unarmed branch."""
        d = fresh()
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        self.assertTrue(any("|mature_dimensions|" in m for m in G.roster(d, mature_dimensions_armed=True)[3]))
        self.assertFalse(any("|mature_dimensions|" in m for m in G.roster(d, mature_dimensions_armed=False)[3]))

    def test_unarmed_the_block_is_not_counted(self):
        d = fresh()
        by(d)[NULL_CROP]["mature_height_ft"] = [2, 4]
        self.assertFalse(any("|mature_dimensions|" in i for i, _ in G.blocks(by(d)[NULL_CROP], False)))
        self.assertTrue(any("|mature_dimensions|" in i for i, _ in G.blocks(by(d)[NULL_CROP], True)))


RR_CROP = "lemon"   # certified, carries an authored recommended_rootstock_note


class RecommendedRootstockNoteSibling(unittest.TestCase):
    """PLA-608 ruling 2 (2026-09-25; anchoring partner amended the same day) and the PLA-625 stop-1 ruling (2026-10-09):
    `recommended_rootstock_note_sources` / `_anchoring_urls` cite recommended_rootstock_note. NAMED now, in the
    rootstock_prose_gate tools commit, so the keys are never UNNAMED; RATCHETED only once
    RECOMMENDED_ROOTSTOCK_NOTE_ARMED flips, in the promote that writes the pair (citrus promote 1: null everywhere,
    three-state contract, register entry). Armed today, every authored note would fail as a NEW uncited block."""

    def setUp(self):
        self.assertIsInstance(by(_CANON)[RR_CROP].get("recommended_rootstock_note"), str)
        self.assertNotIn("recommended_rootstock_note_sources", by(_CANON)[RR_CROP])

    def test_the_flag_matches_the_data(self):
        carrying = any("recommended_rootstock_note_sources" in c for c in _CANON["crops"] if G.certified(c))
        self.assertEqual(G.RECOMMENDED_ROOTSTOCK_NOTE_ARMED, carrying,
                         "RECOMMENDED_ROOTSTOCK_NOTE_ARMED flips in the SAME commit that writes the pair, never before")

    def test_the_pair_is_not_UNNAMED_in_any_of_its_three_states(self):
        for srcs, anchors in ((None, None), ([], {}),
                              (["uf_ifas_hs1153"], {"uf_ifas_hs1153": {"url": "https://ask.ifas.ufl.edu/publication/HS402",
                                                                        "verified": "2026-10-09"}})):
            d = fresh()
            c = by(d)[RR_CROP]
            c["recommended_rootstock_note_sources"] = srcs
            c["recommended_rootstock_note_anchoring_urls"] = anchors
            self.assertEqual(G.unnamed_fields(c), [], (srcs, anchors))
            self.assertFalse(any("UNNAMED" in m for m in violations(d)), (srcs, anchors))

    def test_a_misspelled_pair_key_is_UNNAMED(self):
        """Naming is exact: the ruled pair is note-scoped, so a key spelled on the value field fails."""
        for k in ("recommended_rootstock_sources", "recommended_rootstock_anchoring_urls",
                  "recommended_rootstock_notes_sources"):
            d = fresh()
            by(d)[RR_CROP][k] = ["uf_ifas_hs1153"] if k.endswith("_sources") else {}
            self.assertTrue(any(f"UNNAMED sourced field {k}" in m for m in violations(d)), k)

    def test_armed_an_authored_note_with_a_null_or_empty_pair_FAILS_by_name(self):
        for srcs in (None, [], "absent"):
            d = fresh()
            c = by(d)[RR_CROP]
            if srcs != "absent":
                c["recommended_rootstock_note_sources"] = srcs
            ident = f"{RR_CROP}|recommended_rootstock_note|recommended_rootstock_note_sources"
            self.assertIn(ident, G.uncited(c, recommended_rootstock_note_armed=True), srcs)
            self.assertNotIn(ident, G.uncited(c, recommended_rootstock_note_armed=False), srcs)

    def test_armed_a_cited_note_is_not_uncited(self):
        d = fresh()
        c = by(d)[RR_CROP]
        c["recommended_rootstock_note_sources"] = ["uf_ifas_hs1153"]
        self.assertFalse(any("|recommended_rootstock_note|" in i
                             for i in G.uncited(c, recommended_rootstock_note_armed=True)))

    def test_unarmed_the_live_canonical_counts_no_note_block(self):
        self.assertFalse(any("|recommended_rootstock_note|" in i for c in _CANON["crops"] if G.certified(c)
                             for i, _ok in G.blocks(c)))


# ------------------------------------------------------- closures keep landed replays reproducible
CLOSED_2026_10_04 = {  # cited by housekeeping 60 Phase C (b331e5f2 -> afbd4113), dropped from the live waiver set
    "broad-beans-fava|start_method|sources", "sweet-corn|growth_stages[id=seedling]|sources",
    "watermelon|growth_stages[id=vining]|sources", "watermelon|tips_by_stage.vining[0]|sources"}
CLOSED_2026_10_05 = {"raspberry|start_method|sources"}  # cited by PLA-666 row figures (afbd4113 -> 350eda38)
CLOSED_SOIL_PREP = {  # armed 2026-10-06 (PLA-673 B2); cited before arming, so uncited in every earlier era
    "watermelon|soil_prep|soil_prep_sources", "pumpkin|soil_prep|soil_prep_sources",
    "butternut-squash|soil_prep|soil_prep_sources", "acorn-squash|soil_prep|soil_prep_sources",
    "spaghetti-squash|soil_prep|soil_prep_sources"}
CLOSED_2026_10_06 = {"parsnip|growth_stages[id=established]|sources"}  # cited by PLA-673 B2 (3ccc25f1 -> aaf004a2)


class ClosedWaivers(unittest.TestCase):
    """A waiver closed by a later promote must not redden an EARLIER promote's replay: PLA-10 promotes 1-3 replay
    post-states in which these blocks are still uncited (measured 2026-10-04: the full tree went red on 41 replay
    tests when the live set shrank). Each landed promote checks against the set live in its era, KNOWN_AT_ARMING."""

    def test_arming_set_is_the_live_set_plus_the_closed(self):
        self.assertEqual(set(G.CLOSED), CLOSED_2026_10_04 | CLOSED_2026_10_05 | CLOSED_SOIL_PREP | CLOSED_2026_10_06)
        self.assertEqual(G.KNOWN & set(G.CLOSED), frozenset())
        self.assertEqual(G.KNOWN_AT_ARMING, G.KNOWN | set(G.CLOSED))
        self.assertEqual(len(G.KNOWN_AT_ARMING), 2674)

    def test_an_era_post_state_flags_exactly_the_closed_under_the_live_set(self):
        import promote_fixture
        pre = json.loads(promote_fixture.pre_state(
            "b331e5f2c99378526c3ac8f2f870232953b318c994b7dc3d8c54938f2b62c38d"))
        live_v = G.roster(pre, mature_dimensions_armed=True)[3]
        # b331e5f2 predates every closure (and the soil_prep citations), so the live set flags all ten there
        self.assertEqual({v.split()[3].rstrip(":") for v in live_v},
                         CLOSED_2026_10_04 | CLOSED_2026_10_05 | CLOSED_SOIL_PREP | CLOSED_2026_10_06)
        self.assertEqual(G.roster(pre, mature_dimensions_armed=True, known=G.KNOWN_AT_ARMING)[3], [])

    def test_the_live_canonical_needs_no_era_set(self):
        self.assertEqual(G.roster(_CANON)[3], [])


# ----------------------------------------------------------------------- the live canonical
class LiveCanonical(unittest.TestCase):
    def test_inspected_population_and_verdict(self):
        """NOT pinned to the exact inspected count (7063 on 00dda31c): a promote that adds a CITED
        block moves it legitimately, and a pin that reddens on every promote is the PLA-544 class.
        What IS pinned is the ruled direction: live uncited == the waiver set, so citing a waived
        block forces the waiver edit in the same commit, and growth fails the gate by name."""
        n, inspected, live, V, stale, pot = G.roster(_CANON)
        self.assertGreaterEqual(inspected, G.MIN_INSPECTED)
        self.assertEqual(V, [])
        self.assertEqual(stale, [], "a waived block was cited: drop it from the waiver file")
        self.assertIsNone(G.refusal(n, inspected))

    def test_live_uncited_equals_the_waiver_set_exactly(self):
        self.assertEqual(set(G.roster(_CANON)[2]), set(G.KNOWN))

    def test_per_family_counts(self):
        counts = {}
        for i in G.KNOWN:
            counts[family_of(i)] = counts.get(family_of(i), 0) + 1
        self.assertEqual(counts, FAMILY_COUNTS)

    def test_every_certified_crop_has_at_least_one_waived_block(self):
        self.assertEqual(len({i.split("|")[0] for i in G.KNOWN}), 121)

    def test_the_tickets_98_slot_present_blocks_are_inside_the_population(self):
        """Independent walk, not the gate: a `sources` / `*_sources` slot equal to [] or null on a
        certified crop, outside companions/zones/regions. The ticket measured 98 on 83384c85.
        A crop-root `<name>_sources` sibling counts only when its claim keys carry content: PLA-674 writes
        soil_prep_sources = null on every record (D13, not assessed), and on the 81 with no soil_prep prose that null
        cites nothing (fbe11bc shipped this test red on exactly that, found 2026-10-06). 133 = the 98 + the 35
        soil_prep blocks armed by PLA-673 B2."""
        slots = set()
        for c in _CANON["crops"]:
            if (c.get("verification_status") or {}).get("status") != "verified_gs_arc":
                continue
            for k, v in c.items():
                if k.endswith("_sources") and v in ([], None):
                    carriers = SIBLING_CLAIM_KEYS.get(k[:-8], ())
                    if carriers and not any(c.get(x) not in (None, "", [], {}) for x in carriers):
                        continue
                    slots.add(f"{c['slug']}|{k[:-8]}|{k}")
                if isinstance(v, dict) and k not in ("companions", "zones", "regions") \
                        and "sources" in v and v["sources"] in ([], None):
                    slots.add(f"{c['slug']}|{k}|sources")
        self.assertLessEqual(len(slots), 133, "the slot-present subset may shrink, never grow (98 + 35 armed soil_prep)")
        self.assertEqual(slots - G.KNOWN, set())

    def test_a_clean_crop_passes(self):
        self.assertEqual(G.crop_violations(by(_CANON)[VICTIM]), [])

    def test_no_unnamed_citation_keys_on_canonical(self):
        for c in _CANON["crops"]:
            if G.certified(c):
                self.assertEqual(G.unnamed_fields(c), [], c["slug"])


# ---------------------------------------------------------- the three empty states + scope
class AbsenceHasFourStates(unittest.TestCase):
    """PLA-607's injection table: [], null and a REMOVED KEY were all invisible to every gate."""

    def _one_new(self, d, ident):
        v = violations(d)
        self.assertEqual(len(v), 1, v)
        self.assertIn(ident, v[0])

    def test_c1_storage_sources_empty_list_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["storage"]["sources"] = []
        self._one_new(d, f"{VICTIM}|storage|sources")

    def test_c2_storage_sources_null_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["storage"]["sources"] = None
        self._one_new(d, f"{VICTIM}|storage|sources")

    def test_c3_storage_sources_key_removed_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["storage"].pop("sources")
        by(d)[VICTIM]["storage"].pop("anchoring_urls", None)
        self._one_new(d, f"{VICTIM}|storage|sources")

    def test_c5_harvest_ready_sources_empty_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["harvest_ready_sources"] = []
        self._one_new(d, f"{VICTIM}|harvest_ready|harvest_ready_sources")

    def test_a_list_of_blank_strings_is_not_cited(self):
        d = fresh()
        by(d)[VICTIM]["watering"]["sources"] = ["", "  "]
        self._one_new(d, f"{VICTIM}|watering|sources")

    def test_an_ABSENT_block_is_not_uncited(self):
        d = fresh()
        by(d)[VICTIM].pop("storage")
        self.assertEqual(violations(d), [])

    def test_a_NULL_block_is_not_uncited(self):
        d = fresh()
        by(d)[VICTIM]["storage"] = None
        self.assertEqual(violations(d), [])

    def test_a_block_holding_only_citation_keys_states_nothing(self):
        d = fresh()
        by(d)[VICTIM]["storage"] = {"sources": [], "anchoring_urls": {}}
        self.assertEqual(violations(d), [])

    def test_a_block_holding_only_an_anchors_dict_states_nothing(self):
        """Non-empty citation keys are still citation keys: a block whose ONLY content is an
        anchoring dict makes no claim. (Harness survivor 2026-09-30: the empty-keys driver above
        could not see the CITE_KEYS exclusion, because [] and {} are empty either way.)"""
        d = fresh()
        by(d)[VICTIM]["storage"] = {"anchoring_urls": {"umn_ext": {"url": "https://extension.umn.edu/x",
                                                                   "verified": "2026-09-30"}}}
        self.assertEqual(violations(d), [])

    def test_an_uncertified_shell_is_exempt(self):
        d = fresh()
        shell = by(d)["avocado"]
        shell["storage"] = {"notes_seasoned": "authored", "sources": []}
        self.assertEqual(G.crop_violations(shell), [])
        self.assertEqual(violations(d), [])


class EveryNamedFamilyReaches(unittest.TestCase):
    """One injection per block KIND, so no branch of blocks() is uncovered."""

    def test_new_tip_without_sources_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["tips_by_stage"]["harvest"].append({"text_beginner": "x", "text_seasoned": "y"})
        n = len(by(_CANON)[VICTIM]["tips_by_stage"]["harvest"])
        self.assertTrue(any(f"{VICTIM}|tips_by_stage.harvest[{n}]|sources" in m
                            for m in violations(d)))

    def test_new_pest_without_sources_FAILS_by_its_id(self):
        d = fresh()
        by(d)[VICTIM]["pests"].append({"type": "pest", "id": "zz-new-pest", "control_ladder": []})
        self.assertTrue(any(f"{VICTIM}|pests[id=zz-new-pest]|sources" in m for m in violations(d)))

    def test_new_crop_level_sibling_claim_uncited_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["harvest_urgency_sources"] = []
        by(d)[VICTIM]["harvest_urgency"] = by(d)[VICTIM].get("harvest_urgency") or "high"
        # cabbage's harvest_urgency is already waived uncited -> [] changes nothing
        self.assertEqual(violations(d), [])
        d2 = fresh()
        by(d2)[VICTIM]["description_sources"] = []
        self.assertEqual(violations(d2), [], "description is waived uncited on cabbage already")

    def test_variety_items_are_covered_by_a_cited_parent(self):
        d = fresh()
        by(d)[VICTIM]["varieties"]["recommended"].append({"name": "Zz New Variety"})
        self.assertEqual(violations(d), [], "varieties.sources is cited on cabbage")

    def test_variety_items_become_uncited_when_the_parent_loses_its_sources(self):
        d = fresh()
        by(d)[VICTIM]["varieties"]["sources"] = None
        v = violations(d)
        self.assertTrue(any(f"{VICTIM}|varieties|sources" in m for m in v), v)
        self.assertTrue(any(f"{VICTIM}|varieties.recommended[name=" in m for m in v), v)

    def test_a_string_variety_item_under_an_uncited_parent_is_uncited(self):
        d = fresh()
        by(d)["carrot"]["varieties"]["recommended"].append("Zz String Variety")
        self.assertTrue(any("carrot|varieties.recommended[name=Zz String Variety]|sources" in m
                            for m in violations(d)))

    def test_new_field_addition_without_sources_FAILS(self):
        d = fresh()
        fa = by(d)[VICTIM]["verification_status"]["field_additions"]
        fa.append({"field": "zz", "date": "2026-09-30", "note": "x"})
        self.assertTrue(any(f"{VICTIM}|verification_status.field_additions[{len(fa) - 1}]|sources" in m
                            for m in violations(d)))


# -------------------------------------------------------------------------- the ratchet
class TheRatchet(unittest.TestCase):
    def test_shrinking_PASSES_and_reports_stale(self):
        d = fresh()
        cite(by(d)["grapefruit"]["watering"])
        n, insp, live, V, stale, _ = G.roster(d)
        self.assertEqual(V, [])
        self.assertEqual(stale, ["grapefruit|watering|sources"])

    def test_substitution_FAILS(self):
        """Close one, break another: the count is unchanged and the SET check still fires."""
        d = fresh()
        cite(by(d)["grapefruit"]["watering"])
        by(d)[VICTIM]["watering"]["sources"] = []
        n, insp, live, V, stale, _ = G.roster(d)
        self.assertEqual(len(live), len(G.roster(_CANON)[2]), "the driver must hold the count")
        self.assertTrue(any(f"{VICTIM}|watering|sources" in m for m in V), V)

    def test_keyed_identity_survives_a_reorder(self):
        d = fresh()
        by(d)["strawberry"]["pests"].reverse()
        self.assertEqual(violations(d), [])

    def test_a_cloned_certified_crop_inherits_no_waivers(self):
        d = fresh()
        clone = copy.deepcopy(by(d)[VICTIM])
        clone["slug"] = "zz-new-crop"
        d["crops"].append(clone)
        v = violations(d)
        waived_on_victim = [i for i in G.KNOWN if i.startswith(f"{VICTIM}|")]
        self.assertEqual(len([m for m in v if "zz-new-crop|" in m]), len(waived_on_victim))


# -------------------------------------------------------------------------- discovery
class NamingIsPartOfAdding(unittest.TestCase):
    def test_a_new_sourced_block_is_UNNAMED_until_named(self):
        """Re-homed 2026-10-01: PLA-10 promote 1 NAMED planting_layout (its first proof), so the
        unnamed-list case now uses a list nobody has named."""
        d = fresh()
        by(d)[VICTIM]["zz_layout"] = [{"method": "rows", "sources": ["umn_ext"]}]
        self.assertTrue(any("UNNAMED sourced field zz_layout[].sources" in m
                            for m in violations(d)), violations(d))

    def test_a_new_crop_root_sources_sibling_is_UNNAMED(self):
        d = fresh()
        by(d)[VICTIM]["spacing_inches_sources"] = ["umn_ext"]
        self.assertTrue(any("UNNAMED sourced field spacing_inches_sources" in m
                            for m in violations(d)))

    def test_a_new_crop_root_anchoring_sibling_is_UNNAMED(self):
        d = fresh()
        # re-pointed 2026-10-09: its old example, recommended_rootstock_note_anchoring_urls, is NAMED now (PLA-608
        # ruling 2, PLA-625 stop 1), so a still-unnamed crop-root pair key stands in.
        by(d)[VICTIM]["zz_claim_anchoring_urls"] = {}
        self.assertTrue(any("zz_claim_anchoring_urls" in m
                            for m in violations(d)))

    def test_a_nested_anchoring_dict_on_an_unnamed_block_is_UNNAMED(self):
        d = fresh()
        by(d)[VICTIM]["zz_block"] = {"x": 1, "anchoring_urls": {}}
        self.assertTrue(any("zz_block.anchoring_urls" in m for m in violations(d)))

    def test_the_excluded_subtrees_are_not_walked(self):
        d = fresh()
        by(d)[VICTIM]["regions"]["zz_region"] = {"cell": {"x": 1, "sources": []}}
        self.assertEqual(violations(d), [])

    def test_an_anchor_only_field_is_recorded_not_flagged(self):
        d = fresh()
        by(d)[VICTIM]["weeks_indoors_anchoring_urls"] = {}  # spacing_inches_anchoring_urls retired (PLA-10)
        self.assertEqual(violations(d), [])


# ------------------------------------------------- PLA-10 promote 1: planting_layout entries
LAYOUT_ENTRY = {"id": "row-none", "arrangement": "row", "support": "none", "default": True,
                "in_row_inches": [12, 24], "row_spacing_inches": [24, 36], "row_spacing_reason": None,
                "sources": ["umn_ext"], "anchoring_urls": {"umn_ext": {
                    "url": "https://extension.umn.edu/vegetables/growing-cabbage", "verified": "2026-10-01"}}}
# R5's eight plus W5's five (Trevor, 2026-10-01: "no CITABLE page after a recorded hunt").
MIGRATION_ELIGIBLE = ("bee-balm", "bok-choy", "borage", "cherry-sour", "cherry-sweet", "cosmos", "echinacea",
                      "mulberry", "pomegranate", "rosemary", "sweet-alyssum", "sweet-pea", "viola")


class PlantingLayoutFamily(unittest.TestCase):
    """Spec §1.6 / §10.1: ITEM_FAMILIES names planting_layout keyed by id, so promote 1's entries are
    ratcheted the day they land; R5's migration waiver is the ONLY way an entry ships uncited."""

    def put(self, slug, **over):
        d = fresh()
        e = copy.deepcopy(LAYOUT_ENTRY); e.update(over)
        by(d)[slug]["planting_layout"] = [e]
        return d, e

    def test_the_live_legacy_strings_are_not_blocks(self):
        self.assertEqual([m for m in violations(fresh()) if "planting_layout" in m], [])

    def test_a_cited_entry_passes_and_is_named(self):
        d, _ = self.put(VICTIM)
        self.assertEqual(violations(d), [])

    def test_an_uncited_entry_FAILS_by_its_id(self):
        for slot in ([], None, "__absent__"):
            d, e = self.put(VICTIM)
            if slot == "__absent__":
                del by(d)[VICTIM]["planting_layout"][0]["sources"]
            else:
                by(d)[VICTIM]["planting_layout"][0]["sources"] = slot
            self.assertTrue(any(f"NEW uncited block {VICTIM}|planting_layout[id=row-none]|sources" in m
                                for m in violations(d)), (slot, violations(d)))

    def test_the_migration_set_is_the_R5_list_and_ships_empty(self):
        self.assertEqual(tuple(sorted(G.MIGRATION_ELIGIBLE)), MIGRATION_ELIGIBLE)
        self.assertEqual(G.MIGRATION_WAIVERS, {})

    def _waive(self, slug, eid, in_row):
        saved = dict(G.MIGRATION_WAIVERS)
        G.MIGRATION_WAIVERS.clear()
        G.MIGRATION_WAIVERS[slug] = {"entry_id": eid, "in_row_inches": in_row, "hunt": "test"}
        self.addCleanup(lambda: (G.MIGRATION_WAIVERS.clear(), G.MIGRATION_WAIVERS.update(saved)))

    def test_a_migration_waiver_holds_only_while_byte_equal(self):
        slug = "bok-choy"
        pre = by(_CANON)[slug]["spacing_inches"]
        self._waive(slug, "row-none", list(pre))
        d, _ = self.put(slug, sources=[], anchoring_urls={}, in_row_inches=list(pre))
        self.assertEqual([m for m in violations(d) if slug in m], [])
        d, _ = self.put(slug, sources=[], anchoring_urls={}, in_row_inches=[pre[0], pre[1] + 1])
        self.assertTrue(any("migration waiver" in m and "byte" in m for m in violations(d)), violations(d))
        d, _ = self.put(slug, sources=[], anchoring_urls={}, in_row_inches=[float(pre[0]), pre[1]])
        self.assertTrue(any("migration waiver" in m and "byte" in m for m in violations(d)), violations(d))

    def test_a_migration_waiver_names_its_entry(self):
        slug = "bok-choy"
        pre = by(_CANON)[slug]["spacing_inches"]
        self._waive(slug, "row-stake", list(pre))
        d, _ = self.put(slug, sources=[], anchoring_urls={}, in_row_inches=list(pre))
        self.assertTrue(any(f"NEW uncited block {slug}|planting_layout[id=row-none]" in m
                            for m in violations(d)), violations(d))

    def test_a_migration_waiver_off_the_R5_list_is_REFUSED(self):
        pre = by(_CANON)[VICTIM]["spacing_inches"]
        self._waive(VICTIM, "row-none", list(pre))
        d, _ = self.put(VICTIM, sources=[], anchoring_urls={}, in_row_inches=list(pre))
        self.assertTrue(any("not on the R5 hunt list" in m for m in violations(d)), violations(d))

    def test_a_migration_waiver_covers_only_the_entry_not_other_blocks(self):
        slug = "bok-choy"
        pre = by(_CANON)[slug]["spacing_inches"]
        self._waive(slug, "row-none", list(pre))
        d, _ = self.put(slug, sources=[], anchoring_urls={}, in_row_inches=list(pre))
        e2 = copy.deepcopy(LAYOUT_ENTRY); e2.update(id="row-stake", support="stake", default=False,
                                                    sources=[], anchoring_urls={})
        by(d)[slug]["planting_layout"].append(e2)
        self.assertTrue(any(f"{slug}|planting_layout[id=row-stake]" in m for m in violations(d)))

    def test_A63_reaches_a_bare_sole_anchor_on_an_entry(self):
        """Spec §10.1: A63 needs no code change; a scratch injection must redden it (proof, not trust)."""
        import bare_host_gate as BH
        d, _ = self.put(VICTIM, anchoring_urls={"umn_ext": {"url": "https://extension.umn.edu",
                                                             "verified": "2026-10-01"}})
        v = BH.roster(d)[4]
        self.assertTrue(any(VICTIM in m and "planting_layout" in m for m in v), v)
        d, _ = self.put(VICTIM)
        self.assertEqual([m for m in BH.roster(d)[4] if "planting_layout" in m], [])


# ----------------------------------------------------------------- the folded pot sub-rule
class PotSizeSubRule(unittest.TestCase):
    """container_citation_floor_gate's rule and proofs, carried over verbatim in intent."""

    def test_live_pot_population_is_the_known_four(self):
        self.assertEqual(G.roster(_CANON)[5], list(POT_KNOWN))

    def test_PROOF_a_fifth_FAILS(self):
        d = fresh()
        by(d)[VICTIM]["container_notes"]["anchoring_urls"] = {}
        v = violations(d)
        self.assertTrue(any("is NOT one of the 4 known" in m and VICTIM in m for m in v), v)

    def test_PROOF_closing_one_PASSES(self):
        d = fresh()
        cite(by(d)["dry-bean"]["container_notes"])
        self.assertEqual(violations(d), [])

    def test_giving_a_null_crop_a_figure_without_a_citation_FAILS(self):
        d = fresh()
        cn = by(d)["plum"]["container_notes"]
        self.assertIsNone(cn.get("min_pot_gallons"))
        cn["min_pot_gallons"] = 25
        self.assertTrue(G.pot_uncited(by(d)["plum"]))
        self.assertTrue(any("plum: states container_notes.min_pot_gallons" in m
                            for m in violations(d)))

    def test_the_ceiling_fires_on_a_KNOWN_CEILING_desync(self):
        d = fresh()
        by(d)[VICTIM]["container_notes"]["anchoring_urls"] = {}
        saved = G.POT_KNOWN
        G.POT_KNOWN = saved + (VICTIM,)
        try:
            self.assertTrue(any("ratchet ceiling is 4" in m for m in violations(d)))
        finally:
            G.POT_KNOWN = saved

    def test_a_null_figure_is_out_of_scope_and_shells_are_exempt(self):
        d = fresh()
        self.assertFalse(G.pot_uncited(by(d)["plum"]))
        av = by(d)["avocado"]
        av["container_notes"] = {"min_pot_gallons": 10, "sources": [], "anchoring_urls": {}}
        self.assertFalse(G.pot_uncited(av))

    def test_sources_without_anchors_is_pot_uncited(self):
        d = fresh()
        by(d)[VICTIM]["container_notes"]["anchoring_urls"] = {}
        self.assertTrue(G.pot_uncited(by(d)[VICTIM]))


# ------------------------------------------------------------------- inspected nothing
class RefusesAnEmptyPopulation(unittest.TestCase):
    def test_zero_certified_REFUSES(self):
        d = fresh()
        for c in d["crops"]:
            (c.get("verification_status") or {})["status"] = "draft"
        n, insp, *_ = G.roster(d)
        self.assertEqual((n, insp), (0, 0))
        self.assertIn("0 certified", G.refusal(n, insp))

    def test_below_floor_REFUSES(self):
        self.assertIn("below the declared floor", G.refusal(121, G.MIN_INSPECTED - 1))
        self.assertIsNone(G.refusal(121, G.MIN_INSPECTED))


# --------------------------------------------------------------------------------- CLI
class CLI(unittest.TestCase):
    def _run(self, data):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
        try:
            r = subprocess.run([sys.executable, os.path.join(HERE, "sourced_block_ratchet_gate.py"),
                                f.name], capture_output=True, text=True)
            return r.returncode, r.stdout + r.stderr
        finally:
            os.remove(f.name)

    def test_canonical_rc0_and_reports_population(self):
        r = subprocess.run([sys.executable, os.path.join(HERE, "sourced_block_ratchet_gate.py"),
                            CANON], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"inspected \d+ named blocks on \d+ certified crops; \d+ uncited")

    def test_injection_rc1_names_the_block(self):
        d = fresh()
        by(d)[VICTIM]["storage"]["sources"] = []
        rc, out = self._run(d)
        self.assertEqual(rc, 1, out)
        self.assertIn(f"{VICTIM}|storage|sources", out)

    def test_empty_population_rc2(self):
        d = fresh()
        for c in d["crops"]:
            (c.get("verification_status") or {})["status"] = "draft"
        rc, out = self._run(d)
        self.assertEqual(rc, 2, out)
        self.assertIn("REFUSED", out)


if __name__ == "__main__":
    unittest.main()


# ------------------------------------------------------- PLA-674: the soil_prep sibling (2026-10-05)
class SoilPrepSibling(unittest.TestCase):
    """PLA-674 writes soil_prep_sources / soil_prep_anchoring_urls on every crop record, null where not assessed
    (D13), watermelon backfilled. NAMED 2026-10-05 so the keys are not UNNAMED (A62 discovery); ARMED 2026-10-06 in the
    PLA-673 B2 data commit, as ruled, with the 35 crops whose soil_prep prose still carries a null citation waived by
    identity and the five cited before arming kept CLOSED (era identities)."""

    def _with_siblings(self, value=None):
        d = fresh()
        for c in d["crops"]:
            c["soil_prep_sources"] = value
            c["soil_prep_anchoring_urls"] = None if value is None else {value[0]: {"url": "https://x.edu/a", "verified": "2026-10-05"}}
        return d

    def test_the_flag_is_armed(self):
        """Armed 2026-10-06 in the PLA-673 B2 data commit, as ruled (named-and-unarmed 2026-10-05 to 2026-10-06)."""
        self.assertIs(G.SOIL_PREP_ARMED, True)

    def test_the_sibling_keys_are_not_UNNAMED(self):
        d = self._with_siblings()
        for c in d["crops"]:
            if G.certified(c):
                self.assertEqual([f for f in G.unnamed_fields(c) if "soil_prep" in f], [], c["slug"])

    def test_unarmed_null_siblings_add_no_uncited_block(self):
        """The era switch landed promotes pass (soil_prep_armed=False) still turns the block off."""
        """ABSOLUTE, not relative: a before/after comparison passes when the skip is gone (the base, carrying the prose
        and no sibling, would count the block too). Unarmed, no soil_prep identity exists at all, with or without
        the siblings, on a population that does carry the prose."""
        d = self._with_siblings()
        prose = [c for c in d["crops"] if G.certified(c) and c.get("soil_prep_beginner")]
        self.assertGreaterEqual(len(prose), 30, "the prose population this test inspects")
        for crop in (d, fresh()):
            for c in crop["crops"]:
                if G.certified(c):
                    self.assertEqual([i for i in G.uncited(c, soil_prep_armed=False) if "|soil_prep|" in i], [], c["slug"])

    def test_armed_null_siblings_on_prose_crops_are_uncited(self):
        """Positive control for the flag: armed, a prose-carrying crop with a null sibling IS an uncited block."""
        d = self._with_siblings()
        crop = next(c for c in d["crops"] if G.certified(c) and c.get("soil_prep_beginner"))
        self.assertIn(f"{crop['slug']}|soil_prep|soil_prep_sources", G.uncited(crop, soil_prep_armed=True))


class SoilPrepArmed(unittest.TestCase):
    """PLA-673 B2 (2026-10-06): armed, a NEW soil_prep block with prose and no citation fails by name; a waived one
    passes; a closed one going uncited again fails."""

    def test_a_new_uncited_soil_prep_block_fails(self):
        d = fresh()
        crop = next(c for c in d["crops"] if G.certified(c) and not c.get("soil_prep_beginner")
                    and not c.get("soil_prep_seasoned"))
        crop["soil_prep_seasoned"] = "Work in compost before planting."
        v = G.roster(d)[3]
        self.assertTrue(any(f"{crop['slug']}|soil_prep|soil_prep_sources" in m for m in v), v)

    def test_a_closed_soil_prep_block_going_uncited_fails(self):
        d = fresh()
        c = by(d)["pumpkin"]
        if c.get("soil_prep_sources"):          # only meaningful once B2's backfill is the canonical
            c["soil_prep_sources"] = None
            v = G.roster(d)[3]
            self.assertTrue(any("pumpkin|soil_prep|soil_prep_sources" in m for m in v), v)
        else:
            self.skipTest("pumpkin's soil_prep is not cited on this canonical (pre-B2)")

    def test_the_35_are_exactly_the_waived_soil_prep(self):
        self.assertEqual(len([i for i in G.KNOWN if "|soil_prep|" in i]), 35)


AFBD = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"   # housekeeping 60 Phase C post-state
GLOSS = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"  # PLA-673 glossary post-state


class EraSwitchIsBoundToAHistoricalPostState(unittest.TestCase):
    """The ERA SWITCH (2026-10-06, hardened at Trevor's B2 go-condition 2). A landed promote replaying an earlier
    post-state through the gate subprocesses sets SBR_KNOWN_AT_ARMING to THAT FILE'S SHA. The gate binds it to the file
    it gates (bind_era) and accepts it only if the SHA is a registered replay post-state, equals the gated file's
    sha256, and is NOT the live canonical. Anything else REFUSES, and a switch that is set but never bound refuses at
    first use: setting it in a live run can never let current data pass against an older waiver set."""

    @classmethod
    def setUpClass(cls):
        import promote_fixture, tempfile
        cls.tmp = tempfile.mkdtemp(prefix="era_")
        cls.era = os.path.join(cls.tmp, "afbd.json")
        with open(cls.era, "wb") as f:
            b = promote_fixture.pre_state(AFBD)
            f.write(b if isinstance(b, bytes) else b.encode("utf-8"))
        cls.other = os.path.join(cls.tmp, "other.json")
        with open(cls.other, "wb") as f:
            f.write(open(cls.era, "rb").read() + b" ")
        cls.data = json.load(open(cls.era, encoding="utf-8"))

    def setUp(self):
        os.environ.pop(G.ERA_ENV, None)
        G._ERA_BOUND = None

    tearDown = setUp

    def _pumpkin(self):
        return [m for m in G.roster(self.data)[3] if "pumpkin|soil_prep|soil_prep_sources" in m]

    def test_the_registry_is_exactly_the_two_replays(self):
        self.assertEqual(set(G.ERA_POST_STATES), {AFBD, GLOSS})

    def test_unset_binds_nothing_and_uses_the_live_set(self):
        self.assertIsNone(G.bind_era(self.era))
        self.assertTrue(self._pumpkin(), "afbd4113 predates pumpkin's soil_prep citation: the live set flags it")

    def test_a_registered_sha_bound_to_its_own_file_uses_the_era_set(self):
        os.environ[G.ERA_ENV] = AFBD
        self.assertEqual(G.bind_era(self.era, canonical=CANON), AFBD)
        self.assertEqual(self._pumpkin(), [])
        self.assertIs(G._default_known(), G.KNOWN_AT_ARMING)

    def test_the_old_value_1_refuses(self):
        os.environ[G.ERA_ENV] = "1"
        with self.assertRaisesRegex(G.EraRefused, "not a registered replay post-state"):
            G.bind_era(self.era, canonical=CANON)

    def test_an_unregistered_sha_refuses_even_when_it_matches_the_file(self):
        import hashlib
        os.environ[G.ERA_ENV] = hashlib.sha256(open(self.other, "rb").read()).hexdigest()
        with self.assertRaisesRegex(G.EraRefused, "not a registered replay post-state"):
            G.bind_era(self.other, canonical=CANON)

    def test_a_registered_sha_on_a_different_file_refuses(self):
        os.environ[G.ERA_ENV] = AFBD
        with self.assertRaisesRegex(G.EraRefused, "is not the gated file"):
            G.bind_era(self.other, canonical=CANON)

    def test_a_registered_sha_that_is_the_live_canonical_refuses(self):
        os.environ[G.ERA_ENV] = AFBD
        with self.assertRaisesRegex(G.EraRefused, "is the live canonical"):
            G.bind_era(self.era, canonical=self.era)

    def test_set_but_never_bound_refuses_at_first_use(self):
        os.environ[G.ERA_ENV] = AFBD
        with self.assertRaisesRegex(G.EraRefused, "not bound"):
            G.roster(self.data)

    def test_a_failed_bind_leaves_nothing_bound(self):
        os.environ[G.ERA_ENV] = AFBD
        self.assertEqual(G.bind_era(self.era, canonical=CANON), AFBD)
        with self.assertRaises(G.EraRefused):
            G.bind_era(self.other, canonical=CANON)
        self.assertIsNone(G._ERA_BOUND)

    def test_the_era_set_adds_only_the_closed(self):
        self.assertEqual(G.KNOWN_AT_ARMING - G.KNOWN, frozenset(G.CLOSED))
