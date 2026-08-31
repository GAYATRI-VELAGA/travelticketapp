from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date, time
import bcrypt

from database import SessionLocal
from models import User, Ticket, Transaction, Payment


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password: str):
    password_bytes = password.encode("utf-8")

    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    ).decode("utf-8")


# ==========================================
# PASSWORD VERIFICATION
# ==========================================

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Travel Ticket App"
    }


# ==========================================
# DATABASE SESSION
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================
# USER REGISTRATION
# ==========================================

@app.post("/register")
def register_user(
    name: str,
    email: str,
    phone: str,
    password: str,
    db: Session = Depends(get_db)
):

    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ==========================================
# USER LOGIN
# ==========================================

@app.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return {
            "message": "User not found"
        }

    if not verify_password(password, user.password):
        return {
            "message": "Invalid password"
        }

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


# ==========================================
# CREATE TICKET
# ==========================================

@app.post("/tickets")
def create_ticket(
    owner_id: int,
    passenger_name: str,
    from_location: str,
    to_location: str,
    travel_date: date,
    travel_time: time,
    seat_number: str,
    original_price: float,
    db: Session = Depends(get_db)
):

    new_ticket = Ticket(
        owner_id=owner_id,
        passenger_name=passenger_name,
        from_location=from_location,
        to_location=to_location,
        travel_date=travel_date,
        travel_time=travel_time,
        seat_number=seat_number,
        original_price=original_price,
        status="BOOKED"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket_id": new_ticket.id
    }
# ==========================================
# SELL TICKET
# ==========================================

@app.put("/tickets/{ticket_id}/sell")
def sell_ticket(
    ticket_id: int,
    selling_price: float,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        return {
            "message": "Ticket not found"
        }

    if ticket.status != "BOOKED":
        return {
            "message": "Ticket cannot be sold"
        }

    ticket.selling_price = selling_price
    ticket.status = "AVAILABLE"

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket is now available for sale",
        "ticket_id": ticket.id,
        "selling_price": ticket.selling_price,
        "status": ticket.status
    }
    # ==========================================
# VIEW AVAILABLE TICKETS
# ==========================================

@app.get("/tickets/available")
def get_available_tickets(
    db: Session = Depends(get_db)
):
    tickets = db.query(Ticket).filter(
        Ticket.status == "AVAILABLE"
    ).all()

    return tickets
# ==========================================
# BUY TICKET
# ==========================================

@app.post("/tickets/{ticket_id}/buy")
def buy_ticket(
    ticket_id: int,
    buyer_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        return {
            "message": "Ticket not found"
        }

    if ticket.status != "AVAILABLE":
        return {
            "message": "Ticket is not available for purchase"
        }

    ticket.buyer_id = buyer_id
    ticket.status = "SOLD"

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket purchased successfully",
        "ticket_id": ticket.id,
        "buyer_id": ticket.buyer_id,
        "selling_price": ticket.selling_price,
        "status": ticket.status
    }