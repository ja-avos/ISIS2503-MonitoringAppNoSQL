import datetime

class Place():
    id = str()
    name = str()
    measurements = list()
    critical = bool()

    def __str__(self):
        return self.name

    @staticmethod
    def from_mongo(dto):
        place = Place()
        place.id = str(dto.get('_id', ''))
        place.name = dto.get('name', '')
        place.measurements = dto.get('measurements', [])
        place.critical = dto.get('critical', False)
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
        measurement.id = str(dto.get('_id', ''))
        measurement.variable_id = dto.get('variable_id', '')
        measurement.place_id = dto.get('place_id', '')
        measurement.datetime = dto.get('datetime', datetime.datetime.now())
        measurement.value = dto.get('value', 0.0)
        return measurement