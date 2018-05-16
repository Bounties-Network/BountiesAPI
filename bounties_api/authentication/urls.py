from django.conf.urls import url
from authentication import views


urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^user/$', views.UserView.as_view()),
    url(r'^user/(?P<address>\w+)/nonce/$', views.Nonce.as_view()),
]
