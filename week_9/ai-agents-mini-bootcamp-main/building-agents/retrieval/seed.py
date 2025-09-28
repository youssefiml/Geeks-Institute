import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
# Connect to MongoDB
client_mongo = MongoClient(MONGODB_URI)
db = client_mongo[DB_NAME]
collection = db[COLLECTION_NAME]

data = [
    {
        "question": "What is the return policy?",
        "answer": "Items can be returned within 30 days of purchase with original receipt. Refunds will be processed to the original payment method within 5-7 business days."
    },
    {
        "question": "Do you ship internationally?",
        "answer": "Yes, we ship to over 50 countries worldwide. International shipping typically takes 7-14 business days and costs vary by destination. Please note that customs fees may apply."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, Mastercard, American Express, PayPal, and Apple Pay. All payments are processed securely through our encrypted payment system."
    }

]

collection.insert_many(data)

# Close MongoDB connection when done
client_mongo.close()
