from django.conf.urls import url
from user import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'^languages', views.LanguageViewSet)

urlpatterns = [
    url(r'^$', views.UserView.as_view()),
    url(r'^(?P<public_address>\w+)/nonce/$', views.Nonce.as_view()),
    url(r'^(?P<public_address>\w+)/profile/$', views.UserProfile.as_view()),
    url(r'^', include(router.urls)),
]
