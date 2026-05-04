from typing import Dict, Any

# In-memory storage for now. Easy to swap for Redis later.
_sessions: Dict[str, Dict[str, Any]] = {}

def get_session_id(user_id: str, business_id: str) -> str:
    return f"{user_id}:{business_id}"

def get_default_session(user_id: str, business_id: str) -> Dict[str, Any]:
    return {
        "user_id": user_id,
        "business_id": business_id,
        "stage": "idle",
        "intent": None,
        "selected_category": None,
        "selected_product": None,
        "quantity": 0,
        "mode": "bot",
        "fallback_count": 0,
        "context": {}
    }

class StateManager:
    def get_session(self, user_id: str, business_id: str) -> Dict[str, Any]:
        sid = get_session_id(user_id, business_id)
        if sid not in _sessions:
            _sessions[sid] = get_default_session(user_id, business_id)
        return _sessions[sid]

    def update_session(self, user_id: str, business_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        session = self.get_session(user_id, business_id)
        session.update(updates)
        return session
        
    def clear_session(self, user_id: str, business_id: str) -> Dict[str, Any]:
        sid = get_session_id(user_id, business_id)
        _sessions[sid] = get_default_session(user_id, business_id)
        return _sessions[sid]

state_manager = StateManager()
