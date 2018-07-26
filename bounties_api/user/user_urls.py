from user import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'^languages', views.LanguageViewSet)

urlpatterns = [
    url(r'^$', views.UserView.as_view()),
    url(r'^settings/$', views.SettingsView.as_view()),
    url(r'^(?P<public_address>\w+)/profile/$', views.UserProfile.as_view()),
    url(r'^(?P<public_address>\w+)/info/$', views.UserInfo.as_view()),
    url(r'^', include(router.urls)),
]
