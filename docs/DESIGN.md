# Design: Canary Model Revision

**Project:** `canary-model-revision`  
**Parent system design:** `05-model-monitoring-observability.md`

## 1. What this POC demonstrates

Sticky canary percentage routing with TTFT gate comparison for auto-rollback signal.

## 2. Architecture (POC)

```text
hash(user) % 100 → control|canary revision → metrics → /canary/gates
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Sticky hashing | Fair A/B and stable UX per user. | `hash(user_id) % 100`. |
| Dual metrics | Compare control vs treatment on same shape. | `metrics` dict. |
| Auto-rollback flag | Ship gates must be automated. | `auto_rollback` on TTFT regression. |

## 4. Key endpoints

`GET /health`, `POST /route`, `GET /canary/gates`

## 5. Tradeoffs / POC limits

Only TTFT proxy — add safety/quality slices next.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

Narrated with **ElevenLabs Debpro voice** and Debpro still image (via [GitaProject](/Users/deb/Development/GenAI/GitaProject)):

- Video: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Script: [`video/narration.txt`](./video/narration.txt)

