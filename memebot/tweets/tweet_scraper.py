from typing import List

from memebot.tweets.tweet_helper import TweetHelper

class TweetScraper():
    def __init__(self, tweet_helper: TweetHelper):
        # TODO: replace with automated way of fetching credentials
        self.tweet_helper = tweet_helper

    def scrape_tweets(self, username: str) -> List[str]:
        result = self.tweet_helper.search_tweets(username)
        tweets = result['results']
        return [tweet['text'] for tweet in tweets]
