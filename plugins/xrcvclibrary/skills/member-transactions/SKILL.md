---
name: member-transactions
description: Review the signed-in member's XRCVC Library requests, orders, and cart. Use for a member's own transaction lifecycle; do not use for other members' records or administrative reporting.
---

# Review Member Requests, Orders, and Cart

Use authenticated XRCVC Library MCP Markdown output. The server, not the conversation, decides ownership and role. Never request a Membership ID, bearer value, or OAuth token in chat.

## Allowed member scope

- Start with `/auth/me` through `get_api_output_as_markdown` when role or identity matters.
- Use `get_api_output_as_markdown` with `/cart` for the bearer member's cart, `/requests` for the bearer member's requests, and `/orders` for the bearer member's orders.
- Use `/requests/{requestId}` and `/orders/{orderId}` for one returned record. Preserve the server-provided links and statuses.
- Markdown responses are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Workflow

1. Fetch only the requested surface, or fetch cart, requests, and orders for a complete personal lifecycle summary.
2. Separate cart contents from submitted requests and orders: a cart item is not a submitted request or an order.
3. For an individual request or order, retrieve its detail before explaining status history, due/return information, or linked records.
4. If a user asks about another member, all-member data, or reports, hand off to the appropriate Admin skill; do not probe privileged routes.

## Response rules

- Preserve request/order IDs, status labels, dates, and `Requested For` or `Opened By` context exactly as returned when relevant.
- Group results into cart, open requests, active orders, and completed history; distinguish no results, unavailable data, access denied, and not found.
- If authentication is required, direct the user to the host's XRCVC OAuth connection flow. Installation alone does not authenticate an account.
