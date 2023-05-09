import asyncio
import datetime
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from main.models.notion_models import UserModel, NoteModel, NotionModel, ThemeModel
from main.utils.config import MONGO_TEST_DB_CONNECTION_PATH
from main.utils.exceptons import DBNotFound

logger = logging.getLogger("app.db")


class DbApi:

    async def get_user(self, user_id: int) -> UserModel:
        raise NotImplementedError

    #
    async def get_theme(self, theme_id: int) -> ThemeModel:
        raise NotImplementedError

    #
    async def get_note(self, note_id: int) -> NoteModel:
        raise NotImplementedError

    #
    async def get_notion(self, notion_id: int) -> NotionModel:
        raise NotImplementedError

    #
    async def write_new_user(self, user: UserModel):
        raise NotImplementedError

    #
    async def write_new_theme(self, theme: ThemeModel) -> int:
        raise NotImplementedError

    #
    async def write_new_note(self, note: NoteModel) -> int:
        raise NotImplementedError

    #
    async def write_new_notion(self, notion: NotionModel) -> int:
        raise NotImplementedError

    async def delete_user(self, user_id: int) -> int:
        raise NotImplementedError

    async def delete_theme(self, theme_id: int) -> int:
        raise NotImplementedError

    async def delete_notion(self, notion_id: int) -> int:
        raise NotImplementedError

    async def delete_note(self, note_id: int) -> int:
        raise NotImplementedError

    async def get_all_themes_by_condition(self, condition: dict) -> list[ThemeModel]:
        raise NotImplementedError
    
    async def get_all_notes_by_condition(self, condition: dict) -> list[NoteModel]:
        raise NotImplementedError
    
    async def get_all_notion_by_condition(self, condition: dict) -> list[NotionModel]:
        raise NotImplementedError


class MongoDbApi(DbApi):
    _client: AsyncIOMotorClient
    _collections: dict

    def __init__(self, connection_string, is_test: bool = False):
        self.connect_to_db(connection_string, is_test)

    def connect_to_db(self, connection_string: str, is_test: bool = False) -> None:
        # Connect client
        self._client = AsyncIOMotorClient(connection_string)

        # Connect db
        self._db = self._client.Test if is_test else self._client.Prod

        # Connect collections
        self._collections = {
            "users": self._db.Users,
            "themes": self._db.Themes,
            "notions": self._db.Notions,
            "notes": self._db.Notes
        }

    # ----- Users ----- #
    async def get_user(self, user_id: int) -> UserModel:
        user = await self._collections["users"].find_one({"_id": user_id})
        if user is None:
            logger.error(f"No user found with id: {user_id}")
            raise DBNotFound(f"No user found with id: {user_id}")
        user = UserModel.parse_obj(user)
        return user

    async def write_new_user(self, user: UserModel) -> int:
        """Write new user obj by UserModel in User collection"""
        try:
            inserted_obj = await self._collections["users"].insert_one(user.dict(by_alias=True))
            logger.info(f"Success write user with id: {user.id} to db")
        except DuplicateKeyError as err:
            logger.error(f"Can't write user with id: {user.id}, DuplicateKey: {err}")
            raise err
        else:
            return inserted_obj.inserted_id

    async def delete_user(self, user_id: int) -> int:
        """Delete user from User collection by id
        raise DBNotFound exception if no user with this id in collection"""
        delete_obj = await self._collections["users"].delete_one({"_id": user_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found user with id: {user_id}")
            raise DBNotFound(f"Not found user with id: {user_id}")
        else:
            return user_id

    # ----- Themes ----- #
    async def get_theme(self, theme_id: int) -> ThemeModel:
        theme = await self._collections["themes"].find_one({"_id": theme_id})
        if theme is None:
            logger.error(f"No theme found with id: {theme_id}")
            raise DBNotFound(f"No theme found with id: {theme_id}")
        theme = ThemeModel.parse_obj(theme)
        return theme

    async def write_new_theme(self, theme: ThemeModel) -> int:
        """Write new theme obj by ThemeModel in Theme collection"""
        try:
            inserted_obj = await self._collections["themes"].insert_one(theme.dict(by_alias=True))
            logger.info(f"Success write theme with id: {theme.id} to db")
        except DuplicateKeyError as err:
            logger.error(f"Can't write theme with id: {theme.id}, DuplicateKey: {err}")
            raise err
        else:
            return inserted_obj.inserted_id

    async def get_all_themes_by_condition(self, condition: dict) -> list[ThemeModel]:
        themes = self._collections["themes"].find(condition)
        result = list()
        for theme in await themes.to_list(length=100):
            result.append(ThemeModel.parse_obj(theme))
        if not len(result):
            logger.error(f"No themes found settings condition: {condition}")
            raise DBNotFound(f"No themes found settings condition: {condition}")
        return result

    async def delete_theme(self, theme_id: int) -> int:
        """Delete theme from Theme collection by id
        raise DBNotFound exception if no theme with this id in collection"""
        delete_obj = await self._collections["themes"].delete_one({"_id": theme_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found theme with id: {theme_id}")
            raise DBNotFound
        else:
            return theme_id

    # ----- Notions ----- #
    async def get_notion(self, notion_id: int) -> NotionModel:
        notion = await self._collections["notions"].find_one({"_id": notion_id})
        if notion is None:
            logger.error(f"Not found notion with id: {notion_id}")
            raise DBNotFound(f"Not found notion with id: {notion_id}")
        notion = NotionModel.parse_obj(notion)
        return notion

    async def write_new_notion(self, notion: NotionModel) -> int:
        """Write new notion obj by NotionModel in Notion collection"""
        try:
            inserted_obj = await self._collections["notions"].insert_one(notion.dict(by_alias=True))
            logger.info(f"Success write notion with id: {notion.id} to db")
        except DuplicateKeyError as err:
            logger.error(f"Can't write notion with id: {notion.id}, DuplicateKey: {err}")
            raise err
        else:
            return inserted_obj.inserted_id

    async def get_all_notion_by_condition(self, condition: dict, list_length: int = 100) -> list[NotionModel]:
        notions = self._collections["notions"].find(condition)
        result = list()
        for notion in await notions.to_list(length=list_length):
            result.append(NotionModel.parse_obj(notion))
        if not len(result):
            logger.error(f"No notions found setting conditions: {condition}")
            raise DBNotFound(f"No notions found setting conditions: {condition}")
        return result
    
    async def delete_notion(self, notion_id: int) -> int:
        """Delete notion from Notions collection by id
        raise DBNotFound exception if not notion with this id in collection"""
        delete_obj = await self._collections["notions"].delete_one({"_id": notion_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found notion with id: {notion_id}")
            raise DBNotFound(f"Not found notion with id: {notion_id}")
        else:
            return notion_id

    # ----- Notes ----- #
    async def write_new_note(self, note: NoteModel) -> int:
        """Write new note obj by NoteModel in Note collection"""
        try:
            inserted_obj = await self._collections["notes"].insert_one(note.dict(by_alias=True))
            logger.info(f"Success write note with id: {note.id} to db")
        except DuplicateKeyError as err:
            logger.error(f"Can't write note with id: {note.id}, DuplicateKey: {err}")
            raise err
        else:
            return inserted_obj.inserted_id

    async def get_note(self, note_id: int) -> NoteModel:
        note = await self._collections["notes"].find_one({"_id": note_id})
        if note is None:
            logger.error(f"Not found note with id: {note_id}")
            raise DBNotFound(f"Not found note with id: {note_id}")
        note = NoteModel.parse_obj(note)
        return note

    async def get_all_notes_by_condition(self, condition: dict, list_length: int = 100) -> list[NoteModel]:
        notes = self._collections["notes"].find(condition)
        result = list()
        for note in await notes.to_list(list_length):
            result.append(NoteModel.parse_obj(note))
        if not len(result):
            logger.error(f"No notes found setting conditions: {condition}")
            raise DBNotFound(f"No notes found setting conditions: {condition}")
        return result

    async def delete_note(self, note_id: int) -> int:
        """Delete note from Notes collection by id
        raise DBNotFound exception if not note with this id in collection"""
        delete_obj = await self._collections["notes"].delete_one({"_id": note_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found note with id: {note_id}")
            raise DBNotFound(f"Not found note with id: {note_id}")
        else:
            return note_id
