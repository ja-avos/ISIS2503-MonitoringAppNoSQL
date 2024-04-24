import datetime

class Place():
    id = str()
    name = str()
    measurements = list()

    def __str__(self):
        return self.name

    @staticmethod
    def from_mongo(dto):
        place = Place()
        place.id = str(dto['_id'])
        place.name = dto['name']
        place.measurements = dto['measurements']
        return place

class Measurement():
    id = str()
    variable_id = str()
    datetime = datetime.datetime.now()
    value = float()

    def __str__(self):
        return str(self.id) + " - " + str(self.variable_id) + " - " + str(self.place_id) + " - " + str(self.datetime) + " - " + str(self.value)

    @staticmethod
    def from_mongo(dto):
        measurement = Measurement()
        measurement.id = str(dto['_id'])
        measurement.variable_id = dto['variable_id']
        measurement.place_id = dto['place_id']
        measurement.datetime = dto['datetime']
        measurement.value = dto['value']
        return measurement