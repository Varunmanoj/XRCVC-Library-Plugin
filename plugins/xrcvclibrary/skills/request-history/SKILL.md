---
name: request-history
description: Explain the complete lifecycle of one XRCVC Library request. Use for creation, status changes, updater details, remarks, collection information, and request-history questions; do not use for order-wide timelines or aggregate reporting.
---

# Explain Request History

Use the explicit authenticated history tools. The server decides identity, ownership, and role; never ask the user to paste a Membership ID, bearer value, OAuth code, or token.

## Information-view choice

- Never ask the user to state their role or Membership ID. When `/auth/me` identifies the user as Staff, Admin, or Developer, a request history could use either audience, and the user has not selected one, ask whether they want their own Member request history or a role-authorized Admin request history.
- Use the response only to choose the Member or Admin history route. For an authorized Member, use only the Member route without asking and never offer or query Admin request history. Server authorization remains decisive, and Staff/Admin/Developer users can still use their own Member request history.

## Select the correct history endpoint

- Use `get_member_request_history` for the signed-in person's request. It is self-scoped for every verified role, returns 404 for another member's request, recursively removes Firebase UID fields, and provides only `memberRequestUrl`.
- Use `get_admin_request_history` only when `/auth/me` confirms Staff, Admin, or Developer and the question requires internal access. It returns complete stored party and audit data plus both `memberRequestUrl` and `adminRequestUrl`.
- For a complete Markdown rendering, use `get_api_output_as_markdown` with `/requests/member/{requestId}/history` or `/requests/admin/{requestId}/history` after choosing the same audience boundary.

## Explain returned evidence

- Treat `history` as the authoritative lifecycle. Preserve each returned status, date, `adminName`, `adminMembershipId`, remarks, and status-specific fields. Do not invent a previous status, updater, Membership ID, reason, or event that is absent.
- For every human history event with both fields, render the updater as `adminName (adminMembershipId)`, for example, **Updated by Varun Manoj Kumar (NX 463)**. Use the Membership ID attached to that exact event; never substitute `requestedFor.membershipId`, `openedBy.membershipId`, or the signed-in person's Membership ID.
- When a human event has `adminName` but no `adminMembershipId`, show the returned name without guessing an ID. System-generated events may intentionally omit `adminMembershipId`; present their returned system actor label without adding a Membership ID.
- Use `openedBy`, `requestedFor`, and `createdOnBehalfOfSomeoneElse` exactly as returned. Say the request was opened on behalf of someone else only when that Boolean is `true`.
- `collectionLocation` is already human-readable. For ready events, report the returned St. Xavier's Main Center, Viviana Mall, or saved custom-location text together with `collectionDate` when present; do not translate it back to Firestore keys.
- Preserve `requestId`, resource title/type, current status, request/updated dates, and relevant fulfillment or return fields.

## Date conversion and display

- Treat request, update, collection, fulfillment, return, and history values that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- In a chronological history with multiple events on the same local day, show a `D MMMM YYYY` day heading once, then show only `h:mm AM/PM` for each event under it.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Link and privacy rules

- In member answers, present only the returned member link.
- In administrative answers, label both links: the member link requires the target member's active session; the Admin Console link requires existing Staff/Admin/Developer application authorization.
- `adminMembershipId` is the intended human-readable updater identifier and may be shown in Member or Admin answers. Never reconstruct or expose `userId`, `firebaseUUID`, `adminUID`, or other Firebase identity fields from member output.
