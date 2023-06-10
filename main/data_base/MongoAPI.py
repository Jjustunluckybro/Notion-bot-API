import logging

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from main.models.notion_models import UserModel, NoteModel, NotionModel, ThemeModel
from main.utils.exceptons import DBNotFound

logger = logging.getLogger("app.db")


class DbApi:

    async def get_user_by_id(self, user_id: ObjectId) -> UserModel:
        raise NotImplementedError

    async def get_user_by_tg_id(self, user_id: str) -> UserModel:
        raise NotImplementedError

    async def get_theme(self, theme_id: ObjectId) -> ThemeModel:
        raise NotImplementedError

    #
    async def get_note(self, note_id: ObjectId) -> NoteModel:
        raise NotImplementedError

    #
    async def get_notion(self, notion_id: ObjectId) -> NotionModel:
        raise NotImplementedError

    #
    async def write_new_user(self, user: UserModel):
        raise NotImplementedError

    #
    async def write_new_theme(self, theme: ThemeModel) -> ObjectId:
        raise NotImplementedError

    #
    async def write_new_note(self, note: NoteModel) -> ObjectId:
        raise NotImplementedError

    #
    async def write_new_notion(self, notion: NotionModel) -> ObjectId:
        raise NotImplementedError

    async def delete_user(self, user_id: ObjectId) -> ObjectId:
        raise NotImplementedError

    async def delete_theme(self, theme_id: ObjectId) -> ObjectId:
        raise NotImplementedError

    async def delete_notion(self, notion_id: ObjectId) -> ObjectId:
        raise NotImplementedError

    async def delete_note(self, note_id: ObjectId) -> ObjectId:
        raise NotImplementedError

    async def delete_all_themes_by_condition(self, condition: dict) -> int:
        raise NotImplementedError

    async def delete_all_notes_by_condition(self, condition: dict) -> int:
        raise NotImplementedError

    async def delete_all_notion_by_condition(self, condition: dict) -> int:
        raise NotImplementedError

    async def get_all_themes_by_condition(self, condition: dict, list_length: int = 100) -> list[ThemeModel]:
        raise NotImplementedError

    async def get_all_notes_by_condition(self, condition: dict, list_length: int = 100) -> list[NoteModel]:
        raise NotImplementedError

    async def get_all_notion_by_condition(self, condition: dict, list_length: int = 100) -> list[NotionModel]:
        raise NotImplementedError


class MongoDbApi(DbApi):
    _client: AsyncIOMotorClient
    _collections: dict

    def connect_to_db(self, connection_string: str, is_test: bool = False) -> bool:
        try:
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
        except Exception as err:
            logger.error(f"db connection error: {str(err)}")
            return False
        return True

    # ----- Utils ----- #
    @staticmethod
    def validate_dict(data: UserModel | NoteModel | ThemeModel | NotionModel) -> dict:
        if data.id is None:
            data = data.dict(by_alias=True)
            data.pop("_id")
            return data
        else:
            return data.dict(by_alias=True)

    # ----- Users ----- #
    async def get_user_by_id(self, user_id: ObjectId) -> UserModel:
        user = await self._collections["users"].find_one({"_id": user_id})
        if user is None:
            logger.error(f"No user found with id: {user_id}")
            raise DBNotFound(f"No user found with id: {user_id}")
        user = UserModel.parse_obj(user)
        return user

    async def get_user_by_tg_id(self, user_tg_id: str) -> UserModel:
        user = await self._collections["users"].find_one({"tg_id": user_tg_id})
        if user is None:
            logger.error(f"No user found with tg_id: {user_tg_id}")
            raise DBNotFound(f"No user found with tg_id: {user_tg_id}")
        user = UserModel.parse_obj(user)
        return user

    async def write_new_user(self, user: UserModel) -> ObjectId:
        """Write new user obj by UserModel in User collection"""
        user = self.validate_dict(user)
        inserted_obj = await self._collections["users"].insert_one(user)
        logger.info(f"Success write user with id: {inserted_obj.inserted_id} to db")
        return inserted_obj.inserted_id

    async def delete_user(self, user_id: ObjectId) -> ObjectId:
        """Delete user from User collection by id
        raise DBNotFound exception if no user with this id in collection"""
        delete_obj = await self._collections["users"].delete_one({"_id": user_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found user with id: {user_id}")
            raise DBNotFound(f"Not found user with id: {user_id}")
        else:
            return user_id

    # ----- Themes ----- #
    async def get_theme(self, theme_id: ObjectId) -> ThemeModel:
        theme = await self._collections["themes"].find_one({"_id": theme_id})
        if theme is None:
            logger.error(f"No theme found with id: {theme_id}")
            raise DBNotFound(f"No theme found with id: {theme_id}")
        theme = ThemeModel.parse_obj(theme)
        return theme

    async def write_new_theme(self, theme: ThemeModel) -> ObjectId:
        """Write new theme obj by ThemeModel in Theme collection"""
        theme = self.validate_dict(theme)
        inserted_obj = await self._collections["themes"].insert_one(theme)
        logger.info(f"Success write theme with id: {str(inserted_obj.inserted_id)} to db")
        return inserted_obj.inserted_id

    async def get_all_themes_by_condition(self, condition: dict, list_length: int = 100) -> list[ThemeModel]:
        themes = self._collections["themes"].find(condition)
        result = list()
        for theme in await themes.to_list(length=list_length):
            result.append(ThemeModel.parse_obj(theme))
        if not len(result):
            logger.error(f"No themes found settings condition: {condition}")
            raise DBNotFound(f"No themes found settings condition: {condition}")
        return result

    async def delete_theme(self, theme_id: ObjectId) -> ObjectId:
        """Delete theme from Theme collection by id
        raise DBNotFound exception if no theme with this id in collection"""
        delete_obj = await self._collections["themes"].delete_one({"_id": theme_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found theme with id: {theme_id}")
            raise DBNotFound
        else:
            return theme_id

    async def delete_all_themes_by_condition(self, condition: dict) -> int:
        """"""
        themes = await self._collections["themes"].delete_many(condition)
        if themes.deleted_count == 0:
            logger.error(f"No themes found settings condition: {condition}")
            raise DBNotFound(f"No themes found settings condition: {condition}")
        return themes.deleted_count

    # ----- Notions ----- #
    async def get_notion(self, notion_id: ObjectId) -> NotionModel:
        notion = await self._collections["notions"].find_one({"_id": notion_id})
        if notion is None:
            logger.error(f"Not found notion with id: {notion_id}")
            raise DBNotFound(f"Not found notion with id: {notion_id}")
        notion = NotionModel.parse_obj(notion)
        return notion

    async def write_new_notion(self, notion: NotionModel) -> ObjectId:
        """Write new notion obj by NotionModel in Notion collection"""
        notion = self.validate_dict(notion)
        inserted_obj = await self._collections["notions"].insert_one(notion)
        logger.info(f"Success write notion with id: {str(inserted_obj.inserted_id)} to db")
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

    async def delete_notion(self, notion_id: ObjectId) -> ObjectId:
        """Delete notion from Notions collection by id
        raise DBNotFound exception if not notion with this id in collection"""
        delete_obj = await self._collections["notions"].delete_one({"_id": notion_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found notion with id: {notion_id}")
            raise DBNotFound(f"Not found notion with id: {notion_id}")
        else:
            return notion_id

    async def delete_all_notion_by_condition(self, condition: dict) -> int:
        """"""
        notions = await self._collections["notions"].delete_many(condition)
        if notions.deleted_count == 0:
            logger.error(f"No notions found settings condition: {condition}")
            raise DBNotFound(f"No notions found settings condition: {condition}")
        return notions.deleted_count
    # ----- Notes ----- #
    async def write_new_note(self, note: NoteModel) -> ObjectId:
        """Write new note obj by NoteModel in Note collection"""
        note = self.validate_dict(note)
        inserted_obj = await self._collections["notes"].insert_one(note)
        logger.info(f"Success write note with id: {str(inserted_obj.inserted_id)} to db")
        return inserted_obj.inserted_id

    async def get_note(self, note_id: ObjectId) -> NoteModel:
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

    async def delete_note(self, note_id: ObjectId) -> ObjectId:
        """Delete note from Notes collection by id
        raise DBNotFound exception if not note with this id in collection"""
        delete_obj = await self._collections["notes"].delete_one({"_id": note_id})

        if not delete_obj.deleted_count:
            logger.error(f"Not found note with id: {note_id}")
            raise DBNotFound(f"Not found note with id: {note_id}")
        else:
            return note_id

    async def delete_all_notes_by_condition(self, condition: dict) -> int:
        notes = await self._collections["notes"].delete_many(condition)
        if notes.deleted_count == 0:
            logger.error(f"No notes found settings condition: {condition}")
            raise DBNotFound(f"No notes found settings condition: {condition}")
        return notes.deleted_count
