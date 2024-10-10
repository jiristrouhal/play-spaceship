import os
import time

import openai  # type: ignore
from dotenv import load_dotenv

from prompts import system_prompt
from actions import play, hold, read_state, game_running
from json_helpers import extract_json_func


load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text_with_conversation(messages, model = "gpt-3.5-turbo"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content


available_actions = {
    "hold": hold
}


messages = [
    {"role": "user", "content": "Land the rocket."},
    {"role": "system", "content": system_prompt}
]


def get_orientation(angle):

    if -135 <= angle <= -45:
        return "right"
    elif -45 < angle <= 45:
        return "up"
    elif 45 < angle <= 135:
        return "left"
    else:
        return "down"



play()
time.sleep(0.5)


while game_running():
    response = generate_text_with_conversation(messages)

    print("Response: ", response)

    json_functions = extract_json_func(response)
    state = read_state()
    state["orientation"] = get_orientation(float(state["angle"]))
    if state and not state["running"]:
        hold(0.1, "esc")
        break
    function_result_message = f"Check: {state}"
    messages.append({"role": "system", "content": function_result_message})
    print("Check: ", function_result_message)

    if json_functions:
        if not "function_name" in json_functions[0] or not "function_params" in json_functions[0]:
            continue
        function_name = json_functions[0]["function_name"]
        function_params = json_functions[0]["function_params"]
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_params}")

        msg = f"Running {function_name} with params: {function_params}"
        print(msg)
        messages.append({"role": "system", "content": msg})
        action_function = available_actions[function_name]
        result = action_function(**function_params)
