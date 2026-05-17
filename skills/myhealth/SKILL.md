---
name: myhealth
description: >
  Book and manage appointments on Sutter Health MyHealth Online portal.
  Uses browser automation via Playwright MCP to interact with the patient portal.
---

# MyHealth Online Skill (Sutter Health)

Manage healthcare appointments on Sutter Health's MyHealth Online portal using browser automation.

## Portal URL

- Login: https://www.sutterhealth.org (click "My Health Online" or "Sign in to My Health Online")
- Direct: https://myhealth.sutterhealth.org

## Capabilities

1. **Book appointments** — Search for available slots by doctor, specialty, or location
2. **View upcoming appointments** — Check scheduled visits
3. **Cancel/reschedule** — Modify existing appointments
4. **Message doctor** — Send messages through the portal
5. **View test results** — Check lab results and reports

## Workflow: Booking an Appointment

1. Navigate to the MyHealth portal login page
2. Log in with saved credentials (ask Abhi if not saved)
3. Navigate to "Schedule an Appointment" or equivalent
4. Search by specialty, doctor name, or reason for visit
5. Find available time slots matching Abhi's preferences
6. **PRESENT OPTIONS TO ABHI** — never auto-book
7. After Abhi confirms a slot, complete the booking
8. Add the appointment to Google Calendar (if gcal skill available)
9. Set a reminder in the todo list

## Safety Rules — MANDATORY

⚠️ **NEVER book an appointment without Abhi's explicit confirmation** ⚠️

- Always present available slots and wait for Abhi to choose
- Never cancel or reschedule without asking first
- Never share health information in responses that could be forwarded
- If login fails, ask Abhi to log in manually — do NOT retry with wrong credentials
- Always close the browser session after completing the task

## Tips

- Abhi's timezone is America/Los_Angeles (Pacific)
- Prefer morning appointments unless Abhi says otherwise
- If multiple locations are available, prefer the closest one
- Always include the doctor's name, date, time, and location in the summary
