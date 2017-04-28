#!/usr/bin/env python
from Data import Database

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from ResponseSelection import ResponseSelector, FeatureOneSelector, FeatureTwoSelector
from Preprocessing import *

# Flask app should start in global layout
app = Flask(__name__)
responseSelector = ResponseSelector.ResponseSelector()

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
        print ("i get a question :D ")
        question = (req.get("result")).get("resolvedQuery")
        responseSelector = FeatureOneSelector.FeatureOneSelector(question)
        answer =  responseSelector.getAnswer()
        print (answer)
        return {

            "speech": answer,
            "source": "prof-3abqarino_webhook",
            "displayText": "okk"

        }
    elif req.get("result").get("action") == "createDB":
        conn = Database.Database()
        return DataPreprocessing.DataPreprocessing().__run__(conn)
    elif req.get("result").get("action") == "InsertQuestions_Answers":
        return DataPreprocessing.DataPreprocessing().insertQuestions_Answers()
    elif req.get("result").get("action") == "request-game":
        return FeatureTwoSelector.FeatureTwoSelector().getRandomQuestion()
    elif req.get("result").get("action") == "check-answer":
        return FeatureTwoSelector.FeatureTwoSelector().CheckAnswerCorrectness(req.get("result").get("parameters"))
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')


