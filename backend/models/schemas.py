from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Product(BaseModel):
    display_name: str
    price: str
    aliases: List[str] = []

class BusinessSchema(BaseModel):
    business_id: str
    name: str
    location: Optional[str] = None
    contact: str
    delivery: Optional[str] = "Nationwide delivery available."
    currency: str = "₦"
    categories: List[str] = []
    products: Dict[str, Product] = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str
    business_id: str

class ChatResponse(BaseModel):
    reply: str
    options: List[str] = []
    state: Dict[str, Any] = {}
    card: Optional[Dict[str, Any]] = None
    ui: Dict[str, bool] = {"show_input": True, "lock_input": False}
