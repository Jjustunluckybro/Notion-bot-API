from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request

from main.models.notion_models import ThemeModel, UserModel
from main.data_base.MongoAPI import MongoDbApi, DbApi
from main.utils.exceptons import DBNotFound
from main.utils.utils import create_bson_object_by_id

router = APIRouter(
    prefix="/themes",
    tags=["Themes"]
)


# ----- GET ----- #
@router.get("/get_theme_by_id", status_code=status.HTTP_200_OK)
async def get_theme_by_id(request: Request, theme_id: str | bytes) -> ThemeModel:
    """Get theme by themeId"""
    db: DbApi = request.app.state.mongo_db
    theme_id = create_bson_object_by_id(theme_id)
    try:
        theme = await db.get_theme(theme_id)
        return theme
    except DBNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theme not found")


@router.get("/get_all_user_title_themes_by_tg_id", status_code=status.HTTP_200_OK)
async def get_all_user_title_themes_by_tg_id(request: Request,
                                             user_tg_id: str,
                                             list_length: int = 100,
                                             ) -> list[ThemeModel]:
    """
    :param user_tg_id: Telegram user id
    :param list_length: length of response list with themes
    :return: List of themes linked to user with user_tg_id
    """
    db: DbApi = request.app.state.mongo_db
    try:
        # Try to get userId
        user: UserModel = await db.get_user_by_tg_id(user_tg_id)
        # Try to get themes
        result = await db.get_all_themes_by_condition(
            condition={
                "user_id": user.id,
                "is_sub_theme": False
            },
            list_length=list_length
        )
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/get_all_theme_sub_theme", status_code=status.HTTP_200_OK)
async def get_all_theme_sub_theme(request: Request, parent_theme_id: str | bytes) -> list[ThemeModel]:
    """
    Get all sub-themes linked to one title-theme by title-theme id
    """
    db: DbApi = request.app.state.mongo_db
    parent_theme_id = create_bson_object_by_id(parent_theme_id)
    try:
        result = await db.get_all_themes_by_condition(
            condition={
                "parent_id": parent_theme_id,
                "is_sub_theme": True
            }
        )
        return result
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


# ----- POST ---- #
@router.post("/set_new_theme", status_code=status.HTTP_201_CREATED)
async def set_new_theme(request: Request, theme: ThemeModel) -> str:
    """
    :param theme:  ThemeModel.
    sub-theme must have parent -> required to fill out "parent_id" |
    Title-theme must not have parent -> "parent_id" must not be filled |
    :return: id of new created theme
    """
    db: DbApi = request.app.state.mongo_db
    # Handling user exceptions
    if theme.is_sub_theme and theme.parent_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Sub theme must have parent, fill out 'parent_id'")
    if not theme.is_sub_theme and theme.parent_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title theme must not have parent, don't fill 'parent_id'")

    try:
        insert_object_id = await db.write_new_theme(theme)
        return str(insert_object_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


# ----- DELETE ----- #
@router.delete("/delete_theme_by_id", status_code=status.HTTP_200_OK)
async def delete_theme_by_id(request: Request, theme_id: str | bytes) -> str:
    db: DbApi = request.app.state.mongo_db
    theme_id = create_bson_object_by_id(theme_id)
    print(theme_id)
    print(type(theme_id))
    try:
        deleted_obj_id = await db.delete_theme(theme_id)
        return str(deleted_obj_id)
    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.delete("/delete_all_child_sub_themes", status_code=status.HTTP_200_OK)
async def delete_child_sub_themes(request: Request, parent_theme_id: str | bytes) -> list[str]:
    """
    Delete all title-theme child sub-themes
    """
    db: DbApi = request.app.state.mongo_db
    parent_theme_id = create_bson_object_by_id(parent_theme_id)
    try:
        themes_to_delete = await db.get_all_themes_by_condition(
            condition={
                "parent_id": parent_theme_id,
                "is_sub_theme": True
            }
        )
        themes_to_delete_ids = [theme.id for theme in themes_to_delete]

        deleted_ids = []
        for theme_id in themes_to_delete_ids:
            deleted_id = await db.delete_theme(theme_id)
            deleted_ids.append(str(deleted_id))

        return deleted_ids

    except DBNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))



# @router.post("/get_all_themes_by_condition", status_code=status.HTTP_200_OK)
# async def get_all_themes_by_condition(request: Request,
#                                       condition: dict,
#                                       list_length: int = 100
#                                       ) -> list[ThemeModel]:
#     db: DbApi = request.app.state.mongo_db
#     try:
#         result = await db.get_all_themes_by_condition(condition, list_length)
#         return result
#     except DBNotFound as err:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
