---
name: xrcvc-library-documentation
description: Retrieve and explain the public XRCVC Library Member and Owner's Manual Markdown documentation, including catalog use and the request-to-order lifecycle. Use for how-to, policy, and lifecycle questions; do not use it as evidence of a user's private records.
---

# Explain XRCVC Library Documentation

Use the public documentation Markdown supplied by the API and MCP server. Explain the documented workflow faithfully, and separate instructions from a user's current account state.

## Documentation sources

- Use `list_member_manual_headings` or `list_admin_manual_headings` to locate the most relevant public documentation section.
- Retrieve only the selected section with `get_member_manual_section` or `get_admin_manual_section`. Use the returned stable section ID, not a guessed heading.
- For a complete document specifically requested by the user, use the anonymous `get_member_manual` or `get_admin_manual` structured-text tool. It returns the packaged Markdown unchanged. For a smaller overview, use `/membermanual/sections` or `/adminmanual/sections` through `get_public_api_output_as_markdown`.
- `get_llms_txt` is a public documentation and catalog link index; it is not a replacement for the manuals’ request/order lifecycle guidance.

## Workflow

1. Choose the Member Manual for member-facing catalog, cart, request, order, account, and accessibility instructions; choose the Owner's Manual for authorized staff/admin/developer operations.
2. List headings, select the narrowest relevant section, and retrieve it before explaining the lifecycle or application behavior.
3. Explain the documented flow in order—catalog discovery, cart/request steps, request review, order fulfilment/return where applicable—and preserve stated conditions and role limits.
4. If the question asks what is currently in a user’s account or queue, move to the appropriate authenticated skill rather than inferring it from documentation.

## Response rules

- Cite or link the returned documentation section when available, distinguish documented behavior from live account data, and state the role/audience of the manual.
- Do not invent manual sections, policy rules, or status transitions. If the documentation does not answer the question, say so.
- Documentation is public; do not require authentication merely to explain it.
