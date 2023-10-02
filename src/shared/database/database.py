import os
import pymongo

class Database:
    def __init__(self):
        user = os.getenv('MONGODB_USER')
        password = os.getenv('MONGODB_PASSWORD')
        credentials = f"mongodb+srv://{user}:{password}@apaeleilaoimt.vv5d9ja.mongodb.net/?retryWrites=true&w=majority"
        self.__database_connection = pymongo.MongoClient(credentials).get_database('apaeleilaoimt')

    def get_table_user(self):
        table = self.__database_connection['user']
        return table

    def get_table_auction(self):
        table = self.__database_connection['auction']
        return table
