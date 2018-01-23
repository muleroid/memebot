from collections import defaultdict
import random

class ProbabilityDistribution():
	"""
	Simple class backed by a dict that tracks
	occurrences of strings
	"""
	def __init__(self):
		self._distribution = defaultdict(int)
		self._total = 0

	def add_token(self, token):
		self._distribution[token] += 1
		self._total += 1

	def get(self):
		index = random.random() * self._total
		running = 0

		for token, count in self._distribution.items():
			running += count
			if running >= index:
				return token

class MarkovChain():
	"""
	Can this even be called a markov chain?
	"""
	def __init__(self):
		self.token_map = defaultdict(ProbabilityDistribution)

	def prep_chain(self, tokens):
		for i in range(len(tokens) - 1):
			token = tokens[i]
			distribution = self.token_map[token]
			distribution.add_token(tokens[i+1])

	def get_next_token(self, token):
		"""
		Given a token, returns the next token given
		the weighted distribution of the current state
		"""
		distribution = self.token_map[token]
		return distribution.get()
