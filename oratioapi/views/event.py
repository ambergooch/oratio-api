"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from oratioapi.models import Event

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events

    Arguments:
        serializers
    """
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')
        depth = 2

class Events(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized ProductType instance
        """

        new_event = Event()
        new_event.name = request.data["name"]
        new_event.save()

        serializer = EventSerializer(new_event, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single eventt

        Returns:
            Response -- JSON serialized Event instance
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product type

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        events = Event.objects.all()

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

