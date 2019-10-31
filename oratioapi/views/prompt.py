"""View module for handling requests about prompts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from oratioapi.models import Prompt, Speech

class PromptSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for prompts

    Arguments:
        serializers
    """
    class Meta:
        model = Prompt
        url = serializers.HyperlinkedIdentityField(
            view_name='prompt',
            lookup_field='id'
        )
        fields = ('id', 'url', 'question', 'speech')
        depth = 2

class Prompts(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized Prompt instance
        """

        new_prompt = Prompt()
        new_prompt.question = request.data["question"]
        new_prompt.speech = Speech.objects.get(pk=request.data['speech_id'])
        new_prompt.save()

        serializer = PromptSerializer(new_prompt, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single prompt

        Returns:
            Response -- JSON serialized Prompt instance
        """
        try:
            prompt = Prompt.objects.get(pk=pk)
            serializer = PromptSerializer(prompt, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a prompt

        Returns:
            Response -- Empty body with 204 status code
        """
        prompt = Prompt.objects.get(pk=pk)
        prompt.question = request.data["question"]
        prompt.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single prompt

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            prompt = Prompt.objects.get(pk=pk)
            prompt.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Prompt.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to list prompts

        Returns:
            Response -- JSON serialized list of prompts
        """
        prompts = Prompt.objects.all()

        serializer = PromptSerializer(
            prompts, many=True, context={'request': request})
        return Response(serializer.data)
