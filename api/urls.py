# api/urls.py
from django.urls import path
from .views import MapImagesView

urlpatterns = [
    path('images/', MapImagesView.as_view(), name='location-images'),
]
