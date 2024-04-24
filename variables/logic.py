from variables.models import Variable
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime

def getVariables():
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables_collection = db['variables']
    variables_collection = variables_collection.find({})
    variables = [ Variable.from_mongo(variable) for variable in variables_collection ]
    client.close()

    return variables

def getVariable(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables_collection = db['variables']
    variable = variables_collection.find_one({'_id': ObjectId(id)})
    client.close()

    if variable is None:
        raise ValueError('Variable not found')

    return Variable.from_mongo(variable)

def verifyVariableData(data):
    if 'name' not in data:
        raise ValueError('name is required')
    
    variable = Variable()
    variable.name = data['name']
    variable.min_threshold = data['min_threshold'] if 'min_threshold' in data else None
    variable.max_threshold = data['max_threshold'] if 'max_threshold' in data else None

    return variable

def createVariable(data):

    # Verify variable data
    variable = verifyVariableData(data)

    # Create variable in MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables_collection = db['variables']
    variable.id = variables_collection.insert(
        {
            'name': variable.name,
            'min_threshold': variable.min_threshold,
            'max_threshold': variable.max_threshold
        }
    )
    client.close()
    return variable

def deletePlace(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    result = places_collection.remove({'_id': ObjectId(id)})
    client.close()
    return result

def updateVariable(id, data):

    # Verify variable data
    variable = verifyVariableData(data)

    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables_collection = db['variables']
    result = variables_collection.update(
        {'_id': ObjectId(id)},
        {'$set': {
            'name': variable.name,
            'min_threshold': variable.min_threshold,
            'max_threshold': variable.max_threshold
            }
        }
    )
    client.close()
    return result