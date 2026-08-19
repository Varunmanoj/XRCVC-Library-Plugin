# XRCVC Library Agent Plugin

`xrcvclibrary` is the open-source agent plugin for Xavier's Resource Centre for the Visually Challenged. It connects supported AI hosts to the read-only XRCVC Library MCP server and adds three focused skills for catalog analysis, cart inspection, and account/operational review.

![XRCVC Library logo](plugins/xrcvclibrary/assets/xrcvc-library-logo.png)

## What is included

- OpenAI/Codex plugin metadata and a repository-local marketplace.
- Agent Plugins 1.0 portable manifests.
- Claude Code plugin and marketplace metadata.
- One OAuth 2.1 Streamable HTTP MCP connection.
- Three skills: `analyze-xrcvc-catalog`, `inspect-xrcvc-carts`, and `review-xrcvc-account`.

The plugin is read-only. It can search catalog data and retrieve data the signed-in XRCVC role is already allowed to see; it cannot add to carts, submit requests, place orders, or alter accounts.

## Authentication

The bundled connection uses OAuth 2.1 at:

```text
https://mcp.library.xrcvc.org/mcp/authorize
```

Public catalog and documentation tools work without authentication. Protected tools launch the host's OAuth flow. The server uses S256 PKCE, dynamic client registration, 15-minute access tokens, rotating 30-day refresh tokens, and the scopes `xrcvc.library offline_access`.

The plugin never receives or stores access tokens, refresh tokens, or Membership IDs. Authentication state belongs to the host application. Installing the plugin does not itself sign a member in.

### Legacy bearer connection

Clients that cannot use OAuth may connect directly to `https://mcp.library.xrcvc.org/mcp` with an `Authorization: Bearer <Membership ID>` header. Keep that value in the client's local secret or environment configuration. Do not add it to this repository or paste it into an AI conversation.

For Claude Code, a separate personal configuration can use environment expansion:

```json
{
  "mcpServers": {
    "xrcvc-library-legacy": {
      "type": "http",
      "url": "https://mcp.library.xrcvc.org/mcp",
      "headers": {
        "Authorization": "Bearer ${XRCVC_MEMBERSHIP_BEARER}"
      }
    }
  }
}
```

Do not enable the OAuth and legacy definitions together under different names unless duplicate tool listings are acceptable.

## Local installation

### Codex

From the repository root:

```bash
codex plugin marketplace add "$PWD"
codex plugin add xrcvclibrary@xrcvc-library
```

Start a new task after installation so Codex loads the plugin and MCP tools.

### Claude Code

```bash
claude plugin marketplace add .
claude plugin install xrcvclibrary@xrcvc-library
```

Run `/reload-plugins`, then `/mcp` and complete the XRCVC OAuth flow when a protected tool is first used.

### ChatGPT registered connection

1. In ChatGPT, enable Developer Mode under **Settings → Apps & Connectors → Advanced settings**.
2. Create an app for `https://mcp.library.xrcvc.org/mcp/authorize` and complete OAuth once.
3. Copy the registered technical ID (`plugin_asdk_app_…`).
4. Create `plugins/xrcvclibrary/.app.json`:

```json
{
  "apps": {
    "xrcvc-library": {
      "id": "plugin_asdk_app_REPLACE_WITH_REGISTERED_ID",
      "category": "Productivity"
    }
  }
}
```

5. Add `"apps": "./.app.json"` to `.codex-plugin/plugin.json`, validate, and reinstall the plugin.

The repository intentionally does not ship a fabricated `.app.json`. The technical ID must come from the real XRCVC ChatGPT registration so new conversations resolve the same connection and credential store.

## Access model

| Role | Own data | All carts/requests/orders | Tasks | Reports |
|---|---:|---:|---:|---:|
| Member | Yes | No | No | No |
| Staff | Yes | Yes | Yes | No |
| Admin | Yes | Yes | Yes | Yes |
| Developer | Yes | Yes | Yes | Yes |

The MCP server derives the effective role from current XRCVC account data. OAuth scopes never elevate a role.

## Validation

```bash
python3 scripts/validate_package.py
python3 /path/to/skill-creator/scripts/quick_validate.py plugins/xrcvclibrary/skills/analyze-xrcvc-catalog
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/xrcvclibrary
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete release checks.
The marketplace registration checklist and positive/negative review prompts are in [SUBMISSION.md](SUBMISSION.md).

## Policies and support

- [Privacy Policy](https://console.library.xrcvc.org/privacy-policy)
- [Terms of Service](https://console.library.xrcvc.org/terms-of-service)
- [Plugin Support](https://console.library.xrcvc.org/plugin-support)
- Email: [info@xrcvc.org](mailto:info@xrcvc.org) or [books@xrcvc.org](mailto:books@xrcvc.org)

The OpenAI manifest exposes the Terms URL through `interface.termsOfServiceURL` and uses the Plugin Support page as its documentation `homepage`; OpenAI's submission form receives the same Support URL from [SUBMISSION.md](SUBMISSION.md). The Claude manifest and marketplace entry use Plugin Support as their documented `homepage`. The portable Agent Plugins manifest records the website, privacy, terms, and support URLs under the permitted `org.xrcvc.library` extension namespace.

## License

MIT. See [LICENSE](LICENSE).
