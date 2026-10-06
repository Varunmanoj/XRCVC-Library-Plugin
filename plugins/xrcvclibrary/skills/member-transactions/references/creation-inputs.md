# Collect information before cart, request, and order creation

Read this reference before `add_member_cart_item`, `add_admin_cart_item`, `create_member_request`, `create_admin_request`, `create_member_order`, or `create_admin_order`. These intake rules apply to all hosts loading the plugin skills. Use the current tool schema and selected catalog detail as the source of truth; do not use a failed mutation call to discover missing information.

## Establish the action and exact item

- Check the authenticated identity/role and follow the transaction skill's audience rules. Member tools act only for the signed-in person. An administrative on-behalf action needs a selected, authorized beneficiary, displayed using returned Full Name (Membership ID). Never ask the user for credentials or their own Membership ID; retrieve their identity. When another beneficiary is unclear, resolve them through authorized records and ask which person, rather than guessing.
- Distinguish **add to cart**, **create an individual request**, and **submit the saved cart as an order**. If intent is ambiguous, ask **“Would you like to add this item to your cart, request it now, or place an order for your saved cart?”** Do not turn a catalog question into a write or submit the whole cart for a single-item request.
- Resolve the exact returned `resourceId`, `resourceType`, and title. If several items match, show distinguishing title/author/type details and ask **“Which catalog item would you like?”** Do not guess an item from a partial title.
- Retrieve current catalog detail and, for cart additions/replacements or checkout, the current cart for the selected audience. Verify current requestability and the item's actual supported formats/types. Use its resolved `formats` or `diagramTypes` taxonomy entries; resolve linked taxonomy IDs if only IDs are returned. Show labels to the user, and map to the exact value expected by the live tool. Do not offer every format/type in the whole library when only a subset belongs to this item.

## Required questions by item and action

| Item/action | Information needed before saving | Question when missing |
| --- | --- | --- |
| Book added to cart or requested individually | Selected format(s) from this Book's available formats; send a nonempty `formats` array | “Which available book format would you like?” Show this item's choices. |
| Tactile Diagram added to cart or requested individually | One supported diagram type; send `diagramType` | “Which available tactile diagram type would you like?” Show this item's choices. |
| Teaching Learning Aid added to cart or requested individually | Exact catalog item; copy returned subject context where applicable | Ask which item only if ambiguous; do not invent a Book format or diagram-type question for an aid. |
| Any individual request | Nonblank reason, 1–2,000 characters; send `requestReason` | “What is the reason for this request?” |
| Any order from the saved cart | Nonblank order reason, 1–2,000 characters; send `orderReason`, after all cart item choices are valid | “What is the reason for this order?” |
| Cart addition or replacement only | Item-specific choices above; no submission reason is required | Do not require a request/order reason for a cart-only save. |

Ask only for unanswered information and bundle related questions when helpful: **“Which of these formats would you like, and what is the reason for your request?”** A user-supplied valid choice/reason must not be requested again. If only one format/type is available and no choice was supplied, state it and ask whether to use it; do not silently default it. A preference in a profile or an earlier request is not a choice for a new item unless the user explicitly applies it. If more than one format is requested, use only supported values and the live schema's cardinality; do not create extra requests without instruction.

For TLA/TD `subjects`, retain the selected catalog's returned subject titles/context when the schema permits. These are optional metadata in the current tools, not a mandatory free-text question. Do not fabricate subjects or ask the user to type taxonomy identifiers. If a future tool requires an additional field, ask for that missing field before writing. Do not collect collection dates, return dates, rejection reasons, manually chosen initial statuses, or update comments during creation; those belong to later status updates. The creation reason is separate from an optional comment on a later update.

If a supplied choice is unavailable, present the actual choices and wait for a replacement selection. If the reason is blank or longer than 2,000 characters, ask for a valid reason without inventing or silently truncating it. Do not infer a reason such as “personal use” merely from “request this.”

## Missing catalog configuration and requestability

When no supported format/type can be resolved, or the catalog item is not requestable, stop before saving or submitting. Do not send an empty selection, arbitrary default, `N/A`, guessed taxonomy ID, or unsupported type to get past validation. For Member output use the returned member-safe explanation and direct them to XRCVC admin staff when needed; do not expose internal causes. For administrative output explain the returned cause, such as unavailable requesting configuration, without silently changing catalog settings. Do not remove blocked items or alter the cart just to make checkout pass.

## Cart additions and replacements

- Cart saves add or replace one entry for the same resource type and ID. Read the current cart before a save; compare its stored format/type/subjects with the proposed selection.
- For a new item, collect all missing choices and show the exact item and selected options before saving. A supplied explicit add instruction authorizes that reviewed addition once required answers arrive.
- If the same item already exists with the same choices, explain that it is already in the cart; do not claim another copy was added or invoke a needless replacement.
- If the same item exists with different choices, show **current → proposed** options and explain that the saved selection will be replaced. Ask **“Would you like to replace the existing cart selection with these choices?”** unless the user already explicitly requested that exact replacement. Do not overwrite because a required parameter was omitted or choose a new default. Retain valid existing choices only when the user intends to keep them, and show them in the review.
- A cart replacement is not editing, cancelling, or recreating a submitted request. If “replace my request” refers to a saved request, clarify the intended change and use only a supported authorized workflow; never delete and recreate it automatically.
- Await the save and retrieve the cart afterward. Report the stored item/options and any returned cart count; do not report an add/replacement from the pre-save preview alone.

## Individual request creation

Collect the exact item, valid selected format/type, and request reason before any create call. Review the item title/type, selected options, reason, and on-behalf beneficiary if applicable. If these instructions and answers authorize the exact request, proceed without another redundant questionnaire. A “what would happen” question remains read-only.

Use the proper self/admin creation tool with the reviewed values. Let the server assign the number, initial status, actor, and beneficiary snapshots. Follow the transaction skill's waiting, uncertain-response, itemized saved-result, and link rules. Do not substitute a cart write for a requested individual creation or remove a cart entry unless the supported operation explicitly does so.

## Order checkout from saved cart

1. Retrieve the complete current saved cart and show every item with its selected Book format(s) or Tactile Diagram type. An order submits this cart; it does not accept an invented list of items in place of the saved cart.
2. Validate every item's saved selections against current catalog detail. Keep valid saved choices and show them; do not ask the user to choose them again. If a saved Book has no valid format or a diagram lacks a valid type, ask for that item's missing choices. Identify the affected item in every question, particularly for mixed carts.
3. If corrections are needed, review and obtain authorization for each exact cart replacement, save through the matching cart tool, then re-read the cart before checkout. Do not edit the cart silently while preparing an order or pass missing selections into checkout hoping the server fills them.
4. Collect `orderReason`. Explain that it becomes the request reason for the generated requests; do not invent separate per-item reasons or assume a previous individual-request reason applies to the order. When the user requests different reasons per item, clarify that normal checkout uses one shared reason and offer an authorized individual-request workflow instead.
5. Show the complete final cart, options, reason, and beneficiary, then obtain the transaction skill's explicit checkout confirmation immediately before `create_member_order` or `create_admin_order`. A previous add-to-cart instruction does not authorize checkout. An empty cart cannot produce an order; ask which items they want to add, without creating them automatically. A cart larger than 249 items must be split with the user's instruction; never silently truncate it.
6. Follow the existing partial-order safeguards: present returned blocked items, explain their exclusion and cart-removal consequences, and obtain explicit confirmation of the exact skipped set. This confirmation does not supply a missing format/type/reason. If the cart, selections, or skipped set changes, refresh the review before retrying.
7. Await creation and verify returned order/generated-request details. Report each actual saved item and options, the shared reason, initial statuses, beneficiary, IDs and returned links. Preserve the cart/answers on failure and inspect saved state before retrying an uncertain outcome.

## Example intake decisions

- “Add this Book to my cart.” → resolve the item and show its formats; wait for a format choice; do not ask for a submission reason.
- “Request this Book as DAISY for my course.” → validate DAISY for that Book and use the stated course reason; do not ask the same questions again.
- “Request this diagram.” → ask which supported diagram type and the request reason; do not create with `N/A`.
- “Place my order.” → retrieve/review the cart, resolve incomplete choices per item, ask for the order reason, and obtain checkout confirmation.
- “Change the Book in my cart to Braille.” → validate the choice, show the existing selection and replacement; do not create a new request.
