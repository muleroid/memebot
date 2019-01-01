from google.cloud import firestore
from typing import List, Union

from memebot.models.tweet import Tweet

class TweetService():
    def __init__(self):
        self.client = firestore.Client()

    def save_tweets(self, tweets: List[Tweet]) -> None:
        collection_ref = self.client.collection('tweets')
        for tweet in tweets:
            doc_ref = collection_ref.document(str(tweet.id))
            doc_ref.set(tweet.to_dict())


    def get_tweet_by_id(self, tweet_id: Union[str, int]) -> Tweet:
        doc = self.client.collection('tweets').document(str(tweet_id)).get()
        return Tweet.from_dict(doc.to_dict())


    def get_tweets_by_user_id_and_range(self, user_id: int,
                                        start_time_ms: int = 0, end_time_ms: int = 0) -> List[Tweet]:
        query = self.client.collection('tweets').where('user_id', '==', user_id) \
            .where('created_at_ms', '>=', start_time_ms) \
            .where('created_at_ms', '<=', end_time_ms)
        results = query.get()
        return [Tweet.from_dict(result) for result in results]

    def get_tweets_by_username_and_range(self, username: str,
                                         start_time_ms: int = 0, end_time_ms: int = 0) -> List[Tweet]:
        query = self.client.collection('tweets').where('username', '==', username) \
            .where('created_at_ms', '>=', start_time_ms) \
            .where('created_at_ms', '<=', end_time_ms)
        results = query.get()
        return [Tweet.from_dict(result) for result in results]

    def get_tweets_by_range(self, start_time_ms: int = 0, end_time_ms: int = 0) -> List[Tweet]:
        query = self.client.collection('tweets').where('created_at_ms', '>=', start_time_ms) \
            .where('created_at_ms', '<=', end_time_ms)
        results = query.get()
        return [Tweet.from_dict(result) for result in results]


tweet_service = TweetService()
