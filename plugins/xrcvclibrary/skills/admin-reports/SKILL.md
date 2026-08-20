---
name: admin-reports
description: Explain XRCVC Library reporting for Admin and Developer roles. Use for report catalogs, report summaries, tables, and date-bounded operational analysis; do not use for Staff reporting or raw transaction lookup.
---

# Explain Admin and Developer Reports

Reports are server-authorized for Admin and Developer roles only. Start with `/auth/me` through `get_api_output_as_markdown`; Staff and Member users must not be offered report paths.

## MCP output format

- Use `get_api_output_as_markdown` for `/reports`, `/reports/{reportId}`, `/reports/{reportId}/tables/{tableId}`, and `/reports/combined`.
- Request `/reports` first when the report ID is unknown; use its returned report/table IDs rather than guessing them.
- Use supported `start_date` and `end_date` query values when the requested reporting period differs from the server default. Dates cannot precede `2026-01-01`.
- Markdown report results are complete within their documented report/table bounds. Do not claim a JSON page or cursor is complete Markdown evidence.

## Workflow

1. Confirm the role and select the report catalog, one report, a named table, or the combined report based on the question.
2. State the requested/default time range before interpreting totals, trends, or comparisons.
3. Preserve report/table names, metric labels, units, and source links. Clearly distinguish observed values from an inference.
4. For a transaction-level follow-up, use the Admin Transactions skill rather than treating report aggregates as record detail.

## Response rules

- Do not retrieve or summarize reports for Staff or Member roles; report the server-enforced role boundary.
- Identify filters and dates behind every conclusion, and avoid causal claims that the report does not establish.
- Treat an unavailable report, not found report/table, and access denial as different outcomes.
