# Security Policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability involving authentication, authorization, private member data, or credentials. Email `info@xrcvc.org` with a concise description, affected component, reproduction steps, and impact.

## Credential handling

- Never commit Membership IDs used as bearer credentials, OAuth codes, access tokens, refresh tokens, client secrets, or authorization headers.
- Use the OAuth endpoint for normal plugin operation.
- Keep legacy bearer values only in a user's local secret or environment configuration.
- The skills must not ask users to paste credentials into a conversation.

## Supported release

Security fixes are applied to the latest published release.
