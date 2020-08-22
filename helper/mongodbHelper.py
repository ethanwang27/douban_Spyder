# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 10:16
@File: mongodbHelper.py
@Project: douban_Spyder
@Description: None
"""

from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URL)
db_spyder = client["spyder"]


class MongoDbHelper(object):

    def __init__(self):
        self.client = MongoClient(config.MONGODB_URL)
        self.db = self.client[config.DB_NAME]

    def exists(self, collection: str, key: str, value: str) -> bool:
        if self.db[collection].find_one({key: value}):
            return True
        else:
            return False

    def update(self, collection: str, filters: dict, updates: dict,
               upsert: bool = False) -> int:

        return self.db[collection].update_one(filter=filters,
                                              update=updates,
                                              upsert=upsert).modified_count

    def update_many(self, collection: str, filters: dict, updates: dict,
                    upsert: bool = False) -> int:
        return self.db[collection].update_many(filter=filters,
                                               update=updates,
                                               upsert=upsert).modified_count

    def insert(self, collection: str, insert_doc: dict) -> str:
        return self.db[collection].insert_one(insert_doc).inserted_id



# def insert(collection_name: str, data: dict) -> str:
#     """
#     保存数据
#     :param collection_name: 集合名称
#     :param data: 需要保存的数据
#     :return: 是否成功
#     """
#     collection = db_spyder[collection_name]
#     result = collection.insert_one(data)
#     return result.inserted_id
#
#
# def find_one(collection_name: str, col: str, value: str):
#     collection = db_spyder[collection_name]
#     result = collection.find_one({col: value})
#     return result
#
#
# def delete_one(collection_name: str, col: str, value: str):
#     colletction = db_spyder[collection_name]
#     colletction.delete_one({col: value})
