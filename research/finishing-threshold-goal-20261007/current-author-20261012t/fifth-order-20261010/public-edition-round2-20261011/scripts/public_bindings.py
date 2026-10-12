"""Bind the public obligations and mathematical graph; disclose open review labels."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent.parent;ROOT=B.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def forbidden(p):
 return any(x in p for x in ['frozen-final-original-','final-read-supplement-','final-read-errata-','package-runbook-BJ-','/sources/']) or Path(p).name in ['FOR_CODEX.md','STATUS.md','HANDOVER.md','worker.sh','cvjob.sh','run.sh','mkv.sh','job.txt','DONE'] or Path(p).name.startswith('CLAUDE_REPLY_')
def pins(x):
 if isinstance(x,dict):
  if isinstance(x.get('file'),str) and 'sha256' in x:yield x
  for v in x.values():yield from pins(v)
 elif isinstance(x,list):
  for v in x:yield from pins(v)
checked={};open_labels={}
for name in ['OBLIGATIONS.json','DEPENDENCY_GRAPH.json','LITERAL_STATEMENTS_PUBLIC.json','CLASS_ROW_SOURCES_PUBLIC.json','LABEL11_ARCS_PUBLIC.json','LABEL11_MARGINS_PUBLIC.json']:
 d=json.loads((B/name).read_text())
 for x in pins(d):
  p=x['file'];assert not forbidden(p),p
  q=Path(p);assert not q.is_absolute() and '..' not in q.parts,p
  if x['sha256'] is None:
   assert x.get('label','').startswith('review:') and p.startswith('local-research/claude-20261002/review/public-edition/reports/'),x
   open_labels[x['label']]=p;continue
  if p not in checked:checked[p]=sha(ROOT/p)
  assert checked[p]==x['sha256'],p
ob=json.loads((B/'OBLIGATIONS.json').read_text())['rows'];ids={r['id'] for r in ob}
assert len(ob)==len(ids)==210
for r in ob:assert r['evidence'] and set(r['depends_on'])<=ids,r['id']
assert not open_labels, open_labels
print(json.dumps({'status':'PASS_PUBLIC_BINDINGS','distinct_files':len(checked),'open_review_labels':open_labels,'obligations':len(ob)},indent=2))
print('PASS_PUBLIC_BINDINGS')
