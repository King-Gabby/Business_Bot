# Single source of truth for session storage
sessions = {}

def get_default_session(user_id, business_id=None):
    """MANDATORY: Returns the official session schema for the commerce engine."""
    return {
        "user_id": user_id,
        "business_id": business_id,
        "stage": "idle",
        "intent": None,
        "selected_product": None,
        "quantity": 0,
        "cart": [],
        "mode": "bot",
        "last_message": None,
        "context": {},
        "fallback_count": 0
    }
