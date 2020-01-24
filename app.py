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

def get(r, sub, query, sorter, timeframe):
    buffer = ""
    rand_index = randrange(25)
    i = 0
    if query == None:
        for submission in r.subreddit(sub).top(time_filter=timeframe):
            if i == rand_index:
                if submission.url.endswith(".jpg") or submission.url.endswith(".png")
                    buffer = submission.url
                    break
                else:
                    rand_index += 1
                    i += 1
            else:
                i += 1
    else:
        for submission in r.subreddit(sub).search(query, sort=sorter, syntax='lucene', time_filter=timeframe):
            if i == rand_index:
                buffer = submission.url
                break
            else:
                i += 1
    print("your message", file=sys.stderr)
    return buffer

def bot(sub, query, sorter, time):
    handle = bot_login()
    result = get(handle, sub, query, sorter, time)
    return result

app = Flask(__name__)

valid_timeframes = frozenset(['all', 'day', 'hour', 'month', 'week', 'year'])
valid_sorters = frozenset(['relevance', 'hot', 'top', 'new', 'comments'])

@app.route('/')
def hello():
    sub = request.args.get("sub", "earthporn")
    query = request.args.get("query", "France")
    result = bot(sub, query)
    return f'{escape(result)}'

@app.route('/r/<string:sub>')
def submatch(sub):
    query = request.args.get("query")
    timeframe = request.args.get("time", "all").lower()
    sorter = request.args.get("sort", "relevance").lower()

    if timeframe not in valid_timeframes:
        return f'Invalid timeframe parameter: {escape(timeframe)}'
    elif sorter not in valid_sorters:
        return f'Invalid sort parameter: {escape(sorter)}'
    else:
        result = bot(sub, query, sorter, timeframe)
        return f'{escape(result)}'

if __name__ == "__main__":
    result = bot(default_sub, default_query)
