class Variable():
    id = str()
    name = str()
    min_threshold = float()
    max_threshold = float()
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def from_mongo(dto):
        variable = Variable()
        variable.id = str(dto['_id'])
        variable.name = dto['name']
        variable.min_threshold = dto['min_threshold']
        variable.max_threshold = dto['max_threshold']
        return variable