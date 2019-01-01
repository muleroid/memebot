from bottle import Bottle, get, request, run
from delorean import Delorean
from typing import List
import json

from memebot.services.tweet_service import tweet_service
from memebot.text_generate.markov_chain import MarkovChain
from memebot.tweets.tweet_scraper import tweet_scraper
from memebot.utils import get_project_id, is_running_on_app_engine


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio']

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
    markov_chain = MarkovChain(2)
    for tweet in tweets:
        try:
            markov_chain.parse_string(tweet.text)
        except ValueError:
            # TODO: logging..
            continue
    return json.dumps({'generated_tweet': markov_chain.generate_tweet()})


@app.get('/')
def get():
    return json.dumps({
        'project_id': get_project_id(),
        'is_app_engine': is_running_on_app_engine(),
    })


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
