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
    "public-catalog",
    "member-transactions",
    "admin-transactions",
    "admin-reports",
    "xrcvc-tasks-activity",
    "xrcvc-library-introduction",
    "xrcvc-library-documentation",
}
EXPECTED_CHATGPT_TOOLS = {
    "get_admin_catalog_item",
    "get_admin_manual_section",
    "get_admin_sitemap",
    "get_api_output_as_markdown",
    "get_authenticated_identity",
    "get_catalog_statistics",
    "get_combined_reports",
    "get_library_openapi_schema",
    "get_llms_full_txt",
    "get_llms_txt",
    "get_member_cart",
    "get_member_catalog_item",
    "get_member_manual_section",
    "get_member_recent_activity",
    "get_member_recent_activity_as_markdown",
    "get_member_sitemap",
    "get_order",
    "get_own_cart",
    "get_public_api_output_as_markdown",
    "get_report",
    "get_report_table",
    "get_request",
    "get_taxonomy_item",
    "list_admin_books",
    "list_admin_catalog",
    "list_admin_catalog_as_markdown",
    "list_admin_manual_headings",
    "list_admin_manual_sections",
    "list_admin_tactile_diagrams",
    "list_admin_tasks",
    "list_admin_tasks_as_markdown",
    "list_admin_teaching_learning_aids",
    "list_all_taxonomies",
    "list_carts",
    "list_library_api_endpoints",
    "list_member_books",
    "list_member_catalog",
    "list_member_catalog_as_markdown",
    "list_member_manual_headings",
    "list_member_manual_sections",
    "list_member_tactile_diagrams",
    "list_member_tasks",
    "list_member_tasks_as_markdown",
    "list_member_teaching_learning_aids",
    "list_orders",
    "list_orders_as_markdown",
    "list_reports",
    "list_requests",
    "list_requests_as_markdown",
    "list_taxonomy_collection",
    "list_taxonomy_family",
    "mcp_endpoint_mcp_get",
}
MCP_URL = "https://mcp.library.xrcvc.org/mcp/authorize"
WEBSITE_URL = "https://library.xrcvc.org"
PRIVACY_URL = "https://console.library.xrcvc.org/privacy-policy"
TERMS_URL = "https://console.library.xrcvc.org/terms-of-service"
SUPPORT_URL = "https://console.library.xrcvc.org/plugin-support"
DEVELOPER_NAME = "Xavier's Resource Centre for the Visually Challenged"


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

    chatgpt_submission = load_json(REPO_ROOT / "chatgpt-app-submission.json")
    assert chatgpt_submission.get("$schema") == "https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json"
    assert chatgpt_submission.get("schema_version") == 1
    app_info = chatgpt_submission.get("app_info", {})
    assert app_info.get("display_name") == "XRCVC Library"
    assert DEVELOPER_NAME in str(app_info.get("description", "")), "ChatGPT description must use the official XRCVC organization name"
    assert len(str(app_info.get("subtitle", ""))) <= 30, "ChatGPT subtitle must be at most 30 characters"
    assert app_info.get("category") == "EDUCATION"
    submission_tools = chatgpt_submission.get("tools", {})
    assert set(submission_tools) == EXPECTED_CHATGPT_TOOLS, "ChatGPT submission tool inventory mismatch"
    expected_annotations = {
        "readOnlyHint": True,
        "openWorldHint": False,
        "destructiveHint": False,
    }
    for tool_name, tool in submission_tools.items():
        assert tool.get("annotations") == expected_annotations, f"{tool_name} ChatGPT annotations mismatch"
        justifications = tool.get("justifications", {})
        assert all(
            isinstance(justifications.get(key), str) and justifications[key].strip()
            for key in (
                "read_only_justification",
                "open_world_justification",
                "destructive_justification",
            )
        ), f"{tool_name} needs all ChatGPT hint justifications"
    assert len(chatgpt_submission.get("test_cases", [])) == 5, "ChatGPT submission needs exactly five positive tests"
    assert len(chatgpt_submission.get("negative_test_cases", [])) == 3, "ChatGPT submission needs exactly three negative tests"

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
    assert portable.get("version") == "0.1.4", "portable plugin version mismatch"
    assert claude.get("version") == "0.1.4", "Claude plugin version mismatch"
    assert re.fullmatch(r"0\.1\.4\+codex\.[0-9]{14}", str(codex.get("version", ""))), "Codex plugin cachebuster mismatch"
    assert portable.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert codex.get("repository") == portable.get("repository") == "https://github.com/Varunmanoj/XRCVC-Library-Plugin"
    assert all(item.get("author", {}).get("name") == DEVELOPER_NAME for item in manifests), "developer name mismatch"
    assert DEVELOPER_NAME in submission_text, "submission materials must use the official XRCVC organization name"
    assert portable_mcp.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    assert set(portable).issubset({"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"})

    codex_interface = codex.get("interface", {})
    assert codex.get("homepage") == SUPPORT_URL
    assert codex_interface.get("category") == "Education"
    assert codex_interface.get("developerName") == DEVELOPER_NAME
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
    assert skill_dirs == EXPECTED_SKILLS, f"expected exactly seven skills, found {sorted(skill_dirs)}"
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
    assert claude_marketplace.get("version") == "0.1.4"
    assert claude_entry.get("version") == "0.1.4"
    assert claude_marketplace.get("owner", {}).get("name") == DEVELOPER_NAME
    assert claude_entry.get("author", {}).get("name") == DEVELOPER_NAME
    assert claude.get("repository") == claude_entry.get("repository") == "https://github.com/Varunmanoj/XRCVC-Library-Plugin"

    app_manifest = PLUGIN_ROOT / ".app.json"
    if app_manifest.exists():
        app_payload = load_json(app_manifest)
        app = app_payload.get("apps", {}).get("xrcvc-library", {})
        assert str(app.get("id", "")).startswith("plugin_asdk_app_"), ".app.json must contain the registered ChatGPT MCP connection ID"
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
