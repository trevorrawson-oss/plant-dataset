# PLA-750 heat-hold evidence research: shared instructions

You are a research agent for the plant dataset (repo ~/plant-dataset). You are STRICTLY READ-ONLY on the repo: never edit, write, or git anything inside /Users/trevorrawson/plant-dataset. Write only under the scratchpad:
SCRATCH=/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/bea45699-3b84-405d-a80f-f801d1d6ea92/scratchpad

## What the app does (context)
The app holds a crop's NEXT SUCCESSION SOWING when the 10-day forecast daily HIGH (air temperature) exceeds the crop's `heat_threshold_f` (fallback 85°F if null) and `succession_policy.pause_in_heat` is true. Trevor's rule: a crop holds only when research supports the hold, and the "held" message explains why from a sourced, crop-specific heat reason. Accuracy over velocity: claim only what a source says. A gap is recorded as a gap, NEVER filled by inference or by "general knowledge".

Note the dataset's `heat_threshold_f` was defined (docs/climate_thresholds_contract.md) as the MATURE-PLANT heat-stress number (bolting / quality / crown failure), explicitly NOT a germination number. So for each crop, keep these mechanisms separate:
  G = germination: soil-temperature optimum, upper limit, "poor/no germination above X", "do not sow in midsummer heat because seed won't come up"
  E = seedling / transplant establishment in heat
  M = mature-plant heat effect: bolting, bitterness, tough/coarse, buttoning, poor heading, blossom/pod set failure, with any temperature given
  S = explicit advice about WHEN TO SOW relative to heat (e.g. "stop sowing when temperatures rise", "sow fall crop after heat breaks")
Also record whether a source says the crop TOLERATES heat (evidence AGAINST a hold).

## Source rules
- Prefer T1: US land-grant university extension (.edu extension sites, UC ANR / UC IPM, Cornell, Clemson HGIC, UMN, UMD, USU, NC State, Texas A&M AgriLife, UF/IFAS, OSU, WSU, Purdue, Iowa State, etc.), USDA, peer-reviewed. Seed company pages (Johnny's etc.) are T2: record them, but mark tier T2.
- START with what the dataset already cites. The crop's record lists anchoring URLs; cached text for a URL is at /Users/trevorrawson/plant-dataset/tools/.doc_cache/<sha1(url)>.txt (sha1 of the exact URL string, hex). Skip cached files that are under 300 bytes or start with FETCHFAIL / Incapsula / Access Denied. A per-crop brief (current values, existing tips, existing heat prose and its sources) is at $SCRATCH/heat_brief.json, and a pre-mined list of candidate heat sentences from cached cited docs is at $SCRATCH/heat_mine.json (noisy: verify each yourself).
- Then search the web (WebSearch / WebFetch) for gaps.
- MULTI-CROP PAGES (e.g. Clemson "carrot-beet-radish-parsnip", Wisconsin/UMN combined guides, planting-temperature charts): a quote counts for a crop ONLY if it sits in that crop's section or names the crop. Record the section heading.
- Every quote must be VERBATIM, copied character-for-character from the page text, one or two sentences. No paraphrase, no ellipsis-joined fragments.
- SAVE THE BYTES: for every web page you quote that is not already in tools/.doc_cache, save the page text you read to $SCRATCH/fetched/<sha1(url)>.txt (use curl with a browser user-agent, e.g. `curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36" URL`, then strip tags with python if needed; for PDFs save the pdftotext/pypdf text). An independent verifier will grep your quote in those bytes (whitespace-normalized); a quote it cannot find will be thrown out.
- Never invent a URL. If a fetch fails (403/WAF), say so; try the other user agent once.

## Output
Write ONE JSON file: $SCRATCH/research/<GROUP>.json, shaped:
{
 "<slug>": {
   "evidence": [ {"mech": "G|E|M|S|TOL", "url": "...", "source_name": "Clemson HGIC", "tier": "T1|T2", "section": "heading or null", "quote": "verbatim", "temp_f": [low,high] or number or null, "in_dataset_cache": true|false} ],
   "hold_supported": "yes|no|weak|unsourced",
   "hold_basis": "G|M|G+M|... one line: what mechanism actually justifies pausing a SOWING for a hot 10-day forecast",
   "proposed_pause_in_heat": true|false|null,
   "proposed_threshold_f": number or null,
   "threshold_quote_ref": index into evidence of the quote the number rests on, or null,
   "threshold_note": "how the number follows from the quote (e.g. 'USU: germination reduced above 80°F' -> 80) and any tension with the current value",
   "reason_tip_candidate": {"field": "tips_by_stage.germination | other (name it)", "draft_seasoned": "...", "draft_beginner": "...", "evidence_refs": [indices]} or null,
   "gaps": ["what you looked for and did not find"],
   "notes": "anything Trevor needs to rule on"
 }
}
Draft tips: American English, no em dashes (use commas, colons, semicolons, periods), temperatures as °F, a draft claims nothing beyond its quotes. Beginner register = everyday words.
Finish with a short summary message: per crop one line (hold supported? proposed threshold? strongest quote's source).
