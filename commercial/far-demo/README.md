# FAR Demo

A hosted, link-shareable demonstration interface for Project FAR 1.0.

## What it does

The demo compares a baseline and candidate AI-agent event trace, highlights material changes, surfaces missing authorization evidence, preserves explicit unknowns, and emits a deterministic SHA-256 report fingerprint.

The initial public format is intentionally narrow:

```json
{
  "trace_id": "example",
  "events": [
    {
      "event_id": "e1",
      "actor": "agent",
      "action": "approval_recorded",
      "approved": true,
      "statement": "Supervisor approval recorded."
    }
  ]
}
```

This demo does not accept arbitrary logs and does not infer hidden reasoning, external truth, safety, or regulatory compliance.

## Local run

From the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e commercial/far-decision-integrity
pip install -e commercial/far-demo
uvicorn far_demo.app:app --reload
```

Open `http://localhost:8000`.

## Container

From the repository root:

```bash
docker build -f commercial/far-demo/Dockerfile -t far-demo .
docker run --rm -p 8000:8000 far-demo
```

## Render

Create a Render Blueprint from `commercial/far-demo/render.yaml`, or configure a Python web service with:

- Build: `pip install -e commercial/far-decision-integrity && pip install -e commercial/far-demo`
- Start: `uvicorn far_demo.app:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

## Public demo flow

1. Open the URL.
2. Select **Try the example**, or upload two JSON traces.
3. Read the verdict, findings, and explicit unknowns.
4. Expand **Advanced evidence** to inspect the deterministic report.
