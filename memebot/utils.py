import logging
import requests
import os


METADATA_HEADERS = {
    'Metadata-Flavor': 'Google',
}


def get_project_id() -> bool:
    r = requests.get('http://metadata.google.internal/computeMetadata/v1/project/project-id', headers=METADATA_HEADERS)
    if r.status_code != 200:
        raise RuntimeError(f'Got an error requesting metadata [{r.status_code}]: {r.text}')
    return r.text


def is_running_on_app_engine() -> bool:
    return os.environ.get('IS_GAE')


def get_logger(name: str, log_level: str = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter('[{levelname}] {asctime}: {message}', style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
