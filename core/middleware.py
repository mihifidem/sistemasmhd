from django.conf import settings
from django.utils import translation


class DefaultSpanishLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user has explicitly selected a language via cookie
        has_language_cookie = bool(request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME))

        # If the user has not explicitly selected a language, force project default.
        if not has_language_cookie:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE

        return self.get_response(request)
