import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import TicketStatus, TicketCategory, TicketPriority

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ticket_code: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    assigned_staff_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=True)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, name="ticket_status"), index=True, nullable=False, default=TicketStatus.NEW)
    category: Mapped[TicketCategory] = mapped_column(Enum(TicketCategory, name="ticket_category"), index=True, nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority, name="ticket_priority"), index=True, nullable=False, default=TicketPriority.MEDIUM)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True,)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)





