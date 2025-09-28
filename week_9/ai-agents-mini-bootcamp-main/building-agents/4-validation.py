"""
Validation: Ensures LLM outputs match predefined data schemas.
This component provides schema validation and structured data parsing to guarantee consistent data formats for downstream code.

More info: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses
"""

from openai import OpenAI
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

class TaskResult(BaseModel):
    """
    More info: https://docs.pydantic.dev
    """

    task: str = Field(description="The task to be completed.")
    completed: bool = Field(description="Whether the task is completed.")
    priority: Literal["low", "medium", "high"] = Field(description="The priority of the task.")


def structured_intelligence(prompt: str) -> TaskResult:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract task information from the user input.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format=TaskResult,
    )
    return response.choices[0].message.parsed


if __name__ == "__main__":
    result = structured_intelligence(
        "I need to complete the project presentation by Friday, it's high priority"
    )
    print("Structured Output:")
    print(result.model_dump_json(indent=2))
    print(f"Extracted task: {result.task}")