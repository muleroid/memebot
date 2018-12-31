import requests
import os


METADATA_HEADERS = {
    'Metadata-Flavor': 'Google',
}


def get_project_id():
    r = requests.get('http://metadata.google.internal/computeMetadata/v1/project/project-id', headers=METADATA_HEADERS)
    if r.status_code != 200:
        raise RuntimeError(f'Got an error requesting metadata [{r.status_code}]: {r.text}')
    return r.text


def is_running_on_app_engine():
    env = os.environ.get('NODE_ENV', '')
    return env == 'production'