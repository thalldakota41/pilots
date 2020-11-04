import django_filters

from .models import *

class PilotFilter(django_filters.FilterSet):
    class Meta:
        model = Pilot
        fields = '__all__'