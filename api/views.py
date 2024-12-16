import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.validators import validate_data
from robots.models import Robot


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        validated_data = validate_data(data)
        validated_data['serial'] = (
            f"{validated_data['model']}-{validated_data['version']}"
        )
        robot = Robot(**validated_data)
        robot.save()
        return JsonResponse(data=data, status=201)
