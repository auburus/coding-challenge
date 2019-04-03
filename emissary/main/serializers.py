from rest_framework import serializers
from emissary.main.models import Link, Visit

class VisitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visit
        fields = ('date_time', 'ip', 'user_agent', 'link')

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('created_at', 'title', 'slug', 'visits_count')
