# Restricted Artifacts Policy

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`

## 1. Purpose

The clean-room design requires information barriers that ordinary repository paths cannot enforce for derivators who may have repository access. Restricted content is therefore intentionally omitted from Git.

## 2. Artifacts excluded from the repository

The following generated artifacts are not committed:

- exact public/operational source registry;
- sealed validation identities;
- source titles, organizations, and URLs linked to blind rows;
- captured source bytes and archives;
- packet source-to-edit logs containing identities;
- packet preparation workbook;
- validation packet contents and hashes before reveal;
- challenge packet contents before their reveal gate;
- ZIP bundles or preview images containing restricted metadata;
- the generated v1.0 sealed registry and workbook.

## 3. Reason for exclusion

Committing these files would permit a derivator with repository access to:

- identify validation cases before the freeze;
- infer source domains or likely answers;
- connect blind packets to public source material;
- inspect target-bearing internal IDs;
- recover packet structure and curation choices;
- invalidate the claimed information barrier.

A private repository is not a clean-room boundary when the same account or agent can read it.

## 4. Required custodian store

Restricted artifacts must be held in a separately access-controlled location with:

- custodian identity;
- version;
- timestamp;
- SHA-256 digest;
- access log;
- reveal authorization;
- immutable replacement history;
- backup and recovery procedure.

The location may be encrypted local storage, a restricted vault, or another system whose permissions exclude derivators.

## 5. Public commitment records

Before execution, the repository may contain a commitment record that proves a restricted package existed without exposing its contents. The record may include:

- package version;
- creation time;
- one aggregate cryptographic digest;
- custodian declaration;
- reveal conditions.

It must not include filenames, per-case hashes, or metadata that permits identity matching when those values would weaken blinding.

## 6. Reveal rules

- Development packet: reveal only to its isolated Stage A workspace after packet acceptance.
- Validation packet: reveal only after Stage A and Stage B development outputs, scoring rules, and costs are frozen.
- Challenge packet: reveal only after development synthesis and scoring rules are frozen.
- Source registry: reveal to adjudicators only when source verification requires it and the role is authorized.

Every reveal is logged.

## 7. Independence boundary

External storage does not create investigator independence by itself. If the same person controls curation, sanitation, execution, and adjudication, the evidence remains internal even when workspaces are isolated.

## 8. Workbook disposition

The generated workbook v1.0 is rejected as an execution artifact because of formula-reference, count, lexical-control, and information-barrier defects documented in the chat audit. A corrected workbook must receive a new version and independent audit before use.
