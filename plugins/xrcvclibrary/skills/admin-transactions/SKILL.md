---
name: admin-transactions
description: Review and manage role-authorized XRCVC Library requests, orders, and saved carts across members. Use for Staff, Admin, and Developer operational reads or explicit on-behalf creation and lifecycle updates; do not use for reports or a member's self-only question.
---

# Review and Manage Admin Requests, Orders, and Carts

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
- Use `list_admin_requests_as_markdown(..., is_archived=false, active_only=true)` and `list_admin_orders_as_markdown(..., is_archived=false, active_only=true)` for bare, ordinary, current, active, unfinished, outstanding, or action-needed role-authorized transaction lists. `active_only=true` is also the tool default, so a plain “list the requests” remains lifecycle-active even when the user supplies no active-status keyword.
- Use `get_admin_request` or `get_admin_order` for structured detail, or `get_api_output_as_markdown` with `/requests/admin/{requestId}` or `/orders/admin/{orderId}` for complete Markdown detail.
- For a lifecycle explanation, hand off to the Request History or Order History skill and use `get_admin_request_history` or `get_admin_order_history`; order history includes the parent `orderHistory`, every generated request `history`, and stored request-trigger context.
- Treat `is_archived=false` as mandatory for every ordinary request or order list, including lists that also use Membership ID, status, or resource-type filters. Keep `active_only=true` unless the user explicitly requests all/every non-archived records or explicitly names a terminal lifecycle status.
- Return archived requests or orders only when the user explicitly asks for archived records. In that case, hand off to Admin Archives and use its dedicated archive tools, which enforce stored `isArchived=true` and support the optional requested-for Membership ID filter. Never use `status=archived` because archive state is a separate Boolean field.
- Use `list_admin_carts` and `get_admin_cart` for structured saved-cart review, or `get_api_output_as_markdown` with `/carts/admin` or `/carts/admin/{membershipId}` for complete Markdown. Saved carts are not submitted transactions.
- Every `get_admin_cart` call evaluates the saved items against the current catalog state. Use `isRequestable`, `requestabilityStatus`, `requestabilityReason`, `requestabilityMessage`, `requestableItemCount`, `blockedItemCount`, and `canPlaceOrder` as returned. A fresh call clears a blocked state after requestability is restored without polling; administrative reason values distinguish manual disabling, incomplete configuration, and a missing catalog record.
- When structured JSON is required, use `list_admin_requests(..., is_archived=false, active_only=true)`, `list_admin_orders(..., is_archived=false, active_only=true)`, or `list_admin_carts`. Set `active_only=false` only for the explicit complete non-archived cases below, and follow `pageInfo.nextCursor` until `pageInfo.hasMore` is false when complete coverage is requested.
- Markdown results are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.
- When an operator requests an order, pass `sort_by` and `sort_order=asc|desc` to the Admin request/order Markdown or structured list tool. For name sorting, use request `resourceTitle` or the returned order/request party field `requestedFor.fullName` (falling back to `requestedFor.name` when that is the returned name); date and status fields also work. Keep the chosen audience, archive/active filters, and sort parameters on each JSON continuation using `pageInfo.nextCursor`. Sorting does not authorize another audience or select a mutation target.

## Administrative mutations

- Staff, Admin, and Developer may use `add_admin_cart_item`, `create_admin_request`, `create_admin_order`, `update_admin_request`, and `update_admin_order` for an explicitly selected target Membership ID. The target identifier is operation data, not an authentication credential; never substitute it for the authenticated Membership ID.
- Before adding a cart item or creating a request/order, retrieve the target member's current administrative cart and the selected catalog detail. Confirm requestability, required format/type options, reason, and the exact **Full Name (Membership ID)** beneficiary. After a successful individual `create_admin_request`, use the returned request or retrieve its detail and give an itemized confirmation containing the request ID, catalog item name and type, selected Book format or Tactile Diagram type when applicable, request reason, initial status, and beneficiary. Do not reduce this to a generic “request placed” message.
- `create_admin_order` submits the selected member's saved cart. Show the complete cart and obtain explicit confirmation immediately before placing the order. The server revalidates current catalog requestability at execution time; do not perform polling or continuous availability lookups.
- If order creation returns `requiresPartialOrderConfirmation=true`, present every returned `blockedItems` title and explain before asking the operator to proceed that each named item will be excluded from the order, will not create a request, and will be removed from the submitted cart only if partial checkout succeeds. Ask explicitly whether the operator wants to place the order for the remaining requestable items. For each blocked item, present the server-returned administrative cause or retrieve current catalog detail to distinguish a manually disabled Requestable setting from incomplete requesting configuration such as missing Book Formats or Tactile Diagram types; report a missing catalog record as missing and never invent a cause. Retry only after fresh explicit confirmation, with `confirmPartialOrder=true` and `confirmedSkippedItems` containing the exact returned resource type and ID set. If that set changes, stop and present the refreshed server result; never silently confirm newly blocked items.
- After any successful order, use the returned generated requests or retrieve their details and provide an itemized **Requested items** confirmation. For every included item, state its request ID, catalog item name and type, selected Book format or Tactile Diagram type when applicable, request reason, initial status, and **Full Name (Membership ID)** beneficiary. Also report every returned `skippedItems` title under **Not requested**, state the specific returned administrative reason, and explain that it was excluded from the order and removed from the cart when the submitted cart was cleared. Ask the operator to verify the itemized result and provide both returned Member and Admin links when available. If no requestable items remain, do not retry checkout.
- Before a lifecycle update, retrieve current request/order detail and history, summarize the current status and proposed fields, and use only values accepted by the live MCP schema. Do not skip lifecycle rules or invent timestamps, actors, or history entries.
- Only Admin and Developer may use `remove_admin_cart_item`, `clear_admin_cart`, `delete_admin_request`, `delete_admin_order`, `bulk_delete_admin_requests`, `bulk_delete_admin_orders`, or `bulk_delete_admin_cart_items`. Staff must never call these tools.
- Every removal, clear, individual deletion, and bulk deletion requires fresh explicit confirmation identifying the exact target or reviewed target set. Preserve server dependency checks and report skipped or ineligible records exactly as returned.
- For every mutation, report the returned result and retrieve the affected record afterward when possible. Do not claim success from an attempted call or from a pre-write preview.

## Archive state and lifecycle intent

- Default to the active view for the selected audience. Treat a bare **list the requests/orders**, **show requests/orders and their statuses**, or ordinary **requests/orders** question exactly like **current**, **active**, **unfinished**, **outstanding**, or **action-needed**. Call the matching Markdown list with `is_archived=false, active_only=true` and no lifecycle `status` filter.
- The server, not local model filtering, applies the resource lifecycle. A Book is active until it reaches Issued or Rejected. A physical Teaching Learning Aid or Tactile Diagram remains active in In Review, Ready, Issued, or Overdue and ends only at Returned or Rejected. An order remains active in Received, In Progress, Partially Fulfilled, or Partially Fulfilled Overdue and ends at Completed.
- Only use the complete `isArchived=false` view when the user explicitly asks for **all**, **every**, **not archived**, or **non-archived** requests/orders. Call the matching Markdown list with `is_archived=false, active_only=false`; this includes ongoing work and completed-but-not-yet-archived Books with `status=issued`, physical requests with `status=returned`, rejected requests, and orders with `status=Completed`.
- Add a server `status` filter only when the user explicitly names that exact lifecycle status. When the named status is terminal, pass `active_only=false` so the requested status is not suppressed. Never infer archive state from `completedDate`.
- Archive membership remains independent of lifecycle completion. Use Admin Archives only for an explicit archived-record request; do not treat a completed-but-not-yet-archived record as archived history.

## Current transaction schema

- Treat `requestedFor` and `openedBy` as complete stored party maps. Preserve returned fields such as `role`, `userId`, `firebaseUUID`, `email`, `membershipId`, `name`, `phone`, `disabilityType`, and `accountRole`, plus any additional stored fields relevant to the operational question.
- Administrative request and order party maps include canonical `fullName` values read directly from `membership_info/{membershipId}`. Present the requested-for person as `requestedFor.fullName (requestedFor.membershipId)` and, when opener context matters, `openedBy.fullName (openedBy.membershipId)`. Never make a separate profile or Membership ID directory call to obtain these names.
- Preserve `requestedFor.name` and `openedBy.name` as stored transaction snapshots when relevant, but prefer the returned canonical `fullName` for the person's current display label. The API does not define a separate `displayName` field; do not invent one or claim that `fullName` and `displayName` are two independently returned values.
- Use `createdOnBehalfOfSomeoneElse` as the authoritative delegation indicator. Describe a transaction as opened on behalf of someone else only when it is `true`; do not recalculate it from names, roles, or partial identifiers.
- Keep `requestDate` and `orderDate` as the transaction creation date/time. Preserve a timestamp nested in `openedBy` only when returned; never invent `openedAt`.
- For requests, retain relevant lifecycle, fulfillment, collection, physical-resource, history, notes, reason, taxonomy, and parent-order fields. For orders, retain `orderHistory`, `orderReason`, `requestIds`, `resourceIds`, `resourceTypes`, `requestCount`, `itemCount`, and linked request context when returned.
- Treat `collectionLocation` as the human-readable portal value. Ready history entries return the St. Xavier's Main Center or Viviana Mall label, or the saved custom-location text.
- Retrieve linked request detail before explaining how a request affected its parent order. Do not infer an order transition or attribution from list position alone.
- Administrative responses include `memberRequestUrl` plus `adminRequestUrl`, `memberOrderUrl` plus `adminOrderUrl`, or `memberCartUrl` plus `adminCartUrl`. Always label both: the member link requires the target member's active session, while the Admin Console link requires existing Staff/Admin/Developer application authorization.

## Cart-owner name resolution

- Admin cart summaries, cart detail, and every administrative cart item return the cart owner's canonical `fullName` together with `membershipId`, resolved by the API directly from `membership_info/{membershipId}`.
- Present every cart owner as `fullName (membershipId)`. When several owners' cart items are shown together, include that returned owner label with every cart summary/item group so no item is associated only with an unlabeled Membership ID.
- Do not call `get_admin_membership_id`, `list_admin_membership_ids`, or a profile tool to rediscover the cart owner's name. Do not treat `updatedByName` as the cart owner's name; it identifies the updater and may be a different person.
- If `fullName` is empty or absent in a legacy or unsynchronized response, say that the owner's name is unavailable. Never infer it from email, updater fields, item audit data, request/order records, or another Membership ID.

## Date conversion and display

- Treat returned request, order, cart, fulfillment, collection, history, or audit timestamps that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Workflow

1. Confirm the effective role and resolve the required information view before fetching transaction data.
2. Choose requests, orders, carts, or the smallest combination that answers the operational question.
3. Apply `is_archived=false, active_only=true` to every bare/current/active request/order list. Pass `active_only=false` only for explicit all/every/non-archived intent or an explicitly named terminal status, and use the archive skill only after an explicit archived-record request.
4. Retrieve detail for any transaction whose lifecycle, requester, order linkage, or status history is being explained.
5. For a mutation, review the exact beneficiary, record, current state, and required inputs before invoking one role-authorized tool; verify the resulting state when possible.
6. Keep reporting questions in the Admin Reports skill; use the explicit admin cart endpoints for saved-cart investigations.

## Response rules

- In every administrative response, whenever a Membership ID appears, present that exact record's corresponding returned full name as `Full Name (Membership ID)`. Never list a Membership ID alone when its matching name is returned, and never pair it with a name from another person or event. If no matching name is returned, write `Full name unavailable (Membership ID)` instead of guessing or making an unrelated directory lookup.
- For a bare/current/active list, return only the server-filtered open requests/orders. For an explicit all/every/non-archived list, separate ongoing records from completed-but-not-yet-archived records when useful. Preserve identifiers/statuses/dates and complete party context, and pair every administrative transaction Membership ID with the matching returned canonical `fullName` as specified above.
- Present both returned link fields with clear labels; never imply that a member-app link bypasses the target member's session or that an Admin Console link bypasses application authorization.
- Do not present an operational list as a report or infer causes or performance trends that need report data.
- A server access denial is authoritative; explain the boundary and do not try alternate routes to bypass it.
- A successful request or order response must name the actual requested catalog items and their returned request details. Never use the pre-submit cart alone as proof of what the server created.
