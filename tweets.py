import oauth2 as oauth
import time

from urllib.parse import urlencode

class TweetHelper():
    """
    Helper class for accessing Twitter APIs. Takes care
    of oauth business.
    """

    def __init__(self, consumer, token):
        self.consumer = consumer
        self.token = token
        self.client = oauth.Client(consumer, token)

    def _get_oauth_params(self):
        return {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_consumer_key': self.consumer.key,
            'oauth_token': self.token.key,
        }

    def _generate_request(self, url, method, additional_params=None):
        params = self._get_oauth_params()
        if additional_params:
            params.update(additional_params)

        req = oauth.Request(method=method, url=url, parameters=params)
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)

        return req

    def get(self, url, params=None):
        if params:
            url = url + '?' + urlencode(params)

        return self.client.request(url, headers=self._get_oauth_params())

    def post(self, url, params=None):
        self.client.request(url, method='POST', headers=self._get_oauth_params(), body=urlencode(params))
