"""Read-only wrappers adding fail-closed assertions to the final admission reader.
The geometry is the reader's exact Fraction arithmetic, not a new solver.
"""
if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use replay_public.py for this check; outputs must be redirected.')
import contextlib, importlib, io, json, sys
from pathlib import Path
H=Path(__file__).resolve().parent.parent; ROOT=H.parents[4]
V=H.parent; PK=H/'runtime'
which=sys.argv[1]
if which in ('admission','selector'):
    sys.path.insert(0,str(H/'scripts'))
    import run_adm as a
    roots=['JQ','JPWS','JPW13','JG','JPA','JPG3m','JPG3p','JPG17m','JPG17p','JPG15m','JPG15p']
    if which=='admission':
        for root in roots:
            margin,failures=a.check_root(root,verbose=False)
            assert not failures,(root,failures)
            assert margin[0]>=0,(root,margin)
        print('PASS 11 exact root admissions, 17 labels each')
    else:
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            import extra as e
        for root in roots:
            slots={i:e.phys(s[0]) for i,s in a.spec(root).items()}
            assert len(slots)==17 and all(len(p)>=3 and e.diam2(p)<1 for p in slots.values()),root
            assert all(e.sep(slots[i],slots[j]) for i,j in e.itertools.combinations(slots,2)),root
            d,_=e.loadcls(a.basefile('L_3')[1]); hexagon=e.slots(e.cls(d,'M'))[0][0]
            assert e.diam2(e.phys(hexagon)+slots[12])<1,root
        assert e.cnt==84 and e.bad==[],(e.cnt,e.bad)
        print('PASS 84 selected triggers; 11 injective 17-slot assignments; marker union capacity')
elif which=='graph':
    dag=json.loads((H/'DEPENDENCY_GRAPH.json').read_text())
    h6=json.loads((H/'OBLIGATIONS.json').read_text())
    nodes={n['id']:n for n in dag['nodes']}
    assert len(nodes)==len(dag['nodes'])==328
    ancestors={};active=set()
    def walk(k):
        assert k in nodes and k not in active,k
        if k in ancestors:return ancestors[k]
        active.add(k);res=set()
        for p in nodes[k]['depends_on']:res.add(p);res.update(walk(p))
        active.remove(k);ancestors[k]=res;return res
    assert walk(dag['final_node'])==set(nodes)-{dag['final_node']}
    assert sum(len(n['depends_on']) for n in nodes.values())==1537
    ids={r['id'] for r in h6['rows']}
    assert len(ids)==len(h6['rows'])==210
    bound={n['h6_obligation_id']:n['id'] for n in nodes.values() if 'h6_obligation_id' in n}
    assert set(bound)==ids
    assert len([n for n in nodes.values() if 'h6_obligation_id' in n])==210
    assert all(r['evidence'] for r in h6['rows'])
    # Pure/applied decomposition is intentionally not asserted to be an H6 edge isomorphism.
    assert dag['h6_id_convention']
    print('PASS graph: 328 nodes, 1537 edges, 210 unique H6 bindings, all ancestors of FINAL')
else:raise ValueError(which)
