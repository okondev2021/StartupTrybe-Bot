from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import IdeaValidation
from rest_framework.permissions import IsAuthenticated, AllowAny
from . serializers import IdeaValidationSerializer
from .utility import generate_response
from rest_framework.exceptions import APIException
import threading

# Create your views here.

class TimeoutException(APIException):
  status_code = status.HTTP_408_REQUEST_TIMEOUT
  default_detail = 'The request timed out.'

# Thread wrapper to allow timeouts
class ResponseThread(threading.Thread):
    def __init__(self, user_idea, user_target_market):
        super().__init__()
        self.user_idea = user_idea
        self.user_target_market = user_target_market
        self.result = None
        self.exception = None

    def run(self):
        try:
            # Generate response (the actual process you're trying to time)
            self.result = generate_response(self.user_idea, self.user_target_market)
        except Exception as e:
            self.exception = e

class Validator(viewsets.ModelViewSet):
  queryset = IdeaValidation.objects.all()
  serializer_class = IdeaValidationSerializer

  def create(self, request):
    # Timeout period (in seconds)
    timeout = 30
    try:
      data = request.data

      # Create a new thread to run the bot response
      thread = ResponseThread(request.data['user_idea'], request.data['user_target_market'])
      thread.start()

      # Wait for the thread to finish or timeout
      thread.join(timeout)

      # If the thread is still alive after the timeout, raise TimeoutException
      if thread.is_alive():
          raise TimeoutException()

      # Check if any exception occurred in the thread
      if thread.exception:
          raise thread.exception

      bot_response = thread.result

      # Check if user is authenticated
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
    except TimeoutException:
        return Response({"error": "The request timed out."}, status=status.HTTP_408_REQUEST_TIMEOUT)

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