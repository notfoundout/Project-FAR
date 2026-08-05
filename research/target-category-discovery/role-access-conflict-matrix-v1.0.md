# Role, Access, and Conflict Matrix v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Operational state: **unassigned — execution blocked**

## 1. Required role records

Each role record must contain a named human or controlled service identity, organization, credential boundary, conflict declaration, permitted stores, prohibited stores, reveal authority, start/end date, and substitute.

Required roles:

- governance custodian;
- source selector;
- independent dimension coder;
- source matcher;
- packet sanitizer;
- leakage reviewer;
- Stage A derivator operator;
- Stage A adjudicator 1;
- Stage A adjudicator 2;
- Stage B analyst;
- validation custodian;
- red-team reviewer;
- access-log auditor.

## 2. Prohibited combinations

For the confirmatory program:

- theory author cannot be source selector, dimension coder, leakage reviewer, either final adjudicator, or validation custodian;
- source selector cannot be dimension coder or source matcher;
- packet sanitizer cannot be the sole leakage reviewer;
- Stage A derivator cannot access source registry, curator ledger before A2, other outputs, Stage B materials, or validation identities;
- Stage B analyst cannot alter Stage A records;
- validation custodian cannot perform development synthesis;
- access-log auditor cannot administer the restricted store.

A sacrificial pilot may combine roles only when labeled internal and permanently excluded from evidence.

## 3. Access classes

- `PUBLIC_CONTROL`: public protocol, design, manifest commitments.
- `RESTRICTED_SOURCE`: identities, captured bytes, candidate logs.
- `RESTRICTED_PACKET`: packet drafts, edit logs, curator failure ledger.
- `DERIVATION_A1`: accepted blind A1 packet and fixed prompt only.
- `DERIVATION_A2`: A1 freeze plus curator ledger.
- `STAGE_B`: frozen Stage A ledger and disclosed case facts.
- `VALIDATION_SEALED`: validation identities and packets.
- `AUDIT_LOG`: append-only access and reveal records.

Every role has an explicit allowlist; absence means deny.

## 4. Assignment gate

The public role-assignment commitment must report only role IDs, distinctness assertions, signed-declaration hashes, access-policy hash, and aggregate assignment status. Names and credentials remain restricted.

Execution authorization requires:

- every role assigned;
- every declaration signed and hashed;
- all prohibited combinations absent;
- credentials tested;
- reveal permissions tested;
- substitute rules tested;
- access logging verified;
- independent auditor sign-off.

Current status is `blocked` because no such operational assignment package exists.

## 5. Substitution

A substitute must satisfy the same conflict and access rules. Substitution is recorded before access. Emergency substitution without prior approval terminates the run and requires a new version.

## 6. Revocation

Role completion, withdrawal, incident, or substitution triggers credential revocation and an access-log event. Revocation must be tested during the sacrificial pilot.
