import json, math
FIELDS = {'age':(18,100),'income':(0,10**12),'expenses':(0,10**12),'savings':(0,10**12),'goal':(0,10**12),'years':(1,40)}
def parse_updates(text):
    text=text.strip()
    if text.startswith('```'):
        text=text.split('\n',1)[1].rsplit('```',1)[0].strip()
    data=json.loads(text)
    if not isinstance(data,dict): raise ValueError('Expected JSON object')
    updates={}
    for k,(lo,hi) in FIELDS.items():
        v=data.get(k)
        if isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and lo<=v<=hi and (k not in ('age','years') or v==int(v)):
            updates[k]=int(v) if k in ('age','years') else float(v)
    if data.get('risk') in ('Conservative','Moderate','Aggressive'): updates['risk']=data['risk']
    return updates, data.get('run_audit') is True
