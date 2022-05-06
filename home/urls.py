from . import views
from django.urls import path

urlpatterns = [
    path('', views.index.as_view(), name="homepage"),
]