from pymongo import MongoClient

DATABASE = MongoClient()['Assignment'] #Database Name
DEBUG = True
client = MongoClient('localhost', 27017)
