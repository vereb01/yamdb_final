from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    """Фильтрация по заданному полю."""

    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = rest_framework.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
