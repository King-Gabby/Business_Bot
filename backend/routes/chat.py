from fastapi import APIRouter, HTTPException, Request, Response
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.business_service import business_service
from backend.core.conversation_engine import conversation_engine
from backend.core.state_manager import state_manager
import html

router = APIRouter()

def safe_xml(text: str) -> str:
    return html.escape(text or "")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Tenant Isolation: Load Business
    business = business_service.get_business(request.business_id)
    if not business:
        raise HTTPException(status_code=404, detail=f"Business '{request.business_id}' not found")
        
    # 2. Process through Engine
    try:
        response = conversation_engine.handle(request.user_id, business, request.message)
        return response
    except Exception as e:
        print(f"[CHAT ERROR] {e}")
        # Fallback to avoid crashing the frontend
        session = state_manager.get_session(request.user_id, business.business_id)
        return ChatResponse(
            reply="Sorry, I hit a snag. Let's start over.", 
            options=["🛍️ Browse Products"],
            state=session
        )

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_id = form.get("From", "")
    message = form.get("Body", "")
    # In a real SaaS, the webhook URL would contain the tenant ID (e.g., /whatsapp/{business_id})
    # For now, default to idayat or extract if we change the route.
    business_id = "idayat" 
    
    business = business_service.get_business(business_id)
    if not business:
        return Response(content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>', media_type="application/xml")

    response_data = conversation_engine.handle(user_id, business, message)
    
    text_to_send = response_data.reply
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{safe_xml(text_to_send)}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")

# Admin / Initialization Endpoint
@router.get("/init/{business_id}", response_model=ChatResponse)
async def init_chat(business_id: str):
    """Called by frontend on load to get the custom welcome message."""
    business = business_service.get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    # We pass an empty string to trigger greeting/idle state
    response = conversation_engine.handle("anonymous_init", business, "hello")
    return response
