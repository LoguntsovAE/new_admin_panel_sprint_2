from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CinemaGenericViewSet

router = SimpleRouter()
router.register('movies', CinemaGenericViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
]
