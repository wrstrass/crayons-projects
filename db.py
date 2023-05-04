import motor.motor_asyncio
import config

client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/"
)

database = client.data
projects_collection = database.projects
