from contextlib import asynccontextmanager
from typing import Literal, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.rules import shipping_fee
from app.schemas import Shipment, ShipmentCreate, Stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Suivi des expeditions", lifespan=lifespan)


@app.post("/shipments", response_model=Shipment, status_code=201)
def create_shipment(data: ShipmentCreate, db: Session = Depends(get_db)):
    shipment = models.ShipmentDB(
        reference=data.reference,
        recipient=data.recipient,
        weight_g=data.weight_g,
        status="prepared",
        shipping_fee=shipping_fee(data.weight_g),
    )
    db.add(shipment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cette reference existe deja")
    db.refresh(shipment)
    return shipment


@app.get("/shipments", response_model=list[Shipment])
def list_shipments(
    status: Optional[Literal["prepared", "shipped"]] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(models.ShipmentDB).order_by(models.ShipmentDB.id)
    if status is not None:
        query = query.where(models.ShipmentDB.status == status)
    return db.scalars(query).all()


@app.post("/shipments/{shipment_id}/dispatch", response_model=Shipment)
def dispatch_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.get(models.ShipmentDB, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Colis introuvable")
    if shipment.status == "shipped":
        raise HTTPException(status_code=409, detail="Colis deja expedie")
    shipment.status = "shipped"
    db.commit()
    db.refresh(shipment)
    return shipment


@app.get("/stats", response_model=Stats)
def get_stats(db: Session = Depends(get_db)):
    S = models.ShipmentDB
    prepared = db.scalar(select(func.count()).select_from(S).where(S.status == "prepared"))
    shipped = db.scalar(select(func.count()).select_from(S).where(S.status == "shipped"))
    total = db.scalar(select(func.coalesce(func.sum(S.shipping_fee), 0.0)))
    return Stats(
        prepared_count=prepared or 0,
        shipped_count=shipped or 0,
        total_shipping_fees=round(total or 0.0, 2),
    )