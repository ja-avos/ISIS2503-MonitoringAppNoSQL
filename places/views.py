import places.logic as places_logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@api_view(["GET", "POST"])
def places(request):
    
    if request.method == "GET":
        places = places_logic.getPlaces()
        return JsonResponse([place.__dict__ for place in places], safe=False)

    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            place = places_logic.createPlace(data)
            response = {
                "objectId": str(place.id),
                "message": f"Lugar {place.name} creado en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(["GET", "POST", "DELETE"])
def placeDetail(request, place_id):
    if request.method == "GET":
        try:
            place = places_logic.getPlace(place_id)
            return JsonResponse(place.__dict__, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)

    if request.method == "DELETE":
        result = places_logic.deletePlace(place_id)
        respo = {
            "objectID": str(result),
            "Mensaje": "Se ha borrado un lugar"
        }
        return JsonResponse(respo, safe=False)

@api_view(["POST"])
def measurements(request, place_id):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            add_result = places_logic.add_measurement(place_id, data)
            response = {
                "result": str(add_result),
                "message": f"Medición en lugar con ID {place_id} creada en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(["POST"])
def average(request, place_id):
    try:
        data = JSONParser().parse(request)
        average_data = places_logic.get_average(place_id, data)

        result = {
            "place": average_data["place"],
            "variable": average_data["variable"],
            "average": average_data["average"]
        }

        return JsonResponse(result, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)
