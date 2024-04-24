import variables.logic as variables_logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@api_view(["GET", "POST"])
def variables(request):
    if request.method == "GET":
        variables = variables_logic.getVariables()
        return JsonResponse([variable.__dict__ for variable in variables], safe=False)
    
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            variable = variables_logic.createVariable(data)
            response ={
                "objectId": str(variable.id),
                "message": f"Variable {variable.name} creada en la base de datos"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(["GET", "POST"])
def variablesDetail(request, variable_id):
    if request.method == "GET":
        try:
            variable = variables_logic.getVariable(variable_id)
            return JsonResponse(variable.__dict__, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            result = variables_logic.updateVariable(variable_id, data)
            response = {
                "objectId": str(result),
                "message": "Se ha actualizado una variable"
            }
            return JsonResponse(response, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=404)
