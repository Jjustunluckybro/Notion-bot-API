from pydantic import BaseModel, Field
from datetime import datetime


class UserModel(BaseModel):
    id: int = Field(alias="_id")
    tg_id: str
    name: str

    # class Config:
    #     fields = {"id": "_id"}


class NotionModel(BaseModel):
    """Single notion data model"""
    id: int = Field(alias="_id")
    user_id: int
    parent_id: int
    creation_time: datetime
    next_notion_time: datetime
    is_repeatable: bool
    description: str | None


class ThemeModel(BaseModel):
    """Single theme or subTheme data model"""
    id: int = Field(alias="_id")
    is_sub_theme: bool
    parent_id: int | None
    user_id: int
    name: str
    description: str | None
    content: list[dict]


class CheckPointModel(BaseModel):
    """Single checkpoint data model"""
    text: str
    is_finish: bool
    attachments: list[str] | None
    creation_time: datetime
    notion_id: int | None


class NoteModel(BaseModel):
    """Single note date model"""
    id: int = Field(alias="_id")
    user_id: int
    name: str
    creation_time: datetime
    notion_id: int
    description: str | None
    attachments: list[str]
    check_points: list[CheckPointModel]
