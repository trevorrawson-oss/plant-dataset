import pytest
from planting_layout_gate import check_crop

def C(**kw):
    base = {"slug": "x"}
    base.update(kw)
    return base

def test_absent_field_is_noop():
    assert check_crop(C()) == []

def test_null_field_is_noop():
    assert check_crop(C(planting_layout=None)) == []

def test_block_with_min_rows_passes():
    assert check_crop(C(planting_layout="block", pollination_block_min_rows=4)) == []

def test_block_without_min_rows_fails():
    assert check_crop(C(planting_layout="block")) != []

def test_bad_enum_fails():
    assert check_crop(C(planting_layout="blocks")) != []

def test_min_rows_on_non_block_fails():
    assert check_crop(C(planting_layout="row", pollination_block_min_rows=4)) != []

def test_min_rows_below_floor_fails():
    assert check_crop(C(planting_layout="block", pollination_block_min_rows=1)) != []

def test_min_rows_non_int_fails():
    assert check_crop(C(planting_layout="block", pollination_block_min_rows="4")) != []

def test_min_rows_bool_fails():
    assert check_crop(C(planting_layout="block", pollination_block_min_rows=True)) != []

def test_orphan_min_rows_no_layout_fails():
    assert check_crop(C(pollination_block_min_rows=4)) != []

def test_valid_row_no_min_rows_passes():
    assert check_crop(C(planting_layout="row")) == []
