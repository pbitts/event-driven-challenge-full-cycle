from fastapi import FastAPI, HTTPException
from .models import Balance
from .database import SessionLocal
from .populate_db import init_db
from .kafka_consumer import start_consumer

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()
    start_consumer()

@app.get("/balances/{account_id}")
def get_balance(account_id: str):
    db = SessionLocal()
    balance = db.query(Balance).filter_by(account_id=account_id).first()
    db.close()
    if not balance:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": balance.amount}
