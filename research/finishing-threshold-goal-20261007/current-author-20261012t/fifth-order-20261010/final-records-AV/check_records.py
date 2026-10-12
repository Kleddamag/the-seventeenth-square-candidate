"""Read-only small final-record join. No large tree parsing, hashing or arithmetic."""
from pathlib import Path
import hashlib,json,difflib
R=Path('research/finishing-threshold-goal-20261007');W=R/'window-capture';D=Path(__file__).resolve().parent;WX=Path('research/window-extension-20261008');M=D/'BEFORE.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();pin=lambda p:dict(file=str(p),sha256=sha(p));load=lambda p:json.loads(Path(p).read_text())
expected=[('JPWS','v4',6,'af742507a1553a11084ea98386a294ae997e9749122fe632f7e940aa414b2fed','0a094486675bef106080299862c52968d6256de1c4499b1a4fd27bd339c4bcf6'),('JPW13','v2x',5,'0f7d2cb3f0cb3d101d0e5dbf9c6fc5e86b73526bdf404be2a931392fbd0664f9','2de8ae1b9d0c7ad1439b1ff492a40aae6e6ba00dc72a97bad15d316e13e8fa45'),('JPG3p','v5',4,'16226ebd1dca325b8f3fd2c7c35e91ab8ef5d114a1b751f74ec7291e9e92f319','9fa9013da56b4a184836160cae6b745e8dfe9e38136867ab7b4c27c10a7c4841'),('JPG15m','v5',3,'33b20db1bc7f344e7fcd0f3fcab71d26affc3daa316d5dc52facad628ae23f30','77da7db7f81007c7765dc852b9aeec672c4ea4e4579cd5d587d0c40c43be722a')]
# Every supplied full digest is checked before interpreting the source.
rows=[];m=load(M)
def section(s,start,end):return s.split(start,1)[1].split(end,1)[0]
for region,ver,batch,rhash,vhash in expected:
 name=f'{region}_{ver}';a=W/'third-order-20261010/local-region-audits'/name;rp=WX/'bigbox/join'/f'RECORD_E{name}.md';vp=WX/f'reviews/join_roots/batch{batch}'/f'REVIEW_E{name}.md';op=a/'LEAD_RECORD_SNAPSHOT.md';ap=a/'AUDIT.json'
 assert sha(rp)==rhash,(rp,sha(rp));assert sha(vp)==vhash
 old=op.read_text();new=rp.read_text();review=vp.read_text();audit=load(ap)
 assert (WX/f'reviews/join_roots/batch{batch}/as_reviewed'/rp.name).read_bytes()==op.read_bytes()
 assert sha(op)[:16] in review and vhash[:16] in new
 assert '**STATUS: PROVED' in new
 assert section(old,'## Evidence','## What the statement')==section(new,'## Evidence','## What the statement'),'Evidence or leaf table changed'
 oldstatement=section(old,'## Statement','## Evidence');newstatement=section(new,'## Statement','## Evidence')
 if region=='JPW13':oldstatement=oldstatement.replace('the wall case above:', 'the case "wall above" of the join design:')
 assert oldstatement==newstatement,'Mathematical statement changed'
 root=m['root_obligations'][region]
 assert {k:root[k] for k in ['file','sha256']}==audit['root'] and root['certificate']==audit['certificate']
 assert root['status']=='COUNTED' and root['required']=='EMPTY'
 for p in [audit['root'],audit['expect'],audit['acceptance_log']]+audit['receipts']:
  assert sha(p['file'])==p['sha256']
  assert p['sha256'][:16] in new,(region,p['file'])
 assert audit['certificate']['sha256'][:16] in new and audit['certificate']['uncompressed_sha256'][:16] in new
 rows.append(dict(region=region,root={k:root[k] for k in ['file','sha256']},old_record=pin(op),old_audit=pin(ap),final_record=pin(rp),final_independent_review=pin(vp),as_reviewed_equals_own_snapshot=True,evidence_and_leaf_table_byte_identical=True,statement_identical_after_named_nonmathematical_wording=(region=='JPW13'),statement_equal=True,certificate=audit['certificate'],small_receipts=audit['receipts'],acceptance_log=audit['acceptance_log'],scope='Source/statement/evidence identity only. Prior exact tree arithmetic and coverage reviews remain required.'))
print(json.dumps(dict(status='PASS_FINAL_RECORDS_BIND_THE_SAME_ROOT_STATEMENTS_AND_EVIDENCE',manifest=pin(M),rows=rows,script=pin(__file__),not_replayed=['large compressed or plain tree hashes','local polynomial arithmetic','entire child/option coverage, already independently audited']),indent=2))
