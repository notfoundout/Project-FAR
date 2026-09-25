#!/usr/bin/env python3
"""Black-box acceptance checker for the installed AgePony signer.

This is an enrollment/compatibility tool, not the live protected-repin gate. It checks the frozen
acceptance corpus and detached signatures produced by the actual iPhone build before a permanent
FAR key is trusted. It intentionally verifies exact bytes and the strict SSHSIG envelope used by
``repin_signature``. Hardware origin and per-use presence are ceremony observations and cannot be
proved from a plain ECDSA SSHSIG.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import struct
import tempfile
from pathlib import Path
from typing import Callable

from . import repin_signature as sig

MANIFEST = "far-accept-manifest.json"
FILES = (
    "far-accept-1-basic.json",
    "far-accept-2-same-bytes.json",
    "far-accept-3-escapes.json",
    "far-accept-4-prompts-off.json",
    "far-accept-5-trailing-newline.json",
    "far-enrollment-proof.txt",
)
EXPECTED_PROMPTS = {
    "far-accept-1-basic.json": "prompts ON",
    "far-accept-2-same-bytes.json": "prompts ON",
    "far-accept-3-escapes.json": "prompts ON",
    "far-accept-4-prompts-off.json": "prompts OFF",
    "far-accept-5-trailing-newline.json": "prompts ON",
    "far-enrollment-proof.txt": "prompts ON",
}
EXPECTED_KINDS = {
    "far-accept-1-basic.json": "far",
    "far-accept-2-same-bytes.json": "far-duplicate-of-1",
    "far-accept-3-escapes.json": "far",
    "far-accept-4-prompts-off.json": "far",
    "far-accept-5-trailing-newline.json": "non-canonical",
    "far-enrollment-proof.txt": "non-far",
}

# SEC 2 / NIST P-256 base point. The acceptance checker implements ECDSA verification
# independently so it does not depend on OpenSSH being installed in the audit environment.
P256_GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
P256_GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5


def _point_add(p: tuple[int, int] | None, q: tuple[int, int] | None) -> tuple[int, int] | None:
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p; x2, y2 = q
    mod = sig.P256_P
    if x1 == x2 and (y1 + y2) % mod == 0:
        return None
    if p == q:
        if y1 == 0:
            return None
        lam = ((3 * x1 * x1 - 3) * pow(2 * y1, -1, mod)) % mod
    else:
        lam = ((y2 - y1) * pow((x2 - x1) % mod, -1, mod)) % mod
    x3 = (lam * lam - x1 - x2) % mod
    y3 = (lam * (x1 - x3) - y1) % mod
    return x3, y3


def _scalar(k: int, p: tuple[int, int]) -> tuple[int, int] | None:
    out = None
    add = p
    while k:
        if k & 1:
            out = _point_add(out, add)
        add = _point_add(add, add)
        k >>= 1
    return out


def _verify_independent(message: bytes, armored: str, allowed_signers: bytes) -> None:
    _kind, key = sig.validate_allowed_signers(allowed_signers)
    sig._check_sshsig(armored, key)
    parts = _parts(armored)
    r, s = _int(parts["r"]), _int(parts["s"])
    public = base64.b64decode(key)
    point = sig.parse_public_key(public)
    q = (int.from_bytes(point[1:33], "big"), int.from_bytes(point[33:], "big"))
    digest = hashlib.sha512(message).digest()
    signed = (b"SSHSIG" + _string(sig.NAMESPACE.encode()) + _string(b"")
              + _string(sig.HASH_ALGORITHM.encode()) + _string(digest))
    z = int.from_bytes(hashlib.sha256(signed).digest(), "big")
    w = pow(s, -1, sig.P256_N)
    u1, u2 = (z * w) % sig.P256_N, (r * w) % sig.P256_N
    point_r = _point_add(_scalar(u1, (P256_GX, P256_GY)), _scalar(u2, q))
    if point_r is None or point_r[0] % sig.P256_N != r:
        raise sig.SignatureError("signature does not verify under the pinned key")


def _u32(n: int) -> bytes:
    return struct.pack(">I", n)


def _string(data: bytes) -> bytes:
    return _u32(len(data)) + data


def _read(data: bytes, offset: int) -> tuple[bytes, int]:
    return sig._read_string(data, offset)


def _parts(armored: str) -> dict[str, object]:
    blob = sig.dearmor(armored)
    if blob[:6] != b"SSHSIG" or len(blob) < 10:
        raise sig.SignatureError("not SSHSIG")
    version = int.from_bytes(blob[6:10], "big")
    public, off = _read(blob, 10)
    namespace, off = _read(blob, off)
    reserved, off = _read(blob, off)
    hash_algorithm, off = _read(blob, off)
    inner, off = _read(blob, off)
    trailing = blob[off:]
    kind, ioff = _read(inner, 0)
    components, ioff = _read(inner, ioff)
    inner_trailing = inner[ioff:]
    raw_r, coff = _read(components, 0)
    raw_s, coff = _read(components, coff)
    comp_trailing = components[coff:]
    return {
        "version": version, "public": public, "namespace": namespace, "reserved": reserved,
        "hash": hash_algorithm, "kind": kind, "r": raw_r, "s": raw_s,
        "trailing": trailing, "inner_trailing": inner_trailing, "comp_trailing": comp_trailing,
    }


def _blob(parts: dict[str, object]) -> bytes:
    components = _string(parts["r"]) + _string(parts["s"]) + parts.get("comp_trailing", b"")
    inner = _string(parts["kind"]) + _string(components) + parts.get("inner_trailing", b"")
    return (
        b"SSHSIG" + _u32(int(parts["version"])) + _string(parts["public"]) + _string(parts["namespace"])
        + _string(parts["reserved"]) + _string(parts["hash"]) + _string(inner) + parts.get("trailing", b"")
    )


def _mpint(value: int) -> bytes:
    raw = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
    raw = raw.lstrip(b"\0") or b"\0"
    if raw[0] & 0x80:
        raw = b"\0" + raw
    return raw


def _int(raw: bytes) -> int:
    return int.from_bytes(raw, "big")


def twin_signature(armored: str) -> str:
    parts = _parts(armored)
    parts["s"] = _mpint(sig.P256_N - _int(parts["s"]))
    return sig.armor(_blob(parts))


def malformed_variants(armored: str) -> dict[str, str]:
    """Structural variants that the strict FAR profile must refuse."""
    base = _parts(armored)
    out: dict[str, str] = {}
    def add(name: str, change: Callable[[dict[str, object]], None]) -> None:
        p = dict(base); change(p); out[name] = sig.armor(_blob(p))
    add("version", lambda p: p.__setitem__("version", 2))
    add("namespace", lambda p: p.__setitem__("namespace", b"other"))
    add("reserved", lambda p: p.__setitem__("reserved", b"x"))
    add("hash", lambda p: p.__setitem__("hash", b"sha256"))
    add("sig-alg", lambda p: p.__setitem__("kind", b"ssh-ed25519"))
    add("r-zero", lambda p: p.__setitem__("r", b"\0"))
    add("s-zero", lambda p: p.__setitem__("s", b"\0"))
    add("r-n", lambda p: p.__setitem__("r", _mpint(sig.P256_N)))
    add("s-n", lambda p: p.__setitem__("s", _mpint(sig.P256_N)))
    add("r-nonminimal", lambda p: p.__setitem__("r", b"\0" + p["r"]))
    add("s-nonminimal", lambda p: p.__setitem__("s", b"\0" + p["s"]))
    add("raw-trailing", lambda p: p.__setitem__("trailing", b"x"))
    add("inner-trailing", lambda p: p.__setitem__("inner_trailing", b"x"))
    add("components-trailing", lambda p: p.__setitem__("comp_trailing", b"x"))
    # Canonical armor rules are separate from the binary structure.
    out["crlf-armor"] = armored.replace("\n", "\r\n")
    out["missing-final-lf"] = armored.rstrip("\n")
    out["prefix-text"] = "x\n" + armored
    out["suffix-text"] = armored + "x\n"
    return out


def _allowed_from_public_line(public_line: str) -> tuple[bytes, str]:
    match = sig.PUBLIC_KEY_LINE.fullmatch(public_line.strip())
    if match is None or match.group(1) != sig.KEY_TYPE:
        raise sig.SignatureError(f"public key must be one {sig.KEY_TYPE} line")
    _kind, key = match.groups()
    line = f'{sig.PRINCIPAL} namespaces="{sig.NAMESPACE}" {sig.KEY_TYPE} {key}\n'.encode("ascii")
    sig.validate_allowed_signers(line)
    return line, sig.fingerprint(key)


def _canonical_status(name: str, data: bytes) -> bool:
    try:
        sig.parse_payload(data.decode("ascii"))
        valid = True
    except (UnicodeDecodeError, sig.SignatureError):
        valid = False
    return valid


def check(directory: Path, public_line: str) -> dict[str, object]:
    allowed, fingerprint = _allowed_from_public_line(public_line)
    manifest_path = directory / MANIFEST
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    entries = manifest.get("files")
    if not isinstance(entries, dict) or set(entries) != set(FILES):
        raise ValueError("acceptance manifest file set is not frozen")
    if manifest.get("repository") != "far-acceptance/disposable-key":
        raise ValueError("acceptance manifest repository changed")

    messages: dict[str, bytes] = {}
    signatures: dict[str, str] = {}
    results: dict[str, object] = {}
    for name in FILES:
        item = entries[name]
        if item.get("kind") != EXPECTED_KINDS[name] or item.get("sign_with") != EXPECTED_PROMPTS[name]:
            raise ValueError(f"manifest metadata changed for {name}")
        data = (directory / name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != item.get("sha256"):
            raise ValueError(f"SHA-256 mismatch for {name}")
        armored = (directory / f"{name}.sig").read_text(encoding="ascii")
        _verify_independent(data, armored, allowed)
        messages[name], signatures[name] = data, armored
        results[name] = {"sha256": digest, "signature_valid": True, "canonical_far": _canonical_status(name, data)}

    if messages[FILES[0]] != messages[FILES[1]]:
        raise ValueError("files 1 and 2 must be byte-identical")
    if signatures[FILES[0]] == signatures[FILES[1]]:
        raise ValueError("files 1 and 2 must have separately produced signatures")
    for name in FILES[:4]:
        if not results[name]["canonical_far"]:
            raise ValueError(f"{name} must be a canonical FAR-shaped payload")
    if results[FILES[4]]["canonical_far"] or results[FILES[5]]["canonical_far"]:
        raise ValueError("file 5 and enrollment proof must authorize nothing")

    # Exact-message binding: each signature may verify only its own message, except signatures 1/2
    # intentionally verify both because those messages are identical.
    for sname, armored in signatures.items():
        for mname, message in messages.items():
            should = messages[sname] == message
            try:
                _verify_independent(message, armored, allowed)
                actual = True
            except sig.SignatureError:
                actual = False
            if actual != should:
                raise ValueError(f"cross-message result mismatch: {sname} -> {mname}")

    # One changed byte must invalidate each signature.
    for name in FILES:
        changed = bytearray(messages[name]); changed[0] ^= 1
        try:
            _verify_independent(bytes(changed), signatures[name], allowed)
        except sig.SignatureError:
            pass
        else:
            raise ValueError(f"modified message accepted for {name}")

    # ECDSA's (r, n-s) twin is valid; FAR replay protection therefore keys on payload id/nonce,
    # never signature bytes.
    twin = twin_signature(signatures[FILES[0]])
    _verify_independent(messages[FILES[0]], twin, allowed)

    mutants = malformed_variants(signatures[FILES[0]])
    survivors: list[str] = []
    for label, mutant in mutants.items():
        try:
            sig.verify_signature(messages[FILES[0]], mutant, allowed)
        except sig.SignatureError:
            continue
        survivors.append(label)
    if survivors:
        raise ValueError(f"malformed signature variants survived: {survivors}")

    return {
        "result": "PASS", "fingerprint": fingerprint, "files_checked": len(FILES),
        "mutations_rejected": len(mutants), "twin_verifies": True, "files": results,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("directory", type=Path, help="folder containing the six originals and six detached .sig files")
    parser.add_argument("--public-key", type=Path, required=True, help="text file containing the copied AgePony public key line")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = check(args.directory, args.public_key.read_text(encoding="ascii"))
    except (OSError, ValueError, json.JSONDecodeError, sig.SignatureError) as exc:
        print(f"[FAIL] {exc}")
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Result: {report['result']}")
        print(f"Fingerprint: {report['fingerprint']}")
        print(f"Files checked: {report['files_checked']}")
        print(f"Malformed variants rejected: {report['mutations_rejected']}")
        print("ECDSA twin verifies: yes (replay protection is payload-id based)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
