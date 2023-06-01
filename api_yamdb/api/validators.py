import re
from rest_framework.serializers import ValidationError


PROHIBITED_USERNAMES = ['me', 'mi', 'my', 'i']


def username_validation(value):

    if value.lower() in PROHIBITED_USERNAMES:
        raise ValidationError(f'Недопустимое имя пользователя{value}')
    checked_value = re.match('^[\\w.@+-]+', value)
    if checked_value is None or checked_value.group() != value:
        forbidden_simbol = (
            value[0] if checked_value is None
            else value[checked_value.span()[1]]
        )
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @ . + - _.')
    return value
