import logging
import os

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from models import Person, PersonIn

logger = logging.getLogger(__name__)

MONGO_STR = f'mongodb://{os.environ.get("MONGO_INITDB_USER")}:' \
            f'{os.environ.get("MONGO_INITDB_PWD")}@mongo:27017/{os.environ.get("MONGO_INITDB_DATABASE")}' \
            f'?retryWrites=true&w=majority'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_STR)
db = client.get_default_database()
item_collection = db[os.environ.get('ITEM_COLLECTION')]

async def query_items():
    return await item_collection.find().to_list(1000)


async def query_item(_id: str):
    try:
        return await item_collection.find_one({"_id": ObjectId(_id)})
    except:
        logger.exception(f'failed to query UMF endpoint with id: {_id}')


async def query_create_item(umf_endpoint_in: PersonIn):
    umf_endpoint_in = jsonable_encoder(umf_endpoint_in)
    new_umf_endpoint = await item_collection.insert_one(umf_endpoint_in)
    created_umf_endpoint = await item_collection.find_one({"_id": new_umf_endpoint.inserted_id})
    return created_umf_endpoint


async def query_delete_item(_id: str):
    delete_result = await item_collection.delete_one({"_id": ObjectId(_id)})
    return delete_result.deleted_count
