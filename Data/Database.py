import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import psycopg2
import urlparse

class Database:
    connection = None
    
    def __init__(self):
        print ("--------in Database __init__--------")
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
        print ("--------Opened database successfully--------")

    def __createTables__(self):
        print ("--------in Database createTables--------")
        self.createTable_Answers()
        self.createTable_Keywords()
        self.createTable_Answers_Keywords()
        self.createTable_Synonyms()
        self.createTable_Questions_Answers()
        self.createTable_Tag()
        self.createTable_Gifs()
        self.createTable_User()
        self.createTable_Notification()

        self.connection.commit()
        print ("--------Tables created successfully--------")

       ### conn.close()
       ### print "--------Connection closed--------"
        return

    def __deleteTables__(self):
        print ("--------in Database deleteTables--------")
        self.deleteTable_Answers_Keywords()
        self.deleteTable_Answers()
        self.deleteTable_Synonyms()
        self.deleteTable_Keywords()
        self.deleteTable_Questions_Answers()
        self.deleteTable_Gifs()
        self.deleteTable_User()
        self.deleteTable_Notification()
        self.deleteTable_Tag()

        self.connection.commit()
        print ("--------Tables deleted successfully--------")


    def createTable_Answers(self):
        print ("--------in Database createTable_Answers--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Answer TEXT NOT NULL);''')
        print ("--------Table Answers created successfully--------")

    def deleteTable_Answers(self):
        print ("--------in Database deleteTable_Answers--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Answers";''')
        print ("--------Table Answers deleted successfully--------")


    def createTable_Keywords(self):
        print ("--------in Database createTable_Keywords--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Keywords"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Keyword TEXT NOT NULL,
               Category TEXT NOT NULL);''')
        print ("--------Table Keywords created successfully--------")

    def deleteTable_Keywords(self):
        print ("--------in Database deleteTable_Keywords--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Keywords";''')
        print ("--------Table Keywords deleted successfully--------")


    def createTable_Answers_Keywords(self):
        print ("--------in Database createTable_Answers_Keywords--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Answers_Keywords"
               (Answer_ID INT NOT NULL,
               Keyword_ID INT NOT NULL,
               FOREIGN KEY (Answer_ID) REFERENCES "Answers"(ID),
               FOREIGN KEY (Keyword_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Answer_ID, Keyword_ID));''')
        print ("--------Table Answers_Keywords created successfully--------")

    def deleteTable_Answers_Keywords(self):
        print ("--------in Database deleteTable_Answers_Keywords--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Answers_Keywords";''')
        print ("--------Table Answers_Keywords deleted successfully--------")


    def createTable_Synonyms(self):
        print ("--------in Database createTable_Synonyms--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Synonyms"
               (Key_ID INT NOT NULL,
               Synonym TEXT NOT NULL,
               FOREIGN KEY (Key_ID) REFERENCES "Keywords"(ID),
               PRIMARY KEY(Key_ID, Synonym));''')
        print ("--------Table Synonyms created successfully--------")

    def deleteTable_Synonyms(self):
        print("--------in Database deleteTable_Synonyms--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Synonyms";''')
        print ("--------Table Synonyms deleted successfully--------")


    def createTable_Questions_Answers(self):
        print ("--------in Database createTable_Questions_Answers--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Questions_Answers"
               (ID SERIAL PRIMARY KEY NOT NULL,
               Question TEXT NOT NULL,
               Answer_1 TEXT NOT NULL,
               Answer_2 TEXT NOT NULL,
               Answer_3 TEXT NOT NULL,
               Correct_AnswerID INT NOT NULL,
               CONSTRAINT uniqueQAs UNIQUE (Question, Answer_1, Answer_2, Answer_3, Correct_AnswerID));''')
        print ("--------Table Questions_Answers created successfully--------")

    def deleteTable_Questions_Answers(self):
        print ("--------in Database deleteTable_Questions_Answers--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Questions_Answers";''')
        print("--------Table Questions_Answers deleted successfully--------")


    def createTable_Tag(self):
        print("--------in Database createTable_Tag--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Tag"
                       (ID SERIAL PRIMARY KEY NOT NULL,
                       Tag TEXT NOT NULL UNIQUE);''')
        print("--------Table Tag created successfully--------")

    def deleteTable_Tag(self):
        print ("--------in Database deleteTable_Tag--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Tag";''')
        print("--------Table Tag deleted successfully--------")


    def createTable_Gifs(self):
        print("--------in Database createTable_Gifs--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Gifs"
                       (ID SERIAL PRIMARY KEY NOT NULL,
                       Name TEXT NOT NULL,
                       Url TEXT NOT NULL,
                       Gif_Tag TEXT NOT NULL,
                       FOREIGN KEY (Gif_Tag) REFERENCES "Tag"(Tag));''')
        print("--------Table Gifs created successfully--------")

    def deleteTable_Gifs(self):
        print ("--------in Database deleteTable_Gifs--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Gifs";''')
        print("--------Table Gifs deleted successfully--------")


    def createTable_User(self):
        print("--------in Database createTable_User--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "User"
                       (ID SERIAL PRIMARY KEY NOT NULL,
                       Page_ScopedID INT NOT NULL UNIQUE,
                       App_ScopedID INT NOT NULL UNIQUE,
                       CONSTRAINT uniqueUIDs UNIQUE (Page_ScopedID, App_ScopedID));''')
        print("--------Table User created successfully--------")

    def deleteTable_User(self):
        print ("--------in Database deleteTable_User--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "User";''')
        print("--------Table User deleted successfully--------")


    def createTable_Notification(self):
        print("--------in Database createTable_Notification--------")
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE "Notification"
                       (ID SERIAL PRIMARY KEY NOT NULL,
                       Message TEXT NOT NULL UNIQUE,
                       Attachment TEXT,
                       FOREIGN KEY (Attachment) REFERENCES "Tag"(Tag));''')
        print("--------Table Notification created successfully--------")

    def deleteTable_Notification(self):
        print ("--------in Database deleteTable_Notification--------")
        cur = self.connection.cursor()
        cur.execute('''DROP TABLE "Notification";''')
        print("--------Table Notification deleted successfully--------")


    def deleteData(self):
        cur = self.connection.cursor()
        cur.execute('''DELETE FROM "Answers_Keywords";''')
        cur.execute('''DELETE FROM "Answers";''')
        cur.execute('''DELETE FROM "Synonyms";''')
        cur.execute('''DELETE FROM "Keywords";''')
        cur.execute('''DELETE FROM "Questions_Answers";''')
        cur.execute('''DELETE FROM "Gifs";''')
        cur.execute('''DELETE FROM "User";''')
        cur.execute('''DELETE FROM "Notification";''')
        cur.execute('''DELETE FROM "Tag"''')
        self.connection.commit()


    def insert(self, table_name, cols, values, conflict_fields, conflict_do):
        cur = self.connection.cursor()

        cols_str = "( "
        cols_size = len(cols)
        for i in range(0, cols_size):
            if i == cols_size - 1:
                cols_str += str(cols[i])
                break
            cols_str += (str(cols[i]) + ", ")
        cols_str += (" )")

        values_str = "( "
        values_size = len(values)
        for i in range(0, values_size):
            if i == values_size - 1:
                values_str += str(values[i])
                break
            values_str += (str(values[i]) + ", ")
        values_str += (" )")

        conflict_fields_str = "( "
        conflict_fields_size = len(conflict_fields)
        for i in range(0, conflict_fields_size):
            if i == conflict_fields_size - 1:
                conflict_fields_str += str(conflict_fields[i])
                break
            conflict_fields_str += (str(conflict_fields[i]) + ", ")
        conflict_fields_str += (" )")

        if (not conflict_fields):
            cur.execute('''INSERT INTO "''' + table_name + '''" ''' + cols_str + " VALUES " + values_str);
        else:
            if (conflict_do == ''):
                cur.execute('''INSERT INTO "''' + table_name + '''" ''' + cols_str + " VALUES " + values_str +
                            " ON CONFLICT " + conflict_fields_str + " DO NOTHING");
            else:
                cur.execute('''INSERT INTO "''' + table_name + '''" ''' + cols_str + " VALUES " + values_str +
                            " ON CONFLICT " + conflict_fields_str + " DO " + conflict_do);

        self.connection.commit()
        cur.close()
