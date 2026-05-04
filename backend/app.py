from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import health, chat

app = FastAPI(title="SaaS Commerce Platform", version="4.0")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
app.include_router(health.router)
app.include_router(chat.router)