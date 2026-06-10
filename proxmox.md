# Running AstroLive in a Proxmox LXC (no Docker)

## 1. Create the LXC

Use a **Debian 12** or **Ubuntu 24.04** template. Recommended specs:
- 1 CPU core, 512 MB RAM (increase to 1 GB if using camera image processing)
- 4 GB disk
- Network: bridge to your LAN (needs access to your ASCOM Remote host and MQTT broker)

If you mount a FITS directory from the Proxmox host (for `camerafile`), add a bind mount in `/etc/pve/lxc/<CTID>.conf`:

```
mp0: /path/on/proxmox/fits,mp=/fits,ro=1
```

---

## 2. Install dependencies inside the container

```bash
apt update && apt install -y python3 python3-pip python3-venv git \
    libgl1 libglib2.0-0
```

> `libgl1` and `libglib2.0-0` are required by `opencv-python-headless`. Without them the import will fail.

---

## 3. Clone and install AstroLive

```bash
git clone https://github.com/mawinkler/astrolive.git /opt/astrolive
cd /opt/astrolive
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Configure

```bash
cp astrolive/default.cfg.yaml.sample astrolive.cfg.yaml
# Edit astrolive.cfg.yaml — set ASCOM Remote address, MQTT broker, and devices
```

The config is auto-discovered from `./astrolive.cfg.yaml` (current working directory) or `~/astrolive.cfg.yaml`.

---

## 5. Run as a systemd service

Create `/etc/systemd/system/astrolive.service`:

```ini
[Unit]
Description=AstroLive ALPACA-to-MQTT bridge
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/astrolive
ExecStart=/opt/astrolive/.venv/bin/python run.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable --now astrolive
journalctl -fu astrolive   # follow logs
```

---

## Notes

- **ASCOM Remote** runs on your Windows imaging PC — the LXC only needs TCP access to its port (default `11111`).
- **MQTT broker** (e.g. Mosquitto) can run on Proxmox itself or in another container; configure its address in `astrolive.cfg.yaml`.
- If you are not using the `camerafile` device type, skip the bind mount entirely.
- `Restart=on-failure` with `RestartSec=10` complements the 30-second health-check reconnect loop built into `run.py`.
