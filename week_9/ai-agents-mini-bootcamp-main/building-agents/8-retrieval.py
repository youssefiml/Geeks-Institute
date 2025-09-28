import json
import os

from openai import OpenAI
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

# --------------------------------------------------------------
# Define the knowledge base retrieval tool
# --------------------------------------------------------------


def search_kb(question: str):
    """
    Load the whole knowledge base from the JSON file.
    (This is a mock function for demonstration purposes, we don't search)
    """
    print(f"🔍 Searching knowledge base for: '{question}'")
    with open("retrieval/kb.json", "r") as f:
        kb_data = json.load(f)
    print(f"📚 Found {len(kb_data['records'])} records in knowledge base")
    return kb_data


# --------------------------------------------------------------
# Step 1: Call model with search_kb tool defined
# --------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Get the answer to the user's question from the knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful assistant that answers questions from the knowledge base about our e-commerce store."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the return policy?"},
]

print("Step 1: Calling AI with tools available...")
print(f"User question: '{messages[1]['content']}'")

completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

response_message = completion.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    print(f" AI decided to use {len(tool_calls)} tool(s)")
    for i, tool_call in enumerate(tool_calls, 1):
        print(f"   Tool {i}: {tool_call.function.name}")
else:
    print("AI responded without using tools")

# --------------------------------------------------------------
# Step 3: Execute search_kb function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)
    raise ValueError(f"Unknown function: {name}")


if tool_calls:
    # Add the assistant's response to messages
    messages.append(response_message)
    
    for tool_call in tool_calls:
        print(f"\n Executing function: {tool_call.function.name}")
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"   Arguments: {args}")
        
        result = call_function(name, args)
        
        # Add function result to messages
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": name,
            "content": json.dumps(result)
        })
        print(f" Function executed successfully")

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class KBResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    source: int = Field(description="The record id of the answer.")


if tool_calls:
    print(f"\n Step 4: Getting final response with retrieved data...")
    
    completion_2 = client.beta.chat.completions.parse(
        model=MODEL,
        messages=messages,
        tools=tools,
        response_format=KBResponse,
    )

    # --------------------------------------------------------------
    # Step 5: Check model response
    # --------------------------------------------------------------

    print(f"\n Step 5: Final structured response received")
    final_response = completion_2.choices[0].message.parsed
    
    print(f"\n FINAL ANSWER:")
    print(f"Answer: {final_response.answer}")
    print(f"Source Record ID: {final_response.source}")
else:
    print(f"\n AI responded directly without using tools:")
    print(f"Response: {response_message.content}")

# --------------------------------------------------------------
# Question that doesn't trigger the tool
# --------------------------------------------------------------

print(f"\n" + "="*60)
print(f" TESTING: Question that should NOT trigger knowledge base search")
print(f"="*60)

messages_2 = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the weather in Tokyo?"},
]

print(f"User question: '{messages_2[1]['content']}'")
print(f" Calling AI to see if it uses tools...")

completion_3 = client.chat.completions.create(
    model=MODEL,
    messages=messages_2,
    tools=tools,
    tool_choice="auto"
)

response_3 = completion_3.choices[0].message
if response_3.tool_calls:
    print(f" AI decided to use tools (unexpected for weather question)")
    for tool_call in response_3.tool_calls:
        print(f"   Tool: {tool_call.function.name}")
else:
    print(f" AI responded directly without using tools (as expected)")
    print(f"Response: {response_3.content}")

print(f"\n Retrieval example completed!")