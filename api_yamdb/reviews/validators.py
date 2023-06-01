import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if not (1000 < value <= timezone.now().year):
        raise ValidationError('Указан не корректный год произведения')


def validate_regex(value):
    reg = re.compile(r'^[\w.@+-]+')
    if not reg.match(value):
        raise ValidationError('тест')
