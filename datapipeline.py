# Import Libraries

import urllib, urllib.request, json
import pprint
import requests
import pymongo
import pandas as pd
from pymongo import MongoClient
import re
import datetime
from bson import ObjectId
import unidecode

#Declare Constants -> Access Tokens

MAPS_API_KEYS='AIzaSyAabU45w1hEuoya-m_8EYHYbPoQ4RfMX10'
COPOMEX_API_KEYS='6b0f6b3f-6985-4f05-a300-8a4cca8a363a' #Not Used
DB_username='miguel'
DB_password='4531194169'

#Connect to MongoDb Database
client = pymongo.MongoClient("mongodb+srv://miguel:4531194169@serverlessinstance0.k8rxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.metrobus
buses =  db.buses
postal_code = db.postal_code

#Retrieve Data from Mexico City's metrobus 
metrobus_url = 'https://datos.cdmx.gob.mx/datastore/dump/ad360a0e-b42f-482c-af12-1fd72140032e?format=json'
fileobj = urllib.request.urlopen(metrobus_url)
metrobus_response=(fileobj.read().decode('utf-8'))
metrobus_data = json.loads(metrobus_response)
#pprint.pprint(data)

#Get keys from field's array except for 'id'
key_data =[]
for item in metrobus_data['fields']:
    key_data.append(item['id'])
#pprint.pprint(key_data)

bus_data = {} #Dictionary for each bus information
location = {} #Dictionary for each bus location
pc = {}
for item in metrobus_data['records']:
    for x in range (len(item)): #iterate each item of bus data and fill the dictionary with key gathered
        if key_data[x] != 'id':
            bus_data[key_data[x]]=item[x]
    #pprint.pprint(bus_data)
    #pprint.pprint(------------------)
    #Get Location Address from Geo Data Ponints Latitude and Longitude 
    maps_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(bus_data['position_latitude']) + ',' + str(bus_data['position_longitude']) + '&key=' + MAPS_API_KEYS)
    maps_data = maps_response.content.decode('utf-8')
    maps_json = json.loads(maps_data)
    #pprint.pprint(maps_json)
    #Add maps data to location
    for location_data in maps_json['results'][0]['address_components']:
        #print(location_data['types'][0])
        #print(location_data['long_name'])
        #Transformar información sin acentos y en minúsculas
        location[location_data['types'][0]]=unidecode.unidecode(location_data['long_name'].lower())
    #copomex_response = requests.get('https://api.copomex.com/query/info_cp/'+str(location['postal_code'])+'?token=pruebas')    
    #copomex_data = copomex_response.content.decode('utf-8')
    #copomex_json = json.loads(copomex_data)
    #location['municipality'] = copomex_json[0]['response']['municipio']
    #pprint.pprint(location['postal_code'])
    #Find the municipality given a posta code
    #Use micodigopostal.org as a free source to find municipality given a postal code
    #Service is "free"
    tables = pd.read_html('https://micodigopostal.org/buscarcp.php?buscar=' + str(location['postal_code']))
    cp_table = tables[0]
    #Transform data to lower case and no accents
    municipality_lowercase = unidecode.unidecode(cp_table['Municipio'][0].lower())
    #municipality_final = municipality_lowercase.replace(" ","")
    #municipality_final = municipality_white_space.replace(".","")
    #Delete white spaces and periods from municipality string
    municipality_final = re.sub('[ .]', '', municipality_lowercase)
    location['municipality'] = municipality_final
    #Add location data to bus data
    bus_data['location'] = location
    #bus_data['date'] = datetime.datetime.utcnow()
    bus_data['_id'] = ObjectId()
    #pprint.pprint(bus_data)
    #Save postal code and Municipality for availability
    pc['postal_code'] = location['postal_code']
    pc['municipality'] = municipality_final
    pc['_id'] = ObjectId()

    #pprint.pprint(pc)
    #try:
    #If bus not in database save bus
    if not buses.find_one({'vehicle_id':bus_data['vehicle_id']}):
        bus_id = buses.insert_one(bus_data).inserted_id
    #except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
        #continue

    #try:
    #If postal code not in database save postal code
    if not postal_code.find_one({'municipality':pc['municipality']}):
        postal_code_id = postal_code.insert_one(pc).inserted_id
    #except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
        #continue
