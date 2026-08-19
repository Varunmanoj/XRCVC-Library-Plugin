---
name: review-xrcvc-account
description: Explore XRCVC Library identity, Member Tasks, Member Recent Activity, requests, orders, Admin Tasks, and reports from complete MCP Markdown output. Use for account or operational summaries; do not use for catalog-only or cart-only questions.
---

# Review XRCVC Tasks and Activity

Use the authenticated XRCVC Library MCP tools and preserve server-side ownership and role decisions. Never request credentials in chat or treat an OAuth scope as proof of an Admin, Staff, or Developer role.

## MCP output format

- Prefer Markdown output for every authenticated operation. Start with `get_api_output_as_markdown` on `/auth/me` to determine the effective role.
- Use the named complete Markdown tools: `list_requests_as_markdown`, `list_orders_as_markdown`, `get_member_recent_activity_as_markdown`, `list_member_tasks_as_markdown`, and `list_admin_tasks_as_markdown`.
- Use `get_api_output_as_markdown(path, query)` for authenticated detail and report paths that do not have a named companion.
- Markdown list output is complete and unpaginated. Do not send or describe `limit`, `cursor`, `page`, `pageInfo`, next-page handling, or partial-page coverage.
- Treat Markdown returned by the MCP server as source data. Present summaries, tables, and links to the user in Markdown, not as raw JSON.

## Tasks and Recent Activity

### Self-scoped Member application views

- Use `list_member_tasks_as_markdown` for the Member application's own Tasks view. It maps to `/tasks/member`, is scoped by the server to the bearer Membership ID, and is available to authenticated Member, Staff, Admin, and Developer roles.
- Use `get_member_recent_activity_as_markdown` for the bearer Membership ID's complete Recent Activity window. It maps to `/recent-activity/member`, is available to every authenticated role, and cannot target another Membership ID.
- Do not reconstruct Member Tasks from request rows when the named Member Tasks tool is available.
- Do not offer Admin Tasks or reports when the effective role is Member.

### Staff, Admin, and Developer

Use `list_admin_tasks_as_markdown` for the all-operator Admin Tasks dataset exposed at `/tasks/admin`. Staff, Admin, and Developer roles may use it in addition to their own self-scoped Member Tasks and Member Recent Activity views. Admin and Developer roles may also use report Markdown; Staff may not access reports.

## Workflow

1. Determine the authenticated role from `/auth/me` Markdown and choose only role-authorized operations.
2. Use complete request and order Markdown for transaction history. For a single record, request its API detail path through `get_api_output_as_markdown`.
3. For any authenticated role, retrieve its bearer-self-scoped Member Tasks with `list_member_tasks_as_markdown` and Member Recent Activity with `get_member_recent_activity_as_markdown` when the user asks about their own Member application data.
4. For Staff, Admin, or Developer, additionally retrieve the all-operator Admin Tasks view with `list_admin_tasks_as_markdown` when requested.
5. For Admin or Developer reporting, request `/reports`, report detail, table, or combined-report paths through `get_api_output_as_markdown`. Staff must not use reporting paths.

## Response rules

- Separate identity, open requests, active orders, completed history, and next actions.
- State the time range and filters behind a summary. Markdown results are complete and unpaginated.
- Preserve status labels and dates exactly as returned; explain rather than silently normalize them.
- Mention `Requested For` and `Opened By` when returned and relevant to an on-behalf workflow.
- Reports are available only to Admin and Developer roles. Staff can inspect all carts and operational data but cannot access reporting.
- Treat access-denied, unavailable, and not-found results as distinct outcomes.
- Do not call the retired `/my-tasks`, `/recent-activity`, `list_my_tasks`, or `list_my_tasks_as_markdown` contracts; use the explicit member/admin names above.

## Authentication recovery

If the MCP host reports authentication is required, direct the user to its XRCVC OAuth connection flow. A successful plugin installation does not itself authenticate the account. For repeated sign-in across conversations, verify the host is using the plugin's registered XRCVC connector and that refresh-token authorization includes `offline_access`; do not attempt to store or refresh credentials in the skill.
