from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from oratioapi.models import Speech
from django.contrib.auth.models import User

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
        fields = ('id', 'url', 'user', 'title', 'date', 'set_time', 'actual_time', 'transcript', 'um', 'uh', 'like')
        depth = 2

class Speeches(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Speech instance
        """
        new_speech = Speech()
        new_speech.user = User.objects.get(pk=request.user.pk)
        new_speech.title = request.data["title"]
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
        speech.actual_time = request.data["actual_time"]
        speech.transcript = request.data["transcript"]
        speech.um = request.data["um"]
        speech.uh = request.data["uh"]
        speech.like = request.data["like"]

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
        speeches = Speech.objects.filter(user=request.user.pk)

        incomplete = self.request.query_params.get('incomplete', None)

        if incomplete is not None:
            # speeches = Speech.objects.filter(actual_time__isnull=True)
            speeches = Speech.objects.filter(actual_time=None)


        serializer = SpeechSerializer(
            speeches, many=True, context={'request': request})
        return Response(serializer.data)


