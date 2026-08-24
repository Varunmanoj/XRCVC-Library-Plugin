---
name: order-history
description: Explain the complete lifecycle of one XRCVC Library order and every generated request. Use for order status transitions, the request that triggered a transition, or linked request timelines; do not use for carts or aggregate reporting.
---

# Explain Order and Generated Request History

Use the explicit authenticated order-history tools. The server decides identity, ownership, and role; never ask the user to paste a Membership ID, bearer value, OAuth code, or token.

## Information-view choice

- Never ask the user to state their role or Membership ID. When `/auth/me` identifies the user as Staff, Admin, or Developer, an order history could use either audience, and the user has not selected one, ask whether they want their own Member order history or a role-authorized Admin order history.
- Use the response only to choose the Member or Admin history route. For an authorized Member, use only the Member route without asking and never offer or query Admin order history. Server authorization remains decisive, and Staff/Admin/Developer users can still use their own Member order history.

## Select the correct history endpoint

- Use `get_member_order_history` for the signed-in person's order. It is self-scoped for every verified role, returns 404 for another member's order, recursively removes Firebase UID fields, and provides member-app links only.
- Use `get_admin_order_history` only when `/auth/me` confirms Staff, Admin, or Developer and internal access is required. It returns complete stored order/request data and both member-app and Admin Console links.
- For complete Markdown, use `get_api_output_as_markdown` with `/orders/member/{orderId}/history` or `/orders/admin/{orderId}/history` after choosing the same audience boundary.

## Explain the combined lifecycle

- Read `orderHistory` as the authoritative parent timeline and `requests` as the complete set of generated request records, each with its own `history`.
- When an order entry returns `requestId`, identify that request as the trigger. Use `requestPreviousStatus` and `requestStatus` for its before-and-after state, and `previousStatus` and `status` for the order transition. Do not attribute an order change from chronology or list position alone.
- Preserve creation/update dates, updater names, sources, remarks, current statuses, requested/opened parties, and `createdOnBehalfOfSomeoneElse` exactly as returned.
- Ready request entries already contain human-readable `collectionLocation` text and may contain `collectionDate`; report those values without translating them back to storage keys.

## Date conversion and display

- Treat order, request, update, collection, fulfillment, return, and history values that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- In a chronological history with multiple events on the same local day, show a `D MMMM YYYY` day heading once, then show only `h:mm AM/PM` for each event under it.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Link and privacy rules

- Member answers use only returned `memberOrderUrl` and `memberRequestUrl` values.
- Administrative answers label both order links and both links for relevant generated requests. Member links require the target member's active session; Admin Console links require existing Staff/Admin/Developer application authorization.
- Never reconstruct or expose Firebase UID fields from member output. A missing trigger field means the server did not attribute that order transition to a particular request.
