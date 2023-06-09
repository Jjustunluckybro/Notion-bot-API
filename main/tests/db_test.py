import datetime

import pytest

from pymongo.errors import DuplicateKeyError

from main.models.notion_models import ThemeModel, NotionModel, NoteModel, CheckPointModel
from main.utils.config import MONGO_TEST_DB_CONNECTION_PATH
from main.utils.DbApi.MongoAPI import MongoDbApi, UserModel
from main.utils.exceptons import DBNotFound


class TestDB:
    db = MongoDbApi(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)
    test_user_const = UserModel(
        _id=1,
        tg_id="test_1",
        name="Test Name"
    )
    test_user_flex = UserModel(
        _id=2,
        tg_id="test_1",
        name="Test Name"
    )
    test_theme_cons = ThemeModel(
        _id=1,
        is_sub_theme=True,
        parent_id=0,
        user_id=1,
        name="Test Theme Name",
        description="Some test description",
        content=[]
    )
    test_theme_flex = ThemeModel(
        _id=2,
        is_sub_theme=True,
        parent_id=0,
        user_id=1,
        name="Test Theme Name",
        description="Some test description",
        content=[]
    )
    test_notion_cons = NotionModel(
        _id=0,
        user_id=1,
        parent_id=0,
        creation_time=datetime.datetime(1999, 12, 31, 21, 0),
        next_notion_time=datetime.datetime(1999, 12, 31, 21, 0),
        is_repeatable=True,
        description="Some alarm desc"
    )
    test_notion_flex = NotionModel(
        _id=1,
        user_id=1,
        parent_id=0,
        creation_time=datetime.datetime(1999, 12, 31, 21, 0),
        next_notion_time=None,
        is_repeatable=False,
        description="Some alarm desc"
    )
    test_note_cons = NoteModel(
        _id=0,
        user_id=1,
        name="test notion name",
        creation_time=datetime.datetime(1999, 12, 31, 21, 0),
        notion_id=0,
        description="Note description",
        check_points=[
            CheckPointModel(
                text="Chek-list text",
                is_finish=False,
                attachments=[],
                creation_time=datetime.datetime(1999, 12, 31, 21, 0),
                notion_id=0
            )
        ],
        attachments=[]
    )
    test_note_flex = NoteModel(
        _id=1,
        user_id=1,
        name="test notion name",
        creation_time=datetime.datetime(1999, 12, 31, 21, 0),
        notion_id=0,
        description="Note description",
        check_points=[],
        attachments=[]
    )
    non_exist_id = 11111111

    # ----- Users ----- #
    async def test_get_user(self):
        """Positive test | get user from db"""
        user = await self.db.get_user(self.test_user_const.id)
        assert user == self.test_user_const

    async def test_get_user_not_found(self):
        """Negative test | try to get non-existent user"""
        with pytest.raises(DBNotFound):
            await self.db.get_user(self.non_exist_id)

    async def test_write_new_user(self):
        """Positive test | write new user to db"""
        user_id = await self.db.write_new_user(self.test_user_flex)
        assert user_id == self.test_user_flex.id

    async def test_write_new_user_already_exist(self):
        """Negative test | try to write already exist user"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_user(self.test_user_const)

    async def test_delete_user(self):
        """Positive test | delete user from db"""
        user_2_id = await self.db.delete_user(self.test_user_flex.id)
        assert user_2_id == self.test_user_flex.id

    async def test_delete_user_non_exist(self):
        """Negative test | try to delete non-exist user"""
        with pytest.raises(DBNotFound):
            await self.db.delete_user(self.non_exist_id)

    # ----- Themes ----- #
    async def test_get_theme(self):
        """Positive test | get theme from db"""
        theme = await self.db.get_theme(self.test_theme_cons.id)
        assert theme == self.test_theme_cons

    async def test_get_theme_not_found(self):
        """Negative test | try to get non-existent theme"""
        with pytest.raises(DBNotFound):
            await self.db.get_theme(self.non_exist_id)

    async def test_write_new_theme(self):
        """Positive test | write new theme to db"""
        theme_id = await self.db.write_new_theme(self.test_theme_flex)
        assert theme_id == self.test_theme_flex.id

    async def test_write_new_theme_already_exist(self):
        """Negative test | try to write already exist theme"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_theme(self.test_theme_cons)

    async def test_get_all_themes_by_condition(self):
        """Positive test | get all themes with condition {"name": "Test Theme Name"}"""
        themes = await self.db.get_all_themes_by_condition({"name": "Test Theme Name"})
        assert themes == [self.test_theme_cons, self.test_theme_flex]

    async def test_get_all_themes_by_condition_non_exist(self):
        """Negative test | try to get all themes, No one themes found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_themes_by_condition({"name": "no support name"})

    async def test_delete_theme(self):
        """Positive test | delete theme from db"""
        theme_id = await self.db.delete_theme(self.test_theme_flex.id)
        assert theme_id == self.test_theme_flex.id

    async def test_delete_theme_non_exist(self):
        """Negative test | try to delete non-exist user"""
        with pytest.raises(DBNotFound):
            await self.db.delete_theme(self.non_exist_id)

    # ----- Notions ----- #
    async def test_get_notion(self):
        """Positive test | get notion from db"""
        notion = await self.db.get_notion(self.test_notion_cons.id)
        assert notion == self.test_notion_cons

    async def test_get_notion_not_found(self):
        """Negative test | try to get non-existent notion"""
        with pytest.raises(DBNotFound):
            await self.db.get_notion(self.non_exist_id)

    async def test_write_new_notion(self):
        """Positive test | write new notion to db"""
        notion_id = await self.db.write_new_notion(self.test_notion_flex)
        assert notion_id == self.test_notion_flex.id

    async def test_write_new_notion_already_exist(self):
        """Negative test | try to write already exist notion"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_notion(self.test_notion_cons)

    async def test_get_all_notion_by_condition(self):
        """Positive test | get all notion with condition {"name": "Test Theme Name"}"""
        notion = await self.db.get_all_notion_by_condition({"description": "Some alarm desc"})
        assert notion == [self.test_notion_cons, self.test_notion_flex]

    async def test_get_all_notions_by_condition_non_exist(self):
        """Negative test | try to get all notion, No one notion found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_notion_by_condition({"name": "no support name"})

    async def test_delete_notion(self):
        """Positive test | delete theme from db"""
        notion_id = await self.db.delete_notion(self.test_notion_flex.id)
        assert notion_id == self.test_notion_flex.id

    async def test_notion_theme_non_exist(self):
        """Negative test | try to delete non-exist notion"""
        with pytest.raises(DBNotFound):
            await self.db.delete_notion(self.non_exist_id)

    # ----- Notes ----- #
    async def test_get_note(self):
        note = await self.db.get_note(self.test_note_cons.id)
        assert note == self.test_note_cons

    async def test_get_note_not_found(self):
        with pytest.raises(DBNotFound):
            await self.db.get_note(self.test_note_flex.id)

    async def test_write_new_note(self):
        """Positive test | write new note to db"""
        note_id = await self.db.write_new_note(self.test_note_flex)
        assert note_id == self.test_note_flex.id

    async def test_write_new_note_already_exist(self):
        """Negative test | try to write already exist note"""
        with pytest.raises(DuplicateKeyError):
            await self.db.write_new_note(self.test_note_cons)

    async def test_get_all_notes_by_condition(self):
        """Positive test | get all notes with condition {"name": "test notion name"}"""
        notes = await self.db.get_all_notes_by_condition({"name": "test notion name"})
        assert notes == [self.test_note_cons, self.test_note_flex]

    async def test_get_all_notes_by_condition_non_exist(self):
        """Negative test | try to get all notes, No one notion found setting conditions"""
        with pytest.raises(DBNotFound):
            await self.db.get_all_notes_by_condition({"name": "no support name"})

    async def test_delete_note(self):
        """Positive test | delete note from db"""
        note_id = await self.db.delete_note(self.test_note_flex.id)
        assert note_id == self.test_note_flex.id

    async def test_delete_note_not_found(self):
        """Negative test | try to delete non-exist note"""
        with pytest.raises(DBNotFound):
            await self.db.delete_note(self.non_exist_id)
