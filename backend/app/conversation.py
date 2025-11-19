from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class ConversationState:
    stage: str = "ASK_PRODUCT"
    product_name: str | None = None
    user_name: str | None = None
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConversationResponse:
    reply: str
    is_complete: bool = False

    product_name: str | None = None
    user_name: str | None = None
    product_review: str | None = None


class ConversationManager:
    def __init__(self, expiry_minutes: int = 30) -> None:
        self._states: dict[str, ConversationState] = defaultdict(ConversationState)
        self._expiry = timedelta(minutes=expiry_minutes)

    def _cleanup(self) -> None:
        cutoff = datetime.utcnow() - self._expiry
        expired_numbers = [
            number for number, state in self._states.items() if state.last_updated < cutoff
        ]
        for number in expired_numbers:
            self._states.pop(number, None)

    def handle_message(self, contact_number: str, message: str) -> ConversationResponse:
        self._cleanup()
        state = self._states[contact_number]
        state.last_updated = datetime.utcnow()
        normalized = (message or "").strip()

        if state.stage == "ASK_PRODUCT":
            if not normalized:
                return ConversationResponse("Which product is this review for?")
            state.product_name = normalized
            state.stage = "ASK_NAME"
            return ConversationResponse("What's your name?")

        if state.stage == "ASK_NAME":
            if not normalized:
                return ConversationResponse("Please share your name so we can record the review.")
            state.user_name = normalized
            state.stage = "ASK_REVIEW"
            return ConversationResponse(f"Please send your review for {state.product_name}.")

        if state.stage == "ASK_REVIEW":
            if not normalized:
                return ConversationResponse(
                    f"Please send the review for {state.product_name} when you're ready."
                )
            response = ConversationResponse(
                reply=f"Thanks {state.user_name} -- your review for {state.product_name} has been recorded.",
                is_complete=True,
                product_name=state.product_name,
                user_name=state.user_name,
                product_review=normalized,
            )
            # reset conversation
            self._states.pop(contact_number, None)
            return response

        # default fallback
        self._states.pop(contact_number, None)
        return ConversationResponse("Let's start over. Which product is this review for?")


conversation_manager = ConversationManager()

