# persimmon -- PLA-8 batch 26 record / source pass

Reviewer note on retrieval paths (brief rule 5): `curl` was denied by the session permission system, so every
document below was read through WebFetch (first-party HTTP, summarizer asked for verbatim text), through the
`r.jina.ai` text proxy where the first-party host refused (marked PROXY), or by running `pypdf` locally on a
PDF that WebFetch saved to disk (marked PYPDF). A PROXY or PYPDF read is weaker than a first-party read and is
flagged as such on each anchor. All fetches 2026-09-04.

Two UF/IFAS documents that turn out to be load-bearing for this crop are RETIRED from Ask IFAS:
* ENY-835 / IN669 (Mizell, "The Persimmon Borer Sannina uroceriformis Walker, Pest of Persimmon", pub. 07/2006):
  `https://ask.ifas.ufl.edu/publication/IN669` returns **HTTP 410 Gone**; it is absent from
  `https://ask.ifas.ufl.edu/topics/persimmons`. An archived copy is in UF's EDIS journal archive at
  `https://journals.flvc.org/edis/article/view/116051` (PDF `.../download/116051/114234`), which 403s to WebFetch
  and was read only via PROXY.
* ENY-803 (Mizell & Brinen, "Insect Management in Oriental Persimmon", orig. Oct 1993, reviewed Jan 2015): not on
  Ask IFAS, not on the persimmons topic page; the only copy found is a third-party mirror
  (`growables.org/.../PersimmonInsectManagement.pdf`), read by PYPDF. It carries the footer "This document is
  ENY-803, one of a series of the Entomology and Nematology Department, UF/IFAS Extension." It is quoted below as
  evidence of what UF published, but it has NO first-party live URL to anchor to -- the orchestrator should decide
  whether an archived/mirrored UF document is admissible under `uf_ifas_edis` or is evidence-only.

The record's `uc_ipm` anchor URL `https://ipm.ucanr.edu/PMG/GARDEN/PLANTS/persimmon.html` is live and serves the
same content as `https://ipm.ucanr.edu/home-and-landscape/persimmon/` (title "Persimmon / Home and Landscape");
the proxy reported no redirect. It is a HOME page. Its complete "Pests and Disorders" list, verbatim:
* Invertebrates: "Blister, Bud, Erineum, Gall, and Rust Mites"; "Flatheaded Borers"; "Foliage-feeding
  Caterpillars (Trees and Shrubs)"; "Fuller Rose Beetle"; "Mealybugs (Invertebrates)"; "Nematodes"; "Redhumped
  Caterpillar"; "Scales"
* Plant Diseases: "Armillaria Root Rot"; "Botrytis Blight, or Gray Mold"; "Leaf Spot Diseases"; "Phytophthora
  Root and Crown Rot (Diseases)"; "Wood Decay Fungi in Landscape Trees"
* Environmental Disorders: "Nutrient and Mineral Excesses, Salinity, and Salt Toxicity"; "Nutrient Deficiencies";
  "Water Deficit and Excess"
* Weeds: "Weed Management Around Ornamental Trees and Shrubs"
Every item is a LINK to a generic UC IPM page (e.g. Scales -> `/home-and-landscape/scales/`, Leaf Spot Diseases
-> `/home-and-landscape/leaf-spot-diseases/`); none of the linked pages mentions persimmon. So the persimmon page
asserts that each listed problem occurs on persimmon, and nothing more crop-specific than that. No anthracnose,
no psyllid, no persimmon borer, no dieback or canker appears on it. Its only management sentence: "Persimmons do
well in areas with full sun. They are tolerant of many soil types but require good drainage."

Documents read and their kind (all T1 unless noted):
* `uf_ifas_edis` HS1389 "Japanese Persimmon Cultural Practices in Florida" (Sarkhosh, Huff, Andersen; page
  metadata date 2020-10-20) -- home/commercial hybrid; its Table 3/4 control cells name commercial products.
* `uga_ext` C784 "Home Garden Persimmons" (Westerfield; "Published with full review on August 18, 2022") -- home.
* `clemson_hgic` HGIC 1357 "How to Grow Persimmons in South Carolina" (Parker, Reighard; updated Dec 5, 2025,
  orig. 09/99) -- home.
* `tamu_agrilife` E-611 "Persimmons" (Stein, Nesbitt, Kamas; 2-13; the `persimmons_2015.pdf` file) -- PYPDF,
  6 pages, 11,054 chars of clean text (WebFetch's own summarizer could not read it; pypdf could).
* `ncsu_ext` Plant Toolbox Diospyros kaki -- one sentence field, see below; `ncsu_ext` "Persimmon Psyllid"
  (Baker; Nov 7 2018, rev. Oct 9 2019) -- home.
* `uc_ipm` Pest Notes 7408 Scales (rev. 09/2014), 74174 Mealybugs (03/2016), 74133 Phytophthora Root and Crown
  Rot (01/2025), 74171 Armillaria Root Rot (01/2020), 7420 Anthracnose (05/2020), the home-and-landscape
  "Flatheaded Borers" and "Leaf Spot Diseases" pages -- all home, none mentions persimmon.
* `ucd_fruitnut` "Persimmon Scion & Rootstock Selection" (fruitsandnuts.ucdavis.edu) -- PROXY only (403 direct
  on both the ucdavis and ucanr hosts).
* `uada_ext` Plant Health Clinic disease note "Persimmon Leaf Spot" (Smith & Pavel, Issue 24) -- home/diagnostic.
* `uada_ext_fruit_trees` (scoped key) -- carries one persimmon sentence, quoted under Leaf spot.
* `aces_ext` "Native Fruits: Persimmon" (Taylor & Akers-Campbell, Dec 16 2024) -- native persimmon only.
* `uf_ifas_edis` EENY-666/IN1149 Longtailed Mealybug -- host list.
* VCE 450-726 Botryosphaeria Canker and Dieback (Bush & Rodriguez Salamanca, Nov 17 2023) -- read; does NOT name
  persimmon; no admissible key beyond the scoped `vce_*` entries, and it is not needed.
* UC ANR FNRIC "Persimmon Insect, Mite & Nematode Pests" and "Persimmon Pests & Deficiencies" pages
  (`ucanr.edu/sites/btfnp/...`) -- LOCATED BUT UNREADABLE: 403 on the direct host and 403 through the proxy.
  These are the only pages a search snippet attributes the mealybug-under-the-calyx claim to. Not cited.


## Scale insects [pests]  -- severity medium, type pest
STATUS: SOURCED-OK (one symptom claim is WRONG for the named species; one species name has only a retired anchor)
ORGANISM: white peach scale *Pseudaulacaspis pentagona* (armored), per HS1389 Table 3 ("Scale (Pseudaulacaspis
  pentagona)") and ENY-803 ("Scales, predominantly white peach scale"). Soft scales named on persimmon by
  ENY-803 only: "Indian wax, Ceroplastes ceriferus, Florida wax, C. floridensis, Brown soft scale, C.
  hesperidium, Acuminate scale, Kilifia acuminata, and European fruit leucanium, Parthenoleucanium corni" (sic,
  = *Parthenolecanium corni*); armored also "Hemiberlesia rapax, Greedy scale". UGA C784 names "Persimmon scale
  and tuliptree scale" (tuliptree scale = *Toumeyella liriodendri*, a soft scale; UGA gives no binomial).
ANCHORS: uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04 -- home/commercial hybrid
  > "Scale (Pseudaulacaspis pentagona)" | "Snow-white patches on trunk and limbs, easily scraped off. Most visible
  > when males emerge during warm weather." | "3% dormant oil applied before bud break, summer oil, or two
  > pesticide applications 1–2 weeks apart (imidacloprid, MOA 4A, such as Provado 1.6F; potassium salt such as
  > Safer soap; or Scalecide); ladybird beetles and lacewings for biological control."
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/persimmon/ -- verified 2026-09-04 -- home (list item only)
  > "Scales" (linked list item under Invertebrates; no sentence)
ANCHORS: uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn7408.html -- verified 2026-09-04 -- home (generic, no persimmon)
  > "Armored scales do not produce honeydew. Soft scales and certain other types feed on phloem sap and excrete
  > abundant, sticky honeydew."
  > "Many species are usually well controlled by beneficial predators and parasites"
  > "To control most scales overwintering on deciduous woody plants, thoroughly spray the bark of terminal shoots
  > with oil during winter."
  > "You can prune off heavily infested twigs and branches, if they are limited to a few parts of small plants"
  > "ants attack and feed on scale parasites and predators, control ants if they are tending scales"
  > "To deny ants access to plant canopies, prune branches or weeds that provide a bridge between buildings or the
  > ground and apply a sticky material (Tanglefoot) to trunks."
  > "During the spring before crawlers begin to emerge, tightly encircle each of several scale-infested twigs or
  > branches with transparent tape that is sticky on both sides."
ANCHORS (not in record): uga_ext https://fieldreport.caes.uga.edu/publications/C784/ -- verified 2026-09-04 -- home
  > "Persimmon scale and tuliptree scale are to be expected. In unsprayed situations, scale are generally kept
  > under control by natural parasites, predators and diseases."
  > "Dormant oil application shortly before bud swell should provide good control of scale."
ANCHORS (retired, evidence only): uf_ifas_edis ENY-803 -- PYPDF of a third-party mirror -- no live URL
  > "Scales, predominantly white peach scale, attack the wood on the branches and trunk. Small infestations may
  > be removed by pruning, larger infestations should be treated with a dormant or summer oil or with a
  > conventional pesticide during the growing season targeted to the crawler stage of the scale. Two applications
  > 7-14 days apart may be necessary to control large infestations."
  > "Do not spray unless you have pests present, they were present last year or, as for example borers, you are
  > fairly certain they will occur. Spraying may upset the system. Pests like mites, leafminers and aphids often
  > are induced by pesticide use which kills the natural enemies that usually hold them in check. Often the best
  > strategy is to do nothing and let nature take its course."
RECORD CLAIMS THAT HOLD: white peach scale "snow-white encrustations on the trunk and limbs" (HS1389); dormant
  oil as the main direct control (HS1389 "3% dormant oil applied before bud break"; UGA "shortly before bud
  swell"); natural enemies usually hold scale (UGA verbatim; HS1389 "ladybird beetles and lacewings"); prune out
  encrusted wood (pn7408 generic; ENY-803 "Small infestations may be removed by pruning"); avoid broad-spectrum
  sprays (pn7408; ENY-803); honeydew/sooty mold/ants for SOFT scales (pn7408 generic); monitor the trunk for early
  white patches (HS1389 symptom cell).
RECORD CLAIMS WITH NO ANCHOR: "soft scales (Parthenolecanium spp.)" on persimmon -- carried only by the retired
  ENY-803 (as "Parthenoleucanium corni"); UGA names tuliptree scale instead; "Vigor and fruit quality decline
  where scale builds up unchecked" (no persimmon document says this; pn7408 is generic); "check the trunk and
  branches now and then ... before it spreads" as a timing signal (no document names a monitoring signal; pn7408
  offers the double-sided-tape crawler check).
RECORD CLAIMS THAT ARE WRONG: "Heavy infestations produce sticky honeydew that blackens with sooty mold and draws
  ants" is stated for the entry as a whole, whose headline species is white peach scale, an ARMORED scale.
  pn7408: "Armored scales do not produce honeydew." The honeydew/sooty mold/ant sentence is true of the soft
  scales only and must be scoped to them.
BUNDLE / GENERIC VERDICT: genuine umbrella (armored + soft scales) that the literature itself leaves multi-species;
  HS1389 pins white peach scale as the named species; keep as one `scale-insects` join with the honeydew claim
  scoped to soft scales.
LADDER-RELEVANT FACTS the record does not carry: overwintering site = bark of branches and trunk (ENY-803; pn7408
  "overwintering on deciduous woody plants"); vulnerable stage = crawlers, two applications 7-14 days apart
  (ENY-803) / "1–2 weeks apart" (HS1389); the crawler monitoring method (pn7408 sticky tape); ant exclusion
  with a sticky trunk band (pn7408); the explicit do-nothing default (ENY-803, above); commercial product names
  in HS1389's control cell (imidacloprid/Provado, Scalecide) are commercial-leaning and should not be carried.
PLA-457: pn7408: "Do not apply oil within 3 weeks of an application of sulfur-containing compounds, such as
  wettable sulfur." HS1389's "two pesticide applications 1–2 weeks apart" is a pesticide re-treatment interval,
  not an oil/sulfur interval. ENY-803 lists "Acme Lime - Sulfur Spray (non-bearing)" under Mites with no interval.


## Mealybugs [pests]  -- severity low, type pest
STATUS: SOURCED-WEAK (presence anchored; the crop-specific calyx claim is located on an unreadable page)
ORGANISM: not resolved to a species by any persimmon document read. UF EENY-666 lists persimmon as a host of the
  longtailed mealybug *Pseudococcus longispinus*; that is the only binomial tied to persimmon in an admissible
  document.
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/persimmon/ -- verified 2026-09-04 -- home (list item only)
  > "Mealybugs (Invertebrates)" (linked list item; no sentence)
ANCHORS: ncsu_ext https://plants.ces.ncsu.edu/plants/diospyros-kaki/ -- verified 2026-09-04 -- toolbox, but a SENTENCE
  > "Insects, Diseases, and Other Plant Problems: Scale, mealybug and leaf spot can occur. Fruit drop can be
  > messy."
  (Brief rule 7 does not bite here: this toolbox entry has no "Insects:"/"Diseases:" title rows; the field is a
  prose sentence. It is thin, but it is an assertion, not a factsheet title.)
ANCHORS: uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn74174.html -- verified 2026-09-04 -- home (generic, no persimmon)
  > "Fortunately most species have natural enemies that keep their populations below damaging levels in outdoor
  > systems such as landscapes and gardens."
  > "Preserve naturally occurring biological control agents by avoiding use of broad-spectrum insecticides for
  > any pests in the area. Also keep ants out of mealybug-infested areas and plants because ants protect
  > mealybugs from their natural enemies."
  > "Insecticidal soaps, horticultural oil, or neem oil insecticides applied directly on mealybugs can provide
  > some suppression, especially against younger nymphs that have less wax accumulation."
  > "If mealybugs are somewhat exposed, it may be possible to reduce populations on sturdy plants with a
  > high-pressure or forcible spray of water."
  > "Among fruit trees, citrus has the most problems, but mealybugs may sometimes be found on stone fruits or
  > pome fruits, although rarely at damaging levels."
ANCHORS (not in record): uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04
  > (Persimmon psylla row, Symptoms) "White-colored nymphs found within distorted leaves and black-bodied adults
  > on leaf surface. Mealy bugs may also be present."
ANCHORS (not in record): tamu_agrilife persimmons_2015.pdf -- PYPDF -- home/commercial
  > "Few insect pests attack persimmons. In some summers, caterpillars may defoliate persimmon trees, and cases
  > of mealy bugs, thrips, mites, ants, and fruit flies have been reported."
ANCHORS (not in record): uf_ifas_edis https://ask.ifas.ufl.edu/publication/IN1149 -- verified 2026-09-04 -- host list
  > "The longtailed mealybug has a relatively wide host range that includes many economically important crops,
  > such as avocado, citrus, grapes, pear, persimmon, and pineapple"
ANCHORS (already carved out in the catalog): ucanr_ext_ants pn7411 carries the ant-tending mechanism and the
  sticky-band method; ucanr_ext_sooty_mold pn74108 carries the sooty-mold side.
RECORD CLAIMS THAT HOLD: mealybugs occur on persimmon (UC IPM list; NCSU sentence; HS1389; TAMU); natural enemies
  generally keep them below damaging levels outdoors (pn74174); ants protect them, so control ants (pn74174;
  pn7411); oil / soap spot treatment (pn74174); avoid broad-spectrum sprays (pn74174).
RECORD CLAIMS WITH NO ANCHOR: "under the calyx of the fruit" / "feeding under the calyx can contaminate and
  blemish fruit" / "inspect the calyx end of developing fruit" -- a search snippet attributes exactly this to the
  UC ANR FNRIC page "Persimmon Insect, Mite & Nematode Pests" ("small cracks under the calyx that occur during
  rapid fruit expansion exuding sap which attracts mealybugs"), but that page returned 403 on the direct host
  and 403 through the proxy, so the sentence was NOT read at source and cannot be quoted. Treat as
  located-unread. "removing infested fruit early" -- no document. "white, cottony wax ... in leaf axils" --
  generic pn74174 description, not stated for persimmon.
RECORD CLAIMS THAT ARE WRONG: none found.
BUNDLE / GENERIC VERDICT: bare generic that the literature leaves unresolved on this crop (no persimmon document
  names the species; EENY-666 gives one host-list binomial). Join `mealybugs`.
LADDER-RELEVANT FACTS the record does not carry: water-blast as the physical rung (pn74174); the "rarely at
  damaging levels" framing for fruit trees other than citrus (pn74174), which supports severity low; HS1389
  ties mealybug presence to the psylla's honeydew/ant complex ("May also need to control the ants that feed on
  the honeydew").
PLA-457: none seen in pn74174 ("No oil/sulfur interval is mentioned"); pn7408's 3-week sentence applies if oil
  is used here.


## Persimmon psyllid [pests]  -- severity low, type pest
STATUS: SOURCED-OK (clemson_hgic anchor is a bare list item; a better ncsu_ext anchor exists)
ORGANISM: *Trioza diospyri* (Ashmead) = *Baeoalitriozus diospyri*, per HS1389 Table 3 ("Persimmon psylla (Trioza
  diospyri)") and NC State "Persimmon Psyllid" ("Persimmon psyllids or persimmon psyllas, Baeoalitriozus
  diospyri or Trioza diospyri"). UGA and Clemson give the common name only.
ANCHORS: clemson_hgic https://hgic.clemson.edu/factsheet/persimmon/ -- verified 2026-09-04 -- home (list item only)
  > "Insect pests of persimmons include:" ... "Persimmon psyllid" (bulleted item; no sentence about it)
ANCHORS: uga_ext https://fieldreport.caes.uga.edu/publications/C784/ -- verified 2026-09-04 -- home
  > "Persimmon psyllid is a tiny, leaf feeding, aphid-like pest that causes leaf deformation. Infested leaves
  > roll and curl up on themselves."
  > "Psyllid are often limited by natural parasites. Don't apply insecticides until after you have observed
  > damage."
  > "Native persimmons may be attacked by a number of insects; oriental persimmons are, at this time, relatively
  > free of serious insect problems."
ANCHORS (not in record): ncsu_ext https://content.ces.ncsu.edu/persimmon-psyllid -- verified 2026-09-04 -- home
  > "Persimmon psyllids feed on Japanese persimmon as well as ornamental and native persimmons."
  > "Infested leaves are often misshapen. Nymphs secrete white fluff and also cause terminals to twist and become
  > galled."
  > "Development from egg to adult takes only a few weeks in spring."
  > "On native persimmon, these psyllids can be temporarily abundant; but their populations soon decline
  > naturally, as they are attacked by their natural enemies, including parasitic wasps."
  > "Psyllids also excrete sticky honeydew on which dark sooty molds may grow."
  > "Horticultural oils suppress adult and immature persimmon psyllids without leaving a toxic residue that might
  > harm beneficial insects and mites."
  > "Most insecticides labeled for residential landscape use will give adequate control although the pyrethroids
  > are harsh on beneficials."
ANCHORS (not in record): uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04
  > "Crinkled and deformed young leaves, stunted growth. White-colored nymphs found within distorted leaves and
  > black-bodied adults on leaf surface. Mealy bugs may also be present." | "Best to control very early; sprays
  > less effective when leaves curl. Many pesticide options. May also need to control the ants that feed on the
  > honeydew."
ANCHORS (retired, evidence only): ENY-803 -- PYPDF
  > "Persimmon psylla is the primary leaf pest and is found attacking newly forming leaves in spring. Infested
  > leaves appear crinkled and malformed (Figure 2). The white powdery covered nymphs and black bodied adults are
  > found feeding inside the mishapen leaves which makes control difficult. Psylla infestations stunt the growth
  > of shoots on young trees. Control with conventional pesticides should be timed to the bloom stage."
RECORD CLAIMS THAT HOLD: spring leaf roll/curl around feeding nymphs (UGA; HS1389; NCSU); "waxy filaments" =
  NCSU "white fluff"; damage mostly cosmetic on established trees but can stunt young shoots (ENY-803 "stunt the
  growth of shoots on young trees"; UGA/NCSU on limited importance); natural enemies limit it (UGA; NCSU);
  usually no treatment (UGA "Don't apply insecticides until after you have observed damage"); it attacks both
  native and Oriental persimmon (NCSU; UGA).
RECORD CLAIMS WITH NO ANCHOR: "prune off and destroy the worst rolled tips in spring" -- no document; "Small
  crawlers" -- psyllid nymphs are not called crawlers in any document (NCSU "nymphs are flattened and less
  active").
RECORD CLAIMS THAT ARE WRONG: none refuted, but note the REGISTER TENSION: UF's persimmon documents call it "the
  primary leaf pest" and advise controlling "very early", timed "to the bloom stage" (a Florida
  commercial-leaning stance), whereas UGA and NCSU (home) say natural enemies limit it and to wait for damage.
  The record's "usually no treatment is warranted" follows the home documents; the ladder should say which.
BUNDLE / GENERIC VERDICT: single pinned organism.
LADDER-RELEVANT FACTS the record does not carry: vulnerable stage = new leaves in spring, "only a few weeks"
  egg-to-adult (NCSU); once leaves curl, sprays are "less effective" (HS1389) -- the timing signal is the first
  spring flush, not the rolled leaf; horticultural oil as the soft-chemical rung that spares beneficials (NCSU);
  pyrethroids "harsh on beneficials" (NCSU); honeydew and sooty mold (NCSU) and ant control (HS1389).
PLA-457: none seen.


## Persimmon borer [pests]  -- severity medium, type pest
STATUS: SOURCED-OK for the persimmon borer proper; the record BUNDLES it with flatheaded borers, and its `uc_ipm`
  anchor carries only the flatheaded half.
ORGANISM: (1) persimmon borer / persimmon clearwing borer *Sannina uroceriformis* Walker (Lepidoptera: Sesiidae),
  per HS1389 Table 3 ("Tree borers (Sannina uroceriformis and multiple species)") and ENY-835 ("The persimmon
  borer, Sannina uroceriformis Walker, (Lepidoptera: Sesiidae) attacks the American persimmon, Diospyros
  virginiana, which is its only known host."). (2) flatheaded borers, Buprestidae *Chrysobothris* spp., per the
  UC IPM persimmon list item "Flatheaded Borers" and ENY-803 ("Metallic wood borers (Family Buprestidae), whose
  larvae are known as flatheaded borers"); the UC IPM flatheaded page names *C. mali* and *C. femorata* but does
  NOT list persimmon among their hosts ("infests at least 70 species of broadleaved trees").
ANCHORS: uga_ext https://fieldreport.caes.uga.edu/publications/C784/ -- verified 2026-09-04 -- home
  > "Persimmon borer is a serious pest of native and oriental persimmons."
  > "Where infestations occur, preventive insecticide treatments similar to those made for peachtree borer will
  > be required."
  > "Other sporadic pests of persimmons include ambrosia beetles that attack where bark is injured or sun-scalded."
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/persimmon/ -- verified 2026-09-04 -- home (list item only)
  > "Flatheaded Borers" (linked list item; nothing about persimmon borer)
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/flatheaded-borers/ -- verified 2026-09-04 -- home (generic)
  > "Larvae can sometimes be killed by probing tunnels with a sharp, stiff wire. This method is practical only in
  > a small infestation on small trees. It is often difficult to know whether the wire has reached and killed the
  > larva. Avoid further damaging bark when probing trunks."
  > "Drought stress commonly results in trees being attacked by wood borers."
  > "Wet spots and cracking on bark are usually the first damage symptoms observed."
  > "Whitewash trunks of heavily pruned, newly planted, and young trees by applying white, indoor latex paint
  > diluted with an equal amount of water."
  > "Alternatively, wrap trunks with heavy paper to help prevent sunburned bark that can attract the egg laying
  > female borers."
  > "Unless trees are monitored regularly so that borer activity can be detected early, pesticide use is likely
  > to be too late and ineffective."
  > "Do not substitute insecticide applications for proper plant care."
ANCHORS (not in record): uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04
  > "Tree borers (Sannina uroceriformis and multiple species)" | "Gummy sap, frass, or sawdust coming from small
  > holes in bark, pruning cuts, or trunk near soil line." | "March through June applications best to prevent
  > larvae from entering tree. Limited direct control information; controls for peachtree borer may be effective
  > (imidacloprid)."
ANCHORS (not in record): clemson_hgic https://hgic.clemson.edu/factsheet/persimmon/ -- verified 2026-09-04 -- home
  > "It is important to monitor the persimmon borer. If borer damage is noted on the trunk or exposed roots,
  > treatment may be required."
  > "Chemical control of diseases and insects on large trees is usually not feasible since adequate coverage of
  > the foliage with a pesticide cannot be achieved."
ANCHORS (retired; archive read by PROXY): uf_ifas_edis ENY-835 / IN669, archive
  https://journals.flvc.org/edis/article/download/116051/114234 -- "Publication Date 07/06" -- 410 Gone on Ask IFAS
  > "The persimmon borer, Sannina uroceriformis Walker, (Lepidoptera: Sesiidae) attacks the American persimmon,
  > Diospyros virginiana, which is its only known host."
  > "On hatching, larvae move to suitable sites, usually at or near the root collar, to bore into the bark, but
  > attacks sometimes are initiated 30 to 60 cm above ground."
  > "Black gum exudate, particles of bark, and frass are often present, especially during the early stages of
  > attack on the base of the trunks."
  > "Damage can be readily identified by excavating roots (Figure 5)." "Small roots may be severed or hollowed
  > out, leaving only a shell." "Large roots may have two or more galleries."
  > "Heaviest populations occur in young trees 12 to 50 mm in diameter, but trees up to 20 cm at the root collar
  > have been found to be moderately infested."
  > "Larval feeding causes seedlings and young saplings to wilt and break." "Usually larvae injure large trees
  > less seriously, but populations sometime are large enough to cause weakening."
  > "The life cycle may require two to three years."
  > "Little is known of natural enemies of this borer." "No direct controls have been developed, but measures
  > recommended for the peachtree borer would probably be effective." "Control applications should be timed to
  > the period in spring (March to late June in Florida) when the adults are active to prevent the larvae from
  > entering the wood."
ANCHORS (retired, evidence only): ENY-803 -- PYPDF
  > "Several species of wood-boring insects may attack the roots, trunk and branches of persimmon. Persimmon
  > clearwing borer is a native pest of the American rootstock. The adult moth emerges in early spring and has one
  > generation per year. Pupal cases left by emerging adults can be found at the base of the tree near the root
  > crown (Figure 1)."
  > "The fungus, Botrysphaeria dothidia produces symptoms in many species of fruit trees termed gummosis. In
  > persimmon, the fungus produces discoloration of the wood and deep, elongate scars in the bark. Metallic wood
  > borers (Family Buprestidae), whose larvae are known as flatheaded borers, place their eggs along the scars.
  > The larvae then enter the bark and girdle the scaffold limbs by feeding in the phloem or inner bark tissue.
  > The combination of the fungus and the metallic wood borer damage may lead to severe losses of scaffold
  > limbs. The adult metallic wood borers are present for most of the growing season and are difficult to
  > manage. Control of borers is centered around good management practices. It is very important that healthy
  > trees are used to initiate the orchard and maintained."
  > "Stress will change the persimmon's susceptibility to pests, particularly borers."
RECORD CLAIMS THAT HOLD: gum + sawdust-like frass at the trunk base (HS1389; ENY-835); young trees girdled/killed
  (ENY-835 "wilt and break", "girdling and killing" roots); "the one persimmon pest extension warns can be
  serious, particularly in the Southeast" (UGA "serious pest"; Clemson "important to monitor"); attacks both
  native and Oriental persimmon (UGA), with the nuance that Sannina attacks the D. virginiana ROOTSTOCK and
  other borers the scion; stressed trees attacked first (ENY-803; UC IPM flatheaded "Drought stress"); no
  effective spray once inside (UC IPM flatheaded "pesticide use is likely to be too late and ineffective"; HS1389
  "Limited direct control information"); wire-kill (UC IPM flatheaded page, above -- for FLATHEADED borers, on
  small trees, with the caveat that it often fails); keep the trunk free of wounds (UGA ambrosia-beetle sentence;
  UC IPM flatheaded sunburn/injury sentences).
RECORD CLAIMS WITH NO ANCHOR: "inspect the trunk base each late summer for fresh gum and frass" -- no document
  gives an inspection month; ENY-835 gives adult activity "March to late June in Florida" and frass "especially
  during the early stages of attack", which implies early-summer inspection, not late summer; "Expose the crown
  ... kill larvae by hand with a wire" for the PERSIMMON borer -- ENY-835 says "No direct controls have been
  developed" and refers to peachtree-borer measures; the wire sentence exists only on the UC IPM flatheaded page;
  "Wilting or dying shoots" on an established tree -- ENY-835 describes wilting of seedlings/saplings, and
  scaffold-limb girdling is the FLATHEADED symptom (ENY-803); "healthy bark can also be entered" -- no document
  says this; "Keep ... well watered" -- only the generic flatheaded drought sentence.
RECORD CLAIMS THAT ARE WRONG: none refuted outright. But the documents CONTRADICT EACH OTHER on the life cycle:
  ENY-803 "has one generation per year" vs ENY-835 "The life cycle may require two to three years." Do not carry
  either without naming it. Also the record's beginner cause "larvae (grub stage) of borer beetles and moths" is
  correct only because it bundles Sannina (moth) with buprestids (beetles).
BUNDLE / GENERIC VERDICT: TWO organisms with different biology, hosts and controls. Sannina uroceriformis: SE
  native clearwing moth, larvae in the root collar and roots of D. virginiana (the rootstock), spring adult
  flight, gum/frass at the trunk base, peachtree-borer-style measures. Flatheaded borers (Chrysobothris spp.):
  buprestid beetles, larvae under the bark of scaffold limbs and trunks, entering at sunburn, wounds and
  Botryosphaeria scars, adults present most of the season, managed by whitewash/wraps, stress avoidance and
  wire probing. UC IPM lists only the flatheaded half for persimmon (California); UGA/Clemson/UF name only the
  persimmon borer as serious. Recommend: this entry becomes `persimmon-borer` (Sannina) and the flatheaded
  material moves out (either a second entry anchored to UC IPM + ENY-803, or dropped for the SE-facing record).
LADDER-RELEVANT FACTS the record does not carry: the host is the ROOTSTOCK ("its only known host" D. virginiana);
  attack site "at or near the root collar", sometimes "30 to 60 cm above ground"; adult activity window
  "March to late June in Florida" = the only timing any control can key to; "Heaviest populations occur in young
  trees 12 to 50 mm in diameter"; pupal cases at the root crown as a diagnostic sign (ENY-803); "Little is known
  of natural enemies" (no biological rung available); Clemson's home-tree caveat that chemical control on large
  trees "is usually not feasible"; UC IPM's flatheaded prevention set (whitewash, paper wrap, avoid pruning
  spring-summer) applies to the flatheaded half only.
PLA-457: none seen.


## Anthracnose [diseases]  -- severity medium, type disease
STATUS: ANCHOR-MISPOINTED (clemson_hgic carries nothing about anthracnose; open finding
  `persimmon_anthracnose_source` CONFIRMED) and SOURCED-WEAK for every biology and management sentence.
ORGANISM: *Gloeosporium* spp. ("anthracnose 'bitter rot'") and *Colletotrichum* sp., per HS1389 Table 4. TAMU
  names anthracnose without an organism. The modern synonymy the record leans on (Gloeosporium kaki =
  *Colletotrichum horii*; also C. gloeosporioides, C. acutatum reported on persimmon in the USA) is JOURNAL-ONLY
  (Mycology 2010 "Biology of Colletotrichum horii"; Plant Disease first reports) -- no extension document read
  states it. The record's "Colletotrichum and related genera" is nonetheless defensible from HS1389, which names
  both genera in the same row.
ANCHORS: uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04 -- home/commercial hybrid
  > "Leaf and fruit spots (Cercospora spp., Alternaria spp., Gloeosporium spp., Phyllosticta spp., Botrytis
  > cinerea, Pseudomonas syringae, Colletotrichum sp., Ramularia sp.)" | "Cercospora: leaf spots and early
  > defoliation. Gloeosporium: anthracnose 'bitter rot' that affects fruit and shoots. Colletotrichum: affects
  > ripening fruit. Ramularia: leaf spots sometimes in mid-season. Botrytis: brown leaf patches. Pseudomonas:
  > 'bacterial blast' leaf spots and blackened stem and leaf petioles." | "Proactive fungicide sprays in early
  > season, and cover sprays in summer in rotation."
ANCHORS: clemson_hgic https://hgic.clemson.edu/factsheet/persimmon/ -- verified 2026-09-04 -- home
  > "Persimmon diseases include:" "Fungal leaf spot" "Twig dieback" "Powdery mildew"  (anthracnose is NOT named
  > anywhere on the page -- DROP this key from the entry)
ANCHORS (not in record): tamu_agrilife persimmons_2015.pdf -- PYPDF -- home/commercial
  > "Persimmons are largely free of serious diseases; however, crown gall and anthracnose have occasionally
  > caused problems."
ANCHORS (generic, no persimmon): uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn7420.html -- verified 2026-09-04 -- home
  > "On deciduous trees, these fungi overwinter in infected twigs or dead leaf litter. In spring, the fungi
  > produce numerous microscopic spores that spread via splashing rain or irrigation water to new growth where
  > they germinate."
  > "Prune and destroy or bury infected leaves, twigs, and branches during fall or winter" / "Rake and dispose of
  > fallen leaves and twigs during the growing season and in fall."
  (pn7420's host table is ash, elm, dogwood, maple, oak, sycamore; it does not cover persimmon or any fruit rot,
  so it supports the record's biology only by analogy, which brief rule 2 does not allow as an anchor.)
RECORD CLAIMS THAT HOLD: anthracnose occurs on persimmon fruit and shoots (HS1389 "affects fruit and shoots";
  TAMU "occasionally caused problems"); "Infected fruit can rot" (HS1389 "bitter rot", Colletotrichum "affects
  ripening fruit").
RECORD CLAIMS WITH NO ANCHOR: "Dark, sunken lesions on fruit" (no persimmon document describes the lesion);
  "overwinter in dead wood and mummified fruit" (no persimmon document; pn7420 is generic and does not mention
  mummified fruit); "spread by rain-splash in warm, humid conditions" (pn7420 generic only); "Pressure is highest
  in the wet Southeast and lowest in dry-summer climates" (no document states a regional gradient; UC IPM's
  persimmon page simply omits anthracnose); the whole sanitation regime "prune out ... dead and cankered wood
  and remove mummified fruit ... keep the canopy open" (no persimmon document prescribes it for anthracnose);
  "Fungicides are rarely needed on a backyard tree if sanitation is kept up" (no document; see WRONG below);
  "favor cultivars with better tolerance" / "pick a variety known to hold up better" (NO document names any
  persimmon cultivar as anthracnose-tolerant -- a shape-fill sentence with nothing behind it).
RECORD CLAIMS THAT ARE WRONG: none is refuted verbatim, but "fungicides are rarely needed" runs against the only
  document that manages persimmon anthracnose, HS1389, whose control cell is "Proactive fungicide sprays in early
  season, and cover sprays in summer in rotation" (Florida, commercial-leaning). TAMU's "occasionally caused
  problems" supports low pressure in Texas. Carry the sanitation-first stance only as a home-tree inference
  labeled as such, not as an extension statement.
BUNDLE / GENERIC VERDICT: single disease complex (Gloeosporium/Colletotrichum); HS1389 folds it inside a
  "Leaf and fruit spots" umbrella row, so its Florida control advice is shared with Cercospora leaf spot.
LADDER-RELEVANT FACTS the record does not carry: HS1389's timing = early-season protectant plus summer cover
  sprays "in rotation"; the Florida framing that fruit rot shows on RIPENING fruit (Colletotrichum row); the
  bacterial look-alike in the same row ("Pseudomonas: 'bacterial blast' leaf spots and blackened stem and leaf
  petioles"), which a home diagnosis will confuse with anthracnose; no monitoring threshold anywhere; no
  cultivar resistance anywhere.
PLA-457: none seen.


## Root and crown rot [diseases]  -- severity medium, type disease
STATUS: SOURCED-OK for the Phytophthora attribution and the rootstock claims; genus-precision finding below.
ORGANISM: *Phytophthora* spp. (oomycete water molds) per the UC IPM persimmon list item "Phytophthora Root and
  Crown Rot"; UC IPM ALSO lists "Armillaria Root Rot" (*Armillaria mellea*) for persimmon as a SEPARATE item.
  TAMU's "root rot" names no genus (in a Texas fruit bulletin this is usually cotton root rot,
  *Phymatotrichopsis omnivora*, but the document does not say so and it must not be assumed).
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/persimmon/ -- verified 2026-09-04 -- home (list items)
  > "Phytophthora Root and Crown Rot (Diseases)"  and  "Armillaria Root Rot"  (both linked list items)
  > "They are tolerant of many soil types but require good drainage."
ANCHORS: uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn74133.html -- verified 2026-09-04 -- home (generic, no persimmon)
  > "Although technically not true fungi (Phytophthora is more closely related to brown algae)"
  > "Darkened areas in the bark around the crown and upper roots often develop, sometimes with gumming."
  > "Reddish brown zones, often separated from healthy tissue by a dark line, can be seen in the inner bark and
  > outer layer of wood."
  > "Improve soil drainage before planting."
  > "Consider planting trees and shrubs on mounds. The mounds should be 8 to 10 inches high for annuals and up to
  > 2 feet high"
  > "Avoid prolonged saturation of the soil or standing water around the base of trees"
  > "Do not rely on pesticide applications alone to control Phytophthora root and crown rot diseases."
ANCHORS: tamu_agrilife .../persimmons_2015.pdf -- PYPDF (WebFetch's summarizer could not read this PDF; pypdf
  extracted clean text) -- home/commercial
  > "The common American persimmon, used as the rootstock for Oriental persimmon trees, is widely adapted in
  > Texas. It thrives in sands to bottomland as long as the soils do not stand in water. The Texas persimmon
  > resists root rot; the common American persimmon is moderately susceptible, and the Oriental persimmon is
  > highly susceptible. It is critical that all Oriental trees be grafted or budded onto the common persimmon
  > because root rot is prevalent where the tree can grow."
  > "The best rootstock for Texas is the common American persimmon."
ANCHORS (not in record): uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04
  > "Japanese persimmons in Florida have nearly exclusively been grafted onto Diospyros virginiana, the native
  > persimmon of the United States. D. virginiana is widely used in the southern states due to its adaptability
  > to different soil types. It provides a tolerance of wet soils, is cold hardy, can withstand drought
  > conditions, and is compatible with most scion cultivars."
ANCHORS (not in record): ucd_fruitnut https://fruitsandnuts.ucdavis.edu/persimmon-scion-rooststock-selection --
  PROXY only (403 direct on both hosts) -- verified 2026-09-04
  > "D. virginiana has a fibrous root system tolerant of both drought and excess moisture, however trees
  > propagated on this rootstock are not uniform and are prone to suckering."
  > "D. lotus is tolerant to Armillaria, but susceptible to crown gall and Verticillium and does not tolerate
  > poorly drained soils."
  > "D. kaki is resistant to Agrobacterium and Armillaria but susceptible to Verticilium."
ANCHORS (generic): uc_ipm https://ipm.ucanr.edu/PMG/PESTNOTES/pn74171.html (Armillaria) -- verified 2026-09-04
  > "There are no registered fungicides for Armillaria control in California"; "There are no known cultivars or
  > varieties of plants that are completely immune"; root-collar excavation "remove the soil from the base of
  > infected trees to expose the large structural roots". No persimmon mention.
RECORD CLAIMS THAT HOLD: Phytophthora root and crown rot occurs on persimmon (UC IPM list); Oriental persimmon is
  highly susceptible to root rot and is grafted on native rootstock for that reason (TAMU verbatim); native
  D. virginiana tolerates wet soils (HS1389; UCD FNRIC "tolerant of ... excess moisture"); dark decayed bark at
  and below the soil line (pn74133); drainage, mounds, and not keeping the root zone saturated (pn74133; UC IPM
  persimmon "require good drainage"); no reliance on fungicide (pn74133 "Do not rely on pesticide applications
  alone").
RECORD CLAIMS WITH NO ANCHOR: "the tree may collapse over a season or two once the crown is girdled" (no
  document gives a timescale); "There is no cure once the crown is rotting" (pn74133 says do not rely on
  pesticides alone, not "no cure"); "sparse yellowing foliage" (pn74133 symptom sentences quoted above are about
  bark; the page's foliage sentence was not returned and was not verified).
RECORD CLAIMS THAT ARE WRONG (wording): "Soilborne Phytophthora (and related) fungi" / "Water-mold fungi" --
  pn74133: "technically not true fungi (Phytophthora is more closely related to brown algae)". "Water molds" is
  fine; "fungi" is not. Also: the TAMU tolerance sentence says the native rootstock is "moderately susceptible",
  not tolerant; the record's "more tolerant" is a relative reading of TAMU's ranking plus HS1389/UCD's wet-soil
  tolerance, and should be phrased as relative ("less susceptible than kaki on its own roots").
BUNDLE / GENERIC VERDICT: the record as written is an umbrella ("Phytophthora (and related) fungi"). The evidence
  resolves it: UC IPM names Phytophthora specifically for persimmon and Armillaria separately; the rootstock
  claims are about wet-soil tolerance (a Phytophthora-shaped claim); TAMU's genus-less "root rot" cannot be
  pinned. VERDICT: pin to *Phytophthora* and join the roster's `phytophthora-root-rot` id; drop "(and related)".
  Armillaria should NOT be folded in -- UC IPM treats it as a distinct listed disease, UCD FNRIC says D. kaki is
  "resistant to ... Armillaria" and D. lotus "tolerant to Armillaria", and its management (root-collar
  excavation, no fungicide, no immune cultivars) is different. Either give it its own entry later or leave it out.
LADDER-RELEVANT FACTS the record does not carry: rootstock is the ONLY resistance lever and it is named by
  species, not cultivar: D. virginiana (HS1389; UCD; TAMU), and D. lotus is the wrong choice on wet ground
  ("does not tolerate poorly drained soils", UCD); mound height "up to 2 feet high" for trees (pn74133); the
  diagnostic cut ("Reddish brown zones, often separated from healthy tissue by a dark line, ... inner bark");
  no "no cure" sentence exists in the documents read -- do not carry one.
PLA-457: none seen.


## Leaf spot and twig dieback [diseases]  -- severity low, type disease
STATUS: WRONG as a bundle. Leaf-spot half: UNSOURCED-FOUND (record names no organism; T1 organisms found).
  Twig-dieback half: WRONG (mis-graded as "minor, cosmetic"; the Southeast literature names it the limiting
  disease) and ANCHOR-MISPOINTED (neither of the record's two anchors mentions dieback).
ORGANISM: LEAF SPOT: *Pseudocercospora diospyricola* per UAEX Plant Health Clinic ("The causal agent is
  identified as Pseudocercospora diospyricola"; the note's fungicide sentence calls it "Cercospora leaf spot in
  persimmon"); *Cercospora* spp. per HS1389 Table 4, alongside Alternaria, Phyllosticta, Ramularia, Botrytis
  and the bacterium Pseudomonas syringae; "several fungi" per TAMU. (The literature name Pseudocercospora kaki
  = Cercospora kaki is journal/CABI only; UAEX's spelling is what the T1 note prints.) TWIG DIEBACK:
  *Botryosphaeria dothidea* (also "B. rhodinina, B. obtusa, B. ribis") per HS1389 Table 4 "Botryosphaeria
  canker", plus a second HS1389 row "Phomopsis spp., Verticillium albo-atrum, Botryosphaeria dothidea" for
  leafless terminal twigs and shoot decline; on NATIVE persimmon, persimmon wilt *Cephalosporium diospyri* per
  ACES and HS1389 (D. kaki and D. lotus "are immune"). Clemson names "Twig dieback" with no organism.
ANCHORS: ncsu_ext https://plants.ces.ncsu.edu/plants/diospyros-kaki/ -- verified 2026-09-04 -- toolbox, one sentence
  > "Insects, Diseases, and Other Plant Problems: Scale, mealybug and leaf spot can occur. Fruit drop can be
  > messy."
  (A sentence, not a title row, so it does assert leaf spot on D. kaki. The words "twig dieback", "anthracnose",
  "Phytophthora" and "root rot" do NOT appear anywhere on the page. This anchor carries NOTHING for the dieback
  half.)
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/persimmon/ -- verified 2026-09-04 -- home (list item)
  > "Leaf Spot Diseases" (linked list item). The full disease list is "Armillaria Root Rot"; "Botrytis Blight,
  > or Gray Mold"; "Leaf Spot Diseases"; "Phytophthora Root and Crown Rot (Diseases)"; "Wood Decay Fungi in
  > Landscape Trees". NO dieback, canker or Botryosphaeria item exists. This anchor carries NOTHING for the
  > dieback half.
ANCHORS: uc_ipm https://ipm.ucanr.edu/home-and-landscape/leaf-spot-diseases/ -- verified 2026-09-04 -- home (generic)
  > "Many fungi" cause leaf spots (organisms named only in captions: Cladosporium iridis, Phyllosticta minima --
  > neither on persimmon)
  > "Remove fallen leaves and debris promptly."
  > "avoid overhead sprinklers and irrigate early in the day so that the foliage dries more quickly"
  > "Generally, fungicide treatment is not warranted."
ANCHORS (not in record, LEAF SPOT): uada_ext
  https://www.uaex.uada.edu/yard-garden/plant-health-clinic/disease-notes/posts/persimmon-leaf-spot.aspx --
  verified 2026-09-04 -- home/diagnostic (parent key `uada_ext` is in the catalog; `uada_ext_fruit_trees` is
  scoped to a different page and must NOT be used for this note)
  > "Symptoms begin as small necrotic spots that develop into angular lesions. Lesions may coalesce to form larger
  > blotches on the leaf. Leaves turn yellow and fall from the tree prematurely."
  > "Infection occurs at shoot expansion, leaf formation, and flowering in the spring."
  > "Severe infections can cause trees to defoliate in late August as the fruit begins to ripen." (consequences
  > listed: "failure for fruit sugar to properly accumulate, and poor fruit ripening, biennial bearing
  > tendencies with low overall yields, and increased vulnerability to freeze damage")
  > "Control can be obtained by applying a fungicide cover spray during full bloom and again 3 to 4 weeks later.
  > Abound and Daconil Weather Stik are both labeled for control of Cercospora leaf spot in persimmon."
  > "Clean up diseased leaves and stems."
ANCHORS (not in record, LEAF SPOT): tamu_agrilife persimmons_2015.pdf -- PYPDF
  > "Although not deadly to adult trees, several fungi cause leaf spot and sometimes affect the fruit as well.
  > Leaf spot can lead to early defoliation, but only severe cases warrant treatment."
ANCHORS (not in record, LEAF SPOT): uf_ifas_edis HS1389 -- verified 2026-09-04
  > "Cercospora: leaf spots and early defoliation." | "Proactive fungicide sprays in early season, and cover
  > sprays in summer in rotation."
ANCHORS (not in record, TWIG DIEBACK): uf_ifas_edis https://ask.ifas.ufl.edu/publication/HS1389 -- verified 2026-09-04
  > "Botryosphaeria canker (Botryosphaeria dothidea, B. rhodinina, B. obtusa, B. ribis)" | "Discoloration of wood
  > and deep, elongated bark scars may be present. This disease is the limiting factor for growing persimmons in
  > Florida and the Deep South. Often this fungus limits the lifetime of Japanese persimmons to about 8 to 12
  > years (or less)." | "There is no good chemical control. Pruning to wide crotch angles, pruning during dry
  > days, disinfecting tools, maintaining good airflow in the canopy, reducing water or nutrient stress to trees,
  > and a good fungicide program are recommended to help reduce the incidence of this fungus."
  > "Phomopsis spp., Verticillium albo-atrum, Botryosphaeria dothidea" | "May cause small leaves and fruit, and
  > terminal twigs that are leafless. May also cause wilting, shoot decline, and bark cracking at limb joints."
ANCHORS (not in record, TWIG DIEBACK): clemson_hgic https://hgic.clemson.edu/factsheet/persimmon/ -- verified 2026-09-04
  > "Persimmon diseases include:" "Fungal leaf spot" "Twig dieback" "Powdery mildew" (bulleted; no organism, no
  > sentence about either)
  > "Chemical control of diseases and insects on large trees is usually not feasible since adequate coverage of
  > the foliage with a pesticide cannot be achieved."
ANCHORS (context, "few problems"): uada_ext_fruit_trees https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx
  -- verified 2026-09-04 (within this scoped key's own page)
  > "They are disease and insect free for the most part, requiring a little thinning in the spring, and water
  > and fertilization." (of oriental persimmons)
  tamu_agrilife: "The tree, its leaves, and its fruit don't have to be sprayed because they have no serious
  insect or disease problems." / "Persimmons are largely free of serious diseases".
  uga_ext: "oriental persimmons are, at this time, relatively free of serious insect problems."
ANCHORS (retired, evidence only, TWIG DIEBACK): ENY-803 -- PYPDF -- the Botryosphaeria + flatheaded borer
  paragraph quoted under Persimmon borer ("deep, elongate scars in the bark ... severe losses of scaffold
  limbs").
RECORD CLAIMS THAT HOLD (leaf spot half): "Circular to angular leaf spots that may yellow and drop leaves"
  (UAEX "angular lesions ... Leaves turn yellow and fall"; TAMU "early defoliation"); "favored by prolonged leaf
  wetness" (UC IPM leaf-spot page irrigation sentence, generic); rake and remove fallen leaves (UC IPM leaf-spot
  page; UAEX "Clean up diseased leaves and stems"); fungicides seldom justified on a home tree (UC IPM leaf-spot
  page "Generally, fungicide treatment is not warranted"; TAMU "only severe cases warrant treatment");
  "persimmon ... has few serious disease problems" (TAMU; UAEX fruit-trees; UGA for insects).
RECORD CLAIMS THAT HOLD (dieback half): only that "dieback of small twigs" occurs (Clemson list item; HS1389
  "terminal twigs that are leafless").
RECORD CLAIMS WITH NO ANCHOR: "Several leaf-spot fungi" (true per HS1389/TAMU but the record names none, and
  UAEX pins one); "keep the canopy open" / "light pruning" for leaf spot (no document prescribes pruning for
  leaf spot; HS1389 prescribes airflow for Botryosphaeria); "Good air movement" (same).
RECORD CLAIMS THAT ARE WRONG: "dieback of small twigs. Usually a minor, cosmetic issue on an otherwise healthy
  persimmon" and "Persimmon is generally regarded as having no serious insect or disease problems, so leaf spot
  is typically a low-impact, weather-driven nuisance" -- as applied to dieback. HS1389: Botryosphaeria canker
  "is the limiting factor for growing persimmons in Florida and the Deep South. Often this fungus limits the
  lifetime of Japanese persimmons to about 8 to 12 years (or less)." and "There is no good chemical control."
  The record folds the region's most consequential disease into a "cosmetic" leaf-spot entry graded severity
  low, with two anchors that do not mention it. Note the leaf-spot half's low grading is also softer than UAEX
  ("Severe infections can cause trees to defoliate in late August as the fruit begins to ripen", with yield and
  freeze consequences), though TAMU and UC IPM support "only severe cases warrant treatment".
BUNDLE / GENERIC VERDICT: TWO problems, not one. (a) LEAF SPOT is a genuine umbrella the literature itself leaves
  multi-organism (HS1389 lists seven fungi and a bacterium; TAMU "several fungi") with one principal named
  organism (UAEX: Pseudocercospora diospyricola / "Cercospora leaf spot in persimmon"; HS1389: Cercospora).
  Supportable as an umbrella entry named for the organism family, severity low-to-medium, weather-driven,
  sanitation-first, fungicide only when severe. (b) TWIG DIEBACK is a PINNED organism on the fruiting species:
  Botryosphaeria canker/dieback (B. dothidea et al.), HS1389, severity HIGH for the humid Southeast, "no good
  chemical control", managed by pruning practice, tool sanitation, airflow and stress reduction, and it is the
  entry point for flatheaded borers (ENY-803). It should be split out as its own disease (or, if the orchestrator
  wants no new problem this batch, the dieback words must at least leave this entry so a low-severity cosmetic
  entry does not describe it). Its only current anchors (NCSU sentence, UC IPM list) do not mention dieback at
  all; the anchors that do are HS1389 (organism + severity) and Clemson (name only). Persimmon wilt
  (Cephalosporium diospyri) is a third, native-persimmon disease and should not be pulled into either half.
LADDER-RELEVANT FACTS the record does not carry: LEAF SPOT: infection window "at shoot expansion, leaf formation,
  and flowering in the spring" (UAEX); the defoliation signal "in late August as the fruit begins to ripen"
  (UAEX); fungicide timing if used, "during full bloom and again 3 to 4 weeks later" (UAEX; commercial products
  named there, do not carry names); "avoid overhead sprinklers and irrigate early in the day" (UC IPM). TWIG
  DIEBACK: overwintering as fruiting bodies on dead tissue and spread by splash, air and pruning tools (VCE
  450-726, generic, not persimmon-specific -- use only if a persimmon document is not required for mechanism);
  HS1389's cultural set (wide crotch angles, prune on dry days, disinfect tools, airflow, avoid water/nutrient
  stress); "no good chemical control" (HS1389) / "no effective fungicide controls for Botryosphaeria dieback"
  (VCE); the borer coupling ("place their eggs along the scars", ENY-803); Clemson's large-tree spraying caveat.
PLA-457: none seen.


## SUMMARY
Counts by STATUS (7 entries): SOURCED-OK 3 (Scale insects; Persimmon psyllid; Root and crown rot -- each with a
flagged sub-claim); SOURCED-OK-with-bundle 1 (Persimmon borer: Sannina anchored, flatheaded half needs its own
home); SOURCED-WEAK 1 (Mealybugs: presence anchored, calyx claim located but unreadable); ANCHOR-MISPOINTED 1
(Anthracnose: clemson_hgic carries nothing, open finding confirmed; biology/management sentences unanchored,
one contradicts HS1389); WRONG 1 (Leaf spot and twig dieback: bundle whose dieback half is Botryosphaeria canker,
"the limiting factor for growing persimmons in Florida and the Deep South", filed as a low-severity cosmetic
issue under two anchors that never mention it). Two load-bearing UF/IFAS documents (ENY-835 persimmon borer,
ENY-803 persimmon insect management) are retired from Ask IFAS (410 / absent) and readable only via the EDIS
archive proxy or a third-party mirror.

Single most important finding: the twig-dieback half of the last entry is Botryosphaeria canker, which HS1389
calls the disease that "limits the lifetime of Japanese persimmons to about 8 to 12 years (or less)" in the
Deep South and for which "There is no good chemical control"; the record grades it low, calls it cosmetic, and
anchors it to an NC State sentence and a UC IPM list that do not contain the word dieback. Split it out.

Verdict on the bundle: two problems. Leaf spot = genuine multi-organism umbrella with a T1-named principal
(Pseudocercospora diospyricola, UAEX; Cercospora, HS1389), supportable at low-to-medium severity. Twig dieback =
pinned Botryosphaeria dothidea et al. (HS1389), high severity in the humid Southeast, own entry.

Verdict on the root-rot genus: Phytophthora, pinned by the UC IPM persimmon page (which lists Armillaria root
rot separately); the wet-soil rootstock claim is carried by HS1389 and UCD FNRIC, TAMU's "root rot" is
genus-less. Join `phytophthora-root-rot`, drop "(and related)", fix "fungi" to "water molds", keep Armillaria out.

## PROPOSED TYPE
* Scale insects -> `insect` (Pseudaulacaspis pentagona, HS1389; soft scales per UGA/ENY-803)
* Mealybugs -> `insect` (Pseudococcidae; only Pseudococcus longispinus is tied to persimmon, UF EENY-666)
* Persimmon psyllid -> `insect` (Trioza diospyri = Baeoalitriozus diospyri, HS1389 / NC State)
* Persimmon borer -> `insect` (Sannina uroceriformis, HS1389 / ENY-835; flatheaded Chrysobothris spp. if a second
  entry is made, UC IPM)
* Anthracnose -> `fungal` (Gloeosporium spp. / Colletotrichum sp., HS1389)
* Root and crown rot -> `fungal` is the nearest value in the allowed set, with the caveat that Phytophthora is an
  oomycete ("technically not true fungi", pn74133); the roster's existing `phytophthora-root-rot` id should carry
  whatever type it already has, and this entry inherits it on join
* Leaf spot (half 1) -> `fungal` (Pseudocercospora diospyricola / Cercospora spp., UAEX / HS1389); note HS1389's
  same row also names a bacterial look-alike, Pseudomonas syringae "bacterial blast"
* Twig dieback / Botryosphaeria canker (half 2, if split) -> `fungal` (Botryosphaeria dothidea, HS1389)
