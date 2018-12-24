class Tokenizer():
	"""
	Simple n-order tokenizer.
	"""
	def __init__(self, n):
		self.order = n
		self.results = []

	def generate_tokens(self, s):
		"""
		Given a string input, breaks it into tokens
		and generates a list mapping n tokens to the
		next token.
		"""
		tokens = [token.strip() for token in s.split()]
		if len(tokens) <= self.order:
			raise ValueError('Tokenized input is shorter than order of tokenizer')
		for i in range(self.order, len(tokens)):
			n_tokens = tuple(tokens[i - j] for j in range(self.order, 0, -1))
			self.results.append((n_tokens, tokens[i]))

		# also log the ending token
		end_tokens = tuple(tokens[i] for i in range(self.order * -1, 0))
		self.results.append((end_tokens, None))
		return self.results
