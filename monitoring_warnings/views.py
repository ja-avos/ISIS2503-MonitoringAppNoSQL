import datetime
import monitoring_warnings.logic as warning_logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@api_view(["GET", "POST"])
def warnings(request):
    if request.method == "GET":
        warnings = warning_logic.getWarnings()
        return JsonResponse([warning.__dict__ for warning in warnings], safe=False)
    
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            warning = warning_logic.createWarning(data)
            response = {
                "objectId": str(warning.id),
                "message": f"Advertencia en lugar {warning.place_id} creada en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(["GET"])
def warningDetail(request, warning_id):
    try:
        warning = warning_logic.getWarning(warning_id)
        return JsonResponse(warning.__dict__, safe=False)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)

@api_view(["POST"])
def warningsFilter(request):
    try:
        data = JSONParser().parse(request)
        start = datetime.datetime.strptime(data["startDate"], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(data["endDate"], '%Y-%m-%d %H:%M:%S')
        warnings = warning_logic.getWarnings(from_date=start, to_date=end)
        return JsonResponse([warning.__dict__ for warning in warnings], safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
