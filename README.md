# http-hid-keyboard

Use a Raspberry Pi as a USB keyboard controlled through HTTP requests. We use this project to control a Siemens ACUSON SC2000 ultrasound machine by emulating a keyboard/footswitch. Currently, only predefined actions/keypresses can be triggered.

We use a Raspberry Pi 3 A+ with Raspberry Pi OS, but any Raspberry Pi with USB OTG support should work.

## Installation

```bash
sudo ./install.sh
```

will set the appropriate boot options for USB OTG and install a `usb-gadget.service` and `hid-webserver.service` systemd service. Reboot the Raspberry Pi after installation.

## Usage

Test if keypresses can be issued:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"action": "ping"}' http://localhost:8080
```

You can define an actions in `main.py` and send them via HTTP POST requests to the webserver:

```bash
sudo systemctl restart hid-webserver
curl -X POST -H "Content-Type: application/json" -d '{"action": "save_recording"}' http://localhost:8080
```
