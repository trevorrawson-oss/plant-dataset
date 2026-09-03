#!/usr/bin/env python3
"""ALLIUM RECORD CORRECTIONS, ROUND 3 -- the repoint round. Base 50ffedb0 (after r2).

Four decision families from docs/2026-09-02-pla8-batch24-source-triage.md, every document fetched
and read this session (~20 documents; a search summary counted for nothing). Where the triage's
verdict changed on reading, the change is stated.

1. ONION MAGGOT -- SIX crops, not four. Measured: garlic and spring-onion, both SHIPPED with ladders,
   carry the same two claims in their records and in FIVE shipped rung notes. The population was
   measured before the scope was accepted.
   * "populations carry over in allium residue" is the WRONG MECHANISM. Every document read says the
     pupae overwinter in the SOIL: UMN "Root maggots spend the winter as pupae in the soil"; UMass
     "These insects spends the winter as small brown pupae in the soil"; UC IPM "Mature larvae pupate
     in the soil". What sustains the fly between crops is cull piles and volunteers: UC IPM "Remove
     and dispose of onion culls and volunteer onions" and fields near cull piles "most likely harbor
     overwintering onion maggot pupae"; UMass "limit fly reproduction to the surface layers of the
     cull pile". UMN's end-of-season instruction is about the PLANTS: "Remove target plants in the
     fall, including their roots, and destroy them. This will kill any pupae that might be left."
   * The triage called the residue claim CONTRADICTED by UC IPM's "Thoroughly incorporate organic
     matter such as manure, crop residue ... well in advance of planting". On reading, that sentence
     sits under SEEDCORN maggot. What IS said about onion maggot and organic matter is attraction:
     UMN "Do not use animal manure or green manure in your garden in spring. Rotting and decaying
     organic matter attracts root maggots"; Clemson "Onion maggots are attracted to decomposing
     organic matter"; USU "avoid excessive amounts of organic matter". The records now say that.
   * "row cover at emergence" is sourced NOWHERE. UMN anchors it to fly activity ("by the time adult
     flies are laying eggs, usually early to mid-May", a Minnesota date); UMass to planting ("Place
     cover over the crop at the time of seeding or transplanting and seal the edges with soil").
     The records now say from planting, before the spring flight. The trap precondition (UMN "Do not
     place row covers if onions or other root vegetables were planted in the same area the previous
     year ... will trap adults that hatch from the pupae") is carried into every management register.
   * Delayed planting is supported (UMN "wait until June 1st"; UMass "Planting in late-May is more
     likely to be safer"; UC IPM "wait to plant until later in the spring, after the first generation
     of adult flies has emerged") and goes in as a hedge. UMN: "There are no insecticides available
     as a pre-plant treatment for cabbage and onion maggots in the home garden."
   * Anchors move off `growing-onions` / `growing-leeks` / `growing-garlic` / `growing-scallions`
     (one sentence, no management) to UMN root-maggots + UC IPM maggots. Leek keeps USU (rotation +
     organic matter); garlic keeps USU (not re-read, not this promote's claim); spring-onion keeps
     Clemson (read; attraction + sanitation).

2. PINK ROOT -- leek, onion, shallot. "clean, disease-free transplants/sets" is ABSENT AS A CONTROL
   in all eight documents read (UC IPM, USU x3, NMSU x2, PNW, UF/IFAS); it is the white-rot rule
   that migrated. It comes out. The rotation caveat goes in: UC IPM "Rotating to non-Allium crops for
   3 to 6 years can reduce the incidence"; PNW "reduces the severity of infection; however, the fungus
   still will invade some plants"; NMSU "Crop rotation is not highly effective ... the fungus survives
   on alternate hosts, and the microsclerotia have a long-term survival"; USU "Even though crop
   rotation does not have an effect on the disease, planting onion every five years can keep disease
   incidence low." Resistant varieties are the lead control on ONION (NMSU "The best control is
   varietal resistance"; USU "Talk to your local seed provider about varieties that may work in your
   area"), so onion gets that and shallot and leek do not: no document names a resistant shallot or
   leek, and absence is not asserted either. Mechanism and conditions go in from USU: "It can
   penetrate onion roots directly without the need for wounds and less vigorous plants are more
   susceptible"; "Optimum infection occurs at soil temperatures of 75 F to 85 F"; "higher in fields
   with heavy, poorly drained soils". LEEK SEVERITY medium -> low: UC IPM "Pink root is primarily a
   problem on onion" and the word "leek" appears in none of the seven US documents; the one that
   names it (UF/IFAS HS1388, "Leek is also susceptible to pink root rot") is kept as leek's citation
   for exactly that sentence. Onion and shallot move off the Texas A&M commercial PDF (one table row)
   to UC IPM + USU, cited as onion documents; shallot's prose says why that is honest (shallot is a
   form of the same species, A. cepa).

3. CHIVES RUST -- source add only. UC IPM's rust page supports the chives-susceptibility sentence
   ("In addition to garlic, onion and chives can be affected severely") and NONE of the crowding,
   nitrogen or leaf-wetting claims; the PNW handbook garlic-rust page supports all three verbatim:
   "Avoid dense plantings which favors disease." "Avoid over application of nitrogen, which enhances
   infections." "Avoid wetting of the leaves." Prose untouched. FILED, NOT FIXED: in-season removal
   of rusted leaves is absent from every rust document read; it stays as a chives cultural practice
   and is listed in the close-out.

4. CHIVES BOTRYTIS -- source and content only; the NAME does not move (PLA-448 s2, the rename waits
   for the naming pass) and neither does the batch-24 id `botrytis-leaf-blight-neck-rot`. Neither
   current anchor supports the entry: UMN growing-onions' entire disease text is one sentence naming
   "Botrytis neck rot", USU's is a neck-rot storage note. Repointed to UC IPM's leaf blight page
   (live at `/botrytis-leafspot/`) + PNW onion Botrytis leaf blight. Three claims corrected: spores
   are AIRBORNE, not splash-spread ("Botrytis squamosa spores are airborne" UC IPM; "Wind disperses
   the spores" PNW); "gray fuzzy mold" is a NECK ROT symptom absent from every leaf-blight page and
   comes out; in-season removal of senescing leaves is absent everywhere and becomes end-of-season
   sanitation ("Get rid of cull piles and debris, two overwintering sources" PNW). The conditions go
   in: "wet from dew or rain for long periods (20 or more hours)"; "Poor air circulation in the onion
   canopy also favors the disease. This may occur when onions are planted too closely together". The
   phrase "dense canopies" SURVIVES in cause_seasoned because batch 24's scope pin anchors on it.

SCOPE: 42 prose fields, 7 shipped rung notes, 1 severity, 11 source sets, across 11 problems on 6
crops. No rung added or removed, no id, no name, no type, no catalog. Rung edits are VALUE changes at
existing paths, so the path-keyed snapshot is exact.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "50ffedb00d680576d413a73e1ec7c2bcb1fd07db66bf9c09c017dce148a035f8"
VERIFIED = "2026-09-03"

MAGGOT = "Onion maggot"
PINK = "Pink root"
TARGETS = (
    ("chives", MAGGOT), ("leek", MAGGOT), ("onion", MAGGOT), ("shallot", MAGGOT),
    ("garlic", MAGGOT), ("spring-onion", MAGGOT),
    ("leek", PINK), ("onion", PINK), ("shallot", PINK),
    ("chives", "Rust"), ("chives", "Botrytis (leaf blight and neck rot)"),
)
SHIPPED = (("garlic", MAGGOT), ("spring-onion", MAGGOT))

UMN_MAGGOT = "https://extension.umn.edu/yard-and-garden-insects/root-maggots"
UC_MAGGOT = "https://ipm.ucanr.edu/agriculture/onion-and-garlic/maggots/"
UC_PINK = "https://ipm.ucanr.edu/agriculture/onion-and-garlic/pink-root/"
USU_PINK = "https://extension.usu.edu/planthealth/research/pink-root-onion"

PROSE = {
 # ---------------------------------------------------------------- onion maggot: chives
 ("chives", MAGGOT, "cause_seasoned"): (
  "Delia antiqua overwinters as pupae in the soil; spring flies lay eggs at plant bases and "
  "successive generations attack roots and bulbs, favored by cool wet weather and by cull and debris "
  "that lure egg-laying.",
  "Delia antiqua overwinters as pupae in the soil around last season's alliums; spring flies lay "
  "eggs at plant bases and successive generations attack roots and bulbs, favored by cool, wet "
  "weather and drawn to rotting organic matter, fresh manure and cull piles."),
 ("chives", MAGGOT, "organic_treatment_beginner"): (
  "There is no rescue for a maggot-riddled crown, so remove badly affected plants. Use row cover to "
  "keep the flies off, and clean up debris and culls that attract them.",
  "There is no home-garden spray for maggots already inside a plant, so pull badly affected plants, "
  "roots and all, and get rid of them. Keep the flies off with row cover put on at planting, and do "
  "not leave old bulbs or culls lying around, since rotting onion material draws the fly."),
 ("chives", MAGGOT, "organic_treatment_seasoned"): (
  "Remove and destroy infested plants, exclude flies with floating row cover, and sanitize debris "
  "and culls; rotation and avoiding dense allium plantings limit buildup. No effective organic "
  "rescue exists once larvae are in the crown.",
  "Remove and destroy infested plants with their roots, exclude the flies with row cover sealed at "
  "the edges from planting, and clear culls and volunteer alliums, which sustain the population "
  "between crops. Rotate off last year's allium ground and keep new plantings away from it, since "
  "the pupae overwinter in the soil there. No home-garden insecticide is available for maggots once "
  "larvae are in the crown."),
 ("chives", MAGGOT, "prevention_beginner"): (
  "Cover plants with row cover in spring, avoid leaving old bulbs and debris around, and do not "
  "crowd alliums together.",
  "Put row cover on at planting, before the flies are out, but not over ground that grew onions or "
  "their relatives last year, or you trap the emerging flies under it. Clear away old bulbs and "
  "culls, keep fresh manure out of the bed in spring, and give chives a spot away from last year's "
  "onion beds."),
 ("chives", MAGGOT, "prevention_seasoned"): (
  "Row-cover early, sanitize allium residue, rotate, and avoid clustering chives with other alliums "
  "that concentrate the fly.",
  "Cover from planting on ground that did not carry alliums last year, remove lifted plants and "
  "culls in fall to take the pupae out with them, hold spring manure and green manure out of the "
  "bed, and rotate: the flies emerge from the soil where alliums grew last season."),
 # ---------------------------------------------------------------- onion maggot: leek
 ("leek", MAGGOT, "cause_seasoned"): (
  "Larvae of the onion maggot fly (Delia antiqua), whose eggs are laid at the plant base; "
  "populations carry over in allium residue left in the ground.",
  "Larvae of the onion maggot fly (Delia antiqua), which lays at the base of the plant; the pupae "
  "overwinter in the soil around last season's alliums, and cull piles and volunteer onions keep the "
  "fly going between crops. Rotting organic matter and spring manure draw egg-laying, and cool, wet "
  "springs favor the maggots."),
 ("leek", MAGGOT, "cause_beginner"): (
  "The larvae (maggots) of a small fly that lays eggs at the base of the plant. They survive in "
  "leftover allium debris.",
  "The larvae (maggots) of a small fly that lays its eggs at the base of the plant. It spends the "
  "winter in the soil where onions or leeks grew the year before, and old bulbs and rotting garden "
  "waste draw it in."),
 ("leek", MAGGOT, "management_seasoned"): (
  "Rotate away from alliums, remove cull plants and crop residue, and use floating row cover at "
  "establishment to block egg-laying.",
  "Rotate off ground that carried alliums last season and site new plantings away from it, remove "
  "culls and lifted plants with their roots in fall, keep spring manure and green manure out of the "
  "bed, and cover transplants with row cover sealed at the edges from planting day, before the "
  "spring flight, on ground that did not carry alliums last year. Planting later in spring, once the "
  "first flight has passed, also sidesteps the worst of it."),
 ("leek", MAGGOT, "management_beginner"): (
  "Do not plant leeks where alliums grew recently, clean up old plant debris, and cover young plants "
  "with row-cover fabric so the fly cannot lay eggs on them.",
  "Do not plant leeks where onions or their relatives grew last year, clear out old bulbs and pulled "
  "plants rather than leaving them in the bed, keep fresh manure out of the bed in spring, and cover "
  "the young plants with row-cover fabric from planting day so the fly cannot lay eggs on them. Do "
  "not cover a bed that grew alliums last year, or you seal the emerging flies in with the crop."),
 # ---------------------------------------------------------------- onion maggot: onion
 ("onion", MAGGOT, "cause_seasoned"): (
  "Larvae of the onion maggot fly (Delia antiqua), whose eggs are laid at the plant base; "
  "populations carry over in allium residue.",
  "Larvae of the onion maggot fly (Delia antiqua), which lays at the base of the plant; the pupae "
  "overwinter in the soil around last season's onions, and cull piles and volunteer onions keep the "
  "fly going between crops. Rotting organic matter and spring manure draw egg-laying, and the first "
  "flight arrives with the cool, wet weather of mid-spring."),
 ("onion", MAGGOT, "cause_beginner"): (
  "The larvae (maggots) of a small fly that lays eggs at the base of onion plants. They survive in "
  "leftover onion debris.",
  "The larvae (maggots) of a small fly that lays its eggs at the base of onion plants. It spends the "
  "winter in the soil where onions grew the year before, and old bulbs and rotting garden waste draw "
  "it in."),
 ("onion", MAGGOT, "management_seasoned"): (
  "Rotate away from alliums, remove cull bulbs and crop residue, and use floating row cover at "
  "emergence to block egg-laying.",
  "Rotate off ground that carried alliums last season and site new plantings away from it and from "
  "any cull pile, remove culls and volunteer onions, keep spring manure and green manure out of the "
  "bed, and cover seedlings or sets with row cover sealed at the edges from planting, before the "
  "spring flight, on ground that did not carry alliums last year. Delaying planting until the first "
  "flight has passed reduces damage where the season allows."),
 ("onion", MAGGOT, "management_beginner"): (
  "Do not plant onions in the same place each year, clean up old onion scraps, and cover young "
  "plants with row-cover fabric so the fly cannot lay eggs on them.",
  "Do not plant onions where onions or their relatives grew last year, clear out old bulbs and any "
  "onion volunteers, keep fresh manure out of the bed in spring, and cover the young plants with "
  "row-cover fabric from planting day so the fly cannot lay eggs on them. Do not cover a bed that "
  "grew alliums last year, or you seal the emerging flies in with the crop."),
 # ---------------------------------------------------------------- onion maggot: shallot
 ("shallot", MAGGOT, "cause_seasoned"): (
  "Larvae of the onion maggot fly (Delia antiqua), whose eggs are laid at the plant base; "
  "populations carry over in allium residue.",
  "Larvae of the onion maggot fly (Delia antiqua), which lays at the base of the plant; the pupae "
  "overwinter in the soil around last season's shallots or onions, and cull piles and volunteer "
  "onions keep the fly going between crops. Rotting organic matter and spring manure draw "
  "egg-laying, and cool, wet springs favor the maggots."),
 ("shallot", MAGGOT, "cause_beginner"): (
  "The larvae (maggots) of a small fly that lays eggs at the base of allium plants. They survive in "
  "leftover onion and shallot debris.",
  "The larvae (maggots) of a small fly that lays its eggs at the base of onion-family plants. It "
  "spends the winter in the soil where onions or shallots grew the year before, and old bulbs and "
  "rotting garden waste draw it in."),
 ("shallot", MAGGOT, "management_seasoned"): (
  "Rotate away from alliums, remove cull bulbs and crop residue, and use floating row cover at "
  "emergence to block egg-laying.",
  "Rotate off ground that carried alliums last season and site new plantings away from it, remove "
  "culls and volunteer alliums, keep spring manure and green manure out of the bed, and cover the "
  "sets with row cover sealed at the edges from planting, before the spring flight, on ground that "
  "did not carry alliums last year. Where the season allows, planting after the first flight has "
  "passed reduces damage."),
 ("shallot", MAGGOT, "management_beginner"): (
  "Do not plant shallots in the same place each year, clean up old allium scraps, and cover young "
  "plants with row-cover fabric so the fly cannot lay eggs on them.",
  "Do not plant shallots where onions or their relatives grew last year, clear out old bulbs and any "
  "volunteers, keep fresh manure out of the bed in spring, and cover the young plants with row-cover "
  "fabric from planting day so the fly cannot lay eggs on them. Do not cover a bed that grew alliums "
  "last year, or you seal the emerging flies in with the crop."),
 # ---------------------------------------------------------------- onion maggot: garlic (SHIPPED)
 ("garlic", MAGGOT, "identification_seasoned"): (
  "Wilting, yellowing plants and rotting bulbs riddled by small white larvae; stand loss is worst in "
  "cool, wet conditions and where allium debris carries the pest over.",
  "Wilting, yellowing plants and rotting bulbs riddled by small white larvae; damage is worst in "
  "cool, wet conditions and on ground that carried alliums the year before."),
 ("garlic", MAGGOT, "cause_seasoned"): (
  "Larvae of the onion maggot fly (Delia antiqua), whose eggs are laid at the plant base; "
  "populations carry over in allium residue and cull bulbs.",
  "Larvae of the onion maggot fly (Delia antiqua), which lays at the base of the plant; the pupae "
  "overwinter in the soil around last season's alliums, and cull bulbs and volunteer onions keep the "
  "fly going between crops. Rotting organic matter and spring manure draw egg-laying. Garlic is "
  "generally a lesser host than onion."),
 ("garlic", MAGGOT, "cause_beginner"): (
  "The larvae (maggots) of a small fly that lays eggs at the base of the plants. They survive in "
  "leftover onion and garlic debris.",
  "The larvae (maggots) of a small fly that lays its eggs at the base of the plants. It spends the "
  "winter in the soil where onions or garlic grew the year before, and old bulbs and rotting garden "
  "waste draw it in. Garlic usually gets off lighter than onions."),
 ("garlic", MAGGOT, "management_seasoned"): (
  "Rotate away from alliums, remove cull bulbs and crop residue, and avoid planting into fresh "
  "manure; cultural sanitation is the main home-garden tool.",
  "Rotate off ground that carried alliums last season, remove cull bulbs and volunteer alliums, and "
  "keep fresh manure and green manure out of the bed; no home-garden insecticide is available for "
  "this pest, so bed choice and sanitation are the tools."),
 # ---------------------------------------------------------------- onion maggot: spring-onion (SHIPPED)
 ("spring-onion", MAGGOT, "cause_seasoned"): (
  "Larvae of the onion maggot fly (Delia antiqua), whose eggs are laid at the plant base; "
  "populations carry over in allium residue.",
  "Larvae of the onion maggot fly (Delia antiqua), which lays at the base of the plant; the pupae "
  "overwinter in the soil around last season's alliums, and cull piles and volunteer onions keep the "
  "fly going between crops. Rotting organic matter draws egg-laying, and cool, wet springs favor the "
  "maggots."),
 ("spring-onion", MAGGOT, "cause_beginner"): (
  "The larvae (maggots) of a small fly that lays eggs at the base of the plants. They survive in "
  "leftover onion debris.",
  "The larvae (maggots) of a small fly that lays its eggs at the base of the plants. It spends the "
  "winter in the soil where onions grew the year before, and old bulbs and rotting garden waste draw "
  "it in."),
 ("spring-onion", MAGGOT, "management_seasoned"): (
  "Rotate away from alliums, remove crop residue, and use floating row cover at emergence to block "
  "egg-laying.",
  "Rotate off ground that carried alliums last season, remove culls, volunteer onions and lifted "
  "plants, keep spring manure out of the bed, and cover the sowing with row cover sealed at the "
  "edges from seeding, before the spring flight, on ground that did not carry alliums last year."),
 # ---------------------------------------------------------------- pink root: leek
 ("leek", PINK, "cause_seasoned"): (
  "A soilborne fungus that builds up in continuous allium ground and is favored by warm soil; "
  "stressed plants show it worst.",
  "A soilborne fungus (Setophoma terrestris, long known as Phoma terrestris) that infects roots "
  "directly, builds up with every allium crop on the same ground, and is most active at soil "
  "temperatures of 75 to 85°F; weak or stressed plants are the most susceptible. It is mainly an "
  "onion disease, and leek is a lesser host."),
 ("leek", PINK, "cause_beginner"): (
  "A soil fungus that builds up when onions and their relatives are grown in the same ground year "
  "after year, especially in warm soil.",
  "A soil fungus that builds up when onions and their relatives are grown in the same ground year "
  "after year, especially in warm soil. It is mostly an onion problem, and leeks usually get off "
  "lighter."),
 ("leek", PINK, "management_seasoned"): (
  "Rotate away from alliums for several years, start with clean transplants, and keep plants "
  "unstressed and evenly watered.",
  "Rotate off allium ground for three to six years, knowing that rotation reduces the disease rather "
  "than clearing it, since the fungus persists in soil for years and lives on other crops; keep "
  "plants vigorous with steady water and fertility, since weak roots are the ones it takes, and use "
  "raised or well-drained beds where soil sits wet."),
 ("leek", PINK, "management_beginner"): (
  "Rotate where you plant leeks, start with clean healthy transplants, and keep the plants well "
  "cared for so they are not stressed.",
  "Give leeks a bed that has not grown onions or their relatives for several years, keep them "
  "growing steadily with regular water and feeding so their roots stay strong, and improve drainage "
  "where the soil stays wet. Rotation helps but does not clear the fungus, which lasts in the soil "
  "for years."),
 # ---------------------------------------------------------------- pink root: onion
 ("onion", PINK, "cause_seasoned"): (
  "A soilborne fungus (Setophoma terrestris) that builds in continuous allium ground; stressed "
  "plants show it worst.",
  "A soilborne fungus (Setophoma terrestris, long known as Phoma terrestris) that penetrates onion "
  "roots directly without a wound, builds up with every onion crop on the same ground, and is most "
  "active at soil temperatures of 75 to 85°F; weak or stressed plants are the most susceptible, and "
  "heavy, poorly drained soil makes it worse."),
 ("onion", PINK, "management_seasoned"): (
  "Rotate away from alliums for several years, start with clean, disease-free transplants, and keep "
  "plants unstressed.",
  "Resistant varieties are the best control, so ask your seed supplier which ones hold up locally, "
  "since resistance varies with the strain. Rotate off allium ground for three to six years, "
  "understanding that rotation reduces the disease rather than clearing it, because the fungus "
  "persists in soil for years. Keep plants vigorous with steady water and fertility, and improve "
  "drainage on heavy ground."),
 ("onion", PINK, "management_beginner"): (
  "Rotate where you plant onions, start with clean, healthy transplants, and keep the plants well "
  "cared for so they are not stressed.",
  "Choose a variety sold as resistant to pink root if you can, and ask your seed supplier which ones "
  "do well in your area. Give onions a bed that has not grown onions or their relatives for several "
  "years, keep them watered and fed so the roots stay strong, and improve drainage where the soil "
  "stays wet. Rotation helps but does not clear the fungus, which lasts in the soil for years."),
 # ---------------------------------------------------------------- pink root: shallot
 ("shallot", PINK, "cause_seasoned"): (
  "A soilborne fungus (Setophoma terrestris) that builds in continuous allium ground; stressed "
  "plants show it worst.",
  "A soilborne fungus (Setophoma terrestris, long known as Phoma terrestris) that penetrates the "
  "roots directly without a wound and builds up with every onion-family crop on the same ground; it "
  "is most active at soil temperatures of 75 to 85°F, and weak or stressed plants in heavy, wet soil "
  "are the most susceptible. Shallots are a form of the same species as onion and get it the same "
  "way."),
 ("shallot", PINK, "management_seasoned"): (
  "Rotate away from alliums for several years, start with clean, disease-free sets, and keep plants "
  "unstressed.",
  "Rotate off allium ground for three to six years, understanding that rotation reduces the disease "
  "rather than clearing it, because the fungus persists in soil for years. Keep plants vigorous with "
  "steady water and fertility, since weak roots are the ones it takes, and improve drainage on heavy "
  "ground."),
 ("shallot", PINK, "management_beginner"): (
  "Rotate where you plant shallots, start with clean, healthy sets, and keep the plants well cared "
  "for so they are not stressed.",
  "Give shallots a bed that has not grown onions or their relatives for several years, keep them "
  "watered and fed so the roots stay strong, and improve drainage where the soil stays wet. Rotation "
  "helps but does not clear the fungus, which lasts in the soil for years."),
 # ---------------------------------------------------------------- chives botrytis
 ("chives", "Botrytis (leaf blight and neck rot)", "symptoms_beginner"): (
  "Small whitish sunken spots on the leaves in cool, wet weather that can run together and brown out "
  "the tops, sometimes with a gray fuzzy mold. It is worst in humid, crowded plantings.",
  "Small whitish sunken spots on the leaves in cool, wet weather, often with a pale green halo, that "
  "can run together and brown out the leaf tips. It is worst where the leaves stay wet for a long "
  "time and in crowded plantings."),
 ("chives", "Botrytis (leaf blight and neck rot)", "symptoms_seasoned"): (
  "Botrytis leaf blight and neck rot (Botrytis species) producing small white sunken leaf spots that "
  "coalesce into blast and tip dieback under cool, moist conditions, sometimes with gray sporulation; "
  "humid, crowded stands favor it, and it affects chives among the alliums.",
  "Botrytis leaf blight (Botrytis squamosa): small white sunken oval spots, 0.06 to 0.25 inch, often "
  "with a light green halo, that coalesce into tip dieback and blighted leaves under cool, moist "
  "conditions. Leaves need 20 or more hours of wetness for spots to form, and poor air circulation in "
  "a crowded stand favors it. It is documented on onion, and chives are a related host."),
 ("chives", "Botrytis (leaf blight and neck rot)", "cause_beginner"): (
  "Botrytis is a gray-mold fungus of the onion family that spots and blights the leaves in cool, "
  "damp, crowded conditions.",
  "Botrytis leaf blight is a fungus of the onion family that spots and blights the leaves when they "
  "stay wet for most of a day in cool weather, and crowded, still plantings hold that wetness "
  "longest."),
 ("chives", "Botrytis (leaf blight and neck rot)", "cause_seasoned"): (
  "Botrytis fungi favored by cool, wet, humid weather and dense canopies; splashing water and leaf "
  "wetness spread the spores.",
  "Botrytis squamosa, favored by cool, wet weather and dense canopies; its spores are airborne, and "
  "they infect only where leaf wetness lasts 20 hours or more. It overwinters as sclerotia on "
  "infected leaves, culls and debris, which persist in the soil for months to years."),
 ("chives", "Botrytis (leaf blight and neck rot)", "organic_treatment_beginner"): (
  "Remove spotted leaves or shear the clump to regrow, open up crowded plantings for airflow, and "
  "water at the base instead of over the leaves.",
  "Cut the clump back hard and clear the cut leaves away so it regrows clean, open up crowded "
  "plantings for airflow, and water at the base instead of over the leaves so the foliage dries "
  "between waterings."),
 ("chives", "Botrytis (leaf blight and neck rot)", "organic_treatment_seasoned"): (
  "Cull spotted foliage or shear the clump to regrow, divide to open the stand, irrigate at the soil "
  "line, and remove senescing debris. Fungicides are seldom needed on a home chive planting.",
  "Shear the clump and remove the cut foliage rather than leaving it in the bed, since sclerotia form "
  "on infected leaves; divide to open the stand so leaves dry, water at the soil line and time it so "
  "foliage dries before night, and clear dead foliage and debris at the end of the season. "
  "Fungicides are seldom warranted on a home chive planting."),
 ("chives", "Botrytis (leaf blight and neck rot)", "prevention_beginner"): (
  "Space and divide for airflow, water at the soil line, and clean up dead foliage.",
  "Space and divide for airflow, water at the soil line at a time of day that lets the leaves dry, "
  "and clear out dead foliage at the end of the season."),
 ("chives", "Botrytis (leaf blight and neck rot)", "prevention_seasoned"): (
  "Divide for airflow, water low and early, and sanitize dead foliage to cut inoculum.",
  "Divide for airflow, water at the base and time it for leaf drying, keep new plantings off ground "
  "that carried diseased alliums for three years, and clear dead foliage and culls at season's end, "
  "since the sclerotia overwinter in them."),
}
# (crop, problem name, method, field) -> (before, after). Shipped rung notes on garlic and
# spring-onion that carry the residue mechanism, the emergence timing, or the false-attribution
# device. Values only; no rung is added, removed or reordered.
RUNG_NOTES = {
 ("garlic", MAGGOT, "garden_sanitation", "note_seasoned"): (
  "Removing crop residue and cull bulbs takes away the material the population carries over in, and "
  "it is the primary home-garden lever for onion maggot. Get what you clear out of the garden rather "
  "than piling it at the bed edge, where the same tissue still counts as carryover.",
  "Removing cull bulbs, volunteer onions and lifted plants with their roots takes away what the fly "
  "breeds in and what the pupae overwinter around, and with no home-garden insecticide available it "
  "is the main lever there is. Get what you clear right out of the garden rather than piling it at "
  "the bed edge, since a cull pile is where the fly multiplies."),
 ("spring-onion", MAGGOT, "crop_rotation", "note_beginner"): (
  "Do not put alliums back into the same bed year after year. The problem carries over in old onion "
  "material left behind in the ground, so moving the planting keeps a new crop away from it.",
  "Do not put alliums back into the same bed year after year. The fly spends the winter in the soil "
  "where onions grew, so moving the planting keeps a new crop away from where it will come up in "
  "spring."),
 ("spring-onion", MAGGOT, "crop_rotation", "note_seasoned"): (
  "Populations carry over in allium residue from one crop to the next, so shifting the planting off "
  "last year's allium ground is the foundation the other two rungs sit on.",
  "The pupae overwinter in the soil around last season's alliums, so shifting the planting off that "
  "ground, and away from any cull pile, is the foundation the rest of the program sits on."),
 ("spring-onion", MAGGOT, "garden_sanitation", "note_beginner"): (
  "Clear out old onion tops, roots and trimmings once a bed is finished, and take them away rather "
  "than leaving them lying around. That leftover material is what carries the problem into the next "
  "season.",
  "Clear out old onion plants, roots and all, plus any small or damaged bulbs you did not use, once a "
  "bed is finished, and take them away rather than leaving them lying around. Old onion material is "
  "what the fly breeds in, and pulling the plants with their roots takes the pupae out with them."),
 ("spring-onion", MAGGOT, "garden_sanitation", "note_seasoned"): (
  "Residue is the carryover reservoir the guidance names, so strip the bed of allium culls, tops and "
  "root plates at the end of the crop and remove them from the ground rather than leaving them in "
  "place.",
  "Culls, volunteer onions and plants left standing are what the fly breeds in and overwinters "
  "around, so pull the finished crop with its roots, clear culls and volunteers, and take them out of "
  "the garden rather than leaving them in place. Keep fresh manure and green manure out of the bed in "
  "spring, since rotting organic matter draws the flies to lay."),
 ("spring-onion", MAGGOT, "floating_row_cover", "note_beginner"): (
  "Lay a floating row cover, a light fabric that lets in light and water while keeping insects out, "
  "over the bed as the seedlings come up. The fly has to reach the base of a plant to lay its eggs, "
  "so a sealed cover shuts that out. Do not use a cover on a bed where alliums grew last year, or you "
  "can seal the emerging flies in with the crop.",
  "Lay a floating row cover, a light fabric that lets in light and water while keeping insects out, "
  "over the bed as soon as you sow, so it is in place before the flies are out. The fly has to reach "
  "the base of a plant to lay its eggs, so a sealed cover shuts that out. Do not use a cover on a bed "
  "where alliums grew last year, or you can seal the emerging flies in with the crop."),
 ("spring-onion", MAGGOT, "floating_row_cover", "note_seasoned"): (
  "Cover at emergence, which is the window the guidance points at, and seal the edges: eggs go in at "
  "the plant base, so the barrier counts only if the fly cannot get underneath it. Pair it with the "
  "rotation rung, since covering ground that carried alliums last season can trap what comes up out "
  "of it under the net with the crop.",
  "Cover from sowing, before the spring flight is laying, and seal the edges: eggs go in at the plant "
  "base, so the barrier counts only if the fly cannot get underneath it. It belongs on rotated "
  "ground, since covering a bed that carried alliums last season traps the flies emerging from the "
  "soil under the net with the crop."),
}
SEVERITY = {("leek", PINK): ("medium", "low")}
SOURCES = {
 ("chives", MAGGOT): (["umn_ext"], ["umn_ext", "uc_ipm"],
                      {"umn_ext": UMN_MAGGOT, "uc_ipm": UC_MAGGOT}),
 ("leek", MAGGOT): (["usu_ext", "umn_ext"], ["usu_ext", "umn_ext", "uc_ipm"],
                    {"usu_ext": "https://extension.usu.edu/yardandgarden/research/leeks-in-the-garden",
                     "umn_ext": UMN_MAGGOT, "uc_ipm": UC_MAGGOT}),
 ("onion", MAGGOT): (["umn_ext"], ["umn_ext", "uc_ipm"],
                     {"umn_ext": UMN_MAGGOT, "uc_ipm": UC_MAGGOT}),
 ("shallot", MAGGOT): (["umn_ext"], ["umn_ext", "uc_ipm"],
                       {"umn_ext": UMN_MAGGOT, "uc_ipm": UC_MAGGOT}),
 # garlic keeps usu_ext's existing anchor untouched: not re-read this session, not this promote's claim.
 ("garlic", MAGGOT): (["usu_ext", "umn_ext"], ["usu_ext", "umn_ext", "uc_ipm"],
                      {"umn_ext": UMN_MAGGOT, "uc_ipm": UC_MAGGOT}),
 ("spring-onion", MAGGOT): (["umn_ext", "clemson_hgic"], ["umn_ext", "clemson_hgic", "uc_ipm"],
                            {"umn_ext": UMN_MAGGOT,
                             "clemson_hgic": "https://hgic.clemson.edu/factsheet/onion-leek-shallot-garlic/",
                             "uc_ipm": UC_MAGGOT}),
 ("leek", PINK): (["uf_ifas"], ["uc_ipm", "usu_ext", "uf_ifas"],
                  {"uc_ipm": UC_PINK, "usu_ext": USU_PINK,
                   "uf_ifas": "https://ask.ifas.ufl.edu/publication/HS1388"}),
 ("onion", PINK): (["tamu_agrilife"], ["uc_ipm", "usu_ext"],
                   {"uc_ipm": UC_PINK, "usu_ext": USU_PINK}),
 ("shallot", PINK): (["tamu_agrilife"], ["uc_ipm", "usu_ext"],
                     {"uc_ipm": UC_PINK, "usu_ext": USU_PINK}),
 ("chives", "Rust"): (["uc_ipm"], ["uc_ipm", "osu_ext"],
                      {"uc_ipm": "https://ipm.ucanr.edu/agriculture/onion-and-garlic/rust/",
                       "osu_ext": "https://pnwhandbooks.org/plantdisease/host-disease/garlic-allium-sativum-rust"}),
 ("chives", "Botrytis (leaf blight and neck rot)"): (
     ["umn_ext", "usu_ext"], ["uc_ipm", "osu_ext"],
     {"uc_ipm": "https://ipm.ucanr.edu/agriculture/onion-and-garlic/botrytis-leafspot/",
      "osu_ext": "https://pnwhandbooks.org/plantdisease/host-disease/onion-allium-cepa-botrytis-leaf-blight"}),
}
# 24 maggot (chives 5, leek 4, onion 4, shallot 4, garlic 4, spring-onion 3) + 10 pink root (leek 4,
# onion 3, shallot 3) + 8 botrytis. The first draft asserted 35 from a head count and the table
# refused it: the table is the count, the docstring is not.
EXPECTED_PROSE = 42
EXPECTED_RUNG_NOTES = 7
EXPECTED_SEVERITY = 1
EXPECTED_SOURCE_SETS = 11
# Anchor URLs that must survive on NO target afterward: the one-sentence crop pages and the
# commercial PDF the repoints move off.
RETIRED_URLS = (
    "extension.umn.edu/vegetables/growing-onions", "extension.umn.edu/vegetables/growing-leeks",
    "extension.umn.edu/vegetables/growing-garlic",
    "extension.umn.edu/vegetables/growing-scallions-home-gardens",
    "aggie-horticulture.tamu.edu/vegetable/files/2011/10/onion1.pdf",
)

_MAGGOT_TARGETS = tuple(t for t in TARGETS if t[1] == MAGGOT)
_PINK_TARGETS = tuple(t for t in TARGETS if t[1] == PINK)
_BOT = ("chives", "Botrytis (leaf blight and neck rot)")

# Claims that must be GONE afterward, scanned over the WHOLE problem including its rung notes.
RETIRED = tuple(
 [(t, lambda s: bool(re.search(r"\bresidues?\b", s, re.I)), "the residue carryover mechanism")
  for t in _MAGGOT_TARGETS] +
 [(t, lambda s: bool(re.search(r"\bat (?:emergence|establishment)\b", s, re.I)),
   "the unsourced emergence timing") for t in _MAGGOT_TARGETS] +
 # carr(?:y|ies): the first draft wrote `carries?`, which matches "carries" and "carrie" and NOT
 # "carry", so "populations carry over in allium residue" slipped past this predicate and was
 # caught only by the residue one. The suite's both-directions assertion found it. The object is
 # then REQUIRED to be residue/debris/material/scraps: garlic's shipped rotation note says the
 # population carries over "in allium GROUND", which is the CORRECT mechanism and must pass.
 [(t, lambda s: bool(re.search(r"debris carries the pest over|carr(?:y|ies) over in (?:allium|old|leftover) "
                                r"(?:\w+ )?(?:residue|debris|material|scraps)", s, re.I)),
   "the debris carryover mechanism") for t in _MAGGOT_TARGETS] +
 [(t, lambda s: bool(re.search(r"\bthe guidance\b|guidance (?:names|asks|points)", s, re.I)),
   "the false-attribution device") for t in _MAGGOT_TARGETS] +
 [(t, lambda s: bool(re.search(r"\bclean\b", s, re.I)), "the clean-stock claim") for t in _PINK_TARGETS] +
 [(_BOT, lambda s: bool(re.search(r"senesc", s, re.I)), "in-season senescing-leaf removal"),
  (_BOT, lambda s: bool(re.search(r"gray fuzzy mold|gray sporulation|gray-mold", s, re.I)),
   "the neck-rot gray-mold symptom"),
  (_BOT, lambda s: bool(re.search(r"splash", s, re.I)), "the splash-dispersal mechanism")]
)
# Claims that must be PRESENT afterward in every register named, and ABSENT there in the pre-state.
_TRAP = re.compile(r"do not cover a bed that grew (?:alliums|leeks or onions|onions or leeks) last year|"
                   r"not over ground that grew onions or their relatives last year|"
                   r"on ground that did not carry alliums last year", re.I)
REQUIRED = (
 [(t, ("management_seasoned", "management_beginner"), _TRAP, "the row-cover trap precondition")
  for t in (("leek", MAGGOT), ("onion", MAGGOT), ("shallot", MAGGOT))] +
 [(("chives", MAGGOT), ("prevention_seasoned", "prevention_beginner"), _TRAP,
   "the row-cover trap precondition")] +
 [(t, ("management_seasoned",), re.compile(r"before the spring flight"), "cover BEFORE the flight")
  for t in (("leek", MAGGOT), ("onion", MAGGOT), ("shallot", MAGGOT), ("spring-onion", MAGGOT))] +
 [(t, ("management_seasoned", "cause_seasoned"), re.compile(r"\bmanure\b|rotting organic matter", re.I),
   "the organic-matter attraction") for t in (("leek", MAGGOT), ("onion", MAGGOT), ("shallot", MAGGOT),
                                              ("spring-onion", MAGGOT))] +
 # garlic's management_seasoned ALREADY says "fresh manure" in the pre-state, so requiring it there
 # would be a restatement, not a measurement; only its cause register is required.
 [(("garlic", MAGGOT), ("cause_seasoned",), re.compile(r"\bmanure\b|rotting organic matter", re.I),
   "the organic-matter attraction")] +
 [(t, ("cause_seasoned",), re.compile(r"pupae overwinter in the soil"), "the soil overwintering mechanism")
  for t in (("leek", MAGGOT), ("onion", MAGGOT), ("shallot", MAGGOT), ("garlic", MAGGOT),
            ("spring-onion", MAGGOT))] +
 [(t, ("management_seasoned",), re.compile(r"three to six years"), "the rotation figure")
  for t in _PINK_TARGETS] +
 [(t, ("management_seasoned", "management_beginner"),
   re.compile(r"rotation (?:reduces the disease rather than clearing it|helps but does not clear)", re.I),
   "the rotation caveat") for t in _PINK_TARGETS] +
 # re.I: the seasoned register opens with "Resistant varieties are the best control" and a
 # case-sensitive pattern refused it. A guard that rejects correct input is a defect.
 [(("onion", PINK), ("management_seasoned", "management_beginner"), re.compile(r"resistant", re.I),
   "resistant varieties as the lead onion control")] +
 [(_BOT, ("symptoms_seasoned", "cause_seasoned"), re.compile(r"20 (?:or more hours|hours or more)"),
   "the 20-hour leaf-wetness figure"),
  (_BOT, ("cause_seasoned",), re.compile(r"airborne"), "the airborne mechanism")]
)
# Phrases downstream pins anchor on; they must survive.
SURVIVE = {
 _BOT: ("dense canopies",),                       # batch-24 ID_SCOPE_PINS own-side phrase
 ("chives", MAGGOT): ("Delia antiqua",),
 ("onion", PINK): ("Setophoma terrestris",),
}

BRITISH = (r"\bbin\b", r"colour", r"fortnight", r"whilst", r"\bautumn\b", r"mould", r"practise",
           r"favour", r"sulphur")
ABSOLUTES = ("always", "never", "completely", "totally", "harmless", "guaranteed", "eliminate",
             "eliminates")


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    return [p for f in ("pests", "diseases") for p in crop.get(f) or []]


def find_problem(data, slug, name):
    c = by_slug(data).get(slug)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % slug)
    hits = [p for p in problems(c) if p.get("name") == name]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %s has %d problems named %r, expected exactly 1"
                         % (slug, len(hits), name))
    return hits[0]


def find_rung(data, slug, name, method):
    lad = find_problem(data, slug, name).get("control_ladder") or []
    hits = [r for r in lad if r.get("method") == method]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %s/%s carries %d rungs for %r, expected exactly 1"
                         % (slug, name, len(hits), method))
    return hits[0]


def rung_count(data):
    return sum(len(p.get("control_ladder") or []) for c in data["crops"] for p in problems(c))


def snapshot(data):
    snap = {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + (str(k),))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + ("[%d]" % i,))
        else:
            snap[path] = node
    walk(data, ())
    return snap


def strings_of(p):
    """Every string on a problem INCLUDING its rung notes, tagged by where it sits."""
    out = [(k, v) for k, v in p.items() if isinstance(v, str)]
    for r in p.get("control_ladder") or []:
        for k in ("note_beginner", "note_seasoned"):
            if isinstance(r.get(k), str):
                out.append(("%s/%s" % (r.get("method"), k), r[k]))
    return out


def hygiene(s):
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    for w in ABSOLUTES:
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    for pat in BRITISH:
        if re.search(pat, s, re.I):
            bad.append("british:%s" % pat)
    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):
        bad.append("ladder vocabulary")
    if re.search(r"\d\s+°F", s):
        bad.append("spaced degF")
    if re.search(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)", s, re.I):
        bad.append("false-attribution device")
    return bad


# ------------------------------------------------------------------ guards
def check_pins(data):
    sizes = (len(PROSE), len(RUNG_NOTES), len(SEVERITY), len(SOURCES))
    want = (EXPECTED_PROSE, EXPECTED_RUNG_NOTES, EXPECTED_SEVERITY, EXPECTED_SOURCE_SETS)
    if sizes != want:
        raise SystemExit("REFUSED: edit tables hold %d/%d/%d/%d, expected %d/%d/%d/%d"
                         % (sizes + want))
    keys = [k[:2] for k in PROSE] + [k[:2] for k in RUNG_NOTES] + list(SEVERITY) + list(SOURCES)
    for key in keys:
        if key not in TARGETS:
            raise SystemExit("REFUSED: %s/%s is not a declared target" % key)
    for (slug, name, field), (before, after) in sorted(PROSE.items()):
        p = find_problem(data, slug, name)
        if p.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s does not match its pinned text; the record moved"
                             % (slug, name, field))
        if after == before:
            raise SystemExit("REFUSED: %s/%s/%s replacement is identical" % (slug, name, field))
        bad = hygiene(after)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s replacement: %s" % (slug, name, field,
                                                                    ", ".join(bad)))
    # SHAPE FIRST: a shipped target with no ladder must refuse HERE, before the rung-note pins
    # below try to find a rung on it and refuse for the narrower reason. An UNshipped target must
    # carry no ladder and no id: the batch-24 promote adds both, and this promote lands before it.
    for slug, name in TARGETS:
        p = find_problem(data, slug, name)
        if (slug, name) in SHIPPED:
            if not p.get("control_ladder") or not p.get("id"):
                raise SystemExit("REFUSED: %s/%s is declared shipped but carries no ladder or id"
                                 % (slug, name))
        elif p.get("control_ladder") is not None or p.get("id") is not None:
            raise SystemExit("REFUSED: %s/%s already carries a ladder or id; this promote must land "
                             "BEFORE batch 24" % (slug, name))
    for (slug, name, method, field), (before, after) in sorted(RUNG_NOTES.items()):
        if (slug, name) not in SHIPPED:
            raise SystemExit("REFUSED: %s/%s is not a shipped target; it has no rungs to edit"
                             % (slug, name))
        r = find_rung(data, slug, name, method)
        if r.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s/%s does not match its pinned note; the rung moved"
                             % (slug, name, method, field))
        if after == before:
            raise SystemExit("REFUSED: %s/%s/%s/%s replacement is identical"
                             % (slug, name, method, field))
        bad = hygiene(after)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s/%s replacement: %s"
                             % (slug, name, method, field, ", ".join(bad)))
    for (slug, name), (before, after) in sorted(SEVERITY.items()):
        got = find_problem(data, slug, name).get("severity")
        if got != before:
            raise SystemExit("REFUSED: %s/%s severity is %r, pinned %r" % (slug, name, got, before))
        if after not in ("low", "medium", "high"):
            raise SystemExit("REFUSED: %s/%s new severity %r is not a known value"
                             % (slug, name, after))
    for (slug, name), (before, after, anchors) in sorted(SOURCES.items()):
        p = find_problem(data, slug, name)
        if p.get("sources") != before:
            raise SystemExit("REFUSED: %s/%s sources are %r, pinned %r"
                             % (slug, name, p.get("sources"), before))
        if sorted(set(after)) != sorted(after) or not after:
            raise SystemExit("REFUSED: %s/%s new source list is empty or has duplicates"
                             % (slug, name))
        for sid in after:
            if sid not in data["source_catalog"]:
                raise SystemExit("REFUSED: %s/%s cites %r, which is not in source_catalog"
                                 % (slug, name, sid))
        for sid in anchors:
            if sid not in after:
                raise SystemExit("REFUSED: %s/%s anchors %r which is not in its new source list"
                                 % (slug, name, sid))
        # Every id must end up with a PATHED anchor: either given here or already carried.
        for sid in after:
            if sid not in anchors and sid not in (p.get("anchoring_urls") or {}):
                raise SystemExit("REFUSED: %s/%s cites %r without a document anchor"
                                 % (slug, name, sid))
    # Every declared target must receive at least one edit of some kind.
    for slug, name in TARGETS:
        if (slug, name) not in {k for k in keys}:
            raise SystemExit("REFUSED: %s/%s is declared but receives no edit" % (slug, name))


def check_retired_claims(data):
    left = []
    for (slug, name), still_present, label in RETIRED:
        p = find_problem(data, slug, name)
        for where, v in strings_of(p):
            if still_present(v):
                left.append("%s/%s/%s still carries %s" % (slug, name, where, label))
    if left:
        raise SystemExit("REFUSED: %r" % left)
    return len(RETIRED)


def check_required_claims(data):
    missing = []
    for (slug, name), fields, pat, label in REQUIRED:
        p = find_problem(data, slug, name)
        for f in fields:
            if not pat.search(p.get(f) or ""):
                missing.append("%s/%s/%s lacks %s" % (slug, name, f, label))
    if missing:
        raise SystemExit("REFUSED: %r" % missing)
    return sum(len(f) for _t, f, _p, _l in REQUIRED)


def check_survivors(data):
    for (slug, name), phrases in sorted(SURVIVE.items()):
        p = find_problem(data, slug, name)
        blob = " ".join(v for _w, v in strings_of(p))
        for ph in phrases:
            if ph not in blob:
                raise SystemExit("REFUSED: %s/%s no longer says %r" % (slug, name, ph))
    return sum(len(v) for v in SURVIVE.values())


def check_urls_retired(data):
    """The one-sentence crop pages and the commercial PDF must anchor NO target afterward. The
    `umn_ext` id survives on every maggot entry; it is the URL under it that moves."""
    left = []
    for slug, name in TARGETS:
        p = find_problem(data, slug, name)
        for sid, a in (p.get("anchoring_urls") or {}).items():
            url = (a or {}).get("url") or ""
            for bad in RETIRED_URLS:
                if bad in url:
                    left.append("%s/%s/%s -> %s" % (slug, name, sid, bad))
    if left:
        raise SystemExit("REFUSED: retired anchors survive: %r" % left)
    return len(RETIRED_URLS)


def check_maggot_anchors_uniform(data):
    """All six maggot entries must anchor `umn_ext` at the root-maggots page and `uc_ipm` at the
    maggots page: one insect, one pair of documents. A crop drifting to a different URL under the
    same id is the templated-record defect in the other direction."""
    n = 0
    for slug, name in _MAGGOT_TARGETS:
        au = find_problem(data, slug, name).get("anchoring_urls") or {}
        for sid, want in (("umn_ext", UMN_MAGGOT), ("uc_ipm", UC_MAGGOT)):
            got = (au.get(sid) or {}).get("url")
            if got != want:
                raise SystemExit("REFUSED: %s/%s anchors %s at %r, expected %r"
                                 % (slug, name, sid, got, want))
            n += 1
    return n


def apply_to(data):
    check_pins(data)
    for (slug, name, field), (_b, after) in PROSE.items():
        find_problem(data, slug, name)[field] = after
    for (slug, name, method, field), (_b, after) in RUNG_NOTES.items():
        find_rung(data, slug, name, method)[field] = after
    for (slug, name), (_b, after) in SEVERITY.items():
        find_problem(data, slug, name)["severity"] = after
    for (slug, name), (_b, after, anchors) in SOURCES.items():
        p = find_problem(data, slug, name)
        p["sources"] = list(after)
        au = {k: v for k, v in (p.get("anchoring_urls") or {}).items() if k in after}
        for sid, url in anchors.items():
            au[sid] = {"url": url, "verified": VERIFIED}
        p["anchoring_urls"] = {k: au[k] for k in after if k in au}
    return data


def verify_post(pre, data):
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    want_owners = set(TARGETS)

    def owner(k):
        if len(k) < 4 or k[0] != "crops" or k[2] not in ("pests", "diseases"):
            return None
        try:
            crop = data["crops"][int(k[1][1:-1])]
            return crop["slug"], crop[k[2]][int(k[3][1:-1])].get("name")
        except (ValueError, IndexError, KeyError):
            return None

    for k in added | dropped:
        if "anchoring_urls" not in k and "sources" not in k:
            raise SystemExit("REFUSED: a key was added or dropped outside sources/anchoring_urls: "
                             "%r" % (k,))
        if owner(k) not in want_owners:
            raise SystemExit("REFUSED: a key was added or dropped outside the declared targets: "
                             "%r" % (k,))
    changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
    # NOTHING on a TARGET may change except what this promote pins. A target's unpinned field
    # moving is invisible to the owner check (the owner IS a target) and to the counts (they count
    # only pinned fields), so every changed leaf under a target is matched to a pin directly.
    # r4's suite found this gap; it is closed here too.
    pinned = {}
    for slug, name, field in PROSE:
        pinned.setdefault((slug, name), set()).add(field)
    for slug, name in SEVERITY:
        pinned.setdefault((slug, name), set()).add("severity")
    rung_pins = {}
    for slug, name, method, field in RUNG_NOTES:
        rung_pins.setdefault((slug, name), set()).add((method, field))
    for k in changed:
        o = owner(k)
        if o not in want_owners:
            continue
        if "sources" in k or "anchoring_urls" in k:
            continue
        if "control_ladder" in k:
            crop = data["crops"][int(k[1][1:-1])]
            meth = crop[k[2]][int(k[3][1:-1])]["control_ladder"][int(k[5][1:-1])].get("method")
            if (meth, k[-1]) not in rung_pins.get(o, set()):
                raise SystemExit("REFUSED: %s/%s/%s/%s is not a pinned rung note of this promote"
                                 % (o[0], o[1], meth, k[-1]))
            continue
        if k[-1] not in pinned.get(o, set()):
            raise SystemExit("REFUSED: %s/%s/%s is not a pinned field of this promote"
                             % (o[0], o[1], k[-1]))
    prose_fields = {f for _s, _n, f in PROSE}
    n_prose = sum(1 for k in changed if "control_ladder" not in k and k[-1] in prose_fields)
    if n_prose != EXPECTED_PROSE:
        raise SystemExit("REFUSED: %d prose leaves changed, expected %d" % (n_prose, EXPECTED_PROSE))
    n_rung = sum(1 for k in changed if "control_ladder" in k)
    if n_rung != EXPECTED_RUNG_NOTES:
        raise SystemExit("REFUSED: %d rung leaves changed, expected %d" % (n_rung, EXPECTED_RUNG_NOTES))
    n_sev = sum(1 for k in changed if k[-1] == "severity")
    if n_sev != EXPECTED_SEVERITY:
        raise SystemExit("REFUSED: %d severity leaves changed, expected %d" % (n_sev, EXPECTED_SEVERITY))
    for (slug, name, field), (_b, after) in PROSE.items():
        if find_problem(data, slug, name).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s did not receive its replacement"
                             % (slug, name, field))
    for (slug, name, method, field), (_b, after) in RUNG_NOTES.items():
        if find_rung(data, slug, name, method).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s/%s did not receive its replacement"
                             % (slug, name, method, field))
    for (slug, name), (_b, after) in SEVERITY.items():
        if find_problem(data, slug, name).get("severity") != after:
            raise SystemExit("REFUSED: %s/%s severity was not set to %r" % (slug, name, after))
    for (slug, name), (_b, after, anchors) in SOURCES.items():
        p = find_problem(data, slug, name)
        if p.get("sources") != list(after):
            raise SystemExit("REFUSED: %s/%s sources are %r, expected %r"
                             % (slug, name, p.get("sources"), list(after)))
        if list(p.get("anchoring_urls") or {}) != list(after):
            raise SystemExit("REFUSED: %s/%s anchoring_urls keys %r do not match its sources %r"
                             % (slug, name, list(p.get("anchoring_urls") or {}), list(after)))
        for sid, url in anchors.items():
            if (p["anchoring_urls"].get(sid) or {}).get("url") != url:
                raise SystemExit("REFUSED: %s/%s anchor %s is %r, expected %r"
                                 % (slug, name, sid, p["anchoring_urls"].get(sid), url))
    touched = {owner(k) for k in changed}
    if touched - want_owners:
        raise SystemExit("REFUSED: leaves changed outside the declared targets: %r"
                         % sorted(touched - want_owners))
    # No shipped ladder may change SHAPE: same rung count, same method order, everywhere.
    if rung_count(data) != 3243:
        raise SystemExit("REFUSED: %d rungs after, expected 3243; this promote edits notes only"
                         % rung_count(data))
    for slug, name in SHIPPED:
        methods = [r.get("method") for r in find_problem(data, slug, name)["control_ladder"]]
        if len(methods) != len(set(methods)):
            raise SystemExit("REFUSED: %s/%s ladder carries a duplicate method" % (slug, name))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; every id cited here already exists")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    # `--canonical` is the form promote_fixture's CHAIN replay uses; both spellings are accepted.
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    pre = snapshot(data)
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data)
    check_catalog_untouched(before_cm, before_sc, data)
    retired = check_retired_claims(data)
    required = check_required_claims(data)
    survivors = check_survivors(data)
    urls = check_urls_retired(data)
    uniform = check_maggot_anchors_uniform(data)

    blob = serialize(data)
    print("leaves changed      : %d (%d prose, %d rung notes, %d severity, %d source sets)"
          % (n, EXPECTED_PROSE, EXPECTED_RUNG_NOTES, EXPECTED_SEVERITY, EXPECTED_SOURCE_SETS))
    print("retired claims gone : %d/%d" % (retired, len(RETIRED)))
    print("required claims in  : %d registers" % required)
    print("pinned phrases kept : %d" % survivors)
    print("retired anchors gone: %d URL patterns on 0 targets" % urls)
    print("maggot anchors      : %d uniform across %d crops" % (uniform, len(_MAGGOT_TARGETS)))
    print("leek pink root      : severity medium -> low")
    print("base  SHA           : %s" % sha)
    print("post  SHA           : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
