from django.conf.urls import url
from .views import TimelineBounties, RecordPageView

urlpatterns = [
    url(r'^ping/$', RecordPageView.as_view()),
    url(r'^', TimelineBounties.as_view())
]
