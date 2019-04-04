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
    but I could have pretty much done it that way if this is the way the team works.

    get:
    Return a list of all the links

    post:
    Create a new link.

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

class LinkDetails(APIView):
    """Perform specific actions on a single link

    Be able to update its title and/or slug, or delete it

    get:
    Obtain link information

    put:
    Change link title and/or slug. Title is a mandatory field, and it DOES NOT update
    the slug by default. This is to avoid unknowingly changing a publicly facing
    endpoint that is already available. 

    patch:
    Change link title and/or slug. There are no mandatory fields, and it DOES NOT update
    the slug by default. See `put` for more reference.

    delete:
    Delete this link and all its associated data.
    """

    def get_link(self, pk):
        try:
            return Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        link = self.get_link(pk)
        serializer = LinkSerializer(link)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        link = self.get_link(pk)
        serializer = LinkSerializer(link, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        link = self.get_link(pk)
        serializer = LinkSerializer(link, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        link = self.get_link(pk)
        link.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class Landing(APIView):
    """Landing page for all referral links

    Every time this page is visited for a valid link, its number of visits
    is increased

    get:
    Retrieve the landing page for a link. If the link provided does not exist, it
    is redirected to a 404 error, to avoid having visits to the landing page that are
    not assigned to a link.
    """

    def get(self, request, slug, format=None):
        try:
            link = Link.objects.get(slug=slug)
        except Link.DoesNotExist:
            raise Http404

        visitSerializer = VisitSerializer.build_from_request(request)

        # Create the validated data list
        visitSerializer.is_valid()

        link.save_visit(visitSerializer.validated_data)

        return Response({'title': link.title, 'text': "Tim has just made a revolutionary invention!"}, status=status.HTTP_200_OK)

