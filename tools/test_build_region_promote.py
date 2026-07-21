import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_region_promote as brp


def test_pnw_batch_shape():
    batch = brp.build("pnw", base_sha="deadbeef")
    assert batch["base_sha"] == "deadbeef"
    patches = batch["patches"]
    cells = [p for p in patches if p["json_path"].endswith(".regions.pnw")]
    assert len(cells) == 108, len(cells)
    assert all(p["op"] == "add" for p in cells)  # each pnw cell is net-new
    # every cell path uses the apply_patch slug-filter form
    assert all(p["json_path"].startswith("$.crops[?(@.slug=='") for p in cells)
    # top-level: chill band is an ADD (dict key); provenance is a REPLACE of the global string
    top = {p["json_path"]: p for p in patches if not p["json_path"].endswith(".regions.pnw")}
    assert len(top) == 2, list(top)
    assert top["$.region_chill_delivered.pnw"]["op"] == "add"
    prov = top["$.region_chill_delivered_provenance"]
    assert prov["op"] == "replace" and "from" in prov
    assert prov["value"].startswith(prov["from"])  # appends, never truncates the prior note
    assert "pnw" in prov["value"][len(prov["from"]):].lower()  # the pnw note was appended


def test_no_duplicate_slugs():
    batch = brp.build("pnw", base_sha="x")
    slugs = [p["json_path"] for p in batch["patches"] if p["json_path"].endswith(".regions.pnw")]
    assert len(slugs) == len(set(slugs)) == 108


def test_base_sha_defaults_to_live_canonical():
    import hashlib
    live = hashlib.sha256(open(brp.CANON, "rb").read()).hexdigest()
    batch = brp.build("pnw")
    assert batch["base_sha"] == live


# ---- mid_atlantic registration (Task 2 of the 2026-07-20 Mid-Atlantic region arc) ----
# Task 2 only registers the STAGING/EXPECTED_CELLS entries; the 5 staging files themselves
# are authored later (Tasks 4-7). So this test only pins the registration shape (file names +
# the 111 expected-cell count constant), NOT a full brp.build("mid_atlantic") batch run --
# that needs real staging files on disk and is exercised once Tasks 4-7 land.

def test_mid_atlantic_registered():
    import build_region_promote as brp
    assert "mid_atlantic" in brp.STAGING
    assert brp.EXPECTED_CELLS["mid_atlantic"] == 111
    files, band = brp.STAGING["mid_atlantic"]
    assert band == "mid_atlantic_chill_band.json"
    assert set(files) == {
        "mid_atlantic_annuals_cool.json", "mid_atlantic_annuals_warm.json",
        "mid_atlantic_trees.json", "mid_atlantic_citrus.json", "mid_atlantic_perennials.json"}
    print("  ok: mid_atlantic STAGING + EXPECTED_CELLS registered (111 cells, 5 staging files)")


def test_mid_south_registered():
    import build_region_promote as brp
    assert "mid_south" in brp.STAGING
    assert brp.EXPECTED_CELLS["mid_south"] == 111
    files, band = brp.STAGING["mid_south"]
    assert band == "mid_south_chill_band.json"
    assert set(files) == {
        "mid_south_annuals_cool.json", "mid_south_annuals_warm.json",
        "mid_south_trees.json", "mid_south_citrus.json", "mid_south_perennials.json"}
    print("  ok: mid_south STAGING + EXPECTED_CELLS registered (111 cells, 5 staging files)")


if __name__ == "__main__":
    test_pnw_batch_shape()
    test_no_duplicate_slugs()
    test_base_sha_defaults_to_live_canonical()
    test_mid_atlantic_registered()
    test_mid_south_registered()
    print("ok")
