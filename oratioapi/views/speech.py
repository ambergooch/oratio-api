from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from oratioapi.models import Speech

class SpeechSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for speeches

    Arguments:
        serializers
    """
    class Meta:
        model = Speech
        url = serializers.HyperlinkedIdentityField(
            view_name='speech',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'date', 'set_time', 'actual_time', 'transcript', 'um', 'uh', 'like')
        depth = 2

class Speeches(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Speech instance
        """
        new_speech = Speech()
        new_speech.user = request.auth.user
        new_speech.date = request.data["date"]
        new_speech.set_time = request.data["set_time"]
        new_speech.actual_time = request.data["actual_time"]
        new_speech.transcript = request.data["transcript"]
        new_speech.um = request.data["um"]
        new_speech.uh = request.data["uh"]
        new_speech.like = request.data["like"]

        new_speech.save()

        serializer = SpeechSerializer(new_speech, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single speech

        Returns:
            Response -- JSON serialized speech instance
        """
        try:
            speech = Speech.objects.get(pk=pk)
            serializer = SpeechSerializer(speech, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a speech

        Returns:
            Response -- Empty body with 204 status code
        """
        speech = Speech.objects.get(pk=pk)
        speech.starttime = request.data["starttime"]
        speech.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single speech

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            speech = Speech.objects.get(pk=pk)
            speech.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Speech.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to list speeches for authenicated customer

        Returns:
            Response -- JSON serialized list of speeches
        """
        # customer = Customer.objects.get(user=request.auth.user)
        speeches = Speech.objects.filter(user=request.auth.user)

        serializer = SpeechSerializer(
            speeches, many=True, context={'request': request})
        return Response(serializer.data)


