from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request

from main.models.notion_models import ThemeModel
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/themes",
    tags=["Themes"]
)


@router.get("/get_theme_by_id", status_code=status.HTTP_200_OK)
async def get_theme_by_id(request: Request, theme_id: str | bytes) -> ThemeModel:
    db: DbApi = request.app.state.mongo_db
    theme_id = create_bson_object_by_id(theme_id)
    try:
        theme = await db.get_theme(theme_id)
        return theme
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")


@router.post("/set_new_theme", status_code=status.HTTP_201_CREATED)
async def set_new_theme(request: Request, theme: ThemeModel) -> str:
    db: DbApi = request.app.state.mongo_db
    try:
        insert_object_id = await db.write_new_theme(theme)
        return str(insert_object_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
