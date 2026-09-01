# XRCVC Library Plugin Agent Rules

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

