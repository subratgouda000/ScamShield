import os
import json
import time
from dotenv import load_dotenv
from google import genai
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_message(message):
    prompt = f"""
You are ScamShield, a cybersecurity assistant.

Analyze this suspicious message:

--- MESSAGE ---
{message}
--- END MESSAGE ---

Return ONLY valid JSON.
Do not use markdown.
Do not add any text before or after the JSON.

Use exactly this structure:

{{
  "risk_level": "LOW",
  "risk_score": 0,
  "classification": "Likely Legitimate",
  "warning_signs": [
    "warning sign 1",
    "warning sign 2"
  ],
  "explanation": "Short explanation of why this message may or may not be risky.",
  "safe_actions": [
    "safe action 1",
    "safe action 2",
    "safe action 3"
  ]
}}

Rules:
- risk_level must be exactly LOW, MEDIUM, or HIGH.
- risk_score must be an integer from 0 to 100.
- classification must be exactly Scam, Suspicious, or Likely Legitimate.
- warning_signs must contain concise reasons supported by the message.
- safe_actions must give practical safety advice.
- Do not claim certainty when the evidence is unclear.
"""

    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            text = response.text.strip()

            # Remove accidental markdown code fences
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except Exception as e:

            error_message = str(e)

            # Retry temporary Gemini service problems
            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
            ):
                if attempt < max_attempts - 1:
                    time.sleep(2)
                    continue

            raise e