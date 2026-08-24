---
name: member-transactions
description: Review the signed-in member's XRCVC Library requests, orders, and cart. Use for a member's own transaction lifecycle; do not use for other members' records or administrative reporting.
---

# Review Member Requests, Orders, and Cart

Use authenticated XRCVC Library MCP Markdown output. The server, not the conversation, decides ownership and role. Never request a Membership ID, bearer value, or OAuth token in chat.

## Allowed member scope

- Start with `/auth/me` through `get_api_output_as_markdown` when role or identity matters.
- Prefer `get_api_output_as_markdown` with `/carts/member` for the bearer member's cart, and `list_member_requests_as_markdown` or `list_member_orders_as_markdown` for complete request/order lists.
- Use `get_member_request` or `get_member_order` for structured detail, or `get_api_output_as_markdown` with `/requests/member/{requestId}` or `/orders/member/{orderId}` for complete Markdown detail. Preserve the server-provided member links and statuses.
- When structured JSON is more useful, use `get_member_cart`, `list_member_requests`, or `list_member_orders`. JSON lists are paginated, so follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown responses are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Current request and order schema

- Expect the member `requestedFor` and `openedBy` maps to be recursively UID-redacted before JSON or Markdown rendering. Preserve human-readable returned fields such as `role`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`; do not request, reconstruct, or invent `userId`, `firebaseUUID`, `adminUID`, or other Firebase identity fields.
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

- Preserve request/order IDs, status labels, dates, human-readable party context, and the on-behalf indicator exactly as returned when relevant.
- Present only `memberRequestUrl`, `memberOrderUrl`, or `memberCartUrl` from member responses. Do not construct or expose Admin Console transaction links.
- Group results into cart, open requests, active orders, and completed history; distinguish no results, unavailable data, access denied, and not found.
- If authentication is required, direct the user to the host's XRCVC OAuth connection flow. Installation alone does not authenticate an account.
