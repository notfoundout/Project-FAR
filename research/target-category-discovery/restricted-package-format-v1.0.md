# Restricted Package Format v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`

## 1. Canonical file rules

- regular files only; symlinks, devices, sockets, and hard-link aliases are rejected;
- paths are relative POSIX paths, Unicode NFC, no empty component, `.`, `..`, leading slash, or backslash;
- entries are sorted by UTF-8 path bytes;
- file bytes are hashed exactly as stored with SHA-256;
- timestamps, owners, permissions, compression metadata, and filesystem order are not part of the commitment.

## 2. Canonical manifest

The commitment manifest is canonical JSON:

- UTF-8;
- Unicode NFC strings;
- sorted keys;
- separators `(',', ':')`;
- no insignificant whitespace;
- one terminal LF.

Each entry contains `path`, `size`, and `sha256`.

## 3. Merkle root

For each sorted entry:

`leaf = SHA256(b"leaf\0" + path_utf8 + b"\0" + decimal_size + b"\0" + sha256_hex)`

Build the tree by hashing:

`node = SHA256(b"node\0" + left_digest + right_digest)`

When a level has an odd count, duplicate the last digest. The empty package root is `SHA256(b"empty\0")`.

The public commitment contains package version, file count, canonical-manifest SHA-256, Merkle root, custodian declaration ID, and reveal condition. Per-file metadata remains restricted.

## 4. Reproduction

A second environment must reproduce the same canonical manifest digest and Merkle root from restored bytes. Failure blocks execution. ZIP files may be used for transport only; their archive digest is supplementary and never the package identity.

## 5. Access log

Every creation, copy, restore, reveal, revocation, or destruction event records actor, role, timestamp, action, package root, destination class, authorization, and result. Logs are append-only and separately committed.
