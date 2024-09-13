from rest_framework import serializers
from .models import IdeaValidation

class IdeaValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaValidation
        fields = '__all__'
        
        
