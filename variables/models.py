from django.db import models

class Variable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    min_threshold = models.FloatField()
    max_threshold = models.FloatField()
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def from_mongo(dto):
        variable = Variable()
        variable.id = dto['_id']
        variable.name = dto['name']
        variable.min_threshold = dto['min_threshold']
        variable.max_threshold = dto['max_threshold']
        return variable