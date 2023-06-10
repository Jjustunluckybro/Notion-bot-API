from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field
from datetime import datetime


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        try:
            return cls(v)
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    tg_id: str
    name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }


class NotionModel(BaseModel):
    """Single notion data model"""
    id: Optional[PydanticObjectId] = Field(alias="_id")
    user_id: Optional[PydanticObjectId]
    parent_id: Optional[PydanticObjectId]
    creation_time: datetime
    next_notion_time: datetime | None
    is_repeatable: bool
    description: str | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }


class ThemeModel(BaseModel):
    """Single theme or subTheme data model"""
    id: Optional[PydanticObjectId] = Field(alias="_id")
    is_sub_theme: bool
    parent_id: Optional[PydanticObjectId]
    user_id: Optional[PydanticObjectId]
    name: str
    description: str | None
    content: list[dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }


class CheckPointModel(BaseModel):
    """Single checkpoint data model"""
    text: str
    is_finish: bool
    attachments: list[str] | None
    creation_time: datetime
    notion_id: Optional[PydanticObjectId]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v)
        }


class NoteModel(BaseModel):
    """Single note date model"""
    id: Optional[PydanticObjectId] = Field(alias="_id")
    user_id: Optional[PydanticObjectId]
    name: str
    creation_time: datetime
    notion_id: Optional[PydanticObjectId]
    description: str | None
    attachments: list[str]
    check_points: list[CheckPointModel]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PydanticObjectId: lambda v: str(v)
        }
