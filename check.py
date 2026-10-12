#!/usr/bin/env python3
"""check.py : the one command that checks this edition.

    python3 check.py              levels 0, 1 and 2
    python3 check.py --level 1    one level (0, 1 or 2)
    python3 check.py --only NAME  one check of level 2 (see --list)
    python3 check.py --list       names of the level-2 checks

Level 0: the environment.  Level 1: structure (every file and its SHA-256, the number of files, exact letter
case, no symbolic links, every {"file","sha256"} pin of the listed index files, the
fixed hashes of the root files, the values of EDITION_BINDINGS.json).  Level 2: cheap exact checks (the producers'
31 public checks, among them the one that re-decides every stored capture row; their equivalence check; the records
of the comparison with the earlier executions; the independent endpoint program; the stored outputs of the tree
executions).
Full recomputation (the 13 tree certificates, the capture rows) is described in CHECK.md and is not run here.

Standard library only.  One check of level 2 (endpoint_upper) needs SymPy (tested with 1.14.0):
`python3 -m pip install sympy==1.14.0`, or `python3 check.py --sympy-path DIR`.  Without it the result is FAIL
on that check only.  See CHECK.md.

The last line begins "CHECK RESULT:" and then one word.  PASS: levels 0, 1 and 2 were all run, every check ran,
nothing failed (exit code 0).  PARTIAL: nothing failed, but not everything was run: one level or one check only,
or checks NOT RUN because large files are absent, or checks TOO-SLOW (stopped on this machine by the CPU limit that
the producers' own script sets for itself, or by the time limit of their runner) (exit code 2).  FAIL: something failed (exit code 1).
A PARTIAL result is not a PASS of the edition.

What level 1 does not catch.  Every test of level 1 rests on this file.  The number of listed files and the number
of pins are fixed below (EXPECTED_FILES, EXPECTED_PINS) and printed by every run of level 1.  A changed file with a
changed manifest line fails, and so does an added file with an added manifest line, unless this file is changed as
well.  This file cannot fix its own hash: someone who changes files, MANIFEST.sha256 and check.py together can make
everything pass.  Only the comparison of the printed SHA-256 of MANIFEST.sha256 with the published value closes that.

Where this was run.  The project ran this script on one platform only, the one named in TESTED_ON below.
Other platforms (Linux, Windows, other versions of Python or SymPy) are untested.  The mapping of paths in the
wrapper of level 2 assumes "/" as path separator.
The script finds the edition root from its own location and reads only inside the edition.  It writes under
_check_out/ in the edition root.  The runner of the 31 public checks creates one new folder per check under
the producers' folder public_runs/ ; check.py moves that folder into _check_out/ as soon as the check
has ended.  No listed file is changed.  What a PASS means and what it does not mean: CHECK.md and KNOWN_LIMITS.md.
"""
import sys, os, json, hashlib, subprocess, time, re, csv, shutil, argparse, signal

ROOT = os.path.dirname(os.path.realpath(__file__))
# The root of the repository on the build machine, as the carried files write it.  Some carried data files contain it as
# a path prefix; it is mapped to the edition root when a check opens such a path, and never edited.  "builder" stands in
# these files where the name of the build account stood (KNOWN_LIMITS.md, "One substitution in carried files").
OLD = '/Users/builder/Developer/07-math-research/17-squares-certified-bound'
# Path-neutral substitution (KNOWN_LIMITS.md).  This script does not contain the two replaced strings and does not look for
# them.  It tests that every file that a table of substituted files lists has the SHA-256 that the table gives for it now
# (level 1, path-neutral-table).  It does not test the SHA-256 values before the substitution.
# PATH_NEUTRAL_TABLE: the table of the substituted files of the tree work (path, SHA-256 before, SHA-256 after), or None.
# A pin that names the SHA-256 that a file had BEFORE the substitution does not resolve.
PATH_NEUTRAL_TABLE = 'PATH_NEUTRAL.tsv'
W = 'local-research/claude-20261002/'
BK = 'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/'        # the producers' packet
CAP = 'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/'       # the capture computation (statements, slices, merged receipts, checker sources)
REVIEW_HASHES = 'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/4da8d938feaf76d8e85ad018ef1ed3512d95f77550401797c279226fcab9ecd6/REVIEW_HASHES.json'      # the hash table of the reading copies of the review reports
RECORD_HASHES = 'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/cce600b80d0d7df92da5fa5642dfce1e6576de15c2093adcbf0ecf8584092afa/RECORD_HASHES.json'      # the hash table of the reading copies of the 20 records of the tree work
RUN3 = 'local-research/claude-20261002/rerun-clean-20261011/'     # the records of the comparison with the earlier executions, and its programs and tables
TREES = ['JQ', 'JPG15p_v5', 'JPG17m_v5', 'JPG3m_v5', 'JPG3p_v5', 'JPG17p_v5', 'JPG15m_v5', 'G20S', 'HW', 'JG', 'JPWS_v4', 'JPW13', 'JPA_v5']
RERUN = W + 'results/rerun_trees_20261011/'
NEUTRAL = W + 'results/trees_neutral_20261011/'
HAS_NEUTRAL = True            # whether this build of the edition carries the third execution of the trees
RUNNER = 'replay_round2.py'             # the producers' runner of the public checks
ROOT_MARKER = 'AGENTS.md'              # a short neutral file; several check scripts find the root by this file name
TOP_SKIP = ('_check_out', '_large', 'MANIFEST.sha256', '.git')    # .git: the folder of a git working tree, never part of the edition
SYMPY_TESTED = '1.14.0'
# The one platform on which the project ran this script on this edition (written by the build from the machine it ran on).
TESTED_ON = 'macOS 27.0.1 (Darwin 27.0.0, arm64), CPython 3.9.6, Node.js v25.6.1, SymPy 1.14.0'
# The lines that the time command of the build machine appended to the stored outputs of the second tree execution have the form
# "<integer>  <label>".  These are all the labels that occur there.  Only a line with exactly one of these labels is left out
# when the outputs of the second and third execution are compared; any other line is compared.
RESOURCE_LABELS = (
    'maximum resident set size', 'average shared memory size', 'average unshared data size', 'average unshared stack size', 'page reclaims', 'page faults',
    'swaps', 'block input operations', 'block output operations', 'messages sent', 'messages received', 'signals received', 'voluntary context switches',
    'involuntary context switches', 'instructions retired', 'cycles elapsed', 'peak memory footprint')
TIMEOUT_SCALE = [1.0]                  # --timeout-scale N multiplies every time limit of level 2 (for slow machines)
RUNBOOK_IDS = ['endpoint_upper', 'partition', 'admission', 'selector', 'graph', 'capacity', 'frame', 'wall_triggers', 'loose_identities', 'provenance',
               'bc_composition', 'bd_binding', 'bfbe_pins', 'finite_1', 'finite_2', 'finite_3', 'finite_4', 'finite_join', 'normalized_prefix',
               'normalized_finish', 'root_stops', 'root_stop_binding', 'entry_transfer', 'entry_binding', 'small_entry', 'selection_binding',
               'root_chart_transfer', 'analytic_gate', 'normalized_five_rounds', 'normalized_sixth_round', 'endpoint_enclosure']
# Files whose SHA-256 is fixed HERE: the root files that the producers' PUBLIC_ARTIFACT_ROOTS.json names, that list, their
# manifest PART2_MANIFEST.json and checksum list PART2_SHA256SUMS, the stored output of their seal check, their runner,
# stored replay results and index files, and the tables, documents and scripts of this edition that no other pin covers.
FIXED_SHA256 = {
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_INPUTS.tsv': 'ae3967cb3477a21044d802c13316a17ef84423ecf089c3d3e703aaf5c9cc2065',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EVIDENCE_EQUIVALENCE.json': 'e59573e9b2aa8d60dbc98618d16562ec935456a93b2e078c3062c027b27d5cdf',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/runbook_public.json': 'ef3be16448f277f0b25aa4229f8429bf4c471161b92bb327725541c985a084f0',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/replay_round2.py': '9ed6b55cf58a30fb6b1e772e51a6fdd5baf82962efb8a8aa1f7010d3ca5c2188',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/check_equivalence.py': 'cbf0aa017afd520429bf3f05ed9a2f01230f9310b0be09f69fe06f968b888664',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EQUIVALENCE.md': '5396cf84fd379cf6c4da115a667692ef260ac2f35a7b682c8487c88092651e38',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_REPLAY_RESULTS.json': '099fddb296eac6e6b4dcfe84dc18589a921d8b825d71ccf560b9f6a47e54b732',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITION.json': '76cfc5f4e41961741a7a84df8b6da7302b932cfdbd42aabfd80aa2513970907c',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/revision-v7/PROOF.md': '0d4c408d1e38a8d858281443b27ac4e0cf3591ba9045be8e8ec176a318916ee6',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/revision-v7/LABELS.tsv': '8c2eea257aa3d32d850b9f2468e606ec174ce7f36ae93ea301ef124e2250fffb',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/LABELS_PUBLIC.tsv': '8c2eea257aa3d32d850b9f2468e606ec174ce7f36ae93ea301ef124e2250fffb',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/REVISION_SCOPE.json': '6808db182d20c6f266a35163aadcce8e6ea3be6599a996e650f57acd27b073b9',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/RELEASE_CHECK_ASSESSMENT.json': '0f59fcde2eeaaadb368899b25e137767d8bdeaf607567ac1482bd5e053c1ee48',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/AUTHOR_SEAL_CHECK.out': 'eb4c0f936167b78b5839f71a7574571dde3de04c53dc417526f97fa0cc756ee5',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_POLICY.json': '8bf0a6e240fc7d45e1ca100188cc6872692914f9a8120e9c2abd0abe778d15db',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL.tsv': '0c489e6e341f889d8d6ed0ff3b2f72e408b63741c4f8a05abd81c2b638796151',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_REPLAY.tsv': '2b8397f52e1fccd120e9649d87128630a627a78a1dc55a49892d1bd1e44b556f',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_REFERENCE_BINDINGS.json': 'c0b5dba0ca6838557f78fb6f7c7a92e574b8c02f69fba0c908e9c3ba7eba0400',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_READERS.json': 'bdccde718851d394b70db0215d056678c0044c350b1ae58d0f967a8fff3192e1',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_CHECK_SCOPE.md': '32b088ada6975b2c9180f463ae08b0d2850de6110f0b894faa9d45c740a2a39d',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_LOCATOR_CHANGE.json': '1847578ae4044e2d9f41495efc723391bde4ac27c70cac9bbb4c159e422ab906',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/CURRENT_READ_CLOSURE.json': 'a95e2fd0986d027acc88710942eaeeba7c1f1b6e64c99cd12d4df61e8593ac70',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/READING_COPY_INDEX.json': '93a21c7cbdc75eb436a1f26ffaf13c0126d6813a53d55425c9e44ebf21fbe5fa',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITORIAL_EXTRACTS.json': '806fc5cce84e493107d5151143cdbe3609634a9c51a4a567f0f9095f7b6b89a8',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITORIAL_LINE_EDITS.json': '534afaa4eb368c44ef6efc844ab33a26778399b30e78af4795161563a5ab33dd',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/KNOWN_LIMITS.md': 'caa79a6662be09b8d5a58587b9021169e945d9d8e6a55486810958ae96d9741a',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_ARTIFACT_ROOTS.json': '0f22e7cc80864500720a1cf3776989a3e67033736be7afc6c5c7dd6bd8208dad',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PART2_MANIFEST.json': '09222d9c67e6c92ac541b5bc7819af63226b080d6bd41ad90876cf96691ad1af',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PART2_SHA256SUMS': '8586b7ec7ca7aaf720dcfb7822466535e02962f6dad5ef0dbef4eedab51bc01b',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/CHECK_MAP.tsv': 'c106e418712cc3c0ab88e920b0effcef4721d46b5d1e8be4b3dc9d1dd0dbc02f',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_PATH_ALIASES.json': 'ba365dd21471ca5f69dabf94ea3dff32e663d8a45573f3ebd31abe3a7361103a',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/CURRENT_BINDINGS.json': '8de64fdd01c1d306fff1ca461bf8aa230c19d82e93dcca9e84e590ff397ca4c1',
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/CAPTURE_AUDIT_INPUTS.json': '239f25d7731eab5bd8a87b0a656b572abb85bb11bb4d9f2cfa67f194dd9bb92a',
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/4da8d938feaf76d8e85ad018ef1ed3512d95f77550401797c279226fcab9ecd6/REVIEW_HASHES.json': '902d1e217c42161ebd338ade6b6f22df82b94e5b5634ac550e32d0a6aafff311',
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/cce600b80d0d7df92da5fa5642dfce1e6576de15c2093adcbf0ecf8584092afa/RECORD_HASHES.json': '029aed5495812e2be0f565cd45f5d38b899a7c2662db3ee676e3e84c5acc243c',
    'local-research/claude-20261002/rerun-clean-20261011/records/_calls/k19/SUMMARY.tsv': 'efa432d7566ecea3cff6844321466df0a867b54d2d6b0a37f0e6e050480d8bf9',
    'independent/endpoint_enclosure/own_endpoint_enclosure.py': '11b0a7fbdbe6fdaf77714ef0e64705c9a23ad59888a2595d31dda97f1c35fac2',
    'LARGE_FILES.tsv': '9a01cac28d3377a2ce900b92a99688890d6831d62e767c08d07da0daa12f28cb',
    'check_comparison_records.py': '7661dc730087b9b72724e2096c0d0eefff6a5f3c7652cd6f7f9841a56f538208',
    '.gitattributes': '705fd4d6451a31d36b3df7de96f83f30ac976c9b4a6d1e51671d8e2f33e2d0da',
    '.gitignore': '6e787cf404c7f8d584c3d7e96fdc348a420769ee5259219750e92c0db4bf0895',
    'AGENTS.md': '204ee3607a119d7e81c7274382f1e52454fae62f55f8b4b6b6c19eef9d9f68e4',
    'AUDIT.md': '2775fd1f068eae0224047fda85c08b8dac49ebb3aac771478c9cca6ef4a5a52e',
    'CHANGELOG.md': '4910f79a4e8e6c3a861af613fc0fa4c60ec7f6d2e0f868caeab93fe1bc782a6c',
    'CHECK.md': '603303a19866f73f4e85767fd15315827ab66d95cae3cef020e311a7d6cf75b5',
    'CITATION.cff': '899e0457883915f6c52144deba9862063cc810cc1e4b5e0f5bc9cd4ad69a9971',
    'CREDITS.md': 'fab3b10b36da9842d0f6168ff7b080da50449028d1d116d62995326a5eeda9c8',
    'KNOWN_ISSUES.md': 'a0efb95b96208579601093043602ce306a6c53cd460a12205d8d9ce9df02acb6',
    'KNOWN_LIMITS.md': 'a16dd278828ecdca1745225c17f27338986f8422c6508950f1742fbe618ba8cb',
    'OVERVIEW.md': '9cde99e86458484ac288ae5d80450d556182125e2400f9b5345ba966edce2edd',
    'PATH_NEUTRAL.tsv': '0fa1cbee4c050ece010e5c13fcbd3bd8ba5a3118394607501c7ca4aeff2f8411',
    'PREMISES.md': 'b7a1acd23e90f829a6a4bc956e7a9b06402da0cb4a0bc510ef7656dd83a6da22',
    'PROOF.md': '0d4c408d1e38a8d858281443b27ac4e0cf3591ba9045be8e8ec176a318916ee6',
    'READING_ORDER.md': 'c395d6ce6a66f9075acdd8e5381f783ff15ddb3e39299c87a4998a8f62ea6151',
    'README.md': '98601bedc0b895fe7c515c28ac11bd52b5c2fc044d305da321fa7e9e56254aec',
    'STATEMENT.md': 'dd73365b0681f0efb00e351f89a1dcb1f80a8e758d44563b1e5e81f851521870',
    'STATEMENT_STATUS.md': '411616c8dd76bca5b29d66790cc805deb4b3c44f9cbbe35edfbfb39f59cae578',
    'THIRD_PARTY.md': '5d85a00ff275d972301a4daf246c21f98b6d340272ee01d43c18457d0d9933c0',
    'fetch_large.py': '8fa66c65de94e3bf0041a4ec72844ca55d26402c1ea6f71e3ce71f57ee57fb22',
    'packing.png': '2851e9d8fb0edcf5532277aec5ee91ebeeb90b09b4003d5213a3a4c4c8e8380c',
    'recompute_slice.py': 'd6d887911d480ea24639facbd6cf304b54ab38af8d2c96c9e7c15363cd81e47d',
    'upper-packing-certificate.json': '24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7',
    'independent/endpoint_enclosure/README.md': '0cda5863e8738edd4d5136dea34ca4c73ed89a53af15def9a93193b2b86165e0',
    'independent/endpoint_enclosure/out_control.txt': '1f50e54f6f78d3bfa9ec98878f07376de0a94869e263a807c522400db0e6a4b9',
    'independent/endpoint_enclosure/out_real.txt': '6007f487174af622b1184f0d5522a757d35578dd6b3e546df8ee9f410c0679a7',
}
ROOT_FILES = [
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_INPUTS.tsv',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EVIDENCE_EQUIVALENCE.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/runbook_public.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/replay_round2.py',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/check_equivalence.py',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EQUIVALENCE.md',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_REPLAY_RESULTS.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITION.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/revision-v7/PROOF.md',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/revision-v7/LABELS.tsv',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/LABELS_PUBLIC.tsv',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/REVISION_SCOPE.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/RELEASE_CHECK_ASSESSMENT.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/AUTHOR_SEAL_CHECK.out',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_POLICY.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL.tsv',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_REPLAY.tsv',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_REFERENCE_BINDINGS.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_READERS.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_CHECK_SCOPE.md',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PATH_NEUTRAL_LOCATOR_CHANGE.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/CURRENT_READ_CLOSURE.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/READING_COPY_INDEX.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITORIAL_EXTRACTS.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITORIAL_LINE_EDITS.json',
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/KNOWN_LIMITS.md',
]
# The number of files MANIFEST.sha256 must list.  Any other number fails.
EXPECTED_FILES = 7118
# The pins of this edition, by index file: (number of pins, of which resolved by a large file).  Any other counts fail.
EXPECTED_PINS = {
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PART2_SHA256SUMS': [6754, 12],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PART2_MANIFEST.json': [6753, 12],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_ARTIFACT_ROOTS.json': [26, 0],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/PUBLIC_INPUTS.tsv': [6748, 12],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EDITION.json': [3, 0],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/CURRENT_BINDINGS.json': [1, 0],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/OBLIGATIONS.json': [1288, 10],
    'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/revision-v7/LABELS.tsv': [278, 11],
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/CAPTURE_AUDIT_INPUTS.json': [101, 0],
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/4da8d938feaf76d8e85ad018ef1ed3512d95f77550401797c279226fcab9ecd6/REVIEW_HASHES.json': [29, 0],
    'research/finishing-threshold-goal-20261007/clean-rerun-20261011/reseal-resume-1120/graphs/objects/cce600b80d0d7df92da5fa5642dfce1e6576de15c2093adcbf0ecf8584092afa/RECORD_HASHES.json': [20, 0],
    'LARGE_FILES.tsv': [12, 12],
}
# Every other listed file below the top level (no pin and no fixed hash names it): their number, and the SHA-256 of the
# lines "<sha256>  <path>" of these files in path order.  Any other value fails.
EXPECTED_REST = [344, '6763e3b274c4cb484ee90aea31826e5bed3db47a235b6e36e7aa4ec0778a7c79']
EXPECTED_COMPARISON = 'COMPARISON RECORDS RESULT: PASS (98 statements, each IDENTICAL in its record; the stored side is not in this edition and is not tested)'
# The status words that the output of each public check must contain, and no others (status_words below).  They are the words of the
# producers' stored output of the same check.  Some read like a failure and are the expected outcome of that check (CHECK.md).
EXPECTED_STATUS = {
    'endpoint_upper': ['PASS_INDEPENDENT_EXACT_S_STAR_17_SQUARE_FEASIBILITY'],
    'partition': ['PASS_EXACT_GUARD_PARTITION_ON_ALL_SIGN_ATOMS'],
    'admission': [],
    'selector': [],
    'graph': [],
    'capacity': ['PASS_EXACT_CAPACITY_CURRENT_ESCAPES_FRAME_INCLUSION_AND_DERIVED_GATE'],
    'frame': ['PASS_FIXED_FRAME_WALL_ENDS_AND_T2_ENTRY'],
    'wall_triggers': ['PASS_ALL_29_WALL_TRIGGER_LITERALS'],
    'loose_identities': [],
    'provenance': ['PASS_ALL_98_NEW_CAPTURE_RECORDS_AND_EXACT_MINIMUM_DECISIONS'],
    'bc_composition': [],
    'bd_binding': [],
    'bfbe_pins': ['PASS_PUBLIC_BINDINGS'],
    'finite_1': ['PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED'],
    'finite_2': ['PASS_EXACT_FINITE_PARTIAL_CONTRACTION_TARGET_NOT_REACHED'],
    'finite_3': ['PASS_EXACT_FINITE_COMPLETED_PREFIX_PARTIAL_ROUND_EXCLUDED_TARGET_NOT_REACHED'],
    'finite_4': ['PASS_EXACT_FINITE_ENTRY_TO_ACCEPTED_RATIONAL_THEOREM'],
    'finite_join': [],
    'normalized_prefix': ['ACCEPTED_STOPPED_PROPAGATION_INCONCLUSIVE'],
    'normalized_finish': ['ACCEPTED_STRICT_NORMALIZED_STOPPED_CONTRACTION'],
    'root_stops': [],
    'root_stop_binding': ['ACCEPTED_G20S_BROAD_ROOT_STOP_THEOREM'],
    'entry_transfer': [],
    'entry_binding': ['ACCEPTED_GUARDED_RAW_ENTRY_STOP_PRUNING'],
    'small_entry': ['ACCEPTED_RATIONAL_SMALL_ENTRY_COROLLARY'],
    'selection_binding': [],
    'root_chart_transfer': ['PASS_INDEPENDENT_SOURCE_AND_CONDITIONAL_CONSTANT_ASSESSMENT'],
    'analytic_gate': ['PASS_INDEPENDENT_COMPLETE_ROOT_ANALYTIC_GATE'],
    'normalized_five_rounds': ['ACCEPTED_FIVE_ROUND_OLD_WEIGHT_REUSE_INCONCLUSIVE'],
    'normalized_sixth_round': ['ACCEPTED_SIX_NORM_FACES_ELIMINATED_ONE_REMAINS'],
    'endpoint_enclosure': ['PASS_TIGHT_ENDPOINT_ENCLOSURE'],
}
# The producers' own file of the statuses that read like a failure (check id -> expected_status, explanation), or None if their packet has none.
# Where it names a check, the status words of that check must be the word it gives AND the words fixed above; if the two differ, nothing is run.
STATUS_FILE = 'research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/EXPECTED_INTERMEDIATE_STATUSES.json'
# SHA256_ALL.txt of the second tree execution: how many of its 71 entries name the SHA-256 that a file had before the path-neutral substitution.
EXPECTED_BEFORE_IN_SHA256_ALL = 55
# The number of checks of level 2.  A run of all levels is PASS only if exactly this many checks were carried out.
EXPECTED_CHECKS = 41
INDEPENDENT_EXPECTED = 'RESULT: PROVED  unique root in the statement box; root in X*; L strictly inside the packet and gate'
IGNORED_NAMES = ('.DS_Store',)          # made by the Mac's file browser; never part of the edition

VERBOSE = False
results = []        # (level, name, status, text)
counts = {'files': 0, 'pins': 0, 'checks': 0}
notrun = []
tooslow = []        # checks that were stopped by the CPU limit of their own script or by the time limit of the producers' runner: not run to the end on this machine


def say(level, name, status, text=''):
    results.append((level, name, status, text))
    print('L%d %-7s %-26s %s' % (level, status, name, text))
    sys.stdout.flush()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 22), b''):
            h.update(block)
    return h.hexdigest()


def p(rel):
    return os.path.join(ROOT, *rel.split('/'))


def exact_exists(rel):
    """True only if every component of rel is in its directory listing with exactly these letters."""
    cur = ROOT
    for part in rel.split('/'):
        try:
            if part not in os.listdir(cur):
                return False
        except (NotADirectoryError, FileNotFoundError):
            return False
        cur = os.path.join(cur, part)
    return os.path.isfile(cur)


def read_manifest():
    out = {}
    with open(p('MANIFEST.sha256'), encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip('\n')
            m = re.match(r'^([0-9a-f]{64})  (.+)$', line)
            if not m:
                raise ValueError('MANIFEST.sha256 line %d is not "<sha256>  <path>"' % n)
            if m.group(2) in out:
                raise ValueError('MANIFEST.sha256 lists %s twice' % m.group(2))
            out[m.group(2)] = m.group(1)
    return out


def read_large():
    out = {}
    with open(p('LARGE_FILES.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            out[r['path']] = r
    return out



def large_location(rel):
    """Where a large file is: its mirror path first, then _large/.  None if it is not present."""
    if exact_exists(rel):
        return p(rel)
    if exact_exists('_large/' + rel):
        return p('_large/' + rel)
    return None


def read_pn_table():
    """The declared table of the files of this edition that are carried as substituted copies: path -> (SHA-256 before, SHA-256 after)."""
    if not PATH_NEUTRAL_TABLE or not exact_exists(PATH_NEUTRAL_TABLE):
        return {}
    with open(p(PATH_NEUTRAL_TABLE), encoding='utf-8') as f:
        return {r['path']: (r['sha256_before'], r['sha256_after']) for r in csv.DictReader(f, delimiter='\t')}


def walk_tree():
    files, links, ignored = [], [], 0
    stack = ['']
    while stack:
        rel = stack.pop()
        for name in os.listdir(os.path.join(ROOT, rel) if rel else ROOT):
            if not rel and name in TOP_SKIP:
                continue
            r = rel + '/' + name if rel else name
            full = p(r)
            if os.path.islink(full):
                links.append(r)
            elif os.path.isdir(full):
                stack.append(r)
            elif name in IGNORED_NAMES:
                ignored += 1
            else:
                files.append(r)
    return files, links, ignored


# ----------------------------------------------------------------------------------------------- level 0
ROOT_NAME_MESSAGE = "rename the edition folder or one of its parent folders: the folder name %r occurs twice in the path (the producers' runner splits a path at the first occurrence of that name, and every public check would fail with \"No such file\")"


def root_name_twice():
    # the producers' runner splits a path at the first occurrence of '/<name of the root folder>/': the name must not occur a second time higher up
    name = os.path.basename(ROOT.rstrip('/' + os.sep)); above = os.path.dirname(ROOT.rstrip('/' + os.sep)).replace(os.sep, '/') + '/'
    return name if ('/' + name + '/') in above else None


def level0(args=None):
    ok = True
    v = sys.version_info
    good = v >= (3, 9)
    say(0, 'python', 'PASS' if good else 'FAIL', 'Python %d.%d.%d (3.9 or newer is needed)' % (v[0], v[1], v[2]))
    ok &= good
    if not __debug__:
        say(0, 'python-assertions', 'FAIL', 'do not run with -O or -OO: the checks use assert'); ok = False
    import platform
    say(0, 'platform', 'INFO', 'this machine: %s, %s %s. The project ran this check on one platform only: %s. Other platforms are untested.'
        % (platform.platform(), platform.python_implementation(), platform.python_version(), TESTED_ON))
    st = self_test()
    say(0, 'self-test', 'PASS' if not st else 'FAIL', 'the comparison of two outputs keeps a line "123  unresolved constraints" and leaves out only the %d listed resource lines' % len(RESOURCE_LABELS) if not st else '; '.join(st))
    ok &= not st
    node = shutil.which('node')
    if node:
        try:
            ver = subprocess.run([node, '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=30).stdout.strip()
        except Exception as e:
            ver = 'version not read (%s)' % e
        say(0, 'node', 'PASS', 'Node.js %s found (levels 0 to 2 do not run it; a full recomputation needs it)' % ver)
    else:
        say(0, 'node', 'WARN', 'Node.js not found (levels 0 to 2 do not need it; a full recomputation does)')
    if args is not None:
        found = sympy_python(args)
        if found and found[2] == SYMPY_TESTED:
            say(0, 'sympy', 'PASS', 'SymPy %s found (the version this edition was tested with)' % found[2])
        elif found:
            say(0, 'sympy', 'WARN', 'SymPy %s found; this edition was tested with SymPy %s only' % (found[2], SYMPY_TESTED))
        else:
            say(0, 'sympy', 'MISSING', 'SymPy cannot be imported, so one check of level 2, endpoint_upper (the upper bound), cannot run and the result will be FAIL. '
                'Supply it in one of two ways: `python3 -m pip install sympy==1.14.0`, or `python3 check.py --sympy-path DIR` (DIR holds the sympy and mpmath packages). Tested with SymPy %s.' % SYMPY_TESTED)
    need = ['STATEMENT.md', 'MANIFEST.sha256', 'LARGE_FILES.tsv', 'EDITION_BINDINGS.json', ROOT_MARKER, BK + 'PUBLIC_ARTIFACT_ROOTS.json', BK + 'PART2_SHA256SUMS', BK + 'runbook_public.json']
    missing = [x for x in need if not exact_exists(x)]
    say(0, 'edition-root', 'PASS' if not missing else 'FAIL', ROOT if not missing else 'not an edition root, missing: ' + ', '.join(missing))
    if missing:
        return False
    twice = root_name_twice()
    say(0, 'root-name', 'PASS' if not twice else 'FAIL', ('the folder name %r occurs once in the path of the edition' % os.path.basename(ROOT.rstrip('/' + os.sep))) if not twice else ROOT_NAME_MESSAGE % twice)
    if twice:
        return False
    return ok


# ----------------------------------------------------------------------------------------------- level 1
def collect_pins(obj, pointer, out):
    if isinstance(obj, dict):
        f, h = obj.get('file'), obj.get('sha256')
        if isinstance(f, str) and 'sha256' in obj:
            # a pin-shaped object whose hash is not 64 lowercase hex digits is kept and reported as malformed
            out.append((pointer, f, h if isinstance(h, str) and re.match(r'^[0-9a-f]{64}$', h) else None))
        for k, v in obj.items():
            collect_pins(v, pointer + '/' + str(k), out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            collect_pins(v, pointer + '/' + str(i), out)


HEX64 = re.compile(r'^[0-9a-f]{64}$')


def pins_of(source):
    """The pins of one index file as (where, file, sha256 or None, bytes or None)."""
    out = []
    if source.endswith('SHA256SUMS'):
        with open(p(source), encoding='utf-8') as f:
            for n, line in enumerate(f, 1):
                m = re.match(r'^(\S+)  (.+)$', line.rstrip('\n'))
                out.append(('line %d' % n, m.group(2) if m else '', m.group(1) if m and HEX64.match(m.group(1)) else None, None))
    elif source.endswith('.json'):
        raw = []
        collect_pins(json.load(open(p(source), encoding='utf-8')), '', raw)
        out = [(ptr, f, h, None) for ptr, f, h in raw]
    else:
        with open(p(source), encoding='utf-8') as f:
            for n, r in enumerate(csv.DictReader(f, delimiter='\t'), 2):
                name = r.get('file') if 'file' in r else r.get('path')
                h = r.get('sha256')
                if not name and not h:
                    continue
                out.append(('line %d' % n, name or '', h if h and HEX64.match(h) else None, int(r['bytes']) if (r.get('bytes') or '').isdigit() else None))
    return out


PIN_SOURCES = [BK + 'PART2_SHA256SUMS', BK + 'PART2_MANIFEST.json', BK + 'PUBLIC_ARTIFACT_ROOTS.json', BK + 'PUBLIC_INPUTS.tsv', BK + 'EDITION.json', BK + 'CURRENT_BINDINGS.json', BK + 'OBLIGATIONS.json', BK + 'revision-v7/LABELS.tsv', CAP + 'CAPTURE_AUDIT_INPUTS.json',
               REVIEW_HASHES, RECORD_HASHES, 'LARGE_FILES.tsv']


UNBOUND = ('check.py', 'EDITION_BINDINGS.json')     # bound by the manifest only: check.py cannot fix its own hash


def rest_files(listed, pinned):
    return sorted(r for r in listed if r not in pinned and r not in FIXED_SHA256 and r not in UNBOUND)


def level1():
    ok = True
    t0 = time.time()
    say(1, 'expected', 'INFO', 'this edition has %d listed files and %d pins in %d index files; both numbers are fixed in check.py and any other number fails. What level 1 does not catch: see the head of check.py and CHECK.md'
        % (EXPECTED_FILES, sum(v[0] for v in EXPECTED_PINS.values()), len(EXPECTED_PINS)))
    try:
        manifest = read_manifest(); large = read_large()
    except Exception as e:
        say(1, 'read-lists', 'FAIL', str(e)); return False
    # 1. the file list, with exact letter case
    files, links, ignored = walk_tree()
    on_disk = set(files); listed = set(manifest)
    lower = {}
    for r in on_disk:
        lower.setdefault(r.lower(), []).append(r)
    missing = sorted(listed - on_disk)
    extra = sorted(on_disk - listed)
    for m in missing[:40]:
        other = [x for x in lower.get(m.lower(), []) if x != m]
        say(1, 'file-list', 'FAIL', 'listed but not present: %s%s' % (m, (' (present under another letter case: %s)' % ', '.join(other)) if other else ''))
    for x in extra[:40]:
        hint = ' (a folder left by an interrupted run of a public check; remove it)' if x.startswith(BK + 'public_runs/') else ''
        say(1, 'file-list', 'FAIL', 'present but not listed in MANIFEST.sha256: ' + x + hint)
    for x in links[:40]:
        say(1, 'file-list', 'FAIL', 'symbolic link in the edition: ' + x)
    bad_list = bool(missing or extra or links)
    if len(missing) > 40 or len(extra) > 40:
        say(1, 'file-list', 'FAIL', '... %d listed files not present and %d files not listed in all' % (len(missing), len(extra)))
    if not bad_list:
        say(1, 'file-list', 'PASS', '%d files listed, %d present, none missing, none unlisted, no symbolic link, letter case exact%s'
            % (len(listed), len(on_disk & listed), ('; %d .DS_Store ignored' % ignored) if ignored else ''))
    ok &= not bad_list
    if len(listed) != EXPECTED_FILES:
        say(1, 'file-count', 'FAIL', 'MANIFEST.sha256 lists %d files; this edition has %d' % (len(listed), EXPECTED_FILES)); ok = False
    else:
        say(1, 'file-count', 'PASS', 'MANIFEST.sha256 lists the %d files fixed in check.py' % EXPECTED_FILES)
    # 2. the hashes
    wrong = []
    truth = {}
    for rel in sorted(listed & on_disk):
        h = sha256_file(p(rel)); truth[rel] = h
        if h != manifest[rel]:
            wrong.append(rel)
    for x in wrong[:40]:
        say(1, 'file-hash', 'FAIL', 'sha256 differs from MANIFEST.sha256: ' + x)
    if not wrong:
        say(1, 'file-hash', 'PASS', '%d files have the listed sha256' % len(truth))
    ok &= not wrong
    counts['files'] = len(truth)
    # 3. the large files (kept outside the manifest; listed with their hashes in LARGE_FILES.tsv)
    present = absent = 0; bad_large = []
    for rel, row in sorted(large.items()):
        loc = large_location(rel)
        if loc is None:
            absent += 1; continue
        present += 1
        if sha256_file(loc) != row['sha256'] or os.path.getsize(loc) != int(row['bytes']):
            bad_large.append(rel)
    stray = []
    large_links = ['_large'] if os.path.islink(p('_large')) else []
    if os.path.isdir(p('_large')):
        for d, ds, fs in os.walk(p('_large')):
            for x in ds + fs:
                if os.path.islink(os.path.join(d, x)):
                    large_links.append('_large/' + os.path.relpath(os.path.join(d, x), p('_large')).replace(os.sep, '/'))
            for f in fs:
                r = os.path.relpath(os.path.join(d, f), p('_large')).replace(os.sep, '/')
                if r not in large and f not in IGNORED_NAMES:
                    stray.append('_large/' + r)
    for x in sorted(stray)[:40]:
        say(1, 'large-files', 'FAIL', 'file under _large/ that LARGE_FILES.tsv does not list: ' + x)
    for x in sorted(large_links)[:40]:
        say(1, 'large-files', 'FAIL', 'symbolic link under _large/: ' + x)
    for x in bad_large:
        say(1, 'large-files', 'FAIL', 'present with another sha256 or size: ' + x)
    both = sorted(x for x in large if x in on_disk)
    for x in both:
        say(1, 'large-files', 'FAIL', 'a large file is also listed in the tree: ' + x)
    if not (bad_large or stray or large_links or both):
        say(1, 'large-files', 'PASS', '%d large files listed: %d present with the listed sha256 and size, %d not present (not a failure; see LARGE_FILES.tsv)'
            % (len(large), present, absent))
    ok &= not (bad_large or stray or large_links or both)
    # 5. every pin of the index files resolves: the file is in the edition with exactly that sha256 (and size, where the index gives one)
    got = {}; unresolved = []; pinned = set(); pn_table = read_pn_table()
    if pn_table:
        wrong_t = sorted(k for k, v in pn_table.items() if truth.get(k) != v[1])
        # the producers' table of the same kind, for the files of their packet: every file it names as current has the SHA-256 it gives
        n_theirs = 0
        try:
            if exact_exists(BK + 'PATH_NEUTRAL.tsv'):
                with open(p(BK + 'PATH_NEUTRAL.tsv'), encoding='utf-8') as f:
                    for r in csv.DictReader(f, delimiter='\t'):
                        n_theirs += 1
                        if truth.get(r['current_file']) != r['current_sha256']:
                            wrong_t.append(r['current_file'])
        except Exception as e:
            wrong_t.append('%sPATH_NEUTRAL.tsv cannot be read: %s' % (BK, e))
        if wrong_t:
            say(1, 'path-neutral-table', 'FAIL', '%d file(s) do not have the SHA-256 that a table of substituted files gives for them now: %s' % (len(wrong_t), ', '.join(wrong_t[:5]))); ok = False
        else:
            say(1, 'path-neutral-table', 'PASS', 'the %d files that %s lists and the %d that the producers\' PATH_NEUTRAL.tsv lists have the SHA-256 that these tables give for them now (the values before the substitution are not tested here)' % (len(pn_table), PATH_NEUTRAL_TABLE, n_theirs))
    for src in PIN_SOURCES:
        try:
            pins = pins_of(src)
        except Exception as e:
            say(1, 'pins', 'FAIL', 'cannot read %s: %s' % (src, e)); ok = False; got[src] = None; continue
        n_large = 0
        for where, f, h, size in pins:
            pinned.add(f)
            if h is None:
                unresolved.append('%s %s -> %s : malformed, the sha256 value is not 64 lowercase hex digits' % (src, where, f)); continue
            if truth.get(f) == h and (size is None or os.path.getsize(p(f)) == size):
                continue
            if f in large and large[f]['sha256'] == h and (size is None or int(large[f]['bytes']) == size) and f not in bad_large:
                n_large += 1; continue
            unresolved.append('%s %s -> %s %s : %s' % (src, where, f, h[:16], (('the file has sha256 %s' % truth[f][:16]) + ('; %s lists this file, and the pin names the sha256 it had before the substitution' % PATH_NEUTRAL_TABLE if f in pn_table and pn_table[f][0] == h else '')) if f in truth else 'no such file in the edition'))
        got[src] = [len(pins), n_large]
        counts['pins'] += len(pins)
    for x in unresolved[:40]:
        say(1, 'pins', 'FAIL', 'pin not resolved: ' + x)
    if len(unresolved) > 40:
        say(1, 'pins', 'FAIL', '... %d pins not resolved in all' % len(unresolved))
    if not unresolved and all(v is not None for v in got.values()):
        say(1, 'pins', 'PASS', '%d pins in %d index files, every one resolves to a file of this edition with the pinned sha256 (%d of them to a large file by its listed hash): %s'
            % (counts['pins'], len(PIN_SOURCES), sum(v[1] for v in got.values()), '; '.join('%s %d' % (s.split('/')[-1], got[s][0]) for s in PIN_SOURCES)))
    ok &= not unresolved
    if got != EXPECTED_PINS:
        say(1, 'pin-counts', 'FAIL', 'pin counts by index file (pins, of which large) are %s; this edition has %s' % (json.dumps(got, sort_keys=True), json.dumps(EXPECTED_PINS, sort_keys=True))); ok = False
    else:
        say(1, 'pin-counts', 'PASS', 'the pin counts are the ones fixed in check.py')
    # 5b. the files that no pin and no fixed hash covers are bound by one digest
    rest = rest_files(listed, pinned)
    dg = hashlib.sha256(''.join('%s  %s\n' % (truth.get(r, ''), r) for r in rest).encode('utf-8')).hexdigest()
    if [len(rest), dg] != EXPECTED_REST:
        say(1, 'rest-digest', 'FAIL', 'the %d listed files that no pin and no fixed hash covers have the digest %s; this edition has %d files with %s' % (len(rest), dg[:16], EXPECTED_REST[0], EXPECTED_REST[1][:16])); ok = False
    else:
        say(1, 'rest-digest', 'PASS', '%d listed files that no pin and no fixed hash covers have the digest fixed in check.py' % len(rest))
    # 6. the fixed hashes
    wrong_fixed = [rel for rel, h in sorted(FIXED_SHA256.items()) if truth.get(rel) != h]
    declared = None
    try:
        declared = {x['file']: x['sha256'] for x in json.load(open(p(BK + 'PUBLIC_ARTIFACT_ROOTS.json'), encoding='utf-8'))['roots']}
    except Exception:
        pass
    if wrong_fixed or declared != {r: FIXED_SHA256.get(r) for r in ROOT_FILES}:
        say(1, 'fixed-hashes', 'FAIL', 'not the sha256 fixed in check.py: ' + (', '.join(wrong_fixed) or 'the list of the root files')); ok = False
    else:
        say(1, 'fixed-hashes', 'PASS', '%d files have the sha256 fixed in check.py, among them the %d root files that PUBLIC_ARTIFACT_ROOTS.json names, that list, and the producers\' manifest and checksum list' % (len(FIXED_SHA256), len(ROOT_FILES)))
    # 6c. the top-level PROOF.md is a byte copy of the proof text of the producers' packet
    if exact_exists('PROOF.md') and truth.get('PROOF.md') == truth.get(BK + 'revision-v7/PROOF.md') == FIXED_SHA256.get(BK + 'revision-v7/PROOF.md'):
        say(1, 'proof-copy', 'PASS', 'PROOF.md at the top level has the bytes of the proof text %srevision-v7/PROOF.md (sha256 %s...)' % (BK, truth['PROOF.md'][:16]))
    else:
        say(1, 'proof-copy', 'FAIL', 'PROOF.md at the top level is missing or does not have the bytes of %srevision-v7/PROOF.md' % BK); ok = False
    # 7. EDITION_BINDINGS.json states what this script enforces: every file it names has the sha256 it gives, and that
    #    sha256 is the one fixed above; the expected last lines are the ones used at level 2
    try:
        eb = json.load(open(p('EDITION_BINDINGS.json'), encoding='utf-8')); wrong_b = []
        for b in eb['bindings']:
            if truth.get(b['file']) != b['sha256'] or FIXED_SHA256.get(b['file']) != b['sha256']:
                wrong_b.append(b['file'])
        want_lines = {'comparison_records': EXPECTED_COMPARISON, 'independent_endpoint': INDEPENDENT_EXPECTED}
        if {b['id']: b['expected_last_line'] for b in eb['bindings']} != want_lines:
            wrong_b.append('expected last lines')
        for k, v in eb['roots'].items():
            if FIXED_SHA256.get(k) != v:
                wrong_b.append(k)
        for k, v in eb['seal'].items():
            if FIXED_SHA256.get(k) != v:
                wrong_b.append(k)
        if sorted(eb['roots']) != sorted(ROOT_FILES) or len(eb['seal']) != 3 or eb.get('files') != EXPECTED_FILES or eb.get('pins') != sum(v[0] for v in EXPECTED_PINS.values()):
            wrong_b.append('roots or counts')
        if wrong_b:
            say(1, 'bindings', 'FAIL', 'EDITION_BINDINGS.json disagrees with check.py or with the files: ' + ', '.join(wrong_b)); ok = False
        else:
            say(1, 'bindings', 'PASS', 'EDITION_BINDINGS.json agrees with check.py and with the files (%d bindings, %d root files, the file and pin counts)' % (len(eb['bindings']), len(eb['roots'])))
    except Exception as e:
        say(1, 'bindings', 'FAIL', 'EDITION_BINDINGS.json cannot be tested: %s: %s' % (type(e).__name__, e)); ok = False
    say(1, 'time', 'INFO', 'level 1 took %.0f s' % (time.time() - t0))
    return ok


# ----------------------------------------------------------------------------------------------- level 2
SHIM = r'''# Written by check.py.  Runs one script of the edition with two file-name mappings and no change to the script:
# (1) a path that begins with the old repository root of the build machine is read at the same place under the edition root;
# (2) a large file that is not at its mirror path is read from _large/ ;
import builtins, io, os, sys, runpy
OLD, ROOT = sys.argv[1], sys.argv[2]
script, rest = sys.argv[3], sys.argv[4:]
_stat, _lstat, _listdir, _scandir, _open, _ioopen = os.stat, os.lstat, os.listdir, os.scandir, builtins.open, io.open
def _exists(x):
    try: _stat(x); return True
    except OSError: return False
def mapped(path):
    if isinstance(path, int): return path
    try: s = os.fsdecode(path)
    except TypeError: return path
    if (s == OLD or s.startswith(OLD + '/')) and not (s == ROOT or s.startswith(ROOT + '/')):
        s = ROOT + s[len(OLD):]
    a = os.path.abspath(s)
    if a.startswith(ROOT + '/') and not a.startswith(ROOT + '/_large/') and not _exists(a):
        alt = ROOT + '/_large/' + a[len(ROOT) + 1:]
        if _exists(alt): return alt
    return s
class Wrap:            # an object, not a function: it must not turn into a bound method when a class stores it
    def __init__(self, fn, opener=False): self.fn, self.opener = fn, opener
    def __call__(self, *a, **kw):
        if self.opener and kw.get('opener') is not None: kw.pop('opener')
        if a: a = (mapped(a[0]),) + a[1:]
        elif 'path' in kw: kw['path'] = mapped(kw['path'])
        elif 'file' in kw: kw['file'] = mapped(kw['file'])
        return self.fn(*a, **kw)
os.stat, os.lstat, os.listdir, os.scandir = Wrap(_stat), Wrap(_lstat), Wrap(_listdir), Wrap(_scandir)
builtins.open, io.open = Wrap(_open, True), Wrap(_ioopen, True)
# (3) the same for the one pure path computation the scripts make on such a path: Path.relative_to(edition root).
import pathlib          # imported only now, after the mappings above are in place
_relative_to = pathlib.PurePath.relative_to
def relative_to(self, *other, **kw):
    try: return _relative_to(self, *other, **kw)
    except ValueError:
        s = str(self)
        if (s == OLD or s.startswith(OLD + '/')) and not (s == ROOT or s.startswith(ROOT + '/')):
            return _relative_to(type(self)(ROOT + s[len(OLD):]), *other, **kw)
        raise
pathlib.PurePath.relative_to = relative_to
sys.dont_write_bytecode = True
sys.argv = [script] + rest
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
runpy.run_path(script, run_name='__main__')
'''


LAST_CHILD_CPU = [None]      # CPU-seconds that the last child process used (None where the system does not say)


def child_cpu():
    try:
        import resource
        u = resource.getrusage(resource.RUSAGE_CHILDREN)
        return u.ru_utime + u.ru_stime
    except Exception:
        return None


def run(cmd, cwd, timeout, env_extra=None):
    env = dict(os.environ); env['PYTHONDONTWRITEBYTECODE'] = '1'
    env.pop('PYTHONOPTIMIZE', None)
    if env_extra:
        env.update(env_extra)
    t = time.time(); c0 = child_cpu()
    try:
        timeout = int(timeout * TIMEOUT_SCALE[0])
        r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=timeout, env=env)
        LAST_CHILD_CPU[0] = (child_cpu() - c0) if c0 is not None else None
        return r.returncode, r.stdout, r.stderr, time.time() - t
    except subprocess.TimeoutExpired as e:
        LAST_CHILD_CPU[0] = None        # the child was stopped by check.py; the system gives no figure for it here
        return -9, e.stdout or '', 'timeout after %d s' % timeout, time.time() - t


def sympy_python(args):
    """An interpreter (and PYTHONPATH) in which SymPy can be imported, or None."""
    tries = []
    extra = args.sympy_path
    py = args.sympy_python or sys.executable
    if extra:
        tries.append((py, {'PYTHONPATH': extra}))
    tries.append((py, None))
    for exe, env in tries:
        rc, out, err, _ = run([exe, '-c', 'import sympy; print(sympy.__version__)'], ROOT, 120, env)
        if rc == 0:
            return exe, env, out.strip()
    return None


def out_dir():
    stamp = time.strftime('%Y%m%dT%H%M%S') + '-%d' % os.getpid()
    d = os.path.join(ROOT, '_check_out', stamp)
    os.makedirs(d)
    return d


EXTRA = ['equivalence', 'comparison_records', 'independent_endpoint', 'trees_first_lines', 'trees_post_checks', 'trees_sha256_all', 'trees_certificates'] + (['neutral_first_lines', 'neutral_post_checks', 'neutral_equal'] if HAS_NEUTRAL else [])


def level2_names():
    return RUNBOOK_IDS + EXTRA


STATUS_WORD = re.compile(r'\b(?:PASS|ACCEPTED|FAIL|REJECTED|INCONCLUSIVE)(?:_[A-Za-z0-9]+)+')


def status_words(text):
    """The status words of an output: every word that begins PASS_, ACCEPTED_, FAIL_, REJECTED_ or INCONCLUSIVE_, each once, sorted."""
    return sorted(set(STATUS_WORD.findall(text)))


def last_error_line(err):
    """The last non-empty line of an error output (the line that names the error), without the lines above it."""
    lines = [l for l in err.strip().split('\n') if l.strip()]
    return lines[-1].strip()[:300] if lines else ''


PATH_PREFIX = re.compile(r'''/[^\s'"]*?/(?=(?:_large/)?(?:local-research/|research/|upper-packing-certificate\.json))''')


def norm_text(text):
    """A checker output without what differs between two executions of the same check: path prefixes, times, and
    the resource-usage lines that the time command appended to the outputs of the second execution."""
    out = []
    for line in text.split('\n'):
        if re.match(r'^\s*[0-9.]+ real\b', line) or re.match(r'^\s*(real|user|sys)\s', line):
            continue
        m = re.match(r'^\s*[0-9]+  ([a-z][a-z ]*)$', line)
        if m and m.group(1) in RESOURCE_LABELS:               # a resource-usage line of the time command: one of the listed labels, nothing else
            continue
        line = PATH_PREFIX.sub('', line).replace('_large/', '')
        line = re.sub(r'[0-9]+(\.[0-9]+)? s\b', 'T s', line)
        line = re.sub(r'\b(seconds|elapsed|time)[=: ]+[0-9.]+', r'\1 T', line)
        out.append(line.rstrip())
    while out and not out[-1]:
        out.pop()
    return out


def self_test():
    """The comparison of outputs must not drop a line that is not a listed resource line.  Returns the list of what is wrong."""
    bad = []
    if norm_text('PASS\n  123  unresolved constraints\n') == norm_text('PASS\n'):
        bad.append('a line "123  unresolved constraints" is dropped by the comparison of outputs')
    if norm_text('PASS\n  5  errors\n') == norm_text('PASS\n') or norm_text('PASS\nFAIL 3\n') == norm_text('PASS\n'):
        bad.append('a line that is no resource line is dropped by the comparison of outputs')
    for lab in RESOURCE_LABELS:
        if norm_text('PASS\n           453656576  %s\n' % lab) != norm_text('PASS\n'):
            bad.append('the resource line "%s" is not left out' % lab)
    if norm_text('PASS\n       28.99 real        28.59 user         0.15 sys\n') != norm_text('PASS\n'):
        bad.append('the line of the time command is not left out')
    return bad


def norm_json(x, key=None):
    if isinstance(x, dict):
        return {k: norm_json(v, k) for k, v in x.items() if k not in ('seconds', 'cpu_seconds', 'wall_seconds', 'elapsed')}
    if isinstance(x, list):
        return [norm_json(v) for v in x]
    if isinstance(x, str) and x.startswith('/'):
        return PATH_PREFIX.sub('', x).replace('_large/', '')
    return x


def level2(args):
    ok = True
    t0 = time.time()
    only = args.only
    if only and only not in level2_names():
        say(2, only, 'FAIL', 'no such check; see --list'); return False
    if root_name_twice():
        say(2, 'root-name', 'FAIL', ROOT_NAME_MESSAGE % root_name_twice()); return False
    OUT = out_dir()
    try:
        large = read_large(); manifest = read_manifest()
    except Exception as e:
        say(2, 'read-lists', 'FAIL', str(e)); return False
    shim = os.path.join(OUT, 'shim.py')
    with open(shim, 'w', encoding='utf-8') as f:
        f.write(SHIM)
    py = sys.executable
    absent_large = [x for x in sorted(large) if large_location(x) is None]

    def guarded(name, fn):
        try:
            fn()
        except Exception as e:
            record(name, False, 'could not be carried out: %s: %s' % (type(e).__name__, e))

    def record(name, good, text, secs=None):
        nonlocal ok
        counts['checks'] += 1
        say(2, name, 'PASS' if good else 'FAIL', text + ((' (%.1f s)' % secs) if secs is not None else ''))
        ok &= good

    def too_slow(name, text, secs):
        counts['checks'] += 1; tooslow.append(name)
        say(2, name, 'TOO-SLOW', text + ' (%.1f s)' % secs)

    def cpu_limit_of(script):
        # (the CPU limit in seconds that a script of the producers sets for itself, whether it also installs a handler for the signal SIGXCPU)
        try:
            src = open(p(script), encoding='utf-8', errors='replace').read()
        except OSError:
            return None, False
        m = re.search(r'RLIMIT_CPU\s*,\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', src)
        return (int(m.group(1)) if m else None), bool(re.search(r'signal\.signal\(\s*signal\.SIGXCPU', src))

    def handler_message_of(script):
        # the message of the TimeoutError that the script's handler for SIGXCPU raises, read from the script source (None if it has no such handler)
        try:
            src = open(p(script), encoding='utf-8', errors='replace').read()
        except OSError:
            return None
        h = re.search(r'signal\.signal\(\s*signal\.SIGXCPU\s*,\s*(\w+)\s*\)', src)
        d = re.search(r'def\s+%s\s*\([^)]*\)\s*:\s*raise\s+TimeoutError\(\s*([\'"])(.*?)\1\s*\)' % re.escape(h.group(1)), src) if h else None
        return d.group(2) if d else None

    def last_errors(text):
        # for each traceback of a stored output, in order: (its exception line, whether it is the runner's own traceback)
        out = []
        for b in re.split(r'(?m)^Traceback \(most recent call last\):\n', text)[1:]:
            out.append((next((l for l in b.split('\n') if l and not l.startswith(' ')), ''), 'runpy.run_path' in b))
        return out

    def stopped_by_limit(script, rc, receipt, runner_alarm, stored_output=''):
        """Why a public check did not finish, if a limit stopped it: a sentence, or None.  Decided by the cause alone:
        (1) the runner's receipt names its own TimeoutError of N seconds; (2) the script sets a CPU limit and installs a handler for
        SIGXCPU, and the receipt names the TimeoutError that this handler raises; (3) the script sets a CPU limit without a handler
        and the process was ended by the signal SIGXCPU before a receipt was written; (2b) the script catches the error of its own
        handler, prints it and ends with SystemExit(1): then the receipt says SystemExit(1), the last traceback of the stored output is
        the runner's ("SystemExit: 1"), the one before it (the last of the script itself) ends with the handler's own TimeoutError and
        its message, and the process used at least the limit of CPU seconds.  An amount of time alone decides nothing."""
        lim, handler = cpu_limit_of(script)
        err = (receipt or {}).get('error') or ''
        if receipt is not None and runner_alarm and err == "TimeoutError('%d-second wall limit')" % runner_alarm:
            return "stopped by the runner's own %d-second time limit (its receipt names that limit)" % runner_alarm
        if receipt is not None and lim and handler and err.startswith('TimeoutError(') and 'wall limit' not in err:
            cpu = receipt.get('cpu_seconds')
            return "stopped by the script's own %d-second CPU limit (its handler for SIGXCPU raised %s%s)" % (lim, err, (' after %.1f CPU-seconds' % cpu) if isinstance(cpu, (int, float)) else '')
        msg = handler_message_of(script) if (lim and handler) else None
        if receipt is not None and msg is not None and err == 'SystemExit(1)':
            le = last_errors(stored_output); cpu = LAST_CHILD_CPU[0]
            if len(le) >= 2 and le[-1] == ('SystemExit: 1', True) and le[-2] == ('TimeoutError: ' + msg, False) and isinstance(cpu, (int, float)) and cpu >= lim:
                return "stopped by the script's own %d-second CPU limit (its handler for SIGXCPU raised TimeoutError(%r), the last error of the script in its stored output; the process had used %.1f CPU-seconds)" % (lim, msg, cpu)
        if receipt is None and lim and rc == -int(getattr(signal, 'SIGXCPU', 24)):
            cpu = LAST_CHILD_CPU[0]
            return "stopped by the script's own %d-second CPU limit (the process was ended by the signal SIGXCPU%s)" % (lim, (' after %.1f CPU-seconds' % cpu) if isinstance(cpu, (int, float)) else '')
        return None

    def not_run(name, need):
        counts['checks'] += 1; notrun.append(name)
        say(2, name, 'NOT-RUN', 'needs %d large file(s) that are not present: %s' % (len(need), ', '.join(os.path.basename(x) for x in need[:4]) + (' ...' if len(need) > 4 else '')))

    # ---- (a) the producers' 31 public checks, through their runner replay_round2.py (bytes unchanged)
    def fixed(rel):
        return exact_exists(rel) and sha256_file(p(rel)) == FIXED_SHA256[rel]
    want_rb = (not only) or only in RUNBOOK_IDS
    if want_rb:
        if not fixed(BK + 'runbook_public.json') or not fixed(BK + RUNNER):
            say(2, 'runbook-definition', 'FAIL', 'runbook_public.json or the runner is missing or does not have the sha256 fixed in check.py'); return False
        rb = json.load(open(p(BK + 'runbook_public.json'), encoding='utf-8'))
        ids = [c.get('id') for c in rb.get('checks', [])]
        if ids != RUNBOOK_IDS:
            say(2, 'runbook-definition', 'FAIL', 'runbook_public.json does not define exactly the 31 checks, each once, that check.py expects (%d entries, %d distinct)' % (len(ids), len(set(ids)))); return False
        if not fixed(BK + 'PUBLIC_REPLAY_RESULTS.json'):
            say(2, 'runbook-definition', 'FAIL', 'PUBLIC_REPLAY_RESULTS.json is missing or does not have the sha256 fixed in check.py'); return False
        # the files each check read in the producers' own stored replay (their equivalence check binds these lists to their roster)
        reads = {c['id']: {x['file'] for x in c['inputs']} for c in json.load(open(p(BK + 'PUBLIC_REPLAY_RESULTS.json'), encoding='utf-8'))['checks']}
        alias = {a['logical_path']: a['actual_file'] for a in json.load(open(p(BK + 'PUBLIC_PATH_ALIASES.json'), encoding='utf-8'))['aliases']}
        reads = {k: {alias.get(x, x) for x in v} for k, v in reads.items()}
        declared = {}
        if STATUS_FILE:
            try:
                with open(p(STATUS_FILE), encoding='utf-8') as f:
                    declared = {k: [v['expected_status']] for k, v in json.load(f).items()}
            except Exception as e:
                say(2, 'runbook-definition', 'FAIL', '%s cannot be read: %s: %s' % (STATUS_FILE, type(e).__name__, e)); return False
            differ = sorted(k for k, v in declared.items() if EXPECTED_STATUS.get(k) != v)
            if differ:
                say(2, 'runbook-definition', 'FAIL', 'the expected status in %s differs from the one fixed in check.py for: %s' % (STATUS_FILE, ', '.join(differ))); return False
        runs = BK + 'public_runs/'
        ra = [int(x) for x in re.findall(r'signal\.alarm\((\d+)\)', open(p(BK + RUNNER), encoding='utf-8', errors='replace').read()) if int(x) > 0]
        runner_alarm = max(ra) if ra else None
        for c in rb['checks']:
            name = c['id']
            if only and only != name:
                continue
            if not exact_exists(c['script']) or sha256_file(p(c['script'])) != c['script_sha256']:
                record(name, False, 'the script %s is missing or has another sha256 than runbook_public.json names' % c['script']); continue
            need_large = sorted(x for x in reads.get(name, ()) if x in large)
            if any(x in absent_large for x in need_large):
                not_run(name, [x for x in need_large if x in absent_large]); continue
            cmd = [py, '-B', shim, OLD, ROOT, p(BK + RUNNER), name]; env = None; note = ''
            if name == 'endpoint_upper':
                found = sympy_python(args)
                if not found:
                    record(name, False, 'SymPy cannot be imported: install SymPy 1.14.0 for this Python, or pass --sympy-path DIR (see CHECK.md)'); continue
                cmd[0], env, note = found[0], found[1], ' [SymPy %s]' % found[2]
            # the runner writes into a new folder public_runs/<name> (or <name>-NN, the first free number)
            dest = runs + name; n = 1
            while os.path.lexists(p(dest)):
                n += 1; dest = runs + name + '-%02d' % n
            if any(m == dest or m.startswith(dest + '/') for m in manifest):
                record(name, False, 'the folder the runner would create, %s, is a listed path' % dest); continue
            rc, out, err, secs = run(cmd, ROOT, 600, env)
            receipt = None; moved = os.path.join(OUT, 'level2', 'public_runs', name)
            try:
                if os.path.isdir(p(dest)):
                    os.makedirs(os.path.dirname(moved), exist_ok=True)
                    shutil.move(p(dest), moved)
                    if os.path.exists(os.path.join(moved, 'receipt.json')):
                        receipt = json.load(open(os.path.join(moved, 'receipt.json'), encoding='utf-8'))
            except Exception as e:
                record(name, False, 'the output folder %s could not be moved to _check_out/ or read: %s' % (dest, e), secs); continue
            stdout_new = ''
            if os.path.exists(os.path.join(moved, 'stdout.txt')):
                with open(os.path.join(moved, 'stdout.txt'), encoding='utf-8', errors='replace') as f:
                    stdout_new = f.read()
            last = out.rstrip('\n').split('\n')[-1] if out.strip() else ''
            good = rc == 0 and last == 'PUBLIC CHECK %s: PASS' % name and receipt is not None and receipt.get('status') == 'PASS' and receipt.get('script_sha256') == c['script_sha256']
            if not good and (receipt is None or receipt.get('status') != 'PASS'):
                why = stopped_by_limit(c['script'], rc, receipt, runner_alarm, stdout_new)
                if why:
                    too_slow(name, why + '; the check was not carried out on this machine', secs); continue
            text = last if good else 'exit %d, last line %r, expected %r; %s' % (rc, last, 'PUBLIC CHECK %s: PASS' % name, last_error_line(err) or str((receipt or {}).get('error') or '')[-300:])
            if good:
                # the status words of the output are exactly the ones fixed in check.py (the words of the producers' stored output of this check)
                words = status_words(stdout_new)
                if words != EXPECTED_STATUS.get(name) or words != declared.get(name, words):
                    good = False
                    text = 'the status words of its output are %s; check.py fixes %s%s' % (words, EXPECTED_STATUS.get(name), ('; %s gives %s' % (STATUS_FILE, declared[name])) if name in declared else '')
                elif words:
                    note += ' [status %s%s]' % (', '.join(words), ', as the producers\' file of expected statuses gives it' if name in declared else '')
            if good:
                seen = set(x[len('_large/'):] if x.startswith('_large/') else x for x in receipt.get('inputs_read', []))
                if seen != reads.get(name):
                    good = False
                    text = 'the files it read are not exactly the files the producers\' stored replay of it read (PUBLIC_REPLAY_RESULTS.json): %d read, %d listed; first difference %s' % (
                        len(seen), len(reads.get(name, ())), sorted(seen ^ reads.get(name, set()))[:1])
                else:
                    note += ' [read exactly the %d files that the producers\' stored replay read%s]' % (len(seen), '; %d large from _large/' % len(need_large) if need_large else '')
            record(name, good, text + note, secs)

    # ---- (b) the producers' equivalence check, public mode (no argument)
    def equivalence():
        if not fixed(BK + 'check_equivalence.py'):
            record('equivalence', False, 'check_equivalence.py is missing or does not have the sha256 fixed in check.py'); return
        if absent_large:
            not_run('equivalence', absent_large); return
        rc, out, err, secs = run([py, '-B', shim, OLD, ROOT, p(BK + 'check_equivalence.py')], ROOT, 600)
        with open(os.path.join(OUT, 'equivalence.out'), 'w', encoding='utf-8') as f:
            f.write(out)
        try:
            d = json.loads(out); want = json.load(open(p(BK + 'AUTHOR_SEAL_CHECK.out'), encoding='utf-8'))
        except Exception:
            d = want = None
        good = rc == 0 and d is not None and d == want and str(d.get('status', '')).startswith('PASS')
        record('equivalence', good, ('status %s; output equal to the producers\' stored output AUTHOR_SEAL_CHECK.out: %s' % (d['status'], ', '.join('%s %s' % (k, v) for k, v in d.items() if isinstance(v, int))))
               if good else 'exit %d; output %r; %s' % (rc, out[-300:], last_error_line(err)), secs)

    # ---- (c) the records of the comparison with the earlier executions (which are not carried)
    def comparison_records():
        if not fixed('check_comparison_records.py'):
            record('comparison_records', False, 'check_comparison_records.py is missing or does not have the sha256 fixed in check.py'); return
        rc, out, err, secs = run([py, '-B', p('check_comparison_records.py')], ROOT, 1200)
        with open(os.path.join(OUT, 'comparison_records.out'), 'w', encoding='utf-8') as f:
            f.write(out)
        lines = out.rstrip('\n').split('\n') if out.strip() else ['']
        good = rc == 0 and lines[-1] == EXPECTED_COMPARISON and not any(l.startswith('BAD') for l in lines)
        record('comparison_records', good, ('%s; %s' % (lines[0], lines[-1])) if good else 'exit %d, last line %r, expected %r; %s' % (rc, lines[-1], EXPECTED_COMPARISON, err.strip()[-300:]), secs)

    # ---- (c3) the independent program for the tight enclosure of the endpoint root and of L, and its control
    def independent_endpoint():
        rel = 'independent/endpoint_enclosure/own_endpoint_enclosure.py'
        if not fixed(rel):
            record('independent_endpoint', False, rel + ' is missing or does not have the sha256 fixed in check.py'); return
        rc, out, err, secs = run([py, '-B', p(rel)], ROOT, 600)
        rc2, out2, err2, secs2 = run([py, '-B', p(rel), '--control'], ROOT, 600)
        for name, text in (('independent_endpoint.out', out), ('independent_endpoint_control.out', out2)):
            with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
                f.write(text)
        lines = [l for l in out.split('\n') if l.strip()]
        n_ok = sum(1 for l in lines if l.lstrip().startswith('[ok]'))
        proved = any(l == INDEPENDENT_EXPECTED for l in lines) and not any(l.startswith('RESULT: NOT PROVED') for l in lines)
        control_fails = rc2 != 0 and any(l.startswith('RESULT: NOT PROVED') for l in out2.split('\n')) and not any(l.startswith('RESULT: PROVED') for l in out2.split('\n'))
        good = rc == 0 and proved and n_ok == 39 and control_fails
        record('independent_endpoint', good, ('%s; 39 checks ok; its control (one coefficient of F changed by 1) ends NOT PROVED with exit %d' % (INDEPENDENT_EXPECTED.split('  ')[0], rc2)) if good
               else 'exit %d, %d checks ok (39 expected), proved line found: %s; control exit %d, control fails: %s; %s' % (rc, n_ok, proved, rc2, control_fails, err.strip()[-200:]), secs + secs2)

    # ---- (d) the stored outputs of the executions of the 13 tree certificates
    def first_lines(name, folder):
        bad = []
        for t in TREES:
            for c in ('C1', 'C2'):
                f = folder + '%s_%s.out' % (t, c)
                if not exact_exists(f) or open(p(f), encoding='utf-8', errors='replace').readline().rstrip('\n') != 'PASS':
                    bad.append(f)
        record(name, not bad, '26 stored checker outputs (13 trees, 2 checkers): first line PASS' if not bad else 'missing, or first line is not PASS: ' + ', '.join(bad))

    def post(name, folder):
        bad = []
        for t in TREES:
            f = folder + '%s_report.out' % t
            lines = [l for l in open(p(f), encoding='utf-8', errors='replace').read().split('\n') if l.strip()] if exact_exists(f) else []
            if not lines or lines[-1] != 'RESULT: ACCEPTED':
                bad.append(f)
        record(name, not bad, '13 stored post-check reports: last line RESULT: ACCEPTED' if not bad else 'missing, or last line is not RESULT: ACCEPTED: ' + ', '.join(bad))

    def trees_sha():
        bad = []; n = 0; names = []; by_table = 0; table = read_pn_table()
        expected = sorted(['%s_%s' % (t, x) for t in TREES for x in ('C1.json', 'C1.out', 'C2.json', 'C2.out', 'report.out')]
                          + ['results.tsv', 'reports.tsv', 'driver.py', 'driver2.py', 'driver.log', 'SHA256_G20S_HW.txt'])
        for line in open(p(RERUN + 'SHA256_ALL.txt'), encoding='utf-8'):
            if not line.strip():
                continue
            m = re.match(r'^([0-9a-f]{64})\s+\*?(.+)$', line.rstrip('\n'))
            if not m:
                bad.append('unreadable line %r' % line[:60]); continue
            n += 1; names.append(m.group(2))
            f = RERUN + m.group(2)
            have = sha256_file(p(f)) if exact_exists(f) else None
            if have is not None and have != m.group(1) and table.get(f) == (m.group(1), have):
                by_table += 1       # the list was written at execution time and names the file before the path-neutral substitution; the declared table gives both hashes
            elif have != m.group(1):
                bad.append(m.group(2))
        if sorted(names) != expected:
            bad.append('the list does not name exactly the 71 expected files, each once (%d lines, %d distinct names)' % (len(names), len(set(names))))
        if by_table != EXPECTED_BEFORE_IN_SHA256_ALL:
            bad.append('%d entries name the sha256 of a file before the substitution; check.py fixes %d' % (by_table, EXPECTED_BEFORE_IN_SHA256_ALL))
        record('trees_sha256_all', not bad and n == 71,
               ('SHA256_ALL.txt names the 71 expected files of the second execution, each once: %d have the listed sha256; %d are carried as substituted copies (the list names their sha256 before the substitution, %s gives both values)'
                % (n - by_table, by_table, PATH_NEUTRAL_TABLE)) if not bad else 'missing or different: ' + ', '.join(bad))

    def trees_certificates():
        bad = []; n = 0
        with open(p(BK + 'PUBLIC_INPUTS.tsv'), encoding='utf-8') as f:
            roster = {r['file']: r['sha256'] for r in csv.DictReader(f, delimiter='\t')}
        packing = roster.get('upper-packing-certificate.json'); spec = roster.get('research/window-extension-20261008/SPEC_v3.0.md')
        for folder in [RERUN] + ([NEUTRAL] if HAS_NEUTRAL else []):
            for t in TREES:
                try:
                    a = json.load(open(p(folder + t + '_C1.json'), encoding='utf-8')); b = json.load(open(p(folder + t + '_C2.json'), encoding='utf-8'))
                    m = re.search(r'(?:^|/)((?:local-research|research)/.+)$', a['certificate']); rel = m.group(1) if m else ''
                    good = (rel in roster and a['certificate_sha256'] == roster[rel] and a['packing_sha256'] == b['packing_sha256'] == packing and a['spec_sha256'] == b['spec_sha256'] == spec
                            and b['certificate_sha256'] == a['certificate_uncompressed_sha256'] and a['verdict'] == 'PASS' and b['result'] == 'PASS' and b['certificate'].endswith(rel))
                except Exception as e:
                    good = False
                n += 1
                if not good:
                    bad.append(folder.split('/')[-2] + '/' + t)
        record('trees_certificates', not bad, '%d pairs of machine reports name the certificate of this edition (the SHA-256 the producers\' roster gives; the second checker the SHA-256 of the uncompressed stream that the first reports), this packing file and this specification' % n
               if not bad else 'a stored machine report does not name the certificate, packing file or specification of this edition: ' + ', '.join(bad))

    def neutral_equal():
        bad = []; n = 0
        for t in TREES:
            for c in ('C1', 'C2'):
                a, b = RERUN + '%s_%s' % (t, c), NEUTRAL + '%s_%s' % (t, c)
                if norm_text(open(p(a + '.out'), encoding='utf-8', errors='replace').read()) != norm_text(open(p(b + '.out'), encoding='utf-8', errors='replace').read()):
                    bad.append('%s_%s.out' % (t, c))
                if norm_json(json.load(open(p(a + '.json'), encoding='utf-8'))) != norm_json(json.load(open(p(b + '.json'), encoding='utf-8'))):
                    bad.append('%s_%s.json' % (t, c))
                n += 2
            a, b = RERUN + '%s_report.out' % t, NEUTRAL + '%s_report.out' % t
            if norm_text(open(p(a), encoding='utf-8', errors='replace').read()) != norm_text(open(p(b), encoding='utf-8', errors='replace').read()):
                bad.append('%s_report.out' % t)
            n += 1
        record('neutral_equal', not bad, '%d files of the third execution (26 outputs, 26 machine reports with every node, 13 post-check reports) equal the files of the second execution, apart from path prefixes, times and resource-usage lines' % n
               if not bad else 'different from the second execution: ' + ', '.join(bad))

    table = [('equivalence', equivalence), ('comparison_records', comparison_records), ('independent_endpoint', independent_endpoint),
             ('trees_first_lines', lambda: first_lines('trees_first_lines', RERUN)), ('trees_post_checks', lambda: post('trees_post_checks', RERUN)), ('trees_sha256_all', trees_sha), ('trees_certificates', trees_certificates)]
    if HAS_NEUTRAL:
        table += [('neutral_first_lines', lambda: first_lines('neutral_first_lines', NEUTRAL)), ('neutral_post_checks', lambda: post('neutral_post_checks', NEUTRAL)), ('neutral_equal', neutral_equal)]
    for tname, tfn in table:
        if not only or only == tname:
            guarded(tname, tfn)
    say(2, 'time', 'INFO', 'level 2 took %.0f s; outputs under %s' % (time.time() - t0, os.path.relpath(OUT, ROOT)))
    return ok


def main():
    ap = argparse.ArgumentParser(description='Checks this edition. See CHECK.md.')
    ap.add_argument('--level', type=int, choices=[0, 1, 2], help='run one level only')
    ap.add_argument('--only', help='run one check of level 2 by name')
    ap.add_argument('--list', action='store_true', help='list the level-2 checks and stop')
    ap.add_argument('--sympy-path', help='a folder to put on PYTHONPATH for the one check that needs SymPy')
    ap.add_argument('--sympy-python', help='a Python interpreter that has SymPy, for that one check')
    ap.add_argument('--timeout-scale', type=float, default=1.0, help='multiply every time limit of level 2 by this number (for a slow machine)')
    args = ap.parse_args()
    TIMEOUT_SCALE[0] = max(1.0, args.timeout_scale)
    if args.list:
        print('\n'.join(level2_names())); return 0
    levels = [2] if args.only else ([args.level] if args.level is not None else [0, 1, 2])
    print('edition root: ' + ROOT)
    good = True
    for lv in levels:
        try:
            good &= {0: lambda: level0(args), 1: level1, 2: lambda: level2(args)}[lv]()
        except Exception as e:          # never end with a traceback and without a result line
            say(lv, 'internal', 'FAIL', 'level %d stopped: %s: %s' % (lv, type(e).__name__, e)); good = False
        if lv == 0 and not good:
            break
    full = levels == [0, 1, 2]
    which = 'levels 0-2' if full else 'level %d ONLY' % levels[0] + (', check ' + args.only + ' ONLY' if args.only else '')
    parts = []
    if 1 in levels: parts += ['%d files' % counts['files'], '%d pins' % counts['pins']]
    if 2 in levels: parts += ['%d checks' % counts['checks']]
    if notrun: parts += ['of which NOT RUN for absent large files: ' + ', '.join(notrun)]
    if tooslow: parts += ['of which TOO SLOW ON THIS MACHINE (stopped by the CPU limit of their own script or by the time limit of the runner): ' + ', '.join(tooslow)]
    try:
        mhash = sha256_file(p('MANIFEST.sha256'))
    except OSError:
        mhash = 'MANIFEST.sha256 cannot be read'
    tail = '; sha256 of MANIFEST.sha256: ' + mhash
    if full and counts['checks'] != EXPECTED_CHECKS:
        say(2, 'check-count', 'FAIL', '%d checks of level 2 were carried out; this edition has %d' % (counts['checks'], EXPECTED_CHECKS)); good = False
    fails = [r for r in results if r[2] == 'FAIL']
    if good and not fails:
        if full and not notrun and not tooslow:
            print('CHECK RESULT: PASS (%s%s)%s' % (which, ('; ' + ', '.join(parts)) if parts else '', tail))
            return 0
        why = ' and '.join(x for x in (('%d check(s) NOT RUN' % len(notrun)) if notrun else '', ('%d check(s) stopped by a CPU or time limit on this machine' % len(tooslow)) if tooslow else '', '' if full else 'not all levels and checks were run') if x)
        print('CHECK RESULT: PARTIAL (%s%s; nothing that was run failed, but %s: this is not a PASS of the edition)%s' % (which, ('; ' + ', '.join(parts)) if parts else '', why, tail))
        return 2
    for lv, name, status, text in fails[:50]:
        print('   FAILED L%d %s: %s' % (lv, name, text[:300]))
    causes = []
    for lv, name, status, text in fails:
        c = name + (' (SymPy not found)' if text.startswith('SymPy cannot be imported') else '')
        if c not in causes:
            causes.append(c)
    print('CHECK RESULT: FAIL (%s; %d failure line(s) in: %s%s)%s' % (which, len(fails), ', '.join(causes[:12]) or 'see above', ' ...' if len(causes) > 12 else '', tail))
    return 1


if __name__ == '__main__':
    sys.exit(main())
