import json
import asyncio

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_RETRIES,
    RETRY_DELAY,
    PROMPT_LOG,
    RESPONSE_LOG
)

from prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE
)


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.first_batch_logged = False


    async def normalize_batch(self, records):

        user_prompt = USER_PROMPT_TEMPLATE.format(

            records=json.dumps(
                records,
                indent=4,
                ensure_ascii=False
            )
        )

        if not self.first_batch_logged:

            PROMPT_LOG.write_text(
                user_prompt,
                encoding="utf-8"
            )

        for attempt in range(MAX_RETRIES):

            try:

                response = self.client.models.generate_content(

                    model=MODEL_NAME,

                    contents=user_prompt,

                    config=types.GenerateContentConfig(

                        temperature=TEMPERATURE,

                        system_instruction=SYSTEM_PROMPT,

                        response_mime_type="application/json"
                    )
                )

                if not self.first_batch_logged:

                    RESPONSE_LOG.write_text(
                        response.text,
                        encoding="utf-8"
                    )

                    self.first_batch_logged = True

                response_text = response.text.strip()

                if response_text.startswith("```json"):

                    response_text = (
                        response_text
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )

                elif response_text.startswith("```"):

                    response_text = (
                        response_text
                        .replace("```", "")
                        .strip()
                    )

                return json.loads(response_text)

            except Exception as e:

                print(
                    f"Retry {attempt+1}/{MAX_RETRIES}: {e}"
                )

                if attempt < MAX_RETRIES - 1:

                    await asyncio.sleep(
                        RETRY_DELAY * (attempt + 1)
                    )

                    continue

                return None