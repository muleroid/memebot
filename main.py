from bottle import Bottle, get, request, run
from typing import List
import json

from memebot.tweets.tweet_scraper import tweet_scraper
from memebot.utils import get_project_id, is_running_on_app_engine


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio']

app = Bottle()


@app.get('/tweets/<username>')
def get_tweets(username):
    start_time_ms = request.query.get('start_time_ms', default=None, type=int)
    end_time_ms = request.query.get('end_time_ms', default=None, type=int)
    full_archive = request.query.get('full_archive', default=False, type=bool)

    tweets = tweet_scraper.scrape_tweets(username, start_time_ms, end_time_ms, full_archive)
    return json.dumps({'tweets': tweets})


@app.get('/')
def get():
    return json.dumps({
        'project_id': get_project_id(),
        'is_app_engine': is_running_on_app_engine(),
    })


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
