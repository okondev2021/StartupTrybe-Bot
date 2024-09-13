from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import IdeaValidation
from . serializers import IdeaValidationSerializer
from .utility import generate_response


# Create your views here.

class Validator(viewsets.ModelViewSet):
  queryset = IdeaValidation.objects.all()
  serializer_class = IdeaValidationSerializer

  def create(self, request):
    data = request.data
    bot_response = generate_response(request.data['user_idea'], request.data['user_target_market'])
    if request.user.is_authenticated:
      data['bot_response'] = bot_response
      data['user_info'] = request.user
      serializer = self.get_serializer(data = data)
      if serializer.is_valid():
        serializer.save()
        return Response({"response": bot_response}, status.HTTP_201_CREATED)

    return Response({"response": bot_response}, status.HTTP_200_OK)

  # def list(request):
  #   pass