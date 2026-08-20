---
name: admin-transactions
description: Review role-authorized XRCVC Library requests and orders across members. Use for Staff, Admin, and Developer operational transaction work; do not use for reports or a member's cart-only question.
---

# Review Admin Requests and Orders

Use authenticated XRCVC Library MCP Markdown output and server-enforced access. This operational skill is available only when `/auth/me` reports Staff, Admin, or Developer; never infer that role from the user's wording.

## MCP output format

- Start with `/auth/me` through `get_api_output_as_markdown`.
- Use `list_requests_as_markdown` and `list_orders_as_markdown` for complete, role-authorized transaction lists. Apply only supported status, resource-type, or authorized membership filters.
- Use `get_api_output_as_markdown` with `/requests/{requestId}` or `/orders/{orderId}` for an individual record.
- Markdown results are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Workflow

1. Confirm the effective role, then choose requests, orders, or both according to the operational question.
2. Apply the smallest returned-server filter that answers the question and inspect the complete Markdown for analysis.
3. Retrieve detail for any transaction whose lifecycle, requester, order linkage, or status history is being explained.
4. Keep all-cart investigations in the role-authorized cart interface and reporting questions in the Admin Reports skill.

## Response rules

- Separate requests from orders, preserve their identifiers/statuses/dates, and retain `Requested For` and `Opened By` when relevant.
- Do not present an operational list as a report or infer causes or performance trends that need report data.
- A server access denial is authoritative; explain the boundary and do not try alternate routes to bypass it.
