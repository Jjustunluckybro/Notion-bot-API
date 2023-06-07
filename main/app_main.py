from fastapi import FastAPI
import uvicorn
from pydantic import BaseConfig
from starlette.requests import Request

from utils.config import MONGO_TEST_DB_CONNECTION_PATH
from data_base.MongoAPI import MongoDbApi
from utils import config as cfg
from utils import logger as log

from main.routers.user import router as user_router
from main.routers.notes import router as note_router

ROUTERS = (
    user_router,
    note_router
)


def main():
    # Create app
    app = FastAPI(title="notion_bot_api")

    # Add routers
    for router in ROUTERS:
        app.include_router(router)

    # Create db connection
    db = MongoDbApi()
    db.connect_to_db(connection_string=MONGO_TEST_DB_CONNECTION_PATH, is_test=True)

    # Save ref to db
    app.state.mongo_db = db

    # Set logger
    app_logger_config = log.get_logger_config(cfg.LOGGER_CONFIG_PATH)
    app_logger = log.init_app_logger()

    # Start uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=app_logger_config)


if __name__ == '__main__':
    main()
