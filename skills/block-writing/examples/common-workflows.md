# Common Workflow Examples

## Writing a button label

**Scenario**: Cash App — user taps a CTA to send money to a contact.

**Draft**: "Send Money Now" → ❌ unnecessary word, title case
**Revised**: "Send money" ✅ — verb + object, sentence case, no filler

**Scenario**: Square — seller completes a card-present transaction.

**Draft**: "Process Payment" → ❌ title case, jargon
**Revised**: "Charge $24.50" ✅ — specific, action-forward, sentence case

---

## Writing an error message

**Scenario**: Cash App — P2P payment fails due to insufficient balance.

**Draft**: "Transaction failed" → ❌ vague, no path forward
**Revised**: "Payment didn't go through. Your balance is $12.40 — add money or use a different payment method." ✅ — what happened + why + what to do

**Scenario**: Square — card reader times out during checkout.

**Draft**: "Error: Device not connected" → ❌ technical code framing, no action
**Revised**: "Card reader not responding. Check the connection and try again." ✅ — plain language, specific action

---

## Design review (component audit)

**Scenario**: Reviewing a Cash App modal before launch.

Check against:
1. Title: ≤40 chars, sentence case, names the decision not the system
2. Body: ≤100 chars, answers "why does this matter to me"
3. Primary button: verb + object (not "OK", "Yes", "Confirm")
4. Destructive action: red button last, plain-language consequence ("Delete card", not "Proceed")

**Before**: Title "Are you sure?" / Body "This action cannot be undone." / Buttons "Cancel" + "Yes"
**After**: Title "Remove this card?" / Body "You'll need to add it again to use it for payments." / Buttons "Keep card" + "Remove card"
