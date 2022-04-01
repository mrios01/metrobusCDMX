#Import Libraries

import json
import tornado.ioloop
import tornado.web
import tornado.web
from tornado.options import define, options
import motor
import pprint
import json
from bson import ObjectId

#Define Constants
define("port", default=8888, help="run on the given port", type=int)
#Connect to database
connection = motor.MotorClient(
    "mongodb+srv://miguel:4531194169@serverlessinstance0.k8rxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#Get an instance of database collection metrobus
db = connection.metrobus



