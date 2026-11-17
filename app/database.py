import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Float, DateTime, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./market_prices.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class MarketPrice(Base):
    __tablename__ = "market_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country: Mapped[str] = mapped_column(String(80), default="South Africa")
    market_name: Mapped[str] = mapped_column(String(120), index=True)
    commodity: Mapped[str] = mapped_column(String(80), index=True)
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(8), default="ZAR")
    unit: Mapped[str] = mapped_column(String(20), default="kg")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    verified: Mapped[bool] = mapped_column(default=False)

class USSDSession(Base):
    __tablename__ = "ussd_sessions"
    session_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    language: Mapped[str] = mapped_column(String(8), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

def init_db():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalar(select(MarketPrice.id).limit(1)) is None:
            # Clearly labelled illustrative hackathon data, NOT live market quotes.
            demo = [
                ("Cape Town Fresh Produce Market", "Tomatoes", 12.50),
                ("Johannesburg Fresh Produce Market", "Tomatoes", 15.00),
                ("Durban Fresh Produce Market", "Tomatoes", 13.00),
                ("Cape Town Fresh Produce Market", "Maize", 4.80),
                ("Johannesburg Fresh Produce Market", "Maize", 5.20),
                ("Durban Fresh Produce Market", "Maize", 4.60),
                ("Cape Town Fresh Produce Market", "Potatoes", 8.00),
                ("Johannesburg Fresh Produce Market", "Potatoes", 9.50),
                ("Durban Fresh Produce Market", "Potatoes", 8.50),
            ]
            for market, commodity, price in demo:
                db.add(MarketPrice(
                    market_name=market, commodity=commodity, price=price,
                    currency="ZAR", unit="kg", verified=False
                ))
            db.commit()

def get_prices(commodity: str):
    with SessionLocal() as db:
        return list(db.scalars(
            select(MarketPrice).where(MarketPrice.commodity == commodity)
            .order_by(MarketPrice.price.desc())
        ))

def get_best_price(commodity: str):
    rows = get_prices(commodity)
    return rows[0] if rows else None
