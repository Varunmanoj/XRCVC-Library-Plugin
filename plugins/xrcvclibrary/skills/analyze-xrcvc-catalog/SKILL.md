---
name: analyze-xrcvc-catalog
description: Search, compare, and explain XRCVC Library catalog items, formats, taxonomy, statistics, and requestability. Use for catalog discovery or collection analysis; do not use for carts or private account activity.
---

# Analyze XRCVC Catalog

Use the XRCVC Library MCP server as the source of truth. Catalog and taxonomy tools are public, so do not ask the user to authenticate unless they move into a protected workflow.

## Workflow

1. Clarify only missing criteria that materially affect the search, such as title, subject, resource type, format, or diagram type.
2. For collection-level questions, start with `get_catalog_statistics` or the relevant taxonomy list. Use taxonomy IDs—not display labels—when applying `taxonomy_type` and `taxonomy_id` filters.
3. Use member catalog list/detail tools by default. Use admin catalog tools only when the user explicitly needs operational full-field data such as quantity, purchase, cost, or storage details.
4. Follow `pageInfo.nextCursor` while `pageInfo.hasMore` is true when the requested answer requires more than one page. Stop once the answer is sufficiently supported; do not fetch every page automatically.
5. Use `list_member_catalog_as_markdown` or `list_admin_catalog_as_markdown` when the user explicitly needs a complete unpaginated set. Reserve `get_llms_full_txt` for broad descriptive audits that cannot be answered efficiently with structured tools.
6. Fetch item details before making claims about a specific resource. Preserve direct catalog URLs when the server provides them.

## Response rules

- Distinguish Books, Teaching Learning Aids, and Tactile Diagrams.
- State why each recommended item matches the user's criteria and mention material format, subject, topic, or diagram-type limitations.
- Treat missing fields as unknown, not as negative facts.
- Do not imply that catalog presence guarantees immediate availability or requestability. Report the server's current status and requestability fields.
- Never expose admin-only operational fields unless the user requested that analysis.
