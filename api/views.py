import json

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.servises import get_robots_in_a_period, get_file
from api.validators import validate_data
from robots.models import Robot


@csrf_exempt
@require_http_methods(['POST'])
def add_robot(request):
    """
    Добавление робота в базу данных.
    """

    data = json.loads(request.body)
    validated_data = validate_data(data)
    validated_data['serial'] = (
        f"{validated_data['model']}-{validated_data['version']}"
    )

    robot = Robot(**validated_data)
    robot.save()

    return JsonResponse(data=data, status=201)


@require_http_methods(['GET'])
def download_production_list(request):
    """
    Создание и скачаивание списка роботов
    за определённый период в формате xlsx.

    Доступ только для Директора.
    """

    if request.user.username != 'Director':
        return HttpResponseForbidden()

    robots = get_robots_in_a_period()
    get_file(robots)

    with open('robots.xlsx', 'rb') as f:
        response = HttpResponse(
            f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="robots.xlsx"'
        return response
