"""Public current-edition bytes, statement scope and observed-read closure.

Not an automatic proof of English semantic equivalence, nor an authentication
protocol for execution records. Exact row decisions are replayed separately by
new_capture_check through the provenance entry in the runbook.
"""
from pathlib import Path
import csv,hashlib,json,re,sys
from decimal import Decimal
if not __debug__:raise RuntimeError('Assertions must be enabled')
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
sys.path.insert(0,str(B/'scripts'))
from current_data_core import core,digest,MODES
from new_capture_check import exact_statement
from claim_policy import corrected

def need(x,msg):
    if not x:raise ValueError(msg)
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def load(p):return json.loads(Path(p).read_text(),object_pairs_hook=unique,parse_float=Decimal,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite number')))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def file(f):
    need(type(f) is str and not Path(f).is_absolute() and '..' not in Path(f).parts,'unsafe path')
    p=(ROOT/f).resolve();need(p.is_relative_to(ROOT) and p.is_file(),'missing/outside path '+f)
    need(f==str(p.relative_to(ROOT)),'noncanonical file spelling or symlink alias '+f)
    return p
def checked(p):
    q=file(p['file']);need(sha(q)==p['sha256'],'pin mismatch '+p['file'])
    if 'bytes' in p:need(q.stat().st_size==int(p['bytes']),'byte count')
    return q
def rows(p):
    with p.open() as f:return list(csv.DictReader(f,delimiter='\t'))

cfg=load(B/'CURRENT_BINDINGS.json');capture_index=checked(cfg['capture_index'])
index=rows(B/'PUBLIC_INPUTS.tsv');pins={r['file']:r for r in index}
need(len(index)==len(pins),'duplicate public input')
for r in index:checked(r)
# Reading-copy indices are live roster obligations, not unchecked bibliographies.
reading_index=load(B/'READING_COPY_INDEX.json');reading_tables=reading_index['tables']
need(len(reading_tables)==2 and {Path(t['file']).name for t in reading_tables}=={'REVIEW_HASHES.json','RECORD_HASHES.json'},'reading-copy table coverage')
reading_entries=0
for table in reading_tables:
    need(table['file'] in pins and pins[table['file']]['sha256']==table['sha256'],'reading-copy table absent from roster')
    entries=load(checked(table));need(type(entries) is list and entries,'empty reading-copy table')
    for entry in entries:
        need(entry['file'] in pins and pins[entry['file']]['sha256']==entry['sha256'],'reading copy absent from roster or hash differs '+entry['file'])
        checked(entry);reading_entries+=1
claims=load(B/'OBLIGATIONS.json')['rows'];claimids={r['id']:r for r in claims};eq=load(B/'CLAIM_EQUIVALENCE.json')
need(len(claims)==len(claimids)==len(eq)==210 and {r['old_id'] for r in eq}==set(claimids),'210-claim closure')
for r in eq:
    expected_claim=corrected(r['old_id'],r['old_claim'])
    expected_kind=('VERBATIM' if expected_claim==r['old_claim'] else 'CORRECTED_EXPLICIT_RATIO' if r['old_id']=='G20S_PHYSICAL' else 'EDITORIAL_TEXT_ONLY')
    need(r['classification']==expected_kind and claimids[r['old_id']]['claim']==expected_claim,'undeclared claim change')
    old=hashlib.sha256(r['old_claim'].encode()).hexdigest();new=hashlib.sha256(claimids[r['old_id']]['claim'].encode()).hexdigest()
    need(old==r['old_claim_sha256'] and new==r['new_claim_sha256'],'claim text mismatch')
    for key in ('depends_on','kind','graph_binding'):need(r[key]==claimids[r['old_id']][key],'claim dependency/role changed')
scopes=load(B/'CLAIM_SCOPE_REQUIREMENTS.json');need(len(scopes)==2 and len({r['id'] for r in scopes})==2,'signed restriction count')
expected={r['old_id']:re.findall(r'Only [^\n]*',corrected(r['old_id'],r['old_claim'])) for r in eq if re.findall(r'Only [^\n]*',corrected(r['old_id'],r['old_claim']))}
need(set(expected)=={r['id'] for r in scopes},'signed restriction ids')
for r in scopes:need(r['required_sentences']==expected[r['id']] and all(t in claimids[r['id']]['claim'] for t in r['required_sentences']),'signed scope weakened')
data=load(B/'DATA_EQUIVALENCE.json');need(len(data)==11 and len({r['file'] for r in data})==11,'data projection closure')
need({Path(r['file']).name:r['mode'] for r in data}==MODES,'unexpected mathematical record/mode set')
for r in data:need(digest(core(load(checked(r)),r['mode']))==r['canonical_mathematical_sha256'],'data projection changed')
need({str(p.relative_to(ROOT)) for p in B.glob('*_PUBLIC.json')}<={r['file'] for r in data},'unclassified public mathematical record')
cap=load(capture_index);records={};auditpins={}
for p in cap['records']:
    rec=load(checked(p));sid=rec['statement'];need(sid not in records,'duplicate current capture');records[sid]=rec;auditpins[sid]=p
need(len(records)==98,'capture count')
arcrows=load(B/'LABEL11_ARCS_PUBLIC.json')['rows']
need(len(arcrows)==4 and {r['statement'] for r in arcrows}=={'CLASS_PSSW37_L11_T03','CLASS_PSSW37_L11_T15','CLASS_PSW37_L11_T09','CLASS_PSW37_L11_T17'},'four label11 arc rows')
for r in arcrows:
    sid=r['statement'];rec=records[sid]
    need(r['receipt_folder']==str(Path(rec['classes']['file']).parent),'arc receipt-folder binding')
    need(checked(r['checked_class'])==checked(rec['classes']) and checked(r['audit'])==checked(auditpins[sid]),'arc current class/audit binding')
aliases=load(B/'CLASS_ALIASES_PUBLIC.json');need(len(aliases['aliases'])==98 and aliases['alias_counts']=={'IDENTICAL_BYTES':98},'current alias count')
need({r['id'] for r in aliases['aliases']}==set(records),'alias identities')
for r in aliases['aliases']:
    p=records[r['id']]['classes'];need(r['kind']=='IDENTICAL_BYTES' and r['typed_parsed_value_equal'] is True and r['pinned']==p==r['executed'],'current identity alias');checked(p)
need(len(aliases['signed_rows'])==2,'signed alias rows lost')
for r in aliases['signed_rows']:
    rec=records[r['id']];need(r['executed']==rec['classes'] and r['receipts']==rec['receipts'],'signed current capture pointers')
checked(aliases['actual_Node_checker']);checked(aliases['Node_checker_independent_review'])
lit=load(B/'LITERAL_STATEMENTS_PUBLIC.json')['rows'];need(len(lit)==100 and {r['id'] for r in lit}==set(records)|{'C_7','C_8'},'literal closure')
for r in lit:
    if r['id'] in ('C_7','C_8'):
        need(r['kind']=='DERIVED_OCCUPANCY_NOT_EXECUTED_SCORE' and r['depends_on'],'derived occupancy premise absent');continue
    rec=records[r['id']];cl=load(checked(rec['classes']));cert=load(checked(rec['certificate']))
    need(r['statement']==exact_statement(cl,cert) and r['bound']==rec['header']['bound'],'literal theorem differs from executed class')
    need(r['executed_classes']==rec['classes'] and r['receipts']==rec['receipts'],'literal current receipts')
roster=load(B/'runtime/RECEIPT_ROSTER.json')['rows'];need(len(roster)==100 and len({r['statement'] for r in roster})==100,'roster closure')
for r in roster:
    sid=r['statement']
    if sid in ('C_7','C_8'):need(not r['executions'],'invented occupancy execution');continue
    rec=records[sid];need(len(r['executions'])==1,'historical execution in new roster');e=r['executions'][0]
    need(e['folder']==r['effective_final_execution']==str(Path(rec['classes']['file']).parent),'execution folder')
    need(e['certificate_sha256']==rec['certificate']['sha256'] and e['checked_classes_sha256']==rec['classes']['sha256'] and e['receipts']==rec['receipts'],'execution inputs')
replays=load(B/'PUBLIC_REPLAY_RESULTS.json');book=load(B/'runbook_public.json');bc={r['id']:r for r in book['checks']}
need(checked(replays['runbook'])==B/'runbook_public.json' and checked(replays['driver'])==B/'replay_round2.py','replay driver/runbook identity')
retired=set(cfg['retired_canonical_path_sha256']);need(retired and len(retired)==len(cfg['retired_canonical_path_sha256']),'retirement policy missing/duplicate')
need(replays['status']=='PASS_ALL_31_FRESH_EXECUTIONS' and len(replays['checks'])==len(bc)==31 and {r['id'] for r in replays['checks']}==set(bc),'fresh replay coverage')
need(len(book['checks'])==len(bc),'duplicate raw runbook rows')
for r in replays['checks']:
    receipt=load(checked(r['receipt']));need(receipt['status']=='PASS' and receipt['error'] is None and receipt['id']==r['id'] and receipt['missing_required_output']==[] and r['status']=='PASS' and r['driver_return_code']==0 and r['driver_error'] is None,'fresh replay failure')
    need(r['script']['file']==bc[r['id']]['script'] and r['script']['sha256']==receipt['script_sha256']==bc[r['id']]['script_sha256'],'current script mismatch');checked(r['script'])
    need(len(r['inputs'])==len(receipt['inputs_read']) and {p['file'] for p in r['inputs']}==set(receipt['inputs_read']),'observed read coverage')
    need(len(r['outputs'])==len(receipt['redirected_outputs']) and {p['file'] for p in r['outputs']}==set(receipt['redirected_outputs'].values()),'observed output coverage')
    for p in r['inputs']:
        need(hashlib.sha256(p['file'].encode()).hexdigest() not in retired,'retired execution product read again')
        checked(p);need(p['file'] in pins and pins[p['file']]['sha256']==p['sha256'],'actual read absent from public roster')
    for p in r['outputs']:checked(p)
    stdout=checked(r['receipt']).parent/'stdout.txt';f=str(stdout.relative_to(ROOT));need(f in pins and checked(pins[f])==stdout,'stdout not pinned')
    need(all(t in stdout.read_text() for t in bc[r['id']]['required_output']),'required output missing')
    if r['id']=='provenance':need(str(capture_index.relative_to(ROOT)) in receipt['inputs_read'],'current capture index not read')
# Every current auxiliary pin is a roster obligation; historical hashes are separate.
def current_pins(value):
    if isinstance(value,dict):
        if isinstance(value.get('file'),str) and isinstance(value.get('sha256'),str):yield value
        for v in value.values():yield from current_pins(v)
    elif isinstance(value,list):
        for v in value:yield from current_pins(v)
closure=load(B/'CURRENT_READ_CLOSURE.json')
need(set(closure['checks'])=={r['id'] for r in replays['checks']},'current read closure check set differs')
for r in replays['checks']:
    need(closure['checks'][r['id']]==r['inputs'],'current read closure differs from fresh replay')
auxiliary_pin_count=0
for name in ('CURRENT_READ_CLOSURE.json','EDITORIAL_EXTRACTS.json'):
    for p in current_pins(load(B/name)):
        need(p['file'] in pins and pins[p['file']]['sha256']==p['sha256'],'auxiliary pin absent from roster or hash differs '+p['file'])
        checked(p);auxiliary_pin_count+=1
labels=rows(B/'revision-v7/LABELS.tsv');need(len(labels)==278 and len({r['label'] for r in labels})==95,'label/evidence-row closure')
need((B/'LABELS_PUBLIC.tsv').read_bytes()==(B/'revision-v7/LABELS.tsv').read_bytes(),'public label mirror differs from canonical proof labels')
for p in labels:
    need(p['file'] in pins and pins[p['file']]['sha256']==p['sha256'],'label absent from public roster '+p['file'])
    checked(p)
bylabel={k:[r for r in labels if r['label']==k] for k in ('file:EXECUTION_BINDINGS','file:ROOT_ADMISSION_OUTPUT')};need(all(len(v)==1 for v in bylabel.values()),'execution labels must each name one output');bylabel={k:v[0] for k,v in bylabel.items()};bycheck={r['id']:r for r in replays['checks']}
composition=[p for p in bycheck['bc_composition']['outputs'] if Path(p['file']).name=='SOURCE_BINDINGS.json'];need(len(composition)==1,'composition output missing')
need(checked(bylabel['file:EXECUTION_BINDINGS'])==checked(composition[0]),'composition proof label is not the current output')
need(checked(bylabel['file:ROOT_ADMISSION_OUTPUT'])==checked(bycheck['admission']['receipt']).parent/'stdout.txt','admission proof label is not the current output')
evidence=load(B/'EVIDENCE_EQUIVALENCE.json');need(len(evidence)==len(index) and {r['file'] for r in evidence}==set(pins),'evidence classification closure')
for r in evidence:
    need(r['sha256']==pins[r['file']]['sha256'],'evidence digest mismatch')
    need(r['classification'] in ('UNCHANGED','EDITED_LINES','NEW') and r['reason'],'unexplained evidence classification')
    if r['classification']=='UNCHANGED':need(r['baseline_sha256']==r['sha256'],'unchanged bytes differ')
print(json.dumps({'status':'PASS_CURRENT_PUBLIC_BYTES_SCOPE_AND_READ_CLOSURE','claims':210,'literal_statements':100,'capture_statements':98,'signed_restrictions':2,'data_projections':11,'fresh_checks':31,'proof_label_rows':278,'distinct_proof_labels':95,'public_inputs':len(index),'reading_copy_tables':len(reading_tables),'reading_copy_entries':reading_entries,'auxiliary_current_pins':auxiliary_pin_count,'scope':'Byte, explicit data-projection, statement and observed-read closure. English reasoning and actual-execution authenticity are separate premises.'},indent=2))
