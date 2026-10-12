"""Explicit comparison projections for reissued public mathematical records.

The capture roles require separate current-execution validation. Stripping a pin
for this comparison never establishes that the file it names was validated.
"""
import hashlib,json,re
from decimal import Decimal
RENAMES={('T_label%d_contract_exempt'%n):('T_label%d_exempt'%n) for n in (1,2,5,6,10,11,12,13,14,16)}
MODES={name:'pin_metadata_only' for name in ('SMALL_CHECKS_PUBLIC.json','FRAME_DISJOINTNESS_PUBLIC.json','CLASS_ROW_SOURCES_PUBLIC.json','LABEL11_ARCS_PUBLIC.json','LABEL11_MARGINS_PUBLIC.json','REVIEWS_PUBLIC.json','SELECTED_ORIGINAL_MAP.json')}
MODES.update({'CLASS_ALIASES_PUBLIC.json':'current_aliases','LITERAL_STATEMENTS_PUBLIC.json':'current_literals','RECEIPT_ROSTER.json':'current_roster','SOURCE_BINDINGS.json':'composition'})
MODES['LABEL11_ARCS_PUBLIC.json']='current_arc_records'

def normal(x):
    if type(x) is list:return [normal(v) for v in x]
    if type(x) is not dict:return RENAMES.get(x,x) if type(x) is str else x
    omit={'file','sha256','bytes'} if type(x.get('file')) is str and 'sha256' in x else set()
    if type(x.get('centre')) is dict and type(x['centre'].get('polygon')) is list and type(x.get('angle_tan_half')) is list:omit=omit|{'label'}
    return {k:normal(v) for k,v in x.items() if k not in omit}

def value(x):
    if type(x) is dict:return '{'+','.join(json.dumps(k,ensure_ascii=False)+':'+value(x[k]) for k in sorted(x))+'}'
    if type(x) is list:return '['+','.join(value(v) for v in x)+']'
    if type(x) is Decimal:
        if not x.is_finite():raise ValueError('nonfinite number')
        # Canonical numeric value without context-sensitive normalize(), which
        # could round long exact decimals. Preserve Decimal versus integer type.
        sign,digits,exponent=x.as_tuple();digits=list(digits)
        if not any(digits):return '0e0'
        while digits[-1]==0:digits.pop();exponent+=1
        return ('-' if sign else '')+''.join(str(d) for d in digits)+'e'+str(exponent)
    if type(x) not in (str,int,bool,type(None)):raise ValueError('unexpected type')
    return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def digest(x):return hashlib.sha256(value(x).encode()).hexdigest()

def core(x,mode):
    if mode=='pin_metadata_only':return normal(x)
    if mode=='composition':return normal({k:v for k,v in x.items() if k not in ('source','sources')})
    if mode=='current_aliases':
        return normal({k:v for k,v in x.items() if k not in ('aliases','alias_counts')})
    if mode=='current_roster':
        return normal({**x,'rows':[{k:v for k,v in r.items() if k not in ('executions','effective_final_execution')} for r in x['rows']]})
    if mode=='current_arc_records':
        return normal({**x,'rows':[{k:v for k,v in r.items() if k!='receipt_folder'} for r in x['rows']]})
    if mode=='current_literals':
        rows=[]
        for r in x['rows']:
            s={k:v for k,v in r.items() if k not in ('executed_classes','receipts','execution_role')}
            if r['id'] not in ('C_7','C_8'):
                s['statement']=re.sub('|'.join(re.escape(k) for k in RENAMES),lambda m:RENAMES[m.group(0)],s['statement'])
            rows.append(s)
        return normal({**x,'rows':rows})
    raise ValueError('unknown mode '+str(mode))
