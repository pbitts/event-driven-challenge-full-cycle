from kafka import KafkaConsumer
import json
from .database import SessionLocal
from .models import Balance
import threading
import os

def start_consumer():
    def consume():
        consumer = KafkaConsumer(
            'balances',
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            group_id="balance-service",
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )

        db = SessionLocal()

        for message in consumer:
            event = message.value
            account_id_from = str(event['account_id_from'])
            balance_account_id_from = float(event['balance_account_id_from'])
            account_id_to = str(event['account_id_to'])
            balance_account_id_to = float(event['balance_account_id_to'])

            for account_id, amount in [(account_id_from, balance_account_id_from),
                                        (account_id_to, balance_account_id_to)] 
                balance = db.query(Balance).filter_by(account_id=account_id).first()
                if balance:
                    balance.amount = amount
                else:
                    balance = Balance(account_id=account_id, amount=amount)
                    db.add(balance)
                db.commit()
    
    thread = threading.Thread(name='kafka-consumer-daemon', 
                                target=consume, 
                                daemon=True)
    thread.start()
