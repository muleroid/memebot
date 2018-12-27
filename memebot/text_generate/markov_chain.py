from collections import defaultdict
import random
from typing import Any, Dict, List, Optional, Tuple

from memebot.text_generate.tokenizer import Tokenizer


class ProbabilityDistribution():
    """
    Simple class backed by a dict that tracks
    occurrences of strings
    """
    def __init__(self):
        self._distribution = defaultdict(int)
        self._total = 0

    def add_word(self, word: Optional[str]) -> None:
        self._distribution[word] += 1
        self._total += 1

    def get(self) -> Optional[str]:
        index = random.random() * self._total
        running = 0

        for word, count in self._distribution.items():
            running += count
            if running >= index:
                return word

        return None

class MarkovChain():
    """
    Can this even be called a markov chain?
    """
    def __init__(self, n: int=1):
        self.token_map = defaultdict(ProbabilityDistribution)  # type: Dict[Any, ProbabilityDistribution]
        self.start_token_map = defaultdict(ProbabilityDistribution)  # type: Dict[int, ProbabilityDistribution]
        self.order = n

    def parse_string(self, s: str) -> None:
        tokenizer = Tokenizer(self.order, s)
        results = tokenizer.generate_tokens()
        for tokens, word in results:
            distribution = self.token_map[tokens]
            distribution.add_word(word)

        # fill in starter words
        for i in range(self.order):
            distribution = self.start_token_map[i]
            distribution.add_word(tokenizer.words[i])

    def generate_tweet(self) -> str:
        words = self._get_start_tokens()
        cur_len = 0
        for word in words:
            cur_len += len(words) + 1
        i = 0
        while True:
            tokens = tuple(words[idx] for idx in range(i, i + self.order))
            next_word = self._get_next_word(tokens)
            if next_word is None:
                break
            cur_len += len(next_word) + 1
            if cur_len > 140:
                break
            words.append(next_word)
            i += 1
        return ' '.join(words)

    def _get_next_word(self, tokens: Tuple) -> Optional[str]:
        """
        Given tokens, returns the next word given
        the weighted distribution of the current state
        """
        if len(tokens) != self.order:
            raise ValueError('Input tokens must be same order as Markov Chain')
        distribution = self.token_map[tokens]
        return distribution.get()

    def _get_start_tokens(self) -> List:
        words = []
        for i in range(self.order):
            words.append(self.start_token_map[i].get())

        return words
