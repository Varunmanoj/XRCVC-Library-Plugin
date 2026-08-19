# XRCVC Library Plugin

This distributable package connects supported AI clients to the XRCVC Library MCP server and includes three role-aware skills for catalog research, cart inspection, and account/task/activity review.

The skills use the server's Markdown output for both public and authenticated workflows. The named Markdown tools return complete, unpaginated Catalog, Requests, Orders, Member Recent Activity, Member Tasks, and Admin Tasks data. Public member catalog detail, catalog statistics, taxonomy, manual, and MCP metadata paths use `get_public_api_output_as_markdown`; other authenticated Markdown operations use `get_api_output_as_markdown`. Member Tasks and Member Recent Activity are server-scoped to the bearer Membership ID for every authenticated role; Staff, Admin, and Developer may additionally use the separate `/tasks/admin` view.

## Public listing links

- Website: https://library.xrcvc.org
- Privacy Policy: https://console.library.xrcvc.org/privacy-policy
- Terms of Service: https://console.library.xrcvc.org/terms-of-service
- Plugin Support: https://console.library.xrcvc.org/plugin-support

The support page contains installation, OAuth and legacy authentication, reconnection, revocation, troubleshooting, accessibility, and contact guidance. The OAuth MCP URL returns RFC 9728 protected-resource metadata on `GET`/`HEAD` for desktop-host discovery and accepts MCP traffic on `POST`. Credentials must remain in the selected client's protected connection or secret settings and must never be pasted into a conversation or stored in a skill.
