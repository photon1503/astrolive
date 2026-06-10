# [0.8](https://github.com/mawinkler/astrolive/compare/v0.7...v0.8) (2026-06-10)

### Fixes

- Fixed dome device thread dying permanently when the driver does not implement the optional `altitude` or `azimuth` properties. Unsupported optional dome properties now publish `null` instead of raising an unhandled `AlpacaError` that terminated the MQTT thread.
- Fixed the same class of bug for telescope optional properties (`declinationrate`, `guideratedeclination`, `rightascensionrate`, `guideraterightascension`, `sideofpier`, `siteelevation`, `sitelatitude`, `sitelongitude`) and rotator `mechanicalposition`. Drivers that do not implement these no longer kill the device thread.
- Fixed `CameraFile` accessing FITS header data after the `fits.open()` context manager had already closed the file handle.
- Fixed `Camera._get_imagedata()` using a hardcoded Alpaca URL (`192.168.1.233:11111/camera/1`). Camera image requests now use the configured component endpoint and device number.

### Changes

- Replaced blocking `time.sleep()` with `await asyncio.sleep()` in all device `publish_loop()` methods, allowing the async event loop to remain responsive during polling intervals.
- Replaced `sys.exit(0)` at the end of `publish_loop()` methods with a plain `return`.
- Removed duplicate `logging.basicConfig()` call in `client.py` (superseded by the one in `run.py`).
- Removed unused `from tokenize import String` import in `client.py`.
- Added recursive config validation for endpoint `address` values (must be valid `http://` or `https://` URLs).
- Updated configuration and README guidance for per-device endpoint routing: direct Alpaca endpoints per device are supported, with ASCOM Remote used only where needed by configuration.

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
