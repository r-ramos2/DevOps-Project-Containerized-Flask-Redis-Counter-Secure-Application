import os
import time
import redis
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port, socket_timeout=1, retry_on_timeout=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def increment_vote_count():
    retries = 5
    while True:
        try:
            return cache.incr('votes')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def home():
    count = get_hit_count()
    return render_template('index.html', visit_count=count)

@app.route('/vote', methods=['POST'])
def vote():
    increment_vote_count()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
