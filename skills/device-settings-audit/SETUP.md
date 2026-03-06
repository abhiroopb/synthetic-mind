# Setup: Device Profile Audit Skill

## Prerequisites

### Required Capabilities

You need capabilities for the `device-settings` app in Square's Registry system.

1. Go to https://registry.internal.example.com/applications/device-settings
2. Request "Developer" or "Admin" access
3. Wait for approval (typically automatic for Square employees)

### VPN Connection

Ensure you're connected to Square's VPN to access internal services.

### Command-Line Tools

- `sq` - Square's CLI tool (should be installed if you're working at Square)
- `jq` - JSON processor (optional, for parsing results)
  ```bash
  brew install jq
  ```

## Testing

### Test Merchants

Use test merchants with device profile history:
- Ask in #device-settings Slack channel for test merchant tokens
- Or use your own test merchant with device profiles

### Playpen Testing

To test with local code changes:

1. Start device-settings playpen:
   ```bash
   cd ~/Development/java/device-settings
   sq playpen sync
   ```

2. Use the playpen in curl commands:
   ```bash
   sq curl --playpen device-settings -L --post302 \
     'https://device-settings.stage.internal.example.com/_admin/rpc/call' \
     -H 'content-type: application/json' \
     --data-raw '{"service_name": "your-org.devicesettings.profiles.v2.service.DeviceProfileV2Service", "method_name": "AdminSearchDeviceProfileHistory", "json_body": "{\"merchant_id\":\"TEST_MERCHANT\",\"types\":[\"CREATE_DEVICE_PROFILE\"],\"limit\":10}"}'
   ```

## Environments

- **Staging**: `https://device-settings.stage.internal.example.com`
- **Production**: `https://device-settings.internal.example.com`

Always test in staging first before querying production data.

## Common Issues

### "Permission denied" error
You need to request capabilities for device-settings in Registry (see Prerequisites above).

### "Connection refused" error
Make sure you're connected to Square's VPN.

### "merchant_id is required" error
Check that the `json_body` field contains a valid `merchant_id` parameter.

## Getting Help

- **Slack**: #device-settings - Ask the device-settings team
- **Oncall**: Check Registry for device-settings oncall rotation
- **Documentation**: See SKILL.md for usage examples
