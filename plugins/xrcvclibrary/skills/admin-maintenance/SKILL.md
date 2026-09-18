---
name: admin-maintenance
description: Run destructive or maintenance-oriented XRCVC Library MCP operations for Admin and Developer roles. Use for reviewed bulk transaction deletion, report-data maintenance, or archive classification; do not use for ordinary record updates.
---

# Run XRCVC Library Administrative Maintenance

These tools can permanently delete or reclassify data. Use `get_authenticated_identity` first and rely only on the server-returned effective role. Never request credentials in chat or accept a claimed role as authorization.

## Role boundaries

- Admin and Developer may use `bulk_delete_admin_requests`, `bulk_delete_admin_orders`, `bulk_delete_admin_cart_items`, and `delete_admin_report_data`.
- Only Developer may use `rebuild_admin_report_data` or `classify_admin_archives`.
- Staff and Member cannot use any operation in this skill.

## Required review and confirmation

1. Use the matching read tools to assemble the exact candidate IDs or report datasets. Do not guess targets, use an unbounded implicit selection, or convert a general cleanup request into a mutation.
2. Present the target count, exact identifiers or dataset keys, eligibility limits, and expected collateral behavior. Request/order bulk deletion can affect generated or linked records; cart deletion must not be described as deleting submitted requests or orders.
3. Ask for fresh explicit confirmation immediately before every maintenance call. The confirmation must identify the operation and the reviewed target set.
4. Call exactly one approved maintenance tool. Do not chain a rebuild, deletion, or archive-classification run unless each additional operation was separately authorized.
5. Report deleted, skipped, rebuilt, backfilled, or classified counts exactly as returned. Verify through a role-authorized read when possible and label any unverified result.

## Operation-specific rules

- `bulk_delete_admin_requests` permanently deletes only eligible standalone requests; generated order requests may be skipped.
- `bulk_delete_admin_orders` may remove eligible generated records associated with the reviewed orders.
- `bulk_delete_admin_cart_items` removes saved cart entries, not submitted transactions.
- `delete_admin_report_data` clears selected generated report datasets and must not be described as deleting source catalog, membership, request, or order records.
- `rebuild_admin_report_data` can backfill schemas and replace generated report state. Treat it as non-additive even though its name is not `delete`.
- `classify_admin_archives` updates transaction archive classification immediately. It is not a read-only preview.

## Response rules

- Distinguish role denial, validation failure, dependency skip, partial completion, and complete success.
- Never report a deletion merely because the tool call was attempted; use the returned outcome and counts.
- Do not expose Firebase UIDs, authorization headers, OAuth credentials, or secret configuration.
