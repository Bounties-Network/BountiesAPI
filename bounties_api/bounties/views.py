import copy
from django.http import HttpResponseBadRequest
from django.contrib.sitemaps import views as django_sitemaps_views


def custom_sitemap_index(request, sitemaps, template_name='sitemap_index.xml', content_type='application/xml',
                         sitemap_url_name='django.contrib.sitemaps.views.sitemap'):
    platform = request.GET.get('platform', None)
    platform_in = request.GET.get('platform__in', None)
    url = request.GET.get('domain', None)

    if not domain:
        return HttpResponseBadRequest(content='must pass in url as a querystring argument')

    platform_filters = ''
    platform_selection = platform or platform_in
    if platform_selection:
        platform_filters = platform_selection.split(',')

    sitemaps_copy = copy.deepcopy(sitemaps)
    for section, site in sitemaps_copy.items():
        if callable(site):
            sitemaps_copy[section] = site(platform_filters=platform_filters, domain=domain, name=domain)

    return django_sitemaps_views.index(request, template_name, content_type, sitemaps, sitemap_url_name)

