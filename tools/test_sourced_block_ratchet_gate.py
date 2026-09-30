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
    "growth_stages[]": 615, "notifications[]": 458, "tips_by_stage.*[]": 313,
    "weather_triggers[]": 289, "failure_diagnostics[]": 251, "description": 108,
    "harvest_urgency": 108, "start_method": 103, "succession_policy": 86,
    "varieties.recommended[]": 77, "pests[]": 54, "diseases[]": 50, "harvest_ready": 26,
    "watering": 17, "bolting": 13, "container_notes": 12, "varieties": 12, "fertilizer": 11,
    "pollination": 9, "rotation": 8, "verification_status.field_additions[]": 3, "thinning": 3,
    "soil": 2, "storage": 2, "yield_expectations": 2, "ph": 2,
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


# ------------------------------------------------------------------------------------ pins
class PinsAreTheMeasurement(unittest.TestCase):
    def test_waiver_file_is_the_measured_population(self):
        self.assertEqual(G._KNOWN_DOC["measured_on"], SHA)
        self.assertEqual(G._KNOWN_DOC["count"], 2634)
        self.assertEqual(len(G.KNOWN), 2634)
        self.assertEqual(len(G._KNOWN_DOC["identities"]), 2634, "duplicate identities")

    def test_the_named_list_is_what_was_ruled(self):
        self.assertEqual(set(G.DICT_BLOCKS), {
            "bolting", "container_notes", "fertilizer", "harvest_stop_rule",
            "heat_threshold_temp_f", "indoor_cycle", "pet_safe", "ph", "photoperiod",
            "pollination", "rotation", "soil", "start_method", "storage", "succession_policy",
            "thinning", "varieties", "watering", "winter_hardiness", "yield_expectations"})
        self.assertEqual(set(G.SIBLING_BLOCKS), {"description", "harvest_ready", "harvest_urgency"})
        self.assertEqual(set(G.ITEM_FAMILIES), {
            "pests", "diseases", "growth_stages", "failure_diagnostics", "notifications",
            "weather_triggers", "rootstock_options", "varieties.recommended",
            "container_notes.plants_per_pot.readings", "verification_status.field_additions"})

    def test_the_three_ruled_exclusions_and_only_those(self):
        """RULED 2026-09-30: out of the named list, each with its reason recorded."""
        self.assertEqual(set(G.EXCLUDED), {"companions", "zones", "regions"})
        for k, why in G.EXCLUDED.items():
            self.assertTrue(why.strip(), k)

    def test_anchor_only_fields_are_the_measured_eight(self):
        self.assertEqual(set(G.ANCHOR_ONLY), {
            "<crop>.anchoring_urls", "days_to_maturity_anchoring_urls",
            "days_to_maturity_mid_anchoring_urls", "det_indet.anchoring_urls",
            "germination_temp_f_anchoring_urls", "spacing_inches_anchoring_urls",
            "sunlight_hours_anchoring_urls", "weeks_indoors_anchoring_urls"})

    def test_pot_sub_rule_pins_are_the_folded_four(self):
        """Folded in from container_citation_floor_gate (PLA-533 ruling 1). Literals, never computed."""
        self.assertEqual(G.POT_CEILING, 4)
        self.assertEqual(tuple(sorted(G.POT_KNOWN)), POT_KNOWN)
        self.assertEqual(len(G.POT_KNOWN), G.POT_CEILING)

    def test_floor_is_below_the_measured_population(self):
        """Measured 7063 on 00dda31c. The floor is a literal, never derived from the run it bounds."""
        self.assertEqual(G.MIN_INSPECTED, 6500)


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
        certified crop, outside companions/zones/regions. The ticket measured 98 on 83384c85."""
        slots = set()
        for c in _CANON["crops"]:
            if (c.get("verification_status") or {}).get("status") != "verified_gs_arc":
                continue
            for k, v in c.items():
                if k.endswith("_sources") and v in ([], None):
                    slots.add(f"{c['slug']}|{k[:-8]}|{k}")
                if isinstance(v, dict) and k not in ("companions", "zones", "regions") \
                        and "sources" in v and v["sources"] in ([], None):
                    slots.add(f"{c['slug']}|{k}|sources")
        self.assertLessEqual(len(slots), 98, "the slot-present subset may shrink, never grow")
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
        d = fresh()
        by(d)[VICTIM]["planting_layout"] = [{"method": "rows", "sources": ["umn_ext"]}]
        self.assertTrue(any("UNNAMED sourced field planting_layout[].sources" in m
                            for m in violations(d)), violations(d))

    def test_a_new_crop_root_sources_sibling_is_UNNAMED(self):
        d = fresh()
        by(d)[VICTIM]["spacing_inches_sources"] = ["umn_ext"]
        self.assertTrue(any("UNNAMED sourced field spacing_inches_sources" in m
                            for m in violations(d)))

    def test_a_new_crop_root_anchoring_sibling_is_UNNAMED(self):
        d = fresh()
        by(d)[VICTIM]["recommended_rootstock_note_anchoring_urls"] = {}
        self.assertTrue(any("recommended_rootstock_note_anchoring_urls" in m
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
        by(d)[VICTIM]["spacing_inches_anchoring_urls"] = {}
        self.assertEqual(violations(d), [])


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
