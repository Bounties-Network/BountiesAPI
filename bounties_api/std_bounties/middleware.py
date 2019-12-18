import datetime
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from bleach import clean


class SanitizeDescriptionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "bounty" in request.path:
            if hasattr(response, 'data'):
                description = response.data.get('description')
                if description:
                    response.data['description'] = clean(description)

        return response
