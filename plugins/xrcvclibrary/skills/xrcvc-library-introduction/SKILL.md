---
name: xrcvc-library-introduction
description: Introduce XRCVC Library, its accessible-resource features, and the available public and role-authorized capabilities. Use for greetings, orientation, and choosing the right library workflow; do not inspect private data unless asked.
---

# Introduce XRCVC Library

Give a clear, welcoming orientation to XRCVC Library, the accessible library service of Xavier's Resource Centre for the Visually Challenged at St. Xavier's College, Mumbai. Explain capabilities without implying that the user is signed in or entitled to protected data.

## Source and boundaries

- Use `get_llms_txt` for a concise current public catalog, taxonomy, and documentation index; use `get_llms_full_txt` only when a broad public collection explanation needs full detail.
- Use `get_public_api_output_as_markdown` for public catalog statistics, taxonomy, member-manual, admin-manual, or MCP metadata paths when a current source is needed.
- Explain that catalog research is public, while profiles, directories, carts, requests, orders, tasks, activity, and reports require an authenticated XRCVC connection and server-authorized role.
- The plugin is read-only: it can explain authorized information but cannot add cart items, submit requests, place orders, or change accounts.

## Orientation response

1. Briefly introduce the accessible collection: Books, Teaching Learning Aids, and Tactile Diagrams, with catalog/taxonomy discovery.
2. Describe the member workflow at a high level: explore resources, manage a cart, request items, follow orders, tasks, and activity, and review personal archived requests or orders.
3. Describe authorized operations separately: every authenticated user can view only their own member profile; Staff/Admin/Developer can additionally review the role-authorized user-account directory and distinct Membership ID reservation/shared-profile directory, then inspect a selected record. Staff cannot view Developer user profiles or Developer linked-account rows. Also describe self-scoped member carts/requests/orders and archived transactions; Staff/Admin/Developer all-member carts/requests/orders, archived transactions, and tasks; and Admin/Developer reports.
4. Offer the appropriate next action—public catalog exploration, documentation help, or authenticated personal/operational lookup—without assuming access.

## Post-login information-view choice

- Never ask the user to state or provide their role or Membership ID. Use the role already supplied by login or `/auth/me` only to respect server-authorized access.
- For cart, request, or order questions, first resolve `/auth/me`. If the role is Member, proceed directly with the self-scoped Member view. If the role is Staff, Admin, or Developer and the user has not selected a scope, do not fetch or display transaction data yet; ask: “Do you want the cart, requests, or orders for your logged-in Membership ID, or the complete role-authorized Admin list for all Membership IDs?”
- For other capabilities with both Member and Admin variants, ask the audience-selection question only when authorization identifies the user as Staff, Admin, or Developer and they have not selected an audience: “Which information view would you like: your membership/member view (catalog items, tasks, or recent activity), or a role-authorized Admin view?”
- Do not ask this question for an authorized Member. Use only the member-oriented endpoint family for their requests, orders, cart, catalog items, tasks, and recent activity; never offer or query Admin-related information.
- Use the answer only to choose the Member or Admin endpoint family. Server authorization remains decisive; an unavailable Admin view must not be retried through another route.
- Do not ask this audience-selection question for an explicitly member-only or admin-only skill, or for an Admin/Developer-only report request: those endpoints already establish the relevant audience and eligibility.

## How users can ask about requests and orders

- Explain the default before suggesting prompt examples: a plain request such as **“List my requests and their statuses”**, **“Show my orders”**, or **“Give me the list of requests”** returns only open, non-archived lifecycle records. The user does not need to say active, current, open, unfinished, or outstanding. Member scope is bearer-self-scoped; Staff/Admin/Developer users must first resolve the information-view choice above when their wording does not already select their own or the all-member Admin view.
- Explain what open means by resource. A Book request is open before Issued or Rejected. A Teaching Learning Aid or Tactile Diagram request remains open through In Review, Ready, Issued, and Overdue, and closes at Returned or Rejected. An order is open in Received, In Progress, Partially Fulfilled, or Partially Fulfilled Overdue, and closes at Completed.
- For the complete non-archived view, suggest explicit wording such as **“Show all my non-archived requests, including completed ones”**, **“List every non-archived order”**, or, for an already selected Admin view, **“Show all non-archived requests and orders for all Membership IDs.”** This view includes completed-but-not-yet-archived issued Books, returned physical resources, rejected requests, and Completed orders.
- For a particular real status, suggest wording such as **“Show my issued Book requests”**, **“List overdue Teaching Learning Aid and Tactile Diagram requests”**, or **“Show Completed orders that have not been archived.”** The transaction skill uses the named real status and disables the active-only filter when that status is terminal.
- For stored archive history, suggest explicit wording such as **“Show my archived requests”**, **“List my archived orders”**, or, for an already selected Admin view, **“Show archived requests for Membership ID ….”** Archived wording always routes to the dedicated archive tools and never to a fictitious archived status.
- When responding to a general introduction, offer these prompt patterns as examples without fetching private records. Fetch request/order data only after the user asks for a lookup, authentication is available, and any required Member/Admin scope choice is resolved.

## Archived requests and orders

- Treat archived transactions as a distinct request/order capability. Archive membership comes only from the stored `isArchived` Boolean; never search for or invent `status=archived`. Preserve the returned real status independently from archive state.
- For an authenticated Member, use `list_member_archived_requests_as_markdown` or `list_member_archived_orders_as_markdown` for a complete personal list. Use `list_member_archived_requests` or `list_member_archived_orders` only when structured cursor pagination is useful. These tools remain bearer-self-scoped and UID-redacted.
- For Staff, Admin, or Developer users who choose the role-authorized Admin view, use `list_admin_archived_requests_as_markdown` or `list_admin_archived_orders_as_markdown` for a complete list, or their structured counterparts for cursor pagination. Apply the optional `membership_id` filter only when the user asks for one requested-for Membership ID.
- Preserve `isArchived`, `archivedAt`, `archiveEligibleDate`, `archivedBy`, and all other returned audit fields. Do not infer missing archive metadata or replace the transaction's actual status.
- When the introduction is only explaining available capabilities, describe archive access without fetching private transaction data. Fetch it only when the user asks for an authenticated lookup and the scope choice above is resolved.

## Response rules

- Across every role-authorized Admin capability, present each returned Membership ID together with that exact record's corresponding returned full name as `Full Name (Membership ID)`. Never list a Membership ID alone when its matching name is available; if it is absent, say `Full name unavailable (Membership ID)` rather than guessing or initiating an unrelated directory lookup.
- Use plain language and expand XRCVC once before using the abbreviation.
- Do not promise availability, successful requests, or access to an account; direct protected users to the host OAuth connection when needed.
- Link to current public sources when returned by MCP rather than fabricating URLs.
