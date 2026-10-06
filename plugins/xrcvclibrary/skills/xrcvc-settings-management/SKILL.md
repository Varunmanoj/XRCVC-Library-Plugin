---
name: xrcvc-settings-management
description: Update the signed-in person’s XRCVC Library phone/disability details or role-authorized accessibility, report, Testing Mode, and AI settings. Use for explicit profile or settings changes; do not use for another person’s profile or documentation alone.
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

## Own contact details

- Every authenticated role may use `get_member_profile` and `update_member_profile` for its own shared phone and disability details. The server chooses the Membership ID; do not supply a target or use an administrative directory mutation for a self-service edit.
- Accepted update fields are `phone`, `phoneCountryCode`, `phoneDialCode`, `phoneNationalNumber` and `disabilityType`. Read the live schema for accepted country/disability choices and the ten-digit national-number rule; omitted fields remain unchanged. Names, emails, roles, status, membership linkage and verification are not editable through this tool.
- Review the exact requested changes, await the saved response and verify with `get_member_profile` when useful. Ordinary contact edits send no welcome or request/order email. Do not alter Testing Mode, verification or organization-wide settings merely to work around a failed request.
