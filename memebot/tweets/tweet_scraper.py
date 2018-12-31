from delorean import epoch
from typing import List
import os

from memebot.credentials.gcs_credentials_provider import GCSCredentialsProvider
from memebot.tweets.tweet_helper import TweetHelper

class TweetScraper():
    def __init__(self, credentials_provider):
        self.tweet_helper = TweetHelper(
            client_key=credentials_provider.client_key,
            client_secret=credentials_provider.client_secret,
            resource_owner_key=credentials_provider.resource_owner_key,
            resource_owner_secret=credentials_provider.resource_owner_secret,
        )

    def scrape_tweets(self, username: str, from_ms: int, to_ms: int) -> List[str]:
        tweets = []
        next_pointer = None
        while True:
            result = self.tweet_helper.search_tweets(
                query=f'from:{username} -has:media -has:videos -has:links -has:mentions',
                full_range=True,
                from_date=self._convert_ms_to_string(from_ms),
                to_date=self._convert_ms_to_string(to_ms),
                next_pointer=next_pointer,
            )
            results = result['results']
            tweets.extend(tweet['text'] for tweet in results)
            next_pointer = result.get('next')
            if not next_pointer:
                break
        return tweets

    def _convert_ms_to_string(self, timestamp: int) -> str:
        dt = epoch(timestamp / 1000)
        return dt.format_datetime('YYYYMMddhhmm')


tweet_scraper = TweetScraper(GCSCredentialsProvider())
