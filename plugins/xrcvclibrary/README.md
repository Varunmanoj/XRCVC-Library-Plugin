# XRCVC Library Plugin

This distributable package provides **XRCVC Library**, the accessible library service of Xavier's Resource Centre for the Visually Challenged at St. Xavier's College, Mumbai. It connects supported AI clients to the XRCVC Library MCP server and includes nine focused skills: public catalog research; member requests, orders, and cart; Admin transactions; request history; order history; Admin/Developer reports; tasks and activity; a library introduction; and public documentation guidance.

The skills use the server's Markdown output for both public and authenticated workflows. The named Markdown tools return complete, unpaginated Catalog, Requests, Orders, Member Recent Activity, Member Tasks, and Admin Tasks data. Explicit member/admin request-history and order-history tools return one lifecycle, with order history including every generated request timeline; every resolvable human event supplies `adminName` and `adminMembershipId` so the skills can present **Name (Membership ID)** without exposing Firebase UIDs. Public member catalog detail, catalog statistics, taxonomy, manual, and MCP metadata paths use `get_public_api_output_as_markdown`; other authenticated Markdown operations use `get_api_output_as_markdown`. Member Tasks and Member Recent Activity are server-scoped to the bearer Membership ID for every authenticated role; Staff, Admin, and Developer may additionally use the separate `/tasks/admin` view. Reports remain limited to Admin and Developer roles.

## Public listing links

- Website: https://library.xrcvc.org
- Privacy Policy: https://console.library.xrcvc.org/privacy-policy
- Terms of Service: https://console.library.xrcvc.org/terms-of-service
- Plugin Support: https://console.library.xrcvc.org/plugin-support

The support page contains installation, OAuth and legacy authentication, reconnection, revocation, troubleshooting, accessibility, and contact guidance. The OAuth MCP URL returns RFC 9728 protected-resource metadata on `GET`/`HEAD` for desktop-host discovery and accepts MCP traffic on `POST`. Credentials must remain in the selected client's protected connection or secret settings and must never be pasted into a conversation or stored in a skill.
