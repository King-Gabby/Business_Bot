import json
import os
import shutil
from pydantic import ValidationError
from backend.models.schemas import BusinessSchema

BUSINESS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "businesses")

class BusinessService:
    def __init__(self):
        os.makedirs(BUSINESS_DIR, exist_ok=True)

    def _migrate(self, old_data: dict) -> dict:
        """Migrate older schema versions to current."""
        migrated = {**old_data}
        if "products" not in migrated:
            migrated["products"] = {}
        if "categories" not in migrated:
            migrated["categories"] = []
        if "name" not in migrated and "business_name" in migrated:
            migrated["name"] = migrated["business_name"]
            
        # Ensure products have valid alias lists
        for p_key, p_val in migrated.get("products", {}).items():
            if isinstance(p_val, dict) and "aliases" not in p_val:
                p_val["aliases"] = []
                
        return migrated

    def get_business(self, business_id: str) -> BusinessSchema:
        """Load, migrate (if needed), validate, and return business config."""
        if not business_id:
            return None
            
        config_path = os.path.join(BUSINESS_DIR, f"{business_id}.json")
        
        if not os.path.exists(config_path):
            return None
            
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                
            # Attempt direct validation
            try:
                return BusinessSchema(**data)
            except ValidationError:
                # Need to migrate
                print(f"[BusinessService] Migrating {business_id}.json...")
                backup_path = f"{config_path}.backup"
                if not os.path.exists(backup_path):
                    shutil.copy2(config_path, backup_path)
                
                migrated_data = self._migrate(data)
                
                # Validate migrated
                valid_schema = BusinessSchema(**migrated_data)
                
                # Save back the cleaned/migrated data
                self.save_business(valid_schema)
                return valid_schema
                
        except Exception as e:
            print(f"[ERROR] BusinessService failed to load {business_id}: {e}")
            return None

    def save_business(self, business: BusinessSchema) -> bool:
        """Save a validated BusinessSchema."""
        config_path = os.path.join(BUSINESS_DIR, f"{business.business_id}.json")
        try:
            with open(config_path, 'w') as f:
                f.write(business.model_dump_json(indent=2))
            return True
        except Exception as e:
            print(f"[ERROR] BusinessService failed to save {business.business_id}: {e}")
            return False

# Singleton instance
business_service = BusinessService()
