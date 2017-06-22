#!/usr/bin/env python
import urllib
import json
import os

from flask import Flask ,render_template
from flask import request
from flask import make_response

from ResponseSelection import ResponseSelector, FeatureTwoSelector
from Preprocessing import *

# Flask app should start in global layout
app = Flask(__name__)
responseSelector = ResponseSelector.ResponseSelector()

@app.route('/index')
@app.route('/',methods=['POST','GET'])
def Home():
    return render_template('index.html')

@app.route('/notify', methods=['POST','GET'])
def notify():
    responseSelector = ResponseSelector.ResponseSelector()
    responseSelector.notifyUser()

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
    elif req.get("result").get("action") == "request-game":
        return FeatureTwoSelector.FeatureTwoSelector().getRandomQuestion()
    elif req.get("result").get("action") == "check-answer":
        return FeatureTwoSelector.FeatureTwoSelector().CheckAnswerCorrectness(req.get("result").get("parameters"))
    elif req.get("result").get("action") == "add-menu":
        return MenuPreprocessing.MenuPreprocessing().addMenu()
    elif req.get("result").get("action") == "about":
        return ResponseSelector.ResponseSelector().about()
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')


