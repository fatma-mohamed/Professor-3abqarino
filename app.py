#!/usr/bin/env python
from Data.Database import Database
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from ResponseSelection import ResponseSelector
from ResponseSelection import FeatureOneSelector

from Preprocessing.DataPreprocessing import DataPreprocessing

# Flask app should start in global layout
app = Flask(__name__)
responseSelector = None
@app.route('/webhook', methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    action = req.get("result").get("action")
    if "request_user_name" in action:
        responseSelector = ResponseSelector.ResponseSelector()
        return responseSelector.requestUserName(req, action)
    elif action == "Ask-a-question.Ask-a-question-custom":
        responseSelector = FeatureOneSelector.FeatureOneSelector()
        question = (req.get("result")).get("resolvedQuery")
        print (question)
        return responseSelector.getAnswer(question)
    elif action == "insert":
        DataPreprocessing.insertAnswers_and_keywords()
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')


