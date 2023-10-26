from flask import Flask, request
from flask import render_template
import requests
import time
import json
import jsonpickle
import funct_videomaker

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/make_video/<string>")
def get_subreddits(string):
    funct_videomaker.make_video(string.replace("123-1..43gg3", "?"))
    return "successful"

if __name__ == "__main__":
    app.run()

