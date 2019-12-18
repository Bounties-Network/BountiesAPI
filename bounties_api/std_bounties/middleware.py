import datetime
import json
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from bleach import clean
import logging

logger = logging.getLogger('django')

class SanitizeDescriptionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "bounty" in request.path:
            content = json.loads(response.content.decode('utf-8'))
            description = content.get('description')
            logging.info('description: %s', description)
            if description:
                new_description = clean(description)
                content['description'] = new_description
                logging.info('new_description: %s', new_description)
                logging.info('new_content: %s', content)
                response.content = json.dumps(content)

        return response
