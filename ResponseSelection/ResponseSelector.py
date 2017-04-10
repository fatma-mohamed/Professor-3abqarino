import json
import urllib
from Preprocessing import  config

class ResponseSelector:


    def requestUserName(req):
        originalRequest = req.get("originalRequest")
        data = originalRequest.get("data")
        sender = data.get("sender")
        id = sender.get("id")
        access_token = config.access_token
        rs = urllib.urlopen("https://graph.facebook.com/v2.6/" + id + "?fields=first_name&access_token=" + access_token)
        name = json.load(rs).get("first_name")
        print(name)
        return {
            "speech": "",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "prof-3abqarino",
            "followupEvent": {"name": "name_event", "data": {"user": name}}
        }