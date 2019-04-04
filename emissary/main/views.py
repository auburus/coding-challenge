from emissary.main.models import Link, Visit
from emissary.main.serializers import LinkSerializer, VisitSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LinkList(APIView):
    """Get a list of all the valid links and their visits or create a new link.

    Note: There is a tradeoff on the level of abstraction used
    in the views. I have not used the mixins to avoid falling into
    too much abstraction, and to try to be more explicit than implicit,
    but I see it as a organitzations decision, depending on the team.
    """

    def get(self, request, format=None):
        links = Link.objects.all()
        serializer = LinkSerializer(links, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LinkSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Landing(APIView):
    """Landing page for all referral links"""

    def get(self, request, slug, format=None):
        try:
            link = Link.objects.get(slug=slug)
        except Link.DoesNotExist:
            raise Http404

        visitSerializer = VisitSerializer.build_from_request(request)

        # Create the validated data list
        visitSerializer.is_valid()

        link.save_visit(visitSerializer.validated_data)

        return Response({'title': link.title, 'text': "lorem ipsum"}, status=status.HTTP_200_OK)

