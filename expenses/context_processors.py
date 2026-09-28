from .translations import DEFAULT_LANGUAGE, DEFAULT_THEME, SUPPORTED_LANGUAGES


def preferences(request):
    """Expose language / direction / theme to every template."""
    lang = getattr(request, "LANG", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return {
        "LANG": lang,
        "DIR": SUPPORTED_LANGUAGES[lang]["dir"],
        "THEME": getattr(request, "THEME", DEFAULT_THEME),
        "LANGUAGES": [(code, info["name"]) for code, info in SUPPORTED_LANGUAGES.items()],
        "CURRENT_LANG_NAME": SUPPORTED_LANGUAGES[lang]["name"],
    }
