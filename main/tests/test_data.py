import datetime

from main.models.notion_models import UserModel, PydanticObjectId, ThemeModel, NotionModel, NoteModel, CheckPointModel


test_user_const = UserModel(
        _id=PydanticObjectId("6460f2db26fe8e1b7a473921"),
        tg_id="123",
        name="321"
    )
test_user_flex = UserModel(
        _id=PydanticObjectId("6460f2db26fe8e1b7a473922"),
        tg_id="test_1",
        name="Test Name"
    )
test_theme_cons = ThemeModel(
        _id=PydanticObjectId("6460f9eb095beba251481941"),
        is_sub_theme=True,
        parent_id=PydanticObjectId("6460f2db26fe8e1b7a473921"),
        user_id=PydanticObjectId("6460f2db26fe8e1b7a473921"),
        name="Test Theme Name",
        description="Some test description",
        content=[]
    )
test_theme_flex = ThemeModel(
    _id=PydanticObjectId("6460f9eb095beba251481942"),
    is_sub_theme=True,
    parent_id=PydanticObjectId("6460f2db26fe8e1b7a473922"),
    user_id=PydanticObjectId("6460f2db26fe8e1b7a473922"),
    name="Test Theme Name",
    description="Some test description",
    content=[]
    )
test_notion_cons = NotionModel(
    _id=PydanticObjectId("647c66c43decd3a12fb3647e"),
    user_id=PydanticObjectId("647c66c43decd3a12fb3647f"),
    parent_id=PydanticObjectId("647c66c43decd3a12fb36480"),
    creation_time=datetime.datetime(1999, 12, 31, 21, 0),
    next_notion_time=datetime.datetime(1999, 12, 31, 21, 0),
    is_repeatable=True,
    description="Some alarm desc"
    )
test_notion_flex = NotionModel(
    _id=PydanticObjectId("647c709f79cf313ad8b6c9df"),
    user_id=PydanticObjectId("647c709f79cf313ad8b6c9e0"),
    parent_id=PydanticObjectId("647c709f79cf313ad8b6c9e1"),
    creation_time=datetime.datetime(1999, 12, 31, 21, 0),
    next_notion_time=None,
    is_repeatable=False,
    description="Some alarm desc"
)
test_note_cons = NoteModel(
    _id=PydanticObjectId("647c715ebf0b17d2091d06e1"),
    user_id=PydanticObjectId("647c715ebf0b17d2091d06e2"),
    parent_id=PydanticObjectId("6460f9eb095beba251481941"),
    name="test notion name",
    creation_time=datetime.datetime(1999, 12, 31, 21, 0),
    notion_id=PydanticObjectId("647c715ebf0b17d2091d06e3"),
    description="Note description",
    check_points=[
        CheckPointModel(
            text="Chek-list text",
            is_finish=False,
            attachments=[],
            creation_time=datetime.datetime(1999, 12, 31, 21, 0),
            notion_id=PydanticObjectId("647c715ebf0b17d2091d06e4")
        )
    ],
    attachments=[]
)
test_note_flex = NoteModel(
    _id=PydanticObjectId("647c71ce757c21cca9550368"),
    user_id=PydanticObjectId("647c71ce757c21cca9550369"),
    parent_id=PydanticObjectId("6460f9eb095beba251481942"),
    name="test notion name",
    creation_time=datetime.datetime(1999, 12, 31, 21, 0),
    notion_id=PydanticObjectId("647c71ce757c21cca955036a"),
    description="Note description",
    check_points=[],
    attachments=[]
)
non_exist_id = PydanticObjectId("1000a0aa00fa0a0b0a000001")
