import json
d = json.load(open('certified-18.json'))
crops = d['crops']
catalog = d['source_catalog']
chill_tbl = d['region_chill_delivered']

# True botanical families (judge knowledge) for the 18, to test the rotation-family dimension
TRUE_FAMILY = {
 'cherry-tomato':'Solanaceae','beefsteak-tomato':'Solanaceae','carrot':'Apiaceae',
 'basil':'Lamiaceae','zucchini-courgette':'Cucurbitaceae','green-beans-bush':'Fabaceae',
 'broccoli':'Brassicaceae','peach':'Rosaceae','apple':'Rosaceae','lemon':'Rutaceae',
 'blueberry':'Ericaceae','lettuce-leaf':'Asteraceae','onion':'Amaryllidaceae',
 'strawberry':'Rosaceae','orange-navel':'Rutaceae','microgreens-mix':'mixed',
 'lavender':'Lamiaceae','zinnia':'Asteraceae',
}

print("=== DIMENSION-BY-DIMENSION FP PROBE on the 18 ===\n")

# D1: rotation.family stated vs true family (free-text contains-match, null-tolerant)
print("D1 rotation-family consistency:")
for c in crops:
    s=c['slug']; rot=c.get('rotation') or {}; stated=rot.get('family')
    true=TRUE_FAMILY[s]
    if stated is None:
        verdict='SKIP (null - legit, 4 expected)'
    elif true=='mixed':
        verdict='OK (blend)' if 'mix' in stated.lower() else f'FLAG?? stated={stated}'
    else:
        verdict='OK' if true.lower() in stated.lower() else f'*** FP RISK: stated has no "{true}" -> {stated}'
    print(f'  {s:22} true={true:14} -> {verdict}')

# D2: numeric sanity bounds (species-agnostic physical bounds only here)
print("\nD2 numeric physical-bounds (pH 3-10, DTM>0, spacing>0, sunlight 0-24):")
import numbers
def pair_ok(v, lo, hi):
    return isinstance(v,list) and len(v)==2 and all(isinstance(x,numbers.Number) for x in v) and v[0]<=v[1] and lo<=v[0] and v[1]<=hi
for c in crops:
    s=c['slug']; issues=[]
    ph=(c.get('ph') or {}).get('preferred_range')
    if ph is not None and not pair_ok(ph,3,10): issues.append(f'ph={ph}')
    dtm=c.get('days_to_maturity')
    if dtm not in (None,[]) and not pair_ok(dtm,1,400): issues.append(f'dtm={dtm}')
    sp=c.get('spacing_inches')
    if sp not in (None,[]) and not pair_ok(sp,0.1,360): issues.append(f'spacing={sp}')
    sun=c.get('sunlight_hours')
    if sun not in (None,[]) and not pair_ok(sun,0,24): issues.append(f'sun={sun}')
    print(f'  {s:22} {"OK" if not issues else "*** "+", ".join(issues)}')

# D3: cited-source-in-catalog + tier (C6 structural half — should be 0 violations)
print("\nD3 every cited source catalogued & T1/T2 (structural half of C6):")
def collect(obj,acc):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=='sources' and isinstance(v,list): acc.update(x for x in v if isinstance(x,str))
            else: collect(v,acc)
    elif isinstance(obj,list):
        for it in obj: collect(it,acc)
for c in crops:
    acc=set(); collect(c,acc)
    uncatalogued=sorted(acc-set(catalog))
    print(f'  {c["slug"]:22} cites {len(acc):2} sources; uncatalogued={uncatalogued if uncatalogued else "none"}')
