# Ditto API Parameter Reference

## Generate Account Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `square_id` | string | **required** | Your Square username (use `whoami`) |
| `country_code` | string | `"US"` | `"US"` or `"GB"` |
| `passcode` | string | `"0000"` | Account passcode |
| `link_phone_number` | bool | `false` | Link a phone number to the account |
| `link_debit_card` | bool | `true` | Link a debit card |
| `set_address` | bool | `true` | Set a mailing address |
| `complete_idv` | bool | `false` | Complete identity verification |
| `num_sponsorship_requests` | int | `0` | Number of teen sponsorship requests |
| `business_account` | bool | `false` | Create as business account |
| `custom_alias` | string | `null` | Custom alias/nickname for the account |
| `order_cash_card` | bool | `false` | Order a Cash Card |
| `link_credit_card` | bool | `false` | Link a credit card |
| `banking_stack` | string | `"sutton_marqeta"` | Banking stack (`"sutton_marqeta"`, `"pathward_marqeta"`, `"bancorp_marqeta"`) |
| `borrow_credit_line` | bool | `false` | Enable Borrow eligibility. Requires: `complete_idv`, `set_address`, `order_cash_card`, and a supported `us_state` (e.g. `"TX"`, `"CA"`, `"NY"`) |
| `borrow_lending_program` | string | `"PHASE12E"` | Borrow lending program: `"PHASE12E"` (normal) or `"FAST_OVERDUE"` (fast — loans expire in ~4 min for overdue testing; disable auto-pay post-creation) |
| `retro_credit_line` | bool | `false` | Enable Retro eligibility. Requires: `complete_idv`, `set_address`, `order_cash_card`, `link_phone_number`, a supported `us_state` (e.g. `"TX"`), and `cash-retro-testers` LD segment. Post-creation: approve/activate card, add credit decision via Toolbox Prospector |
| `retro_lending_program` | string | `"RETRO_AFTERPAY_6_WEEK_WEEKLY"` | Retro lending program: `"RETRO_AFTERPAY_6_WEEK_WEEKLY"` (normal) or `"FAST_RETRO_AFTERPAY_6_WEEK_WEEKLY"` (fast — loans expire in ~30 min for overdue testing; disable auto-pay post-creation) |
| `retro_credit_line_amount_cents` | int | `40000` | Retro credit line amount in cents (only used when `retro_credit_line: true`) |
| `apcac_credit_line` | bool | `false` | Enable APCAC (Afterpay on Cash App Card) eligibility. Requires: `complete_idv`, `set_address`, `order_cash_card`, and a supported `us_state`. Post-creation: approve/activate card, add `afterpay-cash-app-card-users` LD segment, add credit decision via Toolbox Prospector with `PRE_PURCHASE_FINANCING` |
| `apcac_lending_program` | string | `"PRE_PURCHASE_6_WEEK"` | APCAC lending program: `"PRE_PURCHASE_6_WEEK"` (normal) or `"FAST_FAST_PRE_PURCHASE_ALPHA"` (fast — loans expire in ~30 min for overdue testing; disable auto-pay post-creation) |
| `apcac_credit_line_amount_cents` | int | `40000` | APCAC credit line amount in cents (only used when `apcac_credit_line: true`) |
| `us_state` | string | — | US state code. Required for borrow, retro, and APCAC eligible accounts. APCAC supported states: `AL`, `AK`, `AR`, `AZ`, `DC`, `DE`, `FL`, `ID`, `IN`, `KY`, `LA`, `MI`, `MO`, `MS`, `MT`, `NH`, `OH`, `OK`, `TN`, `TX`, `UT` |
| `launch_darkly_target_configs` | list | `[]` | LaunchDarkly flag target configs |

## Account Response Fields

The response includes synthetic staging test data (not real PII): `customer_token`, `email`, `cashtag`, `region`, `name`, `phone_number`, `debit_card`, `passcode`, `address`, `postal_code`, `birthdate`, `ssn_last_four`, `idv_completed`, `date_created`, `owner`, `business_account`, `tags`, and more.

## Transaction Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `customer_token` | string | **Required.** The account initiating the transaction |
| `add_cash_amount` | int | Amount in cents to add cash (fund from debit card) |
| `country_code` | string | `"US"` or `"GB"` |
| `recipient_token` | string | Customer token of payment recipient |
| `send_payment_amount` | int | Amount in cents to send via P2P |
| `requestee_token` | string | Customer token to request payment from |
| `request_payment_amount` | int | Amount in cents to request |
