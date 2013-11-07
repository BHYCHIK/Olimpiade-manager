from common.api import ApiUser
import settings
from django.core.urlresolvers import resolve

class ApiMiddleware(object):
    def process_request(self, request):
        if request.path.startswith(settings.MEDIA_URL) or not resolve(request.path):
            return None
        api_user = ApiUser(request)
        request.api_user = api_user
        return None
