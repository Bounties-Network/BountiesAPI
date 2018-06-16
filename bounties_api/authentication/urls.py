from django.conf.urls import url
from authentication import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    url(r'^user/$', views.UserView.as_view()),
    url(r'^user/(?P<public_address>\w+)/nonce/$', views.Nonce.as_view()),
    url(r'^user/(?P<public_address>\w+)/profile/$', views.UserProfile.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^settings/$', views.SettingsView.as_view()),
]
