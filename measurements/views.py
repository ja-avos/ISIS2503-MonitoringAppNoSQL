from django.shortcuts import render
from rest_framework import api_view

@api_view(["GET", "POST"])
def variables(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    variables = db['variables']
    if request.method == "GET":
        result = []
        data = variables.find({})
        for dto in data:
            jsonData = {
                'id': str(dto['_id']),
                "variable": dto['variable'],
                'threshold': dto['threshold']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        result = variables.insert(data)
        respo ={
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)

# Create your views here.
