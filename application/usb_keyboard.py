import time

NULL_CHAR = chr(0)  # KEY_RESERVED
CTRL_CHAR = chr(1)  # KEY_LEFTCTRL
KEY_8 = chr(37)
KEY_9 = chr(38)
KEY_0 = chr(39)

# Foot peddle keys for Siemens SC2000 ultrasound machine (ctrl + key)
LEFT_PEDDLE = KEY_8
MIDDLE_PEDDLE = KEY_9
RIGHT_PEDDLE = KEY_0

# Our configuration of the ultrasound machine
REVIEW_KEY = LEFT_PEDDLE
FREEZE_KEY = MIDDLE_PEDDLE
SAVE_KEY = RIGHT_PEDDLE


def _write_report(report):
    with open("/dev/hidg0", "rb+") as fd:
        fd.write(report.encode())


def test():
    # Test if we can press keys
    _write_report(NULL_CHAR * 8)


def _press_peddle(peddle):
    # press and hold CTRL, otherwise the ultrasound machine won't recognize the CTRL + KEY combination
    _write_report(CTRL_CHAR + NULL_CHAR * 7)
    time.sleep(0.05)  # can't be too fast, our ultrasound system can't handle it

    # press CTRL + PEDDLE_KEY
    _write_report(CTRL_CHAR + NULL_CHAR + peddle + NULL_CHAR * 5)
    time.sleep(0.05)  # can't be too fast, our ultrasound system can't handle it

    # Release keys
    _write_report(NULL_CHAR * 8)


def freeze_and_save():
    _press_peddle(FREEZE_KEY)
    time.sleep(1)
    _press_peddle(SAVE_KEY)


def toggle_freeze():
    _press_peddle(FREEZE_KEY)


def toggle_review():
    _press_peddle(REVIEW_KEY)


def save_recording():
    _press_peddle(SAVE_KEY)
