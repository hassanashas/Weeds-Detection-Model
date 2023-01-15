"""imageNetProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path 
from firstApp import views
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('index', views.index, name = 'index'),
    re_path('history', views.history, name='history'), 
    re_path('predictImage', views.predictImage, name='predictImage'),
    re_path('login', views.login, name='login'),
    re_path('logout', views.logout, name='logout'),
    re_path("record/", views.photo_record, name="record"),
    re_path("comparison_page/", views.comparison_data, name="comparison_page"),
    re_path("get_comparison_photo/", views.get_comparison_photo, name="get_comparison_photo"),
    # re_path('', views.login, name="login_go"),
    # re_path('', views.login_submit, name='Home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
