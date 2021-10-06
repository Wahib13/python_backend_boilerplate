import logging
import os

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from models import Person, PersonIn, Item

logger = logging.getLogger(__name__)

MONGO_STR = f'mongodb://{os.environ.get("MONGO_INITDB_USER")}:' \
            f'{os.environ.get("MONGO_INITDB_PWD")}@mongo:27017/{os.environ.get("MONGO_INITDB_DATABASE")}' \
            f'?retryWrites=true&w=majority'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_STR)
db = client.get_default_database()
item_collection = db['items']


async def query_items():
    return await item_collection.find().to_list(1000)


async def query_item(_id: str):
    try:
        return await item_collection.find_one({"_id": ObjectId(_id)})
    except:
        logger.exception(f'failed to query UMF endpoint with id: {_id}')


async def query_create_item(item: Item):
    item = jsonable_encoder(item)
    new_item = await item_collection.insert_one(item)
    created_item = await item_collection.find_one({"_id": new_item.inserted_id}, {'_id': 0})
    return created_item


async def query_delete_item(_id: str):
    delete_result = await item_collection.delete_one({"_id": ObjectId(_id)})
    return delete_result.deleted_count
