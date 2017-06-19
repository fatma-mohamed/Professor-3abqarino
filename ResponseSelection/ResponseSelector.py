import json
import urllib
from Preprocessing import config
from Data import Database
from ResponseSelection import FeatureOneSelector

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
        if '?' in query:
            featureOne = FeatureOneSelector.FeatureOneSelector(query)
            return featureOne.getAnswer()
        else:
            return{
                "speech": "",
                "displayText": "",
                "source": "webhook-ResponseSelector",
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