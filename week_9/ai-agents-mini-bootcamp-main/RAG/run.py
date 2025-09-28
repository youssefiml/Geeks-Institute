from vector import retriever

question = "what the reviews the quality of the pizza?"

print(f"🔍 Searching reviews for: '{question}'")
reviews = retriever.invoke(question)
print(f"📚 Found {len(reviews)} relevant reviews")
    
# Format reviews for the AI
review_data = []
for review in reviews:
    review_data.append({
            "content": review.page_content,
            "rating": review.metadata.get('rating', 'N/A'),
            "date": review.metadata.get('date', 'N/A'),
            "review_id": review.id
        })

print(review_data)