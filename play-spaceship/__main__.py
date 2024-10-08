import os
import time

import openai  # type: ignore
from dotenv import load_dotenv

from prompts import system_prompt
from actions import play, hold, read_state, game_running
from json_helpers import extract_json_func


DT = 0.1


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
    {"role": "system", "content": system_prompt}
]


play()
time.sleep(0.5)
while game_running():
    response = generate_text_with_conversation(messages)
    json_functions = extract_json_func(response)
    state = read_state()
    function_result_message = f"Check: {state}"
    messages.append({"role": "system", "content": function_result_message})
    print("Check: ", function_result_message)

    if json_functions:
        function_name = json_functions[0]["function_name"]
        function_params = json_functions[0]["function_params"]
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_params}")
        print(f"Running {function_name} with params: {function_params}")
        action_function = available_actions[function_name]
        result = action_function(**function_params)