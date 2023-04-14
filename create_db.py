from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todo = db.todo





# import mysql.connector

# my_db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd = "password123",

# )

# my_cursor = my_db.cursor()

# my_cursor.execute("CREATE DATABASE")