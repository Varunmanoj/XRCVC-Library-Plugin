#!/usr/bin/env python3
"""Compare a saved public MCP tools/list response with the plugin declaration."""

import argparse
import json
from pathlib import Path


def validate(submission: dict, response: dict) -> dict:
    tools = response.get("result", response)["tools"]
    live = {tool["name"]: tool for tool in tools}
    expected = submission["tools"]
    if len(live) != len(tools):
        raise ValueError("The live response contains duplicate tool names.")
    if set(live) != set(expected):
        raise ValueError(f"Tool inventory differs: missing={sorted(set(expected)-set(live))}, unexpected={sorted(set(live)-set(expected))}")
    for name, entry in expected.items():
        for key, value in entry["annotations"].items():
            if live[name].get("annotations", {}).get(key) != value:
                raise ValueError(f"{name} {key} differs from the live declaration.")
    return {"tools": len(live), "mutations": sum(not entry["annotations"]["readOnlyHint"] for entry in expected.values())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tools_response", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(validate(json.loads((root / "chatgpt-app-submission.json").read_text()), json.loads(args.tools_response.read_text()))))
