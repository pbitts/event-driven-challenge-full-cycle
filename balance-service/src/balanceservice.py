import os

from bson.json_util import dumps
from pymongo import MongoClient


class BalanceService():
    DB_NAME = 'account'
    DB_COLLECTION = 'balance'

    def __init__(self):

        self.database_url = os.getenv('DATABASE_URL', "mongodb://root:changeme@balance-mongo")
        if not self.database_url:
            raise AttributeError('Missing environment variable "DATABASE_URL"!')
        
        self.mongo_client = MongoClient(self.database_url)

    def get_balance(self, account_id: str):

        print(f'Searching balance for account id "{account_id}"...')
        balance = self.search_account(account_id)
        print(f'Balance: {balance}')
        return dumps(balance)

    def search_account( self,
        account_id: str
        ):

        mongo_database = self.mongo_client[BalanceService.DB_NAME]
        collection = mongo_database[BalanceService.DB_COLLECTION]

        return collection.find_one({'account_id':account_id})