---
name: review-xrcvc-account
description: Review authenticated XRCVC Library identity, requests, orders, recent activity, staff tasks, and administrative reports. Use for account or operational summaries; do not use for catalog-only or cart-only questions.
---

# Review XRCVC Account

Use the authenticated XRCVC Library MCP tools and preserve server-side ownership and role decisions. Never request credentials in chat or treat an OAuth scope as proof of an Admin, Staff, or Developer role.

## Workflow

1. Start with `get_authenticated_identity`. Use the returned effective role and capabilities to choose the remaining tools.
2. Use `list_requests`/`get_request` and `list_orders`/`get_order` for transaction history. Follow opaque cursors only as far as the question requires.
3. Members may use `get_member_recent_activity`; do not offer staff task or report tools to Members.
4. Staff may use `list_my_tasks` and cross-member operational request/order data, but must not use reporting tools.
5. Admin and Developer roles may use `list_my_tasks`, `list_reports`, `get_report`, `get_report_table`, and `get_combined_reports` as appropriate.
6. Prefer the named Markdown companions when the user requests a complete unpaginated document. Use structured JSON tools for focused lookups and comparisons.

## Response rules

- Separate identity, open requests, active orders, completed history, and next actions.
- State the time range, filters, and pagination coverage behind a summary.
- Preserve status labels and dates exactly as returned; explain rather than silently normalize them.
- Mention `Requested For` and `Opened By` when returned and relevant to an on-behalf workflow.
- Reports are available only to Admin and Developer roles. Staff can inspect all carts and operational data but cannot access reporting.
- Treat access-denied, unavailable, and not-found results as distinct outcomes.

## Authentication recovery

If the MCP host reports authentication is required, direct the user to its XRCVC OAuth connection flow. A successful plugin installation does not itself authenticate the account. For repeated sign-in across conversations, verify the host is using the plugin's registered XRCVC connector and that refresh-token authorization includes `offline_access`; do not attempt to store or refresh credentials in the skill.
