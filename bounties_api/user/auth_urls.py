from django.conf.urls import url
from user import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^settings/$', views.SettingsView.as_view()),
]
