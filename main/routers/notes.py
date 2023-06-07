from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette.requests import Request

from main.models.notion_models import NoteModel
from main.data_base.MongoAPI import MongoDbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.get("/get_note_by_id")
async def get_note_by_id(request: Request, note_id: str | bytes) -> NoteModel:
    db: MongoDbApi = request.app.state.mongo_db
    note_id = create_bson_object_by_id(note_id)
    try:
        note = await db.get_note(note_id)
        return note
    except DBNotFound:
        raise HTTPException(status_code=404, detail="Note not found")


@router.post(
    "/get_all_notes_by_condition")  # TODO: What with post method, need "get", but in get can not use body
async def get_all_notes_by_condition(request: Request,
                                     condition: dict,
                                     list_length: int = 100
                                     ) -> list[NoteModel]:
    """

    :param request:
    :param condition:
    :param list_length:
    :return:
    """
    db: MongoDbApi = request.app.state.mongo_db
    try:
        result = await db.get_all_notes_by_condition(condition, list_length)
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.post("/set_new_note")
async def set_new_note(request: Request, note: NoteModel) -> str:
    db: MongoDbApi = request.app.state.mongo_db
    try:
        insert_object_id = await db.write_new_note(note)
        return str(insert_object_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Note with this id already exist")


@router.delete("/delete_note_by_id")
async def delete_note_by_id(request: Request, note_id: str | bytes) -> str:
    db: MongoDbApi = request.app.state.mongo_db
    note_id = create_bson_object_by_id(note_id)
    try:
        deleted_obj_id = await db.delete_note(note_id)
        return str(deleted_obj_id)
    except DBNotFound as err:
        raise HTTPException(status_code=404, detail=str(err))
