import os

from google.cloud.storage.client import Client

from memebot.utils import get_project_id

class GCSCredentialsProvider():
    """
    Reads Twitter credentials from Google Cloud Storage.
    """
    def __init__(self):
        self.client = Client()
        bucket_name = os.environ.get('BUCKET_NAME', f'{get_project_id()}.appspot.com')
        self.bucket = self.client.get_bucket(bucket_name)
        self.client_key = self._read_gcs_file('client_key')
        self.client_secret = self._read_gcs_file('client_secret')
        self.resource_owner_key = self._read_gcs_file('resource_owner_key')
        self.resource_owner_secret = self._read_gcs_file('resource_owner_secret')

    def _read_gcs_file(self, filename):
        filepath = os.path.join('twitter', filename)

        blob = self.bucket.get_blob(filepath)
        contents = blob.download_as_string().decode('utf-8').strip()
        return contents
