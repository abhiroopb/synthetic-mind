---
name: sms
description: >
  Send and receive SMS messages via Twilio API. Used for text message
  notifications, forwarding important alerts, and two-way SMS communication.
---

# SMS Skill (Twilio)

Send and manage SMS messages using the Twilio API.

## Prerequisites

Set these environment variables (or in the amp-life-agent `.env`):
- `TWILIO_ACCOUNT_SID` — Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` — Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER` — Your Twilio phone number (e.g., +14155551234)
- `MY_PHONE_NUMBER` — Abhi's real phone number

## Sending an SMS

Use curl to send via Twilio REST API:

```powershell
$accountSid = $env:TWILIO_ACCOUNT_SID
$authToken = $env:TWILIO_AUTH_TOKEN
$from = $env:TWILIO_PHONE_NUMBER
$to = $env:MY_PHONE_NUMBER

$body = "Your message here"

$pair = "${accountSid}:${authToken}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)

Invoke-RestMethod -Uri "https://api.twilio.com/2010-04-01/Accounts/$accountSid/Messages.json" `
  -Method POST `
  -Headers @{ Authorization = "Basic $base64" } `
  -Body @{ To = $to; From = $from; Body = $body }
```

## Receiving SMS

To receive SMS, set up a Twilio webhook pointing to a publicly accessible endpoint.
For local development, use ngrok or a cloud function.

## Use Cases

- Forward urgent email summaries as SMS when WhatsApp is unavailable
- Send appointment reminders via text
- Alert on critical calendar events
- Two-factor notification backup channel

## Safety

- Never send SMS to numbers not explicitly approved by Abhi
- Rate limit: max 5 SMS per hour unless overridden
- Always include context about why the SMS was sent
