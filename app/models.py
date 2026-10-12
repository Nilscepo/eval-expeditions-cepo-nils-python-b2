from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ShipmentDB(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    recipient: Mapped[str] = mapped_column(String, nullable=False)
    weight_g: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="prepared")
    shipping_fee: Mapped[float] = mapped_column(Float, nullable=False)