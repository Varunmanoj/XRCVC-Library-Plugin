---
name: admin-member-directory
description: Review XRCVC Library Membership ID records, or administer role-authorized users and memberships. Use for authenticated Membership ID lookups, internal user-directory questions, or explicit Admin/Developer create, update, import, and deletion workflows.
---

# XRCVC Library Member Directory and Administration

Use the protected XRCVC Library MCP tools and server-enforced authorization. Never ask the user to paste a Membership ID, bearer value, OAuth code, or token, and never accept a claimed role as authorization.

## Workflow

1. Call `get_authenticated_identity` before any directory tool. A Member may continue only with the read-only Membership ID tools. Continue to user-account tools or any mutation only when the effective role authorizes that operation.
2. Distinguish the two record families:
   - A **user account** is one login profile. It is available only to Staff, Admin, and Developer. For complete coverage, prefer `list_admin_profiles_as_markdown`; use its optional `role` filter when the question is limited to Member, Staff, Admin, or Developer accounts. Use paginated `list_admin_profiles` when structured paging is useful, and use `get_admin_profile` for a selected returned `userId`.
   - A **Membership ID record** is a reservation or shared membership profile that may have zero, one, or multiple linked login accounts. Its read-only directory is available to every authenticated role because Member signup and login lookup use it. For complete coverage, prefer `list_admin_membership_ids_as_markdown`; use its optional `role` filter for Member or Staff memberships and `link_status` for linked, unlinked, or multi-login records. Use paginated `list_admin_membership_ids` when structured paging is useful, and use `get_admin_membership_id` for a selected returned `membershipId`.
3. Apply only filters requested or clearly implied by the question. Compare complete Markdown results locally. Do not describe a named Markdown directory result as a partial page. For JSON lists, keep the same filters while following `pageInfo.nextCursor` until `hasMore` is false when complete coverage is requested.
4. Retrieve detail only for a selected record. Preserve the returned application profile link and clearly label whether it opens an individual user profile or Membership ID profile.

## Directory mutations

- Member and Staff Membership ID access is read-only. Members cannot use the user-account directory. Only Admin and Developer may call `create_admin_user`, `update_admin_user`, `delete_admin_user`, `create_admin_membership_id`, `update_admin_membership_id`, `delete_admin_membership_id`, `create_admin_membership_profile`, `update_admin_membership_profile`, `delete_admin_membership_profile`, or `bulk_import_admin_membership_ids`.
- Distinguish a login user from its Membership ID reservation and shared profile. Use the user tool only for a returned `userId`; use Membership ID tools only for the exact normalized Membership ID record.
- Before creating or updating, retrieve the related reservation/profile where possible, summarize the exact proposed fields and role, and validate inputs against the live tool schema. The server remains responsible for email, linkage, role, and account safeguards.
- Imports can create or update Membership ID reservations. Preview the target and validated rows, explain overwrite behavior, and obtain explicit confirmation before calling `bulk_import_admin_membership_ids`.
- User, Membership ID, and shared-profile deletion is permanent and subject to linkage, dependency, last-account, and self-protection safeguards. Retrieve the selected record, explain the applicable preconditions, and obtain fresh explicit confirmation immediately before deletion.
- After a mutation, retrieve the affected user or Membership ID record when possible. Report a server rejection, partial import, or dependency failure rather than retrying around it.

## Authorization and privacy

- Staff may read Member, Staff, and Admin user profiles but cannot list or retrieve Developer user profiles. Staff Membership ID detail also omits linked Developer account rows.
- Admin and Developer may read all authorized directory rows.
- Members may read all Membership ID reservations and shared lookup profiles, but their results omit sign-in methods, account-security state, linked-login rows, and Admin Console links. Never attempt to reconstruct or probe those omitted internal fields.
- A `403` is an enforced role boundary, not evidence that the record does not exist. Do not probe alternate routes or infer hidden Developer data.
- Report only returned UI-visible profile information: names, emails, phone data, disability type, roles and status, Membership ID linkage and verification state, linked-account summaries, visible sign-in/security state, activity counts, and application links.
- Never infer or request credentials, tokens, OAuth records, passkey records, raw Firestore fields, or hidden account-security data.
- Treat `requestCount` and `orderCount` as activity totals, not proof of current obligations or eligibility.
- Never use an email address or linked Firebase UID as API identity. Membership ID remains the single server credential and linked accounts only determine the effective highest verified role.

## Response style

Whenever an administrative directory result contains a Membership ID, present that exact account or Membership ID record's returned `fullName` as `Full Name (Membership ID)`. Never output the Membership ID alone when its matching full name is returned, and never substitute a linked account's different name. If no matching full name is returned, write `Full name unavailable (Membership ID)` instead of guessing.

State which directory was used, identify the role boundary when relevant, and separate user-account facts from Membership ID reservation/shared-profile facts. Use readable local timestamps when returned, preserve date-only values, and say when a field is absent or not synchronized instead of guessing.
