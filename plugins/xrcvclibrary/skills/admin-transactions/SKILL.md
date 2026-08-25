---
name: admin-transactions
description: Review role-authorized XRCVC Library requests, orders, and saved carts across members. Use for Staff, Admin, and Developer operational transaction work; do not use for reports or a member's self-only question.
---

# Review Admin Requests, Orders, and Carts

Use authenticated XRCVC Library MCP Markdown output and server-enforced access. This operational skill is available only when `/auth/me` reports Staff, Admin, or Developer; never infer that role from the user's wording.

## Required information-view choice

- First call `/auth/me` through `get_api_output_as_markdown`. Never ask the user to state their role or type a Membership ID; use the authenticated identity and role returned by the server.
- If `/auth/me` reports **Member**, do not ask an information-view question and do not use this skill's Admin routes. Hand off to Member Transactions, which directly retrieves the Member's self-scoped cart, requests, or orders.
- If `/auth/me` reports **Staff, Admin, or Developer** and the user has not already explicitly selected self-scope or all-member scope, ask exactly: **“Do you want the cart, requests, or orders for your logged-in Membership ID, or the complete role-authorized Admin list for all Membership IDs?”**
- For Staff, Admin, or Developer, stop after asking that question. Apart from `/auth/me`, do not call a Member or Admin cart/request/order tool and do not display the signed-in person's current cart, requests, or orders until the user chooses a view.
- If Staff, Admin, or Developer chooses their logged-in Membership ID, hand off to Member Transactions and use its self-scoped Member routes. If they choose all Membership IDs, proceed with the Admin routes in this skill.
- Do not repeat the choice when the user already clearly asked for **their own/logged-in Membership ID** or for **all Membership IDs/the complete Admin list**. Server authorization remains decisive.

## MCP output format

- Start with the required `/auth/me` role check and audience-selection gate above.
- Use `list_admin_requests_as_markdown` and `list_admin_orders_as_markdown` for complete role-authorized transaction lists. Apply only supported status, resource-type, or Membership ID filters.
- Use `get_admin_request` or `get_admin_order` for structured detail, or `get_api_output_as_markdown` with `/requests/admin/{requestId}` or `/orders/admin/{orderId}` for complete Markdown detail.
- For a lifecycle explanation, hand off to the Request History or Order History skill and use `get_admin_request_history` or `get_admin_order_history`; order history includes the parent `orderHistory`, every generated request `history`, and stored request-trigger context.
- Use `list_admin_carts` and `get_admin_cart` for structured saved-cart review, or `get_api_output_as_markdown` with `/carts/admin` or `/carts/admin/{membershipId}` for complete Markdown. Saved carts are not submitted transactions.
- When structured JSON is required, use `list_admin_requests`, `list_admin_orders`, or `list_admin_carts` and follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown results are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Current transaction schema

- Treat `requestedFor` and `openedBy` as complete stored party maps. Preserve returned fields such as `role`, `userId`, `firebaseUUID`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`, plus any additional stored fields relevant to the operational question.
- Use `createdOnBehalfOfSomeoneElse` as the authoritative delegation indicator. Describe a transaction as opened on behalf of someone else only when it is `true`; do not recalculate it from names, roles, or partial identifiers.
- Keep `requestDate` and `orderDate` as the transaction creation date/time. Preserve a timestamp nested in `openedBy` only when returned; never invent `openedAt`.
- For requests, retain relevant lifecycle, fulfillment, collection, physical-resource, history, notes, reason, taxonomy, and parent-order fields. For orders, retain `orderHistory`, `orderReason`, `requestIds`, `resourceIds`, `resourceTypes`, `requestCount`, `itemCount`, and linked request context when returned.
- Treat `collectionLocation` as the human-readable portal value. Ready history entries return the St. Xavier's Main Center or Viviana Mall label, or the saved custom-location text.
- Retrieve linked request detail before explaining how a request affected its parent order. Do not infer an order transition or attribution from list position alone.
- Administrative responses include `memberRequestUrl` plus `adminRequestUrl`, `memberOrderUrl` plus `adminOrderUrl`, or `memberCartUrl` plus `adminCartUrl`. Always label both: the member link requires the target member's active session, while the Admin Console link requires existing Staff/Admin/Developer application authorization.

## Date conversion and display

- Treat returned request, order, cart, fulfillment, collection, history, or audit timestamps that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Workflow

1. Confirm the effective role and resolve the required information view before fetching transaction data.
2. Choose requests, orders, carts, or the smallest combination that answers the operational question.
3. Apply the smallest returned-server filter that answers the question and inspect the complete Markdown for analysis.
4. Retrieve detail for any transaction whose lifecycle, requester, order linkage, or status history is being explained.
5. Keep reporting questions in the Admin Reports skill; use the explicit admin cart endpoints for saved-cart investigations.

## Response rules

- Separate carts, requests, and orders, preserve their identifiers/statuses/dates, and retain complete party context and the on-behalf indicator when relevant.
- Present both returned link fields with clear labels; never imply that a member-app link bypasses the target member's session or that an Admin Console link bypasses application authorization.
- Do not present an operational list as a report or infer causes or performance trends that need report data.
- A server access denial is authoritative; explain the boundary and do not try alternate routes to bypass it.
