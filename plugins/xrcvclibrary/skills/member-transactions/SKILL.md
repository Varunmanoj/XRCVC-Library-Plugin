---
name: member-transactions
description: Review the signed-in person's self-scoped XRCVC Library requests, orders, and cart. Use for personal transaction data after role-aware audience selection; do not use for other members' records or administrative reporting.
---

# Review Member Requests, Orders, and Cart

Use authenticated XRCVC Library MCP Markdown output. The server, not the conversation, decides ownership and role. Never request a Membership ID, bearer value, or OAuth token in chat.

## Required information-view choice

- First call `/auth/me` through `get_api_output_as_markdown`. Never ask the user to state their role or type a Membership ID; use the authenticated identity and role returned by the server.
- If `/auth/me` reports **Member**, do not ask an information-view question. Proceed directly with the requested self-scoped Member cart, requests, or orders because Members cannot access other Membership IDs' transaction data.
- If `/auth/me` reports **Staff, Admin, or Developer** and the user has not already explicitly selected self-scope or all-member scope, ask exactly: **“Do you want the cart, requests, or orders for your logged-in Membership ID, or the complete role-authorized Admin list for all Membership IDs?”**
- For Staff, Admin, or Developer, stop after asking that question. Apart from `/auth/me`, do not call a Member or Admin cart/request/order tool and do not display the signed-in person's current cart, requests, or orders until the user chooses a view.
- If Staff, Admin, or Developer chooses their logged-in Membership ID, use only the self-scoped Member routes in this skill. If they choose all Membership IDs, hand off to the Admin Transactions skill and use its Admin routes.
- Do not repeat the choice when the user already clearly asked for **their own/logged-in Membership ID** or for **all Membership IDs/the complete Admin list**. Server authorization remains decisive.

## Allowed member scope

- Start with the required `/auth/me` role check and audience-selection gate above.
- For the signed-in person's own profile, use `get_member_profile`. It is bearer-self-scoped and UID-redacted for every authenticated role; do not probe `list_admin_profiles`, `get_admin_profile`, or Membership ID administrative routes for a self-profile question.
- Prefer `get_api_output_as_markdown` with `/carts/member` for the bearer member's cart, and `list_member_requests_as_markdown` or `list_member_orders_as_markdown` for complete request/order lists.
- Use `get_member_request` or `get_member_order` for structured detail, or `get_api_output_as_markdown` with `/requests/member/{requestId}` or `/orders/member/{orderId}` for complete Markdown detail. Preserve the server-provided member links and statuses.
- For a lifecycle explanation, hand off to the Request History or Order History skill and use `get_member_request_history` or `get_member_order_history`; the latter returns the parent `orderHistory` plus every generated request and its `history`.
- For archived requests or orders, hand off to Member Archives and use the dedicated `isArchived=true` archive tools. Never use `status=archived` because archive state is a separate Boolean field.
- When structured JSON is more useful, use `get_member_cart`, `list_member_requests`, or `list_member_orders`. JSON lists are paginated, so follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown responses are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Current request and order schema

- Expect the member `requestedFor` and `openedBy` maps to be recursively UID-redacted before JSON or Markdown rendering. Preserve human-readable returned fields such as `role`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`; do not request, reconstruct, or invent `userId`, `firebaseUUID`, `adminUID`, or other Firebase identity fields.
- Use `createdOnBehalfOfSomeoneElse` as the authoritative delegation indicator. Say a request or order was created on behalf of someone else only when it is `true`; do not infer delegation from names, roles, or missing identifiers.
- Keep the returned `requestDate` or `orderDate` as the transaction creation date/time. Preserve a timestamp inside `openedBy` only if the server actually returns one; never invent an `openedAt` field.
- Requests may include lifecycle, fulfillment, collection, physical-resource, history, notes, reason, taxonomy, and parent-order fields. Orders may include `orderHistory`, `orderReason`, linked `requestIds`, resource IDs/types, and request/item counts. Explain only fields actually returned.
- `collectionLocation` is human-readable in request responses and ready history entries: it returns the portal label for St. Xavier's Main Center or Viviana Mall, or the saved custom-location text.
- Cart records are saved selections, not submitted transactions. Do not attach request/order party or on-behalf semantics to cart items unless the server returns those fields.

## Date conversion and display

- Treat returned request, order, cart, fulfillment, collection, history, or activity timestamps that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Workflow

1. Resolve the authenticated role and, when required, the information view before fetching transaction data.
2. Fetch only the requested surface, or fetch cart, requests, and orders for a complete personal lifecycle summary.
3. Separate cart contents from submitted requests and orders: a cart item is not a submitted request or an order.
4. For an individual request or order, retrieve its detail before explaining status history, due/return information, or linked records.
5. If a user asks about another member, all-member data, or reports, hand off to the appropriate Admin skill; do not probe privileged routes.

## Response rules

- Preserve request/order IDs, status labels, dates, human-readable party context, and the on-behalf indicator exactly as returned when relevant.
- Present only `memberRequestUrl`, `memberOrderUrl`, or `memberCartUrl` from member responses. Do not construct or expose Admin Console transaction links.
- Group results into cart, open requests, active orders, and completed history; distinguish no results, unavailable data, access denied, and not found.
- If authentication is required, direct the user to the host's XRCVC OAuth connection flow. Installation alone does not authenticate an account.
