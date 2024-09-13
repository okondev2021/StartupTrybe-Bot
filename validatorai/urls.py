from django.urls import path
from . views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'validator', Validator, basename='validator')

urlpatterns = router.urls