import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>一沐日</h1>"
    homepage += "<a href=/webhook>webhook</a><br>"
    return homepage
	
@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "fangeChoice"):
        fange =  req.get("queryResult").get("parameters").get("fange")
        info = "您想查詢的飲料是：" + fange
    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#    app.run()