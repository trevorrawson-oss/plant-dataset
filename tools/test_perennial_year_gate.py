#!/usr/bin/env python3
"""Tests for tools/perennial_year_gate.py (PLA-6 Round 1, the perennial ramp census).

Run: python3 tools/test_perennial_year_gate.py

WHAT THIS GATE OWNS, and why it is not covered by anything already shipped.

A perennial's grower sees THREE year-pills on the guide -- Establishing / First harvests /
Full harvest -- and plant-app composes their captions from EXISTING dataset prose rather than
from any year-keyed field (there is none; `growth_stages_year_one` is present on 25 crops and
empty on all 25). The composition is, verbatim from `src/app/(tabs)/learn/[slug].tsx`:

    establishing -> tips_by_stage.establishment[0].text_{level}
    first        -> tips_by_stage.establishment[0].text_{level}   <-- the SAME string
    full         -> firstSentence(harvest_ready_{level})

Two dataset contracts fall out of that, and neither was gated:

  ESTAB-CAPTION  a perennial that renders pills must carry BOTH registers of the establishment
                 tip, because that one string is the entire caption for two of the three pills.
                 A50 checks the ramp; A39 checks register presence on the register-map fields;
                 tips_by_stage.establishment[0].text_* is on neither list.

  PILL-CAPTION   the FIRST SENTENCE of harvest_ready_* must stand alone, because the app renders
                 exactly that and nothing else as the Full-harvest caption. A whole-paragraph
                 harvest_ready can be excellent and still open with a bare topic sentence, which
                 is how certified artichoke ships "Squeeze the bud." as its mature-bed guidance.
                 This is the optional-field-gates-go-vacuous class in a new spot: every existing
                 check reads the WHOLE field and passes.

  YEAR-DUP       PLA-6 Round 1 step 3's literal ask: near-identical text between two different
                 stage entries within the SAME crop. The gold-standard template-copy check
                 compares ACROSS crops only, so an intra-crop duplicate is invisible to it.
                 Measured 0 on live canonical fe26f783 -- this is a REFUSAL-SPEC guard (per
                 CLAUDE.md: a guard that refuses an input and stays green is a pass, not a
                 vacuity), and the mutation harness is its only non-vacuity evidence.

RED-proof, recorded at authoring time against canonical fe26f783:
  * PILL-CAPTION is RED on live data -- 4 findings across 3 crops (artichoke both registers,
    mandarin-clementine seasoned, orange-navel seasoned). The live-canonical test asserts that
    exact set BY NAME and stays RED until an authoring pass repairs them, which is the point.
    orange-navel's BEGINNER lead is exactly 8 words and passes: the boundary is real, not a
    rounding artefact, and it was found by the expectation being wrong before the gate was.
  * ESTAB-CAPTION and YEAR-DUP are green on live data and carry synthetic RED cases plus the
    mutation harness (tools/mutate_perennial_year_gate.py).

THRESHOLD IS MEASURED, NOT GUESSED. First-sentence word counts over all 242 harvest_ready
register strings roster-wide: min 3, p05 7, p10 11, median 24. Scoped to perennials that
actually render pills, `< 8 words` yields 4 findings on 3 crops; the same threshold unscoped
would pull in 15, most of them legitimate topic sentences on annuals whose guide has no pill to
truncate into (beet's "Beets give you two harvests."). Narrowing the CHECK to the crops where
the truncation is actually rendered, rather than loosening the threshold, is what keeps it at 4.
"""
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

from perennial_year_gate import (  # noqa: E402
    CAPTION_MIN_WORDS, estab_caption_violations, first_sentence,
    pill_caption_violations, renders_pills, violations, year_dup_violations,
)

CANONICAL = REPO / "crops_data_final.json"


def load():
    return json.load(open(CANONICAL, encoding="utf-8"))


def perennials(data):
    return [c for c in data["crops"] if c.get("perennial") is True]


def stage(sid, **kw):
    base = {"id": sid, "what_to_look_for_beginner": f"{sid} look b",
            "what_to_look_for_seasoned": f"{sid} look s",
            "user_action_beginner": f"{sid} act b", "user_action_seasoned": f"{sid} act s"}
    base.update(kw)
    return base


def crop(**kw):
    """Minimal synthetic perennial that PASSES every family, so each test mutates one thing."""
    base = {
        "slug": "synthetic", "perennial": True,
        "years_to_first_harvest": [2, 3],
        "harvest_ready_beginner": "A synthetic fruit is ready when it has coloured all over and "
                                  "lifts free with a gentle twist. Check twice a week.",
        "harvest_ready_seasoned": "Harvest at full varietal colour once the fruit abscises under "
                                  "light thumb pressure. Sample before a full pick.",
        "tips_by_stage": {"establishment": [
            {"text_beginner": "Water deeply once a week through the first summer.",
             "text_seasoned": "Irrigate to field capacity weekly through establishment."}]},
        "growth_stages": [stage("planting"), stage("establishment"), stage("harvest")],
    }
    base.update(kw)
    return base


# --------------------------------------------------------------------------- first_sentence
class FirstSentenceMatchesTheApp(unittest.TestCase):
    """Ports plant-app's firstSentence() exactly. If these drift the gate measures the wrong
    string, so the app's own regex is pinned here rather than approximated."""

    def test_takes_only_the_lead_sentence(self):
        self.assertEqual(first_sentence("One. Two. Three."), "One.")

    def test_question_and_bang_terminate_too(self):
        self.assertEqual(first_sentence("Ripe yet? Check again."), "Ripe yet?")
        self.assertEqual(first_sentence("Pick it! Then chill."), "Pick it!")

    def test_a_decimal_point_is_not_a_sentence_end(self):
        # "0.25 inch" must not truncate to "0." -- the app's lookahead requires whitespace/EOS.
        self.assertEqual(first_sentence("Spears at 0.25 inch are done. Stop."),
                         "Spears at 0.25 inch are done.")

    def test_an_unterminated_string_returns_whole(self):
        self.assertEqual(first_sentence("no terminator here"), "no terminator here")


# --------------------------------------------------------------------------- scope
class ScopeIsCropsThatActuallyRenderPills(unittest.TestCase):
    def test_a_perennial_with_a_valid_range_renders_pills(self):
        self.assertTrue(renders_pills(crop()))

    def test_an_annual_never_renders_pills(self):
        self.assertFalse(renders_pills(crop(perennial=False)))

    def test_a_perennial_without_a_range_renders_no_pills(self):
        # lavender/sage/thyme: no years_to_first_harvest -> plant-app hides the whole pill row,
        # so a short harvest_ready first sentence is never truncated into a caption.
        self.assertFalse(renders_pills(crop(years_to_first_harvest=None)))

    def test_a_malformed_range_renders_no_pills(self):
        self.assertFalse(renders_pills(crop(years_to_first_harvest=[])))
        self.assertFalse(renders_pills(crop(years_to_first_harvest=[2])))
        self.assertFalse(renders_pills(crop(years_to_first_harvest=["2", "3"])))

    def test_every_family_is_a_no_op_off_scope(self):
        annual = crop(perennial=False, harvest_ready_beginner="Pick it.",
                      harvest_ready_seasoned="Pick it.", tips_by_stage={})
        self.assertEqual(violations(annual), [])


# --------------------------------------------------------------------------- PILL-CAPTION
class PillCaptionStandsAlone(unittest.TestCase):
    def test_a_bare_topic_sentence_flags(self):
        v = pill_caption_violations(crop(harvest_ready_beginner="Squeeze the bud. Then cut it."))
        self.assertEqual(len(v), 1)
        self.assertIn("beginner", v[0])
        self.assertIn("Squeeze the bud.", v[0])

    def test_a_substantive_lead_sentence_passes(self):
        self.assertEqual(pill_caption_violations(crop()), [])

    def test_both_registers_are_checked_independently(self):
        v = pill_caption_violations(crop(harvest_ready_beginner="Squeeze the bud. More.",
                                         harvest_ready_seasoned="Cut on tightness. More."))
        self.assertEqual(len(v), 2)

    def test_exactly_the_threshold_passes_and_one_below_flags(self):
        at = " ".join(["word"] * CAPTION_MIN_WORDS) + ". Tail."
        below = " ".join(["word"] * (CAPTION_MIN_WORDS - 1)) + ". Tail."
        self.assertEqual(pill_caption_violations(crop(harvest_ready_beginner=at)), [])
        self.assertEqual(len(pill_caption_violations(crop(harvest_ready_beginner=below))), 1)

    def test_a_missing_harvest_ready_is_not_this_gate_s_finding(self):
        # A39 owns absence; reporting it here too would double-count the shells.
        self.assertEqual(pill_caption_violations(crop(harvest_ready_beginner=None,
                                                      harvest_ready_seasoned=None)), [])


    def test_an_authored_full_harvest_note_SUPPRESSES_the_finding(self):
        """PLA-6 Round 2 changed what this family measures. `firstSentence(harvest_ready_*)` is
        now only the FALLBACK: plant-app prefers `full_harvest_notes_{level}` and never shears
        it. So once that field is authored, a short harvest_ready lead sentence is no longer
        rendered anywhere and reporting it would be a defect nobody can see -- the gate telling
        a true story about a string that is not on screen."""
        c = crop(harvest_ready_beginner='Squeeze the bud. Then cut it.',
                 full_harvest_notes_beginner='Cut each bud while its scales are still shut flat.')
        self.assertEqual(pill_caption_violations(c), [])

    def test_suppression_is_PER_REGISTER(self):
        # A crop may be half-migrated mid-wave. The register that still falls through is still
        # measured; the one that does not is not.
        c = crop(harvest_ready_beginner='Squeeze the bud. More.',
                 harvest_ready_seasoned='Cut on tightness. More.',
                 full_harvest_notes_beginner='Cut each bud while its scales are still shut flat.')
        v = pill_caption_violations(c)
        self.assertEqual(len(v), 1)
        self.assertIn('seasoned', v[0])

    def test_an_empty_full_harvest_note_does_not_suppress(self):
        c = crop(harvest_ready_beginner='Squeeze the bud. More.', full_harvest_notes_beginner='')
        self.assertEqual(len(pill_caption_violations(c)), 1)


# --------------------------------------------------------------------------- ESTAB-CAPTION
class EstablishmentTipCarriesBothRegisters(unittest.TestCase):
    def test_a_missing_seasoned_register_flags(self):
        c = crop(tips_by_stage={"establishment": [{"text_beginner": "Water it in."}]})
        v = estab_caption_violations(c)
        self.assertEqual(len(v), 1)
        self.assertIn("text_seasoned", v[0])

    def test_a_missing_beginner_register_flags(self):
        c = crop(tips_by_stage={"establishment": [{"text_seasoned": "Irrigate to capacity."}]})
        self.assertEqual(len(estab_caption_violations(c)), 1)

    def test_an_absent_establishment_stage_flags(self):
        self.assertEqual(len(estab_caption_violations(crop(tips_by_stage={}))), 1)

    def test_an_empty_establishment_list_flags(self):
        self.assertEqual(len(estab_caption_violations(crop(tips_by_stage={"establishment": []}))), 1)

    def test_both_registers_present_passes(self):
        self.assertEqual(estab_caption_violations(crop()), [])


# --------------------------------------------------------------------------- YEAR-DUP
class IntraCropStageDuplication(unittest.TestCase):
    def test_two_stages_sharing_a_field_verbatim_flags(self):
        c = crop(growth_stages=[
            stage("establishment", user_action_beginner="Leave the ferns standing all summer."),
            stage("fern_growth", user_action_beginner="Leave the ferns standing all summer."),
        ])
        v = year_dup_violations(c)
        self.assertEqual(len(v), 1)
        self.assertIn("establishment", v[0])
        self.assertIn("fern_growth", v[0])

    def test_a_near_duplicate_above_threshold_flags(self):
        c = crop(growth_stages=[
            stage("a", user_action_beginner="Leave the ferns standing all summer long."),
            stage("b", user_action_beginner="Leave the ferns standing all summer, long."),
        ])
        self.assertEqual(len(year_dup_violations(c)), 1)

    def test_whitespace_and_case_differences_still_count_as_duplicate(self):
        c = crop(growth_stages=[
            stage("a", user_action_beginner="Leave the ferns standing."),
            stage("b", user_action_beginner="  LEAVE   the ferns   standing.  "),
        ])
        self.assertEqual(len(year_dup_violations(c)), 1)

    def test_genuinely_different_stages_pass(self):
        self.assertEqual(year_dup_violations(crop()), [])

    def test_the_same_string_in_DIFFERENT_fields_is_not_a_finding(self):
        # what_to_look_for and user_action may legitimately converge; the ask is cross-STAGE
        # duplication of the SAME field. Widening this floods.
        c = crop(growth_stages=[stage("a", user_action_beginner="Cut the ferns down.",
                                      what_to_look_for_beginner="Cut the ferns down.")])
        self.assertEqual(year_dup_violations(c), [])

    def test_short_strings_are_exempt_unless_exactly_equal(self):
        # log_prompt-length strings ("Any sprouts yet?") collide on similarity without being
        # a copy defect. Exact equality still flags.
        c = crop(growth_stages=[stage("a", user_action_beginner="Any buds yet?"),
                                stage("b", user_action_beginner="Any pods yet?")])
        self.assertEqual(year_dup_violations(c), [])


# --------------------------------------------------------------------------- live canonical
class LiveCanonical(unittest.TestCase):
    """Measured against canonical fe26f783. These assert the CURRENT true state, by name."""

    def test_the_perennial_roster_is_thirty_eight(self):
        self.assertEqual(len(perennials(load())), 38)

    def test_year_dup_is_clean_roster_wide(self):
        found = [v for c in perennials(load()) for v in year_dup_violations(c)]
        self.assertEqual(found, [], "intra-crop stage duplication appeared; read each hit")

    def test_estab_caption_gaps_are_exactly_the_two_known_shells(self):
        gaps = sorted({c["slug"] for c in perennials(load()) if estab_caption_violations(c)})
        # avocado and olive are uncertified shells (5 mushrooms + these 2 are the 7).
        self.assertEqual(gaps, [])   # neither shell renders pills: no years_to_first_harvest

    def test_pill_caption_is_now_ZERO_and_for_the_RIGHT_REASON(self):
        """Measured 4 at fe26f783 (artichoke x2, mandarin-clementine, orange-navel); measured 0
        after the PLA-6 Round 2 rollout. This test previously pinned those four BY NAME so the
        state could not change unnoticed, and it duly reddened the day they were repaired.

        ZERO IS AMBIGUOUS ON ITS OWN, so this asserts the reason as well: 0 findings because
        every pill-rendering perennial now carries `full_harvest_notes_*` and the family is
        therefore suppressed, NOT 0 because the gate stopped reaching anything. Without the
        second half, a scoping bug that silently emptied `renders_pills()` would read as success.
        """
        data = load()
        found = [v for c in perennials(data) for v in pill_caption_violations(c)]
        self.assertEqual(found, [])

        pills = [c for c in perennials(data) if renders_pills(c)]
        self.assertEqual(len(pills), 26, 'the gate stopped reaching the crops it scopes to')
        unmigrated = [c['slug'] for c in pills if not c.get('full_harvest_notes_beginner')]
        self.assertEqual(unmigrated, [], f'zero is not yet earned: {unmigrated}')

    def test_the_gate_still_fires_when_the_defect_is_reintroduced(self):
        """Reachability, kept live now that the roster is clean. A guard whose findings have gone
        to zero looks identical to one that never ran, so the arc's own defect is injected back
        and required to redden -- artichoke's mature-bed caption reverting to "Squeeze the bud."
        """
        data = load()
        artichoke = next(c for c in data['crops'] if c['slug'] == 'artichoke')
        del artichoke['full_harvest_notes_beginner']
        del artichoke['full_harvest_notes_seasoned']
        v = pill_caption_violations(artichoke)
        self.assertEqual(len(v), 2)
        self.assertIn('Squeeze the bud.', ' '.join(v))

    def test_every_pill_rendering_perennial_carries_a_dual_register_establishment_tip(self):
        bad = [c["slug"] for c in perennials(load())
               if renders_pills(c) and estab_caption_violations(c)]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
