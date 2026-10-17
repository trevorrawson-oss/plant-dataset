"""PLA-750: build the ruled per-crop table from the evidence files + ruling 47a09951.

Every quote is READ from research/*.json (the 301 quotes verify750.py checked
against the fetched bytes), never retyped. Output: ruled_table.json.
The sowing-ceiling values are PROPOSED: the field's name and shape wait on the
D1 approval in the promote plan.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = {}
for f in sorted((HERE / "research").glob("*.json")):
    R.update(json.loads(f.read_text()))


def quote(slug, needle):
    hits = [e for e in R[slug]["evidence"] if needle in e["quote"]]
    if len(hits) != 1:
        raise SystemExit(f"{slug}: {len(hits)} evidence rows match {needle!r}")
    e = hits[0]
    return {"quote": e["quote"], "source_name": e["source_name"], "url": e["url"],
            "tier": e["tier"], "mech": e["mech"]}


# HOLD (ruling: 11 keeps minus sweet alyssum under D3) -> pause_in_heat true.
HOLD = {
    "spinach": dict(temp_f=80, measures="air", basis="sowing_statement",
                    claim=("spinach", "until outdoor temperatures reach 80"), temp=None),
    "lettuce-leaf": dict(temp_f=80, measures="soil", basis="germination",
                         claim=("lettuce-leaf", "Soil temperatures above 80"), temp=None, d2_proxy=True),
    "cilantro-coriander": dict(temp_f=75, measures="soil", basis="bolting",
                               claim=("cilantro-coriander", "keep the soil temperature below 75"), temp=None,
                               d2_proxy=True),
    "beet": dict(temp_f=80, measures="soil", basis="germination",
                 claim=("beet", "Temperatures above 80°F reduce seed germination"), temp=None, d2_proxy=True,
                 flag="claim sentence does not say 'soil' (plan row P3)"),
    "radish": dict(temp_f=75, measures="air", basis="maturity_coupled",
                   claim=("radish", "when temperatures are 50-75 degrees"), temp=None,
                   flag="page gives 'degrees' with no unit or medium (plan row P3)"),
    "kohlrabi": dict(temp_f=75, measures="air", basis="maturity_coupled",
                     claim=("kohlrabi", "Avoid planting after May 1"),
                     temp=("kohlrabi", "do not exceed 75")),
    "sugar-snap-peas": dict(temp_f=80, measures="air", basis="germination",
                            claim=("sugar-snap-peas", "soil and air temperatures to remain below 80"), temp=None),
    "snow-peas": dict(temp_f=80, measures="air", basis="germination",
                      claim=("snow-peas", "soil and air temperatures to remain below 80"), temp=None),
    "calendula": dict(temp_f=86, measures="air", basis="sowing_statement",
                      claim=("calendula", "should only be sown in the field"), temp=None,
                      flag="30°C = 86°F from the sowing source; the report's 85 is USU's bloom number (plan row P2)"),
    "viola": dict(temp_f=75, measures="soil", basis="germination",
                  claim=("viola", "only germinate at temperatures between"), temp=None, d2_proxy=True,
                  flag="claim sentence does not say 'soil' (plan row P3)"),
}

# FALSE: the 10 ruled changes, the 9 unsourced holds (carrot is in both lists in
# the ruling; one row), and sweet alyssum (D3). note_quote = the M quote the
# ruling says to carry ("so the next pass starts from it"), or the decisive
# quote for a ruled change.
FALSE = {
    # 10 ruled changes
    "celery": ("change", ("celery", "Average high temperature above 75")),
    "spring-onion": ("change", ("spring-onion", "Green onions are plant")),
    "broccoli": ("change", ("broccoli", "can cause broccoli to grow no crown")),
    "cauliflower": ("change", ("cauliflower", "Cauliflower grows best when temperatures do not exceed 75")),
    "cabbage": ("change", ("cabbage", "Cabbage grows best when temperatures do not exceed 80")),
    "brussels-sprouts": ("change", ("brussels-sprouts", "High summer temperatures reduce plant growth")),
    "kale": ("change", ("kale", "flavor is best if you harvest the plants before the weather becomes hot")),
    "collards": ("change", ("collards", "Collards are more heat-tolerant than kale")),
    "edamame": ("change", ("edamame", "plant every 7-14 days up to mid-July")),
    "borage": ("change", ("borage", "successive sowings of seed at four week intervals")),
    # 9 unsourced holds -> false until a source is found
    "carrot": ("unsourced", ("carrot", "Seeds will not germinate above 95")),
    "arugula": ("unsourced", ("arugula", "Arugula bolts due to longer days and high temperatures")),
    "dill": ("unsourced", ("dill", "At the onset of hot weather")),
    "turnip": ("unsourced", ("turnip", "Turnips grow best when temperatures do not exceed 85")),
    "parsley": ("unsourced", ("parsley", "Parsley 75/50-85 40/90")),
    "bok-choy": ("unsourced", ("bok-choy", "Warm weather can cause bok choy to flower")),
    "sweet-pea": ("unsourced", ("sweet-pea", "will bloom poorly (or not at all) when weather is hot")),
    "nasturtium": ("unsourced", ("nasturtium", "will tend to decline when the temperatures get too hot")),
    "chamomile": ("unsourced", ("chamomile", "Under warm conditions, germination generally occurs within a week")),
    # D3
    "sweet-alyssum": ("d3_flip", ("sweet-alyssum", "alyssum grown from seed may stop producing flowers")),
}

D4 = {"broccoli": "head_forming", "cauliflower": "curd_forming", "brussels-sprouts": "sprout_formation",
      "cabbage": "head_forming", "kale": "harvest", "collards": "harvest"}
D5 = ["sweet-pea", "sweet-alyssum", "nasturtium"]
LIVE = {
    "lettuce-leaf": "re-point tip_85e7xx84 to USU leafy greens",
    "arugula": "rewrite tip_aru_germ1 (+ start_method notes) to what SARE and Steiner support",
    "cilantro-coriander": "move tip_cil_germ1's 75°F to a bolting tip",
    "viola": "re-anchor vio_germ_cool_dark to UF (FP609 / Gardening Solutions); drop the light claim",
    "calendula": "anchor cal_germ_coolsoil to Eberle 2014 (D6)",
    "borage": "drop bor_germ_timing's heat clause",
    "spinach": "re-anchor both germination tips from the evidence file",
    "edamame": "strike the unsupported weather-trigger prose",
    "celery": "strike the unsupported weather-trigger prose",
    "chamomile": "strike the unsupported weather-trigger prose",
}

rows = []
for slug, h in HOLD.items():
    row = {"slug": slug, "verdict": "hold", "pause_in_heat": True,
           "sowing_heat_ceiling": {"temp_f": h["temp_f"], "measures": h["measures"], "basis": h["basis"],
                                   "claim": quote(*h["claim"]),
                                   "temp": quote(*h["temp"]) if h["temp"] else "same as claim"},
           "d2_soil_proxy": bool(h.get("d2_proxy")), "flag": h.get("flag")}
    rows.append(row)
for slug, (cls, q) in FALSE.items():
    rows.append({"slug": slug, "verdict": cls, "pause_in_heat": False,
                 "sowing_heat_ceiling": {"temp_f": None, "note_quote": quote(*q)}})
for r in rows:
    r["d4_stage"] = D4.get(r["slug"])
    r["d5_enum_correction"] = r["slug"] in D5
    r["live_fix"] = LIVE.get(r["slug"])

assert len(rows) == 30 and len({r["slug"] for r in rows}) == 30
assert sum(r["pause_in_heat"] for r in rows) == 10
(HERE / "ruled_table.json").write_text(json.dumps(
    {"ruling": "PLA-750 comment 47a09951 (2026-10-17)", "canonical_measured_on": "2f67359e",
     "rows": sorted(rows, key=lambda r: r["slug"])}, ensure_ascii=False, indent=1) + "\n")
print(f"ruled_table.json: {len(rows)} rows, hold {sum(r['pause_in_heat'] for r in rows)}, "
      f"false {sum(not r['pause_in_heat'] for r in rows)}")
