from datetime import datetime
import pymongo
import os
from todo_app.models.Item import Item

def get_items():
    with getDbClient() as client:
        client = client[os.getenv('MONGO_DB_NAME')]["todo-items"]
        todoItems = list(client.find({"status": "To Do"}))
        doingItems = list(client.find({"status": "Doing"}))
        doneItems = list(client.find({"status": "Done"}))
        return parseItems(todoItems + doingItems + doneItems)

def change_item_status(itemId, status):
    with getDbClient() as client:
        client = client[os.getenv('MONGO_DB_NAME')]["todo-items"]
        client.update_one({"_id": itemId}, {"$set": {"status": status}})

def delete_item(itemId):
    with getDbClient() as client:
        client = client[os.getenv('MONGO_DB_NAME')]["todo-items"]
        client.delete_one({"_id": itemId})

def create_item(title):
    with getDbClient() as client:
        client = client[os.getenv('MONGO_DB_NAME')]["todo-items"]
        client.insert_one({"status": "To Do", "title": title, "created": datetime.now()})

def parseItems(items):
    returnList = []
    for item in items:
        returnList.append(Item.from_mongo_item(item))
    return returnList

def getDbClient():
    connection_string = os.getenv('MONGO_DB_CONNECTION_STRING')
    return pymongo.MongoClient(connection_string)