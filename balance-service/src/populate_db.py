from database import Base, engine, SessionLocal
from models import Balance

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(Balance).first():
        db.add_all([
            Balance(account_id="f8df753c-3b58-43aa-8016-12aaa4f1ea3e", amount=1000),
            Balance(account_id="0216ea38-524f-4e85-8743-d484a8f7538e", amount=500),
        ])
        db.commit()
    db.close()
