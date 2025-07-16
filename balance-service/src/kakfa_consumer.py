from kafka import KafkaConsumer
from pymongo import MongoClient
import json
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

        DATABASE_URL = os.getenv('DATABASE_URL', "mongodb://root:changeme@balance-mongo")

        mongo_client = MongoClient(DATABASE_URL)
        mongo_database = mongo_client['account']
        collection = mongo_database['balance']

        for message in consumer:
            event = message.value
            account_id_from = str(event['account_id_from'])
            balance_account_id_from = float(event['balance_account_id_from'])
            account_id_to = str(event['account_id_to'])
            balance_account_id_to = float(event['balance_account_id_to'])

            for account_id, amount in [(account_id_from, balance_account_id_from),
                                        (account_id_to, balance_account_id_to)]:
                
                balance = collection.find_one({'account_id':account_id})
                if balance:
                    balance.amount = amount
                else:
                    balance = {'account_id':account_id,'amount': amount}
                    collection.insert_one(balance)
    
    thread = threading.Thread(name='kafka-consumer-daemon', 
                                target=consume, 
                                daemon=True)
    thread.start()
