import os

class LocalCredentialsProvider():
    def __init__(self):
        self.client_key = os.environ.get('MEMEBOT_CLIENT_KEY')
        self.client_secret = os.environ.get('MEMEBOT_CLIENT_SECRET')
        self.resource_owner_key = os.environ.get('MEMEBOT_RESOURCE_OWNER_KEY')
        self.resource_owner_secret = os.environ.get('MEMEBOT_RESOURCE_OWNER_SECRET')
