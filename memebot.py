from text_generate.markov_chain import MarkovChain


SECRET_SAUCE = ['dril', 'sosadtoday', 'PakaluPapitio']

class Memebot():
	"""
	The dankest memes.
	"""
	# TODO: a lot of stuff
	def gather_inputs(self, tweet_scraper):
		tweets = []
		for username in SECRET_SAUCE:
			tweets.extend(tweet_scraper.scrape_tweets(username))
		return tweets

	def generate_meme(self, order, tweets):
		chain = MarkovChain(order)
		for tweet in tweets:
			try:
				chain.parse_string(tweet)
			except ValueError:
				continue
		return chain.generate_tweet()
