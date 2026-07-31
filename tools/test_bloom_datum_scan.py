"""Adversarial tests for tools/bloom_datum_scan.py.

The scan answers one question per cited document: does it publish a BLOOM DATE
(month-granular or better), or only bloom risk/management language?

The dangerous direction is a false CLEAR -- the scan reporting "no bloom date"
for a document that has one. That would let a declaration pass write
"the quantity is absent from the literature" onto a cell whose source does
publish it. Every test below that begins `test_no_false_clear_` guards that
direction; they are the ones that matter.

The known live counter-example is apples.extension.org, which states that apple
"will generally bloom in mid-April" in western North Carolina -- month-granular
bloom timing, published, and already cited in our data.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bloom_datum_scan as S  # noqa: E402


def cls(text):
    return S.classify(text)['verdict']


# --------------------------------------------------------------------------
# The false-CLEAR guards. A miss here silently authorises a false declaration.
# --------------------------------------------------------------------------

def test_no_false_clear_on_the_live_apple_counterexample():
    txt = ("Generally, apple trees grown in more southern and warmer climates "
           "with a shorter and mild winter will bloom earlier. For example, in "
           "western North Carolina apple trees will generally bloom in mid-April "
           "whereas apple trees in Minnesota do not bloom until a month later, "
           "generally in mid-May.")
    assert cls(txt) == 'PUBLISHES_TIMING'


def test_no_false_clear_on_bare_month_after_bloom():
    assert cls("Peach trees bloom in March in the low desert.") == 'PUBLISHES_TIMING'


def test_no_false_clear_when_month_precedes_bloom():
    assert cls("In early April, full bloom is typically reached.") == 'PUBLISHES_TIMING'


def test_no_false_clear_on_abbreviated_month():
    assert cls("Full bloom normally occurs about Apr. 10 in this district.") == 'PUBLISHES_TIMING'


def test_no_false_clear_on_blossom_and_flowering_synonyms():
    assert cls("Blossoms open in late February.") == 'PUBLISHES_TIMING'
    assert cls("Flowering occurs in May and June.") == 'PUBLISHES_TIMING'


def test_no_false_clear_across_newlines_and_whitespace():
    assert cls("bloom period\n\n     begins in\tearly   May 2024") == 'PUBLISHES_TIMING'


def test_no_false_clear_on_table_row_layout():
    # PDF/table extraction puts the crop, the bloom column and the month on one line.
    assert cls("Apricot   Bloom   Feb 15 - Mar 1   Harvest   June") == 'PUBLISHES_TIMING'


# --------------------------------------------------------------------------
# False-POSITIVE guards. Less dangerous, but a flood makes the report unreadable
# and "May" as a modal verb is the single most likely source of one.
# --------------------------------------------------------------------------

def test_may_as_modal_verb_is_not_a_bloom_date():
    assert cls("A warm spell may cause the tree to bloom prematurely.") == 'MENTION_NO_DATE'


def test_may_as_modal_verb_before_bloom_is_not_a_date():
    assert cls("Trees may bloom before the last frost and lose the crop.") == 'MENTION_NO_DATE'


def test_capitalised_may_at_sentence_start_is_still_a_modal():
    assert cls("May bloom be damaged by frost? Growers should scout.") == 'MENTION_NO_DATE'


def test_capitalised_may_as_real_month_is_caught():
    assert cls("Bloom begins the first week of May.") == 'PUBLISHES_TIMING'


def test_bloomington_is_not_a_bloom_word():
    assert cls("Bloomington field station, March trials.") == 'NO_MENTION'


def test_bloom_risk_language_without_a_date_is_mention_only():
    txt = ("Late blooming cultivars tend to escape frost. Apricot blooms early "
           "and is therefore unreliable.")
    assert cls(txt) == 'MENTION_NO_DATE'


def test_month_far_from_bloom_word_does_not_count():
    txt = ("Bloom is the most frost-sensitive stage. " + ("filler text. " * 40) +
           "Fertilise in March.")
    assert cls(txt) == 'MENTION_NO_DATE'


def test_no_bloom_word_at_all():
    assert cls("Plant bare-root trees in January. Harvest in July.") == 'NO_MENTION'


def test_empty_and_none_are_undetermined_not_absence():
    assert cls('') == 'NO_MENTION'
    assert S.classify(None)['verdict'] == 'UNDETERMINED'


# --------------------------------------------------------------------------
# Evidence capture -- the report must quote, so a human can read not count.
# --------------------------------------------------------------------------

def test_classify_returns_the_quoted_evidence():
    r = S.classify("Apple trees generally bloom in mid-April here.")
    assert r['verdict'] == 'PUBLISHES_TIMING'
    assert r['evidence'], 'must quote the sentence that carried the verdict'
    assert 'april' in r['evidence'].lower()


def test_unfetchable_document_is_undetermined_never_absence():
    # load_doc surfaces cache failures with a NUL sentinel; they must not read as "no bloom date".
    assert S.classify_doc('\x00FETCHFAIL HTTPError: 403')['verdict'] == 'UNDETERMINED'


# --------------------------------------------------------------------------
# Arm enumeration -- all three bloom encodings must be seen, not just the
# offset arms the handoff described.
# --------------------------------------------------------------------------

def _crop(slug, bloom):
    return {'slug': slug,
            'regions': {'r1': {'plantings': [{'bloom': bloom,
                                              'anchoring_urls': {}}]}}}


def test_enumerates_offset_arms():
    data = {'crops': [_crop('peach', [{'label': 'primary', 'from': 'last_frost',
                                       'offset_days': 7, 'window_days': 21,
                                       'sources': ['x'],
                                       'anchoring_urls': {'x': {'url': 'http://e/'}}}])]}
    arms = S.bloom_arms(data)
    assert len(arms) == 1
    assert arms[0]['shape'] == 'offset'
    assert arms[0]['urls'] == ['http://e/']


def test_enumerates_synthesis_window_arms():
    data = {'crops': [_crop('strawberry', [{'label': 'establishment', 'from': None,
                                            'window': 'Nov - Feb',
                                            'sources': ['y'],
                                            'anchoring_urls': {'y': {'url': 'http://f/'}}}])]}
    arms = S.bloom_arms(data)
    assert len(arms) == 1
    assert arms[0]['shape'] == 'synthesis_window'


def test_enumerates_month_literal_blooms():
    data = {'crops': [_crop('blueberry', ['April', 'June'])]}
    arms = S.bloom_arms(data)
    assert len(arms) == 1
    assert arms[0]['shape'] == 'month_literal'


def test_month_literal_inherits_the_planting_level_urls():
    data = {'crops': [{'slug': 'blueberry',
                       'regions': {'r1': {'plantings': [
                           {'bloom': ['April', 'June'],
                            'anchoring_urls': {'z': {'url': 'http://g/'}}}]}}}]}
    arms = S.bloom_arms(data)
    assert arms[0]['urls'] == ['http://g/'], 'literal blooms carry no arm urls of their own'
