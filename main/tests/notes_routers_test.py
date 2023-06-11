import test_data


from starlette import status
from fastapi import FastAPI
from fastapi.testclient import TestClient

from main.data_base.MongoAPI import MongoDbApi
from main.models.notion_models import NoteModel
from main.routers.routes.notes import router as note_router
from main.utils.config import MONGO_TEST_DB_CONNECTION_PATH

app = FastAPI()
app.include_router(note_router)
client = TestClient(app)

# Create db connection
db = MongoDbApi()
db.connect_to_db(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)

# Save ref to db
app.state.db = db

async def test_get_note_positive():
    response = client.get(f"/notes/get_note_by_id?note_id={test_data.test_note_cons.id}")
    assert response.status_code == status.HTTP_200_OK
    assert NoteModel.parse_obj(response.json()) == test_data.test_note_cons
