from django.db import models

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    measurements = list()

    def __str__(self):
        return self.name

    @staticmethod
    def from_mongo(dto):
        place = Place()
        place.id = dto['_id']
        place.name = dto['name']
        place.measurements = dto['measurements']
        return place

class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    variable_id = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return str(self.id) + " - " + str(self.variable_id) + " - " + str(self.place_id) + " - " + str(self.datetime) + " - " + str(self.value)

    @staticmethod
    def from_mongo(dto):
        measurement = Measurement()
        measurement.id = dto['_id']
        measurement.variable_id = dto['variable_id']
        measurement.place_id = dto['place_id']
        measurement.datetime = dto['datetime']
        measurement.value = dto['value']
        return measurement