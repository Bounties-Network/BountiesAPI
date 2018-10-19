"""helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bounties.views import custom_sitemap_index
from bounties.sitemaps import BountyMap, ProfileMap, StaticMap

sitemaps = {
    'BountyMap': BountyMap,
    'ProfileMap': ProfileMap,
    'StaticMap': StaticMap
}

urlpatterns = [
    url(r'^sitemap\.xml$', custom_sitemap_index,
        {'sitemaps': sitemaps}, name='custom_sitemap_index'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('user.auth_urls', namespace='auth')),
    url(r'^user/', include('user.user_urls', namespace='user')),
    url(r'^notification/', include('notifications.urls', namespace='notification')),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="docs"),
    url(r'^analytics/', include('analytics.urls', namespace='analytics')),
    url(r'^', include('std_bounties.urls', namespace='std_bounties')),
    url(r'^swagger', schema_view, name="docs")
]
