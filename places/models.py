from django.db import models

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Warning(models.Model):
    id = models.AutoField(primary_key=True)
    place_id = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return str(self.id) + " - " + str(self.place_id) + " - " + str(self.datetime)