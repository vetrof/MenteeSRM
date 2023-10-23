from django.urls import path, include
from rest_framework import routers
from .views import lessonsApiViewSet

router = routers.DefaultRouter()
router.register('lesson_api_set', lessonsApiViewSet)

urlpatterns = router.urls

