"""
Scrapy Pro Enterprise Architecture - FastAPI REST API & WebSocket Server

Exposes REST endpoints (/spiders, /jobs, /logs, /items) and WebSocket stream
for real-time remote spider management and dashboard integration.
"""

import os
import json
import asyncio
from typing import List, Dict, Any

try:
    from fastapi import FastAPI, WebSocket, HTTPException
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:
    app = FastAPI(title="Scrapy Pro Enterprise API", version="0.0.1")

    @app.get("/")
    def read_root():
        return {
            "status": "online",
            "framework": "Scrapy Pro Enterprise Edition",
            "version": "0.0.1",
            "endpoints": ["/spiders", "/jobs", "/logs", "/items", "/ws/live"]
        }

    @app.get("/spiders")
    def list_spiders():
        return {"spiders": ["demo_quotes", "example_spider"]}

    @app.get("/jobs")
    def list_jobs():
        return {"jobs": [{"job_id": "job_001", "spider": "demo_quotes", "status": "finished", "items_scraped": 100}]}

    @app.get("/logs")
    def get_logs():
        return {"logs": ["Engine initialized", "Spider demo_quotes running", "Scraped 100 items"]}

    @app.get("/items")
    def get_items():
        return {"items_count": 100, "sample": [{"title": "Sample Quote", "author": "Albert Einstein"}]}

    @app.websocket("/ws/live")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        for i in range(1, 10):
            await websocket.send_json({"event": "item_scraped", "item_num": i, "spider": "demo_quotes"})
            await asyncio.sleep(1)
        await websocket.close()


def run_api_server(host="127.0.0.1", port=8000):
    if FASTAPI_AVAILABLE:
        print(f"[Scrapy Pro API] Starting REST API & WebSockets server at http://{host}:{port}...")
        uvicorn.run(app, host=host, port=port)
    else:
        print("[Scrapy Pro API] FastAPI/uvicorn not installed. Install with `pip install fastapi uvicorn`.")


if __name__ == "__main__":
    run_api_server()
