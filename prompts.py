import json   # ✅ THIS WAS MISSING

def resume_prompt(raw_data: dict) -> str:
    return f"""
You are an expert resume writer and ATS optimization engine.

TRANSFORMATION RULES (MANDATORY):
- Rewrite ALL text to sound professional and impactful
- Replace weak verbs with strong action verbs
- Quantify impact where reasonable
- Improve grammar and clarity
- Optimize for ATS keywords
- Do NOT copy sentences directly
- Rewrite aggressively even if input seems good
- Do NOT invent fake companies or experience

OUTPUT FORMAT:
Return ONLY valid JSON.
No markdown.
No explanation.
No backticks.

JSON SCHEMA:
{{
  "summary": "Professional rewritten summary",
  "skills": ["Category: optimized skills"],
  "projects": [
    {{
      "title": "Improved project title",
      "date": "date",
      "bullets": ["Impactful bullet", "Impactful bullet"]
    }}
  ],
  "education": "Professional education section",
  "certificates": "Professional certificates section"
}}

RAW INPUT:
{json.dumps(raw_data, indent=2)}
"""
