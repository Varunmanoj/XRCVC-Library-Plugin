---
name: xrcvc-tasks-activity
description: Explore XRCVC Library tasks, upcoming work, and recent member activity using role-authorized task views. Use for next actions and activity summaries; do not use for carts, transaction detail, or reports.
---

# Explore XRCVC Tasks and Recent Activity

Use authenticated XRCVC Library MCP Markdown tools. The server determines the role and self-scope, so never ask for credentials or accept a claimed role as authorization.

## Task and activity views

- Start with `/auth/me` through `get_api_output_as_markdown` when the role or view is not already established.
- Use `list_member_tasks_as_markdown` for the bearer member's own Tasks view and `get_member_recent_activity_as_markdown` for the bearer member's own Recent Activity. Both are self-scoped and available to authenticated Member, Staff, Admin, and Developer roles.
- Use `list_admin_tasks_as_markdown` for all-operator tasks only when the effective role is Staff, Admin, or Developer.
- There is no separate Admin Recent Activity endpoint. Do not invent one or relabel member-self-scoped activity as an organization-wide activity feed.
- Named Markdown outputs are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Workflow

1. For “my tasks,” “upcoming tasks,” or “my activity,” retrieve the appropriate self-scoped Member view.
2. Filter task queries by supported task type or request status only when the user gives a concrete criterion; otherwise preserve the server’s ordering and time window.
3. For operational task queues, retrieve the Admin Tasks view only after confirming an authorized effective role.
4. Use the Member or Admin Transactions skill for details of a referenced request/order rather than reconstructing it from a task or activity row.

## Response rules

- Separate actions due now, upcoming work, completed/recent activity, and informational history.
- Preserve task type, status, IDs, dates, and direct links exactly as returned; state the applicable time window.
- State clearly whether the view is the bearer’s own Member data or the role-authorized Admin task dataset.
