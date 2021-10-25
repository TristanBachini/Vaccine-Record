import django_filters
from django_filters import CharFilter
from .models import *

class RecordFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='istartswith')
    last_name = CharFilter(field_name='last_name', lookup_expr='istartswith')

    class Meta:
        model = PatientRecord
        # fields = '__all__'
        fields = ['id','bday']