# Business Bot 🤖

An AI-powered sales and customer service assistant designed for Nigerian commerce. This platform allows businesses to onboard, manage products, and provide a conversational shopping experience for their customers.

## ✨ Features

- **Multi-Store Architecture**: Support for multiple businesses with isolated contexts.
- **AI Intent Extraction**: Understands Nigerian slang and informal speech using GPT-mini.
- **Product Management**: Built-in endpoints for onboarding businesses and managing inventory.
- **WhatsApp Integration**: Ready-to-use webhook for Twilio/WhatsApp integration.
- **Modern UI**: Clean React frontend for chatting and business management.

## 🛠 Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework.
- **OpenAI**: Intent extraction and conversational logic.
- **Pydantic**: Robust data validation and modeling.

### Frontend
- **React + Vite**: Fast and modern web interface.
- **Tailwind CSS**: Sleek, responsive design.
- **Zustand**: Lightweight state management.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key

### Local Setup

#### 1. Clone the repository
```bash
git clone https://github.com/King-Gabby/Business_Bot.git
cd Business_Bot
```

#### 2. Backend Setup
```bash
# Create a virtual environment
python -m venv bot_env
source bot_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
uvicorn backend.app:app --reload
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Deployment

### Backend (Render)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

## 📄 License
MIT
