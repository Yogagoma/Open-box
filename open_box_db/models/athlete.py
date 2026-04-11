from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from base import Base


class Athlete(Base):
    __tablename__ = 'athletes'

    number: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    phone_number: Mapped[int] = mapped_column(unique=True)
    start: Mapped[date] = mapped_column(Date)

    # Foreign keys
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"))

    # Relationships
    shift: Mapped["Shift"] = relationship("Shift", back_populates="athletes")
    plan: Mapped["Plan"] = relationship("Plan", back_populates="athletes")


