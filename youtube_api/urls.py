"""
URL configuration for youtube_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from account import views as account_views 
from youtube_helper import views as youtube_helper_views

urlpatterns = [
    path('', account_views.landing_page, name='landing_page'),
    path('admin/', admin.site.urls),
    path('home/', youtube_helper_views.home, name='home'), 
    path('signup/', account_views.signup, name='signup'),
    path('login/', account_views.log_in, name='login'),
    path('logout/', account_views.log_out, name='logout'),
    path('downloader/', youtube_helper_views.downloader, name='downloader'),
    path('transcriber/',  youtube_helper_views.transcriber, name='transcriber')
]

