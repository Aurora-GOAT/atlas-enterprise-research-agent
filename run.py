"""Run: python run.py --host 127.0.0.1 --port 8000"""
from __future__ import annotations
import argparse
import uvicorn

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args()
    uvicorn.run("research_agent.api:app", host=args.host, port=args.port, reload=False)
