if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
from pathlib import Path
PUBLIC=Path(__file__).resolve().parent.parent
PUBLIC_ROOT=PUBLIC.parents[4]
"""Small BC source/header/chain checks; no polynomial rebuild or solver."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,gzip,re
HERE=PUBLIC;ROOT=PUBLIC_ROOT;W=HERE.parents[0].parent
WX=ROOT/'research/window-extension-20261008';G=W/'g20s-terminal-audit'
def pin(p):
    p=Path(p)
    if not p.is_absolute():p=ROOT/p
    return {'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return json.loads(Path(p).read_text())
I=[str(i) for i in range(1,18) if i!=4]
def expand(e):
    box={i:[[str(-F(e['core'])),e['core']],[str(-F(e['core'])),e['core']]] for i in I}
    for i,cs in e.get('box',{}).items():
        for k,span in cs.items():box[i][int(k)-1]=span
    return {'box':box,'alpha':{i:e['alpha'].get(i,e['alpha']['default']) for i in I}}
def contained(a,b,cut=False):
    for i in I:
        for k in range(2):
            x,y=map(F,a['box'][i][k]);l,u=map(F,b['box'][i][k])
            if cut and i=='2' and k==0:y=min(y,F(0))
            if not l<=x<=y<=u:return False
        if F(a['alpha'][i])>F(b['alpha'][i]):return False
    return True
headers={};expect={};trees=[]
for name in ['G20S','HW']:
    p=WX/'bigbox/gen17'/f'{name}_tree.jsonl.gz'
    with gzip.open(p,'rb') as f:line=f.readline();header=json.loads(line)
    efile=WX/'acceptance'/f'EXPECT_{name}.json';e=load(efile)
    assert header['packing_sha256']=='24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7'
    assert header['Sref']=='4675530093604551/1000000000000000'
    assert header['window']==expand(e['window']) and header['terminal']==expand(e['tube'])
    log=ROOT/'local-research/claude-20261002/review/public-edition/path-neutral-20261012/files/research/window-extension-20261008/acceptance'/f'ACCEPT_{name}_v30.log';text=log.read_text()
    assert 'RESULT: ACCEPTED' in text and 'ok    header tube = expected tube' in text
    digest=re.search(r'sha256 certificate:\s+([0-9a-f]{64})',text)[1]
    trees.append({'name':name,'certificate':{'file':str(p.relative_to(ROOT)),'sha256':digest,'hash_source':'accepted log; full stream not rehashed here'},
                  'header_sha256':hashlib.sha256(line).hexdigest(),'expect':pin(efile),'acceptance':pin(log)})
    headers[name]=header;expect[name]=e
entry=expand({'core':'1/200','alpha':{'default':'1/400'},'box':{
 '2':{'1':['-8/25','0']},'11':{'2':['-1/5','1/20']},'13':{'2':['-1/5','3/40']}}})
assert contained(headers['G20S']['terminal'],headers['HW']['window'],True)
assert not contained(headers['G20S']['terminal'],headers['HW']['window'],False)
assert contained(headers['HW']['terminal'],entry,True)
assert not contained(headers['HW']['terminal'],entry,False)
assert F(headers['G20S']['window']['box']['2'][0][1])==0
interface=load(G/'sixteen-square-corollary/producer/MATHEMATICAL_INTERFACE.json')
ent=interface['finite_entry']
assert ent['core_position_abs_upper']=='1/200' and ent['independent_radian_angle_abs_upper']=='1/400'
assert ent['sliders']=={'2':['0','8/25'],'21':['-1/20','1/5'],'25':['-1/5','3/40']}
assert [s['label'] for s in ent['squares']]==list(map(int,I))
refpin=interface['reference_sources']['rational_reference_file'];ref=load(refpin['path'])
assert pin(refpin['path'])['sha256']==refpin['sha256']==headers['G20S']['packing_sha256']
t9=F(ref['squares'][8]['t']);c9=(1-t9*t9)/(1+t9*t9);T0=c9*(c9+4-F(ref['side']))
for sq in ent['squares']:
    i=sq['label'];raw=ref['squares'][i-1];t=F(raw['t'])
    u=((1-t*t)/(1+t*t),2*t/(1+t*t));v=(-u[1],u[0]);p=[F(raw['x']),F(raw['y'])]
    if i==13:p=[p[k]-T0*v[k]/3 for k in [0,1]]
    assert list(map(F,sq['reference_centre']))==p
    assert tuple(map(F,sq['reference_u']))==u and tuple(map(F,sq['reference_v']))==v

stages=[];allrounds=[];previous=None;builderhashes=set()
for producer,review in [('producer','independent-review'),('continuation','continuation-independent-review'),('finishing-continuation','finishing-independent-review'),('proposal-timeout-retry','proposal-timeout-retry-independent-review')]:
    p=G/'finite-stopped-contraction'/producer;v=G/'finite-stopped-contraction'/review
    cert=load(p/'certificate.json');rs=[]
    for step in cert['steps']:
        n=step['round'];allrounds.append(n);model=p/step['model_file']
        assert pin(model)['sha256']==step['model_sha256']
        data=load(model);assert data['incoming_bounds']==step['incoming_bounds']
        if previous is not None:assert step['incoming_bounds']==previous
        previous=step['outgoing_bounds'];rs.append(n)
    b=pin(v/'independent_model.py');builderhashes.add(b['sha256'])
    stages.append({'rounds':rs,'certificate':pin(p/'certificate.json'),
        'driver':pin(v/'check.py'),'independent_builder':b,'review':pin(v/'REVIEW.md'),'manifest':pin(v/'MANIFEST.json')})
assert allrounds==list(range(1,18)) and len(builderhashes)==1
assert next(iter(builderhashes))=='f1e9b375a3985904e848e7e2ba8149a3efdaf7938cfb9111265f3d689fc35305'
source_paths=[
 G/'sixteen-square-corollary/producer/THEOREM.md',G/'sixteen-square-corollary/producer/MATHEMATICAL_INTERFACE.json',
 G/'sixteen-square-corollary/independent-review/REVIEW.md',G/'sixteen-square-corollary/independent-review/MANIFEST.json',
 G/'finite-entry-stop-pruning/entry-producer/PRUNING.json',G/'finite-entry-stop-pruning/entry-producer/RESULT.md',
 G/'finite-entry-stop-pruning/entry-review/REVIEW.md',G/'finite-entry-stop-pruning/entry-review/MANIFEST.json',
 G/'finite-entry-stop-pruning/entry-review/check_transfer.py',G/'finite-entry-stop-pruning/entry-review/check_binding.py',
 G/'finite-entry-stop-pruning/root-review/REVIEW.md',G/'full-stopped-propagation/rational-entry-review/REVIEW.md',
 G/'full-stopped-propagation/rational-entry-review/MATHEMATICAL_INTERFACE.json',
 G/'full-stopped-propagation/continuation-independent-review/REVIEW.md',
 G/'full-stopped-propagation/continuation-independent-review/MANIFEST.json',
 WX/'bigbox/join/EXPECT_JG_v2.json',ROOT/'local-research/claude-20261002/review/public-edition/path-neutral-20261012/files/research/window-extension-20261008/acceptance'/'ACCEPT_JG_v2.log',WX/'acceptance/h_report30.py',
 ROOT/'local-research/claude-20261002/review/public-edition/round5/records/bigbox/join/RECORD_EJPA_v5.md',
 W/'contract-author-20261009-2110/independent-frame-review/ACCEPTED_INTERFACE.json',
 HERE.parent/'receipt-roster-AX/frame-direct-import/FINAL_BINDING_CHECK.json']
assert pin(ROOT/'local-research/claude-20261002/review/public-edition/round5/records/bigbox/join/RECORD_EJPA_v5.md')["sha256"]=='24a7a4d625b6b2e17407d771a4ce300211cc3eaea6bccdef638d944b28e3a439'
assert load(WX/'bigbox/join/EXPECT_JG_v2.json')['terminal_leaves'] is None
assert "terminal leaves: ['td0f7ae2afe']" in (ROOT/'local-research/claude-20261002/review/public-edition/path-neutral-20261012/files/research/window-extension-20261008/acceptance'/'ACCEPT_JG_v2.log').read_text()
result={'status':'PASS_SMALL_HEADER_SOURCE_CHECKS_NOT_FULL_ARITHMETIC_REPLAY','source':pin(__file__),
 'trees':trees,'T1_cut_to_HW':True,'T2_cut_to_entry':True,
 'negative_controls_without_preserved_xi2_upper0':'both rejected','reference_centres_axes_equal_for_all16':True,'finite_stages':stages,
 'finite_rounds_cover':allrounds,'all_stage_joins_identical':True,'sources':list(map(pin,source_paths)),
 'scope':'Header/EXPECT equality, small interval inclusions,17 saved model hash/box-chain bindings and source pins. Independent row necessity/arithmetic reviews are imported; polynomial rows not rebuilt here.'}
(HERE/'SOURCE_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: two exact header joins (both uncut controls fail);17 model hash/box links; four identical independent builders; JPA copy and JG log.')
