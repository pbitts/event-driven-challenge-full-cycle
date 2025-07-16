import os

from pymongo import MongoClient


def init_db():
    DATABASE_URL = os.getenv('DATABASE_URL', "mongodb://root:changeme@balance-mongo")

    mongo_client = MongoClient(DATABASE_URL)
    mongo_database = mongo_client['account']
    collection = mongo_database['balance']

    docs = [
        {'account_id': "f8df753c-3b58-43aa-8016-12aaa4f1ea3e",
        'amount': 10000},
        {'account_id': "0216ea38-524f-4e85-8743-d484a8f7538e",
        'amount': 10124}
    ]

    response = collection.insert_many(docs)
    print(response)
