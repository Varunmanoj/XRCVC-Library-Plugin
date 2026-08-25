# XRCVC Library Agent Plugin

`xrcvclibrary` is the open-source **XRCVC Library** agent plugin. XRCVC is Xavier's Resource Centre for the Visually Challenged, an integral department of St. Xavier's College, Mumbai. The plugin connects supported AI hosts to the read-only XRCVC Library MCP server and adds ten focused skills for public catalog research, member transactions, Admin transactions, the Admin member directory, request history, order history, Admin/Developer reports, tasks/activity, library orientation, and documentation guidance.

![XRCVC Library logo](plugins/xrcvclibrary/assets/xrcvc-library-logo.png)

## What is included

- OpenAI/Codex plugin metadata and a repository-local marketplace.
- Agent Plugins 1.0 portable manifests.
- Claude plugin and marketplace metadata for Claude.ai, Claude Desktop, Cowork, and Claude Code.
- One OAuth 2.1 Streamable HTTP MCP connection.
- Ten focused skills: `public-catalog`, `member-transactions`, `admin-transactions`, `admin-member-directory`, `request-history`, `order-history`, `admin-reports`, `xrcvc-tasks-activity`, `xrcvc-library-introduction`, and `xrcvc-library-documentation`. Together they keep public catalog and documentation guidance separate from role-authorized member, directory, operational, and lifecycle workflows.
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

Install the complete plugin when you want both the ten XRCVC skills and the remote MCP connector:

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
2. Use the registered **XRCVC Library** development app for `https://mcp.library.xrcvc.org/mcp/authorize`. Its ChatGPT authentication mode is **Mixed** so public catalog tools work anonymously while account tools request OAuth.
3. Choose **Use without an account** for public catalog testing, then complete OAuth once when a protected cart, request, order, task, activity, or report tool requests more access.
4. Validate and reinstall the plugin after any package change.

The package includes `.app.json` with the real registered XRCVC ChatGPT MCP connection identifier (`plugin_asdk_app_…`) copied from the connection URL after it was created in ChatGPT developer mode. New conversations therefore resolve the same registered connection and ChatGPT-managed credential store; no Membership ID or OAuth token is stored in this repository.

## Access model

| Role | Own data | All carts/requests/orders | Member Tasks | Admin Tasks | Reports |
|---|---:|---:|---:|---:|---:|
| Member | Yes | No | Yes | No | No |
| Staff | Yes | Yes | Yes | Yes | No |
| Admin | Yes | Yes | Yes | Yes | Yes |
| Developer | Yes | Yes | Yes | Yes | Yes |

The MCP server derives the effective role from current XRCVC account data. OAuth scopes never elevate a role. Member Tasks and Member Recent Activity are self-scoped to the bearer Membership ID for every authenticated role. Admin Tasks remain an additional all-operator view for Staff, Admin, and Developer.

## MCP Markdown output

The packaged skills prefer the MCP server's Markdown output rather than its paginated JSON list tools. Named Markdown companions return complete, unpaginated Catalog, Requests, Orders, Member Recent Activity, Member Tasks, Admin Tasks, user-account directory, and Membership ID directory data. The user-account directory can filter by account role; the Membership ID directory can filter by member/staff role and linked, unlinked, or multi-login state. Complete Member and Owner's Manual tools return the packaged Markdown unchanged. Explicit request-history and order-history tools return one lifecycle as structured JSON; `get_api_output_as_markdown` can render the matching history path. Both formats include `adminName` and `adminMembershipId` for every resolvable human update, and the history skills present them as **Name (Membership ID)** while preserving member UID redaction. Public catalog detail, taxonomy, manual, and MCP metadata Markdown are requested through `get_public_api_output_as_markdown`; protected profile, directory, cart, identity, transaction detail, history, and report Markdown use `get_api_output_as_markdown`. Catalog Markdown has no free-text search input, so the catalog skill uses resource-type or taxonomy filters when available and inspects the returned Markdown locally.

## Validation

```bash
python3 scripts/validate_package.py
for skill in plugins/xrcvclibrary/skills/*; do python3 /path/to/skill-creator/scripts/quick_validate.py "$skill"; done
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
