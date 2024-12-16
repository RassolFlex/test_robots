from datetime import datetime

from django.core.exceptions import ValidationError

from robots.models import Robot


def validate_data(data):
    FIELDS = ('model', 'version', 'created')
    FORMAT = '%Y-%m-%d %H:%M:%S'

    for field in FIELDS:
        if field not in data:
            raise ValidationError(f'Не указано: {field}')

    try:
        if len(
            data.get('model', '')
        ) > Robot._meta.get_field('model').max_length:
            raise ValidationError('Слишком длинное поле "model"')
        if len(
            data.get('version', '')
        ) > Robot._meta.get_field('version').max_length:
            raise ValidationError('Слишком длинное поле "version"')
        datetime.strptime(data['created'], FORMAT)
    except ValidationError as e:
        raise e

    return data
