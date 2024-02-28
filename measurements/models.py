from django.db import models

class Variable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    min_threshold = models.FloatField()
    max_threshold = models.FloatField()
    
    def __str__(self):
        return self.name

class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    variable_id = models.CharField(max_length=100)
    place_id = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return str(self.id) + " - " + str(self.variable_id) + " - " + str(self.place_id) + " - " + str(self.datetime) + " - " + str(self.value)