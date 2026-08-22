#!/usr/bin/env python3
"""
CLI for the routing agent (SQL vs RAG vs hybrid). Useful for LangFuse trace demos.

Usage:
  python scripts/run_agent_cli.py
  python scripts/run_agent_cli.py --session demo-1 "How many customers do we have?"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent.runner import run_agent


def main():
    parser = argparse.ArgumentParser(description="Routing agent CLI")
    parser.add_argument("question", nargs="?", help="Question to ask")
    parser.add_argument("--session", default="cli-session", help="Thread id for memory")
    args = parser.parse_args()

    if args.question:
        questions = [args.question]
    else:
        print("Interactive mode. Empty line to quit.\n")
        questions = []
        while True:
            q = input("You: ").strip()
            if not q:
                break
            questions.append(q)

    for question in questions:
        result = run_agent(question, session_id=args.session)
        print(f"\n[route={result['route']}]")
        print(result["answer"])
        if result.get("error"):
            print(f"(error: {result['error']})", file=sys.stderr)


if __name__ == "__main__":
    main()
