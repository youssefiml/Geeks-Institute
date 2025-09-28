from vector import retriever
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
MODEL = os.getenv("MODEL")

def search_reviews(question: str):
    """
    Search through restaurant reviews to find relevant information.
    """
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
    
    return review_data

def call_function(name, args):
    """Execute the function call."""
    if name == "search_reviews":
        return search_reviews(**args)
    raise ValueError(f"Unknown function: {name}")

def main():
    print("🍕 Welcome to the Smart Restaurant Assistant!")
    print("Ask me anything - I'll search reviews when needed or chat normally!")
    print("Type 'q' to quit.\n")
    
    # Define the search_reviews tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_reviews",
                "description": "Search through restaurant customer reviews to find relevant information about food, service, atmosphere, pricing, etc. Use this ONLY when the user asks about the restaurant, food, dining experience, or related topics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The user's question about the restaurant"
                        }
                    },
                    "required": ["question"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]
    
    conversation_history = []
    
    while True:
        print("\n" + "="*60)
        question = input("🤔 Ask your question: ")
        print()
        
        if question.lower() == "q":
            print("👋 Thanks for using the Smart Restaurant Assistant!")
            break
        
        # Store question in conversation history
        conversation_history.append(("user", question))
        
        # Create messages for this conversation
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant. You have access to a tool that can search restaurant reviews. Use the search_reviews tool ONLY when the user asks about restaurant-related topics (food, service, dining, etc.). For general questions, respond directly without using any tools."
            },
            {"role": "user", "content": question}
        ]
        
        try:
            print("🤖 Processing your question...")
            
            # Step 1: Call model with tools
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # Step 2: Handle function calls
            if tool_calls:
                print("🔧 AI decided to search restaurant reviews")
                
                # Add the assistant's response to messages
                messages.append(response_message)
                
                # Step 3: Execute each function call
                for tool_call in tool_calls:
                    print(f"\n🛠️ Executing function: {tool_call.function.name}")
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"   Arguments: {function_args}")
                    
                    result = call_function(function_name, function_args)
                    
                    # Display retrieved reviews
                    if result:
                        print("\n📝 Retrieved Reviews:")
                        print("-" * 40)
                        for i, review in enumerate(result, 1):
                            print(f"Review {i} (Rating: {review['rating']}/5):")
                            content = review['content']
                            print(f"  {content[:100]}..." if len(content) > 100 else f"  {content}")
                            print()
                    
                    # Step 4: Add function result to messages
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                    print("✅ Function executed successfully")
                
                # Step 5: Get final response with function results
                print("\n🤖 Generating final response based on reviews...")
                print("-" * 40)
                
                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools
                )
                
                ai_response = final_response.choices[0].message.content
                print(f"🎯 Restaurant Assistant: {ai_response}")
                
            else:
                # No function calls, respond directly
                print("💬 AI responding directly without searching reviews")
                print("-" * 40)
                ai_response = response_message.content
                print(f"🤖 Assistant: {ai_response}")
            
            # Store AI response in conversation history
            conversation_history.append(("assistant", ai_response))
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again with a different question.")

if __name__ == "__main__":
    main()
    
    
    
""" 
Test Examples:
Will trigger the search_reviews tool:
"How's the pizza here?"
"Is this place family-friendly?"
"What do customers say about delivery?"
"Any gluten-free options?"

Will NOT trigger the tool:
"What's the weather today?"
"Tell me a joke"
"How do you make pizza dough?"
"What's 5 + 5?"
"""