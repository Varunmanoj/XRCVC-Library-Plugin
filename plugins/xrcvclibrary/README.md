# XRCVC Library Plugin

This distributable package provides **XRCVC Library**, the accessible library service of Xavier's Resource Centre for the Visually Challenged at St. Xavier's College, Mumbai. It connects supported AI clients to FastMCP 0.2.1 and includes fifteen focused skills for public research, member and Admin transactions, archives and histories, catalog/taxonomy management, user and Membership ID administration, settings, maintenance, reports, tasks/activity, orientation, and documentation.

The package covers all 121 current FastMCP tools, including 42 mutations. Membership ID remains the single protected identity, OAuth resolves to that Membership ID, and multiple active verified linked accounts use the highest role. Every authenticated role may read the Membership ID reservation/shared-profile directory; Member output omits internal account fields. Members may mutate only their own cart and create requests or orders for themselves, and cannot mutate Membership ID records. Staff, Admin, and Developer may create/update operational records and act on behalf of members; Staff cannot delete. Admin and Developer may administer users, Membership IDs, destructive operations, and report defaults; Developer-only settings and maintenance remain restricted. Skills review current state, exact targets, and required fields before writes and require explicit confirmation for destructive or high-impact operations. The relevant read skills cover ascending/descending sorting, including names, and the Admin report skill covers Catalog Taxonomy Breakdown.

The introduction skill describes the same ZeptoMail side effects for website, API, and MCP mutations: standalone request mail, combined order mail, actual lifecycle-transition mail, and documented account-workflow mail. It also identifies cart-only and Membership ID reservation/profile-only changes as intentionally email-silent, preserves the Developer Mode recipient override, and prevents a successful data write from being misreported as proof of asynchronous provider acceptance.

The Member and Admin transaction skills describe each saved cart item's stored `addedAt` date/time and added-actor attribution, unavailable legacy values, and API/MCP sorting. Member JSON and MCP cart detail always includes the stored `addedByName`, including self-added items; Admin detail includes the added actor name and Membership ID.

## Public listing links

- Website: https://library.xrcvc.org
- Privacy Policy: https://console.library.xrcvc.org/privacy-policy
- Terms of Service: https://console.library.xrcvc.org/terms-of-service
- Plugin Support: https://console.library.xrcvc.org/plugin-support

The support page contains installation, OAuth and legacy authentication, reconnection, revocation, troubleshooting, accessibility, and contact guidance. The OAuth MCP URL returns RFC 9728 protected-resource metadata on `GET`/`HEAD` for desktop-host discovery and accepts MCP traffic on `POST`. Credentials must remain in the selected client's protected connection or secret settings and must never be pasted into a conversation or stored in a skill.
