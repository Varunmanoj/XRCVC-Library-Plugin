# XRCVC Library Agent Plugin

`xrcvclibrary` is the open-source agent plugin from Xavier's Resource Center for Visually Challenged. It connects supported AI hosts to the read-only XRCVC Library MCP server and adds three focused skills for catalog analysis, cart inspection, and account/operational review.

![XRCVC Library logo](plugins/xrcvclibrary/assets/xrcvc-library-logo.png)

## What is included

- OpenAI/Codex plugin metadata and a repository-local marketplace.
- Agent Plugins 1.0 portable manifests.
- Claude plugin and marketplace metadata for Claude.ai, Claude Desktop, Cowork, and Claude Code.
- One OAuth 2.1 Streamable HTTP MCP connection.
- Three skills: `analyze-xrcvc-catalog`, `inspect-xrcvc-carts`, and `review-xrcvc-account`. The catalog skill uses the anonymous public Markdown tool for catalog detail and taxonomy paths; the account skill covers protected Member Tasks, Member Recent Activity, Admin Tasks, identity, cart, transaction, and report workflows.
- Explicit XRCVC icon and brand-color metadata for each OpenAI/Codex skill.

The plugin is read-only. It can search catalog data and retrieve data the signed-in XRCVC role is already allowed to see; it cannot add to carts, submit requests, place orders, or alter accounts.

## Authentication

The bundled connection uses OAuth 2.1 at:

```text
https://mcp.library.xrcvc.org/mcp/authorize
```

Public catalog and documentation tools work without authentication. Protected tools launch the host's OAuth flow. The server uses S256 PKCE, dynamic client registration, 15-minute access tokens, rotating 30-day refresh tokens, and the scopes `xrcvc.library offline_access`.

The configured URL also returns RFC 9728 protected-resource metadata on `GET`/`HEAD`, allowing desktop hosts that probe the exact MCP URL before the well-known discovery paths to initialize the plugin consistently. MCP requests continue to use `POST` at the same URL.

MCP initialization publishes the XRCVC Library website plus same-origin 192×192 and 512×512 compact launcher PNGs through `serverInfo.icons`. Compatible clients may display the established St. Xavier's crest and XRCVC eye artwork; the host application retains final control over whether and where it renders server-provided icons.

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

### Claude.ai cloud, Claude Desktop, and Cowork

Install the complete plugin when you want both the three XRCVC skills and the remote MCP connector:

1. In Claude, open **Customize → Plugins**.
2. Under **Personal plugins**, select **+ → Add marketplace → Add from a repository**.
3. Enter `https://github.com/Varunmanoj/XRCVC-Library-Plugin`.
4. Open the **XRCVC Library** marketplace and install `xrcvclibrary`.
5. Connect the bundled `xrcvc-library` service when Claude prompts for authorization. Enter the Membership ID only on the XRCVC authorization page.

Because the bundled MCP server is remote and publicly reachable, the connector is available through the same Claude account on Claude.ai, Claude Desktop, Cowork, and supported mobile surfaces. The plugin skills are available in Claude chat and Cowork.

If you want only the MCP tools without the packaged skills, use **Customize → Connectors → + → Add custom connector**, name it **XRCVC Library**, and enter `https://mcp.library.xrcvc.org/mcp/authorize`. Do not install this connector-only configuration alongside the complete plugin unless duplicate tools are acceptable.

Claude's plugin manifest does not currently define a supported local logo field. The XRCVC icon files remain bundled for other plugin hosts and submission use; Claude connector-directory branding is supplied separately through the connector favicon or directory submission.

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
      "category": "Education"
    }
  }
}
```

5. Add `"apps": "./.app.json"` to `.codex-plugin/plugin.json`, validate, and reinstall the plugin.

The repository intentionally does not ship a fabricated `.app.json`. The technical ID must come from the real XRCVC ChatGPT registration so new conversations resolve the same connection and credential store.

## Access model

| Role | Own data | All carts/requests/orders | Member Tasks | Admin Tasks | Reports |
|---|---:|---:|---:|---:|---:|
| Member | Yes | No | Yes | No | No |
| Staff | Yes | Yes | Yes | Yes | No |
| Admin | Yes | Yes | Yes | Yes | Yes |
| Developer | Yes | Yes | Yes | Yes | Yes |

The MCP server derives the effective role from current XRCVC account data. OAuth scopes never elevate a role. Member Tasks and Member Recent Activity are self-scoped to the bearer Membership ID for every authenticated role. Admin Tasks remain an additional all-operator view for Staff, Admin, and Developer.

## MCP Markdown output

The packaged skills prefer the MCP server's Markdown output rather than its paginated JSON list tools. Named Markdown companions return complete, unpaginated Catalog, Requests, Orders, Member Recent Activity, Member Tasks, and Admin Tasks data. Public catalog detail, taxonomy, manual, and MCP metadata Markdown are requested through `get_public_api_output_as_markdown`; protected cart, identity, transaction detail, and report Markdown use `get_api_output_as_markdown`. Catalog Markdown has no free-text search input, so the catalog skill uses resource-type or taxonomy filters when available and inspects the returned Markdown locally.

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
