# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG = 'en_US'  # can be en_US, fr_FR, ...
ANDROID_ID = None
GOOGLE_LOGIN = None
GOOGLE_PASSWORD = None
AUTH_TOKEN = None

# force the user to edit this file
if any([obj is None for obj in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise RuntimeError("config.py not updated")
