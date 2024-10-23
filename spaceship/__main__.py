from .prompts import system_prompt
from .agent import loop, Agent
from .actions import play, wait_and_thrust, has_landed, exit_game
from .landing_calc import calculate_landing


tools = {
    "wait_and_thrust": wait_and_thrust,
    "calculate_landing": calculate_landing,
    "has_landed": has_landed,
}


agent = Agent(system_prompt)
play()
loop(
    agent,
    tools,
    max_iterations=50,
    query="Land the spaceship. Always calculate next move  and then control the spaceship.",
)
exit_game()
