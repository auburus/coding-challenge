from rest_framework import serializers
from emissary.main.models import Link, Visit
from ipware import get_client_ip

class VisitSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for each visit

    Since this serializer should only be used in "internal" applications,
    all the information can be available.
    """

    class Meta:
        model = Visit
        fields = ('id', 'date_time', 'ip', 'user_agent')

    @classmethod
    def build_from_request(cls, request):
        """Builds a partialy filled VisitSerializer from the request"""

        return cls(data={'ip': get_client_ip(request)[0],
                         'user_agent': request.META.get('HTTP_USER_AGENT', '') })


class LinkSerializer(serializers.ModelSerializer):
    """Serializer for each link

    Every visit is also being shown here. In a more real scenario there should be some
    kind of aggregation or pagination present.
    """

    visits = VisitSerializer(read_only=True, many=True)

    class Meta:
        model = Link
        fields = ('created_at', 'title', 'slug', 'visits_count', 'visits')
        depth = 1

