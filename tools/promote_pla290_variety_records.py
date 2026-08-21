#!/usr/bin/env python3
"""PLA-290: the prose-string variety entries become structured records. Base be8a6d1e.

THE SYMPTOM was a Garden On Deck card reading "Golden Self-Blanching: a compact, pale-stalked
self-blanching type that needs little or no manual blanching" as the variety TITLE, with CELERY
as its subtitle. The cause is not the app's parser. Ten crops carry `varieties.recommended` as
"Name: blurb" prose strings, and plant-app's legacy string branch only splits a TRAILING
parenthetical ("Sungold (orange, exceptionally sweet)"), so a colon-format entry has no split
rule at all and the whole sentence becomes the name -- in variety chips, on-deck rows, seedling
detail, and community cards alike.

WHAT THIS DOES
  1. converts 59 entries across 10 crops to `{id, name, note}` records;
  2. removes the copy-paste artifact "Tagetes... " from nasturtium's Jewel series entry, which
     stays a STRING (its trailing-paren shape parses correctly and is not in scope).

THE ID RULE IS A COMPATIBILITY CONSTRAINT, NOT A PREFERENCE. plant-app shipped PLA-291 Part A
before this promote: `varietyFor()` bridges a planting record stored under the old
sentence-slug by finding the variety whose slug is a DASHED PREFIX of it (longest match wins).
So a stored `golden-self-blanching-a-compact-pale-stalked-...` only survives if this dataset
ships the id `golden-self-blanching`. Every id here is therefore checked against

    slugify(WHOLE original entry).startswith(id + '-')

which holds for 59 of 59. That constraint is also what rules out SPLITTING the type-entries:
turning "Nantes types (Scarlet Nantes, Nelson)" into two records would give neither one a slug
that prefixes the stored id, and the planting would resolve to nothing. One record per entry.

AND `id` == `slugify(name)`, EXACTLY. plant-app has two slug rules that must agree or art and
index lookups miss: `varieties.ts` prefers `v.id`, while `scripts/build-guides-data.mjs`
slugifies `v.name` and never reads `v.id`, despite a comment claiming it mirrors the other. All
53 pre-existing records with an explicit id already satisfy id == slugify(name), so the two
rules agree today by luck of convention rather than by construction. This promote preserves
that invariant and the guard suite pins it. The divergence itself is an app-side finding,
raised on PLA-290 rather than fixed here.

THE SPLIT RULE, and the five entries that needed a judgment instead
  name = the text before the first ": ", verbatim; note = the rest, capitalized, with a
  terminal period. Parentheses stay in the NAME when they carry a binomial or an alternate
  name for the same plant -- the established dataset shape ("Spearmint (Mentha spicata)",
  "Lacinato (Dinosaur / Tuscan)"). They move to the NOTE when they list example cultivars OF a
  type, because that is detail rather than identity:

    beet       Monogerm types (such as Moneta)              -> "Monogerm types"
    carrot     Nantes types (Scarlet Nantes, Nelson)        -> "Nantes types"
    carrot     Round and finger types (Paris Market, Romeo) -> "Round and finger types"
    radish     Daikon and Asian winter types (April Cross, Summer Cross)
                                                            -> "Daikon and Asian winter types"
    lemongrass East Indian lemongrass (Cymbopogon flexuosus, also called Cochin or Malabar
               grass)                       -> "East Indian lemongrass (Cymbopogon flexuosus)"

  In all five the displaced words are preserved in the note, not dropped. A token-level check
  confirms every word of all 59 originals survives into name+note; the only exception is beet's
  "such as", which becomes "Moneta is a common example."

NO days_to_maturity IS INVENTED. Eight sweet-potato and two turnip notes carry a DTM as prose
("about 90 to 100 days"). These entries were never sourced for a DTM and the ranges cannot be
narrowed to the integer the field takes without inventing precision, so they stay prose and the
field stays absent. The app already handles a null dtm.

Guard suite: tools/test_promote_pla290_variety_records.py
Mutation harness: tools/mutate_pla290_variety_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla290_variety_records.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = 'be8a6d1e10c014906ad66aff03fc307525f6f22d9045ff28cb850ffecfc686f4'

CROPS = ('beet', 'carrot', 'celery', 'chamomile', 'lemongrass', 'parsnip', 'potato', 'radish',
         'sweet-potato', 'turnip')

# nasturtium keeps its STRING shape; only the stray genus name leaves.
NASTURTIUM = 'nasturtium'
NAST_INDEX = 0
NAST_PREV = ('Jewel series (bush, Tagetes... Tropaeolum majus; compact mounding ~12 in, '
             'semi-double flowers held above the leaves, classic bedding and container type)')
NAST_NEW = ('Jewel series (bush, Tropaeolum majus; compact mounding ~12 in, semi-double '
            'flowers held above the leaves, classic bedding and container type)')


def slugify_variety(name):
    """plant-app's rule, character for character (varieties.ts + build-guides-data.mjs):
    lowercase, drop straight and curly apostrophes plus ! and . , kebab-case the rest."""
    s = re.sub(r"['’!.]", '', name.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


PREV_ENTRIES = {
    'beet': [
        'Detroit Dark Red: the classic all-purpose round red beet, dependable for roots and greens',
        'Early Wonder: fast-maturing, with especially good edible tops',
        "Bull's Blood: grown mainly for its deep-red ornamental and edible leaves",
        'Chioggia: Italian heirloom with red-and-white candy-stripe rings inside',
        'Touchstone Gold and other golden types: sweet, mild, with non-bleeding yellow flesh',
        'Cylindra (Formanova): long, cylindrical roots that slice into uniform rounds',
        'Monogerm types (such as Moneta): one seedling per seed, so little or no thinning',
    ],
    'carrot': [
        'Nantes types (Scarlet Nantes, Nelson): sweet, cylindrical, and the most forgiving choice for a first crop',
        'Danvers: sturdy and tapered, tolerates heavier soil better than most',
        'Chantenay: short and broad, a good pick for shallow or heavy ground',
        'Imperator: long and slender, needs deep, loose, stone-free soil to size up',
        'Round and finger types (Paris Market, Romeo): best for containers and clay',
    ],
    'celery': [
        'Tall Utah 52-70 and its strains: the standard green, self-blanching home and market type, crisp and stringless when grown well',
        'Tango: vigorous, relatively fast and more forgiving than most, a good first choice',
        'Conquistador: more tolerant of heat and less-than-ideal conditions, easier than classic types',
        'Golden Self-Blanching: a compact, pale-stalked self-blanching type that needs little or no manual blanching',
        'Giant Pascal and other Pascal types: traditional green trench-blanched celery, larger but more demanding',
    ],
    'chamomile': [
        'German chamomile (Matricaria chamomilla / recutita): the common annual tea chamomile; erect to about 2 ft, self-seeding',
        "'Bodegold' (German): an upright strain that blooms a few weeks earlier and heavier, with larger flowers, good for tea and easy picking",
        "'Bona' (German): a productive strain grown for tea flowers",
        'Roman chamomile (Chamaemelum nobile): a distinct low, mat-forming perennial groundcover, not an upright tea annual',
        "'Treneague' (Roman): a non-flowering perennial selection grown as a fragrant chamomile lawn",
        "'Flore Pleno' (Roman): a perennial with showy double, cream-white flowers",
    ],
    'lemongrass': [
        'West Indian lemongrass (Cymbopogon citratus): the common culinary lemongrass, of Malaysian origin, grown for its thick, tender edible stalks; this is the type sold as grocery-store lemongrass and the one to grow for cooking',
        'East Indian lemongrass (Cymbopogon flexuosus, also called Cochin or Malabar grass): native to India, Sri Lanka, Burma, and Thailand; also culinary and a major source of lemongrass essential oil, with somewhat more slender stalks',
        'Citronella grass (Cymbopogon nardus / C. winterianus): a related but non-culinary species grown for citronella oil and as an ornamental insect-repellent plant; do not confuse it with edible lemongrass for cooking',
    ],
    'parsnip': [
        'Harris Model: a long-standing white, smooth-skinned standard with good length and flavor',
        'Hollow Crown: an old open-pollinated heirloom with long, broad-shouldered roots for deep soil',
        'All American: a dependable, uniform main-crop type',
        'Gladiator (F1): a vigorous hybrid with good canker tolerance and smooth roots',
        'Javelin (F1): a uniform hybrid with some canker resistance',
        'Cobham Improved Marrow: a sweet variety with useful canker resistance',
        'Lancer / Avonresister: shorter, smooth types, with Avonresister bred for canker resistance',
    ],
    'potato': [
        'Yukon Gold: yellow-fleshed, all-purpose early-to-mid main crop, widely adapted and a reliable first choice',
        'Red Pontiac: red-skinned, vigorous, tolerant of heavier soils, a strong pick in the South',
        'Kennebec: high-yielding mid-to-late white, with useful late blight tolerance',
        'Russet Burbank: classic late russet for baking and frying, with some scab tolerance',
        'Irish Cobbler: heirloom early white, quick to a first dig of new potatoes',
    ],
    'radish': [
        'Cherry Belle: fast, round, mild red garden radish, an easy and forgiving first choice',
        'Scarlet Globe (Early Scarlet Globe): classic round red, quick and reliable',
        'French Breakfast: oblong red-and-white type, mild and crisp',
        'White Icicle: long, tapered white garden radish',
        'Daikon and Asian winter types (April Cross, Summer Cross): large, long, milder roots sown in late summer for fall, needing deep, loose soil',
    ],
    'sweet-potato': [
        'Beauregard: orange-fleshed, fast and high-yielding (about 90 to 100 days), widely adapted and a reliable first choice',
        'Covington: orange, rose-skinned, excellent storage and root-knot nematode resistance (about 95 to 110 days)',
        'Centennial: classic orange, root-knot nematode and wireworm tolerant, good for shorter seasons (about 90 to 110 days)',
        'Georgia Jet: very fast (about 90 to 100 days), a top pick for short northern seasons',
        'Jewel: high-yielding orange keeper, longer season (about 120 to 135 days)',
        'Vardaman: compact bush habit, space-saving and good for containers (about 100 days)',
        'Murasaki and other Japanese types: purple skin, pale flesh, nutty flavor, nematode resistant (about 100 to 120 days)',
        "O'Henry: creamy white-fleshed sport of Beauregard",
    ],
    'turnip': [
        'Purple Top White Globe: the classic all-purpose turnip, round with a purple-and-white root and good greens, about 50 to 55 days',
        'Hakurei: a sweet, mild white salad turnip (F1) eaten raw or cooked, fast at about 38 days, with tender greens',
        'Tokyo Cross and other Tokyo types: quick, uniform white hybrids good for baby and salad turnips',
        'Shogoin: a Japanese type grown for abundant, mild greens as well as a white root',
        'Seven Top: a greens-only turnip grown for the leaves, with no usable root',
        'Golden Ball (Golden Globe): an heirloom with sweet, mild yellow flesh',
        'Scarlet Queen: a red-skinned, white-fleshed round type with a crisp, mild flavor',
        'White Lady and Just Right: smooth white hybrids, dual-purpose for roots and greens',
    ],
}

RECORDS = {
    'beet': [
        {
            'id': 'detroit-dark-red',
            'name': 'Detroit Dark Red',
            'note': 'The classic all-purpose round red beet, dependable for roots and greens.',
        },
        {
            'id': 'early-wonder',
            'name': 'Early Wonder',
            'note': 'Fast-maturing, with especially good edible tops.',
        },
        {
            'id': 'bulls-blood',
            'name': "Bull's Blood",
            'note': 'Grown mainly for its deep-red ornamental and edible leaves.',
        },
        {
            'id': 'chioggia',
            'name': 'Chioggia',
            'note': 'Italian heirloom with red-and-white candy-stripe rings inside.',
        },
        {
            'id': 'touchstone-gold-and-other-golden-types',
            'name': 'Touchstone Gold and other golden types',
            'note': 'Sweet, mild, with non-bleeding yellow flesh.',
        },
        {
            'id': 'cylindra-formanova',
            'name': 'Cylindra (Formanova)',
            'note': 'Long, cylindrical roots that slice into uniform rounds.',
        },
        {
            'id': 'monogerm-types',
            'name': 'Monogerm types',
            'note': 'One seedling per seed, so little or no thinning. Moneta is a common example.',
        },
    ],
    'carrot': [
        {
            'id': 'nantes-types',
            'name': 'Nantes types',
            'note': 'Sweet, cylindrical, and the most forgiving choice for a first crop. Scarlet Nantes and Nelson are common examples.',
        },
        {
            'id': 'danvers',
            'name': 'Danvers',
            'note': 'Sturdy and tapered, tolerates heavier soil better than most.',
        },
        {
            'id': 'chantenay',
            'name': 'Chantenay',
            'note': 'Short and broad, a good pick for shallow or heavy ground.',
        },
        {
            'id': 'imperator',
            'name': 'Imperator',
            'note': 'Long and slender, needs deep, loose, stone-free soil to size up.',
        },
        {
            'id': 'round-and-finger-types',
            'name': 'Round and finger types',
            'note': 'Best for containers and clay. Paris Market and Romeo are common examples.',
        },
    ],
    'celery': [
        {
            'id': 'tall-utah-52-70-and-its-strains',
            'name': 'Tall Utah 52-70 and its strains',
            'note': 'The standard green, self-blanching home and market type, crisp and stringless when grown well.',
        },
        {
            'id': 'tango',
            'name': 'Tango',
            'note': 'Vigorous, relatively fast and more forgiving than most, a good first choice.',
        },
        {
            'id': 'conquistador',
            'name': 'Conquistador',
            'note': 'More tolerant of heat and less-than-ideal conditions, easier than classic types.',
        },
        {
            'id': 'golden-self-blanching',
            'name': 'Golden Self-Blanching',
            'note': 'A compact, pale-stalked self-blanching type that needs little or no manual blanching.',
        },
        {
            'id': 'giant-pascal-and-other-pascal-types',
            'name': 'Giant Pascal and other Pascal types',
            'note': 'Traditional green trench-blanched celery, larger but more demanding.',
        },
    ],
    'chamomile': [
        {
            'id': 'german-chamomile-matricaria-chamomilla-recutita',
            'name': 'German chamomile (Matricaria chamomilla / recutita)',
            'note': 'The common annual tea chamomile; erect to about 2 ft, self-seeding.',
        },
        {
            'id': 'bodegold-german',
            'name': "'Bodegold' (German)",
            'note': 'An upright strain that blooms a few weeks earlier and heavier, with larger flowers, good for tea and easy picking.',
        },
        {
            'id': 'bona-german',
            'name': "'Bona' (German)",
            'note': 'A productive strain grown for tea flowers.',
        },
        {
            'id': 'roman-chamomile-chamaemelum-nobile',
            'name': 'Roman chamomile (Chamaemelum nobile)',
            'note': 'A distinct low, mat-forming perennial groundcover, not an upright tea annual.',
        },
        {
            'id': 'treneague-roman',
            'name': "'Treneague' (Roman)",
            'note': 'A non-flowering perennial selection grown as a fragrant chamomile lawn.',
        },
        {
            'id': 'flore-pleno-roman',
            'name': "'Flore Pleno' (Roman)",
            'note': 'A perennial with showy double, cream-white flowers.',
        },
    ],
    'lemongrass': [
        {
            'id': 'west-indian-lemongrass-cymbopogon-citratus',
            'name': 'West Indian lemongrass (Cymbopogon citratus)',
            'note': 'The common culinary lemongrass, of Malaysian origin, grown for its thick, tender edible stalks; this is the type sold as grocery-store lemongrass and the one to grow for cooking.',
        },
        {
            'id': 'east-indian-lemongrass-cymbopogon-flexuosus',
            'name': 'East Indian lemongrass (Cymbopogon flexuosus)',
            'note': 'Also called Cochin or Malabar grass. Native to India, Sri Lanka, Burma, and Thailand; also culinary and a major source of lemongrass essential oil, with somewhat more slender stalks.',
        },
        {
            'id': 'citronella-grass-cymbopogon-nardus-c-winterianus',
            'name': 'Citronella grass (Cymbopogon nardus / C. winterianus)',
            'note': 'A related but non-culinary species grown for citronella oil and as an ornamental insect-repellent plant; do not confuse it with edible lemongrass for cooking.',
        },
    ],
    'parsnip': [
        {
            'id': 'harris-model',
            'name': 'Harris Model',
            'note': 'A long-standing white, smooth-skinned standard with good length and flavor.',
        },
        {
            'id': 'hollow-crown',
            'name': 'Hollow Crown',
            'note': 'An old open-pollinated heirloom with long, broad-shouldered roots for deep soil.',
        },
        {
            'id': 'all-american',
            'name': 'All American',
            'note': 'A dependable, uniform main-crop type.',
        },
        {
            'id': 'gladiator-f1',
            'name': 'Gladiator (F1)',
            'note': 'A vigorous hybrid with good canker tolerance and smooth roots.',
        },
        {
            'id': 'javelin-f1',
            'name': 'Javelin (F1)',
            'note': 'A uniform hybrid with some canker resistance.',
        },
        {
            'id': 'cobham-improved-marrow',
            'name': 'Cobham Improved Marrow',
            'note': 'A sweet variety with useful canker resistance.',
        },
        {
            'id': 'lancer-avonresister',
            'name': 'Lancer / Avonresister',
            'note': 'Shorter, smooth types, with Avonresister bred for canker resistance.',
        },
    ],
    'potato': [
        {
            'id': 'yukon-gold',
            'name': 'Yukon Gold',
            'note': 'Yellow-fleshed, all-purpose early-to-mid main crop, widely adapted and a reliable first choice.',
        },
        {
            'id': 'red-pontiac',
            'name': 'Red Pontiac',
            'note': 'Red-skinned, vigorous, tolerant of heavier soils, a strong pick in the South.',
        },
        {
            'id': 'kennebec',
            'name': 'Kennebec',
            'note': 'High-yielding mid-to-late white, with useful late blight tolerance.',
        },
        {
            'id': 'russet-burbank',
            'name': 'Russet Burbank',
            'note': 'Classic late russet for baking and frying, with some scab tolerance.',
        },
        {
            'id': 'irish-cobbler',
            'name': 'Irish Cobbler',
            'note': 'Heirloom early white, quick to a first dig of new potatoes.',
        },
    ],
    'radish': [
        {
            'id': 'cherry-belle',
            'name': 'Cherry Belle',
            'note': 'Fast, round, mild red garden radish, an easy and forgiving first choice.',
        },
        {
            'id': 'scarlet-globe-early-scarlet-globe',
            'name': 'Scarlet Globe (Early Scarlet Globe)',
            'note': 'Classic round red, quick and reliable.',
        },
        {
            'id': 'french-breakfast',
            'name': 'French Breakfast',
            'note': 'Oblong red-and-white type, mild and crisp.',
        },
        {
            'id': 'white-icicle',
            'name': 'White Icicle',
            'note': 'Long, tapered white garden radish.',
        },
        {
            'id': 'daikon-and-asian-winter-types',
            'name': 'Daikon and Asian winter types',
            'note': 'Large, long, milder roots sown in late summer for fall, needing deep, loose soil. April Cross and Summer Cross are common examples.',
        },
    ],
    'sweet-potato': [
        {
            'id': 'beauregard',
            'name': 'Beauregard',
            'note': 'Orange-fleshed, fast and high-yielding (about 90 to 100 days), widely adapted and a reliable first choice.',
        },
        {
            'id': 'covington',
            'name': 'Covington',
            'note': 'Orange, rose-skinned, excellent storage and root-knot nematode resistance (about 95 to 110 days).',
        },
        {
            'id': 'centennial',
            'name': 'Centennial',
            'note': 'Classic orange, root-knot nematode and wireworm tolerant, good for shorter seasons (about 90 to 110 days).',
        },
        {
            'id': 'georgia-jet',
            'name': 'Georgia Jet',
            'note': 'Very fast (about 90 to 100 days), a top pick for short northern seasons.',
        },
        {
            'id': 'jewel',
            'name': 'Jewel',
            'note': 'High-yielding orange keeper, longer season (about 120 to 135 days).',
        },
        {
            'id': 'vardaman',
            'name': 'Vardaman',
            'note': 'Compact bush habit, space-saving and good for containers (about 100 days).',
        },
        {
            'id': 'murasaki-and-other-japanese-types',
            'name': 'Murasaki and other Japanese types',
            'note': 'Purple skin, pale flesh, nutty flavor, nematode resistant (about 100 to 120 days).',
        },
        {
            'id': 'ohenry',
            'name': "O'Henry",
            'note': 'Creamy white-fleshed sport of Beauregard.',
        },
    ],
    'turnip': [
        {
            'id': 'purple-top-white-globe',
            'name': 'Purple Top White Globe',
            'note': 'The classic all-purpose turnip, round with a purple-and-white root and good greens, about 50 to 55 days.',
        },
        {
            'id': 'hakurei',
            'name': 'Hakurei',
            'note': 'A sweet, mild white salad turnip (F1) eaten raw or cooked, fast at about 38 days, with tender greens.',
        },
        {
            'id': 'tokyo-cross-and-other-tokyo-types',
            'name': 'Tokyo Cross and other Tokyo types',
            'note': 'Quick, uniform white hybrids good for baby and salad turnips.',
        },
        {
            'id': 'shogoin',
            'name': 'Shogoin',
            'note': 'A Japanese type grown for abundant, mild greens as well as a white root.',
        },
        {
            'id': 'seven-top',
            'name': 'Seven Top',
            'note': 'A greens-only turnip grown for the leaves, with no usable root.',
        },
        {
            'id': 'golden-ball-golden-globe',
            'name': 'Golden Ball (Golden Globe)',
            'note': 'An heirloom with sweet, mild yellow flesh.',
        },
        {
            'id': 'scarlet-queen',
            'name': 'Scarlet Queen',
            'note': 'A red-skinned, white-fleshed round type with a crisp, mild flavor.',
        },
        {
            'id': 'white-lady-and-just-right',
            'name': 'White Lady and Just Right',
            'note': 'Smooth white hybrids, dual-purpose for roots and greens.',
        },
    ],
}

def apply_to(data):
    """The whole transform, as one function, so the guard suite exercises the code the promote
    runs rather than a re-implementation of it."""
    by = {c['slug']: c for c in data['crops']}
    for slug in CROPS:
        by[slug]['varieties']['recommended'] = [dict(r) for r in RECORDS[slug]]
    by[NASTURTIUM]['varieties']['recommended'][NAST_INDEX] = NAST_NEW
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

    raw = open(canonical, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print(f'ABORT: base SHA mismatch\n  expected {args.expect_sha}\n  found    {sha}',
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    by = {c['slug']: c for c in data['crops']}

    # Refuse text this promote was not written against. An entry someone else has already
    # restructured is a different decision, not this one.
    for slug in CROPS:
        crop = by.get(slug)
        if crop is None:
            print(f'ABORT: no crop {slug!r}', file=sys.stderr)
            return 1
        found = (crop.get('varieties') or {}).get('recommended')
        if found != PREV_ENTRIES[slug]:
            print(f'ABORT: {slug}.varieties.recommended is not the prose list this promote was '
                  f'written against\n  found: {found!r}', file=sys.stderr)
            return 1

    nast = (by.get(NASTURTIUM) or {}).get('varieties', {}).get('recommended') or []
    if len(nast) <= NAST_INDEX or nast[NAST_INDEX] != NAST_PREV:
        print(f'ABORT: {NASTURTIUM}.varieties.recommended[{NAST_INDEX}] is not the entry this '
              f'promote was written against', file=sys.stderr)
        return 1

    # The compatibility constraint, re-checked at run time rather than trusted from authoring.
    for slug in CROPS:
        for prev_entry, rec in zip(PREV_ENTRIES[slug], RECORDS[slug]):
            legacy = slugify_variety(prev_entry)
            if not legacy.startswith(rec['id'] + '-'):
                print(f'ABORT: {slug}/{rec["id"]} would strand the stored id {legacy!r}',
                      file=sys.stderr)
                return 1
            if rec['id'] != slugify_variety(rec['name']):
                print(f'ABORT: {slug}/{rec["id"]} != slugify({rec["name"]!r})', file=sys.stderr)
                return 1

    apply_to(data)

    n = sum(len(RECORDS[s]) for s in CROPS)
    print(f'converted {n} prose entries to {{id, name, note}} records across {len(CROPS)} crops')
    for slug in CROPS:
        print(f'  {slug:<13} {len(RECORDS[slug])} entries')
    print(f'removed the "Tagetes... " artifact from {NASTURTIUM}.varieties.recommended'
          f'[{NAST_INDEX}] (stays a string)')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(canonical, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
