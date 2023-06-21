from httpx import AsyncClient

import test_data

from starlette import status

from main.models.notion_models import NoteModel


class TestNotesRouters:

    # /notes/get_note_by_id
    @staticmethod
    async def test_get_note_positive(client: AsyncClient):
        r = await client.get(f"/notes/get_note_by_id?note_id={test_data.test_note_cons.id}")
        assert r.status_code == status.HTTP_200_OK
        assert NoteModel.parse_obj(r.json()) == test_data.test_note_cons

    @staticmethod
    async def test_get_note_negative_non_exist(client: AsyncClient):
        r = await client.get(f"/notes/get_note_by_id?note_id={test_data.non_exist_id}")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json() == {"detail": "Note not found"}

    # notes/set_new_note
    @staticmethod
    async def test_set_new_note_positive(client: AsyncClient):
        body = {
            "_id": "647c71ce757c21cca9550368",
            "user_id": "647c71ce757c21cca9550369",
            "parent_id": "6460f9eb095beba251481942",
            "name": "test notion name",
            "creation_time": "1999-12-31T21:00:00",
            "notion_id": "647c71ce757c21cca955036a",
            "description": "Note description",
            "attachments": [],
            "check_points": []
        }
        r = await client.post("notes/set_new_note", json=body)
        assert r.status_code == status.HTTP_201_CREATED
        assert r.json() == "647c71ce757c21cca9550368"

    @staticmethod
    async def test_set_new_note_negative(client: AsyncClient):
        body = {
            "name": "test notion name",
            "creation_time": "1999-12-31T21:00:00",
            "description": ""
        }
        r = await client.post("notes/set_new_note", json=body)
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # /notes/get_all_child_notes
    @staticmethod
    async def test_get_all_child_notes_positive(client: AsyncClient):
        r = await client.get("/notes/get_all_child_notes?parent_id=6460f9eb095beba251481942&list_length=100")
        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 1

    @staticmethod
    async def test_get_all_child_notes_negative(client: AsyncClient):
        r = await client.get(f"/notes/get_all_child_notes?parent_id={test_data.non_exist_id}&list_length=100")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json() == {"detail": "Not found child notes"}

    # notes/get_all_notes_by_condition
    @staticmethod
    async def test_get_all_note_by_condition(client: AsyncClient):
        condition = {
            "name": "test notion name",
            "description": "Note description"
        }
        r = await client.post(f"/notes/get_all_notes_by_condition", json=condition)
        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 2

    @staticmethod
    async def test_get_all_note_by_condition_negative(client: AsyncClient):
        condition = {
            "some_not_exist_key": "some_not_exist_value"
        }
        r = await client.post(f"/notes/get_all_notes_by_condition", json=condition)
        assert r.status_code == status.HTTP_404_NOT_FOUND

    # /notes/delete_note_by_id
    @staticmethod
    async def test_delete_note_positive(client: AsyncClient):
        r = await client.delete("/notes/delete_note_by_id?note_id=647c71ce757c21cca9550368")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == "647c71ce757c21cca9550368"

    @staticmethod
    async def test_delete_note_negative(client: AsyncClient):
        r = await client.delete(f"notes/delete_note_by_id?note_id={test_data.non_exist_id}")
        assert r.status_code == status.HTTP_404_NOT_FOUND

    # notes/delete_all_child_notes
    @staticmethod
    async def test_delete_notes_by_parent(client: AsyncClient):
        body1 = {
            "user_id": "647c71ce757c21cca9550369",
            "parent_id": "6460f9eb095beba251480000",
            "name": "test notion name",
            "creation_time": "1999-12-31T21:00:00",
            "notion_id": "647c71ce757c21cca955036a",
            "description": "Note description",
            "attachments": [],
            "check_points": []
        }
        body2 = {
            "user_id": "647c71ce757c21cca9550369",
            "parent_id": "6460f9eb095beba251480000",
            "name": "test notion name",
            "creation_time": "1999-12-31T21:00:00",
            "notion_id": "647c71ce757c21cca955036a",
            "description": "Note description",
            "attachments": [],
            "check_points": []
        }
        await client.post("notes/set_new_note", json=body1)
        await client.post("notes/set_new_note", json=body2)

        r = await client.delete("/notes/delete_all_child_notes?parent_id=6460f9eb095beba251480000")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == 2
