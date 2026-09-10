"""Reproduce protected-validator defects without changing protected files.

Run against an explicit checkout. --expect selects the expected observation,
not an assurance verdict. This is internal maintenance evidence, not EFR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--expect", choices=("defective", "repaired"), required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    from far_validation.assured_engine import ValidationEngine
    from far_validation.model import CheckDefinition
    from far_validation.tracing import parse_strace
    from far_validation.weakening import detect_weakening

    result = ValidationEngine(root)._run_command(CheckDefinition(
        "timeout.reproducer", "partial-output timeout",
        command=(sys.executable, "-c",
                 "import os,time; os.write(1,b'partial\\xff'); os.write(2,b'error'); time.sleep(10)"),
        timeout_seconds=1,
    ))
    try:
        json.dumps(result.to_dict())
        serializable = True
    except TypeError:
        serializable = False
    timeout_defect = result.status == "timed_out" and not serializable

    # Unknown successful dirfds must fail closed. Kernel-annotated dirfds from
    # strace -yy must instead resolve to the actual repository input.
    unresolved = parse_strace('100 openat(3, "secret.txt", O_RDONLY) = 4\n', cwd=root, root=root)
    resolved = parse_strace(
        f'100 openat(3<{root}>, "secret.txt", O_RDONLY) = 4<{root}/secret.txt>\n',
        cwd=root, root=root,
    )
    failed = parse_strace('100 openat(3, "absent.txt", O_RDONLY) = -1 EBADF\n', cwd=root, root=root)
    trace_defect = not unresolved.violations or "secret.txt" not in resolved.reads
    trace_control = not failed.violations

    with tempfile.TemporaryDirectory(prefix="far-rename-reproducer-") as directory:
        repo = Path(directory)
        def git(*arguments: str) -> str:
            return subprocess.check_output(["git", *arguments], cwd=repo, text=True, stderr=subprocess.PIPE).strip()
        git("init", "-q")
        git("config", "user.name", "Internal assurance fixture")
        git("config", "user.email", "fixture@example.invalid")
        (repo / "tests").mkdir()
        source = "".join(f"# retained context {index}\n" for index in range(100))
        source += "def test_required_behavior():\n    assert 1 == 1\n"
        old = repo / "tests/test_old.py"
        old.write_text(source)
        git("add", ".")
        git("commit", "-qm", "baseline")
        base = git("rev-parse", "HEAD")
        git("mv", "tests/test_old.py", "tests/test_new.py")
        (repo / "tests/test_new.py").write_text(source.replace("assert 1 == 1", "pass"))
        git("add", ".")
        git("commit", "-qm", "rename and remove assertion")
        status = git("diff", "--name-status", base, "HEAD")
        if not status.startswith("R"):
            raise RuntimeError(f"reproducer did not establish a rename: {status}")
        report = detect_weakening(repo, base=base)
        rename_defect = report.successful
        rename_observation = {"git_status": status, "accepted": report.successful,
                              "findings": [x.path for x in report.findings]}

    paths = ("far_validation/assured_engine.py", "far_validation/tracing.py", "far_validation/weakening.py")
    defects = {"timeout_json": timeout_defect, "dirfd_trace": trace_defect, "renamed_test": rename_defect}
    expected = args.expect == "defective"
    observation_matches = all(value == expected for value in defects.values()) and trace_control
    print(json.dumps({
        "scope": "internal synthetic maintenance reproductions; not EFR or independent validation",
        "expected_observation": args.expect,
        "observation_matches": observation_matches,
        "defects_observed": defects,
        "negative_control_failed_fd_accepted": trace_control,
        "timeout": {"status": result.status, "json_serializable": serializable},
        "trace": {"unresolved_violations": unresolved.violations, "resolved_reads": resolved.reads},
        "rename": rename_observation,
        "source_sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths},
    }, indent=2, sort_keys=True))
    return 0 if observation_matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
