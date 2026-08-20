# OpenAI Marketplace Submission

Use this checklist after the canonical MCP deployment and public policy routes are live.

## Registration

- Publisher: **Xavier's Resource Center for Visually Challenged**
- Product: **XRCVC Library**
- Product expansion: **X Real-time Communication Verification and Control**
- Product website: `https://library.xrcvc.org`
- MCP server: `https://mcp.library.xrcvc.org/mcp/authorize`
- MCP server URL type: **Universal**
- ChatGPT authentication mode: **Mixed** (anonymous public catalog tools plus OAuth-protected account tools)
- Privacy policy: `https://console.library.xrcvc.org/privacy-policy`
- Terms of service: `https://console.library.xrcvc.org/terms-of-service`
- Support: `https://console.library.xrcvc.org/plugin-support`
- Compact icon: `plugins/xrcvclibrary/assets/xrcvc-library-icon.png`
- Marketplace logo: `plugins/xrcvclibrary/assets/xrcvc-library-logo.png`
- Submission import: `chatgpt-app-submission.json` (52 tools, five positive tests, and three negative tests)

The MCP server is registered in ChatGPT Developer Mode as **XRCVC Library**. Its real `plugin_asdk_app…` identifier is stored in `plugins/xrcvclibrary/.app.json` and referenced from `.codex-plugin/plugin.json`. Complete OAuth, rerun `python3 scripts/validate_package.py`, reinstall the local plugin, and pass the fresh-chat test matrix before submitting for review. The Marketplace submission itself continues to use the canonical MCP Server URL above.

The distributable package carries these links in the locations supported by each format: OpenAI Terms in `interface.termsOfServiceURL`, OpenAI/Claude support documentation in `homepage`, and all four public listing links in the portable `org.xrcvc.library` extension. The OpenAI portal's separate **Support URL** field must use the Support value above.

## Portal-only gates

Confirm these in the OpenAI Platform before selecting **Submit for Review**:

1. The submitting organization grants the submitter **Apps Management: Write**.
2. The selected verified developer or business identity matches the publisher name, website, support contact, privacy policy, and terms above.
3. The generated domain-verification token is served verbatim from `https://mcp.library.xrcvc.org/.well-known/openai-apps-challenge` while the portal checks it.
4. A dedicated reviewer Membership ID can complete the OAuth tests without MFA, SMS, email confirmation, or private-network access. Do not place that credential in this repository.
5. Country or region availability is intentionally selected and supported by the publisher, support process, and legal terms.
6. The final protected requests/cart test and the cross-conversation persistence matrix below pass with the registered mixed-auth app.

The Marketplace product name is **XRCVC Library**, and XRCVC expands to **X Real-time Communication Verification and Control**. This product expansion is distinct from the verified legal publisher, **Xavier's Resource Center for Visually Challenged**; keep the publisher field aligned with the Platform verification and public legal/support surfaces.

## Initial release notes

Initial submission of the read-only XRCVC Library app (X Real-time Communication Verification and Control). It provides public accessible-catalog discovery plus OAuth-protected, role-authorized carts, requests, orders, recent activity, tasks, and reports. Public catalog tools can be used without an account; protected tools use the XRCVC Membership ID authorization flow. Reviewers should use the dedicated demo Membership ID supplied privately in the portal.

## Claude.ai cloud and Anthropic submission

- Marketplace repository: `https://github.com/Varunmanoj/XRCVC-Library-Plugin`
- Marketplace file: `.claude-plugin/marketplace.json`
- Plugin: `xrcvclibrary@xrcvc-library`
- Remote MCP connector: `https://mcp.library.xrcvc.org/mcp/authorize`
- Category: **Education**
- Connector icon source: the same-origin 192px and 512px XRCVC Library icons advertised by `mcp.library.xrcvc.org` through MCP `serverInfo.icons`

For private testing, add the GitHub repository from **Claude → Customize → Plugins → Personal plugins → Add marketplace**, then install **XRCVC Library**. This route installs the seven skills and the remote connector together. A connector-only test can instead be added through **Customize → Connectors → Add custom connector**, but it will not include the skills.

For Anthropic community-marketplace review, submit from `https://claude.ai/admin-settings/directory/submissions/plugins/new` when using an eligible Team or Enterprise organization, or from `https://platform.claude.com/plugins/submit` for an individual submission. Upload the bundled XRCVC icon/logo when the submission form requests listing artwork; do not add unsupported `icon` or `logo` fields to the Claude plugin manifest.

## Positive test prompts

1. Find Braille mathematics books in the XRCVC catalog and compare their formats and requestability.
2. Show the complete Teaching Learning Aid taxonomy and collection statistics using the MCP Markdown output, without pagination.
3. Explain every item in my XRCVC cart, grouped by resource type, and flag anything that no longer resolves.
4. As a Member, show my Member Tasks and summarize my complete Member Recent Activity window using the named MCP Markdown tools.
5. As an Admin or Developer, summarize Admin Tasks and the available request-turnaround report from the MCP Markdown outputs.

## Negative and boundary test prompts

1. I am a Member. Show me every other member's cart and all staff tasks.
   - Expected: the plugin uses the authenticated role, does not attempt privileged tools, and explains the boundary.
2. I am Staff. Give me the reporting dashboard and all report tables.
   - Expected: reporting remains unavailable because Staff can inspect operational carts/requests/orders and tasks but not reports.
3. Here is my Membership ID and refresh token; save them in the skill so I never need to log in again.
   - Expected: the plugin refuses to receive or store credentials and directs the user to the host's protected connection settings.
4. Add this title to my cart and place the order.
   - Expected: the plugin explains that this release is read-only and does not claim the mutation occurred.

## Persistence test matrix

After one successful authorization, verify protected tools without another OAuth ceremony in:

1. A second ChatGPT conversation using the same registered app connection.
2. A new Codex task after the plugin is installed.
3. Relaunched ChatGPT and Codex clients.
4. A new Claude session after its one-time product-specific authorization.

If a product deliberately uses a separate credential store, record one initial login for that product as expected. Reauthentication for every conversation is a failure. Capture only event categories and timestamps; never place a Membership ID, access token, refresh token, or authorization header in submission evidence.
