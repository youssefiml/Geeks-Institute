import json
from pymongo import MongoClient

client = MongoClient("MONGO_URI")


db = client["hr_agent"]


candidates_col = db["candidates"]
jobs_col = db["jobs"]

def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_data():

    candidates = load_json_file("data/candidates.json")
    jobs = load_json_file("data/jobs.json")


    candidates_col.delete_many({})
    jobs_col.delete_many({})


    candidates_col.insert_many(candidates)
    jobs_col.insert_many(jobs)

    print(f"✅ Inserted {len(candidates)} candidates و {len(jobs)} jobs in MongoDB")

if __name__ == "__main__":
    insert_data()