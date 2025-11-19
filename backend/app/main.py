from fastapi import Depends, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.twiml.messaging_response import MessagingResponse

from .config import settings
from .conversation import conversation_manager
from .database import get_db_session
from .models import Review
from .schemas import ReviewOut

app = FastAPI(title="WhatsApp Product Review Collector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/reviews", response_model=list[ReviewOut])
async def list_reviews(session: AsyncSession = Depends(get_db_session)) -> list[ReviewOut]:
    result = await session.execute(select(Review).order_by(Review.created_at.desc()))
    return list(result.scalars().all())


@app.post("/webhooks/twilio")
async def twilio_webhook(
    from_number: str = Form(..., alias="From"),
    message_body: str = Form("", alias="Body"),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    convo_response = conversation_manager.handle_message(from_number, message_body)

    if convo_response.is_complete:
        stmt = (
            insert(Review)
            .values(
                contact_number=from_number,
                user_name=convo_response.user_name,
                product_name=convo_response.product_name,
                product_review=convo_response.product_review,
            )
            .returning(Review)
        )
        await session.execute(stmt)
        await session.commit()

    twilio_response = MessagingResponse()
    twilio_response.message(convo_response.reply)
    return Response(content=str(twilio_response), media_type="application/xml")


@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

