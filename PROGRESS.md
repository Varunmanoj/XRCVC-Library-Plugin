# Plugin progress

- **[2026-10-06] (Request and order status questions, version 1.0.5)**:
  - Updated Admin Transactions, Member Transactions, Request History, Order History, and Introduction routing with a shared status-update reference for every skill-enabled host.
  - Distinguished Book and physical manual statuses from automatic Overdue, documented all five order statuses and item-dependent completion, and required missing collection/return/rejection details.
  - Offer an optional comment before updates, preserve supplied answers, review exact targets and inputs, and verify saved status/history and parent-order synchronization.
  - Synchronized portable, Claude marketplace/plugin and Codex base versions to 1.0.5; refreshed the Codex cachebuster with the repository helper.
  - Existing API/MCP inputs already support the guided updates; no backend, website, or Electron code changed, and no Firebase deployment is required.
  - Package validation and three release-helper tests passed. Archive byte-parity, reference-link and skill-validation results are recorded in the release report. Installed-host reload, remote publication and live mutation behavior are not established by these checks.

- **[2026-10-06] (Required creation questions, version 1.0.6)**:
  - Added shared intake guidance for Member/Admin cart additions/replacements, individual requests, and saved-cart checkout; routed catalog, introduction, and both history skills to it.
  - Ask for missing supported Book formats, Tactile Diagram types, request reasons, and shared order reasons; preserve valid answers and validate each cart item before checkout.
  - Explicitly distinguish cart-only saves from requests/orders, prompt before unintended replacement, and stop on unsupported options or unresolved catalog configuration.
  - Synchronized all host versions to 1.0.6 and refreshed the Codex cachebuster; retained the 1.0.5 status/comment changes.
  - No backend, website, or Electron changes are needed for this skill intake update; no Firebase deployment is required. Validation and archive checks are recorded in release-archives/plugin-release-1.0.6.json. Installed-host/remote publication verification remains separate.

- **[2026-10-06] (ChatGPT website upload identifier correction, version 1.0.6)**:
  - Diagnosed the supplied ChatGPT upload rejection: `.app.json` used the plugin page ID `plugin_asdk_app_…` instead of its registered app ID `asdk_app_…`.
  - Added `scripts/build_chatgpt_archive.py` to derive the accepted app identity and build a dedicated ChatGPT website archive without changing Codex/Claude source manifests or their release versions.
  - Removed the ChatGPT archive’s unused `mcpServers` reference to an absent `.mcp.json`; the upload uses the existing registered app connection.
  - Preserved previous ZIPs and produced `release-archives/chatgpt/xrcvc-chatgpt-personal-update-1.0.6-with-icon-fixed-app-id.zip` with all fifteen skills and existing icon assets.
  - Package validation and five release-helper tests passed; the builder verified ZIP integrity, identifier syntax, registered identity, icons and skill byte parity. Correction evidence is recorded in `release-archives/chatgpt-upload-fix-1.0.6.json`.
  - ChatGPT website upload/acceptance and installed skill reload remain unverified. No website, backend or Electron code changed.

- **[2026-10-06] (Preserve accepted ChatGPT plugin name and verify skill icons)**:
  - Recovered the successfully uploaded 1.0.2 archive from Git commit `3a3e98d` and proved its registered plugin name/app entry key is `dev-6a86fa76513081919da915ed9b23de9b`, separate from the portable/Codex name `xrcvclibrary`.
  - Stored that identity in `chatgpt-upload-identity.json`; the dedicated builder preserves it, the registered app ID, the canonical plain ChatGPT release version and the official developer name.
  - Built `release-archives/chatgpt/xrcvc-chatgpt-personal-update-1.0.6-with-icon-fixed-identity.zip`. The earlier app-ID-only correction failed ChatGPT’s existing-plugin name check and is superseded.
  - Confirmed all fifteen skill small icons are byte-identical to the plugin composer icon and all large icons match the plugin logo; validated each metadata path in the archive. Source skills and Codex/Claude distributions are unchanged.
  - Package validation and five release-helper tests passed. Uploaded through Safari on the existing ChatGPT plugin page; ChatGPT confirmed “New version uploaded”. The page showed 1.0.6, all fifteen skills, the XRCVC plugin icon and its existing connected account, and retained 1.0.6 after refresh.
  - ChatGPT still renders generic cube icons for skill rows despite valid bundled icon metadata/assets. The skill detail dialog exposes no icon-edit control; visual skill-icon restoration remains unresolved on the ChatGPT website. Official icon fields are documented at https://github.com/openai/skills/blob/main/skills/.system/skill-creator/references/openai_yaml.md. Live evidence is recorded in `release-archives/chatgpt-upload-fix-1.0.6.json`.
