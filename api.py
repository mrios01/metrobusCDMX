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

#Define our JSONEncoder:
#Extensible JSON encoder for Python data structures.
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#Define our application and API route paths
app = tornado.web.Application(
    [
        (r"/municipality/(?P<municipality_name>[a-zA-Z_-]{1,50}$)", MunicipalityHandler),
        (r"/municipalities", MunicipalitiesHandler),
        (r"/id/(?P<id>[0-9]{1,10}$)", VehicleHandler),
        (r"/all_units", AllUnitsHandler),
        (r"/", MainHandler)
    ],
    db=db,
)

#Start our application on port 8000
if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()