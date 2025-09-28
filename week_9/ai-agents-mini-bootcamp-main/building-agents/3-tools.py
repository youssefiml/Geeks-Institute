"""
Tools: Enables agents to execute specific actions in external systems.
This component provides the capability to make API calls, database updates, file operations, and other practical actions.


More info: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
"""

import json
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]["temperature_2m"]


def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    raise ValueError(f"Unknown function: {name}")


def intelligence_with_tools(prompt: str) -> str:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for provided coordinates in celsius.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                    },
                    "required": ["latitude", "longitude"],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        }
    ]

    messages = [{"role": "user", "content": prompt}]

    # Step 1: Call model with tools
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 2: Handle function calls
    if tool_calls:
        # Add the assistant's response to messages
        messages.append(response_message)
        
        # Step 3: Execute each function call
        for tool_call in tool_calls:
            # Execute function
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            result = call_function(function_name, function_args)

            # Step 4: Add function result to messages
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(result),
                }
            )

        # Step 5: Get final response with function results
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

        return final_response.choices[0].message.content
    else:
        # No function calls, return the original response
        return response_message.content


if __name__ == "__main__":
    result = intelligence_with_tools(prompt="What's the weather like in Casablanca today?")
    print("Tool Calling Output:")
    print(result)