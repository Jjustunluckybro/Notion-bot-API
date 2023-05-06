import json
import logging


def get_logger_config(path: str) -> dict:
    """Open and parce logger config from json file to python dict obj"""
    with open(path, "r", encoding="UTF-8") as f:
        cfg = dict(json.load(f))
    return cfg


def init_app_logger() -> logging.Logger:
    """Init and return logger for app logic with name 'app'"""
    logger = logging.getLogger("app")
    logger.info("Application logger was init")
    return logger
