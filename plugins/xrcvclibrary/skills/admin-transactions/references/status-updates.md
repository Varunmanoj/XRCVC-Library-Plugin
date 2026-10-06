# Request and order status updates

Read this reference before offering status choices or calling `update_admin_request` or `update_admin_order`. It applies to every host using these skills, including ChatGPT, Codex, Claude, Gemini, and other compatible AI clients. Server authorization and the current tool schema remain decisive. A broad schema that accepts every request status is not permission to offer statuses inappropriate for the selected item.

## Resolve the record and intent

- Check `/auth/me`: only verified Staff, Admin, or Developer can update request/order status. Members may read their own records but cannot change their statuses. Do not ask people to self-declare a role.
- Ask only for missing information. An exact request/order number supplied by the user establishes the target; do not ask an unrelated all-members versus own-record question before retrieving that role-authorized detail. Otherwise resolve the existing audience choice and show the matching records. Ask: **“Which request or order would you like to update?”** Identify each candidate by its number, item title/type, current status, and returned beneficiary Full Name (Membership ID). Never select by title alone when several records match.
- For an explicit **all requests/orders** list, use `is_archived=false, active_only=false`; ordinary/current lists retain `active_only=true`. Use archived routes only for explicit archive intent. A list request never authorizes a status change.
- Read the selected record and history before presenting a proposed update. For orders, read all linked requests and their history. Determine request type from returned `resourceType` and `isPhysical`, with catalog detail if needed; do not assume that a Book becomes physical because its format is Braille. If the fields are missing or inconsistent, resolve the type before offering choices.
- If the user asks to update an order, distinguish an order summary change from fulfillment of one or more items. Ask when unclear: **“Would you like to update the whole order's status, or the status of specific items in it?”** Item fulfillment uses each selected request and its own choices below. Never apply one request status to an order or silently change every linked request.

## Request status choices

Display familiar labels; pass only the exact corresponding value to the tool.

| Selected request | Manual choices (label → tool value) | Automatic status |
| --- | --- | --- |
| Book / non-physical request | In Review → `in_review`; Issued (To Member) → `issued`; Rejected → `rejected` | None |
| Physical Teaching Learning Aid or Tactile Diagram (`isPhysical=true`) | In Review → `in_review`; Ready (Pending Collection) → `ready`; Issued (To Member) → `issued`; Returned → `returned`; Rejected → `rejected` | Overdue → `overdue`, set automatically after the expected return date |

The complete request status vocabulary for reading/filtering is In Review, Ready, Issued, Overdue, Returned, and Rejected. **Overdue is not a manual selection**, even if the tool's schema accepts `overdue`. Do not offer Ready, Returned, or Overdue for a Book/non-physical request. If asked to set an invalid or automatic status, explain the relevant choices and wait for the user to choose a valid action; do not substitute another status.

If the user has not chosen a status, ask **“Which status would you like to use?”** and show only the applicable manual choices. If they already named a valid status, retain it and ask only for missing fields. Do not invent forward-only transition rules: the portal permits correction to the listed manual states. Keeping the current manual status is supported for a comment or fulfillment-detail correction.

## Required details for the chosen request status

| Choice | Ask for missing details before writing | Tool fields |
| --- | --- | --- |
| Ready, physical request | Collection date and time; St. Xavier's Main Center, Viviana Mall, or another collection location; if another, its name/address | `collectionDate`, `collectionLocation` = `center`, `viviana`, or `other`; `otherLocation` for `other` |
| Issued, physical request | Expected return date | `expectedReturnDate` |
| Returned, physical request | Actual return date | `actualReturnDate` |
| Rejected, any request | Reason for rejection | `rejectionReason` |
| In Review, or Issued for a Book/non-physical request | No additional fulfillment field required | `status` |

Use the live schema's date format, resolve ambiguous dates/timezones with the user, and never invent a date or place. Reuse a valid existing field when the operator intends to retain it, and show it in the review. An optional comment does not replace a required rejection reason.

## Order status choices

Use these exact case-sensitive values for a direct `update_admin_order` call:

| Status | Meaning from the linked requests |
| --- | --- |
| Received | No linked request has progressed beyond In Review |
| In Progress | At least one request has progressed, with none finished and none overdue |
| Partially Fulfilled | At least one request has finished, some remain unfinished, and none are overdue |
| Partially Fulfilled Overdue | At least one linked physical request is overdue |
| Completed | All expected linked requests are present and finished |

A Book request finishes at Issued or Rejected. A physical Teaching Learning Aid or Tactile Diagram finishes at Returned or Rejected; Issued alone does not finish it. The same five order status names apply to Book-only, physical-only, and mixed orders, but their eligibility depends on the linked items. Do not offer Partially Fulfilled Overdue for a Book-only order, or Completed while a physical item is still issued/outstanding. A rejected item can count as finished; Completed does not necessarily mean every item was issued.

The application normally recalculates the parent order from its linked requests. Present the full five-status vocabulary when explaining statuses, and only choices consistent with the retrieved item states when proposing a direct change. If the requested order status contradicts the linked requests, explain the mismatch and ask which item updates/corrections the operator intends. Do not silently change linked requests to force the requested summary. Explain that later linked-request updates can recalculate a manually changed order status. If expected linked requests are missing, do not guess a completion state.

## Offer a comment before every update

After resolving the target/status, ask **“Would you like to add a comment to this update? You can enter a comment or continue without one.”** Bundle this with missing required fields when useful. Wait for an answer before writing. If the user already supplied a comment or explicitly said to proceed without one, do not ask again. A request such as “mark it issued” alone does not answer the comment question.

- Send the user's comment as `remarks` (up to 2,000 characters) for either tool. Preserve its meaning; ask for a shorter comment if it exceeds the limit. Do not fabricate text or replace prior history.
- If the user declines, omit `remarks`; the server may record its standard history message. Do not claim that no history note will be saved.
- For rejection, collect `rejectionReason` separately, or use the supplied explanation for both fields only if that is what the user intends. Explain that saved comments may appear in request/order history; do not promise private/internal-only visibility.
- For an explicit multi-record update, review every target and its applicable status/fields. Ask whether one comment applies to all or they want separate comments. Never infer bulk permission from an all-records list or silently apply Book choices to physical requests.

## Review, save, and verify

Summarize the exact number(s), beneficiary, item type(s), current → proposed status, required dates/location/rejection reason, and the supplied comment or “continue without a comment” **before** calling the tool. If the user's instructions and answers already authorize that exact update, proceed; ask for confirmation only when the action or target set remains unclear. A status explanation or preview is not permission to write.

Re-read if the record changed while collecting answers; resolve any conflict before writing. Call the correct update tool with only reviewed inputs, await its response, then retrieve the saved record and relevant history. For request updates, retrieve the parent order when applicable and report its actual returned status. Order synchronization may be asynchronous: state when confirmation is still pending instead of inventing the final parent status. Report the saved status/comment and returned links only after verification. On failure or an uncertain response, inspect the saved state before retrying; never claim success or duplicate an update blindly.
