import json
import urllib
import requests
import datetime
from Preprocessing import config
from Data import Database, DataAccess

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
            ResponseSelector().registerUser(id)
        elif ("help" in action):
            event_name = "help_name_event"
        return {
            "speech": "",
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "prof-3abqarino",
            "followupEvent": {"name": event_name, "data": {"user": name}}
        }

    def registerUser(self, pageScopedID):
        db = Database.Database()
        appScopedID = self.getAppScopedID(pageScopedID)
        db.insert("User", ["Page_ScopedID", "App_ScopedID"], [pageScopedID, appScopedID], ["Page_ScopedID", "App_ScopedID"], "")

    def getAppScopedID(self, pageScopedID):
        name = self.getName(pageScopedID)

        # Get conversations, then get the sender with the required name, then get the appScopedID and return it.
        conversations = self.getConversations()
        print conversations
        for conversation in conversations:
            participants = conversation.get("participants").get("data")
            for participant in participants:
                if participant.get("name") == name:
                    return participant.get("id")

    def getName(self, pageScopedID):
        access_token = config.access_token
        url = "https://graph.facebook.com/v2.9/" + str(pageScopedID) + "?access_token=" + access_token + "&fields=first_name,last_name"
        r = requests.get(url)
        print(r.status_code, r.reason)
        result = json.loads(r.text)
        name = result.get("first_name") + " " + result.get("last_name")
        print(name)
        return name

    def getUsersToNotify(self):
        ids = []
        conversations = self.getConversations()
        for conversation in conversations:
            print "---------------- name"
            print conversation.get("participants").get("data")[0].get("name")
            print "-------------name end"
            updated_time = conversation.get("updated_time")
            updated_time = updated_time.replace("T", " ")  # Replace separator of date and time by " " instead of T -- To match current_time format
            millisecondsIndex = updated_time.find("+")  # Get milliseconds index
            updated_time = updated_time[:millisecondsIndex - len(updated_time)]  # Remove milliseconds
            updated_time = datetime.datetime.strptime(updated_time, "%Y-%m-%d %H:%M:%S")  # Convert to datetime object
            current_time = datetime.datetime.now() - datetime.timedelta(hours=2)  # Convert to GMT (now - 2H)
            resultedTime = current_time - updated_time  # Didn't talk since...
            dayIndex = str(resultedTime).find("day")  # Get day index in result, -1 if not exist
            if(True or (dayIndex > 0 and int(str(resultedTime)[:dayIndex-1])) >= 2):  # If day exists and number of days more than 2 ,, then notify user.
                conversationData = conversation.get("participants").get("data")
                for participant in conversationData:
                    if participant.get("id") != config.page_id:  # Current participant isn't the page
                        appScopedID = participant.get("id")
                        print "--------app scoped id"
                        print appScopedID
                        print "---------appp scode"
                        pageScopedID = DataAccess.DataAccess().select("User", ["Page_ScopedID"], ["App_ScopedID"], [appScopedID], "")
                        print "---------------- Page scoped iD----"
                        print pageScopedID
                        print "---------------- Page scoped ID end"
                        if pageScopedID != []:
                            print "in not none"
                            ids.append(pageScopedID)
                            break
        return ids

    def getConversations(self):
        access_token = config.access_token
        url = "https://graph.facebook.com/v2.9/me/conversations?access_token=" + access_token + "&fields=participants,updated_time"

        r = requests.get(url)
        print(r.status_code, r.reason)
        conversations = json.loads(r.text)
        return conversations.get("data")

    def notifyUser(self):
        listOfUsersToNotify = self.getUsersToNotify()

        access_token = config.access_token
        url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + access_token

        for userID in listOfUsersToNotify:
            paramRecipient = { "id": userID}
            content = DataAccess.DataAccess().selectRandom("Notification", ["Message", "Attachment"], [], [], "")
            msg = content[0][0]
            attachment = content[0][1]
            if(attachment != None): #If there's an attachment, send it before the message itself
                attachedGif = DataAccess.DataAccess().selectRandom("Gifs", ["Url"], ["Gif_Tag"], ["'" + attachment + "'"], "")
                paramUrl = {"url":attachedGif[0][0]}
                paramPayload = json.dumps(paramUrl, ensure_ascii=False)
                paramAttachment = {}
                paramAttachment["type"] = "image"
                paramAttachment["payload"] = json.dumps(paramPayload, ensure_ascii=False)
                requestJSON = {}
                requestJSON["recipient"] = json.dumps(paramRecipient, ensure_ascii=False)
                requestJSON["message"] = json.dumps(paramAttachment, ensure_ascii=False)

                r = requests.post(url, data=requestJSON, headers={'Content-type': 'application/json'})
                print(r.status_code, r.reason)
                print(r.text[:300] + '...')

            paramMessage = {"text": msg}
            requestJSON = {}
            requestJSON["recipient"] = json.dumps(paramRecipient, ensure_ascii=False)
            requestJSON["message"] = json.dumps(paramMessage, ensure_ascii=False)
    
            r = requests.post(url, data = requestJSON, headers={'Content-type': 'application/json'})
            print(r.status_code, r.reason)
            print(r.text[:300] + '...')

    def about(self):
        page_id = config.page_id
        access_token = config.access_token
        url = "https://graph.facebook.com/v2.9/" + page_id + "?access_token=" + access_token + "&fields=about"
        r = requests.get(url)
        print(r.status_code, r.reason)
        result = json.loads(r.text)
        about = result.get("about")
        print(about)
        return {
            "speech": about,
            "displayText": "",
            "data": {},
            "contextOut": [],
            "source": "about"
        }