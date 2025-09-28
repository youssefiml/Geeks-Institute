"""
Intelligence: The "brain" that processes information and makes decisions using LLMs.
This component handles context understanding, instruction following, and response generation.

More info: https://platform.openai.com/docs/guides/text?api-mode=responses
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

def basic_intelligence(prompt: str) -> str:
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    result = basic_intelligence(prompt="What is artificial intelligence?")
    print("Basic Intelligence Output:")
    print(result)
