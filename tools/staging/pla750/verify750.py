import json,hashlib,os,re,sys,collections,html
S=os.path.dirname(os.path.abspath(__file__))
CACHE='/Users/trevorrawson/plant-dataset/tools/.doc_cache'
def norm(t):
    t=html.unescape(t)
    t=t.replace(' ',' ').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    return re.sub(r'\s+',' ',t).strip().lower()
res=collections.Counter(); fails=[]; rows=[]
for g in 'ABCDE':
    D=json.load(open(f'{S}/research/{g}.json'))
    for slug,v in D.items():
        for i,e in enumerate(v.get('evidence',[])):
            h=hashlib.sha1(e['url'].encode()).hexdigest()
            src=None
            for p in (f'{CACHE}/{h}.txt',f'{S}/fetched/{h}.txt'):
                if os.path.exists(p):
                    t=open(p,errors='ignore').read()
                    if len(t)>=300 and not re.search('FETCHFAIL|Incapsula|Access Denied',t[:400]) and norm(e['quote']) in norm(t):
                        src=p;break
            ok=src is not None
            res[ok]+=1
            rows.append((g,slug,i,ok,'cache' if src and CACHE in src else ('fetched' if src else None)))
            if not ok: fails.append((g,slug,i,e['url'],e['quote'][:160]))
print(res)
for f in fails: print('FAIL',f)
json.dump(rows,open(f'{S}/verify750.json','w'))
