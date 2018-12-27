import json
from requests_oauthlib import OAuth1Session

class TweetHelper():
    """
    Helper class for accessing Twitter APIs. Takes care
    of oauth business.
    """

    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret):
        self.oauth = OAuth1Session(
            client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret
        )

    def search_tweets(self, username):
        r = self.oauth.get(
            'https://api.twitter.com/1.1/tweets/search/30day/dev.json',
            params={
                'query': 'from:{}'.format(username),
            })
        if r.status_code != 200:
            raise RuntimeError
        return json.loads(r.content)
