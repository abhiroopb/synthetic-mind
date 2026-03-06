# Ditto Common Workflows

## Create a fully set up test account
1. Generate account with `complete_idv: true`, `link_debit_card: true`, `order_cash_card: true`
2. Add cash to the account using generate-transaction
3. Tag the account for easy identification

## Create two accounts for P2P testing
1. Generate two accounts
2. Add cash to both using generate-transaction
3. Send payment from one to the other

## Create a borrow-eligible account
1. Generate account with `complete_idv: true`, `set_address: true`, `order_cash_card: true`, `borrow_credit_line: true`, and `us_state` set to a supported state (e.g. `"TX"`, `"CA"`, `"NY"`)
2. Add cash to the account using generate-transaction

## Create a retro-eligible account
1. Generate account with `complete_idv: true`, `set_address: true`, `order_cash_card: true`, `link_phone_number: true`, `retro_credit_line: true`, `us_state: "TX"`, and `launch_darkly_target_configs: [{"key": "cash-retro-testers", "type": "segment"}]`
2. Add cash to the account using generate-transaction
3. Use **toolbox** skill to approve and activate the cash card (`postcard/review-card-customizations` → `postcard/activate-cash-card`)
4. Use **toolbox** skill to add credit decision (`prospector/add-credit-decision` with `RETROACTIVE_FINANCING` / `RETRO_AFTERPAY_6_WEEK_WEEKLY`)
5. Use **toolbox** skill to simulate card transactions over $20 (`moneymancer/Simulate`)

## Create an APCAC-eligible account
1. Generate account with `complete_idv: true`, `set_address: true`, `order_cash_card: true`, `link_phone_number: true`, `apcac_credit_line: true`, `us_state: "AL"`, and `launch_darkly_target_configs: [{"key": "afterpay-cash-app-card-users", "type": "segment"}]`
2. Add cash to the account using generate-transaction
3. Use **toolbox** skill to approve and activate the cash card
4. Use **toolbox** skill to add credit decision (`prospector/add-credit-decision` with `PRE_PURCHASE_FINANCING` / `PRE_PURCHASE_6_WEEK`)
5. Enable `mobile-prepurchase-cash-card-pilot` client flag on the staging device

## Create an account with card transaction history
1. Generate account with `complete_idv: true`, `link_debit_card: true`, `order_cash_card: true`
2. Add cash to the account using generate-transaction
3. Use the **toolbox** skill to simulate card transactions via `moneymancer/Simulate`

## Target a test account for a feature flag
1. Call `get-launch-darkly-flag` with the flag key to find the `variation_id` you want
2. Call `add-launch-darkly-targets` with the flag key, variation_id, and customer token(s)
3. Or, include `launch_darkly_target_configs` in `generate-account` to target at creation time

## Create a teen account
1. Generate a parent account with `complete_idv: true`
2. Generate another account with `num_sponsorship_requests: 1` referencing the parent
