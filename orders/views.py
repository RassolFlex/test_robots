import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# from orders.forms import CreateOrderForm
from orders.models import Order
from orders.validators import validate_data
from customers.models import Customer
from robots.models import Robot


@csrf_exempt
@require_http_methods(['POST'])
def add_order(request):
    """
    Добавление заказа в базу данных.

    На вход принимает данные в виде json:
        `{`\n
            `"customer": "<адрес_электронной_почты>",`
            `"robot_serial": "<серийный_номер_робота>"`\n
        `}`
    """

    data = json.loads(request.body)
    validated_data = validate_data(data)

    customer, _ = Customer.objects.get_or_create(
        email=validated_data['customer'])
    robot_serial = validated_data['robot_serial']

    if Robot.objects.filter(serial=robot_serial).exists():
        return JsonResponse(
            {'message': 'Робот есть в наличии, быстрее приобретайте!'},
            status=200
        )
    if Order.objects.filter(customer=customer,
                            robot_serial=robot_serial
                            ).exists():
        return JsonResponse({'message': 'Заявка уже сделана, ожидайте'},
                            status=200)
    else:
        Order.objects.create(customer=customer,
                             robot_serial=robot_serial)
        return JsonResponse({'message': 'Заявка принята, ожидайте'},
                            status=201)
