from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from engine import handle_user
from state import sessions, get_default_session
from utils import load_business, save_business
from fastapi.middleware.cors import CORSMiddleware
import html
import uuid

app = FastAPI(title="Idayat Thrifts Commerce Platform")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class CreateBusinessRequest(BaseModel):
    business_name: str
    contact: str
    categories: List[str]
    currency: str = "₦"

class AddProductsRequest(BaseModel):
    business_id: str
    products: Dict[str, Dict]

class UpdateBusinessRequest(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    delivery: Optional[str] = None
    products: Optional[Dict[str, Dict]] = None

# --- HELPERS ---
def safe_xml(text: str) -> str:
    return html.escape(text or "")

def get_session(user_id: str, business_id: str):
    session_key = f"{user_id}:{business_id}"
    if session_key not in sessions:
        sessions[session_key] = get_default_session(user_id, business_id)
    return sessions[session_key]

# --- CHAT ENDPOINTS ---
@app.get("/")
def home():
    return {"status": "online", "engine": "Commerce Platform v3.0"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "anonymous")
    message = data.get("message", "")
    business_id = data.get("business_id")
    
    if not business_id:
        raise HTTPException(status_code=400, detail="Missing business_id")
    
    config = load_business(business_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Business '{business_id}' not found")
    
    session = get_session(user_id, business_id)
    
    try:
        response_data = handle_user(message, session, config)
    except Exception as e:
        print("ENGINE ERROR:", e)
        response_data = {"reply": "Sorry, I hit a snag.", "options": ["🛍️ Browse Products"], "state": session}

    if response_data is None:
        return {"reply": "", "state": session, "options": []}

    return response_data

# --- ADMIN ENDPOINTS (Onboarding & Management) ---

@app.post("/create-business")
async def create_business(req: CreateBusinessRequest):
    # Generate unique ID (slugified)
    business_id = req.business_name.lower().replace(" ", "_")
    
    # Check for collisions
    if load_business(business_id):
        business_id = f"{business_id}_{str(uuid.uuid4())[:4]}"
    
    config = {
        "business_id": business_id,
        "name": req.business_name,
        "contact": req.contact,
        "categories": req.categories,
        "currency": req.currency,
        "delivery": "Nationwide delivery available.",
        "products": {}
    }
    
    if save_business(config):
        return {"status": "success", "business_id": business_id, "config": config}
    raise HTTPException(status_code=500, detail="Failed to save business config")

@app.post("/add-products")
async def add_products(req: AddProductsRequest):
    config = load_business(req.business_id)
    if not config:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Merge or replace products
    config["products"].update(req.products)
    
    if save_business(config):
        return {"status": "success", "config": config}
    raise HTTPException(status_code=500, detail="Failed to update products")

@app.get("/business/{business_id}")
async def get_business(business_id: str):
    config = load_business(business_id)
    if not config:
        raise HTTPException(status_code=404, detail="Business not found")
    return config

@app.put("/business/{business_id}")
async def update_business(business_id: str, req: UpdateBusinessRequest):
    config = load_business(business_id)
    if not config:
        raise HTTPException(status_code=404, detail="Business not found")
    
    if req.name: config["name"] = req.name
    if req.contact: config["contact"] = req.contact
    if req.delivery: config["delivery"] = req.delivery
    if req.products is not None: config["products"] = req.products
    
    if save_business(config):
        return {"status": "success", "config": config}
    raise HTTPException(status_code=500, detail="Failed to update config")

# --- WHATSAPP ---
@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_id = form.get("From", "")
    message = form.get("Body", "")
    business_id = "idayat" 

    config = load_business(business_id)
    session = get_session(user_id, business_id)
    response_data = handle_user(message, session, config)

    if response_data is None:
        return Response(content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>', media_type="application/xml")

    text_to_send = response_data.get("reply", "")
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{safe_xml(text_to_send)}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")