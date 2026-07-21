#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(ROOT))

from far_validation.certificate import write_certificate
from far_validation.trust import HMACTrust


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def successful(payload: dict[str, Any], evidence_id: str) -> bool:
    if evidence_id == 'formal-model':
        return int(payload.get('runs', 0)) > 0 and int(payload.get('attestation_mutations', 0)) >= 5
    return payload.get('successful') is True


def main() -> int:
    parser = argparse.ArgumentParser(description='Assemble a signed merge-authority validation certificate')
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--run', type=Path)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--evidence', action='append', default=[], metavar='ID=PATH')
    args = parser.parse_args()
    root = args.root.resolve()
    run_path = args.run or root / '.far' / 'runs' / 'latest.json'
    certificate_path = args.certificate or root / '.far' / 'artifacts' / 'validation' / 'certificate.json'
    run_payload = json.loads(run_path.read_text(encoding='utf-8'))
    evidence: dict[str, Any] = {}
    for spec in args.evidence:
        if '=' not in spec:
            raise SystemExit(f'invalid evidence spec: {spec}')
        evidence_id, raw_path = spec.split('=', 1)
        path = Path(raw_path)
        if not path.is_absolute():
            path = root / path
        payload = json.loads(path.read_text(encoding='utf-8'))
        ok = successful(payload, evidence_id)
        if not ok:
            raise SystemExit(f'assurance evidence failed: {evidence_id}')
        evidence[evidence_id] = {
            'path': path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path),
            'sha256': sha256(path),
            'successful': True,
        }
    assurance = dict(run_payload.get('assurance', {}))
    assurance['evidence'] = evidence
    assurance['complete'] = bool(evidence)
    run_payload['assurance'] = assurance
    trust = HMACTrust.from_environment(require_signature=True)
    write_certificate(certificate_path, run_payload, trust=trust)
    print(f'assembled signed validation certificate with {len(evidence)} evidence artifacts')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
