# chives -- Phase C evidence packet (item 1)

Canonical read: `crops_data_final.json` sha256 b331e5f2c993..., HEAD 1250f3a (main). Quotes are `norm_text` form (lowercased, NFKC) of the hashed bytes; every listed sha256 was recomputed over the bytes and matches its file name.

## Hashed pages cited on chives
| source | url | sha256 |
|---|---|---|
| NCSU Plant Toolbox | https://plants.ces.ncsu.edu/plants/allium-schoenoprasum/ | 933eb2c446e453666776892b124b97708e749999ee8f01c3aab6dceb553a4f6e |
| UW-Madison (Wisc) | https://hort.extension.wisc.edu/articles/chives-allium-schoenoprasum/ | e4675fb89284b8bd1228d56443e70f41a68288b886fe4c103ca2a72052a300d6 |
| UMN | https://extension.umn.edu/vegetables/growing-chives | a0ec06f1abf760b79817dfe3c8dade3d6ac890241b029e1721d65bb018b8afde |
| Illinois | https://extension.illinois.edu/herbs/chives | cacc0c830a2886ca0b9812c18e66b02f53c7662f52dc801732325d746fae4418 |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 |
| OSU planting chart | https://ir.library.oregonstate.edu/downloads/v979v342w | f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33 |
| WSU | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | 7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34 |

Cited, NOT hashed (cannot support a claim this session): agrilifeextension.tamu.edu; blogs.ifas.ufl.edu/pascoco/2024/04/16/spice-up-your-life-chives/; extension.arizona.edu (+ az2061 pdf); extension.msstate.edu/lawn-and-garden; extension.uga.edu C943; extension.umaine.edu/gardening/; extension.umd.edu/resource/allium-onion-leafminer; extension.umn.edu/vegetables/growing-onions; extension.umn.edu/yard-and-garden-insects/root-maggots; extension.usu.edu (frost dates pdf, onions-in-the-garden, planting dates); hgic.clemson.edu/factsheet/herbs/; ipm.ucanr.edu onion-and-garlic (botrytis-leafspot, downy-mildew, maggots, rust, white-rot); mg.ucanr.edu; naes.agnt.unr.edu 2002-3280.pdf; pnwhandbooks.org (garlic rust, onion botrytis); pubs.nmsu.edu; ucanr.edu; aspca.org chives; canr.msu.edu growing_chives; ctahr.hawaii.edu; lsuagcenter.com; ndsu.edu; uaex.uada.edu; unlv.edu planting calendar.

## Context: the entry and the crop's height field
- `varieties.recommended[0]` = `{"name": "Common Chives", "days_to_maturity": 80, "note": ..., "container_suitable": true}` -- no `sources` / `anchoring_urls` on the entry. Name is "Common Chives" and the note opens "The standard Allium schoenoprasum", so it is the **species/common type** (not a cultivar). Ruling branch: the note follows NCSU (1 to 1.5 ft) = `mature_height_ft` [1, 1.5].
- `mature_height_ft` = [1, 1.5]; EVIDENCE (pla10_promote3/EVIDENCE.tsv): `chives mature_dimensions mature_height_ft [1,1.5] ncsu_ext https://plants.ces.ncsu.edu/plants/allium-schoenoprasum/ 933eb2c4... "height: 1 ft. 0 in. - 1 ft. 6 in. width: 1 ft. 0 in. - 1 ft. 5 in."`

## Leaf: `varieties.recommended[0].note`
CURRENT (verbatim):
> The standard Allium schoenoprasum: fine, hollow, grass-like leaves in tidy clumps 8 to 14 inches tall, with edible pink to pale purple pom-pom flowers in late spring. Mild onion flavor, extremely hardy, and the workhorse kitchen chive.

| # | claim | verdict | hashed sentence(s) |
|---|---|---|---|
| 1 | it is the standard / species Allium schoenoprasum | MAPPED | Wisc e4675fb8: "this species is a hardy herbaceous perennial that grows in dense clumps of slender bulbs, each bulb producing hollow tubular leaves 8 to 20 inches long." (page title is "chives, allium schoenoprasum"); NCSU 933eb2c4 is the A. schoenoprasum species page |
| 2 | leaves are fine | MAPPED | Illinois cacc0c83: "they grow in clumps from underground bulbs and produce round, hollow leaves that are much finer than onion."; NCSU 933eb2c4 (attribute): "texture: fine" |
| 3 | leaves are hollow | MAPPED | UMN a0ec06f1: "its grass-like hollow leaves have a mild onion flavor and are common in salads and dips."; Illinois (above); NCSU 933eb2c4 (attribute): "leaf description: hollow, fragrant, upright grass-like leaves forming clumps" |
| 4 | leaves are grass-like | MAPPED | UMN a0ec06f1 (above); NCSU (above); Wisc e4675fb8: "the grass-like foliage provides good contrast in texture and form to mounding perennials with coarser foliage, while the attractive flowers offer nice color when in bloom." |
| 5 | grows in clumps | MAPPED | UMN a0ec06f1: "lavender flowers, a clump-forming habit and cold hardiness make this plant an appealing garden perennial."; NCSU attribute "habit/form: clumping"; Wisc "grows in dense clumps of slender bulbs" |
| 6 | clumps are "tidy" | NO HASHED CITED PAGE STATES IT | -- |
| 7 | **8 to 14 inches tall** | NO HASHED CITED PAGE STATES IT | Ruled to follow NCSU: NCSU 933eb2c4: "dimensions: height: 1 ft. 0 in. - 1 ft. 6 in. width: 1 ft. 0 in. - 1 ft. 5 in." Other figures on hashed pages (context, none is 8-14): Illinois "they are a hardy, drought-tolerant perennial growing to about 10-12 inches tall."; Wisc "...hollow tubular leaves 8 to 20 inches long." (leaf length, not plant height); NCSU "while prized for their edible qualities, their clusters of one-inch purple flowers rising up to 18 inches above ground have value as an ornamental flower."; NCSU attribute "stem description: hollow, tubular green stems up to 20 inches tall" |
| 8 | flowers are edible | MAPPED | NCSU 933eb2c4: "chives have edible flowers and leaves used for flavoring with eggs, soups, salads, butter, cheese, dips and spreads."; UMN a0ec06f1: "these are edible, and you can use them in salads and flower arrangements."; Wisc: "culinary use of chives chives can be harvested at any time and the flowers are edible, too." |
| 9 | flowers are pink to pale purple | MAPPED | Wisc e4675fb8: "the pink to pale purple round globes are composed of many small, tightly packed, star-shaped florets ." (other hashed colors, context: UMN "lavender flowers..."; Illinois "in mid-summer, they produce round, pink flowers similar in appearance to clover."; NCSU "flower color: purple/lavender"; NCSU "flower description: clusters of 1/2-3/4 inch star-shaped pale purple flowers with 6 petals bloom april-may on hollow tubular scapes.") |
| 10 | flowers are "pom-pom" (shape) | the word is NOT on any hashed cited page; the round-globe shape is MAPPED | Wisc: "the pink to pale purple round globes are composed of many small, tightly packed, star-shaped florets ."; UMN: "the small puffs of flowers begin to bloom in late may or june."; Illinois: "round, pink flowers similar in appearance to clover" |
| 11 | **bloom in late spring** | MAPPED, but hashed pages DISAGREE on timing -- all quoted | UMN a0ec06f1: "the small puffs of flowers begin to bloom in late may or june."; Wisc e4675fb8: "chives bloom in mid spring to early summer."; NCSU 933eb2c4: "flower description: clusters of 1/2-3/4 inch star-shaped pale purple flowers with 6 petals bloom april-may on hollow tubular scapes." and attribute "flower bloom time: spring summer"; **Illinois cacc0c83 (contrary): "in mid-summer, they produce round, pink flowers similar in appearance to clover."** |
| 12 | mild onion flavor | MAPPED | UMN: "its grass-like hollow leaves have a mild onion flavor and are common in salads and dips."; Wisc: "today the leaves are typically used as a culinary herb with a mild onion flavor."; Illinois: "flavor is much milder and more subtle than other members of the onion family." |
| 13 | hardy | MAPPED | Wisc: "this plant, hardy to zone 4a , is related to garlic chives ( a."; Illinois: "they are a hardy, drought-tolerant perennial growing to about 10-12 inches tall."; UMN: "...a clump-forming habit and cold hardiness make this plant an appealing garden perennial." |
| 14 | "extremely" hardy (intensifier) | NO HASHED CITED PAGE STATES IT | -- |
| 15 | "the workhorse kitchen chive" | NO HASHED CITED PAGE STATES IT | -- |

Notes for the writer:
- Claim 7 is the ruled change. Claim 11: the UMN/Wisc/NCSU sentences support spring bloom; Illinois says mid-summer. "late spring" is closest to UMN's "late may or june".
- `container_suitable` and `days_to_maturity` (80) on the entry are not part of the note and were not examined.
