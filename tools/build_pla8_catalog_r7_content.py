#!/usr/bin/env python3
"""PLA-8 catalog round 7: the two controls the pea batch cannot express, and one widening REFUSED.

Same method as r5: read the crops' prose BEFORE preparing the batch. All eight problems on
`snow-peas` were read against the catalog ahead of batch 6, and two controls the prose leads with
had no home. A third candidate looked obvious, was hunted properly, and is NOT built -- which is the
most useful thing in this round.

--------------------------------------------------------------------------------------------------
MINT 1 -- `biofungicide`
--------------------------------------------------------------------------------------------------
Owed since batch 3 ("no biofungicide or potassium-bicarbonate key"). On the peas it is load-bearing:
powdery mildew is severity HIGH on both crops, and `organic_treatment_seasoned` names exactly two
materials, "Sulfur or a labeled biofungicide". The catalog could express one of the two.

  CU   "Less-toxic spray fungicides containing sulfur or copper soap, as well as biological control
        sprays for plant diseases containing Bacillus subtilis, are available."
  UC   "Bacillus-based fungicides are commercially available for powdery mildew control, for both
        professional use (e.g. Stargus, Cease) and home gardeners (e.g. Monterey Complete Disease
        Control, Revitalize)."
       "The active ingredients, Bacillus subtilis and Bacillus amyloliquifaciens (also known as
        Bacillus velezensis), stop the fungus from growing and attaching to the plant."
       "Research has not shown these products to be as effective as oils or sulfur in controlling
        the pathogen."

THE EFFICACY LIMIT IS THE MOST IMPORTANT SENTENCE ON THE SHEET AND IT IS CARRIED VERBATIM IN SUBSTANCE.
UC IPM says plainly that research has not shown these as effective as oils or sulfur. A method sheet
that recommended a biofungicide without that would be selling the gentler option as an equal one.
The guard suite pins it.

TIER IS `biological`, NOT `soft_chemical`, and that is a consistency call with `bt`: both are living
organisms applied as a spray, and `bt` already sits at `biological`. It also orders the ladder
correctly. Softest-first puts the biofungicide BEFORE sulfur, and UC IPM's efficacy note is exactly
what tells a reader why they might step past it to the sulfur rung rather than stopping there.

--------------------------------------------------------------------------------------------------
MINT 2 -- `weed_host_control`
--------------------------------------------------------------------------------------------------
Owed since batch 1, and refused by BOTH bean passes in batch 5 rather than folded into
`garden_sanitation`. The peas make it unavoidable: it appears on pea aphid, thrips and armyworms,
and USU states it for powdery mildew as well.

  UC   "Some aphids build up on weeds such as sowthistle and mustards, moving onto related crop
        seedlings after they emerge."
       "Before planting vegetables, check surrounding areas for sources of aphids and remove these
        sources."
  UC   "Avoid planting susceptible plants next to these areas, and control nearby weeds that are
        alternate hosts of pest thrips."
  USU  "Remove infected plant debris from fields before planting a new crop and remove weeds in the
        legume family."

NOT A DUPLICATE OF `garden_sanitation`, and the split is the point. That method clears the CROP's own
debris, mostly after harvest. This one clears OTHER plants that host the problem, mostly before and
around the crop. Both bean passes said so unprompted, in the same words: garden sanitation "means
end-of-season crop cleanup plus pulling affected leaves and fruit, which is a different action."

`applies_to` is `insect_soft_bodied` + `fungal_foliar`, the three cases actually read: two
sap-suckers and one foliar fungus whose alternate hosts are named by family. `insect_general` was
considered and REJECTED -- `TYPE_TARGETS` maps `mite` to {mite, insect_general}, so declaring it
would make this method legal on a spider mite, and nothing was read for that. Same trap that
`planting_time_avoidance` fell into at r5 and that its own guard suite caught.

--------------------------------------------------------------------------------------------------
NOT BUILT -- widening `planting_time_avoidance` to a fungal target. THE HUNT CAME BACK EMPTY.
--------------------------------------------------------------------------------------------------
This looked like the obvious third item. Both peas' prevention prose says, in both registers, to
"Plant early so the crop finishes before the mildew weather arrives", and powdery mildew is their
highest-severity problem. r5 scoped `planting_time_avoidance` to insects with an explicit note that
timing a sowing against a DISEASE is a real practice for which nothing had been read. This is where
that evidence should have arrived.

IT DID NOT. Fetched and read: Clemson's Garden Peas factsheet, Clemson's Powdery Mildew factsheet,
UMN's Growing Peas guide, UMN's IPM pea blog, USU's legume powdery mildew page, and Cornell's
disease-resistant pea varieties list. What they support, separately:

  * plant early BECAUSE PEAS ARE A COOL-SEASON CROP -- Clemson: "Plant pea seeds as early in spring
    as the ground can be worked", with peas described as suffering "in the heat and humidity of
    summer"; UMN: "Plant the seed as soon as the soil has thawed and is workable."
  * powdery mildew arrives in that later weather -- UMN: "During periods of hot dry weather, powdery
    mildew can develop on all parts of the plant"; UMN IPM: "The pea-specific powdery mildew is most
    commonly seen in later-season peas."

**Not one of them states the causal link as a control.** Clemson's peas factsheet lists powdery
mildew among the crop's problems and connects it to neither timing nor heat. The connection is an
inference, and a plausible one, but assembling a recommendation out of two true sentences from
different parts of a document is how `planting_time_avoidance` acquired a wrong criterion at r5.
So the method keeps its insect scope, and the widening waits for a document that makes the claim.

RECORDED AS AN EXISTING-PROSE FINDING for the batch-6 read, and it is the sharper half of this
round: **both peas assert timing as a powdery-mildew prevention step in CONSUMER prose on their
HIGHEST-severity problem, citing four sources, and the four documents reachable do not make that
claim.** The components are each sourced; the conclusion is ours. Not fixed here -- this promote
touches no crop.

--------------------------------------------------------------------------------------------------
ALSO ADJUDICATED, NOT MINTED
--------------------------------------------------------------------------------------------------
* "Avoid damaging the roots when planting" now appears on the beans AND the peas, so it is a real
  recurring control with no home. It is still ONE sentence per crop with no document read for it as
  a named practice, and batch 5 already recorded it as a gap. Left for a round that sources it
  properly rather than minted on frequency alone.
* Pea weevil's "freezing saved seed for several days kills any larvae inside" and "inspect dried
  peas for exit holes before storing seed" are seed-handling controls with no catalog home. Narrow
  to one crop family; recorded, not minted.

Used by: tools/promote_pla8_catalog_r7.py
"""

VERIFIED = "2026-08-25"

NEW_SOURCES = {
    "ucanr_ext_thrips": {
        "id": "ucanr_ext_thrips",
        "name": "UC IPM Pest Notes -- Thrips",
        # A54: read OFF THE DOCUMENT.
        "title": "Thrips / Home and Landscape / UC Statewide IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": "UC IPM Pest Notes 7429. Cited for weedy ALTERNATE HOSTS as a thrips source, "
                       "the second insect case behind weed_host_control: 'Avoid planting "
                       "susceptible plants next to these areas, and control nearby weeds that are "
                       "alternate hosts of pest thrips' and 'Thrips species that feed on many "
                       "different plant species often move into gardens and landscapes when plants "
                       "in weedy areas or grasslands begin to dry in spring or summer.'",
        "_admission_provenance":
            "Minted 2026-08-25 (PLA-8 catalog round 7). `weed_host_control` rests on three "
            "documents and two are UC IPM Pest Notes; anchoring_urls allows one URL per source id, "
            "so the second needs a document-scoped sibling rather than overwriting the first. "
            "Document fetched and read before pinning; title read off the document.",
    },
}

MINTS = {
    "biofungicide": {
        "name": "Biological fungicide",
        # `biological`, matching `bt`: both are living organisms applied as a spray. It also puts
        # this rung BEFORE sulfur under softest-first, which is the correct escalation.
        "tier": "biological",
        "applies_to": ["fungal_foliar"],
        "how_it_works_beginner":
            "These sprays contain live bacteria rather than a chemical. Applied to the leaves, they "
            "settle on the surface and get in the way of the fungus taking hold, so they work best "
            "started at the very first spots and repeated on the label's schedule. They are the "
            "gentlest thing on the shelf that does anything at all against a leaf fungus, and they "
            "ask more of your timing than a stronger spray would. If the mildew is already through "
            "the planting, this is not the rung that will turn it around.",
        "how_it_works_seasoned":
            "Bacterial biofungicides, the Bacillus-based products, colonize the leaf surface and "
            "interfere with germination and attachment rather than killing established mycelium. UC "
            "IPM names the active ingredients as Bacillus subtilis and Bacillus amyloliquifaciens, "
            "also known as Bacillus velezensis, and describes them as stopping the fungus from "
            "growing and attaching to the plant. The same source is blunt about where they sit: "
            "research has not shown these products to be as effective as oils or sulfur in "
            "controlling the pathogen. Treat them as a preventive-to-early-curative option chosen "
            "for their low impact, not as a substitute for the stronger rung below them.",
        "best_use":
            "The first spots of a leaf fungus on a crop you would rather not put sulfur on, applied "
            "early and repeated. Distinct from sulfur, which is more effective and sits one rung "
            "further up; reach past this one when the mildew is already established.",
        "find_it_beginner":
            "Sold for home gardens as Serenade Garden Disease Control, Monterey Complete Disease "
            "Control and Revitalize. Check the label lists your crop before you buy.",
        "pros": [
            "The lowest-impact spray that acts on a leaf fungus at all, with no re-entry worries "
            "for a home bed",
            "Works on the leaf surface rather than in the plant, so it fits early where nothing "
            "stronger is wanted yet",
        ],
        "cons": [
            "Research has not shown these as effective as oils or sulfur, so a bad year can outrun them",
            "Preventive to early-curative only, and it needs repeating on the label's interval to do "
            "anything",
        ],
        "cautions": [
            "Live cultures have a shelf life and a storage temperature; an old or heat-stored bottle "
            "may do nothing at all",
        ],
        "sources": ["ucanr_ext", "clemson_hgic"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/home-and-landscape/powdery-mildew-on-ornamentals/",
                          "verified": VERIFIED},
            "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/powdery-mildew/",
                             "verified": VERIFIED},
        },
    },
    "weed_host_control": {
        "name": "Clearing the weeds that host it",
        "tier": "cultural",
        # Two sap-suckers and one foliar fungus: exactly the three cases read. `insect_general` was
        # REJECTED because TYPE_TARGETS maps `mite` to {mite, insect_general}, and nothing here is
        # about mites. Same trap planting_time_avoidance fell into at r5.
        "applies_to": ["insect_soft_bodied", "fungal_foliar"],
        "how_it_works_beginner":
            "Some pests and diseases spend part of the year on weeds in and around the bed, then "
            "move onto the crop as it comes up. Clearing those weeds before you sow, and keeping "
            "the edges of the bed clear through the season, takes away the place the problem waits "
            "in. It helps most where the weeds are close relatives of the crop, because those are "
            "the ones that host the same trouble.",
        "how_it_works_seasoned":
            "Weedy alternate hosts are a reservoir, and removing them lowers the starting pressure "
            "rather than treating the crop. UC IPM puts the aphid case concretely, that some aphids "
            "build up on weeds such as sowthistle and mustards and move onto related crop seedlings "
            "after they emerge, and its instruction is to check surrounding areas for sources "
            "before planting vegetables and remove them. For thrips it is the same move, to control "
            "nearby weeds that are alternate hosts. On the disease side the relationship runs by "
            "family: USU's guidance on pea powdery mildew is to remove weeds in the legume family "
            "along with infected debris. Timing matters more than thoroughness here, since the "
            "clearance is worth most before the crop emerges.",
        "best_use":
            "A bed with a history of aphids, thrips, or a foliar fungus whose weedy relatives grow "
            "nearby, cleared before sowing and kept clear at the edges. Distinct from garden "
            "sanitation, which removes the CROP's own debris, mostly after harvest; this removes "
            "OTHER plants that host the problem, mostly before the crop is up.",
        "pros": [
            "Costs nothing but the weeding you were half doing anyway, and it acts before the crop "
            "is exposed",
            "Lowers the pressure behind several problems at once, since one weedy patch often hosts "
            "more than one",
        ],
        "cons": [
            "Preventive only; it does nothing about a colony or an infection already on the crop",
            "Only as good as your reach, since a reservoir over the fence is outside what you can clear",
        ],
        "cautions": [
            "The relationship is host-specific rather than general tidiness, so it is worth knowing "
            "which weeds host the problem before clearing ground that was doing no harm",
        ],
        "sources": ["ucanr_ext", "ucanr_ext_thrips", "usu_ext"],
        "anchoring_urls": {
            "ucanr_ext": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html", "verified": VERIFIED},
            "ucanr_ext_thrips": {"url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html",
                                 "verified": VERIFIED},
            "usu_ext": {"url": "https://extension.usu.edu/vegetableguide/legumes/powdery-mildew",
                        "verified": VERIFIED},
        },
    },
}

# Qualifiers the prose must remain faithful to. The suite asserts each survives.
REQUIRED_HEDGES = {
    "biofungicide": ("as effective as oils or sulfur",),
    "weed_host_control": ("host-specific",),
}

# The method whose scope this round deliberately did NOT widen, and the target it did not gain.
# A guard asserts the refusal held, so a later pass cannot quietly add it without new sourcing.
REFUSED_WIDENING = ("planting_time_avoidance", ("fungal_foliar", "fungal_soilborne",
                                                "disease_general", "bacterial", "viral"))


def apply_round(data):
    cm = data["control_methods"]
    sc = data["source_catalog"]
    for key in MINTS:
        if key in cm:
            raise AssertionError(f"{key} is already in the catalog")
    for sid in NEW_SOURCES:
        if sid in sc:
            raise AssertionError(f"source id {sid} is already in source_catalog")
    for sid, entry in NEW_SOURCES.items():
        sc[sid] = dict(entry)
    for key, method in MINTS.items():
        cm[key] = dict(method)
    return {"minted": sorted(MINTS), "sources": sorted(NEW_SOURCES)}


if __name__ == "__main__":
    import json, os
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    before_cm, before_sc = len(d["control_methods"]), len(d["source_catalog"])
    s = apply_round(d)
    print(f"minted methods : {', '.join(s['minted'])}")
    print(f"minted sources : {', '.join(s['sources'])}")
    print(f"control_methods: {before_cm} -> {len(d['control_methods'])}")
    print(f"source_catalog : {before_sc} -> {len(d['source_catalog'])}")
