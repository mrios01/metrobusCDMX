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

#/municipality/(?P<municipality_name>[a-zA-Z_-]{1,50}$) path Give bus units avaliable for a given municipality
class MunicipalityHandler(tornado.web.RequestHandler):
    #Set Headers Contant Type as Application Json
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self, municipality_name):
        all_units = []
        municipality = municipality_name
        municipality_document = await self.settings["db"]["buses"].find({"location.municipality": municipality}).to_list(200)
        for item in municipality_document:
            all_units.append(item["vehicle_id"])
        self.write(JSONEncoder().encode(all_units))

#/id/(?P<id>[0-9]{1,10}$) path Give location data for a given bus unit
class VehicleHandler(tornado.web.RequestHandler):
    #Set Headers Contant Type as Application Json
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self, id):
        id = id
        vehicle_document = await self.settings["db"]["buses"].find_one({'vehicle_id': int(id)})
        location = vehicle_document["location"]
        self.write(JSONEncoder().encode(location))

#/municipalities path Prints a List of all available municipalities
class MunicipalitiesHandler(tornado.web.RequestHandler):
    #Set Headers Contant Type as Application Json
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self):
        all_municipalities = []
        municipalities_document = await self.settings["db"]["postal_code"].find().to_list(200)
        for item in municipalities_document:
            all_municipalities.append(item["municipality"])
        self.write(JSONEncoder().encode(all_municipalities))

#/all_units path Prints a List with all available units
class AllUnitsHandler(tornado.web.RequestHandler):
    #Set Headers Contant Type as Application Json
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def get(self):
        all_units = []
        all_units_document = await self.settings["db"]["buses"].find().to_list(200)
        for item in all_units_document:
            all_units.append(item["vehicle_id"])
        self.write(JSONEncoder().encode(all_units))

#/ Root Path Prints "Hello World"
class MainHandler(tornado.web.RequestHandler):
    #Set Headers Contant Type as Application Json
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')
    def get(self):
        self.write("Hello World")

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