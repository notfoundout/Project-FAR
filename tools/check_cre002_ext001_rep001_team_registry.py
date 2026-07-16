#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001'
VOCABS = {'CRE-001-VOCAB-A-1.0','CRE-001-VOCAB-B-1.0','CRE-001-VOCAB-C-1.0'}


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    registry = json.loads((PKG / 'team-registry.json').read_text())
    schema = json.loads((PKG / 'team-registration-schema.json').read_text())
    if schema.get('$id') != 'CRE-002-EXT-001-REP-001-TEAM-REGISTRATION-1.0':
        fail('unexpected registration schema id')
    teams = registry.get('teams')
    if not isinstance(teams, list):
        fail('teams must be a list')
    team_ids: set[str] = set()
    personnel: set[str] = set()
    eligible_impl = []
    eligible_verifiers = []
    for team in teams:
        team_id = team.get('team_id')
        if not team_id or team_id in team_ids:
            fail('team ids must be unique and nonempty')
        team_ids.add(team_id)
        members = team.get('personnel', [])
        if not members or personnel.intersection(members):
            fail('teams must have nonempty disjoint personnel')
        personnel.update(members)
        if team.get('eligibility_status') == 'eligible':
            attest = team.get('attestations', {})
            required = ('no_shared_personnel','no_prohibited_exposure','no_cross_team_encoding_discussion','independent_repository','independent_credentials','truthful_and_complete')
            if any(attest.get(key) is not True for key in required):
                fail(f'eligible team lacks required attestation: {team_id}')
            if not team.get('review_record'):
                fail(f'eligible team lacks review record: {team_id}')
            if team.get('role') == 'implementation':
                if team.get('assigned_vocabulary') not in VOCABS:
                    fail(f'eligible implementation has invalid vocabulary: {team_id}')
                eligible_impl.append(team)
            elif team.get('role') == 'verifier':
                if team.get('assigned_vocabulary') != 'not-applicable':
                    fail(f'verifier must use not-applicable vocabulary: {team_id}')
                eligible_verifiers.append(team)
            else:
                fail(f'invalid team role: {team_id}')
    covered = {team['assigned_vocabulary'] for team in eligible_impl}
    requirements_met = len(eligible_impl) >= 2 and len(eligible_verifiers) >= 1 and covered == VOCABS
    summary = registry.get('eligibility_summary', {})
    if summary.get('eligible_implementation_teams') != len(eligible_impl):
        fail('implementation-team summary mismatch')
    if summary.get('eligible_verifier_teams') != len(eligible_verifiers):
        fail('verifier-team summary mismatch')
    if set(summary.get('covered_vocabularies', [])) != covered:
        fail('vocabulary-coverage summary mismatch')
    if registry.get('minimum_requirements_met') is not requirements_met:
        fail('minimum-requirements flag mismatch')
    if registry.get('execution_unlock_eligible') is not requirements_met:
        fail('execution-unlock flag mismatch')
    if not requirements_met and not registry.get('blocking_reasons'):
        fail('unmet requirements require blocking reasons')
    print('CRE-002-EXT-001-REP-001 TEAM REGISTRY CHECK PASSED')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
