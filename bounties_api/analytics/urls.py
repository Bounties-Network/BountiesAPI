from django.conf.urls import url
from .views import TimelineBounties

urlpatterns = [
    url(r'^', TimelineBounties.as_view())
]
