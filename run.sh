#!/usr/bin/env bash
if ! test "/dev/hidg0"; then
	sudo ./install.sh
fi

python3 application/main.py