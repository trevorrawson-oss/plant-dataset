#!/usr/bin/env python3
"""build_spec -- Trevor's rulings of 2026-09-17 on the twelve woody crops whose plant dimensions stay null
(PLA-465 promote 2). Every text below is the recorded reason and routing; the promote appends one
open_findings entry per crop (two on pear-asian) and ONE dated addendum on plum's existing finding.
Usage: build_spec.py --write"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_SHA = "a7f234ce449c6d74b4f1be2398bb808cfe29bebf9a1f7cc51efdcaea56246c93"
SESSION = "pla465_2026-09-17"
R = "Trevor's ruling 2026-09-17"


def f(crop, fid, severity, status, summary, resolution_note, deferred_to):
    return {"crop": crop, "entry": {"id": fid, "severity": severity, "status": status, "blocks_launch": False,
                                    "filed_in_session": SESSION, "summary": summary,
                                    "resolution_note": resolution_note, "deferred_to": deferred_to}}


APPENDS = [
 f("mandarin-clementine", "mandarin_clementine_plant_dimensions_unusable_anchor_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1 (2026-09-16). No T1 page read states a clementine size in feet. The crop's cited UCR anchor (https://citrusvariety.ucr.edu/crc3178) is a SATSUMA page, the wrong scion; UCR's clementine accessions (e.g. crc0279 Algerian) describe the tree only as 'medium in vigor and size'. UF/IFAS HS1260 rates trifoliate orange 'Sm, less than 8 ft tall at maturity' as a Florida-commercial relative class for common scions, not a clementine measurement.",
   R + ": UNUSABLE SOURCE, null, no derivation attempted. The satsuma anchor is a record defect to repair separately.", None),
 f("orange-navel", "orange_navel_plant_dimensions_sources_conflict_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. The two candidate pages are an archived capture of a WAF-blocked UC Master Gardener page (Santa Clara 'Growing Great Citrus', 2025-10-10 capture: 'Navel -- Standard tree 20-25 feet high, dwarf 8 feet tall') and a retired UF/IFAS bulletin (HS982, read from an LSU-hosted copy: a sweet orange 'on standard or non-dwarfing commercial rootstocks will reach a 15 to 20-foot height'), and they disagree. The live UF/IFAS HS1260 rates Carrizo citrange 'Lg, perhaps 14-20 ft', a size class, not a measurement. No page states a navel spread.",
   R + ": UNUSABLE SOURCE, null, no derivation attempted. Two sources in conflict anchor neither figure.", None),
 f("grapefruit", "grapefruit_plant_dimensions_sources_conflict_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. The retired UF/IFAS HS982 (read from an LSU-hosted copy) gives 15 to 20 ft for grapefruit on standard rootstocks; the live UF/IFAS HS1260 rates Swingle citrumelo, the crop's recommended rootstock, 'I, 8 to 14 ft tall' (in-row spacing 8-12 ft), while LSU pub 1234 calls Swingle 'very vigorous'; the crop's own rootstock row carries 12-20. No page states a grapefruit spread.",
   R + ": UNUSABLE SOURCE, null, no derivation attempted. Two sources in conflict anchor neither figure.", None),
 f("apricot", "apricot_plant_dimensions_page_self_contradicts_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1 after the adversarial review struck the first staging's 20-40 by 20-40. The NC State Plant Toolbox page (https://plants.ces.ncsu.edu/plants/prunus-armeniaca/) contradicts itself: its Dimensions block says 'Height: 20 ft. 0 in. - 40 ft. 0 in. Width: 20 ft. 0 in. - 40 ft. 0 in.' and its prose says 'It is dense and can be 15 - 40 feet tall and wide.' Illinois Hort Answers gives 20-50 ft height only. The crop's own rootstock rows cap the standard tree at 15-20, 15-22 and 15-25 ft. A lead not read (WAF-blocked from the sandbox): the MSU 'Smart Gardening: backyard tree fruit' PDF, reported as 'Standard apricot trees are 15-25 feet tall by 20 feet wide'.",
   R + ": UNUSABLE SOURCE, null, no derivation attempted. A source that disagrees with itself cannot anchor either value.", None),
 f("cherry-sour", "cherry_sour_plant_dimensions_source_not_admitted_pla465", "low", "deferred",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. The only T1 page stating a tart cherry height in feet with Mahaleb, the crop's recommended rootstock, named on the same page as 'this standard rootstock for tart cherry' is Virginia Tech 422-018 (https://www.pubs.ext.vt.edu/422/422-018/422-018.html, read from raw bytes 2026-09-16, 155,925 bytes, sha256 0567e66ae2461dcd7372e6796be65f89d39761bceb2b180be8f24e6d0027af78): 'The tree is relatively small (15 feet to 20 feet tall), fairly spreading'; Mahaleb 'slightly dwarfing (20% smaller than mazzard)'. The source_catalog does not admit Virginia Tech. UMN (umn_ext, admitted) gives 'Tart cherry ... 8-15 feet' under a heading the page itself labels 'Mature height (estimate)', reflecting Minnesota's dwarf cultivars; it was not used.",
   R + ": NOT ADMITTED, null, routed to PLA-532, where Virginia Tech is already a candidate for the container and vertical publications. If admitted there, cherry-sour resolves from the recorded URL with no new reading. Whether a source-labelled estimate (UMN) is citable as such is unruled.", "PLA-532"),
 f("cherry-sweet", "cherry_sweet_plant_dimensions_derivation_declined_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. T1 gives Gisela 6, the crop's recommended rootstock, only as a percent of standard: PNW 619 (osu_ext, a cited anchor) Table 2 'Gisela 6' 80-85 percent of full size (60 percent in the eastern U.S., 90 in the Pacific Northwest); WSU treefruit 80-90 percent; UKY 70-90; VT 60-95; Purdue 50-60. Standard sweet cherry heights also vary by source (VT 30-40 ft; PNW 619 'upwards of 60 feet if left unpruned ... 10-20 feet if properly pruned'). The only feet figure tied to Gisela 6 is a managed height ('can easily be maintained at a height of only 8 feet'). The crop's rootstock row carries 15-20 ft, which no T1 page states in feet either (a Plan E item).",
   R + ": PERCENT-OF-STANDARD, null, derivation DECLINED. Multiplying a percent range by a standard-height range compounds two ranges into a number that reads as measured; unlike the bloom offsets, null is available here and is taken. Recorded as declined-derivation, not unread: a later pass must not 'fix' it by multiplying.", None),
 f("pear-european", "pear_european_plant_dimensions_derivation_declined_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. T1 gives OHxF 87, the crop's recommended rootstock, only as a percent of standard: WVU 'about 85-90% of standard'; USU 'OH x F ... 70-80% of the standard size'; UNH 'about 2/3'; UMN, series-level, 'tops out at about 20 feet tall' (a single figure). Standard pear heights vary by source (UMN 25-40; USU about 25; Oklahoma 16-24; UNH 15-18 maintained). The crop's rootstock row carries 12-16 ft, which no T1 page states in feet either (a Plan E item).",
   R + ": PERCENT-OF-STANDARD, null, derivation DECLINED, for the reason recorded on cherry-sweet. Recorded as declined-derivation, not unread.", None),
 f("raspberry", "raspberry_plant_dimensions_not_applicable_cane_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. Every T1 height read is a cane, tipping or trellis height: USU 'Primocanes can grow 4 to 8 feet the first year under ideal conditions' (summer-bearing, on a T-trellis); UGA C766 erect primocane-fruiting types 'grow to 3 to 4 feet tall'; UMN and OSU spring-prune canes to 4-5 ft and top to trellis height; extension publishes managed row widths (12-24 in) rather than a spread. Canes are biennial and managed; a mature height is not a property of the plant as grown.",
   R + ": NOT A PROPERTY OF THE PLANT, null, recorded as not-applicable-to-cane-fruit (the harvest-start-is-not-a-published-datum shape) so no later pass hunts for it. A per-field N/A predicate on cane_type for the A59 presence floor is owed so the null reads as N/A, not unread.", None),
 f("blackberry", "blackberry_plant_dimensions_not_applicable_cane_pla465", "low", "accepted",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. Every T1 figure read is a maintained ceiling: Clemson HGIC 'Erect varieties do not need support if the primocanes are pruned during the summer to keep the canes from growing more than 3 to 4 feet tall'; ACES erect plants 'maintained at about 3 feet tall'; OSU EC 1303 topped 'to a height of about 3 feet (erect) to 4.5 feet (semierect)'; trailing primocanes 'may grow more than 15 feet long'. No page states an unpruned mature height or a spread.",
   R + ": NOT A PROPERTY OF THE PLANT, null, recorded as not-applicable-to-cane-fruit, for the reason recorded on raspberry. The same A59 N/A predicate on cane_type is owed.", None),
 f("lime", "lime_single_value_shape_two_species_pla465", "low", "deferred",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. The same shape as plum_self_fertile_boolean_european_default on plum: one record, two species (Persian/Tahiti lime, Citrus x latifolia, and Key lime, C. x aurantiifolia; the record's varieties list leads Persian and its rootstock note discusses own-root Key), a single-value shape that breaks wherever they diverge. UF/IFAS CH093 gives Tahiti lime 'a height and spread of about 20 feet' (a single figure); CH092 gives Key lime 'rarely taller than 12 feet'; NC State gives C. x latifolia 8-20 by 8-20 and C. x aurantiifolia 6-13 by 5-15. The crop's cited anchors are one page per species.",
   R + ": TYPE-AWARE, null, attached to the plum shape rather than filed as an isolated gap; height is authored per type when the variety-delta pass builds the type-aware mechanism.", "PLA-12 variety-delta pass"),
 f("pear-asian", "pear_asian_plant_dimensions_basis_unstable_pla465", "low", "deferred",
   "mature_height_ft / mature_spread_ft left null at PLA-465 promote 1. Oklahoma HLA-6257 states 'Asian pears usually are about 8 to12 feet tall when fully mature' at species level, in its training section, with P. betulifolia as the rootstock context; no T1 page states an Asian pear size on OHxF 87, the record's recommended rootstock. Under R2 the crop-level figure is the recommended rootstock's size, and that rootstock is itself questioned (pear_asian_recommended_rootstock_questioned_pla465), so the basis is unstable regardless of height.",
   R + ": null until the recommended-rootstock finding resolves in PLA-463's Plan E; then read on the ruled basis.", "PLA-463 Plan E"),
 f("pear-asian", "pear_asian_recommended_rootstock_questioned_pla465", "medium", "deferred",
   "recommended_rootstock is 'OHxF 87'. WSU EB0937, Fruit Handbook for Western Washington (https://s3.wp.wsu.edu/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf, read from raw bytes 2026-09-16, 1,120,177 bytes, sha256 2ce35f98484a84bac1223a7e75b845167367c34cacbbcc884e83d7a9b15fe665): 'Asian pears -- OHXF series -- Asian pears need vigor so they should be grafted on the more vigorous clones such as OHXF 97 or OHXF 333.' Oklahoma HLA-6257 and WVU: 'Asian pears are commonly grafted to P. betulifolia'. The record's recommendation is steered against by the T1 read on the crop, and R2's meaning for the crop-level height depends on it.",
   R + ": filed on its own, separate from the height gap; routed to PLA-463's Plan E rootstock re-read alongside PLA-466's rootstock items. If the recommended rootstock changes, the crop-level height basis changes with it.", "PLA-463 Plan E"),
]
ADDENDUM = {"crop": "plum", "id": "plum_self_fertile_boolean_european_default",
            "original_summary": "crop-level self_fertile=true / needs_pollinizer=false defaults to the EUROPEAN case; the pollination prose + varieties table carry the full European-self / Japanese-needs-pollinizer split. A type-aware pollination flag is owed at the variety-delta pass so a consumer reading only the boolean is not misled for Japanese plums.",
            "suffix": " [ADDENDUM 2026-09-17, PLA-465: mature_height_ft / mature_spread_ft are the same problem on a second field. NC State gives Prunus domestica (European) 10-20 ft tall and wide and Prunus salicina (Japanese) 20-33 by 15-30 ft, non-overlapping, and the record lists 4 European to 3 Japanese varieties; the adversarial review struck a first staging that had picked the Japanese figure on list order. Both dimension keys left null at PLA-465 promote 1 (2026-09-16). Trevor's ruling 2026-09-17: attached here, not filed separately; one record, two types, a single-value shape that breaks wherever they diverge. When the variety-delta pass builds the type-aware mechanism, height comes with pollination.]"}


def main():
    spec = {"_what": "PLA-465 promote 2: the twelve woody crops whose plant dimensions stay null, each with Trevor's recorded reason and routing (2026-09-17). Twelve open_findings appended on eleven crops (two on pear-asian) and one dated addendum on plum's existing type-aware finding. No dimension value changes.",
            "base_sha": BASE_SHA, "session": SESSION, "appends": APPENDS, "addendum": ADDENDUM,
            "expected": {"appends": len(APPENDS), "crops": len({a["crop"] for a in APPENDS}) + 1, "addenda": 1}}
    if "--write" in sys.argv:
        json.dump(spec, open(os.path.join(HERE, "spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"spec.json written: {len(APPENDS)} appends on {spec['expected']['crops'] - 1} crops + 1 addendum")
    else:
        print(json.dumps(spec["expected"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
