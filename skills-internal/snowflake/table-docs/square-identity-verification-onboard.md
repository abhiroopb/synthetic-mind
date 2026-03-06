# Square Identity Verification — ONBOARD

Query and analyze payment onboarding data from the ONBOARD Snowflake database, owned by the Payment Onboarding team in the Identity Organization at Square.

## Overview

The ONBOARD database tracks the merchant signup flow from initial registration through identity verification and underwriting:

- **Merchant activation**: The core signup flow linking personas, underwriting, legal entities, and browser sessions
- **Identity verification (IDV)**: Persona data collection, vendor-based identity matching, KBA quizzes, and document verification
- **Underwriting decisions**: Automated and manual review of merchant applications

ONBOARD is linked to LEGALENTITIES via `STRUCTURE_TOKEN` — see `square-identity-verification-legalentities.md` for legal entity tables.

For ROSTER merchant/unit token lookups, see `roster-merchant-location-employee-lookups.md`.

**Country-prefixed tables:** Several tables use a 2-letter country code prefix (e.g., `AU_ADDRESSES`, `US_PERSONAS`). These contain similar data but with country-specific structures that were not combined into a single table. The generic `PERSONAS` table holds shared fields for all countries.

---

## Tables

### Core Onboarding Flow

#### ONBOARD.RAW_OLTP.ACTIVATION_FLOWS

Central table for the onboarding flow. Each row represents one activation attempt for a merchant. Links to personas, underwriting, legal entities, and browser interactions.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `USER_TOKEN` (TEXT) — User who initiated the activation
- `MERCHANT_TOKEN` (TEXT) — Merchant being activated
- `UNIT_TOKEN` (TEXT) — Unit token for the merchant
- `EMPLOYEE_TOKEN` (TEXT) — Employee token
- `FLOW_NAME` (TEXT) — Name of the activation flow
- `STATUS` (TEXT) — Current status of the activation flow
- `COUNTRY_CODE` (TEXT) — Country code for the activation
- `PERSONA_ID` (NUMBER) — FK → `PERSONAS.ID` (or country-specific persona table, based on `PERSONA_TYPE`)
- `PERSONA_TYPE` (TEXT) — Determines which country persona table to join
- `COMPANY_ID` (NUMBER) — FK → country-specific companies table (e.g., `US_COMPANIES.ID`)
- `COMPANY_TYPE` (TEXT) — Type of company
- `BUSINESS_CATEGORY` (TEXT) — Business category
- `BUSINESS_SUB_CATEGORY` (TEXT) — Business sub-category
- `MCC` (TEXT) — Merchant Category Code
- `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `MERCHANT_ACTIVATION_ID` (NUMBER) — FK → `MERCHANT_ACTIVATIONS.ID`
- `BROWSER_INTERACTION_ID` (NUMBER) — FK → `BROWSER_INTERACTIONS.ID`
- `BANK_ACCOUNT_ID` (NUMBER) — Bank account linked during signup
- `BANK_ACCOUNT_TYPE` (TEXT) — Type of bank account
- `SIGNUP_TOKEN` (TEXT) — Signup session token
- `STRUCTURE_TOKEN` (TEXT) — FK → `LEGALENTITIES.RAW_OLTP.*` tables (primary cross-database link)
- `LEGALENTITIES_STRUCTURE_VERSION` (TEXT) — Version of the legal entity structure
- `PRIMARY_PERSONA_LEGAL_ENTITY_TOKEN` (TEXT) — FK → legal entity for the primary persona
- `BUSINESS_LEGAL_ENTITY_TOKEN` (TEXT) — FK → legal entity for the business
- `POLL_TOKEN` (TEXT) — Poll token for async operations
- `PREFERRED_LANGUAGE` (TEXT) — User's preferred language
- `EMAIL` (TEXT) — Email address
- `LEGACY_DATA` (BOOLEAN) — Whether this is migrated legacy data
- `LEGACY_ID` (TEXT) — Legacy system ID
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS

Tracks the activation lifecycle for a merchant. There should be **only one record per merchant+unit pair** (though most merchants have a single record per merchant_token). Points to the current activation flow.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `CURRENT_ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID` (the current/latest flow)
- `UNIT_TOKEN` (TEXT) — Unit token
- `MERCHANT_TOKEN` (TEXT) — Merchant token
- `RETRY_COUNT` (NUMBER) — Number of activation retries
- `LAST_VARIANT_SEEN` (TEXT) — Last activation flow variant
- `LE_ACTIVATION_DATA_MIGRATION_STATE` (TEXT) — Legal entities data migration state
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.BREADCRUMBS

Status breadcrumbs for activation flows. Tracks status transitions during onboarding.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `STATUS` (TEXT) — Breadcrumb status
- `ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID`
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.BROWSER_INTERACTIONS

Browser metadata captured during activation sessions. Used for fraud detection and session tracking.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `IP` (TEXT) — IP address
- `USER_AGENT` (TEXT) — Browser user agent string
- `AVT` (TEXT) — AVT token
- `TIME_ZONE` (TEXT) — Browser timezone
- `MULTIPASS_LOGGABLE_SESSION_TOKEN` (TEXT) — Multipass session token
- `BROWSER_FINGERPRINT` (TEXT) — Browser fingerprint hash
- `BROWSER_INTERACTION_METADATA` (BINARY) — Serialized metadata (protobuf, not directly queryable)
- `SUPER_POS_ENABLED` (BOOLEAN) — Whether Super POS is enabled
- `REQUEST_HEADERS` (BINARY) — Serialized request headers (protobuf, not directly queryable)
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.MOBILE_SESSIONS

Mobile activation sessions for merchants signing up via mobile.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `SESSION_TOKEN` (TEXT) — Unique session token
- `MERCHANT_TOKEN` (TEXT) — Merchant token
- `UNIT_TOKEN` (TEXT) — Unit token
- `CUSTOMER_TOKEN` (TEXT) — Customer token
- `EMPLOYEE_TOKEN` (TEXT) — Employee token
- `COUNTRY_CODE` (TEXT) — Country code
- `LANGUAGE_CODE` (TEXT) — Language code
- `FLOW_NAME` (TEXT) — Activation flow name
- `FLOW_VERSION` (NUMBER) — Flow version
- `CURRENT_PANEL_NAME` (TEXT) — Current panel/step in the flow
- `IDEMPOTENT_TOKEN` (TEXT) — Idempotency token
- `PARAMS_DESTROYED_AT` (TIMESTAMP_NTZ) — When sensitive params were cleared
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

---

### Identity & Persona Data

#### ONBOARD.RAW_OLTP.PERSONAS

Generic persona data shared across all countries. Each persona represents an individual associated with a merchant activation (account owner, beneficial owner, etc.).

**Key Fields:**
- `ID` (NUMBER) — Primary key (FK target for `ACTIVATION_FLOWS.PERSONA_ID`)
- `FIRST_NAME` (TEXT) — First name
- `LAST_NAME` (TEXT) — Last name
- `ENCRYPTED_BIRTH_DATE` (TEXT) — Encrypted date of birth
- `ADDRESS_TOKEN` (TEXT) — Address vault token
- `PHONE_NUMBER` (TEXT) — Phone number
- `ACCOUNT_OWNER` (BOOLEAN) — Whether this persona is the account owner
- `COUNTRY_CODE` (TEXT) — Country code
- `POLYMORPHIC_TYPE` (TEXT) — Country-specific persona type (determines which country table to join)
- `BENEFICIAL_OWNER_ROLE` (TEXT) — Role if this persona is a beneficial owner
- `INCORRECT` (NUMBER) — Whether data has been flagged as incorrect
- `INCORRECT_REASON` (TEXT) — Reason for incorrect flag
- `BLETCHLEY_KEY_ID` (NUMBER) — Encryption key ID
- `COUNTRY_PROTO_DATA` (BINARY) — Country-specific data (protobuf, not directly queryable)
- `VAULTED_DATA_SERIALIZED_PROTO` (BINARY) — Vaulted sensitive data (protobuf, not directly queryable)
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.US_PERSONAS

US-specific persona details including SSN data.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FIRST_NAME` (TEXT) — First name
- `LAST_NAME` (TEXT) — Last name
- `ENCRYPTED_BIRTH_DATE` (TEXT) — Encrypted date of birth
- `ENCRYPTED_FULL_SSN` (TEXT) — Encrypted full SSN
- `ENCRYPTED_LAST_4_SSN` (TEXT) — Encrypted last 4 of SSN
- `FULL_SSN_FIDELIUS_TOKEN` (TEXT) — Fidelius vault token for SSN
- `PHONE_NUMBER` (TEXT) — Phone number
- `ADDRESS_TOKEN` (TEXT) — Address vault token
- `ADDRESS_HASH` (TEXT) — Hash of the address
- `BLETCHLEY_KEY_ID` (NUMBER) — Encryption key ID
- `VAULTED_DATA_SERIALIZED_PROTO` (BINARY) — Vaulted data (not directly queryable)
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.AU_PERSONAS

Australian-specific persona details.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FIRST_NAME`, `LAST_NAME` (TEXT) — Name
- `ENCRYPTED_BIRTH_DATE` (TEXT) — Encrypted DOB
- `PHONE_NUMBER` (TEXT) — Phone
- `DOCUMENT_TYPE` (TEXT) — ID document type
- `ENCRYPTED_DOCUMENT` (TEXT) — Encrypted document data
- `ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID`
- `AU_COMPANY_ID` (NUMBER) — FK → `AU_COMPANIES.ID`
- `COMPANY_RELATIONSHIP` (TEXT) — Relationship to company
- `ACCOUNT_OWNER` (BOOLEAN) — Is account owner
- `ADDRESS_TOKEN` (TEXT), `ADDRESS_HASH` (TEXT) — Address references
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.CANADA_PERSONAS

Canadian-specific persona details.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `FIRST_NAME`, `LAST_NAME` (TEXT) — Name
- `ENCRYPTED_BIRTH_DATE` (TEXT) — Encrypted DOB
- `ENCRYPTED_SOCIAL_INSURANCE_NUMBER` (TEXT) — Encrypted SIN
- `FULL_SIN_FIDELIUS_TOKEN` (TEXT) — Fidelius vault token for SIN
- `PHONE_NUMBER` (TEXT) — Phone
- `ADDRESS_TOKEN` (TEXT), `ADDRESS_HASH` (TEXT) — Address references
- `BLETCHLEY_KEY_ID` (NUMBER) — Encryption key ID
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.JP_PERSONAS

Japanese-specific persona details with kanji/katakana/romaji name variants.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `KANJI_FIRST_NAME`, `KANJI_LAST_NAME` (TEXT) — Kanji name
- `KATAKANA_FIRST_NAME`, `KATAKANA_LAST_NAME` (TEXT) — Katakana name
- `ROMAJI_FIRST_NAME`, `ROMAJI_LAST_NAME` (TEXT) — Romaji name
- `ENCRYPTED_BIRTH_DATE` (TEXT) — Encrypted DOB
- `PHONE_NUMBER` (TEXT) — Phone
- `GENDER` (TEXT) — Gender
- `ADDRESS_TOKEN` (TEXT), `ADDRESS_HASH` (TEXT), `ADDRESS_TYPE` (TEXT) — Address references
- `BLETCHLEY_KEY_ID` (NUMBER) — Encryption key ID
- `CREATED_AT` (TIMESTAMP_NTZ)
- `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.US_ADDRESSES

US mailing addresses associated with personas.

**Key Fields:**
- `ID` (NUMBER), `PERSONA_ID` (NUMBER) — FK → `US_PERSONAS.ID`
- `ADDRESS_LINE_1` (TEXT), `ADDRESS_LINE_2` (TEXT), `CITY` (TEXT), `STATE` (TEXT), `POSTAL_CODE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.AU_ADDRESSES

Australian addresses.

**Key Fields:**
- `ID` (NUMBER), `OWNER_ID` (NUMBER) — FK → owning entity ID, `OWNER_TYPE` (TEXT)
- `ADDRESS_LINE_1` (TEXT), `ADDRESS_LINE_2` (TEXT), `CITY` (TEXT), `STATE` (TEXT), `POSTAL_CODE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.CANADA_ADDRESSES

Canadian addresses.

**Key Fields:**
- `ID` (NUMBER), `CANADA_PERSONA_ID` (NUMBER) — FK → `CANADA_PERSONAS.ID`
- `ADDRESS_LINE_1` (TEXT), `ADDRESS_LINE_2` (TEXT), `CITY` (TEXT), `PROVINCE` (TEXT), `POSTAL_CODE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.JP_ADDRESSES

Japanese addresses with kanji/katakana variants.

**Key Fields:**
- `ID` (NUMBER), `OWNER_ID` (NUMBER) — FK → owning entity, `OWNER_TYPE` (TEXT)
- `PREFECTURE_ISO_CODE` (TEXT), `KANJI_PREFECTURE` (TEXT), `KATAKANA_PREFECTURE` (TEXT)
- `KANJI_CITY` (TEXT), `KATAKANA_CITY` (TEXT), `KANJI_TOWN` (TEXT), `KATAKANA_TOWN` (TEXT)
- `CHOME_BANCHI` (TEXT), `BUILDING_NAME` (TEXT), `POSTAL_CODE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.BUSINESSES

Business entity information. Polymorphic across countries.

**Key Fields:**
- `ID` (NUMBER) — Primary key
- `COUNTRY_CODE` (TEXT), `POLYMORPHIC_TYPE` (TEXT) — Country-specific business type
- `OWNERSHIP_STRUCTURE` (TEXT), `ENTITY_TYPE` (TEXT)
- `COUNTRY_PROTO_DATA` (BINARY) — Country-specific data (protobuf, not directly queryable)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.BUSINESS_RELATIONSHIPS

Links personas to businesses. Defines who has what relationship to a business entity.

**Key Fields:**
- `ID` (NUMBER), `PERSONA_ID` (NUMBER) — FK → `PERSONAS.ID`, `BUSINESS_ID` (NUMBER) — FK → `BUSINESSES.ID`
- `RELATIONSHIP` (TEXT) — Relationship type (e.g., owner, officer)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.US_COMPANIES

US company details including EIN.

**Key Fields:**
- `ID` (NUMBER), `NAME` (TEXT), `ENCRYPTED_EIN` (TEXT), `EIN_FIDELIUS_TOKEN` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.AU_COMPANIES

Australian company details including ABN/ACN.

**Key Fields:**
- `ID` (NUMBER), `LEGAL_BUSINESS_NAME` (TEXT)
- `AUSTRALIAN_BUSINESS_NUMBER` (TEXT), `AUSTRALIAN_COMPANY_NUMBER` (TEXT)
- `BUSINESS_STRUCTURE` (TEXT), `ADDRESS_TOKEN` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.JP_COMPANIES

Japanese company details with kanji/katakana/romaji names.

**Key Fields:**
- `ID` (NUMBER)
- `KANJI_COMPANY_NAME` (TEXT), `KATAKANA_COMPANY_NAME` (TEXT), `ROMAJI_COMPANY_NAME` (TEXT)
- `COMPANY_TYPE` (TEXT), `CORPORATE_NUMBER` (TEXT), `PHONE_NUMBER` (TEXT)
- `LICENSE_NUMBER` (TEXT), `LICENSE_TYPE` (TEXT), `WEBSITE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.IDENTITY_HASHES

Hashed identity data for merchants. Used for deduplication and fraud detection.

**Key Fields:**
- `ID` (NUMBER), `MERCHANT_TOKEN` (TEXT), `IDENTITY_HASH` (TEXT), `IDENTITY_HASH_TYPE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

---

### Underwriting & Verification

#### ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS

Underwriting decisions and state for merchant activations. Each activation flow has one underwriting request that tracks the decision lifecycle.

**Key Fields:**
- `ID` (NUMBER) — Primary key (FK target for `ACTIVATION_FLOWS.UNDERWRITING_REQUEST_ID`)
- `DECISION` (TEXT) — Underwriting decision
- `UNDERWRITING_STATE` (TEXT) — Current underwriting state
- `MANUAL_DECISION` (TEXT) — Manual review decision (if any)
- `MANUAL_DECISION_AT` (TIMESTAMP_NTZ) — When manual decision was made
- `RISK_SCORE` (NUMBER) — Risk score
- `RISKARBITER_EVALUATION_RESULT` (TEXT) — Risk arbiter result
- `MATCH_COUNT` (NUMBER) — Number of identity matches
- `QUIZ_QUESTION_COUNT` (NUMBER), `QUIZ_ANSWERS_CORRECT` (NUMBER) — KBA quiz data
- `VERIFICATION_STATE` (TEXT) — Verification state
- `VERIFICATION_DECISION_STATUS` (TEXT), `VERIFICATION_DECISION_REASON` (TEXT) — Verification decision
- `ACTIVATION_DECISION` (TEXT), `ACTIVATION_STATE` (TEXT) — Final activation outcome
- `ACTIVATION_COHORT` (TEXT), `ACTIVATION_VERSION` (NUMBER)
- `BAD_ACTORS_SCREEN_STATE` (TEXT) — Bad actors screening state
- `LAST_PROCESSED_DECISION_SEQUENCE` (NUMBER) — Last processed decision sequence from LEGALENTITIES
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.UNDERWRITING_VENDOR_RESULTS

Responses from external identity verification vendors.

**Key Fields:**
- `ID` (NUMBER), `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `REQUEST_TYPE` (TEXT), `VENDOR_ID` (TEXT), `RESPONSE_STATUS` (TEXT)
- `ENCRYPTED_RESPONSE_TEXT` (TEXT) — Encrypted response data
- `IDMATCH_BACKFILL_STATE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.UNDERWRITING_FEED_ENTRIES

Feed sync entries for underwriting.

**Key Fields:**
- `ID` (NUMBER), `FEED_SYNC_ID` (NUMBER), `ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID`
- `COUNTRY_CODE` (TEXT)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.COMPLIANCE_CHECKS

Compliance check results tied to underwriting requests.

**Key Fields:**
- `ID` (NUMBER), `CHECK_TYPE` (TEXT), `CHECK_RESULT` (TEXT)
- `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.IDMATCH_RESULTS

Identity match results from vendor identity verification.

**Key Fields:**
- `ID` (NUMBER), `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `BENEFICIAL_OWNER_UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `BENEFICIAL_OWNER_UNDERWRITING_REQUESTS.ID`
- `STATE` (TEXT), `REQUEST_TYPE` (TEXT), `RISK_SCORE` (NUMBER)
- `TOTAL_QUESTION_COUNT` (NUMBER), `CORRECT_QUESTION_COUNT` (NUMBER)
- `MORE_VENDORS_AVAILABLE` (BOOLEAN)
- `CREATED_AT` (TIMESTAMP_NTZ), `UPDATED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.IDMATCH_MATCHED_ATTRIBUTES

Individual attribute match details from identity verification.

**Key Fields:**
- `ID` (NUMBER), `IDMATCH_RESULT_ID` (NUMBER) — FK → `IDMATCH_RESULTS.ID`
- `ATTRIBUTE_NAME` (TEXT) — Attribute checked (e.g., name, address, DOB, SSN)
- `MATCHED` (NUMBER) — Whether matched (1 = yes, 0 = no)

#### ONBOARD.RAW_OLTP.MATCHED_ATTRIBUTES

Vendor-level matched attributes from underwriting vendor results.

**Key Fields:**
- `ID` (NUMBER), `UNDERWRITING_VENDOR_RESULT_ID` (NUMBER) — FK → `UNDERWRITING_VENDOR_RESULTS.ID`
- `ATTRIBUTE_NAME` (TEXT), `MATCHED` (BOOLEAN)

#### ONBOARD.RAW_OLTP.QUIZ_RESULTS

Knowledge-Based Authentication (KBA) quiz results from vendor verification.

**Key Fields:**
- `ID` (NUMBER), `UNDERWRITING_VENDOR_RESULT_ID` (NUMBER) — FK → `UNDERWRITING_VENDOR_RESULTS.ID`
- `QUESTION_COUNT` (NUMBER), `CORRECT_ANSWER_COUNT` (NUMBER)

#### ONBOARD.RAW_OLTP.BENEFICIAL_OWNER_UNDERWRITING_REQUESTS

Underwriting requests specifically for beneficial owners of a business.

**Key Fields:**
- `ID` (NUMBER), `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `PERSONA_ID` (NUMBER) — FK → `PERSONAS.ID`, `PERSONA_TYPE` (TEXT)
- `DECISION` (TEXT), `MANUAL_DECISION` (TEXT)

#### ONBOARD.RAW_OLTP.IDV_INVITATIONS

Document identity verification invitations.

**Key Fields:**
- `ID` (NUMBER), `INVITATION_TOKEN` (TEXT), `NODE_TOKEN` (TEXT)
- `STRUCTURE_TOKEN` (TEXT) — FK → LEGALENTITIES structure
- `EXPIRES_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.US_WEB_HISTORICAL_RESULTS

Legacy US web identity verification results. Contains historical IDology and IDA match/quiz data.

**Key Fields:**
- `ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID`
- `UNDERWRITING_REQUEST_ID` (NUMBER) — FK → `UNDERWRITING_REQUESTS.ID`
- `DECISION` (TEXT) — Verification decision
- `IDOLOGY_MATCHED_NAME` (BOOLEAN), `IDOLOGY_MATCHED_ADDRESS` (BOOLEAN), `IDOLOGY_MATCHED_BIRTH_DATE` (BOOLEAN), `IDOLOGY_MATCHED_SSN` (BOOLEAN) — IDology matches
- `IDA_MATCHED_NAME` (BOOLEAN), `IDA_MATCHED_ADDRESS` (BOOLEAN), `IDA_MATCHED_BIRTH_DATE` (BOOLEAN), `IDA_MATCHED_SSN` (BOOLEAN) — IDA matches
- `RISK_SCORE` (NUMBER)

---

### Analytics & Other

#### ONBOARD.RAW_OLTP.MERCHANT_ANALYTICS

Signup analytics and self-reported merchant information collected during onboarding.

**Key Fields:**
- `ID` (NUMBER), `ACTIVATION_FLOW_ID` (NUMBER) — FK → `ACTIVATION_FLOWS.ID`
- `ESTIMATED_REVENUE` (TEXT), `ESTIMATED_MONTHLY_REVENUE` (TEXT), `ESTIMATED_PAYMENT_FREQUENCY` (TEXT)
- `HEARD_ABOUT_SQUARE_VIA` (TEXT), `ACCOUNT_TYPE` (TEXT), `PAYMENT_TYPE` (TEXT)

#### ONBOARD.RAW_OLTP.PAYMENT_BRAND_ENROLLMENTS

Card brand enrollment status. Primarily used for Japan-specific payment brand enrollments.

**Key Fields:**
- `ID` (NUMBER), `UNIT_TOKEN` (TEXT), `CARD_BRAND` (TEXT), `FELICA_BRAND` (TEXT)
- `STATUS` (TEXT), `ENROLLED_AT` (TIMESTAMP_NTZ), `APPROVED_AT` (TIMESTAMP_NTZ)

#### ONBOARD.RAW_OLTP.PAYMENT_LOCATIONS

Payment location types collected during onboarding analytics.

**Key Fields:**
- `ID` (NUMBER), `LOCATION_TYPE` (TEXT), `MERCHANT_ANALYTIC_ID` (NUMBER) — FK → `MERCHANT_ANALYTICS.ID`

#### ONBOARD.RAW_OLTP.VALIDATA_VALIDATION_FINDINGS

Field-level validation findings from the Validata validation service.

**Key Fields:**
- `ID` (NUMBER), `REQUEST_ID` (TEXT), `MERCHANT_TOKEN` (TEXT), `COUNTRY_CODE` (TEXT)
- `FIELD_NAME` (TEXT), `FIELD_PATH` (TEXT), `FIELD_VALUE` (TEXT)
- `VALIDATION_MODE` (TEXT), `ERROR_MESSAGES` (TEXT)

#### ONBOARD.RAW_OLTP.EMONEY_SSP_REQUESTS

Japan e-money SSP (Special Service Provider) requests.

**Key Fields:**
- `ID` (NUMBER), `UNIT_TOKEN` (TEXT), `SSP_REQUEST_TOKEN` (TEXT)
- `SSP_COMPLETE` (BOOLEAN), `SSP_CREATION_STATUS` (TEXT)

---

### Japan-Specific

#### ONBOARD.RAW_OLTP.JP_STORES

Japanese store location data.

**Key Fields:**
- `ID` (NUMBER), `UNIT_TOKEN` (TEXT), `PRIMARY_STORE` (NUMBER)
- `STORE_NAME_KANJI` (TEXT), `STORE_NAME_KATAKANA` (TEXT), `STORE_NAME_ROMAJI` (TEXT)
- `PHONE_NUMBER` (TEXT), `STORE_URL` (TEXT)

#### ONBOARD.RAW_OLTP.JP_JCB_ACTIVATIONS

JCB card brand activation tracking for Japan.

**Key Fields:**
- `ID` (NUMBER), `CURRENT_JCB_ACTIVATION_FLOW_ID` (NUMBER) — FK → `JP_JCB_ACTIVATION_FLOWS.ID`
- `MERCHANT_ACTIVATION_ID` (NUMBER) — FK → `MERCHANT_ACTIVATIONS.ID`
- `MERCHANT_TOKEN` (TEXT), `UNIT_TOKEN` (TEXT)

#### ONBOARD.RAW_OLTP.JP_JCB_ACTIVATION_FLOWS

JCB activation flow steps and states.

**Key Fields:**
- `ID` (NUMBER), `JCB_ACTIVATION_ID` (NUMBER) — FK → `JP_JCB_ACTIVATIONS.ID`
- `STATUS` (TEXT), `STORE_ID` (NUMBER) — FK → `JP_STORES.ID`
- `REGULATOR_CASE_TOKEN` (TEXT), `IRF_TOKEN` (TEXT)

#### ONBOARD.RAW_OLTP.JP_JCB_RESPONSES

JCB screening/approval responses.

**Key Fields:**
- `ID` (NUMBER), `UNIT_TOKEN` (TEXT), `TERMINAL_ID` (TEXT)
- `JUDGEMENT` (TEXT), `MERCHANT_NUMBER` (TEXT), `REASON_CODE1` (NUMBER), `REASON_CODE2` (NUMBER)

#### ONBOARD.RAW_OLTP.JP_METI_FORMS

Japan METI compliance forms.

**Key Fields:**
- `ID` (NUMBER), `MERCHANT_TOKEN` (TEXT), `IS_ELIGIBLE` (BOOLEAN), `ANSWERS` (TEXT)

#### ONBOARD.RAW_OLTP.JP_REGISTER_EMONEY_INTENTS

Japan e-money registration intents.

**Key Fields:**
- `ID` (NUMBER), `UNIT_TOKEN` (TEXT), `REGISTER_ALL` (BOOLEAN)

---

## Table Relationships

```
MERCHANT_ACTIVATIONS (one per merchant+unit pair)
    └── CURRENT_ACTIVATION_FLOW_ID → ACTIVATION_FLOWS.ID

ACTIVATION_FLOWS (central hub)
    ├── MERCHANT_ACTIVATION_ID → MERCHANT_ACTIVATIONS.ID
    ├── PERSONA_ID → PERSONAS.ID (join country table via PERSONA_TYPE)
    ├── COMPANY_ID → US_COMPANIES.ID / AU_COMPANIES.ID / JP_COMPANIES.ID
    ├── UNDERWRITING_REQUEST_ID → UNDERWRITING_REQUESTS.ID
    ├── BROWSER_INTERACTION_ID → BROWSER_INTERACTIONS.ID
    ├── STRUCTURE_TOKEN → LEGALENTITIES tables (see square-identity-verification-legalentities.md)
    ├── PRIMARY_PERSONA_LEGAL_ENTITY_TOKEN → LEGALENTITIES entity tables
    └── BUSINESS_LEGAL_ENTITY_TOKEN → LEGALENTITIES entity tables

UNDERWRITING_REQUESTS
    ├── COMPLIANCE_CHECKS.UNDERWRITING_REQUEST_ID → ID
    ├── IDMATCH_RESULTS.UNDERWRITING_REQUEST_ID → ID
    ├── UNDERWRITING_VENDOR_RESULTS.UNDERWRITING_REQUEST_ID → ID
    └── BENEFICIAL_OWNER_UNDERWRITING_REQUESTS.UNDERWRITING_REQUEST_ID → ID

IDMATCH_RESULTS
    └── IDMATCH_MATCHED_ATTRIBUTES.IDMATCH_RESULT_ID → ID

UNDERWRITING_VENDOR_RESULTS
    ├── MATCHED_ATTRIBUTES.UNDERWRITING_VENDOR_RESULT_ID → ID
    └── QUIZ_RESULTS.UNDERWRITING_VENDOR_RESULT_ID → ID
```

---

## Common Query Patterns

### Look Up Activation Flow by Merchant Token

```sql
SELECT
    AF.*,
    MA.RETRY_COUNT,
    MA.LAST_VARIANT_SEEN
FROM ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS MA
JOIN ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
    ON AF.ID = MA.CURRENT_ACTIVATION_FLOW_ID
WHERE MA.MERCHANT_TOKEN = '<merchant_token>'
```

### Full Onboarding Journey for a Merchant

```sql
SELECT
    AF.MERCHANT_TOKEN,
    AF.STATUS AS activation_status,
    AF.COUNTRY_CODE,
    AF.FLOW_NAME,
    UR.UNDERWRITING_STATE,
    UR.DECISION AS underwriting_decision,
    UR.VERIFICATION_STATE,
    UR.VERIFICATION_DECISION_STATUS,
    UR.VERIFICATION_DECISION_REASON,
    UR.ACTIVATION_DECISION,
    UR.ACTIVATION_STATE,
    AF.CREATED_AT AS activation_started,
    UR.ACTIVATION_DECISION_AT
FROM ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS MA
JOIN ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
    ON AF.ID = MA.CURRENT_ACTIVATION_FLOW_ID
LEFT JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
WHERE MA.MERCHANT_TOKEN = '<merchant_token>'
```

### Underwriting Decision Analysis (Last 7 Days)

```sql
SELECT
    UR.DECISION,
    UR.UNDERWRITING_STATE,
    UR.VERIFICATION_DECISION_STATUS,
    AF.COUNTRY_CODE,
    COUNT(*) AS cnt
FROM ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
WHERE AF.CREATED_AT >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY 1, 2, 3, 4
ORDER BY cnt DESC
```

### Identity Verification Status for a Merchant

```sql
SELECT
    AF.MERCHANT_TOKEN,
    UR.VERIFICATION_STATE,
    UR.VERIFICATION_DECISION_STATUS,
    UR.VERIFICATION_DECISION_REASON,
    IR.STATE AS idmatch_state,
    IR.TOTAL_QUESTION_COUNT,
    IR.CORRECT_QUESTION_COUNT,
    IR.RISK_SCORE,
    CC.CHECK_TYPE,
    CC.CHECK_RESULT
FROM ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS MA
JOIN ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
    ON AF.ID = MA.CURRENT_ACTIVATION_FLOW_ID
LEFT JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
LEFT JOIN ONBOARD.RAW_OLTP.IDMATCH_RESULTS IR
    ON IR.UNDERWRITING_REQUEST_ID = UR.ID
LEFT JOIN ONBOARD.RAW_OLTP.COMPLIANCE_CHECKS CC
    ON CC.UNDERWRITING_REQUEST_ID = UR.ID
WHERE MA.MERCHANT_TOKEN = '<merchant_token>'
```

### US Persona + Address Lookup

```sql
SELECT
    P.FIRST_NAME,
    P.LAST_NAME,
    P.PHONE_NUMBER,
    P.ACCOUNT_OWNER,
    A.ADDRESS_LINE_1,
    A.ADDRESS_LINE_2,
    A.CITY,
    A.STATE,
    A.POSTAL_CODE
FROM ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
JOIN ONBOARD.RAW_OLTP.US_PERSONAS P
    ON P.ID = AF.PERSONA_ID
LEFT JOIN ONBOARD.RAW_OLTP.US_ADDRESSES A
    ON A.PERSONA_ID = P.ID
WHERE AF.MERCHANT_TOKEN = '<merchant_token>'
    AND AF.PERSONA_TYPE = 'UsPersona'
```

### Compliance Check Results by Underwriting Request

```sql
SELECT
    AF.MERCHANT_TOKEN,
    CC.CHECK_TYPE,
    CC.CHECK_RESULT,
    CC.CREATED_AT
FROM ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
JOIN ONBOARD.RAW_OLTP.COMPLIANCE_CHECKS CC
    ON CC.UNDERWRITING_REQUEST_ID = UR.ID
WHERE AF.MERCHANT_TOKEN = '<merchant_token>'
ORDER BY CC.CREATED_AT
```

### IDMatch Attribute Match Details

```sql
SELECT
    AF.MERCHANT_TOKEN,
    IR.STATE AS idmatch_state,
    IR.RISK_SCORE,
    IMA.ATTRIBUTE_NAME,
    IMA.MATCHED
FROM ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
JOIN ONBOARD.RAW_OLTP.IDMATCH_RESULTS IR
    ON IR.UNDERWRITING_REQUEST_ID = UR.ID
JOIN ONBOARD.RAW_OLTP.IDMATCH_MATCHED_ATTRIBUTES IMA
    ON IMA.IDMATCH_RESULT_ID = IR.ID
WHERE AF.MERCHANT_TOKEN = '<merchant_token>'
```

### End-to-End: Merchant Activation Through Legal Entity Verification

This query spans both ONBOARD and LEGALENTITIES databases. See also `square-identity-verification-legalentities.md` for LEGALENTITIES-specific queries.

```sql
-- Full journey from ROSTER merchant to LEGALENTITIES verification
-- See roster-merchant-location-employee-lookups.md for ROSTER MERCHANT_TOKEN binary cast pattern
SELECT
    TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8') AS merchant_token,
    M.PRIMARY_NAME,
    AF.STATUS AS activation_status,
    AF.COUNTRY_CODE,
    UR.UNDERWRITING_STATE,
    UR.ACTIVATION_DECISION,
    SM.STRUCTURE_TOKEN,
    VD.STATUS AS verification_status,
    VD.REASON AS verification_reason,
    BD.LEGAL_NAME AS business_name,
    ID.GIVEN_NAME || ' ' || ID.FAMILY_NAME AS primary_individual
FROM ROSTER.RAW_OLTP.MERCHANTS M
JOIN ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS MA
    ON MA.MERCHANT_TOKEN = TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')
JOIN ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
    ON AF.ID = MA.CURRENT_ACTIVATION_FLOW_ID
LEFT JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
LEFT JOIN LEGALENTITIES.RAW_OLTP.STRUCTURE_MERCHANT SM
    ON SM.STRUCTURE_TOKEN = AF.STRUCTURE_TOKEN
LEFT JOIN LEGALENTITIES.RAW_OLTP.VERIFICATION_DECISIONS VD
    ON VD.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_BUSINESS_DATA BD
    ON BD.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
    AND BD.IS_ROOT = 1
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_NODE_RELATIONSHIP NR
    ON NR.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
    AND NR.IS_PRIMARY = 1
LEFT JOIN LEGALENTITIES.RAW_OLTP.LES_INDIVIDUAL_DATA ID
    ON ID.NODE_TOKEN = NR.CHILD_NODE_TOKEN
    AND ID.STRUCTURE_TOKEN = SM.STRUCTURE_TOKEN
WHERE TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8') = '<merchant_token>'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY SM.STRUCTURE_TOKEN
    ORDER BY VD.SEQUENCE DESC NULLS LAST
) = 1
```

### Join ONBOARD to ROSTER for Merchant Details

See `roster-merchant-location-employee-lookups.md` for the ROSTER binary cast pattern.

```sql
SELECT
    TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8') AS merchant_token,
    M.PRIMARY_NAME,
    AF.STATUS AS activation_status,
    AF.COUNTRY_CODE,
    UR.ACTIVATION_DECISION
FROM ROSTER.RAW_OLTP.MERCHANTS M
JOIN ONBOARD.RAW_OLTP.MERCHANT_ACTIVATIONS MA
    ON MA.MERCHANT_TOKEN = TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8')
JOIN ONBOARD.RAW_OLTP.ACTIVATION_FLOWS AF
    ON AF.ID = MA.CURRENT_ACTIVATION_FLOW_ID
LEFT JOIN ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS UR
    ON UR.ID = AF.UNDERWRITING_REQUEST_ID
WHERE TO_VARCHAR(M.MERCHANT_TOKEN, 'UTF-8') = '<merchant_token>'
```
