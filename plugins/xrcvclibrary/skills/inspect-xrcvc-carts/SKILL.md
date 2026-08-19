---
name: inspect-xrcvc-carts
description: Inspect and explain XRCVC Library carts with server-enforced Member, Staff, Admin, and Developer access. Use for cart contents, comparisons, or cart-wide summaries; do not use for broader request/order reporting.
---

# Inspect XRCVC Carts

Cart tools require an authenticated XRCVC Library MCP connection. Credentials remain with the MCP host; never ask the user to paste a Membership ID, bearer value, access token, or refresh token into chat.

## Workflow

1. Call `get_authenticated_identity` first and use its effective role and capabilities. Never infer privilege from the user's wording.
2. For a Member, use `get_own_cart`. Do not attempt `list_carts` or `get_member_cart`.
3. For Staff, Admin, or Developer, use `list_carts` for cross-member questions and `get_member_cart` only when a specific Membership ID is supplied through the tool input or returned data.
4. Follow `pageInfo.nextCursor` only as far as needed. Explain whether the summary covers one page or the complete result.
5. Group items by resource type and include the server-provided resource ID, title, and direct URL when available. Flag duplicate references, missing titles, or resources that no longer resolve instead of inventing metadata.

## Authentication recovery

- On an OAuth challenge, tell the user to complete the host-provided XRCVC authorization flow and retry. Do not construct authorization URLs or handle tokens yourself.
- If a freshly authenticated connection fails in each new chat, advise the user to verify that the installed plugin is attached to the same registered XRCVC MCP connection and to refresh the app/connector.
- For legacy clients, explain that `/mcp` accepts a locally configured `Authorization: Bearer <Membership ID>` header. The value must stay in the client's secret or environment configuration, never in the plugin repository or conversation.

## Response rules

- Respect the role returned by the server: Members see only their cart; Staff, Admin, and Developer roles may inspect all carts.
- An access-denied result is authoritative. Explain the boundary without trying alternative tools to bypass it.
- Do not imply that cart contents constitute submitted requests or orders.
