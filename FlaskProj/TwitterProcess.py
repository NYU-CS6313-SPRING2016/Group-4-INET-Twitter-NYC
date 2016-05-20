# -*- coding: utf-8 -*-
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import common_word
# Import the necessary package to process data in JSON format
# try:
import json
# except ImportError:
# 	import simplejson as json

class TwitterProcess:
	def __init__(self):
		# Variables that contains the user credentials to access Twitter API 
		self.ACCESS_TOKEN = '703706843978330112-Vtx3ZBhoay3AoYGky1lCzy9bBMQWDRC'
		self.ACCESS_SECRET = 'g8dHFdnKpi4xXqmyVGlQLPRnnAqVGtIRmEkwRS2hBzV5S'
		self.CONSUMER_KEY = '96Q7FV1SgqFHObyGRdq88RUZs'
		self.CONSUMER_SECRET = 'HDZmc1hVFQI6bG9pxdR47zXaKlz0JDDyGfzVa2L5RNpFFKhAF9'
		self.oauth = OAuth(self.ACCESS_TOKEN, self.ACCESS_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)

	def get_data(self):
		# Initiate the connection to Twitter Streaming API
		twitter_stream = TwitterStream(auth=self.oauth)
		MAX = 1000
		tweet_count = MAX

		raw_data_set = []
		print ''
		for tweet in iterator:
			# Twitter Python Tool wraps the data returned by Twitter 
			# as a TwitterDictResponse object.
			# We convert it back to the JSON format to print/score
			data = json.dumps(tweet) # dumps can convert dic to json
			data = json.loads(data)  #loads can convert json to dic
	
			if data["entities"]["hashtags"] == []:
				continue
			data = {
				"hashtags" : data["entities"]["hashtags"],
				"text": data["text"],
				"screen_name": data["user"]["screen_name"],
				"followers_count": data["user"]["followers_count"],
				"created_at": data["created_at"],
				"coordinates": data["place"]["bounding_box"]["coordinates"],
				"place": data["place"]["full_name"]
			}
			raw_data_set.append(data)
			# The command below will do pretty printing for JSON data, try it out
			# print json.dumps(tweet, indent=4)
			#counter += 1
			#print "get %d tweets" % counter
			tweet_count -= 1
			print tweet_count
			if tweet_count <= 0:
				raw_data_set = json.dumps(raw_data_set)
				output_file = open("twitter_data.json", "w")
				output_file.write(raw_data_set)
				output_file.close()
				break
# 		
	def process_data(self):
		
# 		