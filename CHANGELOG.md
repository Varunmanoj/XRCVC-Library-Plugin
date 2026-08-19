# Changelog

All notable changes to this project will be documented here.

## 0.1.1 - 2026-08-19

- Updated all three skills to prefer complete MCP Markdown outputs over paginated JSON lists.
- Switched the account skill to the deployed `list_member_tasks_as_markdown`, `list_admin_tasks_as_markdown`, and `get_member_recent_activity_as_markdown` tools and their explicit forward-only API routes.
- Clarified that Member Tasks and Member Recent Activity are bearer-self-scoped views available to authenticated Developer, Admin, Staff, and Member roles; Admin Tasks remains the separate all-operator view.
- Connected the public Terms of Service and Plugin Support URLs to the OpenAI/Codex, portable Agent Plugins, and Claude package metadata supported by each format.
- Added validation that prevents the website, privacy, terms, and support listing URLs from drifting across connector packages.

## 0.1.0 - 2026-08-19

- Added OpenAI/Codex, Agent Plugins 1.0, and Claude plugin manifests.
- Added the XRCVC Library OAuth MCP connection.
- Added catalog, cart, and account/activity skills.
- Added XRCVC Library branding, marketplace metadata, validation, and installation documentation.
