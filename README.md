# Use Case: Canary a New Model Revision

**YouTube walkthrough:** [Canary Model Revision — System Design #Shorts](https://youtu.be/dke9OsIgSBw)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [05 — Model Monitoring & Behavior Observability](../05-model-monitoring-observability.md)  
**Also references:** [01 — Inference serving](../01-llm-inference-serving.md), [09 — API routing](../09-multi-model-routing-api-platform.md)

## Users & problem

Platform eng ships `v_new` safely. Traffic ramps only if infra and behavioral gates pass against `v_old`.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Initial canary | ~1% sticky traffic |
| Gates | TTFT, errors, safety, thumbs-down bands |
| Auto action | Promote or rollback |
| Sticky | Same users/orgs for fair compare |

## Design (from parent)

```
Registry revision → canary % in router
  → dual metrics (control vs treatment)
  → slice-aware gate evaluator
  → auto-promote / auto-rollback + page on ambiguity
```

Reuse canary contract and signal taxonomy from **05**; wire into router from **01/09**.

## Specializations

| Concern | Canary choice |
|---------|---------------|
| Stickiness | hash(user/org) so UX is stable |
| Duration | Minimum window + minimum sample size |
| Scope | Start on one region/cell |
| Override | Manual hold for risky changes |

## Failure modes

- Simpson’s paradox → always slice (locale, surface, length).
- Safety rate drop (under-refuse) → treat as fail, not “improvement.”
- Canary too small → insufficient power; enforce min samples.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Canary Model Revision — System Design #Shorts](https://youtu.be/dke9OsIgSBw)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd canary-model-revision
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/route -H 'Content-Type: application/json' -d '{"user_id":"u42","prompt":"hi"}' | jq
