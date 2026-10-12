"""Public validation of neutral NEW-run capture evidence.
Derived from the author preparation auditor; not an independent implementation.
Standard library only. No process launch, solver, geometry sweep or old-run read.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal
import hashlib,json,re,sys
ROOT=None
class Refuse(ValueError):pass

def need(ok,msg):
    if not ok:raise Refuse(msg)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def pin(p):
    p=Path(p).resolve();return {'file':str(p.relative_to(ROOT)), 'sha256':sha(p),'bytes':p.stat().st_size}

def pairs(p):
    d={}
    for k,v in p:
        need(k not in d,'duplicate JSON key '+k);d[k]=v
    return d

def load(p):
    return json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_float=Decimal,parse_constant=lambda s:(_ for _ in ()).throw(Refuse('JSON nonfinite '+s)))

def same(a,b):
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

ROW_FIELDS=('interval','passed','minimum_units','cells','deficient_slabs','deficit_minimum_units','default','classes','witness')

HEAD_FIELDS=('schema','symmetry','bound','classes','total_intervals','required_units','budget_units','surplus','certificate_sha256','classes_sha256')

PASS='PASS_CLASSES_EXACT_COVER'

PARTIAL='PASS_CLASSES_INTERVAL_PARTITION_ONLY'

def integer(x,msg,minimum=None):
    need(type(x) is int and (minimum is None or x>=minimum),msg);return x

def assess_row(r,cl,required,index):
    """Re-decide a saved row from exact partition counts/minima, not its flag.
    This does not re-run geometric cells or authenticate an execution.
    """
    need(type(r) is dict and all(k in r for k in ROW_FIELDS),'missing row fields')
    need(integer(r['interval'],'row index')==index,'wrong row index')
    # Conservative admission policy for this fixed 98-statement bundle: a row
    # with no checked cells is refused, even if its PASS flag is vacuously true.
    # This does not assert a general theorem about all checker inputs.
    integer(r['cells'],'nonempty checked row required',1);integer(r['minimum_units'],'row minimum')
    integer(r['deficient_slabs'],'deficient slab count',0)
    need(r['deficient_slabs']<=r['cells'],'more deficient slabs than checked cells')
    need(type(r['classes']) is list and len(r['classes'])==len(cl['classes']),'class count')
    minima=[];failing=[];cells=0
    parts=[r['default']]+r['classes'];thresholds=[Fraction(1)]+[Fraction(c['threshold']) for c in cl['classes']]
    for i,(p,t) in enumerate(zip(parts,thresholds)):
        need(type(p) is dict,'row partition');n=integer(p.get('cells'),'partition cells',0);m=p.get('minimum_units');cells+=n
        if i:need(p.get('name')==cl['classes'][i-1]['name'],'partition name/order')
        if n:
            integer(m,'nonempty minimum');minima.append(m)
            if m*t.denominator<t.numerator*required:failing.append(m)
        else:need(m is None,'empty partition has a minimum')
    need(cells==r['cells'],'partition cell count')
    if minima:need(min(minima)==r['minimum_units'],'row minimum disagrees with partitions')
    passed=not failing;need(type(r['passed']) is bool and r['passed']==passed,'saved PASS contradicts exact row minima')
    need(r['deficit_minimum_units']==(min(failing) if failing else None),'deficit minimum')
    if passed:need(r['witness'] is None,'passing row has witness')
    else:need(type(r['witness']) is dict,'failed row missing witness')
    need(passed,'failing numerical row')
    return {k:r[k] for k in ROW_FIELDS}

def expected_header(cl,cert,csha,clsha):
    need(type(cert['minimum_units']) is int and cert['minimum_units']>0,'positive minimum units')
    need(type(cert['budget_units']) is int,'integer budget units')
    surplus=Fraction(cl['bound'])*cert['minimum_units']-cert['budget_units'];need(surplus>0,'strict positive surplus')
    return dict(schema=cl['schema'],symmetry=cl['symmetry'],bound=str(Fraction(cl['bound'])),classes=[dict(name=c['name'],threshold=str(Fraction(c['threshold'])),slots=len(c['slots'])) for c in cl['classes']],total_intervals=len(cert['entries']),required_units=str(cert['minimum_units']),budget_units=str(cert['budget_units']),surplus=str(surplus),certificate_sha256=csha,classes_sha256=clsha)

def exact_statement(cl,cert):
    S=Fraction(cert['L'])/Fraction(cert['A'])
    need(S==Fraction(cert['normalized_target']),'certificate normalized side')
    which={'orbit':'the listed slots united with their eight D4 images','mirror_x':'the listed slots united with their images under the mirror x -> 2 c_x - x','fixed':'the listed slots exactly as written'}[cl['symmetry']]
    cx,cy=map(Fraction,cl['frame']['center'])
    return ('For every family of closed unit squares with pairwise disjoint interiors inside a square of side %s, '
            'read in the frame with the container centre at (%s, %s), the sum of tau(pose) over the squares is less than %s, '
            'where tau(pose) is the least threshold among the classes that contain the pose and 1 if no class contains it. '
            'A class is %s (angle gates with all quarter-turn lifts). Classes: %s.'
            % (S,cx,cy,Fraction(cl['bound']),which,'; '.join('%s threshold %s (%d slots)'%(c['name'],Fraction(c['threshold']),len(c['slots'])) for c in cl['classes'])))

def check_slice(d,cl,head,start,end,checker):
    for k,v in head.items():need(same(d.get(k),v),'slice header '+k)
    need(same(d.get('checker_sha256'),checker),'slice checker source identity')
    need(type(d.get('start')) is int and d['start']==start and type(d.get('end_exclusive')) is int and d['end_exclusive']==end,'slice range')
    need(d.get('status') in (PASS,PARTIAL) and d.get('failed_intervals')==[],'slice status')
    need(type(d.get('rows')) is list and len(d['rows'])==end-start,'slice row count')
    return [assess_row(r,cl,int(head['required_units']),i) for i,r in enumerate(d['rows'],start)]

def safe_file(root,name):
    need(type(name) is str,'artifact path type');p=Path(name)
    need(not p.is_absolute() and '..' not in p.parts,'artifact path escape')
    p=(root/p).resolve();need(p.is_relative_to(root.resolve()) and p.is_file(),'missing or external artifact');return p

def checked_artifact(root,p):
    need(type(p) is dict and set(['file','sha256','bytes'])<=p.keys(),'artifact pin shape')
    f=safe_file(root,p['file']);need(type(p['bytes']) is int and f.stat().st_size==p['bytes'] and sha(f)==p['sha256'],'artifact bytes mismatch');return f

def check_process(x,name):
    need(type(x) is dict and x.get('started') is True and type(x.get('exit_code')) is int and x['exit_code']==0 and x.get('signal') is None and x.get('timed_out') is False,name+' did not complete successfully')

PY_SOURCE={
 'exact_classes.py':'802dc62aa4f2a9e15ae406d39d5161540403972abbf21819660191d67dd6150b',
 'exact_restricted.py':'caae39b30cfcde513740337792865f43ed18738a539a34d9c8fec1e74d7686f9',
 'exact_general.py':'89954c6c44e1368b8553eb4d71d860f1a51b010be698088b6fbe3d4fad8eac46',
 'integer_sweep.py':'3a2bfd8892a9693b4dfca72e4d8e547a7be8775b22306740f4e6b63d0928b34b',
 'boolean_rule.py':'c49d38ac96027b34103c075a9996b6229fd2cf829055897dce2d8cf9a6db8275'}

NODE_SOURCE={'verify_classes.js':'7f6b234768f812b7acf515c28cc4ced0e5b7fb5bcd4c0ba03114733975087d40'}

PY_ROLES=('python_checker_main','python_checker_restricted','python_checker_general','python_checker_sweep','python_checker_rule')

SLICE_ROLES=PY_ROLES+('node_checker','launch_wrapper','output_comparator')

MERGE_ROLES=PY_ROLES+('node_checker','merge_wrapper')

SOURCE_MANIFEST_PIN='bdaaf36bf5b67f4ff3e81050cd1b95340be8dc2e992eb52e6160896339f57608'

PLAN_MANIFEST_PIN='bc8324cfa721889725f63bd1e2a31cd522e35bee257187154758639e642bd7d6'

MERGE_MANIFEST_PIN='7d26c9e73ab876ef07b62413bcec03c8555b7cccb49f4ce0fbf9ae06fada5075'

def check_sources(source_manifest):
    need(sha(source_manifest)==SOURCE_MANIFEST_PIN,'slice manifest is not the independently reviewed final issue')
    sm=load(source_manifest);need(sm.get('schema')=='s17-neutral-source-manifest-v1','source manifest schema')
    need(type(sm.get('roles')) is dict and set(sm['roles'])==set(SLICE_ROLES),'slice source roles')
    mf=source_manifest.parent/'MERGE_MANIFEST.json';need(sha(mf)==MERGE_MANIFEST_PIN,'merge manifest is not the reviewed issue')
    mm=load(mf);need(mm.get('schema')=='s17-neutral-merge-manifest-v1','merge manifest schema')
    need(type(mm.get('roles')) is dict and set(mm['roles'])==set(MERGE_ROLES),'merge source roles')
    for role in PY_ROLES+('node_checker',):need(same(sm['roles'][role],mm['roles'][role]),'slice and merge checker roles differ')
    roles=dict(sm['roles']);roles['merge_wrapper']=mm['roles']['merge_wrapper']
    for r,p in roles.items():checked_artifact(source_manifest.parent,p)
    need({Path(roles[r]['file']).name:roles[r]['sha256'] for r in PY_ROLES}==PY_SOURCE,'Python checker mathematics bytes changed')
    need(roles['node_checker']['sha256']==NODE_SOURCE['verify_classes.js'],'Node checker mathematics bytes changed')
    return roles

def check_common_provenance(p,sid,start,end,head,sm,pm,roles,merge=False):
    expected_schema='s17-neutral-merge-provenance-v1' if merge else 's17-neutral-slice-provenance-v1'
    need(p.get('schema')==expected_schema,'neutral provenance schema')
    need(p.get('statement_id')==sid and p.get('run_id')==load(pm)['run_id'],'provenance statement/run identity')
    for k in ('run_id','started_utc','finished_utc'):need(type(p.get(k)) is str and bool(p[k]),'missing provenance '+k)
    from datetime import datetime
    times=[datetime.strptime(p[k],'%Y-%m-%dT%H:%M:%SZ') for k in ('started_utc','finished_utc')]
    need(times[0]<=times[1],'reversed execution times')
    rr=p.get('rows');need(type(rr) is dict and same(rr,dict(start=start,end_exclusive=end,total_intervals=head['total_intervals'])),'provenance row range')
    expected={'certificate':head['certificate_sha256'],'classes':head['classes_sha256']}
    need(same(p.get('input_sha256_before'),expected) and same(p.get('input_sha256_after'),expected),'input stability or input identity')
    need(p.get('source_manifest_sha256')==sha(sm) and p.get('plan_manifest_sha256')==sha(pm),'manifest binding')
    if merge:need(p.get('merge_manifest_sha256')==sha(sm.parent/'MERGE_MANIFEST.json'),'merge manifest binding')
    selected_roles=MERGE_ROLES if merge else SLICE_ROLES
    hashes={r:roles[r]['sha256'] for r in selected_roles}
    need(same(p.get('source_sha256_before'),hashes) and same(p.get('source_sha256_after'),hashes),'actual source stability')
    rt=p.get('runtime');need(type(rt) is dict and type(rt.get('python_optimization_level')) is int and rt['python_optimization_level']==0,'Python assertions disabled or unrecorded')
    for k in ('python_implementation','python_version','numpy_version','numba_version','node_version','platform_system','platform_architecture'):
        need(type(rt.get(k)) is str and bool(rt[k]),'missing runtime '+k)
    for name in (('python','node') if merge else ('python','node','compare')):
        check_process(p.get('exits',{}).get(name),name)
        inv=p.get('invocation',{}).get(name);need(type(inv) is dict and type(inv.get('argv')) is list and all(type(x) is str for x in inv['argv']),'missing actual argv '+name)
        integer(inv.get('timeout_seconds'),'missing positive timeout',1)
    code=p.get('exits',{}).get('wrapper',{}).get('exit_code')
    need(type(code) is int and code==0 and p.get('verdict')=='PASS','wrapper incomplete')
    checks=p.get('checks');need(type(checks) is list and len(checks)==13 and all(type(c) is dict and type(c.get('check')) is str and c.get('ok') is True for c in checks),'missing or failed wrapper check')
    need(p.get('detail')==[],'nonempty provenance detail')
    en=p.get('environment_names_set');need(type(en) is list and all(type(k) is str for k in en) and en==sorted(set(en)),'environment names absent, duplicated or unsorted')

def slice_argv(p,start,end,head):
    for name,pre,script,out in [('python',['python','-B'],'src/exact_classes.py','py'),('node',['node'],'src/node/verify_classes_wb.js','node')]:
        inv=p['invocation'][name];workers=integer(inv.get('workers'),'worker count',1)
        want=pre+[script,'inputs/certificate.json','--classes','inputs/classes.json','--start',str(start),'--count',str(end-start),'--workers',str(workers),'--output','out/'+out+'.json']
        need(inv['argv']==want,'unrecognised actual '+name+' invocation')
    want=['python','-B','src/slice_compare.py','out/py.json','out/node.json',str(start),str(end),head['certificate_sha256'],head['classes_sha256'],'0','no','0','RUN','out/compare.json']
    need(p['invocation']['compare']['argv']==want,'unrecognised comparator invocation')

def check_provenance(p,root,sid,start,end,head,sm,pm,roles):
    check_common_provenance(p,sid,start,end,head,sm,pm,roles)
    need(p.get('planned') is True,'unplanned slice')
    for k in ('slice_id','attempt_id'):need(type(p.get(k)) is str and bool(p[k]),'missing '+k)
    need(re.fullmatch(r'a[1-9][0-9]{0,2}',p['attempt_id']) is not None,'attempt id')
    slice_argv(p,start,end,head)
    return {name:checked_artifact(root,p.get('outputs',{}).get(name)) for name in ('python','node','compare')}

def totals(rows,names):
    def join(ps):
        mins=[x['minimum_units'] for x in ps if x['minimum_units'] is not None]
        return dict(cells=sum(x['cells'] for x in ps),minimum_units=min(mins) if mins else None)
    return dict(unrestricted_minimum_units=min(r['minimum_units'] for r in rows),deficit_minimum_units=None,failed_intervals=[],cells_default=join([r['default'] for r in rows]),cells_by_class=[dict(name=n,**join([r['classes'][i] for r in rows])) for i,n in enumerate(names)])

def check_totals(d,rows,names):
    for k,v in totals(rows,names).items():need(same(d.get(k),v),'aggregate disagrees with rows: '+k)

def compare_record(d,files,start,end,head):
    for k,v in dict(rows=[start,end],certificate_sha256=head['certificate_sha256'],classes_sha256=head['classes_sha256'],python='PASS',node='PASS',agree='yes',python_exit=0,node_exit=0,rows_compared=end-start,rows_differing=0,header_fields_differing=0,differences=[]).items():
        need(same(d.get(k),v),'comparator record: '+k)
    for role in ('python','node'):
        need(d.get(role+'_output_sha256')==sha(files[role]) and type(d.get(role+'_output_bytes')) is int and d[role+'_output_bytes']==files[role].stat().st_size,'comparator output identity')

def checked_pin(root,p):
    need(type(p) is dict and set(('file','sha256','bytes'))<=p.keys(),'public pin shape')
    return checked_artifact(root,p)

def verify_new_capture_records(idx,root,only=None):
    """Public replay over the NEW run alone. Prior executions are not premises.
    The full old/new comparison is a separate pre-release compatibility audit.
    """
    global ROOT
    ROOT=Path(root).resolve()
    need(idx.get('schema')=='s17-public-new-capture-index-v1','public capture index schema')
    sm=checked_pin(ROOT,idx['source_manifest']);pm=checked_pin(ROOT,idx['plan_manifest']);mm=checked_pin(ROOT,idx['merge_manifest'])
    need(mm==sm.parent/'MERGE_MANIFEST.json' and pm==sm.parent/'PLAN_MANIFEST.json','manifest co-location')
    roles=check_sources(sm);need(sha(pm)==PLAN_MANIFEST_PIN,'unreviewed plan')
    plan=load(pm);items=plan['statements'];need(type(items) is list and len(items)==98,'plan count')
    plans={s['statement_id']:s for s in items};need(len(plans)==98,'duplicate plan id')
    expected=set(plans)
    if only is not None:
        need(type(only) in (list,tuple,set) and len(only)>0 and len(set(only))==len(only) and set(only)<=expected,'bad internal subset')
        expected=set(only)
    rows=idx.get('records');need(type(rows) is list and len(rows)==len(expected),'public audit count')
    seen=set();summary=[]
    for recpin in rows:
        rp=checked_pin(ROOT,recpin);rec=load(rp);sid=rec['statement']
        need(sid in expected and sid not in seen,'missing/repeated/unplanned public audit');seen.add(sid)
        need(rec.get('status')=='PASS_NEUTRAL_RECEIPTS_AND_EXACT_ROW_DECISIONS','public audit status')
        clp=checked_pin(ROOT,rec['classes']);cp=checked_pin(ROOT,rec['certificate']);cl=load(clp);cert=load(cp)
        head=expected_header(cl,cert,sha(cp),sha(clp));need(same(rec['header'],head),'saved audit header')
        st=plans[sid];total=head['total_intervals'];sl=st['slices'];cursor=0;ids=set()
        need(type(rec.get('rows')) is int and rec['rows']==total,'saved row count differs from pinned input')
        for x in sl:
            need(type(x['start']) is int and x['start']==cursor,'plan gap/overlap')
            cursor=integer(x['end_exclusive'],'plan end',cursor+1);need(x['slice_id'] not in ids,'repeated slice id');ids.add(x['slice_id'])
        need(cursor==total,'plan incomplete')
        for k in ('total_intervals','symmetry','bound','certificate_sha256','classes_sha256'):need(same(st[k],head[k]),'plan header '+k)
        need(st.get('checker_variant')=='wb' and st.get('node_checker_sha256')==NODE_SOURCE['verify_classes.js'],'Node plan variant')
        mpf=checked_pin(ROOT,rec['merge']);mp=load(mpf)
        check_common_provenance(mp,sid,0,total,head,sm,pm,roles,merge=True)
        need(type(mp.get('merge_attempt_id')) is str and re.fullmatch(r'm[1-9][0-9]{0,2}',mp['merge_attempt_id']),'merge attempt id')
        need(mp.get('slice_files_unchanged') is True and mp.get('planned_slices_without_a_selected_attempt')==[],'merge source closure')
        selected=mp['selected_slices'];saved=rec['selected']
        need(type(selected) is list and type(saved) is list and len(selected)==len(saved)==len(sl),'selection count')
        allrows=[]
        for x,c,a in zip(sl,selected,saved):
            for k in ('slice_id','start','end_exclusive'):need(same(x[k],c.get(k)),'selected range')
            need(a.get('slice_id')==c['slice_id'] and a.get('attempt_id')==c['attempt_id'],'saved selected identity')
            pf=checked_pin(ROOT,a['provenance']);p=load(pf);need(sha(pf)==c['provenance_sha256'],'selected provenance bytes')
            need(p.get('slice_id')==c['slice_id'] and p.get('attempt_id')==c['attempt_id'],'actual selected identity')
            lo=x['start'];hi=x['end_exclusive'];files=check_provenance(p,pf.parent,sid,lo,hi,head,sm,pm,roles);pair=[]
            for role,want in [('python',PY_SOURCE),('node',NODE_SOURCE)]:
                need(checked_pin(ROOT,a['outputs'][role])==files[role] and same(c[role],p['outputs'][role]),'selected output binding')
                d=load(files[role]);need(d.get('implementation')==('python exact_classes.py' if role=='python' else 'node verify_classes.js'),'implementation')
                need(d.get('statement')==(exact_statement(cl,cert) if d.get('status')==PASS else None),'slice literal theorem')
                rr=check_slice(d,cl,head,lo,hi,want);check_totals(d,rr,[k['name'] for k in cl['classes']]);pair.append(rr)
            need(same(pair[0],pair[1]),'two-engine exact row disagreement')
            need(checked_pin(ROOT,a['outputs']['compare'])==files['compare'] and same(c['compare'],p['outputs']['compare']),'comparator pin')
            compare_record(load(files['compare']),files,lo,hi,head);allrows.extend(pair[0])
        need(len(allrows)==total,'row total')
        for role,pre,script,ext,want in [('python',['python','-B'],'src/exact_classes.py','py',PY_SOURCE),('node',['node'],'src/node/verify_classes_wb.js','node',NODE_SOURCE)]:
            cmd=pre+[script,'inputs/certificate.json','--classes','inputs/classes.json','--output','out/receipt_'+role+'.json','--merge']+['slices/'+x['slice_id']+'.'+ext+'.json' for x in sl]
            need(mp['invocation'][role]['argv']==cmd,'merge argv')
            f=checked_artifact(mpf.parent,mp['outputs'][role]);need(checked_pin(ROOT,rec['receipts'][role])==f,'public receipt pin');d=load(f)
            need(d.get('implementation')==('python exact_classes.py' if role=='python' else 'node verify_classes.js'),'receipt implementation')
            need(d.get('statement')==exact_statement(cl,cert),'receipt literal theorem')
            for k,v in head.items():need(same(d.get(k),v),'receipt header '+k)
            for k,v in dict(status=PASS,start=0,end_exclusive=total,merged_files=len(sl),problems=[],missing_intervals=0,first_missing_intervals=[],failed_intervals=[],checker_sha256=want).items():need(same(d.get(k),v),'receipt coverage '+k)
            check_totals(d,allrows,[c['name'] for c in cl['classes']])
        summary.append(dict(statement=sid,rows=total,slices=len(sl),audit=pin(rp),classes=pin(clp),certificate=pin(cp),merge=pin(mpf)))
    need(seen==expected,'public statement closure')
    total=sum(s['rows'] for s in summary)
    if only is None:need(total==1728000,'unexpected selected row total')
    return dict(status='PASS_ALL_98_NEW_CAPTURE_RECORDS_AND_EXACT_MINIMUM_DECISIONS' if only is None else 'PASS_SELECTED_NEW_CAPTURE_RECORDS_ONLY',statements=summary,statement_count=len(expected),rows_per_engine=total,slices=sum(s['slices'] for s in summary),scope='Both recorded engines, all selected new saved exact row minima, exact class inequalities, complete coverage, literal theorem/input/source/process bindings. No geometry sweep; no cryptographic execution authentication. Earliest-attempt policy and old/new compatibility require separate release-preparation gates; this replay does not establish them.')

def verify_new_captures(index_path,root):
    index_path=Path(index_path).resolve();result=verify_new_capture_records(load(index_path),root)
    result['index']=pin(index_path);return result

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('index',type=Path);ap.add_argument('--root',required=True,type=Path);a=ap.parse_args()
    result=verify_new_captures(a.index,a.root)
    print(json.dumps({k:v for k,v in result.items() if k!='statements'},indent=2))
