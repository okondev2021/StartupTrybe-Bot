import json

from django.http import StreamingHttpResponse

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import IdeaValidation
from . serializers import IdeaValidationSerializer
from .utility import generate_response




class Validator(viewsets.ModelViewSet):
  queryset = IdeaValidation.objects.all()
  serializer_class = IdeaValidationSerializer

  def create(self, request):
    data = request.data

    combined_response = list()

    def my_iterator(stream):
      for chunk in stream:
        event_data = {
          "message": chunk.text
        }
        combined_response.append(chunk.text)

        yield f"data: {json.dumps(event_data)}\n\n"


    stream = generate_response(data['user_idea'], data['user_target_market'])
    # Check if user is authenticated
    if request.user.is_authenticated:

      # Create a stream for real-time response
      response = StreamingHttpResponse(my_iterator(stream), content_type="text/event-stream")

      # After streaming completes, process and save data
      full_bot_response = "".join(combined_response)  # Combine accumulated data into one string

      data['bot_response'] = full_bot_response
      data['user_info'] = request.user.id

      serializer = self.get_serializer(data = data, many=False)
      if serializer.is_valid():
        serializer.save()
        return response
      else:
        return Response({"error": "Error with validation"}, status=status.HTTP_400_BAD_REQUEST)
    else:
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