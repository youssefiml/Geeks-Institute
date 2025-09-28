# AI-Powered HR Agent CLI

An intelligent command-line recruitment tool that leverages AI to streamline candidate search, shortlist management, and email communication for HR professionals.

## Features

- **Smart Candidate Search**: Find candidates using natural language queries with skill matching, location filtering, and experience requirements
- **AI-Enhanced Ranking**: Automatically ranks candidates using OpenAI's language models for better match quality
- **Shortlist Management**: Save and organize candidate shortlists with persistent storage
- **AI Email Generation**: Automatically draft professional recruitment emails with customizable tone
- **Analytics Dashboard**: Get insights on candidate distribution by stage and top skills
- **Email Preview**: Automatically opens HTML email previews in your browser

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (see Installation)

## Installation

1. Clone or download the project files

2. Install required dependencies:
```bash
pip install openai python-dotenv
```

3. Create a `.env` file in the project root:
```env
API_KEY=your_openai_api_key_here
MODEL=gpt-4o-mini
```

4. Prepare your data files in the `data/` directory:
   - `candidates.json` - Your candidate database
   - `jobs.json` - Available job positions
   - `shortlists.json` - Saved shortlists (auto-created)

## Data Format

### Candidates JSON Structure
```json
[
  {
    "email": "candidate@example.com",
    "name": "John Doe",
    "skills": ["React", "JavaScript", "Node.js"],
    "location": "New York",
    "experienceYears": 5,
    "availabilityDate": "2024-03-15",
    "stage": "SCREENING"
  }
]
```

### Jobs JSON Structure
```json
[
  {
    "title": "Senior Frontend Developer",
    "location": "Remote",
    "requirements": ["React", "TypeScript", "5+ years experience"]
  }
]
```

## Usage

### Starting the CLI
```bash
python main.py
```

### Available Commands

#### 1. Search Candidates
Find candidates using natural language:
```
You: Find top React and Python developers in New York with 3-5 years experience
You: Top candidates with JavaScript skills available this month
You: Find Vue developers with 2+ years experience
```

**Search Parameters:**
- **Skills**: React, Vue, Angular, Python, Node, JavaScript, TypeScript, SQL
- **Location**: Any city/region (e.g., "in New York", "in London")
- **Experience**: Years range (e.g., "3-5 years", "2+ years")
- **Availability**: "available this month" (within 45 days)

#### 2. Save Shortlist
Create and save candidate shortlists:
```
You: Save shortlist "Frontend Team Q1" john@example.com jane@example.com
```

#### 3. Draft Emails
Generate AI-powered recruitment emails:
```
You: Draft email "John Doe" "Jane Smith" job "Senior Developer"
```
- Automatically opens HTML preview in browser
- Generates professional subject line and body
- Customizable tone (friendly by default)

#### 4. Analytics
Get candidate pipeline insights:
```
You: Analytics
```
Returns:
- Candidate count by stage
- Top 5 most common skills

#### 5. Exit
```
You: exit
You: quit
```

## AI Features

### Intelligent Candidate Ranking
The system uses OpenAI's language models to:
- Analyze candidate profiles against job requirements
- Provide contextual ranking beyond simple keyword matching
- Generate human-readable explanations for candidate scores

### Smart Email Generation
AI-powered email drafting includes:
- Professional tone adaptation
- Personalized content based on recipient names
- Job-specific messaging
- Automatic subject line generation

### Natural Language Processing
The CLI understands various input formats:
- Casual language: "Find me some React devs"
- Specific requirements: "Top 5 Python developers in Boston with 4+ years"
- Mixed criteria: "JavaScript experts available soon in remote positions"

## Scoring Algorithm

Candidates are scored based on:
- **Skill Match**: +2 points per matching skill
- **Location Match**: +1 point for exact location match
- **Experience Fit**: +1 point if within ±1 year of requirements
- **Availability**: +1 point if available within specified timeframe

## File Structure

```
project/
├── main.py              # Main application file
├── .env                 # Environment variables (API keys)
├── README.md           # This file
└── data/
    ├── candidates.json  # Candidate database
    ├── jobs.json       # Job positions
    ├── shortlists.json # Saved shortlists (auto-created)
    └── email_preview.html # Email preview (auto-generated)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | OpenAI API key | Required |
| `MODEL` | OpenAI model to use | `gpt-4o-mini` |

## Error Handling

- **Missing API Key**: Application exits with error message
- **AI Service Unavailable**: Falls back to basic scoring and template emails
- **Invalid JSON**: Gracefully handles malformed data files
- **Missing Files**: Creates empty datasets when files don't exist

## Examples

### Complete Workflow Example
```bash
# Start the application
python main.py

# Search for candidates
You: Find top 3 React developers in San Francisco with 4+ years experience

# Save promising candidates
You: Save shortlist "React Senior Roles" alice@dev.com bob@tech.com

# Draft outreach emails
You: Draft email "Alice Johnson" "Bob Chen" job "Senior React Developer"

# Check analytics
You: Analytics

# Exit
You: quit
```

## Troubleshooting

### Common Issues

1. **"Missing GIT_API_KEY in .env"**
   - Ensure your `.env` file contains `API_KEY=your_actual_key`

2. **No candidates found**
   - Check that `candidates.json` exists and contains valid data
   - Verify skill names match the supported list

3. **Email preview doesn't open**
   - Check browser permissions
   - Verify `data/` directory exists and is writable

4. **AI features not working**
   - Verify OpenAI API key is valid and has sufficient credits
   - Check internet connection

## Contributing

To extend functionality:
1. Add new skills to the regex pattern in `parse_user_input()`
2. Extend scoring logic in `search_candidates()`
3. Add new commands by updating the parsing logic
4. Customize email templates in `draft_email()`

## License

This project is provided as-is for demonstration purposes. Ensure compliance with OpenAI's usage policies when deploying.