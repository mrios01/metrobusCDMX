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
COPOMEX_API_KEYS='6b0f6b3f-6985-4f05-a300-8a4cca8a363a'
DB_username='miguel'
DB_password='4531194169'

