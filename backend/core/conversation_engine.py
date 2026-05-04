from backend.models.schemas import BusinessSchema, ChatResponse
from backend.core.state_manager import state_manager
from backend.core.intent_parser import intent_parser

class ConversationEngine:
    
    def _build_response(self, reply: str, state: dict, options: list = None, card: dict = None) -> ChatResponse:
        default_options = ["🛍️ Browse Products", "🚚 Delivery Info", "👤 Talk to Human"]
        return ChatResponse(
            reply=reply,
            options=options or default_options,
            state=state,
            card=card,
            ui={
                "show_input": state.get("mode") == "bot",
                "lock_input": state.get("mode") == "human"
            }
        )

    def handle(self, user_id: str, business: BusinessSchema, message: str) -> ChatResponse:
        session = state_manager.get_session(user_id, business.business_id)
        
        # 1. Human Mode Override
        if session["mode"] == "human":
            if any(w in message.lower() for w in ["resume", "bot", "back"]):
                session = state_manager.update_session(user_id, business.business_id, {"mode": "bot", "stage": "idle"})
                return self._build_response(f"Welcome back to {business.name}! I am the bot again. How can I help?", session)
            return ChatResponse(reply="", state=session) # Stay quiet
            
        # 2. Parse Intent
        parsed = intent_parser.parse(message, business)
        session = state_manager.update_session(user_id, business.business_id, {"intent": parsed.intent})
        
        # 3. Global Interrupts
        if parsed.intent == "human_request":
            session = state_manager.update_session(user_id, business.business_id, {"mode": "human"})
            return self._build_response(
                f"I'll connect you with the seller.\nContact them directly: {business.contact}",
                session, options=["🔄 Resume Bot"]
            )
            
        if parsed.intent == "delivery":
            # Answer but DO NOT change stage
            return self._build_response(f"Delivery Info 🚚: {business.delivery}", session)

        if parsed.intent == "greeting":
            session = state_manager.update_session(user_id, business.business_id, {"stage": "idle"})
            return self._build_response(f"Hi 👋 Welcome to {business.name}! What would you like to shop for?", session)
            
        if parsed.intent == "cancel":
            session = state_manager.update_session(user_id, business.business_id, {"stage": "idle", "selected_product": None})
            return self._build_response("No problem! Let's start over.", session)

        # 4. Contextual Flow
        stage = session["stage"]
        
        if parsed.intent == "browse_products" or (stage == "idle" and parsed.intent == "unknown"):
            session = state_manager.update_session(user_id, business.business_id, {"stage": "browsing"})
            p_names = [p.display_name for p in business.products.values()]
            return self._build_response(f"At {business.name}, we have: {', '.join(p_names)}.", session, options=list(business.products.keys()))

        if parsed.intent == "buy":
            # If product is mentioned, jump to product selected
            if parsed.product and parsed.product in business.products:
                session = state_manager.update_session(user_id, business.business_id, {
                    "stage": "product_selected", 
                    "selected_product": parsed.product
                })
                p_data = business.products[parsed.product]
                card = {"type": "product_detail", "name": p_data.display_name, "price": p_data.price}
                
                # Did they also provide quantity?
                if parsed.quantity:
                     session = state_manager.update_session(user_id, business.business_id, {
                         "stage": "quantity", "quantity": parsed.quantity
                     })
                     return self._build_response(f"Perfect! You want {parsed.quantity} {p_data.display_name}.\nProceed to checkout?", session, options=["✅ Checkout", "❌ Cancel"])
                
                return self._build_response(f"Nice choice! {p_data.display_name} costs {p_data.price}. How many would you like?", session, options=["1", "2", "3", "❌ Cancel"], card=card)
                
            # If we are waiting for quantity
            if stage == "product_selected" and parsed.quantity:
                session = state_manager.update_session(user_id, business.business_id, {
                     "stage": "quantity", "quantity": parsed.quantity
                })
                p_name = business.products[session["selected_product"]].display_name
                return self._build_response(f"Got it, {parsed.quantity} {p_name}.\nProceed to checkout?", session, options=["✅ Checkout", "❌ Cancel"])

        # Checkout Flow
        if stage == "quantity" and (parsed.intent == "buy" or "checkout" in message.lower() or "yes" in message.lower()):
            session = state_manager.update_session(user_id, business.business_id, {"stage": "checkout"})
            return self._build_response("Great! Please provide your Delivery Address and Phone Number.", session, options=["❌ Cancel"])
            
        if stage == "checkout" and len(message) > 10:
             session = state_manager.clear_session(user_id, business.business_id)
             return self._build_response(f"Order Received! 🙌 {business.name} will contact you shortly. Thank you!", session, options=["🛍️ Shop Again"])

        # 5. Anti-Loop Fallback
        count = session.get("fallback_count", 0)
        if count >= 1:
            session = state_manager.update_session(user_id, business.business_id, {"fallback_count": 0})
            return self._build_response(f"I'm having a little trouble. 🤔 Try browsing our collection?", session)
            
        session = state_manager.update_session(user_id, business.business_id, {"fallback_count": count + 1})
        return self._build_response("I didn't quite catch that. Could you rephrase or pick an option?", session)

conversation_engine = ConversationEngine()
