from monitoring_warnings.models import Warning
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime

def getWarnings(from_date=None, to_date=None):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warnings_collection = db['warnings']

    db_filter = {}

    if from_date is not None:
        db_filter['datetime'] = { '$gte': from_date }
    if to_date is not None:
        db_filter['datetime'] = { '$lt': to_date }

    warnings_collection = warnings_collection.find(db_filter)
    warnings = [ Warning.from_mongo(warning) for warning in warnings_collection ]
    client.close()

    return warnings

def getWarning(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    warnings_collection = db['warnings']
    warning = warnings_collection.find_one({'_id': ObjectId(id)})
    client.close()

    if warning is None:
        raise ValueError('Warning not found')

    return Warning.from_mongo(warning)

def verifyWarningData(data):
    if 'place' not in data:
        raise ValueError('place id is required')
    
    warning = Warning()
    warning.place_id = data['place']
    warning.datetime = datetime.datetime.now()

    return warning

def createWarning(data):

    # Verify warning data
    warning = verifyWarningData(data)

    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db

    # Verify place exists
    places_collection = db['places']
    place = places_collection.find_one({'_id': ObjectId(warning.place_id)})
    if place is None:
        raise ValueError('Place not found')

    # Create warning in MongoDB
    warnings_collection = db['warnings']
    warning.id = warnings_collection.insert(
        {
            'place_id': warning.place_id,
            'datetime': warning.datetime
        }
    )
    client.close()
    return warning
