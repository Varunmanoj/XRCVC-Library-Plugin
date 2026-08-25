---
name: admin-member-directory
description: Review role-authorized XRCVC Library user accounts and Membership ID reservations or shared profiles. Use for Admin directory questions about members, staff, admins, developers, linked logins, profile fields, verification, sign-in state, activity counts, or a selected user or Membership ID.
---

# XRCVC Library Admin Member Directory

Use the protected XRCVC Library MCP tools and server-enforced authorization. Never ask the user to paste a Membership ID, bearer value, OAuth code, or token, and never accept a claimed role as authorization.

## Workflow

1. Call `get_authenticated_identity` before any directory tool. Continue only when the effective role is Staff, Admin, or Developer.
2. Distinguish the two record families:
   - A **user account** is one login profile. For complete coverage, prefer `list_admin_profiles_as_markdown`; use its optional `role` filter when the question is limited to Member, Staff, Admin, or Developer accounts. Use paginated `list_admin_profiles` when structured paging is useful, and use `get_admin_profile` for a selected returned `userId`.
   - A **Membership ID record** is a reservation or shared membership profile that may have zero, one, or multiple linked login accounts. For complete coverage, prefer `list_admin_membership_ids_as_markdown`; use its optional `role` filter for Member or Staff memberships and `link_status` for linked, unlinked, or multi-login records. Use paginated `list_admin_membership_ids` when structured paging is useful, and use `get_admin_membership_id` for a selected returned `membershipId`.
3. Apply only filters requested or clearly implied by the question. Compare complete Markdown results locally. Do not describe a named Markdown directory result as a partial page. For JSON lists, keep the same filters while following `pageInfo.nextCursor` until `hasMore` is false when complete coverage is requested.
4. Retrieve detail only for a selected record. Preserve the returned application profile link and clearly label whether it opens an individual user profile or Membership ID profile.

## Authorization and privacy

- Staff may read Member, Staff, and Admin user profiles but cannot list or retrieve Developer user profiles. Staff Membership ID detail also omits linked Developer account rows.
- Admin and Developer may read all authorized directory rows.
- A `403` is an enforced role boundary, not evidence that the record does not exist. Do not probe alternate routes or infer hidden Developer data.
- Report only returned UI-visible profile information: names, emails, phone data, disability type, roles and status, Membership ID linkage and verification state, linked-account summaries, visible sign-in/security state, activity counts, and application links.
- Never infer or request credentials, tokens, OAuth records, passkey records, raw Firestore fields, or hidden account-security data.
- Treat `requestCount` and `orderCount` as activity totals, not proof of current obligations or eligibility.

## Response style

Whenever an administrative directory result contains a Membership ID, present that exact account or Membership ID record's returned `fullName` as `Full Name (Membership ID)`. Never output the Membership ID alone when its matching full name is returned, and never substitute a linked account's different name. If no matching full name is returned, write `Full name unavailable (Membership ID)` instead of guessing.

State which directory was used, identify the role boundary when relevant, and separate user-account facts from Membership ID reservation/shared-profile facts. Use readable local timestamps when returned, preserve date-only values, and say when a field is absent or not synchronized instead of guessing.
