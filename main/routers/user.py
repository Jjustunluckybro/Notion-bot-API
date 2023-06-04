from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette.requests import Request

from main.models.notion_models import UserModel, NoteModel, NotionModel, ThemeModel, PydanticObjectId
from main.data_base.MongoAPI import MongoDbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/get_user_by_id")
async def get_user_by_id(request: Request, _id: str | bytes) -> UserModel:
    db: MongoDbApi = request.app.state.mongo_db
    _id = create_bson_object_by_id(_id)
    try:
        user = await db.get_user_by_id(_id)
        return user
    except DBNotFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/get_user_by_tg_id")
async def get_user_by_tg_id(request: Request, tg_id: str) -> UserModel:
    db: MongoDbApi = request.app.state.mongo_db
    try:
        user = await db.get_user_by_tg_id(tg_id)
        return user
    except DBNotFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/set_new_user")
async def set_new_user(request: Request, user: UserModel) -> str:
    db: MongoDbApi = request.app.state.mongo_db
    try:
        insert_object = await db.write_new_user(user)
        return str(insert_object)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User already exist")
