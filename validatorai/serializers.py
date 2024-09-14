from rest_framework import serializers
from .models import IdeaValidation

class IdeaValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaValidation
        fields = '__all__'

    # def create(self, data):
    #     idea = IdeaValidation(
    #         user_idea = data['user_idea'],
    #         user_target_market = data['user_target_market'],
    #         bot_response = data['bot_response'],
    #         user_info = data['user_info']
    #     )
    #     idea.save()
    #     return idea

        
        
