import subprocess
import os
import threading
from typing import Optional
import time
import json

import pyautogui


GAME_PATH = "/home/jiri-strouhal/Plocha/Generative AI/Controlled/spaceship"


def _start_game():
    subprocess.run(["python3", os.path.join(GAME_PATH, "game", "__main__.py")])


def hold(seconds: float, key: Optional[str] = None):
    if key=="forward":
        key="up"
    _hold(seconds, key)


def game_running():
    return _game_thread.is_alive()


def _read_state() -> None | list:
    file_path = os.path.join(GAME_PATH, "game", "current_state.json")
    try:
        with open(file_path, "r") as file:
            state = json.loads(file.read())
            return state
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception:
        raise Exception("Unknown error occurred while reading the current state.")


def read_state():
    state = _read_state()
    while not state:
        state = _read_state()
        time.sleep(0.01)
    return state


_game_thread = threading.Thread(target=_start_game)


def play():
    _game_thread.start()


def _hold(seconds: float, key: Optional[str] = None):
    if key:
        pyautogui.keyDown(key)
    time.sleep(seconds)
    if key:
        pyautogui.keyUp(key)

