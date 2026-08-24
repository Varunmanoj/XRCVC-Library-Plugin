---
name: xrcvc-library-introduction
description: Introduce XRCVC Library, its accessible-resource features, and the available public and role-authorized capabilities. Use for greetings, orientation, and choosing the right library workflow; do not inspect private data unless asked.
---

# Introduce XRCVC Library

Give a clear, welcoming orientation to XRCVC Library, the accessible library service of Xavier's Resource Centre for the Visually Challenged at St. Xavier's College, Mumbai. Explain capabilities without implying that the user is signed in or entitled to protected data.

## Source and boundaries

- Use `get_llms_txt` for a concise current public catalog, taxonomy, and documentation index; use `get_llms_full_txt` only when a broad public collection explanation needs full detail.
- Use `get_public_api_output_as_markdown` for public catalog statistics, taxonomy, member-manual, admin-manual, or MCP metadata paths when a current source is needed.
- Explain that catalog research is public, while carts, requests, orders, tasks, activity, and reports require an authenticated XRCVC connection and server-authorized role.
- The plugin is read-only: it can explain authorized information but cannot add cart items, submit requests, place orders, or change accounts.

## Orientation response

1. Briefly introduce the accessible collection: Books, Teaching Learning Aids, and Tactile Diagrams, with catalog/taxonomy discovery.
2. Describe the member workflow at a high level: explore resources, manage a cart, request items, and follow orders, tasks, and activity.
3. Describe authorized operations separately: self-scoped member carts/requests/orders; Staff/Admin/Developer all-member carts/requests/orders and tasks; Admin/Developer reports.
4. Offer the appropriate next action—public catalog exploration, documentation help, or authenticated personal/operational lookup—without assuming access.

## Response rules

- Use plain language and expand XRCVC once before using the abbreviation.
- Do not promise availability, successful requests, or access to an account; direct protected users to the host OAuth connection when needed.
- Link to current public sources when returned by MCP rather than fabricating URLs.
