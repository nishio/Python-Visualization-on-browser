import argparse
import json
from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
import core

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/to_bytecode")
def to_bytecode():
    code = json.loads(request.args['code'])
    callback = request.args['callback']
    try:
        ret = core.to_bytecode(code)
    except Exception, e:
        ret = json.dumps({'error': str(e)})

    return "%s(%s)" % (callback, ret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python visualize server')
    parser.add_argument('--port', default=8104, type=int)

    args = parser.parse_args()
    app.run('0.0.0.0', args.port)
