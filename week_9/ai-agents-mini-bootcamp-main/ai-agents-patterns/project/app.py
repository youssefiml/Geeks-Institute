from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import json
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, HtmlContent

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "admin@company.com")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize clients
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
sendgrid_client = SendGridAPIClient(api_key=SENDGRID_API_KEY)

# --------------------------------------------------------------
# Data Models for Prompt Chaining
# --------------------------------------------------------------

class EmailRequest(BaseModel):
    """First step: Analyze if user wants to send an email"""
    is_email_request: bool = Field(description="Whether this is an email sending request")
    recipient_info: str = Field(description="Information about who should receive the email")
    email_purpose: str = Field(description="Purpose or subject of the email")
    confidence_score: float = Field(description="Confidence score between 0 and 1")

class EmailContent(BaseModel):
    """Second step: Generate email content"""
    subject: str = Field(description="Email subject line")
    content: str = Field(description="Email body content in plain text")
    tone: str = Field(description="Tone of the email (professional, friendly, formal, etc.)")

class EmailTemplate(BaseModel):
    """Third step: Generate HTML template"""
    html_content: str = Field(description="Complete HTML email template")
    template_style: str = Field(description="Style description of the template")

class EmailConfirmation(BaseModel):
    """Fourth step: Final confirmation before sending"""
    ready_to_send: bool = Field(description="Whether the email is ready to send")
    final_recipient: str = Field(description="Final recipient email address")
    final_subject: str = Field(description="Final email subject")
    confirmation_message: str = Field(description="Confirmation message for user")

class UserQuery(BaseModel):
    """For user information queries"""
    user_info: dict = Field(description="User information from database")
    formatted_response: str = Field(description="Formatted response about the user")

class AnalyticsQuery(BaseModel):
    """For analytics queries"""
    total_users: int = Field(description="Total number of users")
    analytics_summary: str = Field(description="Summary of analytics data")

# --------------------------------------------------------------
# Database Functions
# --------------------------------------------------------------

def get_user_by_name(first_name: str, last_name: str = None):
    """Get user information from database"""
    logger.info(f"Searching for user: {first_name} {last_name or ''}")
    
    if last_name:
        query = {"firstName": {"$regex": first_name, "$options": "i"}, 
                "lastName": {"$regex": last_name, "$options": "i"}}
    else:
        query = {"$or": [
            {"firstName": {"$regex": first_name, "$options": "i"}},
            {"lastName": {"$regex": first_name, "$options": "i"}}
        ]}
    
    user = collection.find_one(query)
    return user

def get_user_analytics():
    """Get analytics about users"""
    logger.info("Fetching user analytics")
    
    total_users = collection.count_documents({})
    users_by_department = list(collection.aggregate([
        {"$group": {"_id": "$department", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))
    users_by_gender = list(collection.aggregate([
        {"$group": {"_id": "$gender", "count": {"$sum": 1}}}
    ]))
    
    return {
        "total_users": total_users,
        "by_department": users_by_department,
        "by_gender": users_by_gender
    }

# --------------------------------------------------------------
# Email Chain Functions
# --------------------------------------------------------------

def analyze_email_request(user_input: str) -> EmailRequest:
    """First step: Analyze if user wants to send an email"""
    logger.info("Analyzing email request")
    
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Analyze if the user wants to send an email. Look for keywords like 'send email', 'email to', 'notify', 'message', etc."
            },
            {"role": "user", "content": user_input}
        ],
        response_format=EmailRequest,
    )
    
    result = completion.choices[0].message.parsed
    logger.info(f"Email request analysis - Is email: {result.is_email_request}, Confidence: {result.confidence_score:.2f}")
    return result

def generate_email_content(email_purpose: str, recipient_info: str) -> EmailContent:
    """Second step: Generate email content"""
    logger.info("Generating email content")
    
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Generate professional email content based on the purpose and recipient information. Make it clear, concise, and appropriate for business communication."
            },
            {"role": "user", "content": f"Purpose: {email_purpose}\nRecipient: {recipient_info}"}
        ],
        response_format=EmailContent,
    )
    
    result = completion.choices[0].message.parsed
    logger.info(f"Email content generated - Subject: {result.subject}")
    return result

def create_html_template(email_content: EmailContent) -> EmailTemplate:
    """Third step: Create HTML email template"""
    logger.info("Creating HTML template")
    
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Create a professional HTML email template. Include proper HTML structure with CSS styling for a clean, modern look. Use the provided content and make it visually appealing."
            },
            {"role": "user", "content": f"Subject: {email_content.subject}\nContent: {email_content.content}\nTone: {email_content.tone}"}
        ],
        response_format=EmailTemplate,
    )
    
    result = completion.choices[0].message.parsed
    logger.info("HTML template created successfully")
    return result

def prepare_email_confirmation(template: EmailTemplate, email_content: EmailContent, recipient_email: str) -> EmailConfirmation:
    """Fourth step: Prepare final confirmation"""
    logger.info("Preparing email confirmation")
    
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Create a final confirmation for sending the email. Verify all details are correct and provide a clear confirmation message."
            },
            {"role": "user", "content": f"Recipient: {recipient_email}\nSubject: {email_content.subject}\nHTML Template Ready: Yes"}
        ],
        response_format=EmailConfirmation,
    )
    
    result = completion.choices[0].message.parsed
    logger.info("Email confirmation prepared")
    return result

def send_email_with_sendgrid(to_email: str, subject: str, html_content: str) -> bool:
    """Send email using SendGrid"""
    logger.info(f"Sending email to {to_email}")
    
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=HtmlContent(html_content)
        )
        
        response = sendgrid_client.send(message)
        
        if response.status_code == 202:
            logger.info("Email sent successfully")
            return True
        else:
            logger.error(f"Failed to send email. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False

# --------------------------------------------------------------
# Tool Functions
# --------------------------------------------------------------

def search_user(query: str):
    """Search for user information"""
    logger.info(f"Searching for user with query: {query}")
    
    # Extract name from query using AI
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract the first name and last name from the user query. Return them separated by a comma. If only one name is provided, return just that name."
            },
            {"role": "user", "content": query}
        ]
    )
    
    names = completion.choices[0].message.content.strip().split(',')
    first_name = names[0].strip()
    last_name = names[1].strip() if len(names) > 1 else None
    
    user = get_user_by_name(first_name, last_name)
    
    if user:
        # Remove MongoDB ObjectId for JSON serialization
        user.pop('_id', None)
        return {
            "found": True,
            "user": user,
            "formatted_info": f"Found user: {user['firstName']} {user['lastName']}, Age: {user['age']}, Department: {user['department']}, Email: {user['email']}, Location: {user['location']}"
        }
    else:
        return {
            "found": False,
            "user": None,
            "formatted_info": f"No user found with the name '{query}'"
        }

def get_analytics():
    """Get user analytics"""
    logger.info("Fetching analytics")
    
    analytics = get_user_analytics()
    
    dept_summary = ", ".join([f"{item['_id']}: {item['count']}" for item in analytics['by_department']])
    gender_summary = ", ".join([f"{item['_id']}: {item['count']}" for item in analytics['by_gender']])
    
    return {
        "total_users": analytics["total_users"],
        "summary": f"Total Users: {analytics['total_users']}. By Department: {dept_summary}. By Gender: {gender_summary}",
        "detailed_data": analytics
    }

def process_email_chain(user_input: str, recipient_email: str = None):
    """Main email processing chain"""
    logger.info("Starting email processing chain")
    
    # Step 1: Analyze email request
    email_request = analyze_email_request(user_input)
    
    # Gate check
    if not email_request.is_email_request or email_request.confidence_score < 0.7:
        logger.warning("Gate check failed - not an email request")
        return {
            "success": False,
            "message": "This doesn't appear to be an email request. Please specify that you want to send an email."
        }
    
    # Step 2: Generate email content
    email_content = generate_email_content(email_request.email_purpose, email_request.recipient_info)
    
    # Step 3: Create HTML template
    html_template = create_html_template(email_content)
    
    # Step 4: If recipient email provided, prepare for sending
    if recipient_email:
        confirmation = prepare_email_confirmation(html_template, email_content, recipient_email)
        
        return {
            "success": True,
            "email_content": {
                "subject": email_content.subject,
                "content": email_content.content,
                "tone": email_content.tone
            },
            "html_template": html_template.html_content,
            "confirmation": {
                "ready_to_send": confirmation.ready_to_send,
                "final_recipient": confirmation.final_recipient,
                "final_subject": confirmation.final_subject,
                "confirmation_message": confirmation.confirmation_message
            },
            "ready_to_send": True,
            "recipient": recipient_email
        }
    else:
        return {
            "success": True,
            "email_content": {
                "subject": email_content.subject,
                "content": email_content.content,
                "tone": email_content.tone
            },
            "html_template": html_template.html_content,
            "ready_to_send": False,
            "message": "Email content generated. Please provide recipient email to send."
        }

def call_function(name: str, args: dict):
    """Execute function calls"""
    if name == "search_user":
        return search_user(args["query"])
    elif name == "get_analytics":
        return get_analytics()
    elif name == "process_email":
        return process_email_chain(args["user_input"])
    elif name == "send_email":
        return send_email_with_sendgrid(args["to_email"], args["subject"], args["html_content"])
    else:
        raise ValueError(f"Unknown function: {name}")

# --------------------------------------------------------------
# Main Chat Interface
# --------------------------------------------------------------

def main():
    print("🤖 Welcome to the AI Email Assistant!")
    print("I can help you with:")
    print("  📧 Send emails with AI-generated content and HTML templates")
    print("  👤 Search for user information")
    print("  📊 Get user analytics")
    print("Type 'q' to quit.\n")
    
    # Define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_user",
                "description": "Search for user information by name. Use when user asks about a specific person.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Name or partial name to search for"}
                    },
                    "required": ["query"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_analytics",
                "description": "Get analytics about users including total count and demographics. Use when user asks about statistics, analytics, or 'how many users'.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "process_email",
                "description": "Process email request using AI prompt chaining to generate content and HTML template. Use when user wants to send an email.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {"type": "string", "description": "User's email request"}
                    },
                    "required": ["user_input"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send email using SendGrid. Use only after email content has been generated and confirmed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {"type": "string", "description": "Recipient email address"},
                        "subject": {"type": "string", "description": "Email subject"},
                        "html_content": {"type": "string", "description": "HTML email content"}
                    },
                    "required": ["to_email", "subject", "html_content"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]
    
    conversation_history = []
    
    while True:
        print("\n" + "="*60)
        user_input = input("🤔 How can I help you? ")
        print()
        
        if user_input.lower() == "q":
            print("👋 Thanks for using the AI Email Assistant!")
            break
        
        conversation_history.append({"role": "user", "content": user_input})
        
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI assistant that can:
1. Search for user information from a database
2. Provide analytics about users 
3. Help send emails using AI-generated content and HTML templates
4. Use prompt chaining for email generation (analyze request → generate content → create HTML → confirm → send)

IMPORTANT GUIDELINES:
- When users ask to send/create emails TO someone, use BOTH search_user (to find recipient) AND process_email (to generate the email)
- When users ask about specific people only, use search_user function
- When users ask about analytics or "how many users", use the get_analytics function
- For email requests, always use process_email to generate professional content and HTML templates
- Be helpful and guide users through the email sending process step by step

If a user asks to create an email to a specific person, you should:
1. Search for that person's information
2. Process the email request to generate content and template
3. Present the results and ask if they want to send it"""
            }
        ] + conversation_history
        
        try:
            print("🤖 Processing your request...")
            
            # Call AI with tools
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            if tool_calls:
                print("🔧 Using specialized tools...")
                
                messages.append(response_message)
                
                for tool_call in tool_calls:
                    print(f"🛠️ Executing: {tool_call.function.name}")
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    result = call_function(function_name, function_args)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                    
                    print("✅ Tool executed successfully")
                
                # Get final response
                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools
                )
                
                ai_response = final_response.choices[0].message.content
                
                # Handle case where response is None
                if ai_response is None:
                    ai_response = "I've processed your request successfully! Let me know if you need anything else."
                
                print(f"\n🤖 Assistant: {ai_response}")
                
            else:
                ai_response = response_message.content
                print(f"🤖 Assistant: {ai_response}")
            
            conversation_history.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again with a different request.")

if __name__ == "__main__":
    main()
