from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_data(data):
    """
    Валидация входящих данных при добавлении заказа на робота.
    """

    FIELDS = ('customer', 'robot_serial')

    for field in FIELDS:
        if field not in data:
            raise ValidationError(f'Не указано: {field}')

    try:
        if len(data.get('robot_serial', '')) > 5:
            raise ValidationError('Слишком длинное поле "robot_serial"')
        validate_email(data['customer'])
    except ValidationError as e:
        raise e

    return data
