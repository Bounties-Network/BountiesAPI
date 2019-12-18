import datetime
import json
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from bleach import clean


class SanitizeDescriptionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "bounty" in request.path:
            content = json.loads(response.content.decode('utf-8'))
            description = content.get('description')
            if description:
                response.data['description'] = clean(description)

        return response
