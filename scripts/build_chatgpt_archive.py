#!/usr/bin/env python3
"""Build the ChatGPT website upload using its registered app identity."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = json.loads((ROOT / "chatgpt-upload-identity.json").read_text())
APP_ID_PATTERN = r"(?:asdk_app_|connector_|templated_apps_)[A-Za-z0-9][A-Za-z0-9_-]*"


def registered_app_id(value: str) -> str:
    # A plugin-page URL adds plugin_ to the registered app identity.
    if value.startswith("plugin_asdk_app_"):
        value = value.removeprefix("plugin_")
    if not re.fullmatch(APP_ID_PATTERN, value):
        raise ValueError("The ChatGPT upload needs a valid registered app identifier.")
    return value


def validate_archive(path: Path, source: Path) -> dict:
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("The ChatGPT ZIP failed its integrity check.")
        app = json.loads(archive.read(".app.json"))["apps"][IDENTITY["appKey"]]
        if not re.fullmatch(APP_ID_PATTERN, app["id"]):
            raise ValueError("The ChatGPT ZIP contains an invalid app identifier.")
        original = json.loads((source / ".app.json").read_text())["apps"]["xrcvc-library"]
        if app["id"] != registered_app_id(original["id"]):
            raise ValueError("The ChatGPT ZIP changed the registered app identity.")
        manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
        if manifest["name"] != IDENTITY["name"] or app["id"] != IDENTITY["appId"]:
            raise ValueError("The ChatGPT upload must preserve the accepted plugin and app identities.")
        if manifest["version"] != json.loads((source / "plugin.json").read_text())["version"]:
            raise ValueError("The ChatGPT upload version must match the canonical release version.")
        if "mcpServers" in manifest or ".mcp.json" in archive.namelist():
            raise ValueError("The ChatGPT upload must use the registered app connection.")
        if manifest.get("apps") != "./.app.json":
            raise ValueError("The ChatGPT manifest must reference the bundled app manifest.")
        for key in ("composerIcon", "logo", "logoDark"):
            archive.read(manifest["interface"][key].removeprefix("./"))
        for file in (source / "skills").rglob("*"):
            if file.is_file() and archive.read(file.relative_to(source).as_posix()) != file.read_bytes():
                raise ValueError(f"ChatGPT skill differs from source: {file.relative_to(source)}")
        for file in (source / "skills").glob("*/agents/openai.yaml"):
            metadata = archive.read(file.relative_to(source).as_posix()).decode()
            skill_root = file.parent.parent.relative_to(source)
            for field in ("icon_small", "icon_large"):
                match = re.search(rf'{field}: "([^"\n]+)"', metadata)
                if not match:
                    raise ValueError(f"Missing skill icon: {file}")
                asset = archive.read((skill_root / match.group(1).removeprefix("./")).as_posix())
                root_asset = "composerIcon" if field == "icon_small" else "logo"
                if asset != archive.read(manifest["interface"][root_asset].removeprefix("./")):
                    raise ValueError(f"Skill icon differs from plugin asset: {file}")
        return {"name": manifest["name"], "appId": app["id"], "version": manifest["version"],
                "skills": sum(name.endswith("/SKILL.md") for name in archive.namelist())}


def build(source: Path, output: Path) -> dict:
    app = json.loads((source / ".app.json").read_text())
    app["apps"]["xrcvc-library"]["id"] = registered_app_id(app["apps"]["xrcvc-library"]["id"])
    app = {"apps": {IDENTITY["appKey"]: {"id": app["apps"]["xrcvc-library"]["id"]}}}
    manifest = json.loads((source / ".codex-plugin/plugin.json").read_text())
    manifest["name"] = IDENTITY["name"]
    manifest["version"] = json.loads((source / "plugin.json").read_text())["version"]
    manifest["author"]["name"] = "Xavier's Resource Centre for the Visually Challenged (XRCVC)"
    manifest["interface"]["developerName"] = manifest["author"]["name"]
    manifest.pop("mcpServers", None)
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = output.with_suffix(".tmp.zip")
    try:
        with ZipFile(staging, "w", ZIP_DEFLATED) as archive:
            for name, payload in ((".app.json", app), (".codex-plugin/plugin.json", manifest)):
                archive.writestr(name, json.dumps(payload, indent=2) + "\n")
            archive.write(source / "README.md", "README.md")
            for directory in ("assets", "skills"):
                for file in sorted((source / directory).rglob("*")):
                    if file.is_file():
                        archive.write(file, file.relative_to(source).as_posix())
        result = validate_archive(staging, source)
        staging.replace(output)
        return result
    finally:
        staging.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(ROOT / "plugins/xrcvclibrary", args.output), indent=2))
