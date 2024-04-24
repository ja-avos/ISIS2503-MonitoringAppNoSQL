from django.db import models

class Warning(models.Model):
    id = models.AutoField(primary_key=True)
    place_id = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return str(self.id) + " - " + str(self.place_id) + " - " + str(self.datetime)
    
    @staticmethod
    def from_mongo(dto):
        warning = Warning()
        warning.id = dto['_id']
        warning.place_id = dto['place_id']
        warning.datetime = dto['datetime']
        return warning