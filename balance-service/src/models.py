from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True)
    amount = Column(Float)
