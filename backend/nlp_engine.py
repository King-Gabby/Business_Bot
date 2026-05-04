from rapidfuzz import process
import re

# --- CONFIG ---
INTENTS = ["greeting", "browse_products", "ask_price", "order_flow", "human_request", "unknown"]

REPLACEMENTS = {
    "jewelries": "jewellery", "jewelleries": "jewellery", "jewlery": "jewellery", "jewelry": "jewellery",
    "shoe": "shoes", "bag": "bags", "watch": "watches", "perfume": "perfumes",
    "cream": "creams", "cloth": "wears", "clothes": "wears", "wear": "wears",
    "laptop": "electronics", "computer": "electronics", "macbook": "electronics",
    "sneaker": "sneakers"
}

# --- NORMALIZATION LAYER ---
def normalize_text(text: str) -> str:
    """Fix plurals, typos, and variations before understanding."""
    text = text.lower().strip()
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# --- INTENT ROUTER (Lightweight Classifier) ---
def classify_intent(text: str) -> str:
    """STRICT INTENT CLASSIFICATION: No business logic here."""
    t = normalize_text(text)

    if any(w in t for w in ["hi", "hello", "hey", "morning", "evening", "yo"]):
        return "greeting"

    if any(w in t for w in ["what do you have", "stock", "items", "sell", "browse", "collection", "show"]):
        return "browse_products"

    if any(w in t for w in ["price", "cost", "how much", "rate", "naira"]):
        return "ask_price"

    if any(w in t for w in ["order", "buy", "purchase", "want", "get", "need", "confirm", "yes", "proceed"]):
        return "order_flow"

    if any(w in t for w in ["human", "agent", "person", "seller", "talk", "whatsapp", "call"]):
        return "human_request"

    return "unknown"

def extract_product_fuzzy(text: str, products_dict: dict):
    """
    Fuzzy match against product keys AND their aliases.
    Returns the official product key.
    """
    t = normalize_text(text)
    if not products_dict:
        return None
        
    # 1. Create a map of searchable terms -> actual keys
    search_map = {}
    for key, data in products_dict.items():
        # Add the key itself
        search_map[normalize_text(key)] = key
        # Add display name
        search_map[normalize_text(data.get("display_name", ""))] = key
        # Add aliases
        for alias in data.get("aliases", []):
            search_map[normalize_text(alias)] = key
            
    if not search_map:
        return None
        
    # 2. Match against all terms
    terms = list(search_map.keys())
    match = process.extractOne(t, terms)
    
    if match and match[1] > 75: 
        matched_term = match[0]
        return search_map[matched_term]
        
    return None

def extract_quantity_robust(text: str):
    """Handles both digits and word numbers."""
    t = text.lower()
    word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "ten": 10}
    for word, num in word_map.items():
        if word in t: return num
    
    match = re.search(r'\d+', t)
    return int(match.group()) if match else None
