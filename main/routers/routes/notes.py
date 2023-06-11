from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request

from main.models.notion_models import NoteModel
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.routers.utils.notes import utils_get_all_child_notes, utils_delete_all_child_notes
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


# ----- GET ----- #

@router.get("/get_note_by_id", status_code=status.HTTP_200_OK)
async def get_note_by_id(request: Request, note_id: str | bytes) -> NoteModel:
    """Returns a note by id"""
    db: DbApi = request.app.state.db
    note_id = create_bson_object_by_id(note_id)
    try:
        note = await db.get_note(note_id)
        return note
    except DBNotFound:
        raise HTTPException(status_code=404, detail="Note not found")


@router.get("get_all_child_notes", status_code=status.HTTP_200_OK)
async def get_all_child_notes(request: Request,
                              parent_id: str | bytes,
                              list_length: int = 100) -> list[NoteModel]:
    """
    :param parent_id: 12-byte input or a 24-character hex string |
    :param list_length: length of response list
    :return: all notes by parent_id
    """
    db: DbApi = request.app.state.db
    parent_id = create_bson_object_by_id(parent_id)
    notes = await utils_get_all_child_notes(db=db, parent_id=parent_id, list_length=list_length)
    return notes


# ----- POST ----- #

@router.post("/get_all_notes_by_condition", status_code=status.HTTP_200_OK)
async def get_all_notes_by_condition(request: Request,
                                     condition: dict,
                                     list_length: int = 100
                                     ) -> list[NoteModel]:
    """
    :param condition:
    :param list_length: length of response list
    :return:all notes matched by condition
    """
    db: DbApi = request.app.state.db
    try:
        result = await db.get_all_notes_by_condition(condition, list_length)
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("/set_new_note", status_code=status.HTTP_201_CREATED)
async def set_new_note(request: Request, note: NoteModel) -> str:
    """Write new note to db"""
    db: DbApi = request.app.state.db
    try:
        insert_object_id = await db.write_new_note(note)
        return str(insert_object_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Note with this id already exist")


# ----- DELETE ----- #

@router.delete("/delete_note_by_id", status_code=status.HTTP_200_OK)
async def delete_note_by_id(request: Request, note_id: str | bytes) -> str:
    """Delete note from db"""
    db: DbApi = request.app.state.db
    note_id = create_bson_object_by_id(note_id)
    try:
        deleted_obj_id = await db.delete_note(note_id)
        return str(deleted_obj_id)
    except DBNotFound as err:
        raise HTTPException(status_code=404, detail="Note not found")


@router.delete("delete_all_child_notes", status_code=status.HTTP_200_OK)
async def delete_all_child_notes(request: Request, parent_id: str | bytes) -> int:
    """Delete all notes by parent_id"""
    db: DbApi = request.app.state.db
    parent_id = create_bson_object_by_id(parent_id)
    deleted_count = await utils_delete_all_child_notes(db=db, parent_id=parent_id)
    return deleted_count
