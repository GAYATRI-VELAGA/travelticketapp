from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Time,
    Numeric
)
from sqlalchemy.sql import func

from database import Base


# ==========================================
# USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# TICKET MODEL
# ==========================================

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    owner_id = Column(
        Integer,
        nullable=False
    )

    passenger_name = Column(
        String(100),
        nullable=False
    )

    from_location = Column(
        String(100),
        nullable=False
    )

    to_location = Column(
        String(100),
        nullable=False
    )

    travel_date = Column(
        Date,
        nullable=False
    )

    travel_time = Column(
        Time,
        nullable=False
    )

    seat_number = Column(
        String(20),
        nullable=False
    )

    original_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    selling_price = Column(
        Numeric(10, 2),
        nullable=True
    )

    status = Column(
        String(20),
        default="BOOKED"
    )

    buyer_id = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# TRANSACTION MODEL
# ==========================================

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ticket_id = Column(
        Integer,
        nullable=False
    )

    seller_id = Column(
        Integer,
        nullable=False
    )

    buyer_id = Column(
        Integer,
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(20),
        default="PENDING"
    )

    transaction_date = Column(
        DateTime,
        server_default=func.now()
    )


# ==========================================
# PAYMENT MODEL
# ==========================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transaction_id = Column(
        Integer,
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=True
    )

    payment_status = Column(
        String(20),
        default="PENDING"
    )

    payment_date = Column(
        DateTime,
        server_default=func.now()
    )