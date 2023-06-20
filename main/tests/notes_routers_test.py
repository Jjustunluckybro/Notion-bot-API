from httpx import AsyncClient

import test_data

from starlette import status

from main.models.notion_models import NoteModel


class TestNotesRouters:

    @staticmethod
    async def test_get_note_positive(client: AsyncClient):
        response = await client.get(f"/notes/get_note_by_id?note_id={test_data.test_note_cons.id}")
        assert response.status_code == status.HTTP_200_OK
        assert NoteModel.parse_obj(response.json()) == test_data.test_note_cons

    @staticmethod
    async def test_get_note_negative_non_exist(client: AsyncClient):
        response = await client.get(f"/notes/get_note_by_id?note_id={test_data.non_exist_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Note not found"}

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
        response = await client.post("notes/set_new_note", json=body)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == "647c71ce757c21cca9550368"

    @staticmethod
    async def test_get_all_child_notes_positive(client: AsyncClient):
        response = await client.get("/notes/get_all_child_notes?parent_id=6460f9eb095beba251481942&list_length=100")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    @staticmethod
    async def test_get_all_child_notes_negative(client: AsyncClient):
        response = await client.get(f"/notes/get_all_child_notes?parent_id={test_data.non_exist_id}&list_length=100")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found child notes"}

    @staticmethod
    async def test_delete_note_positive(client: AsyncClient):
        response = await client.delete("/notes/delete_note_by_id?note_id=647c71ce757c21cca9550368")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == "647c71ce757c21cca9550368"

    @staticmethod
    async def test_delete_note_negative(client: AsyncClient):
        response = await client.delete(f"notes/delete_note_by_id?note_id={test_data.non_exist_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
