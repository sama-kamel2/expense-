from django.utils import translation

from .models import Profile
from .translations import (
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
    SUPPORTED_LANGUAGES,
    THEMES,
)

COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def get_profile(user, cookie_lang=None, cookie_theme=None):
    """Return the user's Profile, creating it on first use."""
    defaults = {
        "language": cookie_lang if cookie_lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE,
        "theme": cookie_theme if cookie_theme in THEMES else DEFAULT_THEME,
    }
    profile, _ = Profile.objects.get_or_create(user=user, defaults=defaults)
    return profile


class UserPreferencesMiddleware:
    """
    Decides the language + theme for every request:
      * logged-in user  -> saved Profile (follows the user everywhere)
      * anonymous user  -> `lang` / `theme` cookies (login & register pages)
    Also activates the language so Django's own texts (form errors,
    month names, ...) match the chosen language.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookie_lang = request.COOKIES.get("lang")
        cookie_theme = request.COOKIES.get("theme")

        profile = None
        if request.user.is_authenticated:
            profile = get_profile(request.user, cookie_lang, cookie_theme)
            lang, theme = profile.language, profile.theme
        else:
            lang, theme = cookie_lang, cookie_theme

        if lang not in SUPPORTED_LANGUAGES:
            lang = DEFAULT_LANGUAGE
        if theme not in THEMES:
            theme = DEFAULT_THEME

        request.LANG = lang
        request.THEME = theme
        request.DIR = SUPPORTED_LANGUAGES[lang]["dir"]
        translation.activate(lang)

        response = self.get_response(request)

        # Keep the cookies in sync so the login page (after logout) still
        # shows the language/theme the user picked.
        if profile is not None:
            if cookie_lang != profile.language:
                response.set_cookie("lang", profile.language, max_age=COOKIE_MAX_AGE, samesite="Lax")
            if cookie_theme != profile.theme:
                response.set_cookie("theme", profile.theme, max_age=COOKIE_MAX_AGE, samesite="Lax")

        translation.deactivate()
        return response
