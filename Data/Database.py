import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import psycopg2
import urlparse

class Database:
    __db_connection = None
    __db_cur = None

    def __init(self):
        print "--------in Database __init--------"
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        self.__db_connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )

        print "--------Opened database successfully--------"

    def __createTables__(self, conn):
        self.createTable_Answers(conn)
        self.createTable_Answers_Keywords(conn)
        self.createTable_Keywords(conn)
        self.createTable_Synonyms(conn)
        self.createTable_Questions_Answers(conn)
        print "--------Tables created successfully--------"

        return {
        "speech" : "Created tables",
        "displayText": "",
        "data": {},
        "contextOut": [],
        "source": "create-database"
        }

    def __deleteTables__(self, conn):
        self.deleteTable_Answers_Keywords(conn)
        self.deleteTable_Answers(conn)
        self.deleteTable_Synonyms(conn)
        self.deleteTable_Keywords(conn)
        self.deleteTable_Questions_Answers(conn)
        print "--------Tables deleted successfully--------"


    def createTable_Answers(conn):
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Answer TEXT NOT NULL);''')
        print "--------Table Answers created successfully--------"

    def deleteTable_Answers(conn):
        cur = conn.cursor()
        cur.execute('''DROP TABLE "Answers";''')
        print "--------Table Answers deleted successfully--------"

        
    def createTable_Answers_Keywords(conn):
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "Answers_Keywords"
               (Answer_ID INT NOT NULL,
               Keyword_ID INT NOT NULL,
               FOREIGN KEY (Answer_ID) REFERENCES "Answers"(ID),
               FOREIGN KEY (Keyword_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Answer_ID, Keyword_ID));''')
        print "--------Table Answers_Keywords created successfully--------"

    def deleteTable_Answers_Keywords(conn):
        cur = conn.cursor()
        cur.execute('''DROP TABLE "Answers_Keywords";''')
        print "--------Table Answers_Keywords deleted successfully--------"

        
    def createTable_Keywords(conn):
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "Keywords"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Keyword TEXT NOT NULL,
               Category TEXT NOT NULL);''')
        print "--------Table Keywords created successfully--------"

    def deleteTable_Keywords(conn):
        cur = conn.cursor()
        cur.execute('''DROP TABLE "Keywords";''')
        print "--------Table Keywords deleted successfully--------"

        
    def createTable_Synonyms(conn):
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "Synonyms"
               (Key_ID INT NOT NULL,
               Synonym TEXT NOT NULL,
               FOREIGN KEY (Key_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Key_ID, Synonym));''')
        print "--------Table Synonyms created successfully--------"

    def deleteTable_Synonyms(conn):
        cur = conn.cursor()
        cur.execute('''DROP TABLE "Synonyms";''')
        print "--------Table Synonyms deleted successfully--------"


    def createTable_Questions_Answers(conn):
        cur = conn.cursor()
        cur.execute('''CREATE TABLE "Questions_Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Question TEXT NOT NULL,
               Answer_1 TEXT NOT NULL,
               Answer_2 TEXT NOT NULL,
               Answer_3 TEXT NOT NULL,
               Correct_AnswerID INT NOT NULL);''')
        print "--------Table Questions_Answers created successfully--------"


    def deleteTable_Questions_Answers(conn):
        cur = conn.cursor()
        cur.execute('''DROP TABLE "Questions_Answers";''')
        print "--------Table Questions_Answers deleted successfully--------"
