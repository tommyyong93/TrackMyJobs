import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='startswith')
    name_contains = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    date_applied = django_filters.DateFromToRangeFilter(field_name='date_applied',label='Date Applied (Between)',widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'MM/DD/YYYY'}))

    class Meta:
        model = Job
        fields = ['status','location']
