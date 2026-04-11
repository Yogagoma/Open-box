from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))

    athletes: Mapped[list['Athlete']] = relationship("Athlete", back_populates='plan')
