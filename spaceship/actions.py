import subprocess
import os
import threading
from typing import Optional
import time
import json
import datetime

import dotenv
import pyautogui  # type: ignore


try:
    GAME_PATH = dotenv.dotenv_values()["SPACESHIP_GAME_PATH"]
except Exception:
    print("The GAME_PATH environment variable is not set.")
    exit(1)


assert GAME_PATH is not None
GAME_SCRIPT_PATH = os.path.join(GAME_PATH, "game", "__main__.py")
GAME_SPACESHIP_STATE_PATH = os.path.join(GAME_PATH, "game", "state.json")
NOTES_FILE_NAME = "notes.txt"


def _start_game():
    subprocess.run(["python3", GAME_SCRIPT_PATH])


_game_thread = threading.Thread(target=_start_game)


def is_game_running():
    return _game_thread.is_alive()


def read_state() -> str:
    return _read_state()


def play():
    global _start_time, _game_thread
    _start_time = datetime.datetime.now()
    _game_thread.start()


def exit_game():
    pyautogui.keyDown("esc")
    time.sleep(0.1)
    pyautogui.keyUp("esc")


def read_notes() -> str:
    if os.path.isfile(os.path.join(os.path.dirname(__file__), NOTES_FILE_NAME)):
        with open(os.path.join(os.path.dirname(__file__), NOTES_FILE_NAME), "r") as file:
            return file.read()
    else:
        return ""


def update_notes(notes: str):
    with open(os.path.join(os.path.dirname(__file__), NOTES_FILE_NAME), "w") as file:
        file.write(notes)


def wait(seconds: float) -> str:
    """Do nothing for a given time in seconds.

    Returns in information string.
    """
    print("Waiting for", seconds, "seconds.")
    _hold(seconds)
    return "Waited for " + str(seconds) + " seconds."


def rotate(old_angle: float, new_angle: float, rotation_speed: float):
    delta_angle = new_angle - old_angle
    if delta_angle > 0:
        _hold(delta_angle / rotation_speed, "left")
    else:
        _hold(-delta_angle / rotation_speed, "right")


def thrust(seconds: float) -> str:
    """Thrust for a given number of seconds.

    Returns in information string.
    """
    print("Thrusting for", seconds, "seconds.")
    _hold(seconds, "up")
    return "Thrusted for " + str(seconds) + " seconds."


def _hold(seconds: float, key: Optional[str] = None):
    if key:
        pyautogui.keyDown(key)
    time.sleep(seconds)
    if key:
        pyautogui.keyUp(key)


def _read_state() -> str:
    try:
        with open(GAME_SPACESHIP_STATE_PATH, "r") as file:
            state = file.read()
            return state
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""
    except Exception:
        raise Exception("Unknown error occurred while reading the current state.")
