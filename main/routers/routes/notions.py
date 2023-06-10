from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request

from main.models.notion_models import NotionModel
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/notions",
    tags=["Notions"]
)


@router.get("/get_notion_by_id", status_code=status.HTTP_200_OK)
async def get_notion_by_id(request: Request, notion_id: str | bytes) -> NotionModel:
    db: DbApi = request.app.state.mongo_db
    notion_id = create_bson_object_by_id(notion_id)
    try:
        notion = await db.get_notion(notion_id)
        return notion
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/get_all_notion_by_condition", status_code=status.HTTP_200_OK)
async def get_all_notion_by_condition(request: Request,
                                      condition: dict,
                                      list_length: int = 100
                                      ) -> list[NotionModel]:
    db: DbApi = request.app.state.mongo_db
    try:
        result = await db.get_all_notion_by_condition(condition, list_length)
        return result
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notions not found")


@router.post("/set_new_notion", status_code=status.HTTP_201_CREATED)
async def set_new_notion(request: Request, notion: NotionModel) -> str:
    db: DbApi = request.app.state.mongo_db
    try:
        insert_object_id = await db.write_new_notion(notion)
        return str(insert_object_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Notion with theis id already exist")


@router.delete("/delete_notion_by_id", status_code=status.HTTP_200_OK)
async def delete_notion_by_id(request: Request, notion_id: str | bytes) -> str:
    db: DbApi = request.app.state.mongo_db
    notion_id = create_bson_object_by_id(notion_id)
    try:
        deleted_obj_id = await db.delete_notion(notion_id)
        return str(deleted_obj_id)
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
