from django.conf.urls import url
from authentication import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    url(r'^$', views.UserView.as_view()),
    url(r'^(?P<public_address>\w+)/nonce/$', views.Nonce.as_view()),
    url(r'^(?P<public_address>\w+)/profile/$', views.UserProfile.as_view()),
]
