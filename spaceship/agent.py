import os
import re
import json
from typing import Callable

import openai
import dotenv


dotenv.load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Agent:
    def __init__(self, system_prompt: str = "") -> None:
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system = system_prompt
        self.messages: list = []
        if self.system:
            self.messages.append({"role": "system", "content": system_prompt})

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        return completion.choices[0].message.content


def loop(agent: Agent, tools: dict[str, Callable], max_iterations: int = 20, query: str = ""):
    next_prompt = query
    i = 0
    while i < max_iterations:
        i += 1
        result = agent(next_prompt)
        print(result)
        if "PAUSE" in result or "Action" in result:
            next_prompt = _run_action_and_get_observation(tools, result)
        elif "Answer" in result:
            break
    if i == max_iterations:
        print("Max iterations reached. Ending the agent's loop.")


def _run_action_and_get_observation(tools: dict[str, Callable], action_prompt: str) -> str:
    action = re.findall(r"Action: ([a-z_]+): (\{.*\})", action_prompt, re.IGNORECASE)
    if isinstance(action, list) and len(action) == 1:
        action.append("{}")
    if not action:
        next_prompt = "Observation: Unsuccesful action call"
    else:
        chosen_tool = action[0][0]
        args = json.loads(action[0][1])
        if chosen_tool in tools:
            result_tool = tools[chosen_tool](**args)
            next_prompt = f"Observation: {result_tool}"
        else:
            next_prompt = "Observation: Tool not found"
    return next_prompt
