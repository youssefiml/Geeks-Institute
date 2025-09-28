"""
Feedback: Provides strategic points where human judgement is required.
This component implements approval workflows and human-in-the-loop processes for high-risk decisions or complex judgments.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

def get_human_approval(content: str) -> bool:
    print(f"Generated content:\n{content}\n")
    response = input("Approve this? (y/n): ")
    return response.lower().startswith("y")


def intelligence_with_human_feedback(prompt: str) -> None:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    attempt = 1
    while True:
        print(f"\n--- Attempt {attempt} ---")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        draft_response = response.choices[0].message.content

        if get_human_approval(draft_response):
            print("✅ Final answer approved!")
            break
        else:
            print("❌ Answer not approved, generating a new one...")
            attempt += 1


if __name__ == "__main__":
    intelligence_with_human_feedback("Write a very short poem about technology")