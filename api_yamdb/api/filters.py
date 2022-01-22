from django_filters import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category', method='filter_category')
    name = CharFilter(field_name='name', lookup_expr='contains')
    genre = CharFilter(field_name='genre', method='filter_genre')

    def filter_category(self, queryset, name, category):
        return queryset.filter(category__slug__in=category.split(','))

    def filter_genre(self, queryset, name, genre):
        return queryset.filter(genre__slug__in=genre.split(','))

    class Meta():
        model = Title
        fields = ['name', 'category', 'year', 'genre']
