from bottle import Bottle, get, request, run
from datetime import timedelta
from delorean import Delorean
from typing import List
import json

from memebot.services.tweet_service import tweet_service
from memebot.text_generate.markov_chain import MarkovChain
from memebot.tweets.tweet_scraper import tweet_scraper
from memebot.utils import (
    get_logger,
    get_project_id,
    is_running_on_app_engine,
)


logger = get_logger(__name__)


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio', 'degg', 'wolfpupy']

app = Bottle()


@app.get('/tweets/<username>')
def get_tweets(username):
    start_time_ms = request.query.get('start_time_ms', default=None, type=int)
    end_time_ms = request.query.get('end_time_ms', default=None, type=int)

    tweets = tweet_service.get_tweets_by_username_and_range(username, start_time_ms, end_time_ms)
    return json.dumps({'tweets': [tweet.to_dict() for tweet in tweets]})


@app.get('/tweet')
def generate_tweet():
    dt = Delorean()
    now_ms = int(dt.epoch * 1000)
    tweets = tweet_service.get_tweets_by_range(0, now_ms)
    logger.info(f'Retrieved {len(tweets)} tweets for training')
    markov_chain = MarkovChain(2)
    skipped = 0
    for tweet in tweets:
        try:
            markov_chain.parse_string(tweet.text)
        except ValueError:
            skipped += 1
            continue
    logger.info(f'Finished training Markov Chain, skipped {skipped} tweets')
    return json.dumps({'generated_tweet': markov_chain.generate_tweet()})


@app.get('/training')
def gather_training_data():
    """
    Queries Twitter for a day's worth of tweets.
    """
    dt = Delorean()
    dt.truncate('day')
    start_dt = dt - timedelta(days=1)
    start_ms = int(start_dt.epoch * 1000)
    end_ms = int(dt.epoch * 1000)
    logger.info(f'Querying Twitter for training data between {start_ms} and {end_ms}')

    count = 0

    for username in SECRET_SAUCE:
        tweets = tweet_scraper.scrape_tweets(username, start_ms, end_ms)
        logger.info(f'Fetched {len(tweets)} tweets from {username}')
        tweet_service.save_tweets(tweets)
        count += len(tweets)

    logger.info(f'Saved {count} tweets in database')
    return json.dumps({'count': count})


@app.get('/')
def get():
    return json.dumps({
        'project_id': get_project_id(),
        'is_app_engine': is_running_on_app_engine(),
    })


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
