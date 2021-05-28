import os
import sys
import time
import requests
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def index():
    return "Method used: %s" % request.method


@app.route("/update")
def update():

    req = request

    data = req.args

    print(data['value1'], data['value2'])

    x = 0


if __name__ == "__main__":
    app.run(debug=True)
