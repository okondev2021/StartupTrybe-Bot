from rest_framework import serializers
from . models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, data):
        user = CustomUser(
            full_name = data['full_name'], 
            email = data['email'], 
        )
        user.set_password(data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        userInfo = CustomUser.objects.get(email = user.email)
        token['full_name'] = userInfo.full_name
        # ...

        return token