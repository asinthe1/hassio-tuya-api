# Tuya API Add-on for Home Assistant

This add-on fetches device logs (e.g., "Once Charge Energy") from the Tuya Cloud API and exposes them to Home Assistant via a REST sensor.

## Installation

1. Add the repository to Home Assistant:
   - Go to **Settings &gt; Add-ons &gt; Add-on Store**.
   - Click the three-dot menu, select **Repositories**, and add: `https://github.com/yourusername/hassio-tuya-api`.
2. Install the **Tuya API Add-on** from the Add-on Store.
3. Configure the add-on:
   - `tuya_csrf_token`: CSRF token from Tuya API (e.g., `Ukn5tGDO-aordArsw1oawb6jjFKKqEt4p0rw`).
   - `tuya_cookies`: Cookie string from Tuya API request.
   - `tuya_project_code`: Project code (e.g., `p1675001337643t83pqd`).
   - `tuya_source_id`: Source ID (e.g., `eu1648665352810qHhgv`).
   - `tuya_device_id`: Device ID (e.g., `bf01cc72031275fbe8pl7a`).
   - `tuya_region`: Region (e.g., `EU`).
   - `poll_interval`: Polling interval in seconds (e.g., `300` for 5 minutes).
4. Start the add-on.

## Home Assistant Integration

Add a REST sensor to your `configuration.yaml`:

```yaml
sensor:
  - platform: rest
    name: Tuya Charge Energy
    resource: http://<ADDON_IP>:8000/data
    value_template: "{{ value_json[0].eventDetail }}"
    json_attributes:
      - eventTimeStr
      - eventType
      - requestFrom
```

Replace `<ADDON_IP>` with the IP address of your Home Assistant instance or the add-on container.

## Displaying in Lovelace

Use a **Sensor Card** or **Entities Card** to display the sensor data in the Lovelace UI.

## Notes

- The add-on assumes static CSRF tokens and cookies. For production, implement Tuya’s OAuth flow for dynamic authentication.
- The sensor shows the latest "Once Charge Energy" value. Modify the `value_template` to extract other fields if needed.
- Logs are available in the add-on’s log viewer for debugging.

## Repository

https://github.com/yourusername/hassio-tuya-api