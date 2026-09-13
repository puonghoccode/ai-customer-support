import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import (Sentiment, TicketCategory, TicketPriority)

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ticket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tickets.id"), unique=True, index=True, nullable=False)
    suggested_category: Mapped[TicketCategory] = mapped_column(Enum(TicketCategory, name="ai_ticket_category"), nullable=False)
    sentiment: Mapped[Sentiment] = mapped_column(Enum(Sentiment, name="sentiment"), nullable=False)
    suggested_priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority, name="ai_ticket_priority"), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)