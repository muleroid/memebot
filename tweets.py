import oauth2 as oauth
import time

class TweetHelper():
    """
    Helper class for accessing Twitter APIs. Takes care
    of oauth business.
    """

    def __init__(self, consumer, token):
        self.consumer = consumer
        self.token = token

    def _get_oauth_params(self):
        return {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_consumer_key': self.consumer.key,
            'oauth_token': self.token.key,
        }

    def _generate_request(self, url, method, post_params=None):
        params = self._get_oauth_params()
        if post_params:
            params.update(post_params)

        req = oauth.Request(method=method, url=url, parameters=params)
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)

        return req
