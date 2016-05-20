# Import the necessary package to process data in JSON format


def get_data():
	while True:
		try:
			import json
		except ImportError:
			import simplejson as json	
		# Import the necessary methods from "twitter" library
		from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


		# Variables that contains the user credentials to access Twitter API 
		ACCESS_TOKEN = '703706843978330112-Vtx3ZBhoay3AoYGky1lCzy9bBMQWDRC'
		ACCESS_SECRET = 'g8dHFdnKpi4xXqmyVGlQLPRnnAqVGtIRmEkwRS2hBzV5S'
		CONSUMER_KEY = '96Q7FV1SgqFHObyGRdq88RUZs'
		CONSUMER_SECRET = 'HDZmc1hVFQI6bG9pxdR47zXaKlz0JDDyGfzVa2L5RNpFFKhAF9'

		oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

		# Initiate the connection to Twitter Streaming API
		twitter_stream = TwitterStream(auth=oauth)


		# Get a sample of the public data following through Twitter
		iterator = twitter_stream.statuses.filter(locations = '-74,40,-73,41')


		# Print each tweet in the stream to the screen 
		# Here we set it to stop after getting 1000 tweets. 
		# You don't have to set it to stop, but can continue running 
		# the Twitter API to collect data for days or even longer. 
		MAX = 1000
		tweet_count = MAX

		raw_data_set = []

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
				output_file = open("static/data/twitter_data.json", "w")
				output_file.write(raw_data_set)
				output_file.close()
				break
	



	# Process data

		import common_word
		# Import the necessary package to process data in JSON format
		try:
			import json
		except ImportError:
			import simplejson as json

		# if a hashtag in the result , return True and the index
		# else return False and None
		def in_result(hashtag, result):
			for index in range(len(result)):
				if result[index]["hashtag"] == hashtag:
					return True, index
			return False, None
	
		def in_keyword_result(word, keyword_result):
			for index in range(len(keyword_result)):
				if keyword_result[index]["keyword"] == word:
					return True, index
			return False, None

		input_file = open("static/data/twitter_data.json")
		data = input_file.read()
		input_file.close()
		data = json.loads(data)

		result = [] # this result is the hash_tag

		all_words = []  
		keyword_result = []

		mentions_result = []
		mentioners = []

		place_list = []
		treemap_result = []

		for tweet in data:
			#get hash_tag result
			for hashtag in tweet["hashtags"]:
				check, index = in_result(hashtag["text"], result)
				if check == True:
					result[index]["hashtag_num"] += 1
				else:
					result.append({
						"hashtag": hashtag["text"],
						"hashtag_num": 1
					})
	
			#get keyword_result
			words = tweet["text"].split()
			all_words += words
	
			#get mentions
			if tweet["screen_name"] not in mentioners:
				mentions_result.append({
					"mentioners": tweet["screen_name"], 
					"mentioners_num": tweet["followers_count"],
					"text": tweet["text"]
				})
				mentioners.append(tweet["screen_name"])
	
			#get treemap
			if tweet["place"] not in place_list:
				place_list.append(tweet["place"])
				treemap_result.append({"name": tweet["place"], "size": 1})
			else:
				for e in treemap_result:
					if e["name"] == tweet["place"]:
						e["size"] += 1
						break

		#get keyword_result
		for word in all_words:
			if word in common_word.common_word:
				continue
			check, index = in_keyword_result(word, keyword_result)
			if check == True:
				keyword_result[index]["keyword_num"] += 1
			else:
				keyword_result.append({"keyword": word, "keyword_num": 1})

		# sort hashtag_result by count
		for i in range(1, len(result)):
			for index in range(0, len(result) - i):
				if result[index]["hashtag_num"] < result[index + 1]["hashtag_num"]:
					temp = result[index]
					result[index] = result[index + 1]
					result[index + 1] = temp

		# sort keyword_result
		for i in range(1, len(keyword_result)):
			for index in range(0, len(keyword_result) - i):
				if keyword_result[index]["keyword_num"] < keyword_result[index + 1]["keyword_num"]:
					temp = keyword_result[index]
					keyword_result[index] = keyword_result[index + 1]
					keyword_result[index + 1] = temp

		# sort mentions_result
		for i in range(1, len(mentions_result)):
			for index in range(0, len(mentions_result) - i):
				if mentions_result[index]["mentioners_num"] < mentions_result[index + 1]["mentioners_num"]:
					temp = mentions_result[index]
					mentions_result[index] = mentions_result[index + 1]
					mentions_result[index + 1] = temp
			
		# sort treemap
		for i in range(1, len(treemap_result)):
			for index in range(0, len(treemap_result) - i):
				if treemap_result[index]["size"] < treemap_result[index + 1]["size"]:
					temp = treemap_result[index]
					treemap_result[index] = treemap_result[index + 1]
					treemap_result[index + 1] = temp

		# this variable store the first 17 value of result
		filtered_result = []
		counter_result = 0
		while len(filtered_result) <= 17:
			if len(result[counter_result]["hashtag"]) <= 13:
				filtered_result.append(result[counter_result])
			counter_result += 1

		filtered_keyword_result = []
		counter_result = 0
		while len(filtered_keyword_result) <= 17:
			if len(keyword_result[counter_result]["keyword"]) <= 13:
				filtered_keyword_result.append(keyword_result[counter_result])
			counter_result += 1

		filtered_mentions_result = []
		counter_result = 0

		try:
			while len(filtered_mentions_result) <= 34:
				if len(mentions_result[counter_result]["mentioners"]) <= 13:
					filtered_mentions_result.append(mentions_result[counter_result])
				counter_result += 1
		except:
			filtered_mentions_result = mentions_result[0:34]
	
		filtered_result = json.dumps(filtered_result)
		filtered_keyword_result = json.dumps(filtered_keyword_result)
		filtered_mentions_result = json.dumps(filtered_mentions_result)
		treemap_result = json.dumps(treemap_result[0: 30])

		output_file1 = open("static/data/hash_tag.json", "w")
		output_file1.write(filtered_result)
		output_file1.close()

		output_file2 = open("static/data/key_word.json", "w")
		output_file2.write(filtered_keyword_result)
		output_file2.close()

		output_file3 = open("static/data/mentions_tweets.json", "w")
		output_file3.write(filtered_mentions_result)
		output_file3.close()

		output_file4 = open("static/data/treemap.json", "w")
		output_file4.write(treemap_result)
		output_file4.close()

