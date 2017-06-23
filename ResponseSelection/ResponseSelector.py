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
        url = "https://www.googleapis.com/customsearch/v1?key=" \
              + config.api_key + "&cx=" + config.engine_id + "&q=" + query
        response = requests.get(url)
        jData = response.json()
        results = jData.get("items")
        if not results:
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
        second = results[1]
        third = results[2]
        fourth = results[3]
        return {
            "speech": "",
            "displayText": "",
            "data": {
                "facebook": [
                    {
                        "text":"Here are the top results from the web"
                    },
                    {
                        "attachment": {
                            "type": "template",
                            "payload": {
                                "template_type": "list",
                                "top_element_style": "compact",
                                "elements": [
                                    {
                                        "title": first.get("title"),
                                        "subtitle": first.get("snippet"),
                                        "default_action": {
                                            "type": "web_url",
                                            "url": first.get("link")
                                        },
                                        "buttons": [
                                            {
                                                "title": "View",
                                                "type": "web_url",
                                                "url": first.get("link")
                                            }
                                        ]
                                    },
                                    {
                                        "title": second.get("title"),
                                        "subtitle": second.get("snippet"),
                                        "default_action": {
                                            "type": "web_url",
                                            "url": second.get("link")
                                        },
                                        "buttons": [
                                            {
                                                "title": "View",
                                                "type": "web_url",
                                                "url": second.get("link")
                                            }
                                        ]
                                    },
                                    {
                                        "title": third.get("title"),
                                        "subtitle": third.get("snippet"),
                                        "default_action": {
                                            "type": "web_url",
                                            "url": third.get("link")
                                        },
                                        "buttons": [
                                            {
                                                "title": "View",
                                                "type": "web_url",
                                                "url": third.get("link")
                                            }
                                        ]
                                    },
                                    {
                                        "title": fourth.get("title"),
                                        "subtitle": fourth.get("snippet"),
                                        "default_action": {
                                            "type": "web_url",
                                            "url": fourth.get("link")
                                        },
                                        "buttons": [
                                            {
                                                "title": "View",
                                                "type": "web_url",
                                                "url": fourth.get("link")
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ]
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