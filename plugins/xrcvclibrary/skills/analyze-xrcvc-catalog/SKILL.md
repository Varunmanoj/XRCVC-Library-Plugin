---
name: analyze-xrcvc-catalog
description: Explore, compare, and explain the complete XRCVC Library catalog, formats, taxonomy, statistics, and requestability from MCP Markdown output. Use for catalog discovery or collection analysis; do not use for carts or private account activity.
---

# Analyze XRCVC Catalog

Use the XRCVC Library MCP server as the source of truth. Catalog and taxonomy tools are public, so do not ask the user to authenticate unless they move into a protected workflow.

## MCP output format

- Prefer the server's Markdown tools, not the paginated JSON list tools.
- Use `list_member_catalog_as_markdown` for the complete member-safe catalog and `list_admin_catalog_as_markdown` only when role-authorized operational fields are required.
- Markdown catalog output is complete and unpaginated. Do not send or describe `limit`, `cursor`, `page`, `pageInfo`, or page coverage.
- The catalog endpoint has no free-text search parameter. Narrow the server response only with `resource_type` and, when known, the paired `taxonomy_type` and `taxonomy_id`; then inspect the returned Markdown locally for titles, authors, subjects, formats, descriptions, or other requested terms.
- For another public catalog or taxonomy operation, use `get_api_output_as_markdown` with its API path, such as `/catalog/statistics` or a taxonomy collection/detail path.

## Workflow

1. Clarify only missing criteria that materially affect the exploration, such as title, subject, resource type, format, or diagram type.
2. For collection-level questions, request `/catalog/statistics` or the relevant taxonomy data as Markdown. Use taxonomy IDs—not display labels—when applying `taxonomy_type` and `taxonomy_id` filters.
3. Fetch the member-safe catalog Markdown by default. Request admin catalog Markdown only when the authenticated role permits it and the user needs fields such as quantity, purchase, cost, or storage details.
4. Analyze the complete Markdown result locally. Do not claim that the server performed a keyword search when the match was found by inspecting the returned document.
5. Use a Markdown detail path before making claims about a specific resource. Preserve direct catalog URLs when the server provides them.
6. Reserve `get_llms_full_txt` for broad public descriptive audits when its catalog-and-taxonomy document is more suitable than the catalog Markdown tool.

## Response rules

- Distinguish Books, Teaching Learning Aids, and Tactile Diagrams.
- State why each recommended item matches the user's criteria and mention material format, subject, topic, or diagram-type limitations.
- Treat missing fields as unknown, not as negative facts.
- Do not imply that catalog presence guarantees immediate availability or requestability. Report the server's current status and requestability fields.
- Never expose admin-only operational fields unless the user requested that analysis.
