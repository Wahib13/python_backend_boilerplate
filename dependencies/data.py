import logging
import os

import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from models import OMC

logger = logging.getLogger(__name__)

MONGO_STR = f'mongodb://{os.environ.get("MONGO_INITDB_USER")}:' \
            f'{os.environ.get("MONGO_INITDB_PWD")}@mongo:27017/{os.environ.get("MONGO_INITDB_DATABASE_PROJECT")}' \
            f'?authSource=admin&retryWrites=true&w=majority'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_STR)
db = client.get_default_database()
omc_collection = db['omcs']
users_collection = db['users']


async def query_omcs():
    return await omc_collection.find().to_list(1000)


async def query_omc(omc_id: str):
    try:
        omc = await omc_collection.find_one({"_id": ObjectId(omc_id)})
        return omc
    except:
        logger.exception(f'failed to query OMC with id: {omc_id}')


async def query_create_omc(omc: OMC):
    omc = jsonable_encoder(omc)
    new_omc = await omc_collection.insert_one(omc)
    created_omc = await omc_collection.find_one({"_id": new_omc.inserted_id})
    return created_omc


async def query_delete_omc(_id: str):
    delete_result = await omc_collection.delete_one({"_id": ObjectId(_id)})
    return delete_result.deleted_count


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
