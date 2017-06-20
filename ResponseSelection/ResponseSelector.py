import json
import requests
import urllib
from Preprocessing import config
from Data import Database, DataAccess
from ResponseSelection import FeatureOneSelector
from NLP.TextParser import TextParser

class ResponseSelector:

    @staticmethod
    def requestUserName(req, action):
        originalRequest = req.get("originalRequest")
        data = originalRequest.get("data")
        sender = data.get("sender")
        id = sender.get("id")
        access_token = config.access_token
        rs = urllib.urlopen("https://graph.facebook.com/v2.6/" + id + "?fields=first_name&access_token=" + access_token)
        name = json.load(rs).get("first_name")
        print(name)
        event_name = ""
        if ("welcome" in action):
            event_name = "FACEBOOK_WELCOME"
            db  = Database.Database()
            db.insert("User",["FBID"],[id],"","")

        elif ("help" in action):
            event_name = "help_name_event"
        return {
            "speech": "",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "webhook-ResponseSelector",
            "followupEvent": {"name": event_name, "data": {"user": name}}
        }


    def webSearch(self, query):
        Tx = TextParser()
        t = Tx.tokenize(query.lower())
        k = Tx.removeStopWords(t)
        query = ''.join(k)
        if query == '':
            print ("NO QUERY")
            return {
                "speech": "",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "webhook-ResponseSelector",
                "followupEvent": {"name": "fallback"}
            }
        print ("Q:", query)
        url = "https://www.googleapis.com/customsearch/v1?key=" \
              + config.api_key + "&cx=" + config.engine_id + "&q=" + query
        response = requests.get(url)
        jData = response.json()
        results = jData.get("items")
        if len(results)==0:
            print("JSON: ", 0)
            return {
                "speech": "",
                "displayText": "",
                "data": {},
                "contextOut": [],
                "source": "webhook-ResponseSelector",
                "followupEvent": {"name": "fallback"}
            }
        first = results[0]
        print("JSON: ", first)
        text = first.get("title")
        displayLink = first.get("displayLink")
        url = first.get("link")
        return {
            "speech": "",
            "displayText": "",
            "data": {
                "facebook": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "image_aspect_ratio":"square",
                            "elements": [
                                {
                                    "title": text,
                                    "subtitle":displayLink,

                                    "buttons": [{
                                        "type": "web_url",
                                        "url": url,
                                        "title": "View"
                                    }
                                    ]
                                }
                            ]
                        }
                    }
                }
            },
            "contextOut": [],
            "source": "webhook-FeatureOneSelector"
        }



    def notification(self):
        '''
        call select fn in DB Access
        then get users that have been idle for 2 days 
        then send to them a message
        
        :return: 
        '''
        dummy = ""
        print ("hanoma in notification :D ")