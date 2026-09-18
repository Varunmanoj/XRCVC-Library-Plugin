---
name: xrcvc-settings-management
description: Update XRCVC Library accessibility, report, Developer Mode, or AI settings through role-authorized MCP tools. Use when a user explicitly asks to change settings; do not use merely to explain settings documentation.
---

# Manage XRCVC Library Settings

Use `get_authenticated_identity` before any mutation. Membership ID remains the server's single identity source and is obtained from the authenticated connection; never ask the user to paste a Membership ID credential, bearer value, OAuth code, or token.

## Settings boundaries

- `update_accessibility_settings` is self-scoped. Omit any optional target Membership ID and update only the settings bound to the authenticated Membership ID, including when the effective role is Staff, Admin, or Developer.
- `update_report_defaults` requires Admin or Developer.
- `update_developer_settings` and `update_ai_settings` require Developer.
- Staff and Member cannot update report defaults, Developer Mode, or AI configuration. A role denial is authoritative.
- AI-setting responses intentionally omit stored secrets. Never ask for, display, or infer an existing secret value.

## Mutation workflow

1. Determine whether the request concerns personal accessibility preferences, report defaults, Developer Mode, or AI configuration, then confirm the effective role.
2. Use the live MCP input schema to identify accepted fields and values. Do not forward conversational prose as an unreviewed settings object.
3. Summarize the exact fields that will change. Obtain explicit confirmation before changing Developer Mode, AI configuration, or any setting that may affect organization-wide behavior.
4. Call only the matching tool and report returned values without inventing omitted settings. When a read endpoint is available, verify the new state afterward.

## Safety rules

- A question about how a setting works is documentation intent, not permission to change it.
- Never target another Membership ID through the self-scoped accessibility tool, even if a client schema exposes an optional target parameter.
- Do not claim a secret was unchanged, stored, or removed unless the server explicitly reports that outcome.
- Clearly distinguish successful mutation, role denial, validation failure, and unverified post-write state.
