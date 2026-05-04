import json
import os
from nlp_engine import classify_intent, extract_product_fuzzy, extract_quantity_robust

# --- STAGES ---
STAGE_IDLE = "idle"
STAGE_BROWSING = "browsing"
STAGE_SELECTED = "product_selected"
STAGE_QUANTITY = "quantity"
STAGE_CHECKOUT = "checkout"
STAGE_HUMAN = "human"

# --- RESPONSE GENERATOR (UI Layer) ---
def generate_response(state, reply, options=None, card=None):
    """Pure UI layer: Generates structured response for frontend."""
    default_options = ["🛍️ Browse Products", "💰 Check Prices", "🚚 Delivery Info", "👤 Talk to Human"]
    return {
        "reply": reply,
        "options": options or default_options,
        "state": state,
        "card": card,
        "ui": {
            "show_input": state["mode"] == "bot",
            "lock_input": state["mode"] == "human"
        }
    }

# --- FLOW ENGINE (Brain) ---
def handle_user(message: str, session: dict, config: dict):
    """
    DYNAMIC MULTI-SELLER COMMERCE ENGINE
    Reads behavior and products from 'config'.
    """
    user_input = message.strip()
    business_name = config.get("name", "the store")
    
    # 1. HUMAN MODE OVERRIDE (Critical Fix)
    if session.get("mode") == "human":
        if any(w in user_input.lower() for w in ["resume", "back", "bot", "restart"]):
            session["mode"] = "bot"
            session["stage"] = STAGE_IDLE
            return generate_response(session, f"Welcome back to {business_name}! Bot is now active. How can I help you? 🙂")
        return None 

    # 2. INTENT ROUTER
    intent = classify_intent(user_input)
    session["intent"] = intent
    
    # 3. EXTRACTION
    products_dict = config.get("products", {})
    product_match = extract_product_fuzzy(user_input, products_dict)

    # 4. STATE TRANSITIONS
    
    # A. Global Interrupts
    if intent == "human_request":
        session["mode"] = "human"
        session["stage"] = STAGE_HUMAN
        contact = config.get("contact", "+234...")
        return generate_response(session, f"Alright! I'll connect you with the seller of {business_name}.\n\nYou can message them directly here: {contact}", options=["🔄 Resume Bot"])

    if intent == "greeting":
        session["stage"] = STAGE_IDLE
        return generate_response(session, f"Hi 👋 Welcome to {business_name}! What would you like to shop for today?")

    # B. Contextual Flow
    
    # -> PRODUCT SELECTION (High Priority if mentioned)
    if product_match:
        session["selected_product"] = product_match
        session["stage"] = STAGE_SELECTED
        p_data = config.get("products", {}).get(product_match)
        
        if not p_data:
            return generate_response(session, f"We have {product_match} in stock! How many would you like?")
        
        card = {"type": "product_detail", "name": p_data.get("display_name", product_match), "price": p_data.get("price", "TBD")}
        return generate_response(session, f"Nice choice! {p_data['display_name']} costs {p_data['price']}. How many would you like?", options=["1", "2", "3", "❌ Cancel"], card=card)

    # -> BROWSING
    if intent == "browse_products" or (session["stage"] == STAGE_IDLE and intent == "unknown"):
        session["stage"] = STAGE_BROWSING
        product_list = config.get("products", {})
        products_str = ", ".join([p["display_name"] for p in product_list.values()])
        return generate_response(session, f"At {business_name}, we have: {products_str}. Which one would you like to see?", options=list(product_list.keys()))

    # -> PRICE CHECK (Contextual)
    if intent == "ask_price" and session["stage"] == STAGE_BROWSING:
         return generate_response(session, f"Which product at {business_name} would you like to check the price for?", options=list(config.get("products", {}).keys()))

    # -> QUANTITY (Step-based FSM)
    if session["stage"] == STAGE_SELECTED:
        qty = extract_quantity_robust(user_input)
        if qty:
            session["quantity"] = qty
            session["stage"] = STAGE_QUANTITY
            p_data = config.get("products", {}).get(session["selected_product"], {})
            p_name = p_data.get("display_name", session["selected_product"])
            
            p_price_str = p_data.get("price", "0").replace("₦", "").replace(",", "").replace("N", "").strip()
            currency = config.get("currency", "₦")
            try:
                total = int(p_price_str) * qty
                session["total"] = total
                return generate_response(session, f"Perfect! {qty} {p_name} will cost {currency}{total:,} (Total).\n\nProceed to checkout?", options=["✅ Checkout", "❌ Cancel"])
            except:
                return generate_response(session, f"Perfect! You want {qty} {p_name}.\n\nProceed to checkout?", options=["✅ Checkout", "❌ Cancel"])

    # -> CHECKOUT
    if session["stage"] == STAGE_QUANTITY:
        if any(w in user_input.lower() for w in ["checkout", "yes", "confirm", "proceed", "ok"]):
            session["stage"] = STAGE_CHECKOUT
            return generate_response(session, "Great! Please provide your Delivery Address and Phone Number to complete the order.", options=["❌ Cancel"])

    # -> ORDER COMPLETE
    if session["stage"] == STAGE_CHECKOUT:
        if len(user_input) > 10:
             session["stage"] = STAGE_IDLE
             session["selected_product"] = None
             session["quantity"] = 0
             return generate_response(session, f"Order Received! 🙌 {business_name} will contact you shortly to confirm delivery. Thank you!", options=["🛍️ Shop Again"])

    # C. Delivery Info
    if any(w in user_input.lower() for w in ["delivery", "ship", "deliver"]):
        delivery_info = config.get("delivery", "We offer nationwide delivery.")
        return generate_response(session, f"Delivery Info 🚚: {delivery_info}\n\nWould you like to browse our products?", options=["🛍️ Browse Products"])

    # 5. ANTI-LOOP FALLBACK SYSTEM
    if session.get("fallback_count", 0) >= 1:
        session["fallback_count"] = 0
        return generate_response(session, f"I'm having a little trouble understanding. 🤔 Maybe try browsing our collection at {business_name}?", options=["🛍️ Browse Products", "💰 Check Prices", "🚚 Delivery Info"])
    
    session["fallback_count"] = session.get("fallback_count", 0) + 1
    return generate_response(session, "I didn't quite catch that. Could you rephrase or pick an option below?")
