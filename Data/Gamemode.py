import urllib
import json
import os

import psycopg2
import urlparse

class Gamemode:
    connection = None

    def getRandomQuestion(self):
        conn = Database.Database()
        cur = conn.cursor()
        print "--------Getting a random Question--------"
        cur.execute("SELECT * FROM "Questions_Answers" OFFSET floor(random()*(SELECT COUNT(*) FROM "Questions_Answers")) LIMIT 1")
        rows = cur.fetchall()

        for row in rows:
            Question = row[0]
            print "Question = ", Question, "\n"
            A1 = row[1]
            print "A1 = ", A1, "\n"
            A2 = row[2]
            print "A2 = ", A2, "\n"
            A3 = row[3]
            print "A3 = ", A3, "\n"
            CA_ID = row[4]
            print "CA_ID = ", CA_ID, "\n"
        print "--------Got question--------"

        conn.close()
        
        return {
        "speech" : "",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "get-random-question",
        "followupEvent":{
            "name":"Question_Answers",
            "data":{
                "Question":Question,
                "A1":A1,
                "A2":A2,
                "A3":A3,
                "CA_ID":CA_ID
                }
            }
        }
