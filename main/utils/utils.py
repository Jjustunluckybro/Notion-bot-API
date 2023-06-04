from bson.errors import InvalidId
from fastapi import HTTPException

from main.models.notion_models import PydanticObjectId


def create_bson_object_by_id(_id: str | bytes) -> PydanticObjectId:
    try:
        return PydanticObjectId(_id)
    except InvalidId as err:
        raise HTTPException(
            status_code=400,
            detail=f"Is not a valid id, it must be a 12-byte input or a 24-character hex string"
        )
