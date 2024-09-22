from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import IdeaValidation
from rest_framework.permissions import IsAuthenticated, AllowAny
from . serializers import IdeaValidationSerializer
from .utility import generate_response


# Create your views here.

class Validator(viewsets.ModelViewSet):
  queryset = IdeaValidation.objects.all()
  serializer_class = IdeaValidationSerializer

  def create(self, request):
    try:
      data = request.data
      bot_response = generate_response(request.data['user_idea'], request.data['user_target_market'])
      if request.user.is_authenticated:
        data['bot_response'] = bot_response
        data['user_info'] = request.user.id
        serializer = self.get_serializer(data = data, many=False)
        if serializer.is_valid():
          serializer.save()
        else:
          return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": bot_response}, status = status.HTTP_201_CREATED)
      else:
        return Response({"response": bot_response}, status=status.HTTP_200_OK)
    except:
       return Response({"Error"})

  def list(self, request):
    data = IdeaValidation.objects.filter(user_info = request.user)
    serializer = self.get_serializer(data, many = True)
    return Response(serializer.data)
  
  def retrieve(self, request, pk):
    data = IdeaValidation.objects.get(id = pk)
    serializer = self.get_serializer(data, many = False)
    return Response(serializer.data)
  
  def get_permissions(self):
        # Define custom permissions for each method
        if self.action == 'list':  # GET /yourmodel/
            return [IsAuthenticated()]
        elif self.action == 'create':  # POST /yourmodel/
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]