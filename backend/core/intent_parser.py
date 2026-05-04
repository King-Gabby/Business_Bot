import re
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, Literal
from backend.models.schemas import BusinessSchema

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

class ExtractedIntent(BaseModel):
    intent: Literal[
        "greeting", "browse_products", "ask_price", "buy", 
        "human_request", "delivery", "unknown", "cancel"
    ]
    product: Optional[str] = None
    quantity: Optional[int] = None

class IntentParser:
    def __init__(self):
        # Basic normalization replacements
        self.replacements = {
            "jewelries": "jewellery", "shoe": "shoes", "bag": "bags", 
            "watch": "watches", "cloth": "wears", "laptop": "electronics"
        }

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        for k, v in self.replacements.items():
            text = text.replace(k, v)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _deterministic_parse(self, text: str, business: BusinessSchema) -> Optional[ExtractedIntent]:
        """Layer 1: Fast, deterministic rule-based matching."""
        t = self.normalize(text)
        
        # 1. Greetings
        if t in ["hi", "hello", "hey", "morning", "yo", "good morning"]:
            return ExtractedIntent(intent="greeting")
            
        # 2. Cancellations
        if t in ["cancel", "stop", "nevermind", "no"]:
            return ExtractedIntent(intent="cancel")

        # 3. Simple Intents
        if any(w in t for w in ["human", "agent", "person", "talk"]):
            return ExtractedIntent(intent="human_request")
            
        if any(w in t for w in ["delivery", "ship", "location"]):
            return ExtractedIntent(intent="delivery")

        # 4. Pure Quantity (if user just types a number)
        if t.isdigit():
            return ExtractedIntent(intent="buy", quantity=int(t))

        # 5. Exact Product Match (Fast path)
        for p_key, p_val in business.products.items():
            aliases = [p_key.lower(), p_val.display_name.lower()] + [a.lower() for a in p_val.aliases]
            for alias in aliases:
                # If they exactly typed the product name
                if t == self.normalize(alias):
                    return ExtractedIntent(intent="buy", product=p_key)

        return None # Fallback to LLM

    def _llm_parse(self, text: str, business: BusinessSchema) -> ExtractedIntent:
        """Layer 2: LLM Fallback for ambiguous/complex inputs."""
        
        product_list = ", ".join([p.display_name for p in business.products.values()])
        
        system_prompt = f"""
        You are an intent extraction engine for {business.name}.
        Return ONLY valid JSON matching the schema.
        Available products: {product_list}.
        Map user input to the closest intent. If they mention a product, intent is 'buy'.
        Extract product key (not display name) if found.
        """

        if not client:
            print("[LLM Error] OPENAI_API_KEY not set. Using fallback intent.")
            return ExtractedIntent(intent="unknown")

        try:
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format=ExtractedIntent,
                temperature=0
            )
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"[LLM Error] {e}")
            return ExtractedIntent(intent="unknown")

    def parse(self, text: str, business: BusinessSchema) -> ExtractedIntent:
        # Try deterministic first
        intent = self._deterministic_parse(text, business)
        if intent:
            return intent
            
        # Fallback to LLM
        return self._llm_parse(text, business)

intent_parser = IntentParser()
