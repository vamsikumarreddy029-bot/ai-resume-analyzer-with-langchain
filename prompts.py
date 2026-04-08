extract_prompt = """
You are an expert resume parser.

Return ONLY valid JSON.

{{
  "name": "",
  "skills": [],
  "projects": [],
  "experience": [],
  "education": []
}}

Resume:
{resume_text}
"""

clean_prompt = """
Clean and format this resume.

- Fix grammar
- Keep same meaning
- Structure properly

Resume:
{resume_text}
"""

classify_prompt = """
Classify the candidate.

Return JSON ONLY:

{{
  "role": "",
  "experience_level": ""
}}

Resume:
{resume_text}
"""

enhance_prompt = """
Improve resume for ATS:

- Strong action verbs
- Better bullet points
- Professional tone

Resume:
{resume_text}
"""

ats_prompt = """
Evaluate resume ATS score.

Return JSON ONLY:

{{
  "ats_score": "number between 0-100",
  "missing_keywords": [],
  "suggestions": []
}}

Resume:
{resume_text}
"""