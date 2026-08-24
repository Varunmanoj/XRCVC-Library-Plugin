---
name: member-transactions
description: Review the signed-in member's XRCVC Library requests, orders, and cart. Use for a member's own transaction lifecycle; do not use for other members' records or administrative reporting.
---

# Review Member Requests, Orders, and Cart

Use authenticated XRCVC Library MCP Markdown output. The server, not the conversation, decides ownership and role. Never request a Membership ID, bearer value, or OAuth token in chat.

## Allowed member scope

- Start with `/auth/me` through `get_api_output_as_markdown` when role or identity matters.
- Prefer `get_api_output_as_markdown` with `/cart` for the bearer member's cart, and `list_requests_as_markdown` or `list_orders_as_markdown` for complete request/order lists.
- Use `get_request` or `get_order` for structured detail, or `get_api_output_as_markdown` with `/requests/{requestId}` or `/orders/{orderId}` for complete Markdown detail. Preserve the server-provided links and statuses.
- When structured JSON is more useful, use `get_own_cart`, `list_requests`, or `list_orders`. JSON lists are paginated, so follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown responses are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Current request and order schema

- Treat `requestedFor` and `openedBy` as complete stored party maps. Preserve returned fields such as `role`, `userId`, `firebaseUUID`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`, plus any additional stored fields relevant to the question.
- Use `createdOnBehalfOfSomeoneElse` as the authoritative delegation indicator. Say a request or order was created on behalf of someone else only when it is `true`; do not infer delegation from names, roles, or missing identifiers.
- Keep the returned `requestDate` or `orderDate` as the transaction creation date/time. Preserve a timestamp inside `openedBy` only if the server actually returns one; never invent an `openedAt` field.
- Requests may include lifecycle, fulfillment, collection, physical-resource, history, notes, reason, taxonomy, and parent-order fields. Orders may include `orderHistory`, `orderReason`, linked `requestIds`, resource IDs/types, and request/item counts. Explain only fields actually returned.
- Cart records are saved selections, not submitted transactions. Do not attach request/order party or on-behalf semantics to cart items unless the server returns those fields.

## Workflow

1. Fetch only the requested surface, or fetch cart, requests, and orders for a complete personal lifecycle summary.
2. Separate cart contents from submitted requests and orders: a cart item is not a submitted request or an order.
3. For an individual request or order, retrieve its detail before explaining status history, due/return information, or linked records.
4. If a user asks about another member, all-member data, or reports, hand off to the appropriate Admin skill; do not probe privileged routes.

## Response rules

- Preserve request/order IDs, status labels, dates, complete party context, and the on-behalf indicator exactly as returned when relevant.
- Group results into cart, open requests, active orders, and completed history; distinguish no results, unavailable data, access denied, and not found.
- If authentication is required, direct the user to the host's XRCVC OAuth connection flow. Installation alone does not authenticate an account.
