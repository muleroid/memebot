from typing import List, Optional, Tuple

class Tokenizer():
    """
    Simple n-order tokenizer.
    """
    def __init__(self, n: int, s: str):
        """
        Initializes tokenizer. Given a string input,
        splits it into tokens.
        """
        self.order = n
        self.words = [word.strip() for word in s.split()]
        self.results = []  # type: List[Tuple[Tuple, Optional[str]]]
        if len(self.words) <= self.order:
            raise ValueError('Tokenized input is shorter than order of tokenizer')

    def generate_tokens(self) -> List[Tuple[Tuple, Optional[str]]]:
        """
        Generates tokens based on words.
        """
        for i in range(self.order, len(self.words)):
            n_words = tuple(self.words[i - j] for j in range(self.order, 0, -1))
            self.results.append((n_words, self.words[i]))

        # also log the ending words
        end_words = tuple(self.words[i] for i in range(self.order * -1, 0))
        self.results.append((end_words, None))
        return self.results
