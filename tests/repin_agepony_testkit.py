"""Test-only emulation of AgePony's Secure Enclave signing path, in software.

AgePony (norsehorse-dev/AgePonyiOS 3.1.0, ``AgePony/Services/SecureEnclaveSigner.swift`` and
``Sources/AgePonyCore/Signing/SSHSigner.swift``) signs a file as follows: SHA-512 of the file bytes
goes into the SSHSIG signed-data blob for namespace ``agepony``; the Secure Enclave key signs that
blob with ECDSA P-256 over SHA-256 (CryptoKit ``signature(for:)``); ``assembleECDSAP256`` wraps the
raw ``r || s`` as ``string("ecdsa-sha2-nistp256") || string(mpint r || mpint s)`` with minimal
mpints, and the blob is armored at 70 columns with LF line ends and a final LF.

Here ``openssl`` plays the Enclave (a software key, which is exactly what FAR cannot tell apart
from an Enclave key) and the assembly is ported line for line, so every structural variant an
attacker could submit can be built from a genuine signature. ``ssh-keygen`` is never used to sign
here, so its output format is not assumed to be AgePony's.
"""
from __future__ import annotations

import base64
import hashlib
import struct
import subprocess
from pathlib import Path

from far_validation import repin_signature as sig

KEY_TYPE = b"ecdsa-sha2-nistp256"

# AgePony's own interoperability vector (Tests/AgePonyCoreTests/SSHSigECDSATests.swift, Apache-2.0):
# produced by `ssh-keygen -Y sign -f id_ecdsa -n agepony msg.txt` and verified by AgePonyCore.
AGEPONY_GOLDEN_MESSAGE = b"sign me with ecdsa for agepony"
AGEPONY_GOLDEN_KEY = ("AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMCSXvifSs8+c1itwJlTtXPGUsAslwZ+AOL26ASFmHqMp8JpEL0IdNY5Jc+34InF141oFATvy+2zfEtCOd0wQOQ=")
AGEPONY_GOLDEN_SIGNATURE = """-----BEGIN SSH SIGNATURE-----
U1NIU0lHAAAAAQAAAGgAAAATZWNkc2Etc2hhMi1uaXN0cDI1NgAAAAhuaXN0cDI1NgAAAE
EEwJJe+J9Kzz5zWK3AmVO1c8ZSwCyXBn4A4vboBIWYeoynwmkQvQh01jklz7fgicXXjWgU
BO/L7bN8S0I53TBA5AAAAAdhZ2Vwb255AAAAAAAAAAZzaGE1MTIAAABkAAAAE2VjZHNhLX
NoYTItbmlzdHAyNTYAAABJAAAAIHCzjn46/mSGQ15v8otFusU9bv25YnQGxkqwZcZWoJ8i
AAAAIQDFPSGnT0htw6VlRqJe/H6IE0bJdszLsWjdKBFc0hPJng==
-----END SSH SIGNATURE-----
"""


def ssh_string(data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + data


def write_mpint(value: bytes) -> bytes:
    """``SSHWireWriter.writeMPInt``: strip leading zeros, prefix 0x00 when the high bit is set."""
    while len(value) > 1 and value[0] == 0:
        value = value[1:]
    if not value:
        return struct.pack(">I", 0)
    return ssh_string(b"\0" + value if value[0] & 0x80 else value)


def signers_line(key_b64: str, namespace: str = sig.NAMESPACE, kind: str = sig.KEY_TYPE) -> bytes:
    return f'{sig.PRINCIPAL} namespaces="{namespace}" {kind} {key_b64}\n'.encode()


def _der_rs(der: bytes) -> tuple[int, int]:
    assert der[0] == 0x30
    offset = 2 if der[1] < 0x80 else 3
    values = []
    for _ in range(2):
        assert der[offset] == 0x02
        length = der[offset + 1]
        values.append(int.from_bytes(der[offset + 2:offset + 2 + length], "big"))
        offset += 2 + length
    return values[0], values[1]


def signed_data(message: bytes, namespace: str = sig.NAMESPACE, hash_algorithm: str = "sha512") -> bytes:
    digest = hashlib.new(hash_algorithm, message).digest()
    return (b"SSHSIG" + ssh_string(namespace.encode()) + ssh_string(b"") + ssh_string(hash_algorithm.encode())
            + ssh_string(digest))


def blob(public_wire: bytes, inner: bytes, namespace: str = sig.NAMESPACE, hash_algorithm: str = "sha512",
         reserved: bytes = b"", version: int = 1, trailing: bytes = b"") -> bytes:
    return (b"SSHSIG" + struct.pack(">I", version) + ssh_string(public_wire) + ssh_string(namespace.encode())
            + ssh_string(reserved) + ssh_string(hash_algorithm.encode()) + ssh_string(inner) + trailing)


def inner(r: int, s: int, kind: bytes = KEY_TYPE) -> bytes:
    return ssh_string(kind) + ssh_string(write_mpint(r.to_bytes(32, "big")) + write_mpint(s.to_bytes(32, "big")))


class AgePonyKey:
    """A P-256 key used the way AgePony uses its Secure Enclave identity."""

    def __init__(self, directory: Path, name: str = "agepony-far") -> None:
        self.pem = directory / f"{name}.pem"
        subprocess.run(["openssl", "ecparam", "-name", "prime256v1", "-genkey", "-noout", "-out", str(self.pem)],
                       check=True, capture_output=True)
        der = subprocess.run(["openssl", "ec", "-in", str(self.pem), "-pubout", "-outform", "DER"],
                             check=True, capture_output=True).stdout
        self.point = der[-65:]
        assert self.point[0] == 0x04
        self.wire = ssh_string(KEY_TYPE) + ssh_string(b"nistp256") + ssh_string(self.point)
        self.key_b64 = base64.b64encode(self.wire).decode()

    def display_line(self) -> str:
        """``StoredIdentity.publicDisplayString()`` for a Secure Enclave identity (no comment set)."""
        return f"ecdsa-sha2-nistp256 {self.key_b64}"

    def signers(self) -> bytes:
        return signers_line(self.key_b64)

    def raw_rs(self, data: bytes) -> tuple[int, int]:
        """ECDSA-SHA256 over ``data``: what ``SecureEnclave.P256.Signing.PrivateKey.signature(for:)`` computes."""
        der = subprocess.run(["openssl", "dgst", "-sha256", "-sign", str(self.pem)], input=data,
                             check=True, capture_output=True).stdout
        return _der_rs(der)

    def sign(self, message: bytes, namespace: str = sig.NAMESPACE, hash_algorithm: str = "sha512") -> str:
        """The ``.sig`` file AgePony writes for ``message``."""
        r, s = self.raw_rs(signed_data(message, namespace, hash_algorithm))
        return sig.armor(blob(self.wire, inner(r, s), namespace, hash_algorithm))

    def sign_parts(self, message: bytes) -> tuple[int, int]:
        return self.raw_rs(signed_data(message))
