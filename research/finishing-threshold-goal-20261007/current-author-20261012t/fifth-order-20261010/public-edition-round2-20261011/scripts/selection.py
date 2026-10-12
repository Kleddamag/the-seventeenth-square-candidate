if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
from pathlib import Path
PUBLIC=Path(__file__).resolve().parent.parent
PUBLIC_ROOT=PUBLIC.parents[4]
"""Read-only readiness of an explicitly chosen prospective map; never auto-select alternatives."""
from pathlib import Path
import argparse,json,hashlib
O=PUBLIC;W=PUBLIC.parent.parent
a=argparse.ArgumentParser();a.add_argument('--scenario',choices=['original','al6','rm12'],default='original');a.add_argument('--manifest',type=Path,default=W/'second-order-20261010/theorem/THEOREM_MANIFEST.json');args=a.parse_args()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();pin=lambda p:dict(file=str(p),sha256=sha(p));load=lambda p:json.loads(Path(p).read_text())
assert args.scenario=='original', 'Only the selected proof route is in this packet'
mp=PUBLIC/'runtime/SELECTED_ORIGINAL_MAP.json';s=load(mp);m=load(args.manifest)
cat={r['id']:r for r in m['selectable_class_statements']};clauses={r['id']:r for r in m['branch_clauses']};base={r['name']:r for r in m['base_capture_rows']};issues=[];rows=[]
assert len(s['rows'])==84 and len({r['clause'] for r in s['rows']})==84
assert {r['clause'] for r in s['rows']}==set(clauses)
for r in s['rows']:
 assert sha(r['literal']['file'])==r['literal']['sha256']
 root=m['root_obligations'][r['root']];assert {k:root[k] for k in ['file','sha256']}==r['root_binding']
 c=clauses[r['clause']];reason=[];x=cat.get(r['selected'])
 if x is None:reason.append('SELECTOR_REGISTRATION_OPEN')
 else:
  assert {k:x[k] for k in ['file','sha256','bound']}==r['literal'],r['selected']
  if x['status']!='COUNTED':reason.append('LITERAL_BUDGET_OPEN')
  if r['selected'] not in c['options']:reason.append('EXACT_BRANCH_JOIN_OPEN')
  for p in x.get('extra_capture_premises',[]):
   if p['name'] not in base or base[p['name']]['status']!='COUNTED':reason.append('EXTRA_PREMISE_OPEN:'+p['name'])
   else:assert all(base[p['name']][k]==p[k] for k in ['file','sha256','bound'])
  # Extra CLASS prerequisites are AND edges, distinct from an OR clause.
  expected=r.get('extra_class_premises',[])
  if expected != x.get('extra_class_premises',[]):reason.append('EXTRA_CLASS_GUARD_NOT_REGISTERED')
  if not reason:assert c['status']=='COUNTED'
 # Test the proposed map's own guards even before selector registration.
 for p in r.get('extra_class_premises',[]):
  y=cat.get(p['id'])
  if y is None or y['status']!='COUNTED':reason.append('EXTRA_CLASS_BUDGET_OPEN:'+p['id'])
  else:assert all(y[k]==p[k] for k in ['file','sha256','bound'])
  assert p['id'] != r['selected'], 'self-dependent selected input'

 rows.append(dict(clause=r['clause'],selected=r['selected'],status='SELECTED_INPUTS_COUNTED' if not reason else 'OPEN',reasons=reason))
for r in m['base_capture_rows']:
 if r['status']!='COUNTED':issues.append(r['name'])
for g in m['global_premises']:
 if g['status']!='COUNTED':issues.append(g['id'])
for n,r in m['root_obligations'].items():
 if r['status']!='COUNTED':issues.append('LOCAL_'+n)
if m['slab_capture']['status']!='COUNTED':issues.append('SL11_T020')
openrows=[r for r in rows if r['status']=='OPEN'];report=dict(status='SELECTED_MAP_READINESS_ONLY_NOT_A_MATHEMATICAL_REVIEW',scenario=args.scenario,manifest=pin(args.manifest),selected_map=pin(mp),clauses=rows,other_open=issues,unique_open_selected=sorted({r['selected'] for r in openrows}),ready_for_final_assembly_reader=not openrows and not issues,final_independent_review=m['final_independent_assembly_review'],qualification='No alternate COUNTED option may substitute for the chosen ID or a specifically required predecessor CLASS. This is the input gate for a fresh final review, never an optimality seal. Large proof arithmetic is imported via audited manifest pins.',script=pin(__file__))
print(json.dumps(report,indent=2))
