#!/usr/bin/env python3
"""The reporting contract: predicates that refuse an unjustifiable ZERO and an unjustifiable
COMPLETION. Shared by the campaign repricers, `bare_host_scan` and `hunt_footprint`.

PLA-161. Zeros and completions fail differently, and the completion is the more dangerous of the
two, because **a zero invites suspicion and a completion does not.** Nobody re-reads a line that
says the work is done.

  PREDICATE 1 -- `assert_absence_reportable` lives in `cited_claim_scan` and is re-exported here.
                 A zero is an absence only when the instrument can show it read everything the
                 thing could be in.

  PREDICATE 2 -- `assert_completion_reportable`, below. A completion signal that COLLAPSES A UNIT
                 must report the residue at the finer unit.

WHY PREDICATE 2 EXISTS, measured. All four campaigns price work from `if not sole: continue`, and
`bare_host_scan` sets `is_sole=False` the moment a node cites anything pathed. So a decision whose
bare rows are ALL masked never entered any campaign's denominator. Campaign C closed on

    HONEST OPEN after re-scope :  0 of 25 decisions,   0 of 68 nodes

while its own seven hunts carried 196 MASKED node-citations over 39 MASKED-ONLY decisions. The
zero was true of what it counted and silent about what it had filtered away first.

The second half matters as much as the first: **a hunt that was FIXED and a hunt that was FILTERED
AWAY render identically** -- both contribute zero rows and vanish from the header. At `76f92a20`
hunt #24 is genuinely closed and hunt #17 is 0 SOLE / 18 MASKED, and nothing in the output told
them apart. `hunt_footprint` already solved this for its own table; this module is that behaviour
extracted so the repricers can adopt it rather than re-implement it.

DESIGN, inherited deliberately from predicate 1:
  * EVERY reason is collected and raised together, never returned on the first. Fixing the masked
    residue must not then reveal the unexplained-hunt problem as if it were news
    ([[guard-tests-pass-because-an-earlier-check-fires]]).
  * `unguarded_completion_line` is kept as THE WRONG METHOD so a mutation test can re-introduce
    the original defect and prove the guard fires.
"""
import sys

from cited_claim_scan import UnreportableAbsence, assert_absence_reportable  # noqa: F401


class UnreportableCompletion(Exception):
    """Raised when a completion signal cannot account for its own residue."""


def unguarded_completion_line(label, open_units, total_units, unit='decisions'):
    """THE WRONG METHOD, kept so the regression test can prove it lies. Do not call it.

    This is what every campaign printed: a clean `0 of N` with no reference to the population the
    SOLE filter removed before counting.
    """
    return '%s: %d of %d %s' % (label, open_units, total_units, unit)


def assert_completion_reportable(label, open_units, total_units, masked_units=0,
                                 masked_rows=0, hunts_expected=(), hunts_with_rows=(),
                                 empty_hunt_reasons=None, unit='decisions',
                                 masked_unit=None):
    """Raise unless a `0 of N` completion line could honestly be written down.

    `masked_units` / `masked_rows` are the population the SOLE filter removed from the scope this
    line reports on. `masked_unit` names ITS unit, which is NOT always the completion line's unit:
    campaign D's line counts HUNTS while its residue counts DECISIONS, and labelling the residue
    'hunts' there would be exactly the unit slide this arc keeps re-pricing itself with. Defaults
    to `unit` when the two genuinely match. `hunts_expected` is every hunt the scope claims to cover; `hunts_with_rows`
    is those that actually produced rows; `empty_hunt_reasons` maps a hunt that produced none to
    WHY -- 'fixed', 'fully masked', 'withdrawn'. A hunt in neither set is unexplained, and an
    unexplained empty hunt is indistinguishable from a completed one.

    Returns True when the line is honest. Never returns False -- it raises, because a caller that
    ignores a False keeps printing the zero.
    """
    reasons = []

    if masked_units or masked_rows:
        reasons.append(
            'the scope carries %d masked-only %s (%d masked node-citations) that the SOLE filter '
            'removed before counting -- a "%d of %d %s" line reports only what survived the filter'
            % (masked_units, masked_unit or unit, masked_rows, open_units, total_units, unit))

    unexplained = [h for h in hunts_expected
                   if h not in set(hunts_with_rows) and h not in set(empty_hunt_reasons or {})]
    if unexplained:
        reasons.append(
            'hunt(s) %s produced no rows and no reason was given -- a hunt that was FIXED and a '
            'hunt that was FILTERED AWAY render identically, so an empty hunt must say which it is'
            % ', '.join('#%s' % h for h in sorted(unexplained, key=str)))

    if total_units == 0:
        reasons.append(
            'the denominator is 0, so this line establishes nothing -- an empty scope is '
            'UNDETERMINED, not complete')

    if reasons:
        raise UnreportableCompletion('%s: %s' % (label, '; '.join(reasons)))
    return True


def completion_line(label, open_units, total_units, unit='decisions', **contract):
    """The guarded replacement for `unguarded_completion_line`.

    Returns the line only when the contract holds; otherwise the caller gets the exception and
    must print UNDETERMINED with the reasons rather than a zero.
    """
    assert_completion_reportable(label, open_units, total_units, unit=unit, **contract)
    return unguarded_completion_line(label, open_units, total_units, unit)


def describe_refusal(exc):
    """Render a refusal the way a scan should print it: UNDETERMINED, with every reason."""
    return 'UNDETERMINED -- %s' % exc


if __name__ == '__main__':
    print(__doc__)
    sys.exit(0)
