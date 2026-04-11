from sqlalchemy import String, Date, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from .enum.Type_Employee import TypeEmployee
from base import Base


class Employee(Base):
    __tablename__ = 'employee'

    number: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    user_name: Mapped[str] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    phone_number: Mapped[int] = mapped_column(unique=True)
    salary_per_month: Mapped[float] = mapped_column(Float(5))
    paid: Mapped[bool] = mapped_column()
    start_date: Mapped[date] = mapped_column(Date)

    Type: Mapped['TypeEmployee'] = mapped_column(Enum(TypeEmployee), nullable=False)

