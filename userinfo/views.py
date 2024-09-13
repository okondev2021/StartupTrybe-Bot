from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .models import CustomUser

# Create your views here.

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data = data, many = False)
        if serializer.is_valid():
            serializer.save()

            # GET NEW USER FROM DB AND CREATE TOKEN FOR AUTHENTICATION.
            user = CustomUser.objects.get(email = data['email'])
            refresh = RefreshToken.for_user(user)

            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({"message" : "Account Created Successfully", 'Token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    







        



        

