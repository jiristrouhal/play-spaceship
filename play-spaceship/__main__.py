import os
import time

import openai  # type: ignore
from dotenv import load_dotenv

from .prompts import system_prompt
from .actions import play, hold, read_current_state, game_running


DT = 0.1


play()
time.sleep(0.5)


while game_running():
    hold(DT, "up")
    state = read_current_state()
    if state and not state.get("game-on", False):
        break

