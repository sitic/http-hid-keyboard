#!/usr/bin/env bash

USERNAME=1000  # Change this to the username of the user you want to run the webserver as, default it user with id 1000

set -x # Echo commands to stdout.
set -e # Exit on first error.
set -u # Treat undefined environment variables as errors.

dt=$(cat /boot/config.txt | grep "dtoverlay=dwc2,dr_mode=peripheral")
if [ "$dt" != "dtoverlay=dwc2,dr_mode=peripheral" ]; then
    echo "dtoverlay=dwc2" >> /boot/config.txt
    echo "\n\nReboot system to enable changes!\n"
fi
# To see if the line needs to be appended
mod=$(cat /boot/cmdline.txt | grep -o "modules-load=dwc2,g_hid")
if [ "$mod" != "modules-load=dwc2,g_hid" ]; then
    sed -i '1s/$/ modules-load=dwc2,g_hid/' /boot/cmdline.txt
    echo "\nReboot system to enable changes!\n"
fi

chmod +x enable-rpi-hid.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cat << EOF > /etc/systemd/system/usb-gadget.service
[Unit]
Description=Create virtual keyboard USB gadget
After=syslog.target

[Service]
Type=oneshot
User=root
ExecStart=$SCRIPT_DIR/enable-rpi-hid.sh

[Install]
WantedBy=local-fs.target
EOF

cat << EOF > /etc/systemd/system/hid-webserver.service
[Unit]
Description=Keyboard controller web service
After=network.target usb-gadget.service
Wants=usb-gadget.service

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
Restart=on-failure
User=$USERNAME
Environment=PYTHONUNBUFFERED=1
ExecStart=$SCRIPT_DIR/application/main.py
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable usb-gadget.service
systemctl enable hid-webserver.service
