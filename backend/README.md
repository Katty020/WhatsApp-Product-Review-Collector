## Backend Setup

1. Create `.env/backend.env` (folder already exists at project root) with:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:<password>@db.supabase.co:5432/postgres
   TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=whatsapp:+1415XXXXXXX
   ALLOWED_ORIGINS=http://localhost:3000
   ```
2. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Point the Twilio WhatsApp sandbox webhook to `https://<ngrok-host>/webhooks/twilio`.

