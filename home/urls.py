from . import views
from django.urls import path
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('', views.home.as_view(), name="homepage"),
    path('plan', views.timetable.as_view(), name="timetable"),
    path('wybierz-kierunek', views.chooseField.as_view(), name="chooser-field"),
    path('wybierz-grupe', views.chooseGroup.as_view(), name="chooser-group"),
    path('poradnik', views.tutorial.as_view(), name="tutorial"),
    path('o-nas', views.about.as_view(), name="about")
]