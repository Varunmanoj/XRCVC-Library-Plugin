# Contributing

Keep the plugin read-only, accessible, role-aware, and aligned with the deployed XRCVC Library MCP contract.

## Before opening a pull request

1. Run `python3 scripts/validate_package.py`.
2. Run the OpenAI plugin validator against `plugins/xrcvclibrary`.
3. Run the skill validator against each immediate child of `plugins/xrcvclibrary/skills`.
4. Run `claude plugin validate .` and `claude plugin validate ./plugins/xrcvclibrary` when Claude Code is available.
5. Confirm no Membership ID, OAuth token, authorization header, or secret is present in the diff.
6. When MCP tools or role behavior change, update all three host manifests, affected skill instructions, README, and tests together.

Do not add a `.app.json` until a real ChatGPT app connection has been registered. Never use a placeholder ID in a release.
