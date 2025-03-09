import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_match_percentage(resume_text, job_text):
    """Calculate job-resume match percentage using AI."""
    prompt = f"""
    Given the following job description and resume, determine how well they match on a scale of 0 to 100.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_text}

    Provide ONLY a single numerical match percentage (0-100).
    """
    try:
        response = model.generate_content(prompt)
        match_percentage = float(response.text.strip())
        return max(0, min(100, match_percentage))
    except Exception as e:
        print(f"Error with AI model: {e}")
        return 0
