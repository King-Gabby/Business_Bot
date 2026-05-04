from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"status": "online", "engine": "Commerce Platform SaaS v4.0"}
