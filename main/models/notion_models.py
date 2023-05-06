from pydantic import BaseModel
from datetime import datetime


class UserModel(BaseModel):
    _id: int
    tg_name: str
    name: str


class NotionModel(BaseModel):
    """Single notion data model"""
    _id: int
    user_id: int
    parent_id: int
    creation_time: datetime
    next_notion_time: datetime
    is_repeatable: bool
    description: str | None


class ThemeModel(BaseModel):
    """Single theme or subTheme data model"""
    _id: int
    is_sub_theme: bool
    parent_id: int
    user_id: int
    name: str
    description: str | None
    content: list[dict[int: str]]


class CheckPointModel(BaseModel):
    """Single checkpoint data model"""
    text: str
    is_finish: bool
    attachments: list[str] | None
    creation_time: datetime
    notion_id: int | None


class NoteModel(BaseModel):
    """Single note date model"""
    _id: int
    user_id: int
    name: str
    creation_time: datetime
    notion_id: int
    description: str | None
    attachments: list[str]
    check_points: CheckPointModel
