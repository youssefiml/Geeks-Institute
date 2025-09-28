Based on the AI Email Assistant's capabilities and the user data in your database, here are 7 great questions to test the system:

## 📧 **Email Generation & Sending Questions:**

### 1. **Meeting Reminder Email**
```
"Create a meeting reminder email to Mouad Bounfil about the hackathon tomorrow at 10 AM"
```
*Tests: User search + Email prompt chaining + HTML template generation*

### 2. **Department-Wide Announcement**
```
"Send a project update email to all Engineering team members about the new software release"
```
*Tests: Department-based targeting + Professional email content*

### 3. **Welcome Email for New Employee**
```
"Create a welcome email for Oussama Abayoss who just joined our Marketing department"
```
*Tests: User-specific information + Onboarding email template*

## 👤 **User Search & Information Questions:**

### 4. **Individual User Lookup**
```
"Tell me about Emily Davis - what department is she in and what's her contact information?"
```
*Tests: User search functionality + Information formatting*

### 5. **Partial Name Search**
```
"Find information for someone named Christopher in our system"
```
*Tests: Partial name matching + Database search capabilities*

## 📊 **Analytics & Reporting Questions:**

### 6. **User Statistics**
```
"How many users do we have in total and what's the breakdown by department?"
```
*Tests: Analytics aggregation + Data summarization*

### 7. **Complex Multi-Step Request**
```
"Find Amanda Taylor's information and then create a birthday celebration email for her Design team colleagues"
```
*Tests: Multiple tool usage + Workflow coordination + Email generation*

## 🎯 **Expected Outcomes:**

### **Email Questions (1-3):**
- AI will search for users
- Generate professional email content
- Create beautiful HTML templates
- Show preview and ask for sending confirmation

### **User Questions (4-5):**
- Search MongoDB database
- Return formatted user information
- Handle partial matches intelligently

### **Analytics Question (6):**
- Aggregate user data by department and gender
- Provide total counts and breakdowns
- Present in readable format

### **Complex Question (7):**
- Execute multiple tools in sequence
- Combine user search with email generation
- Demonstrate advanced workflow coordination

## 💡 **Bonus Testing Ideas:**

You can also try:
- **General conversation**: "Hi, how are you?" (should respond normally without tools)
- **Invalid user**: "Find information for John Doe" (should handle gracefully)
- **Wrong format**: "What's the weather like?" (should respond without using tools)

These questions will thoroughly test all the AI agent's capabilities: prompt chaining, database integration, analytics, and intelligent tool selection! 🚀