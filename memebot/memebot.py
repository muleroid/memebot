from typing import List

from memebot.text_generate.markov_chain import MarkovChain
from memebot.tweets.tweet_scraper import TweetScraper


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio']

class Memebot():
    """
    The dankest memes.
    """
    # TODO: a lot of stuff
    def gather_inputs(self, tweet_scraper: TweetScraper) -> List[str]:
        tweets = []  # type: List[str]
        for username in SECRET_SAUCE:
            tweets.extend(tweet_scraper.scrape_tweets(username))
        return tweets

    def generate_meme(self, order: int, tweets: List[str]) -> str:
        chain = MarkovChain(order)
        for tweet in tweets:
            try:
                chain.parse_string(tweet)
            except ValueError:
                continue
        return chain.generate_tweet()
