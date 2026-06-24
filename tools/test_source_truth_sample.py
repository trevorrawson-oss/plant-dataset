#!/usr/bin/env python3
"""Smoke + unit tests for the source-truth sampling helper (read-only reporting)."""
import source_truth_sample as sts


def test_effective_plant_unions_plant_out_and_calendar():
    # plant_out names Jan only; calendar has plant tokens in Aug+Nov -> union of both.
    cal = ['plant', 'cold_pause', 'cold_pause', 'harvest', 'heat_pause', 'heat_pause',
           'heat_pause', 'plant', 'harvest', 'harvest', 'plant', 'plant']
    eff = sts.effective_plant_months('Jan 1 - Jan 31', cal)
    assert eff == ['Jan', 'Aug', 'Nov', 'Dec'], eff


def test_effective_plant_handles_null_plant_out():
    # region-primary direct-sow cell: plant_out is None, windows live in calendar.
    cal = ['cold_pause', 'cold_pause', 'cold_pause', 'plant', 'plant', 'plant',
           'plant', 'growing', 'harvest', 'harvest', 'cold_pause', 'cold_pause']
    eff = sts.effective_plant_months(None, cal)
    assert eff == ['Apr', 'May', 'Jun', 'Jul'], eff


def test_tok_months_ignores_non_12_length():
    assert sts.tok_months(['plant'] * 5, 'plant') == []
    assert sts.tok_months(None, 'plant') == []


def test_render_groups_by_region():
    cell = {
        'plant_out': None,
        'harvest': 'Sep - Oct',
        'calendar': ['cold_pause', 'cold_pause', 'cold_pause', 'plant', 'plant',
                     'plant', 'plant', 'growing', 'harvest', 'harvest',
                     'cold_pause', 'cold_pause'],
    }
    region = {'region_label': 'Northern Tier', 'resolved_by_zone': {'3': cell}}
    crop = {'slug': 'carrot', 'regions': {'northern_tier': region}}
    data = {'crops': [crop]}
    out = sts.render(data, ['carrot'], ['northern_tier'])
    assert 'REGION: northern_tier' in out
    assert "EFFECTIVE plant" in out
    assert "['Apr', 'May', 'Jun', 'Jul']" in out
    assert "harvest string: 'Sep - Oct'" in out


if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
            print(f'ok  {name}')
    print('all source_truth_sample tests passed')
