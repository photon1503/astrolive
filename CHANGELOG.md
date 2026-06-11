# [0.9](https://github.com/mawinkler/astrolive/compare/v0.7...v0.9) (2026-06-11)

### Fixes

- Fixed dome device thread dying permanently when the driver does not implement the optional `altitude` or `azimuth` properties. Unsupported optional dome properties now publish `null` instead of raising an unhandled `AlpacaError` that terminated the MQTT thread.
- Fixed the same class of bug for telescope optional properties (`declinationrate`, `guideratedeclination`, `rightascensionrate`, `guideraterightascension`, `sideofpier`, `siteelevation`, `sitelatitude`, `sitelongitude`) and rotator `mechanicalposition`. Drivers that do not implement these no longer kill the device thread.
- Fixed `CameraFile` accessing FITS header data after the `fits.open()` context manager had already closed the file handle.
- Fixed `Camera._get_imagedata()` using a hardcoded Alpaca URL (`192.168.1.233:11111/camera/1`). Camera image requests now use the configured component endpoint and device number.
- Fixed `sleep(30)` in the main supervisor loop using blocking `time.sleep()` inside `async def main()`, which stalled the entire asyncio event loop and prevented polling at the intervals configured per device in YAML.
- Fixed `sleep(3)` thread-stagger delay in `client.py` `start_monitoring()` also using blocking `time.sleep()` inside an async method.
- Fixed `sleep(0.1)` in `mqtthandler.py` `MqttHandler.looper()` using blocking `time.sleep()` inside an `async` function.
- All nine device `publish_loop()` methods (`Telescope`, `Camera`, `CameraFile`, `Focuser`, `Switch`, `FilterWheel`, `Dome`, `Rotator`, `SafetyMonitor`) previously exited permanently on `RequestConnectionError` or `DeviceResponseError`. They now retry after `interval` seconds, surviving transient endpoint outages without requiring the supervisor to recreate threads.
- Added missing Focuser `temperature` property publishing to MQTT state, including Home Assistant autodiscovery metadata (`temperature` sensor in `°C`).
- Added full Alpaca `ObservingConditions` device support (component kind `observingconditions`) with MQTT publishing for weather and sky sensors.

### Changes

- Replaced all blocking `time.sleep()` calls with `await asyncio.sleep()` throughout `run.py`, `client.py`, `mqtthandler.py`, and all device `publish_loop()` methods. Removed `from time import sleep` imports accordingly.
- Replaced `sys.exit(0)` at the end of `publish_loop()` methods with a plain `return`.
- Added `check_interval` property to `AstroLive` client, read from `observatory.check_interval` in the YAML config (default: `10` seconds). The main supervisor loop now sleeps for this configurable interval instead of the previous hardcoded 30 seconds.
- Downgraded log level for transient endpoint failures in `publish_loop()` from `ERROR` to `WARNING` to reflect that these are now retried rather than fatal.
- Removed duplicate `logging.basicConfig()` call in `client.py` (superseded by the one in `run.py`).
- Removed unused `from tokenize import String` import in `client.py`.
- Added recursive config validation for endpoint `address` values (must be valid `http://` or `https://` URLs).
- Updated configuration and README guidance for per-device endpoint routing: direct Alpaca endpoints per device are supported, with ASCOM Remote used only where needed by configuration.
- Added Home Assistant entity definitions and MQTT connector wiring for `observingconditions` sensors (cloud cover, dew point, humidity, pressure, rain rate, sky brightness, sky quality, sky temperature, star distance, temperature, wind direction, wind gust, wind speed).

# [0.7](https://github.com/mawinkler/astrolive/compare/v0.6...v0.7) (2025-04-12)

I am working on making the reconnects more reliable when the observatory is temporarily unavailable.

In the meantime, AstroLive has now implemented PixInsight's AutoStretch!

### Features

- Implemented PixInsights ScreenTransferFunction Autostretch. Stretching method is configured in `const.py` and not yet configurable in `config.yaml`.

# [0.6](https://github.com/mawinkler/astrolive/compare/v0.5...v0.6) (2024-11-17)

### Changes

- Bump dependencies to current versions.
- Added support for MQTTv5.

### Fixes

- Fixed an uncached error that occurred when the filter wheel is inaccessible.

# [0.5](https://github.com/mawinkler/astrolive/compare/v0.4...v0.5) (2023-10-13)

### Features

- Adhere to Home Assistant 2023.9 device and entity naming conventions.
- Fixed object coordinates in camera file. Thanks to @zdesignstudio.

# [0.4](https://github.com/mawinkler/astrolive/compare/v0.3...v0.4) (2023-05-28)

### Features

- Upgraaded dependencies
- Finally got config entries retained
- Code cleanup
- Fix for Home Assisdtant 2023.5 (unit of measurement)

# [0.3](https://github.com/mawinkler/astrolive/compare/v0.2...v0.3) (2023-02-27)

### Features

- Fix to enable different configurations.

# [0.2](https://github.com/mawinkler/astrolive/compare/v0.1...v0.2) (2023-01-28)

### Features

- Added support for filter wheel, dome, rotator, and safetymonitor

# [0.1](https://github.com/mawinkler/astrolive/releases/tag/v0.1) (2022-08-04)

### Initial Release

- The following components are supported:
  - Telescope
  - Camera
  - Camera via File
  - Focuser
  - Switch
