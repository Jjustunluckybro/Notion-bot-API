import datetime

import pytest

from pymongo.errors import DuplicateKeyError

from main.models.notion_models import ThemeModel, NotionModel, NoteModel, CheckPointModel, PydanticObjectId
from main.utils.config import MONGO_TEST_DB_CONNECTION_PATH
from main.data_base.MongoAPI import MongoDbApi, UserModel
from main.utils.exceptons import DBNotFound

import test_data

class TestDB:
    db = MongoDbApi()

    def test_create_db_connection(self):
        db_connect_answer = self.db.connect_to_db(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)
        assert db_connect_answer is True

    # ----- Users ----- #
    async def test_get_user(self):
        """Positive test | get user from db"""
        user = await self.db.get_user_by_id(test_data.test_user_const.id)
        assert user == test_data.test_user_const

    async def test_get_user_not_found(self):
        """Negative test | try to get non-existent user"""
        with pytest.raises(DBNotFound):
            await self.db.get_user_by_id(test_data.non_exist_id)

    async def test_write_new_user(self):
        """Positive test | write new user to db"""
        user_id = await self.db.write_new_user(test_data.test_user_flex)
        assert user_id == test_data.test_user_flex.id

    async def test_write_new_user_already_exist(self):
        """Negative test | try to write already exist user"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_user(test_data.test_user_const)

    async def test_delete_user(self):
        """Positive test | delete user from db"""
        user_2_id = await self.db.delete_user(test_data.test_user_flex.id)
        assert user_2_id == test_data.test_user_flex.id

    async def test_delete_user_non_exist(self):
        """Negative test | try to delete non-exist user"""
        with pytest.raises(DBNotFound):
            await self.db.delete_user(test_data.non_exist_id)

    # ----- Themes ----- #
    async def test_get_theme(self):
        """Positive test | get theme from db"""
        theme = await self.db.get_theme(test_data.test_theme_cons.id)
        assert theme == test_data.test_theme_cons

    async def test_get_theme_not_found(self):
        """Negative test | try to get non-existent theme"""
        with pytest.raises(DBNotFound):
            await self.db.get_theme(test_data.non_exist_id)

    async def test_write_new_theme(self):
        """Positive test | write new theme to db"""
        theme_id = await self.db.write_new_theme(test_data.test_theme_flex)
        assert theme_id == test_data.test_theme_flex.id

    async def test_write_new_theme_already_exist(self):
        """Negative test | try to write already exist theme"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_theme(test_data.test_theme_cons)

    async def test_get_all_themes_by_condition(self):
        """Positive test | get all themes with condition {"name": "Test Theme Name"}"""
        themes = await self.db.get_all_themes_by_condition({"name": "Test Theme Name"})
        assert themes == [test_data.test_theme_cons, test_data.test_theme_flex]

    async def test_get_all_themes_by_condition_non_exist(self):
        """Negative test | try to get all themes, No one themes found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_themes_by_condition({"name": "no support name"})

    async def test_delete_theme(self):
        """Positive test | delete theme from db"""
        theme_id = await self.db.delete_theme(test_data.test_theme_flex.id)
        assert theme_id == test_data.test_theme_flex.id

    async def test_delete_theme_non_exist(self):
        """Negative test | try to delete non-exist user"""
        with pytest.raises(DBNotFound):
            await self.db.delete_theme(test_data.non_exist_id)

    async def test_delete_all_themes_by_condition(self):
        test_theme_1 = test_data.test_theme_cons
        test_theme_2 = test_data.test_theme_flex

        test_theme_1.id = PydanticObjectId("6540f9eb095beba251481989")
        test_theme_2.id = PydanticObjectId("6230f9eb095beba251481999")
        #
        test_theme_1.description = "6460f9eb095beba"
        test_theme_2.description = "6460f9eb095beba"

        await self.db.write_new_theme(test_theme_1)
        await self.db.write_new_theme(test_theme_2)

        themes_deleted = await self.db.delete_all_themes_by_condition({"description": "6460f9eb095beba"})
        assert themes_deleted == 2

    # ----- Notions ----- #
    async def test_get_notion(self):
        """Positive test | get notion from db"""
        notion = await self.db.get_notion(test_data.test_notion_cons.id)
        assert notion == test_data.test_notion_cons

    async def test_get_notion_not_found(self):
        """Negative test | try to get non-existent notion"""
        with pytest.raises(DBNotFound):
            await self.db.get_notion(test_data.non_exist_id)

    async def test_write_new_notion(self):
        """Positive test | write new notion to db"""
        notion_id = await self.db.write_new_notion(test_data.test_notion_flex)
        assert notion_id == test_data.test_notion_flex.id

    async def test_write_new_notion_already_exist(self):
        """Negative test | try to write already exist notion"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_notion(test_data.test_notion_cons)

    async def test_get_all_notion_by_condition(self):
        """Positive test | get all notion with condition {"name": "Test Theme Name"}"""
        notion = await self.db.get_all_notion_by_condition({"description": "Some alarm desc"})
        assert notion == [test_data.test_notion_cons, test_data.test_notion_flex]

    async def test_get_all_notions_by_condition_non_exist(self):
        """Negative test | try to get all notion, No one notion found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_notion_by_condition({"name": "no support name"})

    async def test_delete_notion(self):
        """Positive test | delete theme from db"""
        notion_id = await self.db.delete_notion(test_data.test_notion_flex.id)
        assert notion_id == test_data.test_notion_flex.id

    async def test_notion_theme_non_exist(self):
        """Negative test | try to delete non-exist notion"""
        with pytest.raises(DBNotFound):
            await self.db.delete_notion(test_data.non_exist_id)

    async def test_delete_all_notion_by_condition(self):
        test_notion_1 = test_data.test_notion_cons
        test_notion_2 = test_data.test_notion_flex

        test_notion_1.id = PydanticObjectId("6540f9eb095beba251481989")
        test_notion_2.id = PydanticObjectId("6230f9eb095beba251481999")
        #
        test_notion_1.description = "6460f9eb095beba"
        test_notion_2.description = "6460f9eb095beba"

        await self.db.write_new_notion(test_notion_1)
        await self.db.write_new_notion(test_notion_2)

        themes_deleted = await self.db.delete_all_notion_by_condition({"description": "6460f9eb095beba"})
        assert themes_deleted == 2

    # ----- Notes ----- #
    async def test_get_note(self):
        note = await self.db.get_note(test_data.test_note_cons.id)
        assert note == test_data.test_note_cons

    async def test_get_note_not_found(self):
        with pytest.raises(DBNotFound):
            await self.db.get_note(test_data.test_note_flex.id)

    async def test_write_new_note(self):
        """Positive test | write new note to db"""
        note_id = await self.db.write_new_note(test_data.test_note_flex)
        assert note_id == test_data.test_note_flex.id

    async def test_write_new_note_already_exist(self):
        """Negative test | try to write already exist note"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_note(test_data.test_note_cons)

    async def test_get_all_notes_by_condition(self):
        """Positive test | get all notes with condition {"name": "test notion name"}"""
        notes = await self.db.get_all_notes_by_condition({"name": "test notion name"})
        assert notes == [test_data.test_note_cons, test_data.test_note_flex]

    async def test_get_all_notes_by_condition_non_exist(self):
        """Negative test | try to get all notes, No one notion found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_notes_by_condition({"name": "no support name"})

    async def test_delete_note(self):
        """Positive test | delete note from db"""
        note_id = await self.db.delete_note(test_data.test_note_flex.id)
        assert note_id == test_data.test_note_flex.id

    async def test_delete_note_not_found(self):
        """Negative test | try to delete non-exist note"""
        with pytest.raises(DBNotFound):
            await self.db.delete_note(test_data.non_exist_id)

    async def test_delete_all_note_by_condition(self):
        test_note_1 = test_data.test_note_cons
        test_note_2 = test_data.test_note_flex

        test_note_1.id = PydanticObjectId("6540f9eb095beba251481989")
        test_note_2.id = PydanticObjectId("6230f9eb095beba251481999")
        #
        test_note_1.description = "6460f9eb095beba"
        test_note_2.description = "6460f9eb095beba"

        await self.db.write_new_note(test_note_1)
        await self.db.write_new_note(test_note_2)

        themes_deleted = await self.db.delete_all_notes_by_condition({"description": "6460f9eb095beba"})
        assert themes_deleted == 2

