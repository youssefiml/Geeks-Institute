import os
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pymongo import MongoClient
import json

load_dotenv()


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
# Connect to MongoDB
client_mongo = MongoClient(MONGODB_URI)
db = client_mongo[DB_NAME]
collection = db[COLLECTION_NAME]

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

model = MODEL

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

# --------------------------------------------------------------
# Define the knowledge base retrieval tool
# --------------------------------------------------------------


def search_kb(question: str) -> list[dict]:
    """
    Search the MongoDB knowledge base for relevant records.
    (This is a simple implementation that returns all records)
    """
    records = list(collection.find({}))

    clean_records = [
        {"id": str(record["_id"]),"question": record["question"],"answer": record["answer"]} for record in records
    ]

    return clean_records


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

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

# completion.model_dump()

# --------------------------------------------------------------
# Step 3: Execute search_kb function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    )

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class KBResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    source: str = Field(description="The full id of the answer record.")


completion_2 = client.beta.chat.completions.parse(
    model=model,
    messages=messages,
    tools=tools,
    response_format=KBResponse,
)

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed

print("Final response: ", final_response.answer)
print("Final response source: ", final_response.source)

# --------------------------------------------------------------
# Question that doesn't trigger the tool
# --------------------------------------------------------------

# messages = [
#     {"role": "system", "content": system_prompt},
#     {"role": "user", "content": "What is the weather in Tokyo?"},
# ]

# completion_3 = client.beta.chat.completions.parse(
#     model=model,
#     messages=messages,
#     tools=tools,
# )

# print("Completion 3: ", completion_3.choices[0].message.content)

# ! Close MongoDB connection when done
client_mongo.close()
