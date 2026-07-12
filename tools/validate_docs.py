#!/usr/bin/env python3
import sys
from common_health import run
checks=['check_internal_links.py','check_math_rendering.py','check_release_consistency.py','check_markdown_hygiene.py','check_certification_compliance.py','check_orphaned_docs.py']
fail=[]; warn=[]
for tool in checks:
    required = tool != 'check_orphaned_docs.py'
    print(f'\n==> {tool}')
    cp=run([sys.executable, f'tools/{tool}'])
    if cp.stdout: print(cp.stdout.rstrip())
    if cp.returncode==0: print(f'PASS {tool}')
    elif required: print(f'FAIL {tool}'); fail.append(tool)
    else: print(f'WARN {tool}'); warn.append(tool)
print(f'\nDocs validation summary: warnings={len(warn)} failures={len(fail)}')
if fail: raise SystemExit(1)
