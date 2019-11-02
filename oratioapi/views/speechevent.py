
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from oratioapi.models import SpeechEvent, Speech, Event
from .speech import SpeechSerializer

"""Author: Krystal Gates
Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE entries for orderproduct.
Methods: GET DELETE(id) POST"""

class SpeechEventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    class Meta:
        model = SpeechEvent
        url = serializers.HyperlinkedIdentityField(
            view_name='speechevent',
            lookup_field='id'
        )
        fields = ('id', 'url', 'speech', 'event')

        depth = 1


class SpeechEvents(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized SpeechEvent instance
        """
        new_speechevent = SpeechEvent()
        event = Event.objects.get(pk=request.data["event_id"])
        new_speechevent.event = event
        speech = Speech.objects.get(pk=request.data["speech_id"])
        new_speechevent.speech = speech

        new_speechevent.save()

        serializer = SpeechEventSerializer(new_speechevent, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single SpeechEvent
        Returns:
            Response -- JSON serialized SpeechEvent instance
        """
        try:
            speechevent = SpeechEvent.objects.get(pk=pk)
            serializer = SpeechEventSerializer(speechevent, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a order
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            speechevent = SpeechEvent.objects.get(pk=pk)
            speechevent.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except SpeechEvent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to SpeechEvents resource
        Returns:
            Response -- JSON serialized list of SpeechEvents
        """
        speechevents = SpeechEvent.objects.all()

        speech = self.request.query_params.get('product', None)
        event = self.request.query_params.get('order', None)

        if speech is not None:
            speechevents = speechevents.filter(speech__id=speech)
        if event is not None:
            speechevents = speechevents.filter(event_name=request.data["name"])
        # if payment is not None:
        #     SpeechEvents = SpeechEvents.filter(payment__none=None)


        serializer = SpeechEventSerializer(
            speechevents, many=True, context={'request': request})
        return Response(serializer.data)