from bottle import Bottle, get, request, run
from typing import List
import json

from memebot.tweets.tweet_scraper import tweet_scraper


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio']

app = Bottle()


@app.get('/tweets/<username>')
def get_tweets(username):
    start_time_ms = int(request.query.start_time_ms)
    end_time_ms = int(request.query.end_time_ms)

    tweets = tweet_scraper.scrape_tweets(username, start_time_ms, end_time_ms)
    return json.dumps({'tweets': tweets})


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
