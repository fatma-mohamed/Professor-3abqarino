#!/usr/bin/env python
from Data import Database

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from ResponseSelection import ResponseSelector, FeatureTwoSelector
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
    if req.get("result").get("action") == "request_user_name":
        return responseSelector.requestUserName(req)
    elif req.get("result").get("action") == "createDB":
        conn = Database.Database()
        return DataPreprocessing.__run__(conn)
    elif req.get("result").get("action") == "InsertQuestions_Answers":
        return DataPreprocessing.DataPreprocessing().insertQuestions_Answers()
    elif req.get("result").get("action") == "request-game":
        return FeatureTwoSelector.getRandomQuestion()
    else:
        return {}



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')


