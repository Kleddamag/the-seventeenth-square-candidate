#!/usr/bin/env python3
"""Replay the full conditional local-optimality chain, with fixed inputs."""
import hashlib
import json
from pathlib import Path
import bridge
import relational
import rigidity

HERE=Path(__file__).resolve().parent


def main():
    path=HERE/'uniform-relational-projection.json'
    capture=relational.check(path)
    print(json.dumps(dict(stage='capture',**capture)),flush=True)
    transfer=bridge.run(path)
    if capture['certificate_sha256']!=transfer['contraction_certificate_sha256']:
        raise ValueError('capture/bridge digest mismatch')
    local=rigidity.check(HERE/'uniform-rigidity.json')
    if rigidity.F(transfer['maximum_transferred_radius'])>=rigidity.F(local['epsilon']):
        raise ValueError('bridge does not enter the rigidity radius')
    parameter_box=rigidity.initial()
    for name,index in zip(('a','b','z'),rigidity.u.PARAMETERS):
        if transfer['padded_parameter_box'][name]!=list(map(str,parameter_box[index])):
            raise ValueError('parameter-box mismatch')
    receipt=dict(status='PASS',capture=capture,bridge=transfer,rigidity=local,
                 source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py'))},
                 conclusion='Every physical packing with S<=S* in the stated rational neighbourhood and slider box has S=S* and its 16 non-rattler squares lie exactly on the endpoint family.',
                 global_status='OPEN: no theorem that arbitrary packings enter the neighbourhood and slider box.',
                 proof_status='Computer-assisted local proof, using hand-derived analytic inequalities and exact arithmetic; not proof-assistant formalized or independently peer reviewed.')
    (HERE/'proof-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',rigidity_ratio=local['ratio'],global_status=receipt['global_status'])),flush=True)


if __name__=='__main__':
    main()
