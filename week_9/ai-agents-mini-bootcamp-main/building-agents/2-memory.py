"""
Memory: Stores and retrieves relevant information across interactions.
This component maintains conversation history and context to enable coherent multi-turn interactions.

More info: https://platform.openai.com/docs/guides/conversation-state?api-mode=responses
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def ask_joke_without_memory():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Tell me a joke about programming"},
        ],
    )
    return response.choices[0].message.content


def ask_followup_without_memory():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "What was my previous question?"},
        ],
    )
    return response.choices[0].message.content


def ask_followup_with_memory(joke_response: str):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Tell me a joke about programming"},
            {"role": "assistant", "content": joke_response},
            {"role": "user", "content": "What was my previous question?"},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # First: Ask for a joke
    print("First: Ask for a joke")
    joke_response = ask_joke_without_memory()
    print(joke_response, "\n")

    # Second: Ask follow-up without memory (AI will be confused)
    print("Second: Ask follow-up without memory (AI will be confused)")
    confused_response = ask_followup_without_memory()
    print(confused_response, "\n")

    # Third: Ask follow-up with memory (AI will remember)
    print("Third: Ask follow-up with memory (AI will remember)")
    memory_response = ask_followup_with_memory(joke_response)
    print(memory_response)