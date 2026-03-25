# Payment & Query Filter Values

**Payment statuses:** `APPROVED`, `COMPLETED`, `FAILED`, `CANCELED`, `IN_PROGRESS`

**Payment source types:** `CARD`, `MOBILE_APP`, `EXTERNAL_API`, `CASH`, `OTHER`

**Entry methods:** `SWIPED`, `KEYED`, `EMV`, `CONTACTLESS`

**Card brands:** `VISA`, `MASTERCARD`, `AMEX`, `DISCOVER`, `OTHER`

**Risk levels:** `NORMAL`, `HIGH`, `VERY_HIGH`

**Customer types:** `STANDARD`, `MOBILE_APP`, `CAPITAL`, `GIFT_CARD`, `REMITTANCE`

**Amount range:** in cents (e.g., `{"min": 1000, "max": 5000}` = $10–$50)

**Sort fields:** `CREATED_AT`, `AMOUNT`, `STATUS`

**Sort order:** `ASC`, `DESC`
