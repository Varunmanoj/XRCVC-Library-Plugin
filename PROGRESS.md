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
