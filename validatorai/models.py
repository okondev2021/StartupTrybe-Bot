from django.db import models
from userinfo.models import CustomUser

# Create your models here.

class IdeaValidation(models.Model):
    user_idea = models.TextField(default="")
    user_target_market = models.CharField(max_length=200)
    bot_response = models.TextField()
    user_info = models.ForeignKey(CustomUser, on_delete=models.Case, related_name="user_idea_validation")
    time_stamp = models.DateTimeField(auto_now_add=True)
