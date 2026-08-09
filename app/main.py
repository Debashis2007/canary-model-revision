# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Canary Model Revision — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Canary Model Revision"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


CONTROL = "r_old"
CANARY = "r_new"
CANARY_PCT = 10
metrics = {CONTROL: {"n": 0, "ttft_ms": []}, CANARY: {"n": 0, "ttft_ms": []}}

class RouteIn(BaseModel):
    user_id: str
    prompt: str

@app.post("/route")
async def route(body: RouteIn):
    bucket = hash(body.user_id) % 100
    rev = CANARY if bucket < CANARY_PCT else CONTROL
    metrics[rev]["n"] += 1
    metrics[rev]["ttft_ms"].append(40 if rev == CONTROL else 55)
    text = await MockLLM(model=rev).complete(body.prompt, max_tokens=10)
    return {"revision": rev, "text": text}

@app.get("/canary/gates")
def gates():
    def avg(xs):
        return sum(xs) / len(xs) if xs else 0
    c, t = metrics[CONTROL], metrics[CANARY]
    regression = avg(t["ttft_ms"]) > avg(c["ttft_ms"]) * 1.1 if c["ttft_ms"] and t["ttft_ms"] else False
    return {"metrics": {k: {"n": v["n"], "ttft_avg": avg(v["ttft_ms"])} for k, v in metrics.items()}, "auto_rollback": regression}
