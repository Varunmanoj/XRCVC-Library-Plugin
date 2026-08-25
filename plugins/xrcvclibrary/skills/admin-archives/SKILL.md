---
name: admin-archives
description: Review archived XRCVC Library requests and orders across members for Staff, Admin, or Developer operations. Use when archive selection must use stored isArchived=true and may be narrowed by requested-for Membership ID.
---

# Review Administrative Request and Order Archives

Use the dedicated authenticated XRCVC Library administrative archive tools and server-enforced roles. Never accept a claimed role as authorization or ask the user to paste a Membership ID credential, bearer value, OAuth code, or token.

## Authorization and scope

1. Call `get_authenticated_identity`. Continue with administrative archive tools only when the effective role is Staff, Admin, or Developer.
2. If the effective role is Member, hand off to Member Archives and use only bearer-self-scoped archive tools.
3. Use `list_admin_archived_requests_as_markdown` and `list_admin_archived_orders_as_markdown` for complete role-authorized archive lists. Use the matching structured JSON tools when cursor pagination is useful.
4. Apply `membership_id` only when the user requests one requested-for Membership ID. This is a server-side administrative filter, not a credential and not an authorization override.

## Archive selection contract

- Dedicated archive tools select only documents whose stored `isArchived` boolean is `true`. Never pass or search for `status=archived`; request/order status remains an independent lifecycle field.
- A real status may additionally narrow archived records. Archived request tools also accept a real resource-type filter.
- Preserve `isArchived`, `archivedAt`, `archiveEligibleDate`, `archivedBy`, and every other returned audit field. Do not infer missing archive metadata from history actors or the signed-in operator.
- For a specific lifecycle explanation, hand off to Request History or Order History. Use returned history entries rather than treating archive metadata as status history.

## Administrative identity and links

- Administrative requested-for and opened-by party maps include canonical `fullName` paired with `membershipId`. Present each as **Full Name (Membership ID)** and never make a separate profile or Membership ID directory lookup for a name already returned.
- When a canonical name is missing, write **Full name unavailable (Membership ID)**. Do not substitute a stored snapshot name, updater name, email, Firebase UID, or another person's name as the canonical current name.
- Preserve both returned member-app and Admin Console links and label their access boundaries: the member link requires the target member's active session; the Admin Console link requires existing Staff/Admin/Developer application authorization.

## Date display

- Convert timestamps with a time or UTC offset to the user's known local timezone; otherwise use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render timestamps as `D MMMM YYYY, h:mm AM/PM`; render date-only values as `D MMMM YYYY` without inventing a time.

## Response rules

- State that each record is archived because `isArchived` is true, then report its independent real status.
- Preserve identifiers, requested-for identity, archive audit fields, completion information, and relevant links. Distinguish no matches from access denial or unavailable data.
- Never infer that a record is archived from its age, terminal status, report grouping, or a word in free text.
