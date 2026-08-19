# OpenAI Marketplace Submission

Use this checklist after the canonical MCP deployment and public policy routes are live.

## Registration

- Publisher: **XRCVC Library**
- Product website: `https://library.xrcvc.org`
- MCP server: `https://mcp.library.xrcvc.org/mcp/authorize`
- Privacy policy: `https://console.library.xrcvc.org/privacy-policy`
- Terms of service: `https://console.library.xrcvc.org/terms-of-service`
- Support: `https://console.library.xrcvc.org/plugin-support`
- Compact icon: `plugins/xrcvclibrary/assets/xrcvc-library-icon.png`
- Marketplace logo: `plugins/xrcvclibrary/assets/xrcvc-library-logo.png`

Register the MCP server in ChatGPT Developer Mode, complete OAuth, copy the real `plugin_asdk_app…` identifier into `plugins/xrcvclibrary/.app.json`, reference it from `.codex-plugin/plugin.json`, and rerun `python3 scripts/validate_package.py`. Never submit a fabricated identifier.

The distributable package carries these links in the locations supported by each format: OpenAI Terms in `interface.termsOfServiceURL`, OpenAI/Claude support documentation in `homepage`, and all four public listing links in the portable `org.xrcvc.library` extension. The OpenAI portal's separate **Support URL** field must use the Support value above.

## Claude.ai cloud and Anthropic submission

- Marketplace repository: `https://github.com/Varunmanoj/XRCVC-Library-Plugin`
- Marketplace file: `.claude-plugin/marketplace.json`
- Plugin: `xrcvclibrary@xrcvc-library`
- Remote MCP connector: `https://mcp.library.xrcvc.org/mcp/authorize`
- Category: **Education**
- Connector icon source: the XRCVC favicon published by `mcp.library.xrcvc.org`

For private testing, add the GitHub repository from **Claude → Customize → Plugins → Personal plugins → Add marketplace**, then install **XRCVC Library**. This route installs the three skills and the remote connector together. A connector-only test can instead be added through **Customize → Connectors → Add custom connector**, but it will not include the skills.

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
