import datetime

class Warning():
    id = str()
    place_id = str()
    datetime = datetime.datetime.now()
    
    def __str__(self):
        return str(self.id) + " - " + str(self.place_id) + " - " + str(self.datetime)
    
    @staticmethod
    def from_mongo(dto):
        warning = Warning()
        warning.id = str(dto['_id'])
        warning.place_id = dto['place_id']
        warning.datetime = dto['datetime']
        return warning