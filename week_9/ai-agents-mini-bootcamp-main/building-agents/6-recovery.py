"""
Recovery: Manages failures and exceptions gracefully in agent workflows.
This component implements retry logic, fallback processes, and error handling to ensure system resilience.
"""

from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

class UserInfo(BaseModel):
    name: str
    email: str
    age: Optional[int] = None  # Optional field


def resilient_intelligence(prompt: str) -> str:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    # Get structured output
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Extract user information from the text."},
            {"role": "user", "content": prompt},
        ],
        response_format=UserInfo,
        temperature=0.0,
    )

    user_data = response.choices[0].message.parsed.model_dump()

    try:
        # Try to access age field and check if it's valid
        age = user_data["age"]
        if age is None:
            raise ValueError("Age is None")
        age_info = f"User is {age} years old"
        return age_info

    except (KeyError, TypeError, ValueError):
        print("❌ Age not available, using fallback info...")

        # Fallback to available information
        return f"User {user_data['name']} has email {user_data['email']}"


if __name__ == "__main__":
    result = resilient_intelligence(
        "My name is John Smith and my email is john@example.com"
    )
    print("Recovery Output:")
    print(result)