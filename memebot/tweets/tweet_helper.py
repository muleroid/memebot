import json
from requests_oauthlib import OAuth1Session
from typing import Any, Dict, Optional

from memebot.utils import get_logger


logger = get_logger(__name__)


class TweetHelper():
    """
    Helper class for accessing Twitter APIs. Takes care
    of oauth business.
    """
    def __init__(self,
                 client_key: str,
                 client_secret: str,
                 resource_owner_key: str,
                 resource_owner_secret: str):
        self.oauth = OAuth1Session(
            client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret
        )

    def search_tweets(self,
                      query: str,
                      full_range: bool = False,
                      from_date: Optional[str] = None,
                      to_date: Optional[str] = None,
                      next_pointer: Optional[str] = None) -> Dict[str, Any]:
        params = {
            'query': query,
        }
        if from_date:
            params['fromDate'] = from_date
        if to_date:
            params['toDate'] = to_date
        if next_pointer:
            params['next'] = next_pointer
        if full_range:
            product = 'fullarchive'
        else:
            product = '30day'
        logger.info(f'Querying Twitter: {json.dumps(params)}')
        r = self.oauth.get(
            f'https://api.twitter.com/1.1/tweets/search/{product}/dev.json',
            params=params)
        if r.status_code != 200:
            raise RuntimeError(f'Error: Search endpoint returned {r.status_code}: {r.text}')
        return json.loads(r.content)

    def post_tweet(self, content: str) -> None:
        r = self.oauth.post(
            'https://api.twitter.com/1.1/statuses/update.json',
            data={
                'status': content,
            },
        )
        if r.status_code != 200:
            raise RuntimeError(f'Error: Failed to post tweet {r.status_code}: {r.text}')
