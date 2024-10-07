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
    if key:
        pyautogui.keyDown(key)
    time.sleep(seconds)
    if key:
        pyautogui.keyUp(key)


def game_running():
    return _game_thread.is_alive()


def read_current_state() -> None | dict:
    file_path = os.path.join(GAME_PATH, "game", "current_state.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return json.loads(file.read())


_game_thread = threading.Thread(target=_start_game)


def play():
    _game_thread.start()




