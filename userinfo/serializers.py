from rest_framework import serializers
from . models import CustomUser

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
