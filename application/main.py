#!/usr/bin/env python3

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime

from webserver import WebServer
import usb_keyboard as keyboard

SERVER_ADDRESS = ""  # Address to listen on, empty string means all available addresses
SERVER_PORT = 8080  # Port to listen on
AUTHORIZATION_TOKEN = ""  # If set authenticate requests by comparing with `Authorization` header value, e.g. "Bearer abcdefg"
LOG_LEVEL = logging.INFO

ACTIONS = {
    "ping": lambda: None,  # do nothing, just check if web server is alive
    "test": keyboard.test,  # test if key press works
    
    # Keyboard actions for Siemens SC2000 ultrasound machine
    "toggle_freeze": keyboard.toggle_freeze,  # left foot peddle
    "toggle_review": keyboard.toggle_review,  # right foot peddle
    "save_recording": keyboard.save_recording,  # middle foot peddle
    "freeze_and_save": keyboard.freeze_and_save,  # assumes that we aren't in freeze mode
}


def setup_logging():
    logdir = Path(__file__).parent.parent
    logfile = logdir / f"main.log.{datetime.today().strftime('%Y%m%d')}.txt"

    fileloghandler = TimedRotatingFileHandler(logfile, when="midnight", interval=1)
    fileloghandler.suffix = "%Y%m%d"
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            fileloghandler,
        ],
    )
    logging.getLogger("").info(f"Saving log to file '{logfile.absolute()}'")


def main():
    setup_logging()

    webserver = WebServer(
        ACTIONS, addr=SERVER_ADDRESS, port=SERVER_PORT, auth_token=AUTHORIZATION_TOKEN
    )
    webserver.run()


if __name__ == "__main__":
    main()
