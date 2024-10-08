import json
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import IdeaValidation
from . serializers import IdeaValidationSerializer
from .utility import generate_response
import markdown


class Validator(viewsets.ModelViewSet):
  queryset = IdeaValidation.objects.all()
  serializer_class = IdeaValidationSerializer

  def create(self, request):

    data = request.data

    total_message = []

    def my_iterator(stream):
      for chunk in stream:
        total_message.append(chunk.text)
        event_data = {"message": chunk.text}
        yield json.dumps(event_data)

      # this will run after the steam has been exhausted, and the user is authenticated
      if request.user.is_authenticated:
        response_html_content = markdown.markdown("".join(total_message))
        formatted_response_html_content = response_html_content.replace('\n', '')

        data["bot_response"] = formatted_response_html_content
        data["user_info"] = request.user.id

        serializer = self.get_serializer(data=data, many=False)
        if serializer.is_valid():
          serializer.save()

    # this will return a streaming response if the user is authenticated or not
    stream = generate_response(data["user_idea"], data["user_target_market"])
    return StreamingHttpResponse(my_iterator(stream), content_type="text/event-stream")

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