from fastapi import APIRouter, HTTPException
from starlette import status


from main.models.notion_models import NoteModel, PydanticObjectId
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.utils.exceptons import DBNotFound


async def utils_get_all_child_notes(db: DbApi,
                              parent_id: PydanticObjectId,
                              list_length: int = 100) -> list[NoteModel]:
    """"""
    try:
        notes = await db.get_all_notes_by_condition(
            condition={
                "parent_id": parent_id
            },
            list_length=list_length
        )
        return notes
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found child notes")


async def utils_delete_all_child_notes(db: DbApi, parent_id: PydanticObjectId) -> int:
    """"""
    try:
        deleted_count = await db.delete_all_notes_by_condition(
            {
                "parent_id": parent_id
            }
        )
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found child notes")
