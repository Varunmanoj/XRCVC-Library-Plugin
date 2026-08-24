---
name: xrcvc-tasks-activity
description: Explore XRCVC Library tasks, upcoming work, and recent member activity using role-authorized task views. Use for next actions and activity summaries; do not use for carts, transaction detail, or reports.
---

# Explore XRCVC Tasks and Recent Activity

Use authenticated XRCVC Library MCP Markdown tools. The server determines the role and self-scope, so never ask for credentials or accept a claimed role as authorization.

## Information-view choice

- Never ask the user to state their role or Membership ID. Ask whether they want their own Member view (including their tasks and recent activity) or a role-authorized Admin task view only when `/auth/me` identifies them as Staff, Admin, or Developer and they have not selected an audience.
- Treat the response only as endpoint selection. For an authorized Member, use the Member view without asking and never offer or query an Admin view; confirm the Admin-view authorization through `/auth/me`.

## Task and activity views

- Start with `/auth/me` through `get_api_output_as_markdown` when the role or view is not already established.
- Use `list_member_tasks_as_markdown` for the bearer member's own Tasks view and `get_member_recent_activity_as_markdown` for the bearer member's own Recent Activity. Both are self-scoped and available to authenticated Member, Staff, Admin, and Developer roles.
- Use `list_admin_tasks_as_markdown` for all-operator tasks only when the effective role is Staff, Admin, or Developer.
- There is no separate Admin Recent Activity endpoint. Do not invent one or relabel member-self-scoped activity as an organization-wide activity feed.
- Named Markdown outputs are complete and unpaginated. Do not use or describe `limit`, `cursor`, pages, or partial coverage.

## Date conversion and display

- Treat returned task, activity, due, request-status, or completion values that include a time or UTC offset as UTC database instants. Convert them to the user's known local timezone; if that timezone is unavailable or conversion fails, use Indian Standard Time (`Asia/Kolkata`, UTC+05:30).
- Render every converted timestamp as `D MMMM YYYY, h:mm AM/PM` in a 12-hour clock, including the timezone when useful for clarity (for example, `25 August 2026, 9:30 PM IST`). Do not use condensed numeric dates such as `25082026`, and do not return ISO/UTC timestamps unless the user asks for the source value.
- In a chronological activity list with multiple events on the same local day, show a `D MMMM YYYY` day heading once, then show only `h:mm AM/PM` for each event under it.
- Do not convert a date-only value without a time or offset; format it as `D MMMM YYYY` without inventing a time.

## Workflow

1. For “my tasks,” “upcoming tasks,” or “my activity,” retrieve the appropriate self-scoped Member view.
2. Filter task queries by supported task type or request status only when the user gives a concrete criterion; otherwise preserve the server’s ordering and time window.
3. For operational task queues, retrieve the Admin Tasks view only after confirming an authorized effective role.
4. Use the Member or Admin Transactions skill for details of a referenced request/order rather than reconstructing it from a task or activity row.

## Response rules

- Separate actions due now, upcoming work, completed/recent activity, and informational history.
- Preserve task type, status, IDs, dates, and direct links exactly as returned; state the applicable time window.
- State clearly whether the view is the bearer’s own Member data or the role-authorized Admin task dataset.
