from typing import Any, Dict


class Tweet():
    def __init__(self, id: int, text: str, user_id: int, username: str):
        self.id = id
        self.text = text
        self.user_id = user_id
        self.username = username

    @staticmethod
    def from_tweet_json(json: Dict[str, Any]) -> 'Tweet':
        user = json.get('user', {})

        # check for extended tweets
        if json.get('truncated'):
            text = json.get('extended_tweet', {}).get('full_text')
        else:
            text = json.get('text')

        return Tweet(
            id=int(json.get('id_str')),
            text=text,
            user_id=int(user.get('id_str')),
            username=user.get('screen_name'),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'username': self.username,
        }
