#!/usr/bin/env python3
"""PLA-256 task 1 -- export the register-pair frame.

Every path in canonical where a `_beginner` and a `_seasoned` sibling BOTH exist and
BOTH are non-empty. One record per pair, both texts complete, sharded by crop.

WHAT THIS DELIBERATELY DOES NOT DO
----------------------------------
No similarity score. Not character overlap, not a token ratio, not a diff, not a
length delta. PLA-256's whole premise is that a similarity metric already answered
this question (0.4%) and reading contradicted it by two orders of magnitude (40%).
A score in the export would anchor the reader against the instrument this frame
exists to replace. There is nothing here to sort by except the data itself.

No sampling, filtering, ranking or deduping either. The whole frame ships.

THE ONE EXCLUSION, WHICH IS THE SPEC AND NOT A FILTER
-----------------------------------------------------
"both non-empty" is the stated definition. 683 structurally-paired sites have one or
both sides null/empty; they are counted and reported, not silently dropped.

RENDER STATUS
-------------
Bucket A/B/C per PLA-255's key inventory. That inventory was never persisted as a
file -- it lives only in the Linear description -- so the classification below was
rebuilt by grepping both app repos (plant-app + plant-astro, 1,299 code files) and
READING the hits. Three traps had to be walked past, each of which produces a wrong
answer on a naive grep:

  1. TEMPLATE-LITERAL ACCESS. `feeding-guide.ts` does f[`${base}_beginner`], and
     `guide-phases.ts` exports registerNote(source, base, level). A literal grep for
     `hardiness_notes_beginner` returns ZERO -- and the field is read and rendered by
     CitrusFrostCard via registerNote(guide, 'hardiness_notes', level).
  2. BUILD-TIME RENAMING. `build-guides-data.mjs` maps how_it_works_* -> how_* and
     label_note_* -> label_*. Grepping canonical's key names finds nothing.
  3. SUBSTRING COLLISION. `note_beginner` matches inside `suitability_note_beginner`;
     `message_beginner` inside `notify_message_beginner`; `notes_beginner` inside
     `region_notes_beginner`. All matching here is identifier-boundary anchored.

Also excluded from "is it read" evidence: the export-boundary scripts
(export-projection / verify-export-projection / mutate-export-projection-gate). Those
enumerate key NAMES to decide what ships; they do not read values. Counting them as
reads would have made `bloom_time` and `chill_basis` look live.

  A -- read AND rendered: some component prints the authored text.
  B -- read, NOT rendered: reaches product code but is never printed as authored copy.
       In practice B here means exactly one thing: the field is copied wholesale into
       Herb's LLM grounding slice (`herb/slice.ts` FACT_KEYS) and nowhere else. The
       grower may see an LLM paraphrase; they never see this prose.
  C -- never referenced: no product code reads the pair at that path.

Classification is PATH-KEYED, not name-keyed -- the repo's own standing lesson.
`note` is Bucket A at `ph.note` and Bucket C at `harvest_stop_rule.note`. A
name-keyed table would call both the same and be wrong about one of them.

READ-ONLY. Opens canonical, writes only under tools/staging/.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "crops_data_final.json")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "staging", "pla256_register_pair_frame")

BEG, SEA = "_beginner", "_seasoned"

# --- render-status table -----------------------------------------------------
# Keyed on (generalized container path, leaf key). Value: (bucket, evidence).
# Evidence names the file that decides it, so a future reader can re-check the call
# rather than re-derive the verdict.
A = "A"; B = "B"; C = "C"

RENDER = {
    # ---- crop root -----------------------------------------------------------
    ("", "description"):        (A, "HeroCard.astro / learn/[slug].tsx:292"),
    ("", "harvest_ready"):      (A, "HarvestYieldPair.astro / registerNote in [slug].tsx:366"),
    ("", "chill_hours_note"):   (A, "BerryChillCard + tree/ChillHoursCard"),
    ("", "pollinator_notes"):   (A, "tree/BloomPollinationCard.astro:117"),
    ("", "hardiness_notes"):    (A, "CitrusFrostCard.tsx:34 registerNote -- NO literal grep hit"),
    ("", "deadheading"):        (A, "guides/crops/[crop]/[zone].astro"),
    ("", "type_selection"):     (A, "guides/crops/[crop]/[zone].astro"),
    ("", "renovation"):         (A, "BerryYearCalendarCard + guide-perennial-calendar.ts:370"),
    ("", "soil_prep"):                        (C, "no reference in either repo"),
    ("", "bloom_time"):                       (C, "export-projection.mjs only -- that is the allowlist, not a read"),
    ("", "year_one_notes"):                   (C, "no reference"),
    ("", "tip"):                              (C, "no reference (tip_* hits are succession_policy)"),
    ("", "planting_method_notes"):            (C, "no reference"),
    ("", "cane_management"):                  (C, "export-projection.mjs only"),
    ("", "disease_resistance_notes_default"): (C, "no reference"),
    ("", "harvest_ramp_na"):                  (C, "no reference"),
    # ---- simple containers ---------------------------------------------------
    ("ph", "note"):                     (A, "PhCard.astro:56 / guide-chapters.ts:169"),
    ("companions", "note"):             (A, "CompanionsCard.astro:142"),
    ("companions", "good"):             (A, "guide-chapters.ts:206 fallback comp.good_beginner"),
    ("companions", "bad"):              (A, "guide-chapters.ts:207 fallback comp.bad_beginner"),
    ("companions.good_beginner_seasoned[]", "why"): (A, "CompanionsCard.astro:200"),
    ("companions.bad_beginner_seasoned[]", "why"):  (A, "CompanionsCard.astro:227"),
    ("fertilizer", "notes"):            (A, "FeedingCard.astro:109"),
    ("fertilizer", "amount"):           (A, "feeding-guide.ts:77 pair(f,'amount')"),
    ("fertilizer", "npk_hint"):         (A, "FeedingCard.astro / feeding-guide npkBadge"),
    ("fertilizer", "notify_message"):   (A, "FeedingCard.astro"),
    ("watering", "frequency"):          (A, "WateringCard.astro / guide-chapters.ts:189"),
    ("watering", "amount"):             (A, "WateringCard.astro:82"),
    ("watering", "method"):             (A, "WateringCard.astro / guide-chapters.ts:191"),
    ("watering", "signs_overwater"):    (A, "WateringCard.astro / guide-chapters.ts:192"),
    ("watering", "signs_underwater"):   (A, "WateringCard.astro / guide-chapters.ts:193"),
    ("watering", "method_note"):        (B, "no renderer; watering is in herb FACT_KEYS"),
    ("watering", "critical_periods"):   (B, "no renderer; watering is in herb FACT_KEYS"),
    ("watering.schedule_by_stage[]", "note"): (A, "stage-watering.ts:24 -> guide-journey.ts:48"),
    ("start_method", "notes"):          (A, "TimingSpineCard.astro:87 / StartFromSeedCard.tsx:34"),
    ("start_method", "hardening_off"):  (A, "TimingSpineCard.astro / [zone].astro:464"),
    ("storage", "room_temp"):           (A, "StoringCard.astro / guide-chapters.ts:216"),
    ("storage", "fridge"):              (A, "StoringCard.astro / guide-chapters.ts:217"),
    ("storage", "freezer"):             (A, "StoringCard.astro / guide-chapters.ts:218"),
    ("storage", "notes"):               (A, "StoringCard.astro:78"),
    ("varieties", "note"):              (A, "RecommendedVarietiesCard.astro:48"),
    ("varieties.recommended[]", "note"):(A, "varieties.ts:94 noteBeginner/noteSeasoned"),
    ("rotation", "note"):               (A, "RotationCard.astro:52"),
    ("rotation", "avoid_after"):        (A, "RotationCard.astro"),
    ("soil", "preferred_description"):  (A, "guide-chapters.ts / [zone].astro"),
    # the *_texture pairs are SHADOWED: renderers read *_texture_core and
    # *_texture_seasoned. The *_beginner sibling (46 crops) is read by nothing.
    ("soil", "preferred_texture"):      (C, "guide-chapters.ts:168 reads _core/_seasoned, never _beginner"),
    ("soil", "tolerated_texture"):      (C, "guide-chapters.ts:173 reads _core/_seasoned, never _beginner"),
    ("soil", "problematic_texture"):    (C, "guide-chapters.ts:174 reads _core/_seasoned, never _beginner"),
    ("yield_expectations", "per_plant"):       (A, "HarvestYieldPair.astro / guide-chapters.ts:214"),
    ("yield_expectations", "first_year_note"): (A, "HarvestYieldPair.astro"),
    ("yield_expectations", "peak_production"): (A, "HarvestYieldPair.astro"),
    ("succession_policy", "tip"):       (A, "SuccessionCard.astro:402 / PlantingCalendarCard.astro:373"),
    ("pruning_window", "note"):         (A, "BerryYearCalendarCard.astro:186"),
    ("photoperiod", "explainer"):       (A, "PhotoperiodCard.astro"),
    ("bolting", "note"):                (B, "no renderer; bolting is in herb FACT_KEYS"),
    ("bolting", "prevention"):          (B, "no renderer; bolting is in herb FACT_KEYS"),
    ("container_notes", "notes"):                  (C, "CareGuideCard reads unsuffixed .notes only"),
    ("container_notes", "self_watering_notes"):    (C, "no reference"),
    ("container_notes", "watering_adjustment"):    (C, "no reference"),
    ("container_notes", "fertilizer_adjustment"):  (C, "no reference"),
    ("container_notes", "shape_requirements"):     (C, "no reference"),
    ("container_notes", "container_overwintering"):(C, "no reference"),
    ("container_notes.soil_mix", "type"):          (C, "soil_mix never referenced"),
    ("container_notes.soil_mix", "amendments"):    (C, "soil_mix never referenced"),
    ("container_notes.overwintering", "approach"): (C, "overwintering never referenced"),
    ("container_notes.drainage", "saucer_practice"):(C, "no reference"),
    ("pollination", "notes"):           (C, "BloomPollinationCard reads crop.pollinator_notes_*, not pollination.notes_*"),
    ("thinning", "tip"):                (C, "no reference"),
    ("indoor_cycle", "tip"):            (C, "no reference"),
    ("det_indet", "detail"):            (C, "no reference"),
    ("dormancy_window", "note"):        (C, "dormancy_window never referenced"),
    ("harvest_stop_rule", "note"):      (C, "harvest_stop_rule never referenced"),
    ("winter_hardiness", "explainer"):  (C, "winter_hardiness never referenced"),
    ("rootstock_options[]", "traits"):  (C, "TreeRootstockCard reads recommended_rootstock_note, not traits"),
    # ---- arrays --------------------------------------------------------------
    ("growth_stages[]", "user_action"):      (A, "GrowingJourneyCard.astro / guide-journey.ts:58"),
    ("growth_stages[]", "what_to_look_for"): (A, "GrowingJourneyCard.astro / guide-journey.ts:57"),
    ("growth_stages[]", "log_prompt"):       (A, "note-prompts.ts:140 journal prompt fallback"),
    ("growth_stages[]", "timing"):           (B, "no renderer; growth_stages is in herb FACT_KEYS"),
    ("tips_by_stage.<stage>[]", "text"):     (A, "GrowingJourneyCard.astro:230 / guide-journey.ts:59"),
    ("notifications[]", "title"):   (A, "PlantNotificationsCard.astro:74"),
    ("notifications[]", "body"):    (A, "PlantNotificationsCard.astro:82"),
    ("notifications[]", "message"): (C, "no reference (message_* hits were notify_message_*)"),
    ("weather_triggers[]", "title"): (B, "herb/slice.ts FACT_KEYS only -- no renderer in either repo"),
    ("weather_triggers[]", "body"):  (B, "herb/slice.ts FACT_KEYS only -- no renderer in either repo"),
    ("failure_diagnostics[]", "label"):           (A, "CommonProblemsCard.astro:87"),
    ("failure_diagnostics[]", "what_happened"):   (A, "CommonProblemsCard.astro:93"),
    ("failure_diagnostics[]", "next_season_tip"): (A, "CommonProblemsCard.astro:102"),
    ("failure_diagnostics[]", "cause"):      (B, "not in the 3 slots either renderer reads; in herb FACT_KEYS"),
    ("failure_diagnostics[]", "symptom"):    (B, "not read by either renderer; in herb FACT_KEYS"),
    ("failure_diagnostics[]", "fix"):        (B, "not read by either renderer; in herb FACT_KEYS"),
    ("failure_diagnostics[]", "prevention"): (B, "not read by either renderer; in herb FACT_KEYS"),
    ("regions.<R>", "region_notes"): (C, "referenced nowhere in either repo (PLA-255 finding)"),
    ("regions.<R>", "chill_basis"):  (C, "verify-export-projection.mjs only"),
    ("regions.<R>", "cold_basis"):   (C, "no reference"),
    ("regions.<R>", "heat_basis"):   (C, "no reference"),
    ("regions.<R>.plantings[]", "synthesis_note"): (C, "no reference"),
    ("regions.<R>.resolved_by_zone.<Z>", "suitability_note"):
        (A, "TreeCalendarCard/HardinessFruitingCard + registerNote in [slug].tsx:454 -- SEE PLA-323"),
    ("regions.<R>.resolved_by_zone.<Z>", "grown_as_note"):
        (A, "BerryYearCalendarCard + guide-perennial-calendar contextNoteBase"),
    ("regions.<R>.resolved_by_zone.<Z>", "day_length_note"):
        (A, "PhotoperiodCard.astro / guide-calendar.ts"),
    ("regions.<R>.resolved_by_zone.<Z>", "synthesis_note"): (C, "no reference"),
    ("regions.<R>.resolved_by_zone.<Z>", "type_note"):      (C, "no reference"),
    ("regions.<R>.resolved_by_zone.<Z>", "region_notes"):   (C, "referenced nowhere in either repo"),
    ("regions.<R>.tip_overrides.<stage>[]", "text"): (C, "tip_overrides never referenced"),
    ("zones.<Z>", "safe_sowing_note"): (C, "no reference"),
    ("pesticide_safety_education", "label_note"):         (A, "build-guides-data.mjs:214 -> safetyEducation -> pest-control page"),
    ("pesticide_safety_education", "preharvest_interval"):(A, "build-guides-data.mjs:216 -> safetyEducation"),
    ("pesticide_safety_education", "pollinator_note"):    (A, "build-guides-data.mjs:218 -> safetyEducation"),
    ("pesticide_safety_education", "handling_note"):      (A, "build-guides-data.mjs:220 -> safetyEducation"),
    ("pesticide_safety_education", "resistance_note"):    (A, "build-guides-data.mjs:222 -> safetyEducation"),
}
# pests[] and diseases[] share one shape, handled by rule below.
PROBLEM_LEAVES = {
    "name":              (A, "pest-control.ts:108 / guide-chapters.ts:115"),
    "description":       (A, "pest-control.ts:116 'What it is' slot"),
    "symptoms":          (A, "pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:117"),
    "cause":             (A, "pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:118"),
    "organic_treatment": (A, "pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:119"),
    "prevention":        (A, "pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:120"),
    "note":              (B, "entry-level note is not a slot; pests/diseases in herb FACT_KEYS"),
    "management":        (B, "no renderer; in herb FACT_KEYS"),
    "identification":    (B, "no renderer; in herb FACT_KEYS"),
}

BUCKET_LABEL = {
    A: "A -- read and rendered",
    B: "B -- read, not rendered (Herb LLM grounding slice only)",
    C: "C -- never referenced in either app repo",
}


def classify(container, leaf):
    if container in ("pests[]", "diseases[]") and leaf in PROBLEM_LEAVES:
        return PROBLEM_LEAVES[leaf]
    if container in ("pests[].control_ladder[]", "diseases[].control_ladder[]") and leaf == "note":
        return (A, "pest-control.ts:177 buildLadderRungs / guide-chapters.ts:99 ladderRungs")
    if container.startswith("control_methods.") and leaf == "how_it_works":
        return (A, "build-guides-data.mjs:201 how_it_works_* -> how_* -> MethodSheet + pest-control page")
    return RENDER.get((container, leaf), (None, None))


def nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def main():
    with open(CANON, encoding="utf-8") as fh:
        data = json.load(fh)

    region_ids, zone_ids = set(), set()
    for c in data["crops"]:
        region_ids.update((c.get("regions") or {}).keys())
        zone_ids.update((c.get("zones") or {}).keys())

    def generalize(path):
        p = re.sub(r"\[\d+\]", "[]", path)
        segs = p.split(".") if p else []
        out = []
        for i, s in enumerate(segs):
            bare = s.split("[")[0]
            prev = segs[i - 1] if i else ""
            if prev == "regions" and bare in region_ids:
                s = "<R>" + s[len(bare):]
            elif prev == "zones" and bare in zone_ids:
                s = "<Z>" + s[len(bare):]
            elif prev == "resolved_by_zone":
                s = "<Z>" + s[len(bare):]
            elif prev in ("tips_by_stage", "tip_overrides"):
                s = "<stage>" + s[len(bare):]
            out.append(s)
        return ".".join(out)

    records = []
    empty_side = []
    unclassified = set()

    def walk(node, path, crop_slug):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.endswith(BEG):
                    base = k[: -len(BEG)]
                    sib = base + SEA
                    if sib in node:
                        bv, sv = node[k], node[sib]
                        if nonempty(bv) and nonempty(sv):
                            gen = generalize(path)
                            bucket, ev = classify(gen, base)
                            if bucket is None:
                                unclassified.add((gen, base))
                                bucket, ev = "UNCLASSIFIED", "no table entry"
                            records.append({
                                "crop_slug": crop_slug,
                                "field_path": f"{path}.{base}" if path else base,
                                "container_path": path,
                                "leaf_key": base,
                                "field_family": f"{gen} :: {base}" if gen else f"(crop root) :: {base}",
                                "value_type": type(bv).__name__,
                                "beginner_key": k,
                                "seasoned_key": sib,
                                "beginner": bv,
                                "seasoned": sv,
                                "render_status": bucket,
                                "render_status_label": BUCKET_LABEL.get(bucket, bucket),
                                "render_evidence": ev,
                            })
                        else:
                            empty_side.append({
                                "crop_slug": crop_slug,
                                "field_path": f"{path}.{base}" if path else base,
                                "beginner_empty": not nonempty(bv),
                                "seasoned_empty": not nonempty(sv),
                            })
                walk(v, f"{path}.{k}" if path else k, crop_slug)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]", crop_slug)

    for crop in data["crops"]:
        walk(crop, "", crop["slug"])
    # top-level shared catalogs (control_methods, pesticide_safety_education)
    walk({k: v for k, v in data.items() if k != "crops"}, "", "_catalog")

    if unclassified:
        print("UNCLASSIFIED FAMILIES -- refusing to ship an unlabelled frame:", file=sys.stderr)
        for g, b in sorted(unclassified):
            print(f"  {g or '(crop root)'} :: {b}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTDIR, exist_ok=True)
    for fn in os.listdir(OUTDIR):
        os.remove(os.path.join(OUTDIR, fn))

    by_crop = defaultdict(list)
    for r in records:
        by_crop[r["crop_slug"]].append(r)
    for slug, rows in by_crop.items():
        with open(os.path.join(OUTDIR, f"{slug}.json"), "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTDIR, "_all_records.jsonl"), "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_status = Counter(r["render_status"] for r in records)
    by_family = Counter(r["field_family"] for r in records)
    fam_status = {}
    for r in records:
        fam_status[r["field_family"]] = r["render_status"]
    by_crop_n = Counter(r["crop_slug"] for r in records)
    by_type = Counter(r["value_type"] for r in records)

    manifest = {
        "canonical_sha_note": "run shasum -a 256 crops_data_final.json to confirm",
        "record_count": len(records),
        "crops_with_pairs": len(by_crop),
        "distinct_field_families": len(by_family),
        "excluded_one_side_empty": len(empty_side),
        "by_render_status": dict(by_status),
        "by_value_type": dict(by_type),
        "by_field_family": [
            {"field_family": f, "pairs": n, "render_status": fam_status[f]}
            for f, n in by_family.most_common()
        ],
        "by_crop": dict(by_crop_n.most_common()),
        "one_side_empty_detail": empty_side,
        "no_similarity_score": "deliberate -- see module docstring",
    }
    with open(os.path.join(OUTDIR, "_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    print(f"records: {len(records)}")
    print(f"crops:   {len(by_crop)}  families: {len(by_family)}")
    print(f"excluded (one side empty): {len(empty_side)}")
    print("by render status:", dict(by_status))
    print("by value type:", dict(by_type))
    print(f"written to {OUTDIR}")


if __name__ == "__main__":
    main()
