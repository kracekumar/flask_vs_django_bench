#flask simple app
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/index')
def index():
    return jsonify({'hello': 'world'})


if __name__ == "__main__":
    app.run()
