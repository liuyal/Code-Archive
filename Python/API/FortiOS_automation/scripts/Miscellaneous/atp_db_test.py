import os
import sys
import time
import pymongo
import mysql.connector


def mongo_test():
    mongo = pymongo.MongoClient("mongodb://10.59.71.25:27017/", username='admin', password='fgt123456')
    print(mongo.list_database_names())
    for item in mongo["fgt_test"].list_collection_names():
        print(item)
        for doc in mongo["fgt_test"][item].find({}): print(doc)

def sql_test():
    # mysql -h 127.0.0.1 -P 3306 -u root -p fgt

    db = mysql.connector.connect(host="10.59.71.25", database='fgt', user="root", password="123456")

    cursor = db.cursor()

    cursor.execute("show tables;")

    for tables in cursor.fetchall():
        print(tables[0])

if __name__ == "__main__":
    mongo_test()

