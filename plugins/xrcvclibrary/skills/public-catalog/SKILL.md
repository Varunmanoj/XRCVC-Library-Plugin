---
name: public-catalog
description: Explore and explain publicly visible XRCVC Library catalog items, statistics, accessible formats, and taxonomies. Use for open catalog research; do not use for private carts, transactions, or account activity.
---

# Explore the Public XRCVC Catalog

Use the XRCVC Library MCP server as the source of truth. This skill is public: do not ask the user to authenticate unless their question moves into a protected workflow.

## MCP output format

- Prefer `list_member_catalog_as_markdown` for complete member-safe catalog data. It is unpaginated.
- Use `get_public_api_output_as_markdown` for `/catalog/statistics`, public member catalog details, taxonomy paths, and MCP metadata. Never use the OAuth-only Markdown tool for those public routes.
- The catalog has no server-side free-text search. Narrow only by `resource_type` and known `taxonomy_type` plus `taxonomy_id`; inspect the returned Markdown locally for title, author, subject, format, or topic matches.
- Use `get_llms_full_txt` only for a broad public catalog-and-taxonomy audit, not as proof of private availability.

## Workflow

1. Establish the material type, subject, format, or taxonomy criteria that meaningfully narrow the question.
2. Fetch catalog statistics or taxonomy data first when the question is about collection composition or valid filters. Use taxonomy IDs, not display labels, in catalog filters.
3. Retrieve member-safe catalog Markdown by default. Use the Admin catalog only when the authenticated user specifically needs role-authorized operational fields.
4. Confirm a specific resource through its public detail path before making a detailed claim, and retain its direct URL when supplied.

## Response rules

- Distinguish Books, Teaching Learning Aids, and Tactile Diagrams.
- Explain why each item matches, including material format and known subject/topic or diagram-type limits.
- Treat absent fields as unknown. Catalog inclusion does not guarantee availability or requestability; report the returned status instead.
- Never expose Admin-only operational fields unless the user explicitly requested and is authorized for that analysis.
