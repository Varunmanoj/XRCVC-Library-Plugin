# XRCVC Library Plugin Agent Rules

## User-facing Language and Cloud Function Deployment

- Use plain, user-facing language across the entire XRCVC Library ecosystem: Member and Admin websites, desktop apps, Member and Admin plugins on every supported host, emails, notifications, dialogs, errors, help text, and user-visible API/MCP responses. Explain what a feature does, what happened, and what the user can do next using familiar words. Avoid technical jargon, internal identifiers, implementation details, and raw service errors in user-facing communication; describe technology-related functionality in terms users can understand. Keep implementation terminology in developer documentation and diagnostic logs.
- Whenever `AGENTS.md` is updated, preserve this language rule and review the changed instructions for consistent coverage across Member, Admin, desktop, and plugin platforms. Include plain-language communication in UI and email audits.
- Whenever Firebase Cloud Functions are added or changed, automatically deploy the affected functions to the configured Firebase project after development is complete and all required tests and checks pass. This rule provides standing authorization for that deployment without a separate confirmation. Include functions affected by changes to shared backend code, confirm the target project and deployment scope, and verify the live deployment before reporting completion. If testing or deployment fails, or access is unavailable, report the exact blocker and remaining work; do not claim deployment succeeded. Function deletion must still follow the repository's explicit deletion safeguards.

## Cross-host version synchronization

- Treat `plugins/xrcvclibrary/plugin.json` as the canonical release version for the XRCVC Library plugin.
- Whenever the release version changes, update the same base version in all of these files in the same change:
  - `plugins/xrcvclibrary/plugin.json`
  - `plugins/xrcvclibrary/.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`, both the marketplace-level `version` and the XRCVC Library plugin entry `version`
  - `plugins/xrcvclibrary/.codex-plugin/plugin.json`, before its Codex cachebuster suffix
- The ChatGPT/Codex manifest must use `<base-version>+codex.<14-digit-UTC-timestamp>`. The `+codex...` portion is a host cachebuster, not a separate release version, and must be refreshed with the plugin-creator cachebuster helper instead of changing the base version independently.
- Never bump or publish the ChatGPT/Codex and Claude distributions separately. A release is ready only when every manifest has the same base version and `scripts/validate_package.py` passes.
- Keep `scripts/validate_package.py` version checks derived from the canonical portable manifest; do not hard-code a release number into separate host assertions.

## Release archives

- Store ChatGPT personal plugin upload ZIPs in `release-archives/chatgpt/` and keep them tracked in the repository.
- Keep release ZIPs outside `plugins/xrcvclibrary/` and outside both marketplace source paths so archives are never treated as plugin contents by the desktop app.
