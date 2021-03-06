from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
redis_connection = os.getenv('REDIS_CONNECTION',"redis")

hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    print(redis_connection)
    if not hasattr(g, redis_connection):
        g.redis = Redis(host=redis_connection, db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def reader_tmpl():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

@app.route("/health", methods=['GET'])
def health():
    return "ok"


if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
