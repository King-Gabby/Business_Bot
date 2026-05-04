from openai import OpenAI
import os
from pydantic import BaseModel
from typing import Optional, Literal
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class CustomerDetails(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class ExtractedIntent(BaseModel):
    intent: Literal[
        "buy", "browse", "ask_price", "confirm",
        "provide_details", "out_of_scope",
        "frustration", "greeting", "handoff", "unknown",
        "business_info", "location", "delivery", "resume_bot"
    ]
    product: Optional[str] = None
    quantity: Optional[int] = None
    details: Optional[CustomerDetails] = None


def extract_intent(message: str, context: dict) -> ExtractedIntent:
    system_prompt = f"""
You are an intent extraction engine for a Nigerian e-commerce chatbot.

Return ONLY valid JSON matching this schema:
{ExtractedIntent.model_json_schema()}

Rules:
- Understand Nigerian slang and informal speech.
- Map intent strictly.
- Extract product + quantity when possible.
- If user is angry → frustration.
- If unrelated (laptops, jobs) → out_of_scope.
"""

    try:
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0
        )

        text = response.output[0].content[0].text
        return ExtractedIntent.model_validate_json(text)
    except Exception as e:
        print(f"LLM Error: {e}")
        return ExtractedIntent(intent="unknown")