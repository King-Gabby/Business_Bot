import json
import os

BUSINESS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "businesses")

def load_business(business_id: str):
    """
    Dynamic Business Loader: Loads configuration from /data/businesses/
    """
    if not business_id:
        return None
        
    config_path = os.path.join(BUSINESS_DIR, f"{business_id}.json")
    
    if not os.path.exists(config_path):
        return None
        
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load business {business_id}: {e}")
        return None

def save_business(config: dict):
    """
    Saves or updates a business configuration file.
    """
    business_id = config.get("business_id")
    if not business_id:
        return False
        
    config_path = os.path.join(BUSINESS_DIR, f"{business_id}.json")
    
    # Ensure directory exists
    os.makedirs(BUSINESS_DIR, exist_ok=True)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save business {business_id}: {e}")
        return False
