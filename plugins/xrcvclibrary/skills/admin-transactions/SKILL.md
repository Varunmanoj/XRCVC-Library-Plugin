---
name: admin-transactions
description: Review role-authorized XRCVC Library requests, orders, and saved carts across members. Use for Staff, Admin, and Developer operational transaction work; do not use for reports or a member's self-only question.
---

# Review Admin Requests, Orders, and Carts

Use authenticated XRCVC Library MCP Markdown output and server-enforced access. This operational skill is available only when `/auth/me` reports Staff, Admin, or Developer; never infer that role from the user's wording.

## MCP output format

- Start with `/auth/me` through `get_api_output_as_markdown`.
- Use `list_admin_requests_as_markdown` and `list_admin_orders_as_markdown` for complete role-authorized transaction lists. Apply only supported status, resource-type, or Membership ID filters.
- Use `get_admin_request` or `get_admin_order` for structured detail, or `get_api_output_as_markdown` with `/requests/admin/{requestId}` or `/orders/admin/{orderId}` for complete Markdown detail.
- Use `list_admin_carts` and `get_admin_cart` for structured saved-cart review, or `get_api_output_as_markdown` with `/carts/admin` or `/carts/admin/{membershipId}` for complete Markdown. Saved carts are not submitted transactions.
- When structured JSON is required, use `list_admin_requests`, `list_admin_orders`, or `list_admin_carts` and follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown results are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Current transaction schema

- Treat `requestedFor` and `openedBy` as complete stored party maps. Preserve returned fields such as `role`, `userId`, `firebaseUUID`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`, plus any additional stored fields relevant to the operational question.
- Use `createdOnBehalfOfSomeoneElse` as the authoritative delegation indicator. Describe a transaction as opened on behalf of someone else only when it is `true`; do not recalculate it from names, roles, or partial identifiers.
- Keep `requestDate` and `orderDate` as the transaction creation date/time. Preserve a timestamp nested in `openedBy` only when returned; never invent `openedAt`.
- For requests, retain relevant lifecycle, fulfillment, collection, physical-resource, history, notes, reason, taxonomy, and parent-order fields. For orders, retain `orderHistory`, `orderReason`, `requestIds`, `resourceIds`, `resourceTypes`, `requestCount`, `itemCount`, and linked request context when returned.
- Retrieve linked request detail before explaining how a request affected its parent order. Do not infer an order transition or attribution from list position alone.
- Administrative responses include `memberRequestUrl` plus `adminRequestUrl`, `memberOrderUrl` plus `adminOrderUrl`, or `memberCartUrl` plus `adminCartUrl`. Always label both: the member link requires the target member's active session, while the Admin Console link requires existing Staff/Admin/Developer application authorization.

## Workflow

1. Confirm the effective role, then choose requests, orders, carts, or the smallest combination that answers the operational question.
2. Apply the smallest returned-server filter that answers the question and inspect the complete Markdown for analysis.
3. Retrieve detail for any transaction whose lifecycle, requester, order linkage, or status history is being explained.
4. Keep reporting questions in the Admin Reports skill; use the explicit admin cart endpoints for saved-cart investigations.

## Response rules

- Separate carts, requests, and orders, preserve their identifiers/statuses/dates, and retain complete party context and the on-behalf indicator when relevant.
- Present both returned link fields with clear labels; never imply that a member-app link bypasses the target member's session or that an Admin Console link bypasses application authorization.
- Do not present an operational list as a report or infer causes or performance trends that need report data.
- A server access denial is authoritative; explain the boundary and do not try alternate routes to bypass it.
