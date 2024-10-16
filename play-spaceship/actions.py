import subprocess
import os
import threading
from typing import Optional
import time
import json
import datetime
import dataclasses

import pyautogui


GAME_PATH = "/home/jiri-strouhal/Plocha/Generative AI/Controlled/spaceship"


def _start_game():
    subprocess.run(["python3", os.path.join(GAME_PATH, "game", "__main__.py")])


_start_time = datetime.datetime.now()
_game_thread = threading.Thread(target=_start_game)


@dataclasses.dataclass
class State:
    vx: float
    vy: float
    x: float
    y: float
    mass: float
    fuel_mass: float
    fuel_consumption: float
    angle: float
    rotation_speed: float
    time: datetime.datetime
    thrust: float
    g: float
    time_slowdown: float


def game_running():
    return _game_thread.is_alive()


def read_state() -> State | None:
    global _start_time
    state = _read_state()
    while not state or not _read_time(state["time"]) or _read_time(state["time"]) < _start_time:
        state = _read_state()
        time.sleep(0.001)
    try:
        return State(
            vx=state["horizontal-velocity"],
            vy=state["vertical-velocity"],
            x=state["horizontal-position"],
            y=state["vertical-position"],
            mass=state["mass"],
            fuel_mass=state["fuel-mass"],
            fuel_consumption=state["fuel-consumption"],
            thrust=state["thrust"],
            angle=state["angle"],
            rotation_speed=state["rotation-speed"],
            time=datetime.datetime.strptime(state["time"], "%Y-%m-%d %H:%M:%S"),
            g=state["gravity"],
            time_slowdown=state["time-slowdown"]
        )
    except KeyError:
        return None


def play():
    global _start_time, _game_thread
    _start_time = datetime.datetime.now()
    _game_thread.start()


def exit_game():
    pyautogui.keyDown("esc")
    time.sleep(0.1)
    pyautogui.keyUp("esc")


def wait(seconds: float) -> str:
    """Do nothing for a given time in seconds.

    Returns in information string.
    """
    print("Waiting for", seconds, "seconds.")
    _hold(seconds)
    return "Waited for " + str(seconds) + " seconds."


def has_landed() -> bool:
    """Check if the spaceship has landed."""
    state = read_state()
    return state.y < 30


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


def wait_and_thrust(t_wait: float, t_burn: float) -> str:
    """Wait for a given time and then thrust for a given time.

    Returns in information string.
    """
    wait(t_wait-1)
    return thrust(t_burn)


def _hold(seconds: float, key: Optional[str] = None):
    if key:
        pyautogui.keyDown(key)
    time.sleep(seconds)
    if key:
        pyautogui.keyUp(key)


def _read_state() -> None | list:
    file_path = os.path.join(GAME_PATH, "game", "state.json")
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


def _read_time(date_str: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Error while parsing date string: ", date_str)
        return None

