from django.conf import settings

BASE_TEMPLATE = getattr(settings, "BASE_TEMPLATE", "base.html")
TEMPLATE_THEME_DIR = getattr(settings, "TEMPLATE_THEME_DIR", "base")

AVATAR_MAX_FILE_SIZE = getattr(settings, "AVATAR_MAX_FILE_SIZE", 5)
AVATAR_MAX_WIDTH = getattr(settings, "AVATAR_MAX_FILE_SIZE", 250)
AVATAR_MAX_HEIGHT = getattr(settings, "AVATAR_MAX_FILE_SIZE", 250)
AVATAR_DEFAULT_QUALITY = getattr(settings, "AVATAR_DEFAULT_QUALITY", 75)
