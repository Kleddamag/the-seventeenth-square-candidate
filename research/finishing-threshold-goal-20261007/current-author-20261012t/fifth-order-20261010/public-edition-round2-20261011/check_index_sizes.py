"""Recheck the selected input-size bounds only. Stdlib, stdout, no row sweep."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time
if not __debug__:raise RuntimeError('Assertions required')
H=Path(__file__).resolve().parent;R=H.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
start=time.process_time();record=json.loads((H/'INDEX_SIZES.json').read_text())
assert sha((R/record['node_checker']['file']).read_bytes())==record['node_checker']['sha256']
assert sha((R/record['roster']['file']).read_bytes())==record['roster']['sha256']
roster=json.loads((R/record['roster']['file']).read_text())
expected={r['statement']:r for r in roster['rows'] if r['executions']}
assert len(record['rows'])==len(expected)==98
seen=set();maxima={k:0 for k in record['maxima']}
for row in record['rows']:
    name=row['statement'];assert name not in seen and name in expected;seen.add(name)
    parent=expected[name];folder=parent['effective_final_execution'] or parent['executions'][-1]['folder']
    execution=next(e for e in parent['executions'] if e['folder']==folder)
    assert row['file']==folder+'/certificate.json'
    data=(R/row['file']).read_bytes();assert sha(data)==row['sha256']==execution['certificate_sha256']
    d=json.loads(data)
    if 'sites' in d:n=len(d['sites'])
    else:
        LD=F(d['L'])*F(d['coordinate_denominator']);assert LD.denominator==1;LD=int(LD);n=0
        for x,y,_ in d['point_orbits']:
            x,y=int(x),int(y)
            n+=len({(a,b) for u,v in ((x,y),(y,x)) for a in (u,LD-u) for b in (v,LD-v)})
    coords=2*n+4;leaves=coords-1;size=1<<(leaves-1).bit_length();cells=leaves**2
    values=dict(sites_exact=n,rows_exact=len(d['entries']),coordinate_array_length_bound=coords,
      bisect_index_sum_bound=2*coords,tree_leaf_capacity_bound=size,tree_array_length_bound=2*size,
      tree_midpoint_sum_bound=2*size,cells_per_row_bound=cells,
      all_rows_cell_accumulator_bound=cells*len(d['entries']))
    assert 2*coords<2**31 and 2*size<2**31 and values['all_rows_cell_accumulator_bound']<2**53
    for k,v in values.items():assert row[k]==v;maxima[k]=max(maxima[k],v)
assert maxima==record['maxima']
print(json.dumps({'status':'PASS_INDEX_SIZES_98','maxima':maxima,'cpu_seconds':time.process_time()-start}))
