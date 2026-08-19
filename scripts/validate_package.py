#!/usr/bin/env python3
"""Validate the portable and host-specific XRCVC Library plugin package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "xrcvclibrary"
EXPECTED_SKILLS = {
    "analyze-xrcvc-catalog",
    "inspect-xrcvc-carts",
    "review-xrcvc-account",
}
MCP_URL = "https://mcp.library.xrcvc.org/mcp/authorize"
WEBSITE_URL = "https://library.xrcvc.org"
PRIVACY_URL = "https://console.library.xrcvc.org/privacy-policy"
TERMS_URL = "https://console.library.xrcvc.org/terms-of-service"
SUPPORT_URL = "https://console.library.xrcvc.org/plugin-support"


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AssertionError(f"{path.relative_to(REPO_ROOT)} is not valid JSON: {error}") from error
    assert isinstance(payload, dict), f"{path.relative_to(REPO_ROOT)} must contain an object"
    return payload


def require_file(path: Path) -> None:
    assert path.is_file(), f"missing {path.relative_to(REPO_ROOT)}"


def validate_skill(skill_dir: Path) -> None:
    skill_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    metadata_file = skill_dir / "agents" / "openai.yaml"
    require_file(skill_file)
    require_file(metadata_file)

    skill_text = skill_file.read_text(encoding="utf-8")
    metadata_text = metadata_file.read_text(encoding="utf-8")
    assert skill_text.startswith("---\n"), f"{skill_name} is missing YAML frontmatter"
    assert re.search(rf"^name:\s*{re.escape(skill_name)}\s*$", skill_text, re.MULTILINE), f"{skill_name} frontmatter name mismatch"
    assert re.search(r"^description:\s*\S", skill_text, re.MULTILINE), f"{skill_name} needs a description"
    assert "TODO" not in skill_text, f"{skill_name} contains unfinished TODO text"
    assert f"${skill_name}" in metadata_text, f"{skill_name} default prompt must name the skill"
    assert MCP_URL in metadata_text, f"{skill_name} dependency URL mismatch"
    assert 'value: "xrcvc-library"' in metadata_text, f"{skill_name} MCP dependency name mismatch"
    assert 'icon_small: "./assets/xrcvc-library-icon.png"' in metadata_text, f"{skill_name} small icon mismatch"
    assert 'icon_large: "./assets/xrcvc-library-logo.png"' in metadata_text, f"{skill_name} large icon mismatch"
    assert 'brand_color: "#E8601C"' in metadata_text, f"{skill_name} brand color mismatch"
    for asset_name in ("xrcvc-library-icon.png", "xrcvc-library-logo.png"):
        asset = skill_dir / "assets" / asset_name
        require_file(asset)
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"{skill_name} {asset_name} is not a PNG"


def validate() -> None:
    submission_text = (REPO_ROOT / "SUBMISSION.md").read_text(encoding="utf-8")
    assert submission_text.count("Expected:") >= 3, "submission needs at least three negative prompt expectations"
    assert "## Positive test prompts" in submission_text, "submission needs positive test prompts"
    positive_section = submission_text.split("## Positive test prompts", 1)[1].split("## Negative", 1)[0]
    assert len(re.findall(r"^\d+\. ", positive_section, re.MULTILINE)) >= 5, "submission needs five positive prompts"

    for asset in (
        PLUGIN_ROOT / "assets" / "xrcvc-library-icon.png",
        PLUGIN_ROOT / "assets" / "xrcvc-library-logo.png",
        PLUGIN_ROOT / "assets" / "xrcvc-and-xavier-logo.png",
    ):
        require_file(asset)
        assert asset.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"{asset.name} is not a PNG"

    codex = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    portable = load_json(PLUGIN_ROOT / "plugin.json")
    portable_mcp = load_json(PLUGIN_ROOT / "mcp.json")
    native_mcp = load_json(PLUGIN_ROOT / ".mcp.json")
    claude = load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
    codex_marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")

    manifests = (codex, portable, claude)
    assert all(item.get("name") == "xrcvclibrary" for item in manifests), "plugin name mismatch"
    assert portable.get("version") == "0.1.3", "portable plugin version mismatch"
    assert claude.get("version") == "0.1.3", "Claude plugin version mismatch"
    assert re.fullmatch(r"0\.1\.3\+codex\.[0-9]{14}", str(codex.get("version", ""))), "Codex plugin cachebuster mismatch"
    assert portable.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert codex.get("repository") == portable.get("repository") == "https://github.com/Varunmanoj/XRCVC-Library-Plugin"
    assert portable_mcp.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    assert set(portable).issubset({"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"})

    codex_interface = codex.get("interface", {})
    assert codex.get("homepage") == SUPPORT_URL
    assert codex_interface.get("category") == "Education"
    assert codex_interface.get("websiteURL") == WEBSITE_URL
    assert codex_interface.get("privacyPolicyURL") == PRIVACY_URL
    assert codex_interface.get("termsOfServiceURL") == TERMS_URL
    assert portable.get("homepage") == SUPPORT_URL
    assert portable.get("extensions", {}).get("org.xrcvc.library") == {
        "websiteURL": WEBSITE_URL,
        "privacyPolicyURL": PRIVACY_URL,
        "termsOfServiceURL": TERMS_URL,
        "supportURL": SUPPORT_URL,
    }
    assert claude.get("homepage") == SUPPORT_URL

    assert native_mcp["mcpServers"]["xrcvc-library"]["url"] == MCP_URL
    assert portable_mcp["mcpServers"]["xrcvc-library"] == {"type": "streamable-http", "url": MCP_URL}
    assert codex.get("mcpServers") == "./.mcp.json"
    assert claude.get("mcpServers") == "./.mcp.json"

    skill_dirs = {path.name for path in (PLUGIN_ROOT / "skills").iterdir() if path.is_dir()}
    assert skill_dirs == EXPECTED_SKILLS, f"expected exactly three skills, found {sorted(skill_dirs)}"
    for skill_name in sorted(EXPECTED_SKILLS):
        validate_skill(PLUGIN_ROOT / "skills" / skill_name)

    codex_entry = codex_marketplace["plugins"][0]
    assert codex_marketplace.get("name") == "xrcvc-library"
    assert codex_entry.get("name") == "xrcvclibrary"
    assert codex_entry.get("source", {}).get("path") == "./plugins/xrcvclibrary"
    assert codex_entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    assert codex_entry.get("category") == "Education"

    claude_entry = claude_marketplace["plugins"][0]
    assert claude_marketplace.get("name") == "xrcvc-library"
    assert claude_entry.get("name") == "xrcvclibrary"
    assert claude_entry.get("source") == "./plugins/xrcvclibrary"
    assert claude_entry.get("homepage") == SUPPORT_URL
    assert claude_entry.get("category") == "Education"
    assert claude_marketplace.get("version") == "0.1.3"
    assert claude_entry.get("version") == "0.1.3"
    assert claude.get("repository") == claude_entry.get("repository") == "https://github.com/Varunmanoj/XRCVC-Library-Plugin"

    app_manifest = PLUGIN_ROOT / ".app.json"
    if app_manifest.exists():
        app_payload = load_json(app_manifest)
        app = app_payload.get("apps", {}).get("xrcvc-library", {})
        assert str(app.get("id", "")).startswith("plugin_asdk_app_"), ".app.json must contain the real registered ChatGPT app ID"
        assert codex.get("apps") == "./.app.json", "Codex manifest must reference an existing .app.json"
    else:
        assert "apps" not in codex, "Codex manifest must not reference a missing .app.json"


if __name__ == "__main__":
    try:
        validate()
    except AssertionError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("XRCVC Library plugin package validation passed.")
