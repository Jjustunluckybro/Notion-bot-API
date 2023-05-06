from fastapi import FastAPI
import uvicorn

from utils import config as cfg
from utils import logger as log


app = FastAPI(
    title="notion_bot_api"
)

if __name__ == '__main__':
    app_logger_config = log.get_logger_config(cfg.LOGGER_CONFIG_PATH)
    app_logger = log.init_app_logger()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=app_logger_config)
