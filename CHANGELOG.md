# Changelog

All notable changes to this project will be documented here.

## 0.1.6 - 2026-08-24

- Split request, order, and cart tools into explicit member/self and Staff/Admin/Developer administrative contracts.
- Updated member transaction guidance for recursively UID-redacted responses and member-only links.
- Expanded administrative transaction guidance to saved carts and both labeled member-app and Admin Console links.
- Updated the ChatGPT submission inventory to the 58-tool MCP contract and refreshed portable, Claude, and Codex package versions.

## 0.1.5 - 2026-08-24

- Updated Member and Admin transaction skills for the expanded request/order MCP schema, including complete `requestedFor` and `openedBy` party maps, Disability Type, and `createdOnBehalfOfSomeoneElse`.
- Added order-specific guidance for history, reason, linked request/resource identifiers, counts, and parent-order attribution without inventing missing fields or timestamps.
- Kept carts distinct from submitted requests/orders and documented the structured JSON pagination contract alongside complete unpaginated Markdown.
- Refreshed the portable, Claude, and ChatGPT/Codex package versions so clients can detect and install the updated skills.

## 0.1.4 - 2026-08-19

- Published same-origin 192px and 512px XRCVC Library MCP implementation icons for compatible connected-app clients.
- Preserved the existing OAuth URL, tool names, three skills, role enforcement, and read-only behavior.
- Standardized developer, author, owner, and publisher metadata as `Xavier's Resource Centre for the Visually Challenged` across OpenAI/Codex, portable Agent Plugins, and Claude packages.

## 0.1.3 - 2026-08-19

- Added Claude.ai cloud installation guidance for the GitHub marketplace plugin and the connector-only fallback.
- Documented Anthropic community marketplace submission routes and the separate connector favicon/listing artwork behavior.
- Corrected Claude repository metadata and bumped the pinned Claude plugin version so cloud clients refresh the package.

## 0.1.2 - 2026-08-19

- Added the anonymous `get_public_api_output_as_markdown` workflow for public member-catalog detail, catalog statistics, taxonomy, manual, and MCP metadata paths.
- Kept `get_api_output_as_markdown` OAuth-only for identity, transaction, cart, task, administrative catalog, and report paths.
- Updated the catalog skill so an unauthenticated public lookup no longer selects a tool descriptor that forces sign-in.

## 0.1.1 - 2026-08-19

- Changed the plugin category from Productivity to Education across Codex, ChatGPT setup guidance, and Claude marketplace metadata.
- Added explicit XRCVC small and large icon metadata to all three OpenAI/Codex skills so the app does not choose inconsistent fallback glyphs.
- Updated all three skills to prefer complete MCP Markdown outputs over paginated JSON lists.
- Switched the account skill to the deployed `list_member_tasks_as_markdown`, `list_admin_tasks_as_markdown`, and `get_member_recent_activity_as_markdown` tools and their explicit forward-only API routes.
- Clarified that Member Tasks and Member Recent Activity are bearer-self-scoped views available to authenticated Developer, Admin, Staff, and Member roles; Admin Tasks remains the separate all-operator view.
- Connected the public Terms of Service and Plugin Support URLs to the OpenAI/Codex, portable Agent Plugins, and Claude package metadata supported by each format.
- Added validation that prevents the website, privacy, terms, and support listing URLs from drifting across connector packages.

## 0.1.0 - 2026-08-19

- Added OpenAI/Codex, Agent Plugins 1.0, and Claude plugin manifests.
- Added the XRCVC Library OAuth MCP connection.
- Added catalog, cart, and account/activity skills.
- Added XRCVC Library branding, marketplace metadata, validation, and installation documentation.
