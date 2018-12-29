from delorean import epoch
from typing import List

from memebot.tweets.tweet_helper import TweetHelper

class TweetScraper():
    def __init__(self, tweet_helper: TweetHelper):
        # TODO: replace with automated way of fetching credentials
        self.tweet_helper = tweet_helper

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
