"""PlanProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler400, handler403, handler404, handler500
from home import views

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler400 = 'home.views.error400'
handler403 = 'home.views.error403'
handler404 = 'home.views.error404'
handler500 = 'home.views.error500'