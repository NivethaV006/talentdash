import json

from google import genai

from google.genai import types

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent / "llm")
)

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def llm_classify(role, experience):

    prompt = f"""
You are a job level classifier.

Return ONLY valid JSON.

Allowed Levels:

L3
L4
L5
L6
SDE-I
SDE-II
SDE-III
Staff
Principal
IC4
IC5

Role:
{role}

Experience:
{experience} years

Return format:

{{
    "level":"L4",
    "confidence":0.70
}}
"""

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=0,

                response_mime_type="application/json"
            )
        )

        data = json.loads(
            response.text
        )

        return {

            "level": data["level"],

            "confidence": data["confidence"],

            "method": "LLM_FALLBACK"
        }

    except Exception:

        return {

            "level": "Unknown",

            "confidence": 0.40,

            "method": "LLM_FALLBACK"
        }