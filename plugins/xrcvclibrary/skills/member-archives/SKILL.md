---
name: member-archives
description: Review the signed-in person's archived XRCVC Library requests and orders. Use for personal archive questions that must select stored isArchived=true records; do not use for current transactions or another member's records.
---

# Review My Archived Requests and Orders

Use the dedicated authenticated XRCVC Library archive tools. The server derives the Membership ID from the connection and enforces self-scope; never ask for a Membership ID, bearer value, OAuth code, or token in chat.

## Archive selection contract

- Use `list_member_archived_requests_as_markdown` and `list_member_archived_orders_as_markdown` for complete archive lists. Use `list_member_archived_requests` or `list_member_archived_orders` when structured paginated JSON is useful.
- These tools select only documents whose stored `isArchived` boolean is `true`. Never pass or search for `status=archived`, because requests and orders retain their real lifecycle status independently from archive state.
- A real request/order status filter may additionally narrow the already archived records. Archived request tools also accept a real resource-type filter.
- Member archive output is bearer-self-scoped, recursively Firebase-UID-redacted, and contains only member-app transaction links.

## Fields to preserve

- Preserve `isArchived`, `archivedAt`, `archiveEligibleDate`, and `archivedBy` when returned. Do not invent a missing audit field or infer who archived a record from another actor field.
- Preserve the real `status`, request/order ID, title or linked request IDs, completion information, and `memberRequestUrl` or `memberOrderUrl` independently from archive metadata.
- Treat `requestedFor`, `openedBy`, and `createdOnBehalfOfSomeoneElse` using the same member-safe transaction contract. Do not reconstruct `userId`, `firebaseUUID`, `adminUID`, or another Firebase identity field.
- For the detailed lifecycle of one archived request/order, hand off to Request History or Order History and use its self-scoped history tool; archive listing does not replace lifecycle evidence.

## Date display

- Convert returned timestamps with a time or UTC offset to the user's known local timezone. If it is unavailable, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render timestamps as `D MMMM YYYY, h:mm AM/PM`; render date-only values as `D MMMM YYYY` without inventing a time.

## Response rules

- Distinguish an empty archive from authentication failure, access denial, and tool unavailability.
- Never describe archive as a request/order status transition. State that the record is archived because `isArchived` is true, then report its separate real status.
- Do not expose an Admin Console link, another Membership ID's records, or Firebase UIDs from member archive output.
