#!/usr/bin/env python3
"""Refresh the Codex cachebuster using the canonical portable release version."""

from datetime import datetime, timezone
import json
from pathlib import Path
import re


def refresh(plugin_root: Path, now: datetime | None = None) -> str:
    portable = json.loads((plugin_root / "plugin.json").read_text())
    version = portable["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?", version):
        raise ValueError("The portable manifest needs a release version without build metadata.")
    instant = now or datetime.now(timezone.utc)
    if instant.tzinfo is None:
        raise ValueError("The cachebuster time must include a timezone.")
    path = plugin_root / ".codex-plugin" / "plugin.json"
    codex = json.loads(path.read_text())
    codex["version"] = f"{version}+codex.{instant.astimezone(timezone.utc):%Y%m%d%H%M%S}"
    path.write_text(json.dumps(codex, indent=2) + "\n")
    return codex["version"]


if __name__ == "__main__":
    print(refresh(Path(__file__).resolve().parents[1] / "plugins" / "xrcvclibrary"))
