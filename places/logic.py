from places.models import Place, Measurement
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime

def getPlaces():
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    places_collection = places_collection.find({})
    places = [ Place.from_mongo(place) for place in places_collection ]
    client.close()

    return places

def getPlace(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    place = places_collection.find_one({'_id': ObjectId(id)})
    client.close()

    if place is None:
        raise ValueError('Place not found')

    return Place.from_mongo(place)

def verifyPlaceData(data):
    if 'name' not in data:
        raise ValueError('name is required')
    
    place = Place()
    place.name = data['name']

    return place

def createPlace(data):

    # Verify place data
    place = verifyPlaceData(data)

    # Create place in MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    place.id = places_collection.insert(
        {
            'name': place.name,
            'measurements': place.measurements
        }
    )
    client.close()
    return place

def deletePlace(id):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    result = places_collection.remove({'_id': ObjectId(id)})
    client.close()
    return result

def verifyMeasurementData(data):
    if 'variable_id' not in data:
        raise ValueError('variable_id is required')
    if 'value' not in data or not isinstance(data['value'], (int, float)):
        raise ValueError('value is required and must be number')

    measurement = Measurement()
    measurement.variable_id = data['variable_id']
    measurement.value = data['value']
    measurement.datetime = datetime.datetime.now()

    return measurement

def add_measurement(place_id, data):
    # Verify measurement data
    new_measurement = verifyMeasurementData(data)

    # Create measurement in MongoDB
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    place = places_collection.find_one({'_id': ObjectId(place_id)})
    if place is None:
        raise ValueError('Place not found')
    
    place = Place.from_mongo(place)
    measurement_group = next(
        (measurement for measurement in place.measurements
                        if measurement["variable_id"] == new_measurement.variable_id),
        None
    )

    result = None

    if measurement_group is None:
        measurement_group = {
            'variable_id': new_measurement.variable_id,
            'values': [new_measurement.__dict__]
        }
        result = places_collection.update_one(
            {'_id': ObjectId(place_id)},
            {'$push': {'measurements': measurement_group}}
        )
    else:
        measurement_group['values'].append(new_measurement.__dict__)
        result = places_collection.update_one(
            {'_id': ObjectId(place_id)},
            {'$set': {'measurements': place.measurements}}
        )

    client.close()

    return result.modified_count

def verifyAverageData(data):
    if 'variable' not in data:
        raise ValueError('variable is required')

def get_average(place_id, data):

    # Verify average data
    verifyAverageData(data)

    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    places_collection = db['places']
    place = Place.from_mongo(places_collection.find_one({'_id': ObjectId(place_id)}))

    # Obtener nombre de la variable
    variables_collection = db['variables']
    variable = variables_collection.find_one({'_id': ObjectId(data["variable"])})

    if variable is None:
        raise ValueError('Variable not found')

    # Calculo de promedio
    average = 0
    measurement_group = next(
        (measurement for measurement in place.measurements
                        if measurement['variable_id'] == data['variable']),
        None
    )

    if measurement_group is None or len(measurement_group.get('values', [])) == 0:
        return {
            'place': place.name,
            'variable': variable['name'],
            'average': None
        }

    for measure in measurement_group['values']:
        average = average + measure["value"]
    average = average / len(measurement_group["values"])

    client.close()

    return {
        'place': place.name,
        'variable': variable['name'],
        'average': average
    }