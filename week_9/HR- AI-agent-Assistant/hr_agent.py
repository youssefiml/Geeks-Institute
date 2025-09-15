import os
import json
import re
import webbrowser
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GIT_API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL", "gpt-4.1-mini")

if not GIT_API_KEY:
    print("❌ Missing GIT_API_KEY in .env")
    exit(1)

client = OpenAI(api_key=GIT_API_KEY)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CANDIDATES_FILE = DATA_DIR / "candidates.json"
SHORTLISTS_FILE = DATA_DIR / "shortlists.json"
JOBS_FILE = DATA_DIR / "jobs.json"

def load_json_file(path: Path) -> List[Dict[str, Any]]:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

candidates = load_json_file(CANDIDATES_FILE)
shortlists = load_json_file(SHORTLISTS_FILE) if SHORTLISTS_FILE.exists() else {}
jobs = load_json_file(JOBS_FILE)

# ----------------- Tools -----------------
def search_candidates(skills: List[str], location: Optional[str] = None,
                      minExp: int = 0, maxExp: int = 100,
                      availabilityWindowDays: Optional[int] = None,
                      top_n: int = 5) -> List[Dict[str, Any]]:
    today = datetime.now().date()
    results = []
    for c in candidates:
        score = 0
        reason = []

        cand_skills = c.get("skills", [])
        matched_skills = [s for s in skills if s.lower() in [cs.lower() for cs in cand_skills]]
        score += 2 * len(matched_skills)
        if matched_skills:
            reason.append(f"{'+'.join(matched_skills)} match (+{2*len(matched_skills)})")

        if location and c.get("location","").lower() == location.lower():
            score += 1
            reason.append("Location match (+1)")

        exp = c.get("experienceYears",0)
        if minExp-1 <= exp <= maxExp+1:
            score += 1
            reason.append("Experience fits (±1)")

        avail = c.get("availabilityDate")
        if availabilityWindowDays and avail:
            try:
                avail_dt = datetime.fromisoformat(avail).date()
                if (avail_dt - today).days <= availabilityWindowDays:
                    score +=1
                    reason.append("Available soon (+1)")
            except:
                pass

        if score>0:
            results.append({"candidate": c, "score": score, "reason": " → ".join(reason)})

    # AI-enhanced ranking: ask GPT to rerank top candidates
    try:
        prompt = f"Rank these candidates based on best fit:\n{json.dumps(results, indent=2)}"
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=400
        )
        
    except:
        pass

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]

def save_shortlist(name: str, candidate_emails: List[str]):
    shortlists[name] = candidate_emails
    with SHORTLISTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(shortlists, f, indent=2, ensure_ascii=False)
    return f"✅ Shortlist '{name}' saved with {len(candidate_emails)} candidates."

def draft_email(recipients: List[str], job_title: str, tone: str = "friendly") -> Dict[str,str]:
    """
    Drafts email using AI and returns subject + text.
    Also opens an HTML preview in the browser.
    """
    recipient_names = ", ".join(recipients)
    system_prompt = f"You are a recruiting assistant. Write a {tone} email with subject + body for job '{job_title}' to: {recipient_names}."
    user_prompt = f"Generate a concise subject line and a professional email body for {recipient_names} for the role '{job_title}'. Keep it engaging and action-oriented."

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        ai_text = resp.choices[0].message.content.strip()
        lines = ai_text.splitlines()
        if len(lines)>1 and lines[0].lower().startswith("subject"):
            subject = lines[0].split(":",1)[1].strip()
            body = "\n".join(lines[1:]).strip()
        else:
            subject = f"Opportunity: {job_title}"
            body = ai_text

        # HTML preview
        html_content = f"""
        <html>
        <body>
        <h2>{subject}</h2>
        <p>{body.replace(chr(10), '<br>')}</p>
        </body>
        </html>
        """
        preview_file = DATA_DIR / "email_preview.html"
        with preview_file.open("w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open(preview_file.as_uri())

        return {"subject": subject, "text": body}
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        return {"subject": f"Opportunity: {job_title}",
                "text": f"Hi {recipient_names.split(',')[0]},\n\nWe have an opening for {job_title}. Please let us know if interested.\n\nBest,\nHR Team"}

def analytics_summary():
    stages = [c.get("stage","UNKNOWN") for c in candidates]
    skills = [s for c in candidates for s in c.get("skills",[])]
    return {
        "countByStage": dict(Counter(stages)),
        "topSkills": Counter(skills).most_common(5)
    }

# ----------------- Simple Agent -----------------
def parse_user_input(text: str) -> Dict[str, Any]:
    out = {"action": None, "params": {}}
    t = text.lower()
    if any(k in t for k in ["top","find"]):
        out["action"] = "search_candidates"
        skills = re.findall(r'\b(React|Vue|Angular|Python|Node|JS|JavaScript|TypeScript|SQL)\b', text, re.IGNORECASE)
        out["params"]["skills"] = [s.capitalize() if s.lower() not in ("js","node") else s.upper() for s in skills]
        loc = re.search(r'in\s+([A-Za-z\s]+)', text)
        if loc:
            out["params"]["location"] = loc.group(1).strip()
        exp = re.search(r'(\d+)[\s\-–to]*(\d+)?\s*years?', text)
        if exp:
            out["params"]["minExp"] = int(exp.group(1))
            out["params"]["maxExp"] = int(exp.group(2)) if exp.group(2) else int(exp.group(1))
        if "available this month" in t:
            out["params"]["availabilityWindowDays"] = 45
        out["params"]["top_n"] = 5
    elif "save shortlist" in t:
        out["action"] = "save_shortlist"
        names = re.findall(r'"([^"]+)"', text)
        out["params"]["name"] = names[0] if names else "default"
        emails = re.findall(r'\S+@\S+', text)
        out["params"]["candidate_emails"] = emails
    elif "draft email" in t:
        out["action"] = "draft_email"
        names = re.findall(r'"([^"]+)"', text)
        out["params"]["recipients"] = names
        job = re.search(r'job\s+"([^"]+)"', text)
        if job:
            out["params"]["job_title"] = job.group(1)
    elif "analytics" in t:
        out["action"] = "analytics_summary"
    return out

def agent_respond(user_text: str):
    parsed = parse_user_input(user_text)
    action = parsed.get("action")
    params = parsed.get("params", {})
    if not action:
        return "Unknown command. Try: top candidates, draft email, save shortlist, analytics, exit."
    if action == "search_candidates":
        return search_candidates(**params)
    if action == "save_shortlist":
        return save_shortlist(**params)
    if action == "draft_email":
        return draft_email(**params)
    if action == "analytics_summary":
        return analytics_summary()

# ----------------- CLI -----------------
if __name__ == "__main__":
    print("🤖 AI-Powered HR Agent CLI (all tools AI)")
    while True:
        text = input("You: ").strip()
        if text.lower() in ("quit","exit"):
            break
        response = agent_respond(text)
        print("Agent:", json.dumps(response, indent=2, ensure_ascii=False))