import os, json
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId # For querying by _id
import certifi # Make sure to import certifi

class MongoDB:
    def __init__(self):
        try:
            client = MongoClient(os.environ["MONGODB_URL"], tlsCAFile=certifi.where())
            client.admin.command('ismaster')
            print("MongoDB connection successful!")
            self.collection = client[os.environ["MONGODB_NAME"]]["cheese"]
        except ConnectionFailure:
            print("MongoDB connection failed!")
            return None

    def update(self):
        with open(os.environ["RECORDS_JSON"], "rb") as f:
            records = json.load(f)

        skus = [rec["metadata"]["sku"] for rec in records]

        for rec in records:
            self.collection.update_one({"sku": rec["metadata"]["sku"]}, {"$set": rec["metadata"]}, upsert=True)

        self.collection.delete_many({"sku": {"$nin": skus}})

    def get_skus(self, query, sort, limit):
        result = self.collection.find(query)
        if len(sort):
            result = result.sort(sort)
        result = result.limit(limit)
        try:
            skus = [r["sku"] for r in list(result)]
        except:
            skus = []

        return skus

    def aggregate(self, pipeline):
        result = self.collection.aggregate(pipeline)
        res = list(result)
        try:
            skus = [r["sku"] for r in res]
            flag = True
        except:
            skus = res
            flag = False
        return skus, flag

        



