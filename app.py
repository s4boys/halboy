import praw
from flask import Flask, escape, request
from random import randrange

default_sub = "earthporn"
default_query = "France"

def bot_login():
	r = praw.Reddit(client_id = "LEEBAVxoj1949A",
					client_secret = "aZ_38CJIX5caWkeCS0z-IVokSD8",
					user_agent = "linux:LEEBAVxoj1949A:0.1 (by /u/oneSAPpyboy)")
	return r
	
def get(r, sub, query, timeframe):
	buffer = ""
	rand_index = randrange(10)
	i = 0;
	for submission in r.subreddit(sub).search(query, sort='relevance', syntax='lucene', time_filter=timeframe):
		if i == rand_index:
			buffer = submission.url
			break
		else:
			i += 1
	return buffer

def bot(sub, query, time):
	handle = bot_login()
	result = get(handle, sub, query, time)
	return result

app = Flask(__name__)

valid_timeframes = frozenset(['all', 'day', 'hour', 'month', 'week', 'year'])

@app.route('/')
def hello():
	sub = request.args.get("sub", "earthporn")
	query = request.args.get("query", "France")
	result = bot(sub, query)
	return f'{escape(result)}'

@app.route('/r/<string:sub>')
def submatch(sub):
	query = request.args.get("query", "France")
	timeframe = request.args.get("time", "all").lower()

	if timeframe not in valid_timeframes:
		return f'Invalid timeframe parameter: {escape(timeframe)}'
	else:
		result = bot(sub, query, timeframe)
		return f'{escape(result)}'

if __name__ == "__main__":
	result = bot(default_sub, default_query)