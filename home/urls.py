from . import views
from django.urls import path

urlpatterns = [
    path('', views.home.as_view(), name="homepage"),
    path('plan', views.timetable.as_view(), name="timetable"),
]