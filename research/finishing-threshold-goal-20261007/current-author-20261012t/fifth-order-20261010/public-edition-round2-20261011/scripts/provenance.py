"""Replay the current neutral capture records and exact saved inequalities.
Derived author verifier, not an independent implementation or a geometry sweep.
"""
if __name__ == '__main__' and not globals().get('_S17_PUBLIC_RUNNER_ACTIVE', False):
    raise SystemExit('Use the public replay runner so outputs are redirected.')
from pathlib import Path
import json
from new_capture_check import verify_new_captures, pin
HERE=Path(__file__).resolve().parent.parent
ROOT=HERE.parents[4]
result=verify_new_captures(ROOT/'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/CAPTURE_AUDIT_INPUTS.json',ROOT)
result['source']=pin(Path(__file__))
(HERE/'PROVENANCE_INDEX.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='statements'},indent=2))
