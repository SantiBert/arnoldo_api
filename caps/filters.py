from django_filters import FilterSet
from django_filters import rest_framework as filters

from .models import Episodies

class EpisodiesFilter(FilterSet):
    class Meta:
        model = Episodies
        fields = ["name","description"]