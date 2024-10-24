from typing import Callable

from prompts import system_prompt
from agent import loop, Agent
from actions import play, thrust, read_state, rotate, wait, exit_game, read_notes, update_notes


tools: dict[str, Callable] = {
    "thrust": thrust,
    "read_state": read_state,
    "read_notes": read_notes,
    "update_notes": update_notes,
    "rotate": rotate,
    "wait": wait,
}


agent = Agent(system_prompt)
play()
loop(
    agent,
    tools,
    max_iterations=50,
    query="Land the spaceship. Always calculate next move and then control the spaceship.",
)
exit_game()
