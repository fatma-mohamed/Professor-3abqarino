import requests
import json

from Preprocessing import config

class MenuPreprocessing:

    def __run__(self):
        self.deleteMenu()
        self.addMenu()
        print("Menu preprocessing done!")

    def addMenu(self):
        access_token = config.access_token
        url = config.graph_api_url + "me/messenger_profile?access_token=" + access_token

        browse_submenu = [{
                "title":"Answers",
                "type":"postback",
                "payload":"Help_Get_Answers"
            },
            {
                "title":"Quiz games",
                "type":"postback",
                "payload":"Game"
            }]

        more_submenu = [{
                "title":"About",
                "type":"postback",
                "payload":"about"
            },
            {
                "title": "Feedback",
                "type": "web_url",
                "url": "https://www.surveymonkey.com/r/8MC3BQ2"
            },
            {
                "title":"Restart",
                "type":"postback",
                "payload":"Get Started"
            }]

        main_menu = [{
                "title":"Browse",
                "type":"nested",
                "call_to_actions":json.dumps(browse_submenu, ensure_ascii=False)
            },
            {
                "title":"Help",
                "type":"postback",
                "payload":"Help"
            },
            {
                "title":"More",
                "type":"nested",
                "call_to_actions":json.dumps(more_submenu, ensure_ascii=False)
            }]

        presistent_menu = [{
                "locale":"default",
                "composer_input_disabled":False,
                "call_to_actions":json.dumps(main_menu, ensure_ascii=False)
            },
            {
                "locale":"zh_CN",
                "composer_input_disabled":False
            }]
    
        values = {}
        values["persistent_menu"] = json.dumps(presistent_menu, ensure_ascii=False)

        r = requests.post(url, data = values, headers={'Content-type': 'application/json'})
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')
        print ("--------------------->>>>>>>>>>>>>>" + "<<<<<<<<<<<<--------------------")

    def deleteMenu(self):
        access_token = config.access_token
        url = config.graph_api_url + "me/messenger_profile?access_token=" + access_token

        fields = ["persistent_menu"]
        values = {}
        values["fields"] = json.dumps(fields, ensure_ascii=False)
    
    
        r = requests.delete(url, data = values, headers={'Content-type': 'application/json'})
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')
        print ("--------------------->>>>>>>>>>>>>>" + "SUCCESS" + "<<<<<<<<<<<<--------------------")
        
