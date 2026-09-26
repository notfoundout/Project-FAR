"""Owner-signed repin authorizations, AgePony Secure Enclave P-256 profile.

Signatures come from ``repin_agepony_testkit``, a software emulation of AgePony's signing path
(its Secure Enclave key replaced by an ``openssl`` P-256 key, which is exactly what FAR cannot tell
apart). Every rejection test starts from a genuinely signed payload and changes one thing an
attacker controls. Checks that OpenSSH also enforces are tested directly against the structural
parser as well, so each local check is shown to matter on its own.
"""
from __future__ import annotations

import base64
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import repin_signature as sig

try:
    from tests import repin_agepony_testkit as kit
except ImportError:  # discovered with tests/ as the top-level directory
    import repin_agepony_testkit as kit

PAYLOAD = {
    "schema": sig.SCHEMA, "domain": sig.DOMAIN, "id": "0123456789abcdef0123456789abcdef",
    "repository": "notfoundout/Project-FAR", "repository_id": 1283452680, "path": "validation/runtime-policy.json",
    "old_sha256": "a" * 64, "new_sha256": "b" * 64, "target_pr": 538,
    "base_sha": "7fb4816e4aa53aed749b7008b46ba9393d3d29b2",
    "reason": "owner-reviewed replacement of this exact protected artifact",
    "issued_at": "2026-09-24T00:00:00Z", "expires_at": "2026-10-08T00:00:00Z",
}


def text(payload: dict) -> str:
    return sig.canonical_bytes(payload).decode()


def openssh_accepts(message: bytes, armored: str, signers: bytes) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "signers").write_bytes(signers)
        (Path(tmp) / "sig").write_text(armored)
        completed = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", f"{tmp}/signers", "-I", sig.PRINCIPAL,
                                    "-n", sig.NAMESPACE, "-s", f"{tmp}/sig"], input=message, capture_output=True)
    return completed.returncode == 0


class PayloadTests(unittest.TestCase):
    def test_canonical_payload_parses(self) -> None:
        self.assertEqual(sig.parse_payload(text(PAYLOAD)), PAYLOAD)

    def test_malformed_payloads_are_rejected(self) -> None:
        cases = {
            "pretty-printed (non-canonical)": json.dumps(PAYLOAD, indent=1, sort_keys=True),
            "unsorted keys": json.dumps(PAYLOAD, separators=(",", ":")),
            "duplicate key": text(PAYLOAD)[:-1] + ',"target_pr":1}',
            "extra field": text({**PAYLOAD, "approved_by": "notfoundout"}),
            "missing field": text({k: v for k, v in PAYLOAD.items() if k != "expires_at"}),
            "boolean pr": text({**PAYLOAD, "target_pr": True}),
            "zero pr": text({**PAYLOAD, "target_pr": 0}),
            "uppercase digest": text({**PAYLOAD, "new_sha256": "B" * 64}),
            "no-op": text({**PAYLOAD, "new_sha256": "a" * 64}),
            "short nonce": text({**PAYLOAD, "id": "1234"}),
            "branch name as base": text({**PAYLOAD, "base_sha": "main"}),
            "path traversal": text({**PAYLOAD, "path": "../outside"}),
            "absolute path": text({**PAYLOAD, "path": "/etc/passwd"}),
            "short reason": text({**PAYLOAD, "reason": "because"}),
            "validity over 30 days": text({**PAYLOAD, "expires_at": "2026-11-24T00:00:00Z"}),
            "expires before issue": text({**PAYLOAD, "expires_at": "2026-09-23T00:00:00Z"}),
            "non-UTC timestamp": text({**PAYLOAD, "issued_at": "2026-09-24T00:00:00+00:00"}),
            "older FAR schema (B'' FIDO profile)": text({**PAYLOAD, "schema": "far-repin-authorization/2"}),
            "missing domain (B'' payload shape)": text({k: v for k, v in PAYLOAD.items() if k != "domain"}),
            "another domain": text({**PAYLOAD, "domain": "far-release-approval"}),
            "domain differing in case": text({**PAYLOAD, "domain": sig.DOMAIN.upper()}),
            "repository id as string": text({**PAYLOAD, "repository_id": "1283452680"}),
            "repository id as boolean": text({**PAYLOAD, "repository_id": True}),
            "missing repository id": text({k: v for k, v in PAYLOAD.items() if k != "repository_id"}),
            "not an object": "[]",
        }
        for name, bad in cases.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.parse_payload(bad)

    def test_canonical_encoding_is_deterministic(self) -> None:
        shuffled = dict(reversed(list(PAYLOAD.items())))
        self.assertEqual(sig.canonical_bytes(shuffled), sig.canonical_bytes(PAYLOAD))
        with_accent = {**PAYLOAD, "reason": "owner-reviewed réplacement of this exact artifact"}
        self.assertIn(b"\\u00e9", sig.canonical_bytes(with_accent))  # ASCII-only, escaped
        self.assertEqual(sig.parse_payload(text(with_accent)), with_accent)

    def test_equivalent_but_differently_serialized_payloads_are_rejected(self) -> None:
        canonical = text(PAYLOAD)
        variants = {
            "space after colon": canonical.replace('":', '": ', 1),
            "space after comma": canonical.replace(",", ", ", 1),
            "trailing newline (a phone editor's save)": canonical + "\n",
            "CRLF trailing newline": canonical + "\r\n",
            "leading BOM": "﻿" + canonical,
            "escaped ASCII letter": canonical.replace('"schema"', '"sch\\u0065ma"'),
            "escaped slash": canonical.replace("notfoundout/Project-FAR", "notfoundout\\/Project-FAR"),
            "float pull request": canonical.replace('"target_pr":538', '"target_pr":538.0'),
            "exponent pull request": canonical.replace('"target_pr":538', '"target_pr":5.38e2'),
            "raw non-ASCII instead of escape": text({**PAYLOAD, "reason": "owner-reviewed réplacement of this exact artifact"})
                .replace("\\u00e9", "é"),
            "keys out of order": json.dumps(dict(reversed(list(PAYLOAD.items()))), separators=(",", ":")),
        }
        for name, variant in variants.items():
            with self.subTest(case=name):
                self.assertNotEqual(variant, canonical)
                with self.assertRaises(sig.SignatureError):
                    sig.parse_payload(variant)


class PinnedKeyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.key = kit.AgePonyKey(self.dir)

    def test_only_one_plain_p256_key_in_the_agepony_namespace_is_accepted(self) -> None:
        good = self.key.signers().decode()
        self.assertEqual(sig.validate_allowed_signers(good.encode()), (sig.KEY_TYPE, self.key.key_b64))
        cases = {
            "no-touch-required": good.replace(f'{sig.NAMESPACE}"', f'{sig.NAMESPACE}",no-touch-required'),
            "cert-authority": good.replace(f'{sig.NAMESPACE}"', f'{sig.NAMESPACE}",cert-authority'),
            "validity window option": good.replace(f'{sig.NAMESPACE}"', f'{sig.NAMESPACE}",valid-after="20260101"'),
            "any namespace": good.replace(f' namespaces="{sig.NAMESPACE}"', ""),
            "B'' namespace": good.replace(f'"{sig.NAMESPACE}"', '"far-repin-authorization@v1"'),
            "two namespaces": good.replace(f'"{sig.NAMESPACE}"', f'"{sig.NAMESPACE},git"'),
            "wildcard principal": good.replace(sig.PRINCIPAL, "*"),
            "second key": good + good,
            "comment line": "# owner\n" + good,
            "trailing comment": good[:-1] + " far@iphone\n",
            "CRLF": good[:-1] + "\r\n",
            "no newline": good[:-1],
            "ed25519 key type": good.replace(sig.KEY_TYPE, "ssh-ed25519"),
            "FIDO P-256 key type": good.replace(sig.KEY_TYPE, "sk-ecdsa-sha2-nistp256@openssh.com"),
            "P-384 key type": good.replace(sig.KEY_TYPE, "ecdsa-sha2-nistp384"),
            "rsa key type": good.replace(sig.KEY_TYPE, "ssh-rsa"),
        }
        for name, bad in cases.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.validate_allowed_signers(bad.encode())

    def test_key_blob_must_be_a_valid_uncompressed_p256_point(self) -> None:
        point = self.key.point
        x, y = int.from_bytes(point[1:33], "big"), int.from_bytes(point[33:], "big")
        def wire(kind: bytes = kit.KEY_TYPE, curve: bytes = b"nistp256", q: bytes = point, extra: bytes = b"") -> str:
            return base64.b64encode(kit.ssh_string(kind) + kit.ssh_string(curve) + kit.ssh_string(q) + extra).decode()
        cases = {
            "curve name nistp384": wire(curve=b"nistp384"),
            "inner key type differs from line": wire(kind=b"ecdsa-sha2-nistp384"),
            "compressed point": wire(q=bytes([2 + (y & 1)]) + point[1:33]),
            "hybrid point prefix": wire(q=b"\x06" + point[1:]),
            "point off the curve": wire(q=b"\x04" + point[1:33] + ((y + 1) % sig.P256_P).to_bytes(32, "big")),
            "x coordinate not reduced (x + p of a real point)": wire(q=self.unreduced_point()),
            "trailing data after the point": wire(extra=b"\0"),
            "truncated": wire()[:-8],
        }
        for name, key in cases.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.validate_allowed_signers(kit.signers_line(key))

    @staticmethod
    def unreduced_point() -> bytes:
        """``04 || x+p || y`` for a genuine P-256 point with small x: satisfies the curve equation mod p."""
        p, b = sig.P256_P, sig.P256_B
        for x in range(1, 1000):
            rhs = (x * x * x - 3 * x + b) % p
            y = pow(rhs, (p + 1) // 4, p)  # p = 3 (mod 4)
            if y * y % p == rhs:
                assert x + p < 2**256
                return b"\x04" + (x + p).to_bytes(32, "big") + y.to_bytes(32, "big")
        raise AssertionError("no small-x point found")

    def test_unreduced_point_is_otherwise_on_the_curve(self) -> None:
        q = self.unreduced_point()
        x, y = int.from_bytes(q[1:33], "big") % sig.P256_P, int.from_bytes(q[33:], "big")
        self.assertEqual((y * y - (x * x * x - 3 * x + sig.P256_B)) % sig.P256_P, 0)

    def test_non_canonical_base64_key_is_rejected(self) -> None:
        body = self.key.key_b64
        self.assertTrue(body.endswith("="))
        flipped = body[:-2] + chr(ord(body[-2]) + 1) + "="  # same bytes decoded, different spelling
        if base64.b64decode(flipped) == base64.b64decode(body):
            with self.assertRaises(sig.SignatureError):
                sig.validate_allowed_signers(kit.signers_line(flipped))

    def test_pin_key_takes_the_line_agepony_displays(self) -> None:
        repo = self.dir / "repo"
        (repo / "validation_bootstrap").mkdir(parents=True)
        (repo / sig.ASSURANCE_LOCK_PATH).write_text(json.dumps({"schema_version": "1.0", "files": {}}))
        copied = self.dir / "agepony-public-key.txt"
        for pasted in (self.key.display_line(), self.key.display_line() + " FAR repin owner\n", "  " + self.key.display_line() + "\n\n"):
            with self.subTest(pasted=pasted[-20:]):
                copied.write_text(pasted)
                self.assertEqual(sig.main(["pin-key", str(copied), "--repo", str(repo)]), 0)
                self.assertEqual((repo / sig.ALLOWED_SIGNERS_PATH).read_bytes(), self.key.signers())
        for pasted in ("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA==", self.key.display_line() + "\nsecond line", "not a key"):
            with self.subTest(rejected=pasted[:20]):
                copied.write_text(pasted)
                self.assertEqual(sig.main(["pin-key", str(copied), "--repo", str(repo)]), 1)

    def test_fingerprint_matches_openssh(self) -> None:
        (self.dir / "k.pub").write_text(self.key.display_line() + "\n")
        openssh = subprocess.run(["ssh-keygen", "-lf", str(self.dir / "k.pub")], capture_output=True, text=True, check=True).stdout
        self.assertIn(sig.fingerprint(self.key.key_b64), openssh)


class SignatureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.key = kit.AgePonyKey(self.dir)
        self.signers = self.key.signers()
        self.message = sig.canonical_bytes(PAYLOAD)
        self.entry = {"payload": text(PAYLOAD), "signature": self.key.sign(self.message)}

    def test_agepony_signature_verifies(self) -> None:
        self.assertEqual(sig.verify_entry(self.entry, self.signers), PAYLOAD)
        self.assertTrue(openssh_accepts(self.message, self.entry["signature"], self.signers))

    def test_agepony_published_golden_vector_verifies_as_a_signature_but_authorizes_nothing(self) -> None:
        """AgePony's own ecdsa vector: a valid ``agepony`` signature over a non-FAR file."""
        signers = kit.signers_line(kit.AGEPONY_GOLDEN_KEY)
        sig.verify_signature(kit.AGEPONY_GOLDEN_MESSAGE, kit.AGEPONY_GOLDEN_SIGNATURE, signers)
        with self.assertRaises(sig.SignatureError):
            sig.verify_entry({"payload": kit.AGEPONY_GOLDEN_MESSAGE.decode(), "signature": kit.AGEPONY_GOLDEN_SIGNATURE},
                             signers)

    def test_any_change_to_a_signed_payload_is_rejected(self) -> None:
        changed = {
            "one byte of the reason": {**PAYLOAD, "reason": PAYLOAD["reason"].replace("exact", "exacT")},
            "another path": {**PAYLOAD, "path": "far_validation/repin.py"},
            "another pull request": {**PAYLOAD, "target_pr": 539},
            "another new digest": {**PAYLOAD, "new_sha256": "c" * 64},
            "another old digest": {**PAYLOAD, "old_sha256": "d" * 64},
            "another base": {**PAYLOAD, "base_sha": "0" * 40},
            "another repository": {**PAYLOAD, "repository": "notfoundout/Other"},
            "another repository id": {**PAYLOAD, "repository_id": 1},
            "extended expiry": {**PAYLOAD, "expires_at": "2026-10-20T00:00:00Z"},
            "earlier issuance": {**PAYLOAD, "issued_at": "2026-09-23T00:00:00Z"},
            "another nonce (replay under new id)": {**PAYLOAD, "id": "f" * 32},
        }
        for name, payload in changed.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.verify_entry({"payload": text(payload), "signature": self.entry["signature"]}, self.signers)
        for index in range(len(self.message)):  # every single-byte alteration of the signed file
            altered = bytearray(self.message)
            altered[index] ^= 0x01
            with self.subTest(byte=index), self.assertRaises(sig.SignatureError):
                sig.verify_entry({"payload": altered.decode("latin-1"), "signature": self.entry["signature"]}, self.signers)

    def test_arbitrary_agepony_signed_files_authorize_nothing(self) -> None:
        """The owner's FAR key signs, in AgePony's namespace, files that are not exact FAR payloads."""
        files = {
            "a photo": bytes(range(256)) * 4,
            "a note": b"meet at 10",
            "empty file": b"",
            "B'' schema payload": sig.canonical_bytes({**{k: v for k, v in PAYLOAD.items() if k != "domain"},
                                                       "schema": "far-repin-authorization/2"}),
            "payload for another domain": sig.canonical_bytes({**PAYLOAD, "domain": "far-release-approval"}),
            "pretty-printed payload": json.dumps(PAYLOAD, indent=2, sort_keys=True).encode(),
            "payload saved with a trailing newline": self.message + b"\n",
            "payload list": json.dumps([PAYLOAD]).encode(),
            "payload with extra field": sig.canonical_bytes({**PAYLOAD, "note": "x"}),
        }
        for name, data in files.items():
            signature = self.key.sign(data)
            sig.verify_signature(data, signature, self.signers)  # genuinely signed by the pinned key
            with self.subTest(file=name), self.assertRaises(sig.SignatureError):
                sig.verify_entry({"payload": data.decode("latin-1"), "signature": signature}, self.signers)

    def test_namespace_confusion_is_rejected(self) -> None:
        for namespace in ("far-repin-authorization@v1", "git", "file", "agepony2", "AgePony", "agepony\0"):
            with self.subTest(namespace=namespace), self.assertRaises(sig.SignatureError):
                sig.verify_entry({"payload": text(PAYLOAD), "signature": self.key.sign(self.message, namespace=namespace)},
                                 self.signers)

    def test_wrong_and_substituted_keys_are_rejected(self) -> None:
        software = kit.AgePonyKey(self.dir, "software-substitute")
        forged = software.sign(self.message)
        cases = {
            "another P-256 key (software substitute after enrollment)": forged,
            "substitute key spliced into a genuine signature": sig.armor(kit.blob(
                software.wire, kit.inner(*self.key.sign_parts(self.message)))),
            "genuine key spliced into the substitute's signature": sig.armor(kit.blob(
                self.key.wire, kit.inner(*software.sign_parts(self.message)))),
        }
        for name, signature in cases.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.verify_entry({"payload": text(PAYLOAD), "signature": signature}, self.signers)
        # A signature verifies only under its own key, which no gate trusts.
        sig.verify_entry({"payload": text(PAYLOAD), "signature": forged}, software.signers())

    def test_other_signature_algorithms_under_the_same_name_are_rejected(self) -> None:
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "", "-f", str(self.dir / "ed")], check=True)
        target = self.dir / "payload"
        target.write_bytes(self.message)
        subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(self.dir / "ed"), "-n", sig.NAMESPACE, str(target)], check=True)
        kind, key = (self.dir / "ed.pub").read_text().split()[:2]
        with self.assertRaises(sig.SignatureError):  # a valid ed25519 signature, and a pin that names it
            sig.verify_entry({"payload": text(PAYLOAD), "signature": (self.dir / "payload.sig").read_text()},
                             kit.signers_line(key, kind=kind))
        with self.assertRaises(sig.SignatureError):
            sig.verify_entry({"payload": text(PAYLOAD), "signature": (self.dir / "payload.sig").read_text()}, self.signers)

    def test_sha256_message_hash_is_refused(self) -> None:
        signature = self.key.sign(self.message, hash_algorithm="sha256")
        self.assertTrue(openssh_accepts(self.message, signature, self.signers))
        with self.assertRaises(sig.SignatureError):
            sig.verify_entry({"payload": text(PAYLOAD), "signature": signature}, self.signers)

    def test_unsigned_and_forged_entries_are_rejected(self) -> None:
        armored = self.entry["signature"].splitlines()
        body = base64.b64decode("".join(armored[1:-1]))
        tampered = sig.armor(body[:-1] + bytes([body[-1] ^ 1]))
        cases = {
            "unsigned": {"payload": text(PAYLOAD), "signature": ""},
            "self-written text": {"payload": text(PAYLOAD), "signature": "approved by notfoundout"},
            "signature of another payload": {"payload": text(PAYLOAD),
                                             "signature": self.key.sign(sig.canonical_bytes({**PAYLOAD, "target_pr": 1}))},
            "bit-flipped signature": {"payload": text(PAYLOAD), "signature": tampered},
            "signature not a string": {"payload": text(PAYLOAD), "signature": ["-----BEGIN SSH SIGNATURE-----"]},
            "extra entry field": {**self.entry, "approved": True},
        }
        for name, entry in cases.items():
            with self.subTest(case=name), self.assertRaises(sig.SignatureError):
                sig.verify_entry(entry, self.signers)


class MalformedSignatureTests(unittest.TestCase):
    """Malformed and malleable P-256 SSHSIGs. ``openssh`` records what OpenSSH alone would accept."""

    def setUp(self) -> None:
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.key = kit.AgePonyKey(self.dir)
        self.message = sig.canonical_bytes(PAYLOAD)
        self.r, self.s = self.key.sign_parts(self.message)

    def variant(self, **overrides) -> str:
        inner = overrides.pop("inner", kit.inner(self.r, self.s))
        return sig.armor(kit.blob(overrides.pop("wire", self.key.wire), inner, **overrides))

    def mp(self, value: int) -> bytes:
        return kit.write_mpint(value.to_bytes(33, "big"))[4:]

    def components(self, r: bytes, s: bytes, trailing: bytes = b"") -> bytes:
        return kit.ssh_string(kit.KEY_TYPE) + kit.ssh_string(kit.ssh_string(r) + kit.ssh_string(s) + trailing)

    def assert_rejected(self, armored: str, *, openssh: bool) -> None:
        self.assertEqual(openssh_accepts(self.message, armored, self.key.signers()), openssh)
        with self.assertRaises(sig.SignatureError):
            sig.verify_signature(self.message, armored, self.key.signers())
        with self.assertRaises(sig.SignatureError):  # the local parser alone rejects it, too
            sig._check_sshsig(armored, self.key.key_b64)

    def test_encoding_malleability_openssh_accepts_is_rejected(self) -> None:
        genuine = kit.blob(self.key.wire, kit.inner(self.r, self.s))
        encoded = base64.b64encode(genuine).decode()
        cases = {
            "r with a redundant leading zero byte": self.variant(inner=self.components(b"\0" + self.mp(self.r), self.mp(self.s))),
            "s with a redundant leading zero byte": self.variant(inner=self.components(self.mp(self.r), b"\0" + self.mp(self.s))),
            "non-empty reserved field": self.variant(reserved=b"x"),
            "CRLF armor": sig.armor(genuine).replace("\n", "\r\n"),
            "76-column armor": "\n".join([sig.ARMOR_BEGIN, *[encoded[i:i + 76] for i in range(0, len(encoded), 76)],
                                          sig.ARMOR_END]) + "\n",
            "no final newline": sig.armor(genuine)[:-1],
            "blank line inside armor": sig.armor(genuine).replace("\n", "\n\n", 1),
        }
        for name, armored in cases.items():
            with self.subTest(case=name):
                self.assert_rejected(armored, openssh=True)

    def test_malformed_components_are_rejected_locally_and_by_openssh(self) -> None:
        n = sig.P256_N
        r_raw = self.r.to_bytes(32, "big")
        cases = {
            "r = 0": self.variant(inner=self.components(b"", self.mp(self.s))),
            "r = 0 as one zero byte": self.variant(inner=self.components(b"\0", self.mp(self.s))),
            "s = n": self.variant(inner=kit.inner(self.r, n) if n < 2**256 else ""),
            "s = s + n": self.variant(inner=self.components(self.mp(self.r), (self.s + n).to_bytes(33, "big"))),
            "r = r + n": self.variant(inner=self.components((self.r + n).to_bytes(33, "big"), self.mp(self.s))),
            "negative r": self.variant(inner=self.components(b"\x80" + r_raw[1:], self.mp(self.s))),
            "trailing data after s": self.variant(inner=self.components(self.mp(self.r), self.mp(self.s), b"\0\0\0\0")),
            "trailing data after the ECDSA blob": self.variant(inner=kit.inner(self.r, self.s) + b"x"),
            "trailing data after the SSHSIG": self.variant(trailing=b"\0"),
            "SSHSIG version 2": self.variant(version=2),
            "FIDO signature type": self.variant(inner=kit.inner(self.r, self.s, b"sk-ecdsa-sha2-nistp256@openssh.com")),
            "P-384 signature type": self.variant(inner=kit.inner(self.r, self.s, b"ecdsa-sha2-nistp384")),
            "wrong namespace in blob": self.variant(namespace="far-repin-authorization@v1"),
            "sha256 in blob": self.variant(hash_algorithm="sha256"),
            "text before armor": "signed on iPhone\n" + self.variant(),
        }
        for name, armored in cases.items():
            with self.subTest(case=name):
                self.assert_rejected(armored, openssh=False)

    def test_value_malleability_verifies_but_cannot_be_replayed(self) -> None:
        """``(r, n - s)`` is a second valid signature over the same payload (ECDSA is malleable, and
        Secure Enclave signatures are not documented to be low-S normalized, so neither form is refused). It adds no
        power: it authorizes only the same payload, whose ``id`` is single-use in the ledger
        (see ``test_protected_repin_ledger``)."""
        twin = self.variant(inner=kit.inner(self.r, sig.P256_N - self.s))
        self.assertTrue(openssh_accepts(self.message, twin, self.key.signers()))
        self.assertEqual(sig.verify_entry({"payload": text(PAYLOAD), "signature": twin}, self.key.signers()), PAYLOAD)


class OwnerToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.key = kit.AgePonyKey(self.dir)

    def test_prepare_then_agepony_sign_then_bundle_round_trip(self) -> None:
        out = self.dir / "far-538-policy.json"
        self.assertEqual(sig.main(["prepare", "--repository", PAYLOAD["repository"], "--repository-id", "1283452680",
                                   "--path", PAYLOAD["path"], "--old", "a" * 64, "--new", "b" * 64, "--target-pr", "538",
                                   "--base-sha", PAYLOAD["base_sha"], "--reason", PAYLOAD["reason"], "--out", str(out)]), 0)
        payload = sig.parse_payload(out.read_text())
        self.assertEqual((payload["schema"], payload["domain"]), (sig.SCHEMA, sig.DOMAIN))
        self.assertFalse(out.read_bytes().endswith(b"\n"))  # the file AgePony signs is exactly the canonical bytes
        # The returned .sig was re-wrapped in transit (76 columns, CRLF, no final newline); bundling stores canonical armor.
        genuine = self.key.sign(out.read_bytes())
        body = "".join(genuine.splitlines()[1:-1])
        rewrapped = "\r\n".join([sig.ARMOR_BEGIN, *[body[i:i + 76] for i in range(0, len(body), 76)], sig.ARMOR_END])
        self.assertNotEqual(rewrapped.replace("\r\n", "\n"), genuine)
        (self.dir / "far-538-policy.json.sig").write_bytes(rewrapped.encode("ascii"))
        signers = self.dir / "allowed_signers"
        signers.write_bytes(self.key.signers())
        ledger = self.dir / "ledger.json"
        ledger.write_text(json.dumps({"schema_version": "2.0", "consumptions": []}))
        self.assertEqual(sig.main(["bundle", str(out), "--allowed-signers", str(signers), "--append-to", str(ledger)]), 0)
        entry = json.loads(ledger.read_text())["consumptions"][0]
        self.assertEqual(entry["signature"], sig.armor(sig.dearmor(entry["signature"])))
        self.assertEqual(sig.verify_entry(entry, self.key.signers())["id"], payload["id"])

    def test_bundle_refuses_a_signature_that_does_not_verify(self) -> None:
        out = self.dir / "p.json"
        out.write_bytes(sig.canonical_bytes(PAYLOAD))
        (self.dir / "p.json.sig").write_text(kit.AgePonyKey(self.dir, "other").sign(out.read_bytes()))
        signers = self.dir / "allowed_signers"
        signers.write_bytes(self.key.signers())
        ledger = self.dir / "ledger.json"
        ledger.write_text(json.dumps({"schema_version": "2.0", "consumptions": []}))
        self.assertEqual(sig.main(["bundle", str(out), "--allowed-signers", str(signers), "--append-to", str(ledger)]), 1)
        self.assertEqual(json.loads(ledger.read_text())["consumptions"], [])


if __name__ == "__main__":
    unittest.main()
