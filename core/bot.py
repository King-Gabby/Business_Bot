import json
import os
import re

def normalize_input(text):
    """Standardize input for reliable matching."""
    return text.lower().strip()

def extract_quantity(text):
    """
    Upgraded Quantity Extraction (V7): Handles word-numbers and digits.
    """
    text = text.lower()
    word_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    # Check for word-numbers
    for word, num in word_numbers.items():
        if word in text:
            return num
            
    # Check for digits
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
        
    return None

def detect_product(text, products, context=None):
    """
    Robust Product Detection (V6): Substring matching across keys and aliases.
    """
    text = normalize_input(text)
    
    for product_key, data in products.items():
        # 1. Check primary key (e.g., 'shoes')
        if product_key in text:
            return product_key
            
        # 2. Check aliases (e.g., 'shoe', 'sneakers')
        for alias in data.get("aliases", []):
            if alias in text:
                return product_key
                
    return None

def is_relevant_to_business(text, products):
    """Checks if the input is about the business or its products."""
    text = normalize_input(text)
    
    # Check if a product is mentioned
    if detect_product(text, products):
        return True
        
    # Check for general business keywords
    business_keywords = ["price", "cost", "order", "buy", "sell", "location", "address", "stock", "range", "what do you"]
    if any(kw in text for kw in business_keywords):
        return True
        
    return False

def detect_intent(text):
    """Detect user intent based on keywords."""
    text = normalize_input(text)
    
    keywords = {
        "greeting": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "what's up", "sup", "yo", "who's here"],
        "delivery": ["delivery", "deliver", "outside lagos", "shipping", "how do you deliver"],
        "price": ["price", "cost", "how much", "amount", "last price", "selling price", "range"],
        "location": ["location", "where", "address", "find you", "office", "stay"],
        "product_list": ["product", "stock", "items", "have", "sell"],
        "business_info": ["what do you do sell", "what is your business", "who are you", "about you"],
        "budget": ["budget", "around", "range", "within", "cheap"],
        "interest": ["i need", "i want", "looking for", "searching for"],
        "buy": ["buy", "order", "get", "purchase", "buying now"],
        "confirm": ["yes", "yeah", "yep", "sure", "ok", "okay", "proceed", "go ahead"],
        "neutral": ["ok", "okay", "alright", "cool", "fine"],
        "confused": ["what", "huh", "pardon", "idk", "not sure", "oh", "hmm"],
        "negative": ["stupid", "nonsense", "bullshit", "useless", "bad", "what the hell"]
    }

    for intent, terms in keywords.items():
        if any(term in text for term in terms):
            return intent
    
    return "fallback"

def list_products(products):
    """Returns a short list of primary products."""
    keys = list(products.keys())
    return ", ".join([p.capitalize() for p in keys[:5]]) + " and more"

def generate_response(user_input, business_data, context=None):
    """
    V8 Orchestration Logic: Intent Priority System and State Isolation.
    """
    # Initialize state if missing
    if context is not None:
        if "stage" not in context: context["stage"] = "idle"
        if "product" not in context: context["product"] = None
        if "quantity" not in context: context["quantity"] = None

    intent = detect_intent(user_input)
    product_found = detect_product(user_input, business_data["products"])
    
    # 🔥 PRIORITY 1: Service-level intents (Resets Flow)
    if intent in ["delivery", "business_info", "greeting", "confused", "negative", "location", "neutral", "confirm"]:
        # Only reset if we are NOT in an active order flow for neutral/confirm
        if intent not in ["neutral", "confirm"] or (context and context.get("stage") == "idle"):
            if context is not None:
                context["stage"] = "idle"
                context["product"] = None
                context["quantity"] = None

        if intent == "greeting":
            return f"Hi 👋 Welcome to {business_data['name']}! How can I help you today?"
        
        if intent == "delivery":
            return (
                "Yes 🙂 We deliver both inside and outside Lagos.\n"
                "Delivery fee depends on your location.\n"
                "What would you like to order?"
            )
        
        if intent == "location":
            return f"📍 We are located at {business_data['location']}. {business_data['delivery']}"
            
        if intent == "business_info":
            return (
                f"{business_data['name']} sells quality items like "
                f"{list_products(business_data['products'])}.\n"
                "We help you get great products at affordable prices 🙂"
            )
            
        if intent == "confused":
            return "No worries 🙂 You can ask me about our products, prices, location, or how to order. What's on your mind?"
            
        if intent == "negative":
            return "I understand 😅 Let me try better. What product are you looking for?"

        if intent in ["neutral", "confirm"] and (not context or context.get("stage") == "idle"):
            return "Alright 🙂 What would you like to do next? See products or check a price?"

    # 🔥 PRIORITY 2: Order flow (State Machine)
    if context and context.get("stage") == "quantity_waiting":
        qty_input = extract_quantity(user_input)
        if qty_input:
            context["quantity"] = qty_input
            context["stage"] = "order_confirmed"
            
            product_key = context["product"]
            product_data = business_data["products"][product_key]
            raw_price = product_data["price"]
            price_val = int(raw_price.replace("₦", "").replace(",", "").replace("N", ""))
            total = price_val * qty_input
            display_name = product_data.get("display_name", product_key)
            
            return (
                f"Perfect 👍 {qty_input} {display_name} will cost ₦{total:,}.\n"
                "Should I proceed with your order?"
            )
        # If no quantity found but a NEW product is mentioned, switch products
        if product_found and product_found != context.get("product"):
            context["product"] = product_found
            product_data = business_data["products"][product_found]
            display_name = product_data.get("display_name", product_found)
            return (
                f"Nice choice 🙂 We have {display_name} available.\n"
                f"Price is {product_data['price']}.\n"
                "How many would you like?"
            )
        return "How many would you like?"

    if context and context.get("stage") == "order_confirmed":
        if intent in ["confirm", "neutral"]:
            return (
                "Great 🙌 Please send your name and delivery address.\n"
                "I'll process your order right away."
            )
        # If they say something else after confirmed, check if it's a new product
        if product_found:
            context["product"] = product_found
            context["stage"] = "quantity_waiting"
            context["quantity"] = None
            product_data = business_data["products"][product_found]
            return f"Nice choice 🙂 The {product_data.get('display_name', product_found)} cost {product_data['price']}. How many?"

    # 🔥 PRIORITY 3: Product flow
    if product_found:
        if context is not None:
            context["product"] = product_found
            context["stage"] = "quantity_waiting"
        
        product_data = business_data["products"][product_found]
        display_name = product_data.get("display_name", product_found)
        return (
            f"Nice choice 🙂 We have {display_name} available.\n"
            f"Price is {product_data['price']}.\n"
            "How many would you like?"
        )

    # General Product List
    if intent == "product_list":
        return f"We have items like {list_products(business_data['products'])} 🙂 What are you looking for?"

    # Price range
    if intent == "price" and "range" in user_input.lower():
        prices = [int(p["price"].replace("₦","").replace(",","").replace("N","")) for p in business_data["products"].values()]
        return f"Our products range from ₦{min(prices):,} to ₦{max(prices):,}. 💰 What are you interested in?"

    # Domain Guardrail / Fallback
    if intent in ["price", "buy", "product_list", "budget", "interest"] or not is_relevant_to_business(user_input, business_data["products"]):
        return (
            f"I don't have that at the moment 🙂\n"
            f"But I can help with fashion items like {list_products(business_data['products'])}."
        )

    # Final Fallback
    return "I'm not sure I understand. Would you like to see our products or check a price?"

def load_config(config_path):
    """Helper to load JSON data."""
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r') as f:
        return json.load(f)
