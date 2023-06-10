from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request

from main.models.notion_models import NoteModel, PydanticObjectId, UserModel
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id


async def get_user_id_by_tg_id(db: DbApi, tg_id: str) -> PydanticObjectId:
    try:
        user: UserModel = await db.get_user_by_tg_id(tg_id)
        return user.id
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with this id")


