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


if __name__ == "__main__":
    test_pnw_batch_shape()
    test_no_duplicate_slugs()
    test_base_sha_defaults_to_live_canonical()
    print("ok")
