# Trace Candidate 001 — Acquisition Chain

Status: `ACQUISITION_IN_PROGRESS`
Registered: 2026-07-23 (America/New_York)
Candidate source family: SWE-bench / SWE-agent public trajectories
Initial candidate identifier: `django__django-15044.traj`

## Source chain

1. Canonical experiment index: `SWE-bench/experiments`.
2. Submission: `evaluation/lite/20240402_sweagent_gpt4`.
3. Submission metadata declares:
   - logs: `s3://swe-bench-submissions/lite/20240402_sweagent_gpt4/logs`
   - trajectories: `s3://swe-bench-submissions/lite/20240402_sweagent_gpt4/trajs`
4. A public Hugging Face mirror, `sailplane/swe-agent-trajs`, exposes the trajectory corpus in Parquet form and identifies `django__django-15044.traj` as an unresolved ten-step SWE-agent + GPT-4 run.

## Access-friction record

The SWE-bench repository README states that an AWS account and configured AWS CLI are required to download logs and trajectories. The repository's current `analysis/download_logs.py` implementation instead initializes an unsigned S3 client by default (`signature_version=UNSIGNED`), indicating that public unauthenticated retrieval is intended to work without AWS credentials. Both facts are retained because the documented instruction and implementation behavior differ.

Observed local-environment limitation: the execution container available for this run could not resolve `github.com`, so direct cloning was unavailable. Repository files were inspected through the GitHub connector, and trajectory availability was corroborated through the public Hugging Face dataset viewer.

## Evidence-integrity requirements

Before FAR analysis begins, this record must be extended with:

- exact acquired artifact filename;
- source URL or object key;
- acquisition timestamp;
- byte size;
- SHA-256 digest;
- any decompression or conversion steps;
- derived artifact digests;
- confirmation that the raw artifact was not altered before hashing.

No FAR result may be reported from this candidate until the raw trace and benchmark artifacts are locally available and hashed.
