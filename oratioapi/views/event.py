"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from oratioapi.models import Event, Speech, SpeechEvent
from .speech import SpeechSerializer
from .speechevent import SpeechEventSerializer
from django.contrib.auth.models import User
# from oratioapi.views.speechevent import

"""
Purpose: Allows a user to communicate with the Oratio database to GET POST and DELETE entries for events.
Methods: GET DELETE(id) POST
"""

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events

    Arguments:
        serializers
    """

    speeches = SpeechSerializer(many=True)
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'speeches')
        depth = 2

class Events(ViewSet):

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized ProductType instance
        """


        # current_user = User.objects.get(pk=request.user.id)
        event = Event.objects.filter(name=request.data["name"])

        if event.exists():
            print("Event in db. Add it and the speech to SpeechEvent")
            speech_event = SpeechEvent()
            speech_event.speech = Speech.objects.get(pk=request.data["speech_id"])
            speech_event.event = event[0]
            speech_event.save()
        else:
            print("No event by this name. Make new event to add speech to")
            new_event = Event()
            new_event.name = request.data["name"]
            new_event.save()
            # speech_event.event = new_event



        # serializer = EventSerializer(speech_event, context={'request': request})

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
        """Handle PUT requests for events

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        # event.name = request.data["name"]
        speech = request.data["speech_id"]

        if speech is not None:
            event.speech = Speech.objects.get(pk=speech)
            event.save()

        # if event.name is not None:
        #     event.nam

        else:
            speech = Speech.objects.get(pk=request.data["speech_id"])
            speechevent = SpeechEvent.objects.filter(event=event, speech=speech)[0]
            speechevent.delete()

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

        withspeeches = self.request.query_params.get('withspeeches', None)

        if withspeeches is not None:
            for event in events:
                events = Event.objects.exclude(speeches=None)
                # event.speeches = related_speeches

        # events = events.filter(user_id=request.user.id)


        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

