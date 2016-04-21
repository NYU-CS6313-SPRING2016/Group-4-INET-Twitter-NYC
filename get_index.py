import ast
import json

def add_tweet_info(tweet, topic_word, dest_list):
	if topic_word != '':
		for topic in topic_info:
			if topic["topic_word"] == topic_word:
				topic["count"] += 1
				topic["tweets"].append({
											"created_at": tweet["created_at"],
											"screen_name": tweet["screen_name"],
											"followers_count": tweet["followers_count"],
											"text": tweet["text"]
										})
				return
		# if topic not included, add this topic
		dest_list.append({
							"topic_word" : topic_word,
							"count" : 1,
							"tweets" : [{
											"created_at": tweet["created_at"],
											"screen_name": tweet["screen_name"],
											"followers_count": tweet["followers_count"],
											"text": tweet["text"]
										}]
						})


#def data_generator(topic_word, dest_list, num_topic):
#	for i in range(0, num_topic):
#		dest_list.append(
#						 {"created_at":"Sat Apr 16 23:57:23 +0000 2016","screen_name":"Ruthless4Real","followers_count":379,
#						 "hashtags":[{"topic": topic_word}],"text":"I'm at @%s in Toms River, NJ https://t.co/sUOueL37pJ" %topic_word}
#						)


#read in data and convert string type to list type

input_file = open("my_data2.json", 'r')
data_to_crawl = input_file.read()

data_to_crawl = ast.literal_eval(data_to_crawl)


topic_info = []


for tweet in data_to_crawl:
	for hashtags in tweet["hashtags"]:
		add_tweet_info(tweet, hashtags["topic"], topic_info)

topic_info = json.dumps(topic_info)
print topic_info

input_file.close()


