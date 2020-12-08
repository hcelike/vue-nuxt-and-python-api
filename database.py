from config import *
import mongoengine

mongoengine.connect(
    db=DATABASE_NAME,
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
)

